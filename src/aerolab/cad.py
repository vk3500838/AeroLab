"""Optional CadQuery adapter for parametric propeller blade section lofting.

Install the optional dependency with: pip install -e '.[cad]'
This is a preliminary geometry generator. Validate exported solids in CAD before CFD.
"""
from pathlib import Path
import numpy as np
from .design import BladeDefinition


def generate_blade_step(blade: BladeDefinition, airfoil_files, output_step):
    try:
        import cadquery as cq
    except ImportError as exc:
        raise RuntimeError("CadQuery is optional. Install with: pip install -e '.[cad]'") from exc
    blade.validate()
    if len(airfoil_files) != len(blade.radial_fraction):
        raise ValueError("Provide one airfoil coordinate file per radial station.")
    sections = []
    R = blade.diameter_m/2
    for rfrac, chord, twist, path in zip(
        blade.radial_fraction, blade.chord_m, blade.twist_deg, airfoil_files
    ):
        coords = np.loadtxt(path, delimiter=",", comments="#")
        if coords.ndim != 2 or coords.shape[1] < 2 or len(coords) < 10:
            raise ValueError(f"Invalid airfoil coordinate file: {path}")
        xy = coords[:, :2]
        # Coordinates are expected normalized by chord; twist is about span axis.
        theta = np.deg2rad(twist)
        x = (xy[:, 0]-0.25)*chord
        y = xy[:, 1]*chord
        # chordwise coordinate lies tangentially; section plane normal is radial.
        tangential = x*np.cos(theta)-y*np.sin(theta)
        axial = x*np.sin(theta)+y*np.cos(theta)
        points = [cq.Vector(axial_i, tangential_i, rfrac*R)
                  for axial_i, tangential_i in zip(axial, tangential)]
        wire = cq.Wire.makePolygon(points + [points[0]])
        sections.append(wire)
    solid = cq.Solid.makeLoft(sections, ruled=False)
    cq.exporters.export(solid, str(output_step))
    return Path(output_step)
