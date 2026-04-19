"""
Part 5: Colour Channels and the Imaging Pipeline

Demonstrates RGB channel decomposition, per-channel statistics, the luminance
formula, and the non-uniform lighting (shading) effect from the tungsten filament
example in Gonzalez & Woods DIP3E.

Run: python part5_colour_and_pipeline.py
"""

# --- Setup ---
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

COLORS = {
    'primary':   '#2196F3',
    'secondary': '#4CAF50',
    'result':    '#FFC107',
    'highlight': '#F44336',
    'transform': '#9C27B0',
    'gradient':  '#FF9800',
}

DIP_CH02 = Path(__file__).parent / '../../DIP3E_Original_Images_CH02'

np.random.seed(42)
print("Part 5: Colour Channels and the Imaging Pipeline")
print("=" * 50)


# ── Algorithm ──────────────────────────────────────────────
# Colour channel decomposition
# 1. Load a colour image (rose from DIP3E — Fig0219)
# 2. Split into R, G, B channels
# 3. Display the full colour image and each channel as grayscale
# 4. Plot per-channel histograms
# What to look for: each channel is an independent grayscale image.
#   The rose has high values in the R channel and low values in B.
#   The histograms show that each channel has a different distribution.
# ───────────────────────────────────────────────────────────

rose_path  = DIP_CH02 / 'Fig0219(rose1024).tif'
rose_rgb   = np.array(Image.open(rose_path).convert('RGB'))

red_channel   = rose_rgb[:, :, 0]
green_channel = rose_rgb[:, :, 1]
blue_channel  = rose_rgb[:, :, 2]

channel_names  = ['Red',  'Green', 'Blue']
channel_arrays = [red_channel, green_channel, blue_channel]
channel_colors = ['#E53935', '#43A047', '#1E88E5']

fig, axes = plt.subplots(2, 4, figsize=(16, 8))
fig.suptitle('Colour Image = Three Independent Grayscale Arrays', fontsize=13)

axes[0, 0].imshow(rose_rgb)
axes[0, 0].set_title(f'Full RGB image\n{rose_rgb.shape[1]}×{rose_rgb.shape[0]}', fontsize=11)
axes[0, 0].axis('off')

for col, (name, channel, color) in enumerate(
        zip(channel_names, channel_arrays, channel_colors), start=1):
    axes[0, col].imshow(channel, cmap='gray', vmin=0, vmax=255)
    axes[0, col].set_title(f'{name} channel\nmean={channel.mean():.0f}', fontsize=11)
    axes[0, col].axis('off')

# Combined histogram (bottom row, spanning all 4 axes merged)
ax_hist = fig.add_subplot(2, 1, 2)
for name, channel, color in zip(channel_names, channel_arrays, channel_colors):
    ax_hist.hist(channel.ravel(), bins=64, range=(0, 255),
                 color=color, alpha=0.5, label=name, density=True)
ax_hist.set_xlabel('Pixel value', fontsize=11)
ax_hist.set_ylabel('Density', fontsize=11)
ax_hist.set_title('Per-Channel Histograms — Different distributions per channel', fontsize=11)
ax_hist.legend(fontsize=10)
ax_hist.grid(True, alpha=0.3)

# Remove the individual bottom axes
for ax in axes[1]:
    ax.remove()

plt.tight_layout()
plt.show()

print("Per-channel statistics (rose image):")
for name, channel in zip(channel_names, channel_arrays):
    print(f"  {name:6s}: mean={channel.mean():5.1f}  std={channel.std():5.1f}  "
          f"min={channel.min():3d}  max={channel.max():3d}")
print()


# ── Algorithm ──────────────────────────────────────────────
# Grayscale conversion: luminance formula
# 1. Convert the rose to grayscale using PIL (standard perceptual formula)
# 2. Also convert using equal-weight average (mean of R+G+B)
# 3. Compare the two — show the difference image
# What to look for: the perceptual formula weights green heavily (0.7152)
#   because human vision is most sensitive to green. Equal-weight average
#   over-weights red and blue, producing slightly different brightness values.
# ───────────────────────────────────────────────────────────

# Perceptual luminance: L = 0.2126*R + 0.7152*G + 0.0722*B
luminance_perceptual = (
    0.2126 * rose_rgb[:, :, 0].astype(float)
    + 0.7152 * rose_rgb[:, :, 1].astype(float)
    + 0.0722 * rose_rgb[:, :, 2].astype(float)
).clip(0, 255).astype(np.uint8)

