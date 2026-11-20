"""Parametric preliminary propeller blade definition and station export.

This module stores a design definition. It does not yet generate watertight
CAD or claim a converged BEMT solution.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import numpy as np


@dataclass(frozen=True)
class BladeDefinition:
    diameter_m: float
    hub_diameter_m: float
    blade_count: int
    rpm: float
    radial_fraction: tuple[float, ...]
    chord_m: tuple[float, ...]
    twist_deg: tuple[float, ...]
    airfoil_names: tuple[str, ...]

    def validate(self):
        n = len(self.radial_fraction)
        if self.diameter_m <= 0 or self.hub_diameter_m < 0:
            raise ValueError("Diameter must be positive and hub diameter non-negative.")
        if self.hub_diameter_m >= self.diameter_m:
            raise ValueError("Hub diameter must be smaller than propeller diameter.")
        if self.blade_count < 2 or self.rpm <= 0:
            raise ValueError("blade_count must be >=2 and rpm must be positive.")
        if n < 2 or not (len(self.chord_m) == len(self.twist_deg) == len(self.airfoil_names) == n):
            raise ValueError("All radial station arrays must have equal length >=2.")
        r = np.asarray(self.radial_fraction, dtype=float)
        c = np.asarray(self.chord_m, dtype=float)
        b = np.asarray(self.twist_deg, dtype=float)
        if not np.isfinite(r).all() or not np.isfinite(c).all() or not np.isfinite(b).all():
            raise ValueError("Station data must be finite.")
        if np.any(np.diff(r) <= 0) or r[0] <= self.hub_diameter_m / self.diameter_m or r[-1] > 1:
            raise ValueError("Radial fractions must increase from outside the hub to <=1.")
        if np.any(c <= 0):
            raise ValueError("Chord lengths must be positive.")
        if any(not name.strip() for name in self.airfoil_names):
            raise ValueError("Airfoil names cannot be blank.")
        return self

    def stations(self):
        self.validate()
        radius = self.diameter_m / 2.0
        return [
            {
                "radial_fraction": float(r),
                "radius_m": float(r * radius),
                "chord_m": float(c),
                "twist_deg": float(beta),
                "airfoil": airfoil,
            }
            for r, c, beta, airfoil in zip(
                self.radial_fraction, self.chord_m, self.twist_deg, self.airfoil_names
            )
        ]

    def export_json(self, path):
        self.validate()
        payload = asdict(self)
        payload["stations"] = self.stations()
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return Path(path)
