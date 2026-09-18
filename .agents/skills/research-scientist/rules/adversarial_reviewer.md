# Adversarial Reviewer 2 Protocol: Eliminating AI Sycophancy & Confirmation Bias

Autonomous AI systems are inherently prone to **sycophancy**—a systematic tendency to agree with researcher premises, report flattering correlations, and select model specifications that confirm the user's initial hypothesis.

The **Reviewer 2 Protocol** is an epistemological counter-measure. Before any empirical finding is finalized or summarized in `06_reports/`, the agent must execute an adversarial audit or assume the persona of a relentless, skeptical peer-reviewer whose explicit mandate is to invalidate the primary conclusion.

---

## 1. The 5 Adversarial Attack Vectors

Every primary finding must withstand five systematic attacks:

### Attack 1: The "Marginal Significance" Trap ($0.01 \le p < 0.05$)
* **Mechanism**: P-values hovering between 0.01 and 0.05 are disproportionately false positives resulting from researcher degrees of freedom.
* **Audit**:
  - Were multiple dependent variables, subgroups, or specifications tested?
  - If more than 1 hypothesis was evaluated, enforce strict Holm-Bonferroni or FDR (Benjamini-Hochberg) corrections. If the adjusted $p \ge 0.05$, the finding must be declared exploratory/inconclusive.

### Attack 2: Outlier Trimming & Influence Fragility
* **Mechanism**: A statistical effect driven entirely by 1–3 leverage points is not a genuine population phenomenon.
* **Audit**:
  - Calculate Cook's Distance $D_i$ for all observations. Identify any $D_i > 4/n$.
  - Re-fit the model removing the top 5% most influential observations (or winsorizing at the 5th and 95th percentiles).
  - If the effect size attenuates by $> 50\%$ or loses significance, flag the finding as **Fragile / Outlier-Dependent**.

### Attack 3: Confounder & Omitted Variable Stress Test
* **Mechanism**: Spurious correlations arising from unmodeled confounders (e.g., batch effects, cohort demographics, seasonal time trends).
* **Audit**:
  - Formulate at least two plausible omitted confounders.
  - Compute Oster's delta ($\delta$) or Rosenbaum bounds for sensitivity to unobserved selection.
  - Report the degree of confounding selection bias required to explain away the observed effect.

### Attack 4: Placebo & Permutation Testing
* **Mechanism**: Testing whether the analytical pipeline generates false positives on pure noise.
* **Audit**:
  - Permute (shuffle) the treatment or independent variable randomly across observations while keeping covariates and outcomes intact.
  - Re-run the estimator over 1,000 permutations.
  - Compute the empirical Monte Carlo p-value:
    $$\hat{p} = \frac{1 + \sum_{b=1}^{B} \mathbb{I}(|\hat{\beta}^{(b)}| \ge |\hat{\beta}|)}{B + 1}$$
  - If the empirical permutation p-value contradicts the parametric p-value, reject the parametric assumption.

### Attack 5: Specification Curve & Multiverse Analysis
* **Mechanism**: Arbitrary decisions regarding covariate inclusion, functional forms (log vs. level), and filtering thresholds.
* **Audit**:
  - Run a mini-multiverse (at least 6 reasonable alternative model specifications).
  - Plot or list the coefficient distribution across specifications.
  - Report the proportion of specifications in which the direction and significance hold.

---

## 2. Deliverable: The Adversarial Audit Report

All adversarial checks must be formally synthesized in `00_meta/adversarial_audit.md` using the standardized template in `.agents/skills/research-scientist/templates/adversarial_audit_template.md`.

No empirical finding may be described as "proven", "demonstrated", or "established" without a completed Adversarial Audit Scorecard.
