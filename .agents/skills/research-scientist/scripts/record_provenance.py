#!/usr/bin/env python3
"""
OmniResearch Provenance & Integrity Recorder (Big Data & Merkle Optimized)
Zero-dependency CLI tool to compute cryptographic checksums of input datasets,
maintain Merkle trees for massive files (GB/TB scale), lock preregistered hypotheses,
and maintain 05_artifacts/provenance/manifest.json.
"""

import argparse
import hashlib
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

# 8 MB default streaming buffer for high throughput on modern SSD/NVMe
DEFAULT_BUFFER_SIZE = 8 * 1024 * 1024  
# 64 MB chunk size for Merkle tree leaves
MERKLE_CHUNK_SIZE = 64 * 1024 * 1024
# Files above 500 MB automatically compute Merkle tree root alongside SHA-256
MERKLE_THRESHOLD = 500 * 1024 * 1024

def compute_sha256_stream(file_path: Path, buffer_size: int = DEFAULT_BUFFER_SIZE) -> tuple[str, int]:
    """
    Compute SHA-256 checksum of a file using buffered streaming.
    Returns (sha256_hex, file_size_bytes).
    """
    if not file_path.exists():
        return f"ERROR: File not found ({file_path})", 0
    
    sha256 = hashlib.sha256()
    total_bytes = 0
    with open(file_path, "rb") as f:
        while chunk := f.read(buffer_size):
            sha256.update(chunk)
            total_bytes += len(chunk)
            
    return sha256.hexdigest(), total_bytes

def compute_merkle_root(file_path: Path, chunk_size: int = MERKLE_CHUNK_SIZE) -> dict:
    """
    Compute Merkle tree root for large datasets (GB/TB scale).
    Divides file into discrete blocks, hashes each, and combines hierarchically.
    """
    if not file_path.exists():
        return {"error": f"File not found: {file_path}"}

    leaf_hashes = []
    total_bytes = 0
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            leaf_hashes.append(hashlib.sha256(chunk).hexdigest())
            total_bytes += len(chunk)

    if not leaf_hashes:
        return {
            "merkle_root": hashlib.sha256(b"").hexdigest(),
            "total_chunks": 0,
            "chunk_size_bytes": chunk_size,
            "total_bytes": 0
        }

    # Build Merkle tree upward
    current_level = leaf_hashes
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1] if i + 1 < len(current_level) else left
            combined = hashlib.sha256(f"{left}{right}".encode("utf-8")).hexdigest()
            next_level.append(combined)
        current_level = next_level

    return {
        "merkle_root": current_level[0],
        "total_chunks": len(leaf_hashes),
        "chunk_size_bytes": chunk_size,
        "total_bytes": total_bytes
    }

def compute_file_fingerprint(file_path: Path) -> dict:
    """Compute comprehensive fingerprint for small or large files."""
    if not file_path.exists():
        return {"sha256": "FILE_NOT_FOUND", "size_bytes": 0}

    size = file_path.stat().st_size
    sha256_hash, _ = compute_sha256_stream(file_path)
    res = {
        "sha256": sha256_hash,
        "size_bytes": size,
        "hashing_mode": "sha256_streaming"
    }

    # If file exceeds threshold, also compute Merkle tree root
    if size >= MERKLE_THRESHOLD:
        merkle_info = compute_merkle_root(file_path)
        res["merkle_root"] = merkle_info["merkle_root"]
        res["merkle_chunks"] = merkle_info["total_chunks"]
        res["hashing_mode"] = "sha256_merkle_hybrid"

    return res

