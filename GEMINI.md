# Gemini / Google Antigravity Configuration for Scientific Research

You are augmented with the **OmniResearch Scientist Skill** located at `.agents/skills/research-scientist/`.

## Activation & Behavior
- Whenever the user asks to analyze data, run an experiment, formulate hypotheses, test statistical models, or synthesize scientific findings:
  1. Always consult `.agents/skills/research-scientist/SKILL.md`.
  2. Adhere strictly to the rules in `.agents/skills/research-scientist/rules/scientific_integrity.md` and `data_provenance.md`.
  3. Ensure raw data in `01_data/raw/` is never modified in place.
  4. Always pair any empirical result with uncertainty estimates (confidence intervals, error bars, p-values with effect sizes).
  5. Automatically register artifact lineage using `python .agents/skills/research-scientist/scripts/record_provenance.py`.

## Tool Usage
- When setting up environments, prioritize reproducible package management (`uv` for Python, `renv` for R, `Project.toml` for Julia).
- For figures, generate publication-grade vector graphics (PDF/SVG) or high-res PNG (300 DPI) using colorblind-friendly palettes.
