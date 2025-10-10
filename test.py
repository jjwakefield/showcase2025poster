import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(6, 1.2))

# Define frequency bands (Hz)
bands = [(1, 10), (10, 500), (500, 25000), (25000, 100000)]
labels = [
    "Geophysical\nMicroseisms",
    "Anthropogenic\nShipping, Surf",
    "Biological\nSnapping Shrimp",
    "Biological\nEcholocation",
]
colors = ["#94a3b8", "#60a5fa", "#34d399", "#10b981"]

for (low, high), label, color in zip(bands, labels, colors):
    ax.barh(0, width=high - low, left=low, color=color, edgecolor="white", height=0.8)
    ax.text(
        np.sqrt(low * high),
        0,
        label,
        ha="center",
        va="center",
        fontsize=9,
        color="white",
        fontweight="bold",
    )

ax.set_xscale("log")
ax.set_xlim(1, 1e5)
ax.set_xlabel("Frequency (Hz)")
ax.set_yticks([])
ax.spines[["top", "right", "left"]].set_visible(False)

plt.tight_layout()
# plt.savefig("frequency_bands.svg", dpi=300)
plt.show()
