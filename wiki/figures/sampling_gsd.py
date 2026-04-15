"""
Ground Sampling Distance (GSD) Visualization
=============================================
Bird's-eye view of the same scene captured at two different GSDs.
Shows how pixel size determines what details are resolvable —
grounded in industrial inspection context.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.colors import Normalize


def draw_inspection_scene(ax):
    """Draw a simple industrial part: a metal plate with bolts and a scratch."""
    # Metal plate background
    ax.add_patch(Rectangle((0.1, 0.1), 0.8, 0.8, facecolor="#b0b0b0", edgecolor="black", linewidth=2))

    # Bolts (small circles)
    bolt_positions = [(0.25, 0.75), (0.75, 0.75), (0.25, 0.25), (0.75, 0.25)]
    for bx, by in bolt_positions:
        ax.add_patch(Circle((bx, by), 0.04, facecolor="#505050", edgecolor="black", linewidth=1))
        # Cross-slot on bolt head
        ax.plot([bx - 0.02, bx + 0.02], [by, by], color="black", linewidth=0.8)
        ax.plot([bx, bx], [by - 0.02, by + 0.02], color="black", linewidth=0.8)

    # Scratch / defect (thin diagonal line)
    ax.plot([0.4, 0.65], [0.55, 0.45], color="#8B0000", linewidth=1.5, linestyle="-")

    # Label the defect
    ax.annotate(
        "scratch\n(defect)",
        xy=(0.52, 0.50),
        xytext=(0.52, 0.65),
        fontsize=8,
        color="#8B0000",
        ha="center",
        arrowprops=dict(arrowstyle="->", color="#8B0000", lw=1),
    )


def overlay_grid(ax, grid_size, color="blue"):
    """Overlay a sampling grid and label cell size."""
    positions = np.linspace(0, 1, grid_size + 1)
    for p in positions:
        ax.axhline(y=p, color=color, linewidth=0.6, alpha=0.6)
        ax.axvline(x=p, color=color, linewidth=0.6, alpha=0.6)


fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# --- Panel 0: the "real" scene (no grid) ---
ax = axes[0]
draw_inspection_scene(ax)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("equal")
ax.set_title("Scene (continuous)", fontsize=12, fontweight="bold")

# --- Panel 1: coarse GSD (large pixels, few samples) ---
ax = axes[1]
draw_inspection_scene(ax)
coarse_grid = 5
overlay_grid(ax, coarse_grid, color="blue")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("equal")
cell_size_coarse = 100 / coarse_grid  # assuming 100mm plate
ax.set_title(
    f"Coarse GSD\n{coarse_grid}×{coarse_grid} grid — {cell_size_coarse:.0f} mm/pixel",
    fontsize=11,
    fontweight="bold",
)
ax.text(
    0.5, -0.08,
    "Bolts: ~1 pixel each. Scratch: sub-pixel → invisible.",
    transform=ax.transAxes,
    ha="center",
    fontsize=9,
    color="red",
    fontweight="bold",
)

# --- Panel 2: fine GSD (small pixels, many samples) ---
ax = axes[2]
draw_inspection_scene(ax)
fine_grid = 25
overlay_grid(ax, fine_grid, color="blue")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("equal")
cell_size_fine = 100 / fine_grid
ax.set_title(
    f"Fine GSD\n{fine_grid}×{fine_grid} grid — {cell_size_fine:.0f} mm/pixel",
    fontsize=11,
    fontweight="bold",
)
ax.text(
    0.5, -0.08,
    "Bolts: ~4 pixels across. Scratch: spans multiple pixels → detectable.",
    transform=ax.transAxes,
    ha="center",
    fontsize=9,
    color="green",
    fontweight="bold",
)

for ax in axes:
    ax.tick_params(labelsize=8)

fig.suptitle(
    "Ground Sampling Distance: pixel size determines what defects you can see",
    fontsize=13,
    fontweight="bold",
    y=1.02,
)
plt.tight_layout()
plt.savefig(
    "wiki/figures/sampling_gsd.png",
    dpi=150,
    bbox_inches="tight",
    facecolor="white",
)
plt.close()
print("Saved: wiki/figures/sampling_gsd.png")
