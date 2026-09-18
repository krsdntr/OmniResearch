# Paradigm 1: Experimental Design & Randomized Controlled Trials (RCT)

Applicable Domains: Clinical Medicine, Pharmacology, Agriculture & Agronomy, Psychology, Laboratory Biology/Biotechnology.

---

## 1. Experimental Design Typology

### A. Biomedical & Clinical Trials
- **Parallel Group RCT**: Treatment vs. Placebo / Standard of Care.
- **Crossover Design**: Patient receives Treatment A $\to$ Washout Period $\to$ Treatment B.
- **Factorial Design**: $2 \times 2$ testing two concurrent interventions and interaction effects.

### B. Agricultural & Environmental Field Trials
- **Completely Randomized Design (CRD / RAL)**: Homogeneous experimental units.
- **Randomized Complete Block Design (RCBD / RAK)**: Blocking on environmental gradients (soil fertility, slope).
- **Split-Plot Design**: Main plots (irrigation/tillage) split into subplots (varieties/fertilizer doses).

---

## 2. Statistical Power Analysis & Sample Size Determination

Prior to data collection or post-hoc adequacy check:
- Calculate required sample size ($N$) based on:
  - $\alpha$ (Type I error rate, default $0.05$)
  - $\beta$ (Type II error rate, power $1 - \beta \ge 0.80$)
  - Minimal Detectable Effect size (Cohen's $d$, odds ratio, or hazard ratio)
- Recommended Toolchains:
  - Python: `statsmodels.stats.power.TTestIndPower`
  - R: `pwr::pwr.t.test()`, `pwr::pwr.anova.test()`

---

## 3. Analysis Pipeline & Robust Modeling

1. **Baseline Balance Check**:
   - Compare control and intervention arms (Table 1 demographics). Note: Avoid relying solely on p-values for baseline differences in large randomized trials; evaluate standardized mean differences (SMD $< 0.1$).
2. **Primary Intention-to-Treat (ITT)**:
   - Analyze all randomized participants regardless of adherence or dropout.
   - Use Per-Protocol (PP) analysis only as a secondary sensitivity check.
3. **ANOVA & Linear Mixed-Effects Models (LMM)**:
   - For repeated measures / agricultural blocks:
     $$\text{Yield}_{ijk} = \mu + \alpha_i + \beta_j + (\alpha\beta)_{ij} + \gamma_k + \epsilon_{ijk}$$
   - Python: `statsmodels.formula.api.mixedlm`
   - R: `lme4::lmer()`, `agricolae::sp.plot()`
4. **Post-Hoc Multiple Comparisons**:
   - Tukey's HSD, Dunnett's test (vs. control), or Bonferroni adjustments.
