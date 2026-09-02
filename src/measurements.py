"""
Measurement plotting for bundle latency tests.

Usage
-----
1. Run the bundle client once with ODRL and once without (same client.py):
       python src/client.py --all --repeat 10
2. Copy the per-call latency values printed by the client into the DATA dict
   below (values in milliseconds, one per call, in call order).
3. Generate the charts:
       python src/measurements.py

This produces one line chart per bundle (bundle1.png, bundle2.png,
bundle3.png). Each chart shows the latency on the y-axis against the call
number on the x-axis, with an "with ODRL" line and, when available, an
"without ODRL" line.
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Paste your measurements here (in milliseconds, one per call, in call order).
# Leave "no_odrl" empty until you have the ODRL-free run.
# ---------------------------------------------------------------------------
DATA = {
    "bundle1": {
        "odrl": [],  # e.g. [12.3, 11.8, 12.1, ...]
        "no_odrl": [],
    },
    "bundle2": {
        "odrl": [],
        "no_odrl": [],
    },
    "bundle3": {
        "odrl": [],
        "no_odrl": [],
    },
}

OUTPUT_DIR = "charts"


def plot_bundle(bundle: str, series: dict, outdir: str) -> str:
    """Plot the latency line chart for a single bundle."""
    plt.figure(figsize=(8, 5))

    lines = [
        ("with ODRL", series.get("odrl")),
        ("without ODRL", series.get("no_odrl")),
    ]
    plotted = 0
    for label, values in lines:
        if not values:
            continue
        xs = list(range(1, len(values) + 1))
        plt.plot(xs, values, marker="o", label=label)
        plotted += 1

    if plotted == 0:
        plt.close()
        raise ValueError(f"No data provided for '{bundle}'.")

    plt.xlabel("Call number")
    plt.ylabel("Latency (ms)")
    plt.title(bundle)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)

    path = os.path.join(outdir, f"{bundle}.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def main() -> int:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    saved = []
    for bundle, series in DATA.items():
        if not any(series.values()):
            print(f"[skip] {bundle}: no data")
            continue
        path = plot_bundle(bundle, series, OUTPUT_DIR)
        saved.append(path)
        print(f"[saved] {path}")

    if not saved:
        print("No charts generated: paste measurements into DATA first.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
