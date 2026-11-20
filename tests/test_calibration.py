import numpy as np
import pytest
from aerolab.calibration import LinearCalibration


def test_linear_calibration():
    calibration = LinearCalibration(slope=10, intercept=-2)
    assert np.allclose(calibration.apply([0, 1, 2]), [-2, 8, 18])


def test_calibration_uncertainty():
    calibration = LinearCalibration(2, 1, slope_std=0.1, intercept_std=0.2)
    value = calibration.standard_uncertainty(raw=[3], raw_std=[0.5])
    assert value[0] == pytest.approx(np.sqrt(1.0 + 0.09 + 0.04))
