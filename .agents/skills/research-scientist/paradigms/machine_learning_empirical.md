# Paradigm 4: Machine Learning & Empirical Benchmarking

Applicable Domains: Computer Science, AI/ML, Bioinformatics, Chemometrics, Quantitative Finance, Remote Sensing.

---

## 1. Experimental Integrity in ML Research

### A. Partitioning & Data Leakage Prevention
- **Golden Rule**: Never fit any transformer (scaler, PCA, impute, tokenizer) on test or validation splits.
- Pipelines must encapsulate all steps (`sklearn.pipeline.Pipeline`).
- For hierarchical or grouped data (e.g. repeated samples from same subject or biological replicate), use `GroupKFold` or `StratifiedGroupKFold`.

### B. Baseline Benchmarking
- A novel proposed architecture must always be compared against:
  1. Naive baseline (majority class, mean/median, random walk).
  2. Standard canonical baseline (Linear/Logistic, Random Forest, XGBoost).
  3. Current state-of-the-art literature baseline under identical evaluation conditions and seeds.

---

## 2. Mandatory Ablation Studies

- For any composite method claiming novelty, systematically remove individual components to verify contribution:
  - Feature ablation (importance drop).
  - Module ablation (removing attention heads, residual layers, loss regularization terms).
  - Hyperparameter sensitivity (performance surface over learning rate, weight decay).

---

## 3. Statistical Significance of ML Benchmarks
- Do not compare models using single point scores on a single test split.
- Use 5x2 cross-validation with Dietterich's 5x2cv paired t-test or Wilcoxon signed-rank test across folds to prove significance of improvements ($p < 0.05$).
