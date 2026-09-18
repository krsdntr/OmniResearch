# Data Handler 3: Biological Sequences & Molecular Structures

Format Scope: Genomic/Proteomic (`.fasta`, `.fastq`, `.vcf`, `.sam`, `.bam`), Structural (`.pdb`, `.cif`, `.mmcif`), Cheminformatics (`.smi`, `.sdf`, `.mol2`).

---

## 1. Sequence Bioinformatics & Differential Expression

- **Genomic & RNA-Seq Processing**:
  - Quality control: Adapter trimming, Phred score check ($Q > 30$).
  - Differential Expression Analysis (RNA-Seq counts):
    - Modeling overdispersed counts using Negative Binomial distributions.
    - Tools: R (`DESeq2`, `edgeR`), Python (`PyDESeq2`).
- **Multiple Sequence Alignment (MSA)**:
  - BLOSUM62 / PAM250 substitution matrices.
  - Tools: Clustal Omega, MUSCLE, MAFFT via CLI or `BioPython`.

---

## 2. Structural Biology & Cheminformatics

- **Small Molecules & SMILES**:
  - Descriptors: Molecular weight, LogP, TPSA, Lipinski's Rule of 5.
  - Fingerprints: Morgan / ECFP4 fingerprints for Tanimoto similarity searches.
  - Tool: Python (`rdkit`).
- **Macromolecular 3D Structures**:
  - Coordinate extraction, secondary structure assignment (DSSP), Ramachandran plot validation.
  - Tools: Python (`Bio.PDB`, `MDAnalysis`, PyMOL command-line).
