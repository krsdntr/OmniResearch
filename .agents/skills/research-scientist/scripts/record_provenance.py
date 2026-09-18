#!/usr/bin/env python3
"""
OmniResearch Provenance Recorder
Zero-dependency CLI tool to compute SHA-256 checksums of input datasets, record script hashes,
capture execution parameters, and update 05_artifacts/provenance/manifest.json.
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
    parser = argparse.ArgumentParser(description="Record artifact provenance receipt.")
    parser.add_argument("--artifact", required=True, help="Path to generated figure, table, or output artifact")
    parser.add_argument("--script", required=True, help="Path to the source script that created the artifact")
    parser.add_argument("--inputs", nargs="+", default=[], help="Paths to input dataset(s) used")
    parser.add_argument("--params", default="{}", help="JSON string of parameters/hyperparameters")
    parser.add_argument("--manifest", default="05_artifacts/provenance/manifest.json", help="Manifest output path")

    args = parser.parse_args()

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
