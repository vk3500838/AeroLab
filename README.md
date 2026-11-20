# AeroLab

**Integrated aerospace design, simulation and experimental analysis platform.**

AeroLab is a modular engineering workbench intended to connect preliminary aerodynamic design, CFD automation, experimental signal processing, and validation in one reproducible workflow.

## Main workspaces

- **Design Studio:** parametric rotor/propeller definitions, airfoil section assignment, and future BEMT-based performance prediction.
- **CFD Studio:** planned CAD generation, rotating-domain setup, meshing, solver orchestration and post-processing. The first automated CFD target is parameterized propeller analysis.
- **Experimental Studio:** sensor calibration, stall-inception signal post-processing, FFT, Welch PSD, STFT, band energy and time-window feature extraction.
- **Validation Studio:** planned comparison of design estimates, CFD and experimental results.

## Current implementation

The current release contains a tested Python analysis core, propeller performance calculations, linear sensor calibration, first-order uncertainty utilities, signal-processing tools for stall investigations, parametric blade-station definitions, command-line workflows, report generation, tests and CI.

CAD/mesh/CFD automation and BEMT are explicitly planned, not represented as completed features. See [ROADMAP.md](ROADMAP.md) and [platform architecture](docs/PLATFORM_ARCHITECTURE.md).

## Install

```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
pip install -e ".[dev]"
pytest
```

## Existing workflows

```bash
aerolab analyze examples/data/propeller_run.csv --output outputs/demo
aerolab spectrum examples/data/vibration_signal.csv --signal vibration_m_s2 --fs 2000 --output outputs/spectrum
```

## Engineering integrity

AeroLab reports measurable signal features; it does not automatically declare stall without validated criteria. Likewise, automated CFD will require geometry/mesh quality checks, solver convergence monitoring and validation. A generated result is not automatically a trustworthy result.


## Propeller design workflow

AeroLab now includes a parametric blade definition, airfoil polar interpolation,
a preliminary BEMT implementation, an optional CadQuery STEP loft adapter, and
an OpenFOAM MRF case-dictionary generator. See
[docs/PROPELLER_WORKFLOW.md](docs/PROPELLER_WORKFLOW.md).

Example CLI commands:

```bash
aerolab bemt examples/designs/demo_blade.json --polar examples/airfoils/demo_polar.csv --airspeed 12
aerolab openfoam-case --rpm 8000 --inlet-velocity 12 --output outputs/foam_case
```

The BEMT implementation and CFD workflow are engineering prototypes requiring
benchmark validation. The OpenFOAM generator creates starter dictionaries only;
it does not yet generate a complete mesh or a ready-to-run validated case.
