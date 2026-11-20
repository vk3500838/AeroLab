import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .io import load_propeller_data, load_signal_data
from .performance import calculate_performance
from .report import create_campaign_report
from .signal import estimate_sampling_frequency, amplitude_spectrum, welch_psd, dominant_peaks
from .design import BladeDefinition
from .polars import AirfoilPolar
from .bemt import solve_bemt
from .openfoam import generate_mrf_case


def _analyze(args):
    raw = load_propeller_data(args.input)
    result = calculate_performance(raw)
    summary = create_campaign_report(result, args.output)
    print(json.dumps({"status": "success", "output": str(args.output),
                      "rows": summary["row_count"]}, indent=2))


def _spectrum(args):
    frame = load_signal_data(args.input)
    if args.signal not in frame:
        raise SystemExit(f"Signal column not found: {args.signal}")
    fs = args.fs or estimate_sampling_frequency(frame["time_s"].to_numpy())
    frequency, amplitude = amplitude_spectrum(frame[args.signal].to_numpy(), fs)
    psd_f, psd = welch_psd(frame[args.signal].to_numpy(), fs)
    peaks = dominant_peaks(frequency, amplitude, args.peaks, args.minimum_frequency)

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    import pandas as pd
    pd.DataFrame({"frequency_hz": frequency, "amplitude": amplitude}).to_csv(
        output / "amplitude_spectrum.csv", index=False)
    pd.DataFrame({"frequency_hz": psd_f, "psd": psd}).to_csv(
        output / "welch_psd.csv", index=False)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(frequency, amplitude)
    ax.set(xlabel="Frequency (Hz)", ylabel="Amplitude", title=args.signal)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output / "spectrum.png", dpi=180)
    plt.close(fig)
    (output / "peaks.json").write_text(json.dumps(peaks, indent=2))
    print(json.dumps({"status": "success", "sampling_frequency_hz": fs,
                      "dominant_peaks": peaks, "output": str(output)}, indent=2))



def _bemt(args):
    import json
    data = json.loads(Path(args.design).read_text())
    blade = BladeDefinition(
        diameter_m=data["diameter_m"], hub_diameter_m=data["hub_diameter_m"],
        blade_count=data["blade_count"], rpm=data["rpm"],
        radial_fraction=tuple(data["radial_fraction"]), chord_m=tuple(data["chord_m"]),
        twist_deg=tuple(data["twist_deg"]), airfoil_names=tuple(data["airfoil_names"]))
    polar = AirfoilPolar.from_csv(args.polar)
    result = solve_bemt(blade, polar, args.airspeed, args.density)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    result.station_data.to_csv(out/"bemt_radial_results.csv", index=False)
    summary = {k: getattr(result, k) for k in (
        "thrust_N","torque_Nm","shaft_power_W","efficiency","advance_ratio",
        "thrust_coefficient","power_coefficient","converged_sections","total_sections")}
    (out/"bemt_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


def _openfoam(args):
    path = generate_mrf_case(args.output, args.rpm, args.inlet_velocity, args.density)
    print(f"Generated OpenFOAM starter case at {path}. Review README_CASE.md before running.")


def build_parser():
    parser = argparse.ArgumentParser(prog="aerolab",
        description="Analyze propeller experiments and rotor time-series signals.")
    sub = parser.add_subparsers(dest="command", required=True)

    analyze = sub.add_parser("analyze", help="Analyze a propeller operating-point CSV.")
    analyze.add_argument("input")
    analyze.add_argument("--output", default="outputs/campaign")
    analyze.set_defaults(func=_analyze)

    spectrum = sub.add_parser("spectrum", help="Compute FFT amplitude spectrum and Welch PSD.")
    spectrum.add_argument("input")
    spectrum.add_argument("--signal", required=True)
    spectrum.add_argument("--fs", type=float, default=None)
    spectrum.add_argument("--peaks", type=int, default=5)
    spectrum.add_argument("--minimum-frequency", type=float, default=0.0)
    spectrum.add_argument("--output", default="outputs/spectrum")
    spectrum.set_defaults(func=_spectrum)
    return parser


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
