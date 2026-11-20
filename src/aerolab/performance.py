import numpy as np
import pandas as pd

from .exceptions import DataValidationError

RPM_TO_RPS = 1.0 / 60.0


def calculate_performance(frame: pd.DataFrame) -> pd.DataFrame:
    """Calculate standard propeller performance quantities using SI inputs."""
    required = {
        "rpm", "thrust_N", "torque_Nm", "airspeed_m_s",
        "density_kg_m3", "diameter_m",
    }
    missing = required.difference(frame.columns)
    if missing:
        raise DataValidationError(f"Missing performance columns: {sorted(missing)}")

    out = frame.copy()
    n = out["rpm"].to_numpy(dtype=float) * RPM_TO_RPS
    rho = out["density_kg_m3"].to_numpy(dtype=float)
    d = out["diameter_m"].to_numpy(dtype=float)
    thrust = out["thrust_N"].to_numpy(dtype=float)
    torque = out["torque_Nm"].to_numpy(dtype=float)
    velocity = out["airspeed_m_s"].to_numpy(dtype=float)

    omega = 2.0 * np.pi * n
    power = torque * omega
    out["rev_per_s"] = n
    out["omega_rad_s"] = omega
    out["shaft_power_W"] = power
    out["advance_ratio_J"] = velocity / (n * d)
    out["thrust_coefficient_CT"] = thrust / (rho * n**2 * d**4)
    out["power_coefficient_CP"] = np.divide(
        power, rho * n**3 * d**5, out=np.full_like(power, np.nan), where=power > 0
    )
    out["propulsive_efficiency"] = np.divide(
        thrust * velocity, power, out=np.full_like(power, np.nan), where=power > 0
    )
    return out


def blade_passing_frequency(rpm: float, blade_count: int) -> float:
    if rpm <= 0 or blade_count <= 0:
        raise ValueError("rpm and blade_count must be positive.")
    return rpm / 60.0 * blade_count
