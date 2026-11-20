# AeroLab Roadmap

## Product Vision

AeroLab is an integrated propeller design, aerodynamic analysis, CFD and optimization platform.

The long-term objective is to automate the propeller development workflow, from initial design requirements to optimized blade geometry, CFD evaluation and downloadable engineering deliverables.

## Phase 1 — Propeller Design Foundation

- [x] Parametric blade-station data model
- [x] Airfoil polar CSV import and interpolation
- [x] Preliminary BEMT solver prototype
- [x] Propeller performance calculations
- [x] Command-line interface
- [x] Automated test foundation
- [ ] Validate BEMT against trusted experimental and numerical reference data
- [ ] Improve induction-factor convergence and tip/hub loss modelling
- [ ] Support Reynolds-number-dependent airfoil polars
- [ ] Generate radial chord, twist and pitch distributions
- [ ] Generate propeller performance maps across operating conditions

## Phase 2 — Parametric CAD Generation

- [ ] Generate complete 3D propeller blade geometry
- [ ] Generate hub and multi-blade assemblies
- [ ] Support variable chord, twist, sweep and skew distributions
- [ ] Support different airfoil sections along the blade
- [ ] Add geometry validation and repair
- [ ] Export STEP, STL and other supported CAD formats

## Phase 3 — CFD Automation

- [x] Initial OpenFOAM MRF dictionary generator
- [ ] Automated computational-domain generation
- [ ] Rotating and stationary domain configuration
- [ ] Automated meshing using Gmsh and/or OpenFOAM meshing tools
- [ ] Mesh quality checks and mesh-independence studies
- [ ] Complete OpenFOAM case generation and boundary conditions
- [ ] Automated solver execution
- [ ] Convergence and force-monitoring tools

## Phase 4 — CFD Visualization and Results

- [ ] Pressure and velocity contour visualization
- [ ] Blade-surface pressure distribution
- [ ] Streamline and wake visualization
- [ ] Vorticity and turbulence-field visualization
- [ ] Thrust, torque and power extraction from CFD
- [ ] BEMT versus CFD comparison
- [ ] Export plots, contours and simulation fields
- [ ] Generate downloadable engineering reports

## Phase 5 — Propeller Optimization

- [ ] Differential Evolution optimization
- [ ] Genetic Algorithm-based optimization
- [ ] Multi-objective optimization using NSGA-II
- [ ] Chord and twist distribution optimization
- [ ] Airfoil selection and section optimization
- [ ] Blade sweep, skew and geometric optimization
- [ ] Optimize efficiency, thrust and power objectives
- [ ] Generate and visualize Pareto fronts
- [ ] Explore surrogate-assisted optimization

## Phase 6 — Automated Propeller Design

- [ ] Generate initial propeller designs from user requirements
- [ ] Automatically evaluate candidate geometries
- [ ] Integrate aerodynamic analysis and CFD evaluation
- [ ] Automatically optimize feasible designs
- [ ] Compare alternative designs and operating conditions
- [ ] Generate final CAD geometry and engineering reports

## Phase 7 — Extended Propeller Configurations

- [ ] Fixed-pitch propellers
- [ ] Variable-pitch propellers
- [ ] Ducted propellers and fans
- [ ] Contra-rotating propellers
- [ ] Coaxial propeller configurations
- [ ] Multirotor propeller configurations
- [ ] Configuration-specific aerodynamic and CFD models

## Phase 8 — Integrated Engineering Application

- [ ] Develop a graphical desktop interface
- [ ] Integrate design, analysis, CAD and CFD workflows
- [ ] Provide interactive geometry and results visualization
- [ ] Enable downloadable CAD, plots, contours and reports
- [ ] Support reusable engineering projects and configurations

## Engineering Principles

- Modular and maintainable software architecture
- Automated testing and continuous integration
- Aerodynamic validation against trusted reference data
- Reproducible CFD workflows
- Transparent reporting of assumptions and limitations
- Separation of implemented, experimental and planned capabilities

## Current Development Priority

The immediate priority is to establish a reliable propeller design and aerodynamic analysis foundation, validate the BEMT implementation, and develop complete parametric CAD generation before expanding into automated CFD and optimization.