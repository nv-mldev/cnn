"""
Spatial Frequency Intuition
============================
Builds the mental model: frequency in images = how fast intensity changes
across space. Smooth gradients are low-frequency; edges and fine textures
are high-frequency. Every image is a sum of 2D sinusoidal patterns.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

# =============================================================================
# Figure 1: Low vs High spatial frequency — the core intuition
# =============================================================================
fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
size = 200
x = np.linspace(0, 1, size)
xx, yy = np.meshgrid(x, x)

# (a) Low-frequency: smooth gradient — intensity changes slowly
low_freq = np.sin(2 * np.pi * 1 * xx)
axes[0].imshow(low_freq, cmap="gray")
axes[0].set_title("Low spatial frequency\n(1 cycle — smooth, slow change)", fontsize=11, fontweight="bold")
axes[0].set_xticks([]); axes[0].set_yticks([])

# (b) Medium-frequency
medium_freq = np.sin(2 * np.pi * 5 * xx)
axes[1].imshow(medium_freq, cmap="gray")
axes[1].set_title("Medium spatial frequency\n(5 cycles)", fontsize=11, fontweight="bold")
axes[1].set_xticks([]); axes[1].set_yticks([])

# (c) High-frequency: fine stripes — intensity changes rapidly
high_freq = np.sin(2 * np.pi * 25 * xx)
axes[2].imshow(high_freq, cmap="gray")
axes[2].set_title("High spatial frequency\n(25 cycles — rapid change)", fontsize=11, fontweight="bold")
axes[2].set_xticks([]); axes[2].set_yticks([])

fig.suptitle(
    "Spatial frequency = how quickly intensity changes across space",
    fontsize=13, fontweight="bold", y=1.02,
)
plt.tight_layout()
plt.savefig("wiki/figures/spatial_frequency_intuition.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved: spatial_frequency_intuition.png")

# =============================================================================
# Figure 2: 2D sinusoidal patterns — the basis of all images
# =============================================================================
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
size = 200
x = np.linspace(0, 1, size)
xx, yy = np.meshgrid(x, x)

configs = [
    (3, 0, "Horizontal, low freq"),
    (10, 0, "Horizontal, high freq"),
    (0, 3, "Vertical, low freq"),
    (0, 10, "Vertical, high freq"),
    (5, 5, "Diagonal, medium freq"),
    (15, 15, "Diagonal, high freq"),
]

for ax, (fx, fy, label) in zip(axes.flat, configs):
    pattern = np.sin(2 * np.pi * (fx * xx + fy * yy))
    ax.imshow(pattern, cmap="gray")
    ax.set_title(f"{label}\n(fx={fx}, fy={fy})", fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])

fig.suptitle(
    "2D sinusoidal patterns — every image is a weighted sum of these",
    fontsize=13, fontweight="bold", y=1.00,
)
plt.tight_layout()
plt.savefig("wiki/figures/spatial_frequency_2d_basis.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved: spatial_frequency_2d_basis.png")

# =============================================================================
# Figure 3: Low-pass vs high-pass filtering — what each frequency band contains
# =============================================================================
from scipy import ndimage

# Build a synthetic "natural" image: smooth shapes + sharp edges + fine texture
size = 256
x = np.linspace(-1, 1, size)
xx, yy = np.meshgrid(x, x)

# Smooth background gradient (low freq)
background = 0.3 * xx + 0.2 * yy
# A disk (medium freq edges)
disk = (np.sqrt(xx**2 + yy**2) < 0.4).astype(float) * 0.5
# Fine texture (high freq)
texture = 0.15 * np.sin(2 * np.pi * 30 * xx) * np.sin(2 * np.pi * 30 * yy)
# Compose
original = background + disk + texture
original = (original - original.min()) / (original.max() - original.min())

# Low-pass filter: Gaussian blur (keeps only low frequencies)
low_pass = ndimage.gaussian_filter(original, sigma=5)
# High-pass: original minus low-pass (keeps only high frequencies)
high_pass = original - low_pass
# Normalize high-pass for display
high_pass_display = (high_pass - high_pass.min()) / (high_pass.max() - high_pass.min())

fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

axes[0].imshow(original, cmap="gray")
axes[0].set_title("Original image\n(all frequencies mixed)", fontsize=11, fontweight="bold")
axes[0].set_xticks([]); axes[0].set_yticks([])

axes[1].imshow(low_pass, cmap="gray")
axes[1].set_title("Low-pass filtered\n(only smooth, slow changes)", fontsize=11, fontweight="bold")
axes[1].set_xticks([]); axes[1].set_yticks([])

axes[2].imshow(high_pass_display, cmap="gray")
axes[2].set_title("High-pass filtered\n(only edges & fine texture)", fontsize=11, fontweight="bold")
axes[2].set_xticks([]); axes[2].set_yticks([])

fig.suptitle(
    "Decomposing an image by frequency: smooth parts (low) vs edges/texture (high)",
    fontsize=13, fontweight="bold", y=1.02,
)
plt.tight_layout()
plt.savefig("wiki/figures/spatial_frequency_decomposition.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved: spatial_frequency_decomposition.png")
