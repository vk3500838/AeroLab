import numpy as np
import pytest
from aerolab.signal import estimate_sampling_frequency, amplitude_spectrum, dominant_peaks
from aerolab.exceptions import AnalysisError


def test_sampling_frequency():
    t = np.arange(0, 1, 1/1000)
    assert estimate_sampling_frequency(t) == pytest.approx(1000)


def test_fft_finds_sine_frequency():
    fs = 2048
    t = np.arange(0, 2, 1/fs)
    x = 2.5 * np.sin(2*np.pi*120*t)
    f, a = amplitude_spectrum(x, fs)
    peaks = dominant_peaks(f, a, count=1, minimum_frequency=10)
    assert peaks[0]["frequency_hz"] == pytest.approx(120, abs=1)


def test_irregular_sampling_rejected():
    t = np.array([0, .01, .02, .031, .04, .05])
    with pytest.raises(AnalysisError):
        estimate_sampling_frequency(t)
