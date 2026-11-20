"""Steady blade-element/momentum propeller performance solver.

Convention: beta is blade pitch angle measured from the rotor plane normal
(axis direction); alpha = beta - inflow angle. Positive thrust/torque are
defined for propulsive operation. This is a preliminary model, not CFD.
"""
from dataclasses import dataclass
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from .design import BladeDefinition
from .polars import AirfoilPolar


@dataclass
class BEMTResult:
    thrust_N: float
    torque_Nm: float
    shaft_power_W: float
    efficiency: float
    advance_ratio: float
    thrust_coefficient: float
    power_coefficient: float
    converged_sections: int
    total_sections: int
    station_data: pd.DataFrame


def _prandtl_loss(blade_count, radius, hub_radius, tip_radius, phi):
    sin_phi = max(abs(np.sin(phi)), 1e-6)
    f_tip = blade_count / 2 * (tip_radius - radius) / (radius * sin_phi)
    f_hub = blade_count / 2 * (radius - hub_radius) / (hub_radius * sin_phi) if hub_radius > 0 else 50
    tip = 2 / np.pi * np.arccos(np.clip(np.exp(-max(f_tip, 0)), 0, 1))
    hub = 2 / np.pi * np.arccos(np.clip(np.exp(-max(f_hub, 0)), 0, 1))
    return max(float(tip * hub), 1e-3)


def solve_bemt(blade: BladeDefinition, polar: AirfoilPolar, airspeed_m_s,
               density_kg_m3=1.225, max_iterations=300, tolerance=1e-5):
    """Solve annular blade elements with a scalar inflow-angle root per station."""
    blade.validate()
    if airspeed_m_s < 0 or density_kg_m3 <= 0:
        raise ValueError("Airspeed must be non-negative and density positive.")
    omega = blade.rpm * 2*np.pi/60
    radius = blade.diameter_m/2
    hub = blade.hub_diameter_m/2
    r_nodes = np.asarray(blade.radial_fraction)*radius
    chords = np.asarray(blade.chord_m)
    betas = np.deg2rad(np.asarray(blade.twist_deg))
    rows = []
    for r, chord, beta in zip(r_nodes, chords, betas):
        sigma = blade.blade_count*chord/(2*np.pi*r)
        tangential_speed = omega*r
        def residual(phi):
            alpha = np.rad2deg(beta-phi)
            try:
                cl, cd = polar.coefficients(alpha)
            except ValueError:
                # Root search outside polar range: penalize rather than extrapolate.
                return np.nan
            cl, cd = float(cl), float(cd)
            cn = cl*np.cos(phi)-cd*np.sin(phi)
            ct = cl*np.sin(phi)+cd*np.cos(phi)
            F = _prandtl_loss(blade.blade_count, r, hub, radius, phi)
            # Momentum relation for propeller axial inflow; use robust BEMT
            # inflow-angle residual with axial velocity V + induced velocity.
            v_axial = airspeed_m_s
            if abs(cn) < 1e-9 or abs(ct) < 1e-9:
                return np.nan
            a_term = 4*F*np.sin(phi)**2/(sigma*cn)
            ap_term = 4*F*np.sin(phi)*np.cos(phi)/(sigma*ct)
            if a_term <= -0.95 or ap_term <= -0.95:
                return np.nan
            return np.tan(phi) - (v_axial*(1+a_term))/(tangential_speed*(1-ap_term))
        # Search only physically relevant positive inflow angles, avoid extrapolating polars.
        lo, hi = np.deg2rad(0.5), np.deg2rad(75)
        grid = np.linspace(lo, hi, 250)
        vals = [residual(x) for x in grid]
        bracket = None
        for x0, x1, y0, y1 in zip(grid[:-1], grid[1:], vals[:-1], vals[1:]):
            if np.isfinite(y0) and np.isfinite(y1) and y0*y1 <= 0:
                bracket = (x0, x1)
                break
        if bracket is None:
            continue
        phi = brentq(residual, *bracket, xtol=tolerance, maxiter=max_iterations)
        alpha = np.rad2deg(beta-phi)
        cl, cd = [float(v) for v in polar.coefficients(alpha)]
        q = 0.5*density_kg_m3*((airspeed_m_s)**2+(omega*r)**2)
        lift_per_span = q*chord*cl
        drag_per_span = q*chord*cd
        dT_dr = blade.blade_count*(lift_per_span*np.cos(phi)-drag_per_span*np.sin(phi))
        dQ_dr = blade.blade_count*r*(lift_per_span*np.sin(phi)+drag_per_span*np.cos(phi))
        rows.append({"r_m":r, "r_over_R":r/radius, "chord_m":chord,
                     "twist_deg":np.rad2deg(beta), "phi_deg":np.rad2deg(phi),
                     "alpha_deg":alpha, "cl":cl, "cd":cd,
                     "dT_dr_N_m":dT_dr, "dQ_dr_Nm_m":dQ_dr})
    if len(rows) < max(3, len(r_nodes)//2):
        raise RuntimeError(
            "BEMT did not find enough valid station solutions. Check blade pitch, "
            "airfoil polar range, radial stations and operating point."
        )
    stations = pd.DataFrame(rows).sort_values("r_m")
    thrust = float(np.trapz(stations.dT_dr_N_m, stations.r_m))
    torque = float(np.trapz(stations.dQ_dr_Nm_m, stations.r_m))
    power = torque*omega
    n = blade.rpm/60
    J = airspeed_m_s/(n*blade.diameter_m)
    ct = thrust/(density_kg_m3*n*n*blade.diameter_m**4)
    cp = power/(density_kg_m3*n**3*blade.diameter_m**5)
    eta = thrust*airspeed_m_s/power if power > 0 else float("nan")
    return BEMTResult(thrust, torque, power, eta, J, ct, cp,
                      len(rows), len(r_nodes), stations)
