import json
import os

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

sns.set_theme(style="whitegrid")


def create_timing_chart(data_path, output_path):
    """Generates and saves the snap timing chart."""
    with open(data_path, "r") as f:
        data = json.load(f)

    time = [d["time"] for d in data]
    rate = [d["rate"] for d in data]

    fig, ax = plt.subplots(figsize=(5, 2.5))
    ax.plot(time, rate, color="#3b82f6", linewidth=2)

    # Style the plot to match the poster
    ax.set_xlabel("Time (hrs)", fontsize=12)
    ax.set_ylabel("Snap Rate", fontsize=12)
    ax.set_xlim(0, 48)
    ax.set_ylim(25, 50)
    ax.set_xticks(range(0, 49, 6))
    ax.set_yticks(range(25, 51, 5))
    ax.tick_params(axis="both", which="major", labelsize=10)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()

    plt.savefig(output_path, format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)
    print(f"Saved snap rate figure to {output_path}")


def create_waveform_chart(data_path, output_path):
    """Generates and saves the single snap waveform chart."""
    with open(data_path, "r") as f:
        data = json.load(f)

    time = [d["time"] for d in data if d["time"] <= 2]
    amplitude = [d["amplitude"] for d in data if d["time"] <= 2]

    fig, ax = plt.subplots(figsize=(5, 2.5))
    ax.plot(time, amplitude, color="#14b8a6", linewidth=2)

    # Style the plot
    ax.set_xlabel("Time (ms)", fontsize=12)
    ax.set_ylabel("Normalised Amplitude", fontsize=12)
    ax.set_xlim(0, 2)
    ax.set_ylim(-1.1, 1.1)
    ax.tick_params(axis="both", which="major", labelsize=10)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()

    plt.savefig(output_path, format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)
    print(f"Saved snap waveform figure to {output_path}")


def create_amplitude_chart(data_path, output_path):
    """Generates and saves the amplitude distribution chart."""
    with open(data_path, "r") as f:
        data = json.load(f)

    histogram = data["histogram"]
    pdf = data["pdf"]
    plot_limits = data["plot_limits"]

    # Extract data for plotting
    bar_x = [item["x"] for item in histogram]
    bar_height = [item["y"] for item in histogram]
    bar_width = [item["width"] for item in histogram]

    pdf_x = [item["x"] for item in pdf]
    levy_pdf = [item["levy_pdf"] for item in pdf]
    gauss_pdf = [item["gauss_pdf"] for item in pdf]

    fig, ax = plt.subplots(figsize=(5, 2.5))

    # Plotting
    ax.bar(
        bar_x,
        bar_height,
        width=bar_width,
        color="cornflowerblue",
        alpha=0.6,
        label="Empirical Data",
        align="edge",
    )
    ax.plot(pdf_x, levy_pdf, color="#ff7260", linewidth=2.5, label="SαS")
    ax.plot(
        pdf_x,
        gauss_pdf,
        color="#6b7280",
        linestyle=(0, (4, 2)),
        linewidth=1.5,
        label="Gaussian",
    )

    # Style the plot
    ax.set_xlabel("Uncalibrated Pressure", fontsize=12)
    ax.set_ylabel("Probability Density", fontsize=12)
    ax.tick_params(axis="both", which="major", labelsize=10)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Apply plot limits from data
    ax.set_xlim(plot_limits["xlim"])
    ax.set_ylim(plot_limits["ylim"])

    # Custom tick formatters to match D3 style
    def x_formatter(x, pos):
        if abs(x) >= 1000:
            return f"{int(x / 1000)}k"
        return f"{int(x)}"

    def y_formatter(y, pos):
        if y == 0:
            return "0"
        # Format to exponential with 0 decimal places, e.g., 1e-4
        return f"{y:.0e}".replace("e-0", "e-")

    ax.xaxis.set_major_formatter(FuncFormatter(x_formatter))
    ax.yaxis.set_major_formatter(FuncFormatter(y_formatter))

    # Position legend below the chart
    ax.legend(
        fontsize=8,
        loc="upper right",
        ncol=1,
        frameon=False,  # No frame
    )

    plt.savefig(output_path, format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)
    print(f"Saved snap amplitude figure to {output_path}")


def main():
    """Main function to generate all figures."""
    # Define directories
    data_dir = "data"
    assets_dir = "assets"

    # Create assets directory if it doesn't exist
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)

    # File paths
    rate_data_path = os.path.join(data_dir, "snap_rate.json")
    waveform_data_path = os.path.join(data_dir, "snap_waveform.json")
    amplitude_data_path = os.path.join(data_dir, "snap_amplitude.json")

    rate_output_path = os.path.join(assets_dir, "snap_rate.svg")
    waveform_output_path = os.path.join(assets_dir, "snap_waveform.svg")
    amplitude_output_path = os.path.join(assets_dir, "snap_amplitude.svg")

    # Generate charts
    create_timing_chart(rate_data_path, rate_output_path)
    create_waveform_chart(waveform_data_path, waveform_output_path)
    create_amplitude_chart(amplitude_data_path, amplitude_output_path)


if __name__ == "__main__":
    main()
