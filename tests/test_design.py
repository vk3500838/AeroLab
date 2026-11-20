import pytest
from aerolab.design import BladeDefinition


def sample_blade():
    return BladeDefinition(
        diameter_m=0.254, hub_diameter_m=0.0254, blade_count=2, rpm=8000,
        radial_fraction=(0.15, 0.35, 0.6, 0.85, 1.0),
        chord_m=(0.025, 0.032, 0.03, 0.02, 0.008),
        twist_deg=(35, 27, 18, 10, 5),
        airfoil_names=("ClarkY", "ClarkY", "NACA4412", "NACA4412", "NACA4412"),
    )


def test_blade_station_generation():
    stations = sample_blade().stations()
    assert len(stations) == 5
    assert stations[0]["radius_m"] == pytest.approx(0.01905)


def test_invalid_chord_rejected():
    blade = sample_blade()
    invalid = BladeDefinition(**{**blade.__dict__, "chord_m": (0, 0.03, 0.03, 0.02, 0.01)})
    with pytest.raises(ValueError):
        invalid.validate()
