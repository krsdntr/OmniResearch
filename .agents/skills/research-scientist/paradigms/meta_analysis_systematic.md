# Paradigm 5: Systematic Reviews & Meta-Analyses

Applicable Domains: Evidence-Based Medicine, Public Health, Psychology, Education, Environmental Science.

---

## 1. Methodological Standards (PRISMA 2020)

### A. Study Selection Flow
- Document every step of the PRISMA flow diagram:
  1. Records identified through database searching (PubMed, Scopus, Web of Science, arXiv).
  2. Duplicates removed.
  3. Records screened by title/abstract and excluded with explicit criteria.
  4. Full-text articles assessed for eligibility.
  5. Studies included in qualitative synthesis and quantitative meta-analysis.

### B. Risk of Bias Assessment
- Use domain-specific tools:
  - Cochrane RoB 2 for randomized trials.
  - ROBINS-I for non-randomized studies of interventions.
  - Newcastle-Ottawa Scale (NOS) for cohort and case-control studies.

---

## 2. Quantitative Pooling & Effect Sizes

- **Continuous Outcomes**: Standardized Mean Difference (Hedges' $g$ or Cohen's $d$).
- **Binary Outcomes**: Risk Ratio (RR), Odds Ratio (OR), or Risk Difference (RD).
- **Pooling Models**:
  - Fixed-effect model (assumes one true underlying effect size).
  - Random-effects model (DerSimonian-Laird or REML; recommended for ecological and clinical diversity).

---

## 3. Heterogeneity & Publication Bias Diagnostics

- **Heterogeneity Metrics**:
  - Cochran's $Q$ test ($p < 0.10$ indicates significant heterogeneity).
  - $I^2$ statistic ($<25\%$ low, $50\%$ moderate, $>75\%$ high heterogeneity).
  - Tau-squared ($\tau^2$) estimation of between-study variance.
- **Publication Bias & Small-Study Effects**:
  - Visual inspection of Funnel plots.
  - Egger's linear regression test for funnel plot asymmetry.
  - Duval and Tweedie's trim-and-fill method for imputed missing studies.
- Tools: R (`meta`, `metafor`), Python (`statsmodels`).
