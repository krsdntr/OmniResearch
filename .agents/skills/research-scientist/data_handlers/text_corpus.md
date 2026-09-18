# Data Handler 5: Text Corpora & Digital Humanities

Format Scope: Plain Text (`.txt`), Structured Docs (`.xml`, `.tei`, `.html`), PDFs (`.pdf`), JSON Lines (`.jsonl`).

---

## 1. Corpus Preparation & Normalization

- Tokenization, lemmatization (morphological base form), case folding, stop-word removal.
- Domain-specific stop words: In academic literature review, filter out words like *study*, *result*, *method*, *et al.*
- Tools: Python (`spacy`, `nltk`), R (`quanteda`, `tidytext`).

---

## 2. Quantitative Text Analysis & Humanities Methods

- **Stylometry & Authorship Attribution**: Burrows' Delta, MFW (Most Frequent Words) distance metrics. Tool: R (`stylo`).
- **Topic Modeling**: Latent Dirichlet Allocation (LDA) and BERTopic with coherence score optimization ($C_v > 0.5$).
- **Collocation & N-Grams**: Mutual Information (MI), Log-Likelihood ratio, t-score for significant multi-word associations.
- **Sentiment & Lexicon Scoring**: VADER, LIWC (Linguistic Inquiry and Word Count) categories, transformer zero-shot classification.
