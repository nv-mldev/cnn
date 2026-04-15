"""
Sampling Grid Density Comparison
================================
Shows the same continuous 2D signal (concentric circles) sampled at three
different grid densities: coarse, medium, and fine. Grid lines are overlaid
to make the sampling explicit.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

# --- Continuous signal: concentric circular pattern ---
high_resolution = 500
x_continuous = np.linspace(-1, 1, high_resolution)
y_continuous = np.linspace(-1, 1, high_resolution)
xx, yy = np.meshgrid(x_continuous, y_continuous)
# Concentric rings — high spatial frequency so aliasing is visible
continuous_signal = np.sin(2 * np.pi * 6 * np.sqrt(xx**2 + yy**2))

# --- Sampling grids at three densities ---
grid_sizes = [8, 20, 60]
grid_labels = [
    f"Coarse ({g}×{g} grid)" for g in grid_sizes
]
grid_labels = [
    f"Coarse (8×8)",
    f"Medium (20×20)",
    f"Fine (60×60)",
]

fig, axes = plt.subplots(1, 4, figsize=(18, 4.2))
norm = Normalize(vmin=-1, vmax=1)

# Panel 0: the "continuous" signal (high-res rendering)
axes[0].imshow(continuous_signal, cmap="gray", norm=norm, extent=[-1, 1, -1, 1])
axes[0].set_title("Continuous scene", fontsize=12, fontweight="bold")
axes[0].set_xlabel("x")
axes[0].set_ylabel("y")

# Panels 1-3: sampled versions with grid overlay
for idx, (grid_size, label) in enumerate(zip(grid_sizes, grid_labels)):
    ax = axes[idx + 1]

    # Sample the continuous signal on this grid
    sample_points = np.linspace(-1, 1, grid_size)
    sx, sy = np.meshgrid(sample_points, sample_points)
    sampled_values = np.sin(2 * np.pi * 6 * np.sqrt(sx**2 + sy**2))

    # Display the sampled image (nearest-neighbour to show pixel blocks)
    ax.imshow(
        sampled_values,
        cmap="gray",
        norm=norm,
        extent=[-1, 1, -1, 1],
        interpolation="nearest",
    )

    # Overlay grid lines
    for point in sample_points:
        ax.axhline(y=point, color="red", linewidth=0.3, alpha=0.5)
        ax.axvline(x=point, color="red", linewidth=0.3, alpha=0.5)

    ax.set_title(label, fontsize=12, fontweight="bold")
    ax.set_xlabel("x")

# Clean up
for ax in axes:
    ax.set_aspect("equal")
    ax.tick_params(labelsize=8)

fig.suptitle(
    "Sampling: same scene, different grid densities",
    fontsize=14,
    fontweight="bold",
    y=1.02,
)
plt.tight_layout()
plt.savefig(
    "wiki/figures/sampling_grid_density.png",
    dpi=150,
    bbox_inches="tight",
    facecolor="white",
)
plt.close()
print("Saved: wiki/figures/sampling_grid_density.png")
