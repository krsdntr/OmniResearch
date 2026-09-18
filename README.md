# OmniResearch Scientist Workbench

> **Transform any Agentic IDE into a High-Rigor, Polyglot Scientific Research Lab.**

OmniResearch is a universal Agent Skill suite that elevates AI coding environments (Google Antigravity, Claude Code, Cursor, OpenAI Codex, Copilot Workspaces, Open Interpreter, Aider) into a structured scientific workbench.

Instead of writing ungrounded code or hallucinating figures, the agent operates as a **Senior Quantitative Methodologist** adhering to FAIR data principles, preregistered hypotheses, multi-language pipelines, and cryptographic provenance tracing.

---

## 🌟 Core Features

1. **Epistemological Guardrails**:
   - Strictly enforces raw data immutability (`01_data/raw/` is locked and checksummed).
   - Zero tolerance for p-hacking, data leakage, and unadjusted multi-hypothesis testing.
   - Mandates reporting of uncertainty intervals (CIs, SEs) and sensitivity/ablation checks.

2. **5 Methodological Paradigms (`paradigms/`)**:
   - **Experimental & RCT**: Clinical trials, agricultural split-plot, ANOVA/LMM, power analysis.
   - **Causal & Observational**: DiD (staggered), Instrumental Variables (IV), RDD, Survival Analysis.
   - **Computational Simulation**: ODE/PDE solvers, Monte Carlo, molecular dynamics, reaction kinetics.
   - **Machine Learning Empirical**: Strict pre-processing leakage prevention, ablation studies, 5x2cv benchmarks.
   - **Systematic Reviews & Meta-Analyses**: PRISMA 2020 flow, Cochrane RoB, effect pooling, funnel plots.

