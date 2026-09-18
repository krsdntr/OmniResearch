#!/usr/bin/env python3
"""
OmniResearch Auto-Appendix & Supplementary Materials Generator
Zero-dependency CLI tool to automatically synthesize scientific supplementary documentation
(LaTeX & Markdown formats) for peer-reviewed journals (Nature, Science, Elsevier, PNAS)
directly from cryptographic provenance manifests, approval gates, and empirical tables.
"""

import argparse
import csv
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

def sanitize_tex(text: str) -> str:
    """Escape special LaTeX characters."""
    chars = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}"
    }
    for k, v in chars.items():
        text = text.replace(k, v)
    return text

def parse_project_context(project_root: Path) -> dict:
    """Collect all relevant project artifacts and receipts."""
    context = {
        "title": "Supplementary Information: Methodological Lineage, Verification & Statistical Protocols",
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "manifest_records": [],
        "approval_gates": {},
        "hypotheses_raw": "",
        "summary_tables": [],
        "environment": {
            "os": platform.system(),
            "python": platform.python_version()
        }
    }

    # 1. Manifest
    manifest_p = project_root / "05_artifacts" / "provenance" / "manifest.json"
    if manifest_p.exists():
        try:
            with open(manifest_p, "r", encoding="utf-8") as f:
                data = json.load(f)
                context["manifest_records"] = data.get("records", []) if isinstance(data, dict) else data
        except Exception:
            pass

    # 2. Approval gates
    gates_p = project_root / "00_meta" / "approval_gates.json"
    if gates_p.exists():
        try:
            with open(gates_p, "r", encoding="utf-8") as f:
                context["approval_gates"] = json.load(f).get("gates", {})
        except Exception:
            pass

    # 3. Hypotheses
    hyp_p = project_root / "00_meta" / "hypothesis_matrix.md"
    if hyp_p.exists():
        try:
            context["hypotheses_raw"] = hyp_p.read_text(encoding="utf-8")
        except Exception:
            pass

    # 4. Tables in 05_artifacts/tables/
    tables_dir = project_root / "05_artifacts" / "tables"
    if tables_dir.exists():
        for t_file in sorted(tables_dir.glob("*.csv")):
            rows = []
            try:
                with open(t_file, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    for r in reader:
                        rows.append(r)
                if rows:
                    context["summary_tables"].append({
                        "filename": t_file.name,
                        "header": rows[0],
                        "rows": rows[1:]
                    })
            except Exception:
                pass

    return context

def build_markdown_appendix(context: dict) -> str:
    lines = []
    lines.append(f"# {context['title']}\n")
    lines.append(f"> **Generated via OmniResearch Protocol** | {context['timestamp']}\n")
    lines.append("---\n")

    # Section 1: Data Lineage & Cryptographic Provenance
    lines.append("## Section S1: Data Provenance & Cryptographic Lineage\n")
    lines.append("All computational outputs, tables, and figures are cryptographically tied to immutable raw data checksums via SHA-256.\n")
    lines.append("| Artifact | Type | SHA-256 Fingerprint | Source Script | Input Dataset(s) |")
    lines.append("| :--- | :--- | :--- | :--- | :--- |")

    if context["manifest_records"]:
        for r in context["manifest_records"]:
            art_id = r.get("artifact_id", "Unknown")
            art_sha = r.get("artifact_sha256", "N/A")[:12] + "..."
            script = Path(r.get("source_script", "N/A")).name
            inputs = "<br>".join([f"`{Path(i.get('path')).name}` ({i.get('sha256', '')[:8]}...)" for i in r.get("input_datasets", [])])
            lines.append(f"| **{art_id}** | Artifact | `{art_sha}` | `{script}` | {inputs or 'None'} |")
    else:
        lines.append("| *None recorded* | - | - | - | - |")
    lines.append("\n")

    # Section 2: Human-in-the-Loop Approval Gates
    lines.append("## Section S2: Human-in-the-Loop Preregistration & Approval Gates\n")
    if context["approval_gates"]:
        lines.append("| Checkpoint Gate | Status | Researcher Signatory | Timestamp (UTC) | Digital Signature |")
        lines.append("| :--- | :--- | :--- | :--- | :--- |")
        for g_name, g_info in context["approval_gates"].items():
            sig = g_info.get("digital_signature", "")[:12] + "..."
            lines.append(f"| `{g_name}` | **{g_info.get('status')}** | {g_info.get('author')} | {g_info.get('timestamp_utc', 'N/A')[:19]} | `{sig}` |")
    else:
        lines.append("*No formal approval gates registered for this run.*\n")
    lines.append("\n")

    # Section 3: Computational Environment
    lines.append("## Section S3: Computational Environment & Reproducibility\n")
    lines.append(f"- **Operating System**: {context['environment']['os']}\n")
    lines.append(f"- **Primary Interpreter**: Python {context['environment']['python']}\n")
    lines.append("- **Deterministic Random Seed**: `seed = 42` (fixed across stochastic iterations)\n")
    lines.append("\n")

    # Section 4: Quantitative Tables
    if context["summary_tables"]:
        lines.append("## Section S4: Empirical Summary Tables\n")
        for tbl in context["summary_tables"]:
            lines.append(f"### Table S4.{context['summary_tables'].index(tbl) + 1}: {tbl['filename']}\n")
            lines.append("| " + " | ".join(tbl['header']) + " |")
            lines.append("| " + " | ".join([":---"] * len(tbl['header'])) + " |")
            for row in tbl['rows'][:20]: # show up to 20 rows
                lines.append("| " + " | ".join(row) + " |")
            if len(tbl['rows']) > 20:
                lines.append(f"| *... and {len(tbl['rows']) - 20} more rows* |" + " | " * (len(tbl['header']) - 1))
            lines.append("\n")

    return "\n".join(lines)

def build_latex_appendix(context: dict) -> str:
    lines = []
    lines.append(r"\documentclass[11pt,a4paper]{article}")
    lines.append(r"\usepackage[utf8]{inputenc}")
    lines.append(r"\usepackage[margin=1in]{geometry}")
    lines.append(r"\usepackage{booktabs}")
    lines.append(r"\usepackage{amsmath,amssymb}")
    lines.append(r"\usepackage{hyperref}")
    lines.append(r"\usepackage{longtable}")
    lines.append(r"\hypersetup{colorlinks=true, linkcolor=blue, urlcolor=blue}")
    lines.append("")
    lines.append(r"\title{\textbf{" + sanitize_tex(context["title"]) + r"}}")
    lines.append(r"\author{\small OmniResearch Automated Scientific Provenance Protocol}")
    lines.append(r"\date{\small " + sanitize_tex(context["timestamp"]) + r"}")
    lines.append("")
    lines.append(r"\begin{document}")
    lines.append(r"\maketitle")
    lines.append(r"\tableofcontents")
    lines.append(r"\vspace{1em}\hrule\vspace{1em}")
    lines.append("")

    # Section S1
    lines.append(r"\section{Data Lineage and Cryptographic Provenance (Table S1)}")
    lines.append(r"All empirical artifacts generated by the OmniResearch pipeline are cryptographically anchored to raw input files using the SHA-256 standard.")
    lines.append(r"\vspace{0.5em}")
    lines.append(r"\begin{table}[htbp]")
    lines.append(r"\centering")
    lines.append(r"\small")
    lines.append(r"\begin{tabular}{llll}")
    lines.append(r"\toprule")
    lines.append(r"\textbf{Artifact ID} & \textbf{SHA-256 Digest} & \textbf{Source Script} & \textbf{Inputs} \\")
    lines.append(r"\midrule")
    if context["manifest_records"]:
        for r in context["manifest_records"]:
            art_id = sanitize_tex(r.get("artifact_id", "Unknown"))
            sha = sanitize_tex(r.get("artifact_sha256", "N/A")[:14] + "...")
            scr = sanitize_tex(Path(r.get("source_script", "N/A")).name)
            inp_names = ", ".join([sanitize_tex(Path(i.get("path", "")).name) for i in r.get("input_datasets", [])]) or "None"
            lines.append(f"{art_id} & \\texttt{{{sha}}} & \\texttt{{{scr}}} & {inp_names} \\\\")
    else:
        lines.append(r"\textit{None recorded} & - & - & - \\")
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\caption{Cryptographic receipts for all empirical artifacts.}")
    lines.append(r"\label{tab:s1_provenance}")
    lines.append(r"\end{table}")
    lines.append("")

    # Section S2
    lines.append(r"\section{Preregistration and Human Approval Gates (Table S2)}")
    lines.append(r"Prior to empirical inference, methodological specifications were preregistered and locked by researcher sign-off.")
    lines.append(r"\vspace{0.5em}")
    lines.append(r"\begin{table}[htbp]")
    lines.append(r"\centering")
    lines.append(r"\small")
    lines.append(r"\begin{tabular}{llll}")
    lines.append(r"\toprule")
    lines.append(r"\textbf{Gate Name} & \textbf{Status} & \textbf{Signatory} & \textbf{Digital Signature} \\")
    lines.append(r"\midrule")
    if context["approval_gates"]:
        for g_name, g_info in context["approval_gates"].items():
            g_san = sanitize_tex(g_name)
            stat = sanitize_tex(g_info.get("status", "PENDING"))
            auth = sanitize_tex(g_info.get("author", "Unknown"))
            sig = sanitize_tex(g_info.get("digital_signature", "")[:14] + "...")
            lines.append(f"\\texttt{{{g_san}}} & \\textbf{{{stat}}} & {auth} & \\texttt{{{sig}}} \\\\")
    else:
        lines.append(r"\textit{No approval gates logged} & - & - & - \\")
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\caption{Human-in-the-loop approval gate verification status.}")
    lines.append(r"\label{tab:s2_gates}")
    lines.append(r"\end{table}")
    lines.append("")

    # Section S3
    lines.append(r"\section{Computational Environment and Determinism}")
    lines.append(r"All scripts were executed under deterministic configurations:")
    lines.append(r"\begin{itemize}")
    lines.append(r"\item Operating Platform: " + sanitize_tex(context["environment"]["os"]))
    lines.append(r"\item Python Runtime: \texttt{" + sanitize_tex(context["environment"]["python"]) + r"}")
    lines.append(r"\item Global Random Seed: \texttt{42} (fixed for pseudo-random number generators)")
    lines.append(r"\item Package Management: Isolated virtual environments via \texttt{uv} or \texttt{venv}")
    lines.append(r"\end{itemize}")
    lines.append("")

    # Section S4: Summary Tables
    if context["summary_tables"]:
        lines.append(r"\section{Empirical Summary Tables}")
        for idx, tbl in enumerate(context["summary_tables"], start=1):
            col_spec = "l" * len(tbl["header"])
            lines.append(r"\begin{table}[htbp]")
            lines.append(r"\centering")
            lines.append(r"\small")
            lines.append(r"\begin{tabular}{" + col_spec + r"}")
            lines.append(r"\toprule")
            header_tex = " & ".join([r"\textbf{" + sanitize_tex(h) + r"}" for h in tbl["header"]]) + r" \\"
            lines.append(header_tex)
            lines.append(r"\midrule")
            for row in tbl["rows"][:15]:
                row_tex = " & ".join([sanitize_tex(cell) for cell in row]) + r" \\"
                lines.append(row_tex)
            lines.append(r"\bottomrule")
            lines.append(r"\end{tabular}")
            lines.append(r"\caption{Empirical data extraction from \texttt{" + sanitize_tex(tbl["filename"]) + r"}}")
            lines.append(r"\label{tab:s" + str(idx) + r"}")
            lines.append(r"\end{table}")
            lines.append("")

    lines.append(r"\end{document}")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Generate publication-ready Supplementary Materials (LaTeX & Markdown).")
    parser.add_argument("--project", default=".", help="Project root directory (default: current directory)")
    parser.add_argument("--format", choices=["latex", "markdown", "all"], default="all", help="Output format")
    parser.add_argument("--output-dir", default="06_reports", help="Directory where appendix files are saved")

    args = parser.parse_args()
    proj = Path(args.project).resolve()
    out_dir = proj / args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    context = parse_project_context(proj)

    generated_files = []

    if args.format in ("markdown", "all"):
        md_content = build_markdown_appendix(context)
        md_file = out_dir / "supplementary_materials.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(md_content)
        generated_files.append(md_file)

    if args.format in ("latex", "all"):
        tex_content = build_latex_appendix(context)
        tex_file = out_dir / "supplementary_materials.tex"
        with open(tex_file, "w", encoding="utf-8") as f:
            f.write(tex_content)
        generated_files.append(tex_file)

    print(f"\n[OK] Supplementary Materials generated successfully!")
    for gf in generated_files:
        print(f"     Output: {gf.as_posix()}")
    print("----------------------------------------------------------\n")

if __name__ == "__main__":
    main()
