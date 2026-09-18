# Formal Hypothesis Registration Matrix

| ID | Research Question | Null Hypothesis ($H_0$) | Alternative Hypothesis ($H_1$) | Primary Variable ($Y$) | Estimator / Test | Expected Direction | Alpha ($\\alpha$) | Status |
|:---|:------------------|:------------------------|:-------------------------------|:-----------------------|:-----------------|:-------------------|:------------------|:-------|
| H-01 | [e.g. Does compound A reduce tumor volume?] | $\mu_{\text{treat}} = \mu_{\text{ctrl}}$ | $\mu_{\text{treat}} < \mu_{\text{ctrl}}$ | Tumor Volume ($\text{mm}^3$) | Mixed-effects ANOVA | Negative | 0.05 | Registered |
| H-02 | [e.g. Does policy P reduce youth unemployment?] | $\beta_{\text{DiD}} = 0$ | $\beta_{\text{DiD}} < 0$ | Unemployment Rate (%) | Two-Way Fixed Effects | Negative | 0.05 | Registered |
| H-03 | [e.g. Does architecture M improve sample efficiency?] | $\text{Reward}_M = \text{Reward}_{\text{base}}$ | $\text{Reward}_M > \text{Reward}_{\text{base}}$ | Cumulative Reward | 5x2cv Paired t-test | Positive | 0.05 | Registered |