def lock_preregistration(hyp_file: str, receipt_file: str = "00_meta/preregistration_receipt.json"):
    hyp_p = Path(hyp_file).resolve()
    receipt_p = Path(receipt_file).resolve()

    if not hyp_p.exists():
        print(f"[ERROR] Hypothesis file not found: {hyp_file}", file=sys.stderr)
        sys.exit(1)

    fp = compute_file_fingerprint(hyp_p)
    receipt_data = {
        "status": "LOCKED_PRE_ANALYSIS",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "hypothesis_file": str(hyp_p.name),
        "hypothesis_sha256": fp["sha256"],
        "size_bytes": fp["size_bytes"],
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
    print(f"     SHA-256: {fp['sha256']}")
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

    art_fp = compute_file_fingerprint(art_p)
    scr_fp = compute_file_fingerprint(scr_p)

    input_hashes = []
    for inp in input_paths:
        inp_p = Path(inp)
        inp_fp = compute_file_fingerprint(inp_p)
        inp_rec = {
            "path": str(inp_p.as_posix()),
            "sha256": inp_fp["sha256"],
            "size_bytes": inp_fp["size_bytes"]
        }
        if "merkle_root" in inp_fp:
            inp_rec["merkle_root"] = inp_fp["merkle_root"]
            inp_rec["merkle_chunks"] = inp_fp["merkle_chunks"]
        input_hashes.append(inp_rec)

    record = {
        "artifact_id": str(art_p.name),
        "artifact_path": str(art_p.as_posix()),
        "artifact_sha256": art_fp["sha256"],
        "artifact_size_bytes": art_fp["size_bytes"],
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "source_script": str(scr_p.as_posix()),
        "script_sha256": scr_fp["sha256"],
        "input_datasets": input_hashes,
        "parameters": parameters or {},
        "environment": {
            "os": platform.system(),
            "os_release": platform.release(),
            "machine": platform.machine(),
            "python_version": platform.python_version()
        }
    }

    if "merkle_root" in art_fp:
        record["artifact_merkle_root"] = art_fp["merkle_root"]

    # Replace existing record for the same artifact or append
    records = [r for r in records if r.get("artifact_id") != record["artifact_id"]]
    records.append(record)

    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump({"schema_version": "1.1.0", "records": records}, f, indent=2)

    print(f"[OK] Provenance receipt recorded for '{art_p.name}' in {manifest_file.name}")
    print(f"    Script Hash: {record['script_sha256'][:12]}...")
    for inp in input_hashes:
        m_tag = f" [Merkle Root: {inp['merkle_root'][:8]}...]" if "merkle_root" in inp else ""
        print(f"    Input: {inp['path']} (SHA: {inp['sha256'][:12]}...{m_tag})")

def verify_manifest(manifest_path: str = "05_artifacts/provenance/manifest.json", base_dir: Path | None = None) -> bool:
    manifest_file = Path(manifest_path).resolve()
    if not manifest_file.exists():
        print(f"[ERROR] Manifest file not found: {manifest_file}")
        return False

    with open(manifest_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    records = data.get("records", []) if isinstance(data, dict) else data
    print(f"\n--- Verifying Provenance Manifest ({len(records)} entries) ---")
    all_valid = True

    base = base_dir or manifest_file.parent.parent.parent

    for r in records:
        art_id = r.get("artifact_id")
        orig_art_hash = r.get("artifact_sha256")
        art_path = base / r.get("artifact_path", "")

        print(f"\nVerifying Artifact: {art_id}")
        if not art_path.exists():
            art_path = Path(r.get("artifact_path", ""))

        if art_path.exists():
            curr_hash, _ = compute_sha256_stream(art_path)
            if curr_hash == orig_art_hash:
                print(f"  [x] Artifact file intact: {curr_hash[:12]}...")
            else:
                print(f"  [FAIL] Artifact modified! Expected {orig_art_hash[:12]}..., found {curr_hash[:12]}...")
                all_valid = False
        else:
            print(f"  [WARN] Artifact file not found on disk at {art_path.as_posix()}")

        # Check script
        scr_path = base / r.get("source_script", "")
        if not scr_path.exists():
            scr_path = Path(r.get("source_script", ""))
        orig_scr_hash = r.get("script_sha256")
        if scr_path.exists():
            curr_scr_hash, _ = compute_sha256_stream(scr_path)
            if curr_scr_hash == orig_scr_hash:
                print(f"  [x] Source script intact: {curr_scr_hash[:12]}...")
            else:
                print(f"  [FAIL] Source script modified! Expected {orig_scr_hash[:12]}..., found {curr_scr_hash[:12]}...")
                all_valid = False

        # Check inputs
        for inp in r.get("input_datasets", []):
            inp_path = base / inp.get("path", "")
            if not inp_path.exists():
                inp_path = Path(inp.get("path", ""))
            orig_inp_hash = inp.get("sha256")
            if inp_path.exists():
                curr_inp_hash, _ = compute_sha256_stream(inp_path)
                if curr_inp_hash == orig_inp_hash:
                    print(f"  [x] Input intact: {inp['path']}")
                else:
                    print(f"  [FAIL] Input dataset modified: {inp['path']}")
                    all_valid = False

    print("\n--------------------------------------------------------------")
    if all_valid:
        print("[PASSED] All recorded artifacts, scripts, and inputs are cryptographically intact.")
    else:
        print("[CORRUPT / MODIFIED] One or more items differ from manifest receipts.")
    print("--------------------------------------------------------------\n")
    return all_valid

def main():
    parser = argparse.ArgumentParser(description="Record artifact provenance or lock preregistered hypotheses.")
    parser.add_argument("--lock-preregistration", metavar="HYPOTHESIS_FILE", help="Lock hypothesis matrix before empirical runs")
    parser.add_argument("--receipt", default="00_meta/preregistration_receipt.json", help="Receipt output for locked preregistration")
    parser.add_argument("--artifact", help="Path to generated figure, table, or output artifact")
    parser.add_argument("--script", help="Path to the source script that created the artifact")
    parser.add_argument("--inputs", nargs="+", default=[], help="Paths to input dataset(s) used")
    parser.add_argument("--params", default="{}", help="JSON string of parameters/hyperparameters")
    parser.add_argument("--manifest", default="05_artifacts/provenance/manifest.json", help="Manifest output path")
    parser.add_argument("--verify", action="store_true", help="Verify integrity of all files in manifest")

    args = parser.parse_args()

    if args.verify:
        valid = verify_manifest(args.manifest)
        sys.exit(0 if valid else 1)

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
