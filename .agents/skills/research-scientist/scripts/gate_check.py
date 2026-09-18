#!/usr/bin/env python3
"""
OmniResearch Human-in-the-Loop Approval Gate Checker
Zero-dependency CLI tool to enforce researcher approval checkpoints before critical
research phases (hypothesis freeze, final model execution, publication synthesis).
"""

import argparse
import hashlib
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

STANDARD_GATES = {
    "hypothesis-lock": {
        "description": "Preregistration freeze: locks hypothesis matrix and power plan prior to raw data exposure.",
        "prerequisite_files": ["00_meta/hypothesis_matrix.md"]
    },
    "model-specification": {
        "description": "Pre-analysis protocol: locks model specifications, estimators, and alpha thresholds.",
        "prerequisite_files": ["02_methodology/statistical_plan.md"]
    },
    "synthesis-approval": {
        "description": "Publication sign-off: researcher certifies conclusions and adversarial audit before paper drafting.",
        "prerequisite_files": ["05_artifacts/provenance/manifest.json"]
    }
}

def compute_file_sha256(file_path: Path) -> str:
    """Compute SHA-256 of a file if it exists."""
    if not file_path.exists():
        return "MISSING"
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    return sha256.hexdigest()

def get_gates_file(project_root: Path) -> Path:
    return project_root / "00_meta" / "approval_gates.json"

def load_gates(project_root: Path) -> dict:
    gates_file = get_gates_file(project_root)
    if gates_file.exists():
        try:
            with open(gates_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"schema_version": "1.0.0", "gates": {}}
    return {"schema_version": "1.0.0", "gates": {}}

def save_gates(project_root: Path, data: dict):
    gates_file = get_gates_file(project_root)
    gates_file.parent.mkdir(parents=True, exist_ok=True)
    with open(gates_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def lock_gate(project_root: Path, gate_name: str, author: str, notes: str = ""):
    data = load_gates(project_root)
    if "gates" not in data:
        data["gates"] = {}

    gate_info = STANDARD_GATES.get(gate_name, {"description": "Custom research approval checkpoint", "prerequisite_files": []})
    
    # Audit prerequisite files
    prereq_hashes = {}
    for rel_p in gate_info["prerequisite_files"]:
        target_p = project_root / rel_p
        prereq_hashes[rel_p] = compute_file_sha256(target_p)

    timestamp = datetime.now(timezone.utc).isoformat()
    raw_signature = f"{gate_name}|{author}|{timestamp}|{json.dumps(prereq_hashes, sort_keys=True)}"
    digital_signature = hashlib.sha256(raw_signature.encode("utf-8")).hexdigest()

    record = {
        "gate_name": gate_name,
        "status": "APPROVED",
        "author": author,
        "timestamp_utc": timestamp,
        "notes": notes,
        "description": gate_info["description"],
        "prerequisites": prereq_hashes,
        "digital_signature": digital_signature,
        "environment": {
            "os": platform.system(),
            "python_version": platform.python_version()
        }
    }

    data["gates"][gate_name] = record
    save_gates(project_root, data)

    print(f"[OK] Approval Gate '{gate_name}' successfully signed and locked!")
    print(f"     Signatory: {author}")
    print(f"     Signature: {digital_signature[:16]}...")
    print(f"     Recorded in: {get_gates_file(project_root).as_posix()}")

def verify_gate(project_root: Path, gate_name: str, strict: bool = False) -> bool:
    data = load_gates(project_root)
    gates = data.get("gates", {})

    if gate_name not in gates:
        msg = f"[BLOCKED] Approval Gate '{gate_name}' has NOT been signed by a human researcher."
        if strict:
            print(msg, file=sys.stderr)
            print(f"          Action required: python gate_check.py lock --gate {gate_name} --author \"<Your Name>\"", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"[WARN] {msg}")
            return False

    gate_rec = gates[gate_name]
    if gate_rec.get("status") != "APPROVED":
        print(f"[BLOCKED] Approval Gate '{gate_name}' status is {gate_rec.get('status')} (not APPROVED).", file=sys.stderr)
        if strict:
            sys.exit(1)
        return False

    # Check tampering on prerequisites
    for rel_p, orig_hash in gate_rec.get("prerequisites", {}).items():
        curr_hash = compute_file_sha256(project_root / rel_p)
        if curr_hash != orig_hash:
            print(f"[TAMPER WARNING] Prerequisite '{rel_p}' has changed since gate was signed!", file=sys.stderr)
            print(f"                 Original SHA: {orig_hash[:12]}... Current: {curr_hash[:12]}...", file=sys.stderr)
            if strict:
                sys.exit(1)
            return False

    print(f"[PASSED] Approval Gate '{gate_name}' verified. Signed by {gate_rec.get('author')} at {gate_rec.get('timestamp_utc')}")
    return True

def list_gates(project_root: Path):
    data = load_gates(project_root)
    gates = data.get("gates", {})

    print("\n--- OmniResearch Approval Gates Status ---")
    for g_name, g_def in STANDARD_GATES.items():
        if g_name in gates:
            rec = gates[g_name]
            print(f"  [x] {g_name:<22} : APPROVED by {rec.get('author')} ({rec.get('timestamp_utc')})")
        else:
            print(f"  [ ] {g_name:<22} : PENDING APPROVAL - {g_def['description']}")
    print("------------------------------------------\n")

def main():
    parser = argparse.ArgumentParser(description="Manage OmniResearch Human-in-the-Loop Approval Gates.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: lock
    p_lock = subparsers.add_parser("lock", help="Sign and lock an approval gate.")
    p_lock.add_argument("--gate", required=True, choices=list(STANDARD_GATES.keys()) + ["custom"], help="Name of the gate")
    p_lock.add_argument("--author", required=True, help="Human researcher name or ID")
    p_lock.add_argument("--notes", default="", help="Notes or rationale for approval")
    p_lock.add_argument("--project", default=".", help="Project root directory")

    # Subcommand: verify
    p_verify = subparsers.add_parser("verify", help="Verify if a gate is signed and intact.")
    p_verify.add_argument("--gate", required=True, help="Name of the gate to verify")
    p_verify.add_argument("--strict", action="store_true", help="Exit with code 1 if verification fails")
    p_verify.add_argument("--project", default=".", help="Project root directory")

    # Subcommand: list
    p_list = subparsers.add_parser("list", help="List all approval gates status.")
    p_list.add_argument("--project", default=".", help="Project root directory")

    args = parser.parse_args()
    proj = Path(args.project).resolve()

    if args.command == "lock":
        lock_gate(proj, args.gate, args.author, args.notes)
    elif args.command == "verify":
        success = verify_gate(proj, args.gate, strict=args.strict)
        if not success and not args.strict:
            sys.exit(2)
    elif args.command == "list":
        list_gates(proj)

if __name__ == "__main__":
    main()
