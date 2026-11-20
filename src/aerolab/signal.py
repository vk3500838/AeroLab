import numpy as np
from scipy import signal as scipy_signal

from .exceptions import AnalysisError


def estimate_sampling_frequency(time_s, uniformity_tolerance=0.01):
    t = np.asarray(time_s, dtype=float)
    if t.ndim != 1 or len(t) < 4 or not np.isfinite(t).all():
        raise AnalysisError("time_s must be a finite 1-D array with at least four samples.")
    dt = np.diff(t)
    if np.any(dt <= 0):
        raise AnalysisError("Timestamps must be strictly increasing.")
    median_dt = float(np.median(dt))
    relative_spread = float(np.max(np.abs(dt - median_dt)) / median_dt)
    if relative_spread > uniformity_tolerance:
        raise AnalysisError(
            f"Sampling is not sufficiently uniform (relative interval deviation "
            f"{relative_spread:.3%}). Resample before FFT analysis."
        )
    return 1.0 / median_dt


def amplitude_spectrum(values, sampling_frequency):
    """Return single-sided amplitude spectrum using a Hann window."""
    x = np.asarray(values, dtype=float)
    if x.ndim != 1 or len(x) < 4 or not np.isfinite(x).all():
        raise AnalysisError("Signal must be a finite 1-D array with at least four samples.")
    if sampling_frequency <= 0:
        raise ValueError("sampling_frequency must be positive.")
    x = scipy_signal.detrend(x, type="constant")
    window = np.hanning(len(x))
    coherent_gain = np.sum(window) / len(x)
    spectrum = np.fft.rfft(x * window)
    amplitude = np.abs(spectrum) / (len(x) * coherent_gain)
    if len(x) % 2 == 0:
        amplitude[1:-1] *= 2
    else:
        amplitude[1:] *= 2
    frequency = np.fft.rfftfreq(len(x), d=1.0 / sampling_frequency)
    return frequency, amplitude


def welch_psd(values, sampling_frequency, segment_length=None):
    x = np.asarray(values, dtype=float)
    if x.ndim != 1 or len(x) < 4 or not np.isfinite(x).all():
        raise AnalysisError("Signal must be a finite 1-D array with at least four samples.")
    if sampling_frequency <= 0:
        raise ValueError("sampling_frequency must be positive.")
    nperseg = segment_length or min(1024, len(x))
    if nperseg < 4:
        raise ValueError("segment_length must be at least four.")
    return scipy_signal.welch(x, fs=sampling_frequency, nperseg=min(nperseg, len(x)))


def dominant_peaks(frequency, amplitude, count=5, minimum_frequency=0.0):
    f = np.asarray(frequency)
    a = np.asarray(amplitude)
    mask = f >= minimum_frequency
    if not mask.any():
        return []
    local_f, local_a = f[mask], a[mask]
    peaks, _ = scipy_signal.find_peaks(local_a)
    ranked = sorted(peaks, key=lambda idx: local_a[idx], reverse=True)[:count]
    return [{"frequency_hz": float(local_f[i]), "amplitude": float(local_a[i])}
            for i in ranked]
