#!/usr/bin/env python3
"""
Example Script: Analysis of KR-42 Dose-Response Trial
Zero-dependency script calculating group means, standard deviations, and 95% confidence intervals,
and programmatically recording artifact provenance.
"""

import csv
import math
import os
import subprocess
import sys
from pathlib import Path

def mean(vals):
    return sum(vals) / len(vals)

def std_dev(vals, m):
    variance = sum((x - m) ** 2 for x in vals) / (len(vals) - 1)
    return math.sqrt(variance)

def main():
    base_dir = Path(__file__).resolve().parent.parent.parent
    raw_data = base_dir / "01_data" / "raw" / "dose_response_trial.csv"
    table_out = base_dir / "05_artifacts" / "tables" / "dose_summary.csv"
    manifest_file = base_dir / "05_artifacts" / "provenance" / "manifest.json"

    print(f"[+] Reading raw data from: {raw_data}")

    groups = {}
    with open(raw_data, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dose = float(row["dose_mg"])
            inhibition = float(row["biomarker_inhibition"])
            groups.setdefault(dose, []).append(inhibition)

    table_out.parent.mkdir(parents=True, exist_ok=True)
    summary_rows = []

    print("[+] Calculating dose tiers and 95% confidence intervals:")
    for dose, vals in sorted(groups.items()):
        n = len(vals)
        m = mean(vals)
        sd = std_dev(vals, m) if n > 1 else 0.0
        se = sd / math.sqrt(n) if n > 1 else 0.0
        # t-critical for df=2 (95%) is approximately 4.303
        ci_half = 4.303 * se
        ci_lower = max(0.0, m - ci_half)
        ci_upper = min(1.0, m + ci_half)

        summary_rows.append({
            "dose_mg": dose,
            "sample_size": n,
            "mean_inhibition": round(m, 4),
            "std_dev": round(sd, 4),
            "std_error": round(se, 4),
            "ci_95_lower": round(ci_lower, 4),
            "ci_95_upper": round(ci_upper, 4)
        })
        print(f"    Dose {dose:>5.1f} mg (N={n}): Mean={m:.3f} +/- {se:.3f} [95% CI: {ci_lower:.3f}, {ci_upper:.3f}]")

    with open(table_out, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"[OK] Summary table saved to: {table_out}")

    # Register provenance receipt automatically
    recorder_script = base_dir.parent.parent / ".agents" / "skills" / "research-scientist" / "scripts" / "record_provenance.py"
    if recorder_script.exists():
        subprocess.run([
            sys.executable,
            str(recorder_script),
            "--artifact", str(table_out),
            "--script", str(Path(__file__).resolve()),
            "--inputs", str(raw_data),
            "--params", '{"confidence_level": 0.95, "model": "dose_group_summary"}',
            "--manifest", str(manifest_file)
        ], check=True)

if __name__ == "__main__":
    main()
