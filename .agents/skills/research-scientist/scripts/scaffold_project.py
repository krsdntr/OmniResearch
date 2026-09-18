#!/usr/bin/env python3
"""
OmniResearch Project Scaffolder
Zero-dependency CLI tool to generate a standardized, reproducible, FAIR-compliant scientific research directory tree.
Compatible with Windows, Linux, and macOS.
"""

import argparse
import os
import sys
from pathlib import Path

DIRECTORY_STRUCTURE = {
    "00_meta": "Hypothesis preregistrations, research questions, decision logs, and study protocols.",
    "01_data/raw": "Immutable, read-only external datasets. Never edit files in this folder.",
    "01_data/interim": "Intermediate transformed or cleaned datasets.",
    "01_data/processed": "Analysis-ready datasets used for final modeling.",
    "02_methodology": "Formal statistical plans, experimental specifications, and power analyses.",
    "03_src/python": "Python source code modules and analytical pipelines.",
    "03_src/r": "R scripts and analysis notebooks.",
    "03_src/julia": "Julia simulation models and numerical solvers.",
    "03_src/cpp": "C/C++ performance-critical kernels or simulations.",
    "04_experiments": "Batch runs, exploratory notebooks, and parameter sweeps.",
    "05_artifacts/figures": "Publication-grade figures (300+ DPI, vector SVG/PDF).",
    "05_artifacts/tables": "Summary tables formatted in CSV, Markdown, and LaTeX.",
    "05_artifacts/provenance": "Cryptographic receipts (manifest.json) linking artifacts to inputs.",
    "06_reports": "Manuscript drafts, executive summaries, and presentation slides."
}

GITIGNORE_CONTENT = """# Research Project Git Ignore
# Ignore large/raw data files
01_data/raw/*
!01_data/raw/.gitkeep
01_data/interim/*
!01_data/interim/.gitkeep
01_data/processed/*
!01_data/processed/.gitkeep

# Ignore large binary artifacts/models
*.pt
*.onnx
*.pkl
*.h5
*.parquet
*.tar.gz
*.zip

# Python
__pycache__/
*.py[cod]
.venv/
env/
.pytest_cache/

# R
.Rhistory
.RData
.Rproj.user/

# Julia
Manifest.toml

# OS Files
.DS_Store
Thumbs.db
"""

HYPOTHESIS_TEMPLATE = """# Hypothesis Registration Matrix

| ID | Research Question | Null Hypothesis ($H_0$) | Alternative Hypothesis ($H_1$) | Target Metric | Min. Detectable Effect | Status |
|:---|:------------------|:------------------------|:-------------------------------|:--------------|:-----------------------|:-------|
| H1 | [e.g. Does Treatment X increase outcome Y?] | $\\beta_1 = 0$ (No effect) | $\\beta_1 > 0$ (Positive effect) | Cohen's d / $\\beta$ | $d \\ge 0.35$ | Registered |
"""

STATISTICAL_PLAN_TEMPLATE = """# Formal Statistical Analysis Plan

## 1. Study Design & Population
- **Target Population**:
- **Sampling Strategy**:
- **Sample Size & Power**: Target $N = ...$, Power $(1-\\beta) = 0.80$, $\\alpha = 0.05$.

## 2. Variables
- **Primary Dependent Variable (Outcome)**:
- **Primary Independent Variable (Treatment)**:
- **Covariates / Controls**:

## 3. Primary Analytical Model
- **Model Specification**:
- **Distributional Assumptions & Tests**:
  - Normality of residuals (Shapiro-Wilk / Q-Q)
  - Homoscedasticity (Breusch-Pagan)
  - Multicollinearity (VIF $< 5$)

## 4. Sensitivity & Robustness Checks
- [ ] Specification curve / alternative functional forms
- [ ] Subgroup analysis
- [ ] Placebo / permutation tests
"""

def scaffold_project(target_dir: Path, force: bool = False):
    target_dir = target_dir.resolve()
    print(f"[+] Initializing OmniResearch Workbench at: {target_dir}")

    for rel_path, description in DIRECTORY_STRUCTURE.items():
        dir_path = target_dir / rel_path
        dir_path.mkdir(parents=True, exist_ok=True)
        gitkeep = dir_path / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()
        
        readme = dir_path / "README.md"
        if not readme.exists() or force:
            with open(readme, "w", encoding="utf-8") as f:
                f.write(f"# {os.path.basename(rel_path)}\n\n{description}\n")

    # Create root templates if not present
    gitignore_path = target_dir / ".gitignore"
    if not gitignore_path.exists():
        with open(gitignore_path, "w", encoding="utf-8") as f:
            f.write(GITIGNORE_CONTENT)

    hyp_matrix = target_dir / "00_meta" / "hypothesis_matrix.md"
    if not hyp_matrix.exists() or force:
        with open(hyp_matrix, "w", encoding="utf-8") as f:
            f.write(HYPOTHESIS_TEMPLATE)

    stat_plan = target_dir / "02_methodology" / "statistical_plan.md"
    if not stat_plan.exists() or force:
        with open(stat_plan, "w", encoding="utf-8") as f:
            f.write(STATISTICAL_PLAN_TEMPLATE)

    print("[OK] Scaffolding complete! Structure is FAIR-compliant and ready for analysis.")

def main():
    parser = argparse.ArgumentParser(description="Scaffold an OmniResearch scientific workspace.")
    parser.add_argument("target", nargs="?", default=".", help="Target directory (default: current directory)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing template files")
    args = parser.parse_args()

    scaffold_project(Path(args.target), args.force)

if __name__ == "__main__":
    main()
