import numpy as np
import pytest
from aerolab.polars import AirfoilPolar
from aerolab.design import BladeDefinition


def test_polar_interpolation_and_no_extrapolation():
    p = AirfoilPolar([-10, 0, 10], [-0.8, 0, 0.8], [.04, .01, .04])
    cl, cd = p.coefficients(5)
    assert float(cl) == pytest.approx(.4)
    assert float(cd) == pytest.approx(.025)
    with pytest.raises(ValueError):
        p.coefficients(12)


def test_blade_validation():
    b = BladeDefinition(.25, .025, 2, 7000,
        (.15,.35,.55,.75,.95), (.02,.03,.03,.02,.01),
        (35,27,20,13,7), ("a","a","a","a","a"))
    assert len(b.stations()) == 5
