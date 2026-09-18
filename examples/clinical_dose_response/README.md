# Reference Example: Clinical Dose-Response Study (KR-42)

This directory demonstrates a complete, end-to-end scientific study adhering to the **OmniResearch Scientist Protocol**.

---

## 🔬 Study Overview
- **Scenario**: Phase II dose-ranging trial for novel kinase inhibitor compound `KR-42`.
- **Primary Endpoint**: Target biomarker kinase inhibition ratio ($0.0 - 1.0$) across 6 dose cohorts ($0, 5, 15, 50, 100, 150\text{ mg}$).
- **Sample Size**: $N = 18$ subjects (3 subjects per dose cohort).

---

## 📂 Provenance & FAIR Structure in this Example

1. **`00_meta/hypothesis_matrix.md`**: Pre-registered hypotheses ($H_0$: no effect, $H_1$: monotonic positive response with sigmoidal ceiling).
2. **`01_data/raw/dose_response_trial.csv`**: Raw input data (immutable and cryptographically tracked).
3. **`02_methodology/statistical_plan.md`**: Pre-analysis plan specifying 4PL model and 95% confidence intervals.
4. **`03_src/python/analyze_dose_response.py`**: Zero-dependency analysis script that produces summary metrics and automatically records provenance receipts.
5. **`05_artifacts/tables/dose_summary.csv`**: Output data table with 95% confidence bounds.
6. **`05_artifacts/provenance/manifest.json`**: Tamper-proof provenance receipt containing SHA-256 digests of input data, script, parameters, and environment.

---

## 🚀 How to Run this Example

From the repository root:
```bash
python examples/clinical_dose_response/03_src/python/analyze_dose_response.py
```

Inspect the generated provenance receipt:
```bash
cat examples/clinical_dose_response/05_artifacts/provenance/manifest.json
```
