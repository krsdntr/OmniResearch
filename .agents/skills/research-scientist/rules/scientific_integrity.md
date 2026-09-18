# Scientific Integrity & Methodological Guardrails

This document establishes the ethical and procedural boundaries for autonomous and semi-autonomous quantitative research.

---

## 1. Prevention of P-Hacking & Selective Reporting

- **Hypothesis Registration**: A hypothesis must be defined in `00_meta/hypothesis_matrix.md` prior to executing regressions or comparative tests.
- **Multiple Comparisons**: If testing more than one endpoint or hypothesis, apply appropriate correction:
  - Family-Wise Error Rate (FWER): Bonferroni or Holm-Bonferroni correction.
  - False Discovery Rate (FDR): Benjamini-Hochberg procedure.
- **Full Model Reporting**: Never omit non-significant covariates or null results to make a model look better. Report full coefficient tables alongside filtered summaries.

---

## 2. Assumption Checking & Diagnostics

Before accepting any statistical inference:
1. **Normality of Residuals**: Assess via Shapiro-Wilk, Jarque-Bera, or Q-Q plots.
2. **Homoscedasticity**: Test with Breusch-Pagan or White's test; use heteroskedasticity-robust standard errors (HC1, HC3, or cluster-robust) by default.
3. **Multicollinearity**: Calculate Variance Inflation Factors (VIF); investigate any predictor with $\text{VIF} > 5$.
4. **Endogeneity & Omitted Variable Bias**: Test instrumental validity (Sargan-Hansen test, weak instrument F-statistic $> 10$).
5. **Time-Series Stationarity**: Test unit roots via Augmented Dickey-Fuller (ADF) or KPSS before cointegration or ARIMA modeling.

---

## 3. Data Leakage Prevention (Empirical & ML Models)

- **Strict Pre-Processing Partition**: Imputation, scaling, normalization, and feature selection must be fitted **strictly on training folds**, never on the full dataset prior to train/test split.
- **Temporal Split**: For time-series, always use walk-forward validation or temporal cutoff splits; never use standard random k-fold cross-validation.
- **Group-Aware Splitting**: If data contains hierarchical clusters (patients, schools, countries), use `GroupKFold` to prevent patient/subject leakage across splits.

---

## 4. Sensitivity & Robustness Standards

Every major conclusion must survive at least two of the following checks:
1. **Alternative Specifications**: Re-estimating with different functional forms (e.g., log-linear vs. level-level).
2. **Subsample Analysis**: Verifying the effect persists across demographic or temporal splits.
3. **Outlier Sensitivity**: Re-evaluating after winsorizing or trimming extreme observations (Cook's distance $> 4/n$).
4. **Placebo / Permutation Tests**: Randomly shuffling treatment labels or outcome variables to ensure false discovery rate aligns with nominal $\alpha$.
