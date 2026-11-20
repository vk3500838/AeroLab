"""Airfoil polar loading and interpolation."""
from pathlib import Path
import numpy as np
import pandas as pd
from .exceptions import DataValidationError


class AirfoilPolar:
    """2-D polar with alpha_deg, cl, cd columns; linear interpolation in alpha."""
    def __init__(self, alpha_deg, cl, cd, name="airfoil"):
        a = np.asarray(alpha_deg, dtype=float)
        lift = np.asarray(cl, dtype=float)
        drag = np.asarray(cd, dtype=float)
        if a.ndim != 1 or len(a) < 3 or len(a) != len(lift) or len(a) != len(drag):
            raise DataValidationError("Polar arrays must have equal length >=3.")
        if not (np.isfinite(a).all() and np.isfinite(lift).all() and np.isfinite(drag).all()):
            raise DataValidationError("Polar values must be finite.")
        order = np.argsort(a)
        a, lift, drag = a[order], lift[order], drag[order]
        if np.any(np.diff(a) <= 0) or np.any(drag <= 0):
            raise DataValidationError("Alpha values must be unique and Cd must be positive.")
        self.alpha_deg, self.cl, self.cd, self.name = a, lift, drag, name

    @classmethod
    def from_csv(cls, path, name=None):
        path = Path(path)
        if not path.exists():
            raise DataValidationError(f"Polar file not found: {path}")
        frame = pd.read_csv(path)
        required = {"alpha_deg", "cl", "cd"}
        if not required.issubset(frame.columns):
            raise DataValidationError(f"Polar CSV requires columns {sorted(required)}")
        return cls(frame.alpha_deg, frame.cl, frame.cd, name or path.stem)

    def coefficients(self, alpha_deg):
        """Interpolate within measured polar range; never silently extrapolate."""
        alpha = np.asarray(alpha_deg, dtype=float)
        if np.any(alpha < self.alpha_deg[0]) or np.any(alpha > self.alpha_deg[-1]):
            raise ValueError(
                f"Angle of attack outside {self.name} polar range "
                f"[{self.alpha_deg[0]}, {self.alpha_deg[-1]}] deg."
            )
        return (np.interp(alpha, self.alpha_deg, self.cl),
                np.interp(alpha, self.alpha_deg, self.cd))
