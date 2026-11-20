import pytest
from aerolab.uncertainty import shaft_power_uncertainty, expanded_uncertainty


def test_power_uncertainty_is_nonnegative():
    value = shaft_power_uncertainty(.1, .002, 2400, 2)
    assert value > 0


def test_expanded_uncertainty():
    assert expanded_uncertainty(0.2, 2) == pytest.approx(0.4)
