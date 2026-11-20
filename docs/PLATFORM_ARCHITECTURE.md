# AeroLab platform architecture

AeroLab is intended to be a modular aerospace engineering workbench. Its design,
CFD, experimental-analysis, and validation capabilities share data contracts,
units, project metadata, and reporting, but remain independently usable.

## Workspaces

### 1. Preliminary design
- Parametric blade/rotor definition.
- Airfoil coordinate library and section assignment.
- Chord, twist, radius and blade-count parameters.
- BEMT-based performance estimation and off-design sweeps (next implementation stage).
- Export of design stations to CAD-generation adapters.

### 2. CAD and CFD automation
A constrained, parameter-driven workflow is feasible:
1. Read a validated parametric design definition.
2. Generate blade section curves from airfoil coordinate files.
3. Loft sections into a blade solid and create hub/assembly geometry.
4. Build a surrounding flow domain and rotating/stationary regions.
5. Generate a mesh and run geometry/mesh quality checks.
6. Write solver dictionaries and boundary conditions from a reviewed case template.
7. Run the CFD solver, monitor residuals and force histories, and extract coefficients.
8. Compare results with a design model or experiment.

The first target should be propeller CFD because its geometry and operating conditions
are sufficiently parameterizable. This is not a universal push-button CFD system.
Automatic meshing and solver setup can fail on poor geometry, thin trailing edges,
highly twisted blades, bad periodic interfaces, or unsuitable cell quality. The
software must stop and report failures rather than silently producing questionable
results.

Potential implementation stack:
- CAD generation: CadQuery/OpenCascade or FreeCAD Python API.
- Meshing: Gmsh for controlled geometry/mesh workflows, or OpenFOAM
  blockMesh + snappyHexMesh for an OpenFOAM-native workflow.
- Solver: OpenFOAM, with MRF for an initial steady rotating-frame workflow;
  sliding mesh/transient rotor-stator interaction can be a later milestone.
- Post-processing: OpenFOAM function objects and Python readers/parsers.

External CAD/meshing/solver executables are dependencies; AeroLab orchestrates them
and records versions, settings, logs, and outputs. It does not replace their solvers.

### 3. Experimental aerodynamics and stall inception
This workspace is solver-independent and accepts time-series measurements such as
pressure, hot-wire, accelerometer, microphone, or other sensor channels.

Planned analyses:
- Time alignment, missing-data checks and sampling-rate verification.
- Calibration, detrending and filtering.
- RMS, peak-to-peak, skewness, kurtosis and band-limited energy.
- FFT amplitude spectrum and Welch PSD.
- STFT spectrogram and optional wavelet analysis.
- Blade-passing frequency and harmonic tracking when RPM/blade count are supplied.
- Windowed feature trends and comparison across operating conditions.
- Export of figures, feature tables and analysis metadata.

AeroLab will not label a record as stalled based only on a large spectral peak.
Stall inception criteria must be defined for the particular experiment and validated
against known pre-stall, inception and developed-stall records.

### 4. Validation and reporting
- Compare model predictions, CFD outputs and experimental measurements.
- Align operating points and units before comparison.
- Plot residuals, percentage differences and uncertainty bands.
- Preserve source file hashes, configuration, software versions and analysis timestamps.

## Design principle

Every calculation must have a documented equation, unit convention, assumptions,
failure modes and automated tests. Every automated simulation must retain its
input geometry, mesh settings, solver configuration, logs and convergence evidence.
