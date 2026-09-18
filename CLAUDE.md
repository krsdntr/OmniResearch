# Claude Code Configuration: OmniResearch Scientist Workbench

This repository functions as a dedicated Scientific Research Environment governed by `.agents/skills/research-scientist/`.

## Core Commands
- `/scaffold` : Run `python .agents/skills/research-scientist/scripts/scaffold_project.py .` to initialize directory tree.
- `/check-data` : Inspect `01_data/raw/` for missing values, distributions, types, and compute SHA-256 hashes.
- `/provenance` : Run `python .agents/skills/research-scientist/scripts/record_provenance.py` after generating any artifact.
- `/toolchains` : Run `python .agents/skills/research-scientist/scripts/validate_toolchains.py` to check system compilers and interpreters.

## Methodological Guardrails
- **No P-Hacking**: Never run multiple exploratory regressions and present only significant ones without correction (Bonferroni / FDR).
- **Data Quarantine**: `01_data/raw/` is read-only. Transform into `01_data/interim/` or `01_data/processed/`.
- **Always Quantify Uncertainty**: Never state point estimates alone; include 95% CIs or standard errors.
- **Reproducibility**: Every script in `03_src/` must be deterministic with explicit random seeds.
