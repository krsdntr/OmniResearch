# Data Handler 4: Signals, Physiological & Physical Sensor Streams

Format Scope: Biomedicine (`.edf`, `.bdf`, `.set`), Acoustic & Audio (`.wav`, `.flac`), Industrial IoT & High-Frequency Accelerometry (`.csv`, `.parquet`, `.mat`).

---

## 1. Digital Signal Preprocessing

- **Sampling Rate & Nyquist Criterion**: Ensure sampling rate $f_s > 2 f_{\max}$.
- **Filtering Protocols**:
  - Detrending and DC-offset removal.
  - Notch filter (50 Hz or 60 Hz) for powerline interference removal.
  - Butterworth bandpass filtering (e.g. 0.5 - 45 Hz for EEG rhythms: Delta, Theta, Alpha, Beta, Gamma).

---

## 2. Spectral & Time-Frequency Analysis

- **Fourier Analysis (FFT)**: Welch's method for Power Spectral Density (PSD) estimation.
- **Wavelet Transform**: Continuous Wavelet Transform (CWT) using Morlet wavelets for non-stationary signals.
- **Event-Related Potentials (ERP)**: Epoching, baseline correction, artifact rejection ($> 100\,\mu\text{V}$).
- Tools: Python (`scipy.signal`, `mne` for electrophysiology, `librosa` for acoustic analysis).
