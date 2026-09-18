# Contributing to OmniResearch

Thank you for your interest in contributing to the **OmniResearch Scientist Workbench**! We welcome contributions from scientists, researchers, software engineers, and methodologists worldwide.

---

## 🧭 How You Can Contribute

1. **Add Methodological Paradigms (`paradigms/`)**:
   - Have a specialized methodology (e.g., Synthetic Control, Structural Equation Modeling, Quantum Chemistry simulations)?
   - Submit a new markdown guide under `.agents/skills/research-scientist/paradigms/`.

2. **Add Scientific Data Handlers (`data_handlers/`)**:
   - Handle unique scientific formats (e.g., DICOM medical images, Cryo-EM maps, seismic SEG-Y, mass spectrometry mzML)?
   - Submit a reference guide under `.agents/skills/research-scientist/data_handlers/`.

3. **Improve Toolchain Automation (`scripts/`)**:
   - Enhance `validate_toolchains.py`, `scaffold_project.py`, or `record_provenance.py`.
   - **Constraint**: All core scripts must remain **100% Python standard library** (zero external dependencies).

4. **IDE & Agent Bridges**:
   - Expand compatibility with new agentic IDEs, local LLM runners, or CLI tools.

---

## 🛠 Development & Testing Workflow

### 1. Fork & Clone
```bash
git clone https://github.com/krsdntr/OmniResearch.git
cd OmniResearch
```

### 2. Verify Core Scripts Locally
Make sure all zero-dependency CLI scripts execute cleanly across Python 3.10+:
```bash
python .agents/skills/research-scientist/scripts/validate_toolchains.py
python .agents/skills/research-scientist/scripts/scaffold_project.py --help
python .agents/skills/research-scientist/scripts/record_provenance.py --help
```

### 3. Commit Guidelines
We adhere to Conventional Commits:
- `feat:` A new feature, paradigm, or data handler.
- `fix:` A bug fix or encoding correction.
- `docs:` Documentation improvements in README or guides.
- `ci:` Updates to GitHub Actions workflows.

### 4. Pull Request (PR) Checklist
- [ ] Code is formatted and clean.
- [ ] No external dependencies introduced to `scripts/`.
- [ ] Cross-platform compatibility maintained (Windows, Linux, macOS).
- [ ] All new documentation includes actionable guidance.
