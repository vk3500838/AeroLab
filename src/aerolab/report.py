from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def create_campaign_report(frame: pd.DataFrame, output_dir: str | Path) -> dict:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    processed = frame.copy()
    processed.to_csv(output / "processed_data.csv", index=False)

    numeric_summary = processed.select_dtypes(include="number").describe().replace(
        {np.nan: None}
    ).to_dict()
    summary = {
        "row_count": int(len(processed)),
        "run_ids": [str(x) for x in processed["run_id"].drop_duplicates().tolist()]
                   if "run_id" in processed else [],
        "numeric_summary": numeric_summary,
        "generated_files": ["processed_data.csv", "performance_overview.png", "summary.json"],
    }
    (output / "summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False))

    fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
    x = processed["advance_ratio_J"]
    plots = [
        ("thrust_coefficient_CT", "Thrust coefficient, $C_T$"),
        ("power_coefficient_CP", "Power coefficient, $C_P$"),
        ("shaft_power_W", "Shaft power (W)"),
        ("propulsive_efficiency", "Propulsive efficiency"),
    ]
    for ax, (column, label) in zip(axes.flat, plots):
        for run_id, group in processed.groupby("run_id"):
            ax.plot(group["advance_ratio_J"], group[column], marker="o",
                    label=str(run_id))
        ax.set_xlabel("Advance ratio, J")
        ax.set_ylabel(label)
        ax.grid(True, alpha=0.3)
    axes.flat[0].legend(title="Run")
    fig.suptitle("AeroLab propeller performance overview")
    fig.savefig(output / "performance_overview.png", dpi=180)
    plt.close(fig)
    return summary
