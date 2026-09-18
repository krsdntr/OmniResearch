# Statistical Analysis Plan: KR-42 Dose-Ranging Study

## 1. Study Design
- **Type**: Multi-cohort dose-escalation trial (6 dose tiers: 0, 5, 15, 50, 100, 150 mg).
- **Target Population**: Healthy volunteers / Phase II oncology cohort ($N = 18$).
- **Primary Endpoint**: Target biomarker kinase inhibition ratio (baseline normalized).

## 2. Primary Model & Parametric Form
- 4-Parameter Logistic (4PL) Hill equation:
  $$E(\text{Dose}) = E_0 + \frac{E_{\max} - E_0}{1 + \left(\frac{\text{IC}_{50}}{\text{Dose}}\right)^h}$$
- Linear baseline comparison: $E(\text{Dose}) = \alpha + \beta \cdot \text{Dose}$.
- Model selection criterion: Akaike Information Criterion (AIC) and residual sum of squares F-test.

## 3. Assumptions & Diagnostics
- Homoscedasticity of residuals across dose tiers.
- Non-negative constraint on inhibition metric ($0 \le E \le 1.0$).
