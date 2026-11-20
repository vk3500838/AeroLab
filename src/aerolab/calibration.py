from dataclasses import dataclass
import numpy as np
import pandas as pd

from .exceptions import DataValidationError


@dataclass(frozen=True)
class LinearCalibration:
    """Linear sensor calibration: engineering_value = slope * raw + intercept."""
    slope: float
    intercept: float
    input_unit: str = "V"
    output_unit: str = "N"
    slope_std: float = 0.0
    intercept_std: float = 0.0

    def __post_init__(self):
        values = [self.slope, self.intercept, self.slope_std, self.intercept_std]
        if not np.isfinite(values).all():
            raise ValueError("Calibration parameters must be finite.")
        if self.slope_std < 0 or self.intercept_std < 0:
            raise ValueError("Calibration standard uncertainties cannot be negative.")

    def apply(self, raw):
        values = np.asarray(raw, dtype=float)
        if not np.isfinite(values).all():
            raise DataValidationError("Raw calibration input contains non-finite values.")
        return self.slope * values + self.intercept

    def standard_uncertainty(self, raw, raw_std):
        """Independent first-order uncertainty, including raw, slope and intercept terms."""
        x = np.asarray(raw, dtype=float)
        u_x = np.asarray(raw_std, dtype=float)
        if np.any(u_x < 0):
            raise ValueError("raw_std cannot be negative.")
        return np.sqrt(
            (self.slope * u_x) ** 2
            + (x * self.slope_std) ** 2
            + self.intercept_std ** 2
        )


def calibrate_column(frame: pd.DataFrame, source: str, target: str,
                     calibration: LinearCalibration) -> pd.DataFrame:
    if source not in frame:
        raise DataValidationError(f"Source column not found: {source}")
    result = frame.copy()
    result[target] = calibration.apply(result[source].to_numpy())
    return result
