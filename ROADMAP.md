# AeroLab roadmap

## Propeller-first product strategy
The first major product release focuses on a complete propeller design-to-analysis workflow.
Stall-inception processing remains a separate experimental-analysis workspace and is not
part of the initial propeller release scope.

### Implemented foundation
- [x] CSV ingestion, validation and reporting
- [x] Propeller performance coefficients
- [x] Sensor calibration and uncertainty utilities
- [x] FFT, Welch PSD, STFT and windowed stall signal features
- [x] Parametric blade station data model
- [x] Airfoil polar loader and interpolation
- [x] Preliminary BEMT solver prototype
- [x] Optional CadQuery loft adapter
- [x] OpenFOAM MRF dictionary generator
- [x] CLI and automated tests

### Propeller release milestones
- [ ] Benchmark BEMT against trusted reference datasets
- [ ] Reynolds-number-dependent polar management
- [ ] BEMT convergence and radial refinement study
- [ ] Blade geometry repair, hub and multi-blade assembly
- [ ] Automated Gmsh meshing with named boundary groups
- [ ] Mesh quality and mesh-independence reports
- [ ] Complete OpenFOAM case generation and boundary conditions
- [ ] Solver execution and residual/force convergence monitoring
- [ ] CFD post-processing and experimental validation
- [ ] Desktop engineering interface

### Separate future experimental release
- [ ] Stall-inception data campaign manager
- [ ] Sensor metadata and calibration records
- [ ] Advanced wavelet and time-frequency analysis
- [ ] Validated stall inception indicators
- [ ] Multi-sensor correlation and event annotation
