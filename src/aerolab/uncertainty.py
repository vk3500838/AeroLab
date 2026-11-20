import numpy as np


def product_uncertainty(value_a, std_a, value_b, std_b):
    """Standard uncertainty of a*b for independent inputs, first-order propagation."""
    if std_a < 0 or std_b < 0:
        raise ValueError("Standard uncertainties cannot be negative.")
    return float(np.sqrt((value_b * std_a) ** 2 + (value_a * std_b) ** 2))


def shaft_power_uncertainty(torque_Nm, torque_std_Nm, rpm, rpm_std):
    """Uncertainty of P=Q*2*pi*rpm/60 for independent Q and rpm."""
    if torque_std_Nm < 0 or rpm_std < 0:
        raise ValueError("Standard uncertainties cannot be negative.")
    factor = 2.0 * np.pi / 60.0
    dP_dQ = factor * rpm
    dP_dRPM = factor * torque_Nm
    return float(np.sqrt((dP_dQ * torque_std_Nm) ** 2
                         + (dP_dRPM * rpm_std) ** 2))


def expanded_uncertainty(standard_uncertainty, coverage_factor=2.0):
    if standard_uncertainty < 0 or coverage_factor <= 0:
        raise ValueError("Uncertainty must be non-negative and coverage factor positive.")
    return float(standard_uncertainty * coverage_factor)
