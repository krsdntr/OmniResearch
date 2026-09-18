# AGENTS.md: Universal Instructions for Autonomous AI Agents

This repository operates under the **OmniResearch Scientist Protocol**. Any autonomous AI agent (OpenAI Codex, GitHub Copilot Workspace, Open Interpreter, Aider, Devv, or custom LLM runners) MUST follow these operational guidelines:

## 1. Directory Scaffolding & FAIR Structure
All projects must strictly adhere to the following directory layout:
- `00_meta/`: Research question, hypothesis matrix, decision log.
- `01_data/raw/`: Raw input data (IMMUTABLE). Never modify or delete files here.
- `01_data/interim/`: Intermediate transformations.
- `01_data/processed/`: Analysis-ready normalized tables/matrices.
- `02_methodology/`: Statistical analysis plan, formal protocol specifications.
- `03_src/`: Source code organized by language (`python/`, `r/`, `julia/`, `cpp/`).
- `04_experiments/`: Computational runs, notebooks, and model checkpoints.
- `05_artifacts/`: Figures (vector/300 DPI), tables, and `provenance/manifest.json`.
- `06_reports/`: Formal synthesis documents, LaTeX/Typst papers, summaries.

## 2. Quantitative & Analytical Standards
- **Zero Hallucination of Data**: Never invent data rows, parameters, or citations.
- **Explicit Random Seeds**: All stochastic processes (Monte Carlo, ML cross-validation, bootstrap) must fix seeds (e.g., `seed=42`).
- **Power & Assumptions**: Always check distributional assumptions (normality, collinearity, heteroskedasticity) before reporting p-values.
- **Provenance Receipts**: Every output artifact in `05_artifacts/` must have a corresponding entry in `05_artifacts/provenance/manifest.json` generated using `.agents/skills/research-scientist/scripts/record_provenance.py`.

## 3. Polyglot Toolchains
- **Python**: Run via `python` or `uv run`.
- **R**: Run via `Rscript`.
- **Julia**: Run via `julia --project`.
- **C/C++**: Compile with optimization flags (`-O3 -march=native -Wall`).
