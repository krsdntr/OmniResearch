# Data Provenance, Lineage & FAIR Compliance

This document enforces the FAIR (Findable, Accessible, Interoperable, Reusable) data standards and end-to-end traceability of research outputs.

---

## 1. The Immutability Quarantine

- All external source files deposited into `01_data/raw/` are **cryptographically locked**.
- Upon receipt, the system computes the SHA-256 digest of each raw file and writes it into `01_data/raw_checksums.sha256`.
- Automated checks will fail if any file in `01_data/raw/` has been modified after initial ingestion.

---

## 2. Transformation Lineage

Every dataset in `01_data/interim/` or `01_data/processed/` must be reproducible via a dedicated script in `03_src/`.
- File naming convention:
  - `03_src/01_clean_<dataset_name>.<ext>`
  - `03_src/02_transform_<dataset_name>.<ext>`
- Each cleaning script must document:
  - Input raw file path and SHA-256
  - Number of rows dropped / imputed and rationale
  - Output file path and SHA-256

---

## 3. Artifact Receipts (The Provenance Manifest)

No figure in `05_artifacts/figures/` or table in `05_artifacts/tables/` is considered final without a corresponding record in `05_artifacts/provenance/manifest.json`.

The manifest must capture:
1. `artifact_id`: Filename and relative path.
2. `timestamp_utc`: ISO 8601 creation timestamp.
3. `source_script`: The exact script that produced the artifact.
4. `script_hash`: SHA-256 of the source script code.
5. `input_datasets`: Array of input file paths with their respective SHA-256 checksums.
6. `parameters`: Dictionary of all hyperparameters, random seeds, and cutoff thresholds used.
7. `environment`: Operating system, interpreter version (Python/R/Julia), and key library versions.
