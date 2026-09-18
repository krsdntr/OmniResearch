#!/usr/bin/env python3
"""
OmniResearch Provenance & Integrity Recorder
Zero-dependency CLI tool to compute SHA-256 checksums of input datasets, record script hashes,
lock preregistered hypotheses, and maintain 05_artifacts/provenance/manifest.json.
"""

import argparse
import hashlib
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

def compute_sha256(file_path: Path) -> str:
    """Compute SHA-256 checksum of a file in streaming chunks."""
    if not file_path.exists():
        return f"ERROR: File not found ({file_path})"
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    return sha256.hexdigest()

def lock_preregistration(hyp_file: str, receipt_file: str = "00_meta/preregistration_receipt.json"):
    hyp_p = Path(hyp_file).resolve()
    receipt_p = Path(receipt_file).resolve()

    if not hyp_p.exists():
        print(f"[ERROR] Hypothesis file not found: {hyp_file}")
        sys.exit(1)

    hyp_hash = compute_sha256(hyp_p)
    receipt_data = {
        "status": "LOCKED_PRE_ANALYSIS",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "hypothesis_file": str(hyp_p.name),
        "hypothesis_sha256": hyp_hash,
        "tamper_proof_guideline": "Do not modify 00_meta/hypothesis_matrix.md after locking without logging an amendment.",
        "environment": {
            "os": platform.system(),
            "python_version": platform.python_version()
        }
    }

    receipt_p.parent.mkdir(parents=True, exist_ok=True)
    with open(receipt_p, "w", encoding="utf-8") as f:
        json.dump(receipt_data, f, indent=2)

    print(f"[OK] Preregistration locked successfully!")
    print(f"     Target: {hyp_p.name}")
    print(f"     SHA-256: {hyp_hash}")
    print(f"     Receipt: {receipt_p.as_posix()}")

def record_provenance(
    artifact_path: str,
    script_path: str,
    input_paths: list[str],
    parameters: dict | None = None,
    manifest_path: str = "05_artifacts/provenance/manifest.json"
):
    manifest_file = Path(manifest_path).resolve()
    manifest_file.parent.mkdir(parents=True, exist_ok=True)

    records = []
    if manifest_file.exists():
        try:
            with open(manifest_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    records = data
                elif isinstance(data, dict) and "records" in data:
                    records = data["records"]
        except Exception:
            records = []

    art_p = Path(artifact_path)
    scr_p = Path(script_path)

    input_hashes = []
    for inp in input_paths:
        inp_p = Path(inp)
        input_hashes.append({
            "path": str(inp_p.as_posix()),
            "sha256": compute_sha256(inp_p)
        })

    record = {
        "artifact_id": str(art_p.name),
        "artifact_path": str(art_p.as_posix()),
        "artifact_sha256": compute_sha256(art_p) if art_p.exists() else "NOT_YET_CREATED",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "source_script": str(scr_p.as_posix()),
        "script_sha256": compute_sha256(scr_p) if scr_p.exists() else "UNKNOWN",
        "input_datasets": input_hashes,
        "parameters": parameters or {},
        "environment": {
            "os": platform.system(),
            "os_release": platform.release(),
            "machine": platform.machine(),
            "python_version": platform.python_version()
        }
    }

    # Replace existing record for the same artifact or append
    records = [r for r in records if r.get("artifact_id") != record["artifact_id"]]
    records.append(record)

    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump({"schema_version": "1.0.0", "records": records}, f, indent=2)

    print(f"[OK] Provenance receipt recorded for '{art_p.name}' in {manifest_file.name}")
    print(f"    Script Hash: {record['script_sha256'][:12]}...")
    for inp in input_hashes:
        print(f"    Input: {inp['path']} (SHA: {inp['sha256'][:12]}...)")

def main():
    parser = argparse.ArgumentParser(description="Record artifact provenance or lock preregistered hypotheses.")
    parser.add_argument("--lock-preregistration", metavar="HYPOTHESIS_FILE", help="Lock hypothesis matrix before empirical runs")
    parser.add_argument("--receipt", default="00_meta/preregistration_receipt.json", help="Receipt output for locked preregistration")
    parser.add_argument("--artifact", help="Path to generated figure, table, or output artifact")
    parser.add_argument("--script", help="Path to the source script that created the artifact")
    parser.add_argument("--inputs", nargs="+", default=[], help="Paths to input dataset(s) used")
    parser.add_argument("--params", default="{}", help="JSON string of parameters/hyperparameters")
    parser.add_argument("--manifest", default="05_artifacts/provenance/manifest.json", help="Manifest output path")

    args = parser.parse_args()

    if args.lock_preregistration:
        lock_preregistration(args.lock_preregistration, args.receipt)
        return

    if not args.artifact or not args.script:
        parser.error("Both --artifact and --script are required when recording artifact provenance.")

    try:
        params_dict = json.loads(args.params)
    except Exception:
        params_dict = {"raw_params": args.params}

    record_provenance(
        artifact_path=args.artifact,
        script_path=args.script,
        input_paths=args.inputs,
        parameters=params_dict,
        manifest_path=args.manifest
    )

if __name__ == "__main__":
    main()