# Simple mean (equal weights)
luminance_mean = rose_rgb.astype(float).mean(axis=2).astype(np.uint8)

# Absolute difference
lum_difference = np.abs(luminance_perceptual.astype(int)
                        - luminance_mean.astype(int)).astype(np.uint8)

fig, axes = plt.subplots(1, 3, figsize=(14, 5))
fig.suptitle('Grayscale Conversion: Perceptual Luminance vs Equal-Weight Average',
             fontsize=13)

axes[0].imshow(luminance_perceptual, cmap='gray', vmin=0, vmax=255)
axes[0].set_title('Perceptual luminance\n(0.2126R + 0.7152G + 0.0722B)', fontsize=11)
axes[0].axis('off')

axes[1].imshow(luminance_mean, cmap='gray', vmin=0, vmax=255)
axes[1].set_title('Equal-weight mean\n(R + G + B) / 3', fontsize=11)
axes[1].axis('off')

axes[2].imshow(lum_difference, cmap='hot', vmin=0, vmax=50)
axes[2].set_title(f'Absolute difference\nmean={lum_difference.mean():.1f}  '
                  f'max={lum_difference.max()}', fontsize=11)
axes[2].axis('off')

plt.tight_layout()
plt.show()

print("Grayscale conversion comparison:")
print(f"  Perceptual: mean={luminance_perceptual.mean():.1f}")
print(f"  Equal-weight: mean={luminance_mean.mean():.1f}")
print(f"  Difference: mean={lum_difference.mean():.1f}  max={lum_difference.max()}")
print()


# ── Algorithm ──────────────────────────────────────────────
# Non-uniform lighting: tungsten filament shading example
# 1. Load Fig0229(a) — tungsten filament with shading artefact
# 2. Load Fig0229(b) — the sensor shading pattern
# 3. Display both images side by side
# 4. Plot intensity profiles across the middle row of both images
# What to look for: the shading pattern shows that the sensor/lighting
#   response varies across the image. The centre is brighter than the edges.
#   This means pixel values encode POSITION, not just the object's reflectance.
# ───────────────────────────────────────────────────────────

tungsten_original = np.array(
    Image.open(DIP_CH02 / 'Fig0229(a)(tungsten_filament_shaded).tif')
)
tungsten_shading  = np.array(
    Image.open(DIP_CH02 / 'Fig0229(b)(tungsten_sensor_shading).tif')
)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

axes[0].imshow(tungsten_original, cmap='gray', vmin=0, vmax=255)
axes[0].set_title('Tungsten Filament\n(with shading artefact)', fontsize=12)
axes[0].axis('off')

axes[1].imshow(tungsten_shading, cmap='gray', vmin=0, vmax=255)
axes[1].set_title('Sensor Shading Pattern\n(non-uniform response)', fontsize=12)
axes[1].axis('off')

# Intensity profile across the middle row
mid_row = tungsten_original.shape[0] // 2
axes[2].plot(tungsten_original[mid_row, :], color=COLORS['primary'], linewidth=1.5,
             label='Original (with shading)')
axes[2].plot(tungsten_shading[mid_row, :], color=COLORS['highlight'], linewidth=1.5,
             label='Shading pattern', alpha=0.7)
axes[2].set_xlabel('Column (pixel position)', fontsize=11)
axes[2].set_ylabel('Intensity', fontsize=11)
axes[2].set_title('Intensity Profile — Middle Row', fontsize=12)
axes[2].legend(fontsize=9)
axes[2].grid(True, alpha=0.3)

plt.suptitle('Non-Uniform Lighting: Same Object → Different Pixel Values Across the Image\n'
             '(Tungsten Filament — Gonzalez & Woods DIP3E)', fontsize=14, y=1.02)
plt.tight_layout()
plt.show()

print("The shading pattern shows that the sensor/lighting response varies across the image.")
print("Pixels in the centre are brighter than at the edges — even for the SAME material.")
print("This means pixel values depend on POSITION, not just on the object.")
print()
print("For template matching: a template from the bright centre won't match the same")
print("material at the darker edges. The I = a·T + b model applies LOCALLY, not globally.")
