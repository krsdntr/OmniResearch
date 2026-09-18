# Supplementary Information: Methodological Lineage, Verification & Statistical Protocols

> **Generated via OmniResearch Protocol** | 2026-09-18 13:06:40 UTC

---

## Section S1: Data Provenance & Cryptographic Lineage

All computational outputs, tables, and figures are cryptographically tied to immutable raw data checksums via SHA-256.

| Artifact | Type | SHA-256 Fingerprint | Source Script | Input Dataset(s) |
| :--- | :--- | :--- | :--- | :--- |
| **dose_summary.csv** | Artifact | `e5309e7567f7...` | `analyze_dose_response.py` | `dose_response_trial.csv` (c88f4bd4...) |


## Section S2: Human-in-the-Loop Preregistration & Approval Gates

| Checkpoint Gate | Status | Researcher Signatory | Timestamp (UTC) | Digital Signature |
| :--- | :--- | :--- | :--- | :--- |
| `hypothesis-lock` | **APPROVED** | Dr. Sarah Chen (Principal Investigator) | 2026-09-18T13:04:40 | `9f873d8cf342...` |


## Section S3: Computational Environment & Reproducibility

- **Operating System**: Windows

- **Primary Interpreter**: Python 3.14.2

- **Deterministic Random Seed**: `seed = 42` (fixed across stochastic iterations)



## Section S4: Empirical Summary Tables

### Table S4.1: dose_summary.csv

| dose_mg | sample_size | mean_inhibition | std_dev | std_error | ci_95_lower | ci_95_upper |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 0.0 | 3 | 0.02 | 0.03 | 0.0173 | 0.0 | 0.0945 |
| 5.0 | 3 | 0.1833 | 0.0351 | 0.0203 | 0.0961 | 0.2706 |
| 15.0 | 3 | 0.48 | 0.04 | 0.0231 | 0.3806 | 0.5794 |
| 50.0 | 3 | 0.7933 | 0.0351 | 0.0203 | 0.7061 | 0.8806 |
| 100.0 | 3 | 0.9167 | 0.0252 | 0.0145 | 0.8541 | 0.9792 |
| 150.0 | 3 | 0.9467 | 0.0153 | 0.0088 | 0.9087 | 0.9846 |

