# Propeller design-to-CFD workflow

## Current implementation
- Parametric blade station model and validation.
- Airfoil polar reader with interpolation and strict no-extrapolation behavior.
- Preliminary BEMT station integration implementation.
- Optional CadQuery loft adapter from normalized section coordinates.
- OpenFOAM steady MRF dictionary/case skeleton generator.
- Existing experimental-data and stall-analysis modules remain separate.

## BEMT assumptions and limitations
The solver is a preliminary steady blade-element/momentum implementation. Its
accuracy depends on appropriate section polars at representative Reynolds numbers,
consistent twist/pitch convention, radial station resolution, and valid operating
conditions. The current implementation is not yet independently benchmarked and
should not be used as a design authority. Compare against measured thrust/torque,
published propeller data, and a trusted reference implementation before relying on it.

## CAD limitations
The CadQuery adapter expects one normalized x-y airfoil coordinate CSV per radial
station. It generates a preliminary lofted blade solid. Hub generation, multi-blade
assembly, trailing-edge repair, watertightness checks, and CAD regression tests are
future work. Inspect exported STEP geometry before meshing.

## CFD limitations
The OpenFOAM generator creates starter dictionaries and metadata, not a complete
ready-to-run CFD case. A mesh, patch boundary conditions, turbulence fields,
mesh-quality checks, solver-version compatibility and convergence review remain
necessary. The next engineering milestone is automated geometry-to-Gmsh meshing
with named physical groups, then an OpenFOAM mesh conversion and validated MRF case.

## Validation gates before release
1. Verify BEMT against independent benchmark cases at several advance ratios.
2. Verify integrated thrust/torque convergence with radial station refinement.
3. Inspect CAD solids for self-intersection and trailing-edge defects.
4. Demonstrate mesh-quality acceptance and mesh-independence study.
5. Compare CFD thrust/torque with experimental uncertainty bounds.
