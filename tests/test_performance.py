import numpy as np
import pandas as pd
import pytest
from aerolab.performance import calculate_performance, blade_passing_frequency


def sample():
    return pd.DataFrame({
        "rpm": [2400.0], "thrust_N": [5.0], "torque_Nm": [0.12],
        "airspeed_m_s": [10.0], "density_kg_m3": [1.225], "diameter_m": [0.254],
    })


def test_power_matches_torque_times_angular_speed():
    result = calculate_performance(sample())
    expected = 0.12 * 2 * np.pi * 2400 / 60
    assert result.loc[0, "shaft_power_W"] == pytest.approx(expected)


def test_advance_ratio():
    result = calculate_performance(sample())
    expected = 10.0 / (40.0 * 0.254)
    assert result.loc[0, "advance_ratio_J"] == pytest.approx(expected)


def test_blade_passing_frequency():
    assert blade_passing_frequency(2400, 15) == pytest.approx(600.0)


@pytest.mark.parametrize("rpm,blades", [(0, 2), (1000, 0), (-1, 3)])
def test_bpf_rejects_nonphysical_values(rpm, blades):
    with pytest.raises(ValueError):
        blade_passing_frequency(rpm, blades)
