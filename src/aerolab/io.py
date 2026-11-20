from pathlib import Path
import numpy as np
import pandas as pd

from .exceptions import DataValidationError

REQUIRED_COLUMNS = {
    "run_id", "time_s", "rpm", "thrust_N", "torque_Nm",
    "airspeed_m_s", "density_kg_m3", "diameter_m",
}


def load_propeller_data(path: str | Path) -> pd.DataFrame:
    """Load and validate a propeller operating-point CSV."""
    path = Path(path)
    if not path.exists():
        raise DataValidationError(f"Input file does not exist: {path}")
    try:
        frame = pd.read_csv(path)
    except Exception as exc:
        raise DataValidationError(f"Could not read CSV: {exc}") from exc

    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise DataValidationError(f"Missing required columns: {sorted(missing)}")
    if frame.empty:
        raise DataValidationError("Input CSV contains no data rows.")

    numeric = REQUIRED_COLUMNS.difference({"run_id"})
    for column in numeric:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    bad = [c for c in numeric if frame[c].isna().any()]
    if bad:
        raise DataValidationError(f"Non-numeric or missing values in: {sorted(bad)}")
    if not np.isfinite(frame[list(numeric)].to_numpy(dtype=float)).all():
        raise DataValidationError("Input contains infinite or non-finite numeric values.")
    if (frame["rpm"] <= 0).any():
        raise DataValidationError("rpm must be positive.")
    if (frame["density_kg_m3"] <= 0).any() or (frame["diameter_m"] <= 0).any():
        raise DataValidationError("Density and diameter must be positive.")
    if (frame["thrust_N"] < 0).any() or (frame["torque_Nm"] < 0).any():
        raise DataValidationError("Thrust and torque must be non-negative.")
    if (frame["airspeed_m_s"] < 0).any():
        raise DataValidationError("Airspeed must be non-negative.")
    return frame.sort_values(["run_id", "time_s"]).reset_index(drop=True)


def load_signal_data(path: str | Path) -> pd.DataFrame:
    """Load a time-series CSV and check timestamp integrity."""
    path = Path(path)
    if not path.exists():
        raise DataValidationError(f"Input file does not exist: {path}")
    frame = pd.read_csv(path)
    if "time_s" not in frame:
        raise DataValidationError("Signal CSV must contain a time_s column.")
    if len(frame) < 4:
        raise DataValidationError("At least four samples are required.")
    frame["time_s"] = pd.to_numeric(frame["time_s"], errors="coerce")
    if frame["time_s"].isna().any():
        raise DataValidationError("time_s contains missing or non-numeric values.")
    if not np.isfinite(frame["time_s"].to_numpy()).all():
        raise DataValidationError("time_s contains non-finite values.")
    if not frame["time_s"].is_monotonic_increasing:
        raise DataValidationError("time_s must be strictly increasing.")
    if np.any(np.diff(frame["time_s"].to_numpy()) <= 0):
        raise DataValidationError("time_s must not contain duplicate timestamps.")
    return frame
