# Research Protocol & Preregistration Specification

**Project Title**: [Insert Title]  
**Lead Investigator**: [Name / Team]  
**Date**: [YYYY-MM-DD]  
**Registration Status**: [Draft / Preregistered / Under Revision]  

---

## 1. Background & Research Question
- **Scientific Context**:
- **Primary Research Question (RQ)**:
- **Theoretical Framework**:

---

## 2. Sampling & Data Acquisition Strategy
- **Target Population / Experimental Units**:
- **Inclusion Criteria**:
- **Exclusion Criteria**:
- **Sample Size Calculation**:
  - Significance Level ($\alpha$): 0.05
  - Target Statistical Power ($1 - \beta$): 0.80
  - Anticipated Effect Size ($d$ / Hazard Ratio / Cohen's $f^2$):
  - Required $N$ per arm / overall:

---

## 3. Operationalization of Variables
- **Primary Outcome Variable ($Y$)**: [Exact measurement unit and definition]
- **Treatment / Primary Predictor ($X$)**: [Categorical or continuous definition]
- **Predefined Covariates ($Z$)**: [List of controls justified by DAG / causal diagram]

---

## 4. Analytical Pipeline & Pre-Specified Models
- **Primary Estimator**: [e.g. OLS with clustered SEs / ANCOVA / Cox PH / Negative Binomial]
- **Handling of Missing Values**: [Complete-case / Multiple Imputation (MICE, $m=10$)]
- **Correction for Multiple Endpoints**: [Bonferroni / Benjamini-Hochberg FDR]

---

## 5. Robustness & Sensitivity Protocol
- [ ] Specification 1: Non-linear transformations ($\log$, polynomial).
- [ ] Specification 2: Subsample restriction by demographic / temporal split.
- [ ] Specification 3: Outlier exclusion test (Cook's distance $> 4/n$).
- [ ] Specification 4: Placebo outcome or permutation test.
