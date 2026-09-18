# Data Handler 1: Tabular & Complex Survey Data

Format Scope: `.csv`, `.tsv`, `.parquet`, `.feather`, `.dta` (Stata), `.sav` (SPSS), `.rds` (R).

---

## 1. Complex Survey Weighting & Stratification

In national or regional surveys (DHS, Susenas, NHANES, Eurobarometer), unweighted analysis introduces severe sampling bias:
- **Design Elements**:
  - Primary Sampling Units (PSU / Cluster).
  - Stratification variables (`strata`).
  - Survey Sampling Weights (`pweight`, `fweight`, or replicate weights).
- **Execution**:
  - Python: `samplics` or `statsmodels.survey`.
  - R: `survey::svydesign()`, `srvyr::as_survey_design()`.
  - Stata: `svyset psu [pweight=weight], strata(strata)`.

---

## 2. Missing Data Treatment

- Audit missingness mechanism:
  - Missing Completely at Random (MCAR) $\to$ Little's test.
  - Missing at Random (MAR) $\to$ Multiple Imputation by Chained Equations (MICE).
  - Missing Not at Random (MNAR) $\to$ Pattern-mixture models or sensitivity bounds.
- **Rule**: Avoid mean/median imputation. Use MICE (Python `fancyimpute`, R `mice`) generating $m \ge 10$ imputed datasets pooled via Rubin's rules.
