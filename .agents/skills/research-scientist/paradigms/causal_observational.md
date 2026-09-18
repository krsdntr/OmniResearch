# Paradigm 2: Causal Inference & Observational Studies

Applicable Domains: Economics, Public Health & Epidemiology, Sociology, Political Science, Education, Environmental Policy.

---

## 1. Identification Strategies

When randomization is impossible, use quasi-experimental methods to establish causality:

### A. Difference-in-Differences (DiD)
- **Equation**: $Y_{it} = \alpha_i + \lambda_t + \beta (\text{Post}_t \times \text{Treated}_i) + X'_{it}\gamma + \epsilon_{it}$
- **Essential Diagnostic**: Parallel trends assumption test in pre-treatment periods.
- **Staggered Adoption**: Use modern estimators (Callaway & Sant'Anna, Sun & Abraham) when treatment timing varies.
- Tools: R (`fixest::feols`, `did`), Python (`pyfixest`, `linearmodels`).

### B. Instrumental Variables (IV / 2SLS)
- **Conditions**: Relevance ($\text{Cov}(Z, D) \ne 0$) and Exogeneity ($\text{Cov}(Z, \epsilon) = 0$).
- **Essential Diagnostics**:
  - First-stage F-statistic ($F > 10$, or effective F test $> 104$ for weak instruments).
  - Hansen-Sargan overidentification test if overidentified.
  - Durbin-Wu-Hausman test for endogeneity.
- Tools: R (`AER::ivreg`, `fixest`), Python (`linearmodels.iv.IV2SLS`).

### C. Regression Discontinuity Design (RDD)
- Sharp vs. Fuzzy RDD.
- **Essential Diagnostics**:
  - McCrary density test (check for manipulation around the cutoff).
  - Balance tests on predetermined covariates at the threshold.
  - Bandwidth sensitivity (optimal MSE vs. CER bandwidths).
- Tools: R (`rdrobust`), Python (`rdrobust`).

### D. Survival & Time-to-Event Analysis
- Kaplan-Meier non-parametric survival curves with log-rank tests.
- Cox Proportional Hazards Model: check Schoenfeld residuals for proportional hazards assumption.
- Tools: Python (`lifelines`), R (`survival::coxph`).

---

## 2. Standard Error Clustering
- Panel/clustered data must use cluster-robust standard errors at the level of treatment assignment (e.g., state, village, hospital).
