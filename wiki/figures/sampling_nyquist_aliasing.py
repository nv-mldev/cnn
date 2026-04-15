"""
Nyquist & Aliasing Visualization
=================================
A high-frequency stripe pattern sampled at three rates:
below Nyquist (aliased), at Nyquist (borderline), and above Nyquist (faithful).
Shows how undersampling creates phantom low-frequency patterns (moiré).
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

# --- Continuous signal: vertical stripes (high frequency) ---
signal_frequency = 12  # cycles across the domain
high_resolution = 600
x_continuous = np.linspace(0, 1, high_resolution)
y_continuous = np.linspace(0, 1, high_resolution)
xx, yy = np.meshgrid(x_continuous, y_continuous)
# Vertical stripes
continuous_signal = np.sin(2 * np.pi * signal_frequency * xx)

# --- Three sampling rates ---
# Nyquist criterion: need >= 2 * frequency samples
nyquist_rate = 2 * signal_frequency  # 24 samples

sampling_configs = [
    (10, f"Below Nyquist ({10} samples)\n< {nyquist_rate} needed → ALIASED"),
    (nyquist_rate, f"At Nyquist ({nyquist_rate} samples)\nBorderline — just enough"),
    (60, f"Above Nyquist ({60} samples)\nFaithful reproduction"),
]

fig, axes = plt.subplots(1, 4, figsize=(18, 4.2))
norm = Normalize(vmin=-1, vmax=1)

# Panel 0: continuous signal
axes[0].imshow(
    continuous_signal,
    cmap="gray",
    norm=norm,
    extent=[0, 1, 0, 1],
    aspect="equal",
)
axes[0].set_title(
    f"Continuous signal\n({signal_frequency} cycles)", fontsize=11, fontweight="bold"
)

# Panels 1-3: sampled at different rates
for idx, (num_samples, label) in enumerate(sampling_configs):
    ax = axes[idx + 1]

    sample_x = np.linspace(0, 1, num_samples)
    sample_y = np.linspace(0, 1, num_samples)
    sx, sy = np.meshgrid(sample_x, sample_y)
    sampled = np.sin(2 * np.pi * signal_frequency * sx)

    ax.imshow(
        sampled,
        cmap="gray",
        norm=norm,
        extent=[0, 1, 0, 1],
        interpolation="nearest",
        aspect="equal",
    )
    ax.set_title(label, fontsize=10, fontweight="bold")

# Annotate the aliased panel
axes[1].annotate(
    "Phantom low-frequency\npattern (moiré)",
    xy=(0.5, 0.5),
    xytext=(0.5, -0.15),
    textcoords="axes fraction",
    fontsize=9,
    color="red",
    fontweight="bold",
    ha="center",
    arrowprops=dict(arrowstyle="->", color="red", lw=1.5),
)

for ax in axes:
    ax.set_xlabel("x")
    ax.tick_params(labelsize=8)
axes[0].set_ylabel("y")

fig.suptitle(
    "Nyquist criterion: sampling rate determines whether the signal survives",
    fontsize=13,
    fontweight="bold",
    y=1.02,
)
plt.tight_layout()
plt.savefig(
    "wiki/figures/sampling_nyquist_aliasing.png",
    dpi=150,
    bbox_inches="tight",
    facecolor="white",
)
plt.close()
print("Saved: wiki/figures/sampling_nyquist_aliasing.png")
