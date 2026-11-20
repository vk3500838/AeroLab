"""Signal-processing tools for experimental stall-inception investigations.

These routines extract repeatable signal features. They do not independently
declare that a flow has stalled; that interpretation requires sensor context,
test conditions, and validation against known stall events.
"""
from dataclasses import dataclass, asdict
import numpy as np
from scipy import signal

from .exceptions import AnalysisError


@dataclass(frozen=True)
class StallSignalFeatures:
    sample_count: int
    sampling_frequency_hz: float
    duration_s: float
    mean: float
    rms_fluctuation: float
    peak_to_peak: float
    crest_factor: float
    dominant_frequency_hz: float
    dominant_amplitude: float

    def to_dict(self):
        return asdict(self)


def _validate_signal(time_s, values):
    t = np.asarray(time_s, dtype=float)
    x = np.asarray(values, dtype=float)
    if t.ndim != 1 or x.ndim != 1 or len(t) != len(x) or len(t) < 16:
        raise AnalysisError("time_s and signal must be equal-length 1-D arrays with >=16 samples.")
    if not np.isfinite(t).all() or not np.isfinite(x).all():
        raise AnalysisError("Time and signal arrays must contain only finite values.")
    dt = np.diff(t)
    if np.any(dt <= 0):
        raise AnalysisError("Timestamps must be strictly increasing.")
    median_dt = float(np.median(dt))
    deviation = np.max(np.abs(dt - median_dt)) / median_dt
    if deviation > 0.02:
        raise AnalysisError(
            "Sampling is not sufficiently uniform for this analysis. "
            "Resample the signal and retain the original timestamps."
        )
    return t, x, 1.0 / median_dt


def extract_stall_features(time_s, values):
    """Extract basic fluctuation and spectral features from one sensor channel."""
    t, x, fs = _validate_signal(time_s, values)
    fluctuation = x - np.mean(x)
    rms = float(np.sqrt(np.mean(fluctuation ** 2)))
    peak_to_peak = float(np.ptp(x))
    peak = float(np.max(np.abs(fluctuation)))
    crest = peak / rms if rms > 0 else float("nan")

    window = np.hanning(len(x))
    spectrum = np.abs(np.fft.rfft(fluctuation * window))
    frequency = np.fft.rfftfreq(len(x), d=1.0 / fs)
    if len(spectrum) > 1:
        spectrum[0] = 0.0
    index = int(np.argmax(spectrum))
    coherent_gain = np.sum(window) / len(x)
    amplitude = float(2.0 * spectrum[index] / (len(x) * coherent_gain))
    return StallSignalFeatures(
        sample_count=len(x),
        sampling_frequency_hz=fs,
        duration_s=float(t[-1] - t[0]),
        mean=float(np.mean(x)),
        rms_fluctuation=rms,
        peak_to_peak=peak_to_peak,
        crest_factor=float(crest),
        dominant_frequency_hz=float(frequency[index]),
        dominant_amplitude=amplitude,
    )


def band_rms(time_s, values, low_hz, high_hz):
    """Return RMS of a Butterworth-filtered band; frequencies are in Hz."""
    t, x, fs = _validate_signal(time_s, values)
    if low_hz <= 0 or high_hz <= low_hz or high_hz >= fs / 2:
        raise ValueError("Require 0 < low_hz < high_hz < Nyquist frequency.")
    sos = signal.butter(4, [low_hz, high_hz], btype="bandpass",
                        fs=fs, output="sos")
    filtered = signal.sosfiltfilt(sos, x - np.mean(x))
    return float(np.sqrt(np.mean(filtered ** 2)))


def stft_map(time_s, values, nperseg=1024, noverlap=None):
    """Return frequency, time, and magnitude arrays for a spectrogram view."""
    _, x, fs = _validate_signal(time_s, values)
    if nperseg < 16:
        raise ValueError("nperseg must be at least 16.")
    nperseg = min(nperseg, len(x))
    noverlap = nperseg // 2 if noverlap is None else noverlap
    if not 0 <= noverlap < nperseg:
        raise ValueError("noverlap must be in [0, nperseg).")
    f, t, z = signal.stft(x - np.mean(x), fs=fs, nperseg=nperseg,
                          noverlap=noverlap, boundary=None)
    return f, t, np.abs(z)


def compare_windows(time_s, values, window_s, step_s):
    """Compute RMS and dominant frequency over sequential time windows."""
    t, x, fs = _validate_signal(time_s, values)
    if window_s <= 0 or step_s <= 0:
        raise ValueError("window_s and step_s must be positive.")
    window_n = int(round(window_s * fs))
    step_n = int(round(step_s * fs))
    if window_n < 16 or window_n > len(x):
        raise ValueError("Window length must contain >=16 samples and fit the record.")
    rows = []
    for start in range(0, len(x) - window_n + 1, step_n):
        end = start + window_n
        features = extract_stall_features(t[start:end], x[start:end])
        rows.append({
            "window_start_s": float(t[start]),
            "window_end_s": float(t[end - 1]),
            "rms_fluctuation": features.rms_fluctuation,
            "peak_to_peak": features.peak_to_peak,
            "dominant_frequency_hz": features.dominant_frequency_hz,
            "dominant_amplitude": features.dominant_amplitude,
        })
    return rows
