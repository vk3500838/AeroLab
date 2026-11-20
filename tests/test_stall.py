import numpy as np
import pytest
from aerolab.stall import extract_stall_features, band_rms, stft_map, compare_windows
from aerolab.exceptions import AnalysisError


def test_stall_features_find_known_tone():
    fs = 2000
    t = np.arange(0, 2, 1/fs)
    x = 0.4 + 0.7*np.sin(2*np.pi*30*t)
    result = extract_stall_features(t, x)
    assert result.dominant_frequency_hz == pytest.approx(30, abs=1)
    assert result.rms_fluctuation == pytest.approx(0.7/np.sqrt(2), rel=0.02)


def test_band_rms_detects_in_band_tone():
    fs = 2000
    t = np.arange(0, 2, 1/fs)
    x = np.sin(2*np.pi*80*t) + 0.2*np.sin(2*np.pi*500*t)
    value = band_rms(t, x, 60, 100)
    assert value == pytest.approx(1/np.sqrt(2), rel=0.03)


def test_stft_and_window_comparison():
    fs = 1000
    t = np.arange(0, 2, 1/fs)
    x = np.sin(2*np.pi*40*t)
    f, ts, mag = stft_map(t, x, nperseg=256)
    assert mag.shape == (len(f), len(ts))
    windows = compare_windows(t, x, window_s=0.5, step_s=0.25)
    assert len(windows) > 1


def test_irregular_time_rejected():
    t = np.array([0, .01, .02, .031, .04, .05, .06, .07,
                  .08, .09, .10, .11, .12, .13, .14, .15])
    with pytest.raises(AnalysisError):
        extract_stall_features(t, np.ones_like(t))
