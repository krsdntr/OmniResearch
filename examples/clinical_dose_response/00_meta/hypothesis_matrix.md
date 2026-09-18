# Hypothesis Registration: Phase II Dose-Ranging Trial (KR-42)

| ID | Research Question | Null Hypothesis ($H_0$) | Alternative Hypothesis ($H_1$) | Primary Variable ($Y$) | Target Estimator | Direction | Alpha ($\\alpha$) | Status |
|:---|:------------------|:------------------------|:-------------------------------|:-----------------------|:-----------------|:----------|:------------------|:-------|
| H-01 | Does oral KR-42 administration significantly inhibit biomarker kinase activity? | $\beta_{\text{dose}} = 0$ | $\beta_{\text{dose}} > 0$ | Inhibition Ratio ($0-1.0$) | Monotonic Trend / ANOVA | Positive | 0.05 | Registered |
| H-02 | Does biomarker inhibition exhibit a non-linear sigmoidal ceiling effect above 50 mg? | $E_{\max} = \infty$ (linear model holds) | Sigmoidal 4PL fits significantly better than linear ($p < 0.01$) | $\Delta \text{AIC} > 10$ | F-test / AIC comparison | Non-linear | 0.01 | Registered |
