# Adversarial Audit & Robustness Scorecard (Reviewer 2 Report)

> **Protocol**: OmniResearch Adversarial Anti-Bias Standard  
> **Target Hypothesis**: [Insert Hypothesis ID from 00_meta/hypothesis_matrix.md]  
> **Primary Claim**: [Brief statement of observed effect size, direction, and p-value]  
> **Auditing Agent / Reviewer**: Reviewer 2 (Adversarial Persona)  
> **Date**: [YYYY-MM-DD]

---

## 1. Attack Vector Evaluations

| Attack Vector | Stress Test Applied | Result / Impact on Primary Effect | Status |
| :--- | :--- | :--- | :--- |
| **1. Marginal Significance Trap** | Multiple comparison correction (Holm-Bonferroni / Benjamini-Hochberg) | Primary p-value: `[P_VAL]`, Adjusted p-value: `[ADJ_P]` | `[PASS / FAIL / MARGINAL]` |
| **2. Outlier Fragility** | 5% Cook's distance trimming or 95% Winsorization | Effect changed from `[ORIG]` to `[NEW]` ($\Delta = [X]\%$) | `[ROBUST / FRAGILE]` |
| **3. Confounder Stress Test** | Plausible unobserved confounder test (Oster $\delta$ / Rosenbaum bounds) | Selection ratio required to nullify effect: `[DELTA]` | `[INSENSITIVE / VULNERABLE]` |
| **4. Placebo / Permutation** | 1,000 Monte Carlo label permutations | Empirical permutation p-value: `[PERM_P]` | `[CONFIRMED / REJECTED]` |
| **5. Multiverse Specifications** | Alternative functional forms and covariate subsets | Effect direction preserved in `[X]` of `[N]` models (`[Y]\%`) | `[HIGH / MEDIUM / LOW]` |

---

## 2. Adversarial Critique & Skeptic's Summary

### Key Vulnerabilities Identified:
- **Point 1**: [Describe potential weakness or limitation in data/model]
- **Point 2**: [Alternative non-causal explanation for findings]

### Required Author Rebuttals / Boundary Conditions:
- [Specify under what exact conditions this conclusion holds and where it breaks down]

---

## 3. Overall Epistemological Verdict

- [ ] **CONFIRMED ROBUST**: Finding withstood all 5 stress tests. Cleared for definitive publication claims.
- [ ] **QUALIFIED / CONDITIONAL**: Finding is valid only under specific model specifications or bounded contexts. Must report boundary conditions in abstract and conclusions.
- [ ] **REFUTED / INCONCLUSIVE**: Finding collapsed under outlier trimming, permutation, or multiple comparison adjustment. Relegated to exploratory hypothesis.
