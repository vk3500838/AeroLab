# AeroLab

### Propeller Design, Aerodynamic Analysis, CFD and Optimization Platform

AeroLab is an open-source engineering software project focused on developing an integrated workflow for propeller design, aerodynamic performance prediction, computational fluid dynamics (CFD), geometry generation and design optimization.

The long-term goal is to automate the propeller development process, from initial design requirements to optimized blade geometry and downloadable engineering deliverables.

## Core Modules

### 1. Propeller Design Studio
- Parametric blade geometry definition
- Radial chord and twist distributions
- Airfoil section assignment
- Blade sweep, skew and geometric parameterization
- Support for different propeller configurations (planned)

### 2. Aerodynamic Analysis
- Airfoil polar import and interpolation
- Preliminary Blade Element Momentum Theory (BEMT)
- Thrust, torque and power calculations
- Propeller performance coefficients
- Performance analysis across operating conditions

### 3. CAD Generation
- Parametric blade geometry generation
- Airfoil-section-based blade construction
- STEP and STL export (under development)
- Hub and complete propeller assembly (planned)

### 4. CFD Automation
- OpenFOAM case configuration generation
- Rotating-domain and MRF workflow development
- Automated meshing and solver execution (planned)
- Pressure and velocity contour visualization (planned)
- CFD post-processing and downloadable results (planned)

### 5. Design Optimization
Planned optimization capabilities include:
- Differential Evolution
- Genetic Algorithms and multi-objective optimization
- Chord and twist distribution optimization
- Airfoil and blade geometry selection
- Efficiency, thrust and power optimization
- Surrogate-assisted optimization

### 6. Engineering Deliverables
The long-term platform will support downloadable:
- CAD geometry (STEP/STL)
- Blade geometry distributions (CSV)
- Performance plots and maps
- CFD contours and simulation fields
- Optimization results
- Engineering reports (PDF)

## Current Implementation

The current Python codebase includes:
- Parametric blade-station definitions
- Airfoil polar CSV import and interpolation
- Preliminary BEMT implementation
- Propeller performance calculations
- Optional CadQuery-based blade loft adapter
- OpenFOAM MRF starter dictionary generation
- Command-line workflows
- Automated tests and GitHub Actions CI

**Engineering status:** BEMT, CAD generation and CFD workflow components are prototypes. The OpenFOAM generator currently creates starter dictionaries, not a complete ready-to-run CFD case. Aerodynamic predictions require independent benchmark validation.

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

Run tests:

```powershell
pytest
```

## Example Workflows

Preliminary BEMT analysis:

```powershell
aerolab bemt examples/designs/demo_blade.json --polar examples/airfoils/demo_polar.csv --airspeed 12
```

Generate an OpenFOAM starter case:

```powershell
aerolab openfoam-case --rpm 8000 --inlet-velocity 12 --output outputs/foam_case
```

## Development Roadmap

1. Validate and improve the BEMT engine.
2. Develop complete parametric propeller CAD generation.
3. Automate CFD geometry preparation, meshing and simulation.
4. Add CFD visualization and engineering result exports.
5. Implement single-objective and multi-objective optimization.
6. Expand support for different propeller configurations.
7. Develop an integrated graphical engineering interface.

## Project Philosophy

AeroLab aims to connect aerodynamic theory, numerical simulation, geometry generation and optimization in one reproducible engineering workflow.

The project prioritizes modular software architecture, automated testing, engineering validation and transparent reporting of computational results.

## License

See the LICENSE file.