3. **6 Scientific Data Type Handlers (`data_handlers/`)**:
   - **Tabular & Complex Surveys**: Survey weighting (PSU/strata), MICE multiple imputation.
   - **Spatial & Geospatial**: CRS hygiene, GeoTIFF, Shapefiles, NetCDF, spatial autocorrelation (Moran's I).
   - **Biological Sequences & Molecules**: FASTA, RNA-Seq counts (DESeq2), 3D PDB structures, SMILES.
   - **Signals & Sensor Streams**: EDF (EEG/ECG), acoustic WAV, Nyquist compliance, Fourier & Wavelet transforms.
   - **Text Corpora & Humanities**: Stylometry (Burrows' Delta), Topic Modeling (LDA/BERTopic), Collocations.
   - **Graphs & Networks**: Degree distributions, small-worldness, community detection, centrality metrics.

4. **Cryptographic Provenance Receipts (`05_artifacts/provenance/manifest.json`)**:
   - Automatically records the SHA-256 hash of input datasets, analysis scripts, runtime hyperparameters, and execution environment for every publication-ready figure and table.

5. **Polyglot Execution**:
   - Seamless orchestration across **Python** (`uv`), **R** (`renv`), **Julia** (`Project.toml`), and **C/C++** (`-O3 -march=native`).

---

## 📂 Standard FAIR Workspace Scaffolding

```text
my_project/
├── 00_meta/                  # Hypotheses, preregistrations, decision logs
│   ├── hypothesis_matrix.md  # Formal hypothesis matrix and rejection thresholds
│   └── research_plan.md      # Methodological milestones and timeline
├── 01_data/
│   ├── raw/                  # Immutable raw source data (READ-ONLY)
│   ├── interim/              # Partially transformed intermediate data
│   └── processed/            # Fully cleaned, analysis-ready tables
├── 02_methodology/           # Formal statistical plans and study designs
│   └── statistical_plan.md   # Pre-analysis assumptions and power calculations
├── 03_src/                   # Polyglot analysis scripts (Python, R, Julia, C++)
├── 04_experiments/           # Computational runs, sweeps, and exploratory notebooks
├── 05_artifacts/
│   ├── figures/              # Publication-grade vector/300+ DPI figures
│   ├── tables/               # Formatted results (CSV, Markdown, LaTeX)
│   └── provenance/           # manifest.json cryptographic receipts
└── 06_reports/               # Final synthesis papers (Typst, Quarto, LaTeX, MD)
```

---

## 🧭 Comprehensive Guide: Using with Google Antigravity

Google Antigravity natively detects and activates this skill through [GEMINI.md](file:///d:/kris/Research%20skill/GEMINI.md) and [.agents/skills/research-scientist/SKILL.md](file:///d:/kris/Research%20skill/.agents/skills/research-scientist/SKILL.md). No third-party extensions or complex configurations are required.

### End-to-End Real-World Workflow

```
[1. Deposit Raw Data] ──► [2. Prompt Research Goal] ──► [3. Review Protocol/Plan] ──► [4. Approve & Run] ──► [5. Inspect Manifest]
      (01_data/raw/)             (Natural Language)            (hypothesis_matrix.md)        (Polyglot Engine)        (manifest.json)
```

#### Step 1: Deposit Data into Quarantine
Place your raw data files (`.csv`, `.parquet`, `.fasta`, `.tif`, `.edf`, etc.) directly into `01_data/raw/`.  
> **Rule**: Treat this directory as read-only. Never modify or clean raw data in place.

#### Step 2: Prompt Antigravity with Your Research Goal
Open the chat panel in Antigravity and state your scientific inquiry in plain language. Antigravity will automatically adopt the **Senior Lead Scientist** persona and engage its 5-phase research state machine:
- **Automatic Intake**: Audits data columns, shapes, distributions, and missingness.
- **Hypothesis Preregistration**: Populates `00_meta/hypothesis_matrix.md` with explicit null ($H_0$) and alternative ($H_1$) hypotheses.
- **Protocol Formulation**: Prepares `02_methodology/statistical_plan.md` detailing required assumption tests (e.g. Shapiro-Wilk, Breusch-Pagan, VIF) before calculating p-values.

#### Step 3: Review and Approve the Implementation Plan
Antigravity generates an interactive Implementation Plan. Review the proposed model specifications, sample splits, and controls. Click **"Approve"** (or reply to confirm) to proceed with execution.

#### Step 4: Autonomous Polyglot Analysis & Robustness Testing
Antigravity executes the analysis in the appropriate toolchain (Python, R, Julia, or C++):
- Cleans data to `01_data/processed/` using documented transformation pipelines in `03_src/`.
- Estimates models with appropriate standard errors (heteroskedasticity-robust, clustered, or wild-bootstrap).
- Executes mandatory sensitivity/ablation checks (alternative specifications, outlier trims, permutation tests).

#### Step 5: Receive Publication-Grade Artifacts & Provenance Receipts
Upon completion:
- High-resolution figures (300 DPI PNG, vector PDF/SVG) are saved in `05_artifacts/figures/`.
- Summary tables (LaTeX, CSV, Markdown) are saved in `05_artifacts/tables/`.
- Cryptographic receipt is automatically registered in `05_artifacts/provenance/manifest.json`.
- A formal findings report is synthesized in `06_reports/`.

---

### Global Installation (Use Across Any Workspace in Antigravity)

By default, this skill lives inside the local workspace (`.agents/skills/research-scientist/`).  
To make this skill **globally available across every project** you open in Google Antigravity:

1. Copy the skill folder `.agents/skills/research-scientist/` to your global Antigravity configuration directory:
   - **Windows**: `C:\Users\<YourUsername>\.gemini\config\skills\research-scientist\`
   - **Linux / macOS**: `~/.gemini/config/skills/research-scientist/`
2. Once copied globally, you can open any empty folder in Antigravity and say:
   > *"Initialize an OmniResearch scientific workspace for my new study."*
   Antigravity will scaffold the entire FAIR structure and apply the scientific protocol anywhere on your system.

---

## 💬 Domain Prompt Cheatsheet

Use these ready-to-use prompt patterns to trigger specialized domain paradigms:

### 1. Economics, Finance & Social Sciences (Causal Inference)
```text
"Analyze the provincial panel data in 01_data/raw/regional_survey.csv.
Estimate the causal impact of the social program on youth employment using a
Difference-in-Differences (DiD) model with state-clustered standard errors.
Perform a parallel trends diagnostic and event-study plot."
```

### 2. Clinical Trials, Medicine & Pharmacology (Survival Analysis / RCT)
```text
"Examine the patient cohort in 01_data/raw/oncology_trial.csv.
Generate Kaplan-Meier survival curves comparing Treatment vs. Standard of Care,
run a log-rank test, and fit a Cox Proportional Hazards model while testing
Schoenfeld residuals for proportional hazards compliance."
```

### 3. Physics, Chemistry & Materials (Simulation & Kinetics)
```text
"Build a numerical simulation in 03_src/python/ for the enzymatic reaction network
defined by Michaelis-Menten kinetics. Test solver stability across stiff ODE regimes,
perform a parameter sweep for the catalytic rate constant, and plot phase portraits."
```

### 4. Machine Learning & Computer Science (Empirical Benchmarks)
```text
"Benchmark the tabular classification models on 01_data/raw/credit_risk.csv.
Ensure strict leak-free pre-processing via scikit-learn Pipelines, perform 5x2
cross-validation with statistical significance tests against baseline XGBoost,
and run an ablation study on the engineered interaction features."
```

### 5. Meta-Analysis & Systematic Reviews
```text
"Synthesize the 24 effect sizes extracted in 01_data/raw/intervention_studies.csv.
Compute pooled effect sizes using a random-effects model (REML), generate a
publication-grade forest plot, calculate Cochran's Q and I^2 heterogeneity,
and evaluate publication bias via Egger's test and a funnel plot."
```

### 6. Audit & Provenance Verification
```text
"Perform a scientific integrity audit on this workspace:
Verify that all files in 01_data/raw/ match their initial SHA-256 checksums,
confirm that no p-values are reported without confidence intervals,
and display the complete data lineage for Figure 2."
```

---

## 🚀 Cross-Platform Adaptability

| Platform / Engine | Configuration File | Activation Mechanism |
| :--- | :--- | :--- |
| **Google Antigravity** | [GEMINI.md](file:///d:/kris/Research%20skill/GEMINI.md) + [SKILL.md](file:///d:/kris/Research%20skill/.agents/skills/research-scientist/SKILL.md) | Automatically loaded on startup; active on all research prompts |
| **Claude Code** | [CLAUDE.md](file:///d:/kris/Research%20skill/CLAUDE.md) | Terminal CLI with slash commands (`/scaffold`, `/check-data`, `/toolchains`) |
| **Cursor IDE** | [.cursorrules](file:///d:/kris/Research%20skill/.cursorrules) | Active in Cursor Composer / Chat (`Ctrl+I` / `Cmd+I`) |
| **OpenAI Codex & Copilot** | [AGENTS.md](file:///d:/kris/Research%20skill/AGENTS.md) | Discovered automatically by GitHub Copilot Workspace and Codex engines |
| **Open Interpreter & Aider** | [AGENTS.md](file:///d:/kris/Research%20skill/AGENTS.md) + CLI tools | Operates via standard terminal commands and pure Python utilities |

---

## 🛠 Included CLI Utilities (Zero External Dependencies)

All utility scripts are written in pure Python 3 standard library (`pathlib`, `hashlib`, `json`, `argparse`, `platform`, `subprocess`):

1. **Scaffold Workspace**:
   ```bash
   python .agents/skills/research-scientist/scripts/scaffold_project.py [path]
   ```
2. **Audit System Toolchains**:
   ```bash
   python .agents/skills/research-scientist/scripts/validate_toolchains.py
   ```
3. **Lock Preregistration (Tamper-Proof Timestamp)**:
   ```bash
   python .agents/skills/research-scientist/scripts/record_provenance.py \
     --lock-preregistration 00_meta/hypothesis_matrix.md
   ```
4. **Record Artifact Provenance**:
   ```bash
   python .agents/skills/research-scientist/scripts/record_provenance.py \
     --artifact 05_artifacts/figures/fig1.pdf \
     --script 03_src/python/plot_fig1.py \
     --inputs 01_data/processed/clean.parquet \
     --params '{"seed": 42, "ci": 0.95}'
   ```

---

## ⚡ Instant One-Liner Installation

Install OmniResearch globally for **Google Antigravity** in one command:

### Linux & macOS (Bash):
```bash
curl -fsSL https://raw.githubusercontent.com/krsdntr/OmniResearch/main/install.sh | bash
```

### Windows (PowerShell):
```powershell
irm https://raw.githubusercontent.com/krsdntr/OmniResearch/main/install.ps1 | iex
```

*To install inside the current directory only, append `--local` to the installer.*

---

## 🧪 Reference Implementations

Explore our fully reproducible end-to-end examples in [`examples/`](file:///d:/kris/Research%20skill/examples/):
- **[Clinical Dose-Response Study (KR-42)](file:///d:/kris/Research%20skill/examples/clinical_dose_response/README.md)**: A complete Phase II dose-escalation trial with locked hypotheses, raw trial data, 4PL analysis script, 95% confidence intervals, and verifiable provenance receipt.

---

## 📜 Community & License

- **License**: [MIT License](file:///d:/kris/Research%20skill/LICENSE)
- **Contributing**: [Contribution Guidelines](file:///d:/kris/Research%20skill/CONTRIBUTING.md)
- **Code of Conduct**: [Scientific Ethics & Community Pledge](file:///d:/kris/Research%20skill/CODE_OF_CONDUCT.md)

