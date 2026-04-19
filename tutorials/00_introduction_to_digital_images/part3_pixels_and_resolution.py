"""
Part 2: Pixels and Resolution — What a Pixel Actually Is

Demonstrates what a pixel is (a single number), how spatial resolution affects
detail, and how quantization maps continuous brightness to discrete integers.

Run: python part2_pixels_and_resolution.py
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

# DIP3E image folder (relative to this script's location)
DIP_CH02 = Path(__file__).parent / '../../DIP3E_Original_Images_CH02'

np.random.seed(42)
print("Part 2: Pixels and Resolution")
print("=" * 40)


# ── Algorithm ──────────────────────────────────────────────
# Show a pixel grid — what a pixel actually is
# 1. Load a small region of a real image (top-left 32×32 patch)
# 2. Display it at normal size and zoomed in (nearest-neighbour)
# 3. Overlay the pixel grid lines on the zoomed view
# 4. Print the raw integer values for a small crop
# What to look for: zooming does NOT reveal detail — it reveals the grid.
#   Each square is one integer value. The image is literally a 2D array.
# ───────────────────────────────────────────────────────────

image_path = DIP_CH02 / 'Fig0222(b)(cameraman).tif'
full_image = np.array(Image.open(image_path).convert('L'))   # convert to grayscale

# Take a small patch to make the pixel grid visible
patch_size = 32
patch = full_image[:patch_size, :patch_size]

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
fig.suptitle('A Pixel Is Just a Number — The Grid Is the Image', fontsize=13)

# Full image
axes[0].imshow(full_image, cmap='gray', vmin=0, vmax=255)
axes[0].set_title(f'Full image\n{full_image.shape[1]}×{full_image.shape[0]} pixels', fontsize=11)
axes[0].axis('off')

# Small patch at normal display size
axes[1].imshow(patch, cmap='gray', vmin=0, vmax=255, interpolation='nearest')
axes[1].set_title(f'Top-left {patch_size}×{patch_size} patch', fontsize=11)
axes[1].axis('off')

# Tiny crop zoomed in with grid overlay — 8×8 pixels
tiny_crop = patch[:8, :8]
axes[2].imshow(tiny_crop, cmap='gray', vmin=0, vmax=255, interpolation='nearest')
# Draw grid lines to show individual pixels
for row in range(tiny_crop.shape[0] + 1):
    axes[2].axhline(row - 0.5, color='cyan', linewidth=0.8)
for col in range(tiny_crop.shape[1] + 1):
    axes[2].axvline(col - 0.5, color='cyan', linewidth=0.8)
# Annotate each pixel with its value
for row in range(tiny_crop.shape[0]):
    for col in range(tiny_crop.shape[1]):
        value = tiny_crop[row, col]
        text_color = 'white' if value < 128 else 'black'
        axes[2].text(col, row, str(value), ha='center', va='center',
                     fontsize=7, color=text_color, fontweight='bold')
axes[2].set_title('8×8 crop (each square = one integer)', fontsize=11)
axes[2].axis('off')

plt.tight_layout()
plt.show()

print(f"Image shape: {full_image.shape}  dtype: {full_image.dtype}")
print(f"Value range: {full_image.min()} – {full_image.max()}")
print(f"Top-left 4×4 pixel values:")
print(full_image[:4, :4])
print()


# ── Algorithm ──────────────────────────────────────────────
# Spatial resolution comparison
# 1. Downsample the image to several resolutions using PIL
# 2. Display all versions side by side
# 3. Show that lower resolution permanently loses detail
# What to look for: fine details (face, camera texture) disappear at low
#   resolution. Upscaling back to the original size does not recover them.
# ───────────────────────────────────────────────────────────

original_pil = Image.open(image_path).convert('L')
original_size = original_pil.size   # (width, height)

resolutions = [256, 128, 64, 32, 16]

fig, axes = plt.subplots(1, len(resolutions) + 1, figsize=(16, 4))
fig.suptitle('Spatial Resolution: More Pixels = More Detail', fontsize=13)

axes[0].imshow(np.array(original_pil), cmap='gray', vmin=0, vmax=255)
axes[0].set_title(f'Original\n{original_size[0]}×{original_size[1]}', fontsize=10)
axes[0].axis('off')

for ax, target_res in zip(axes[1:], resolutions):
    # Downsample then upsample back to original size for fair visual comparison
    downsampled = original_pil.resize((target_res, target_res), Image.NEAREST)
    upscaled    = downsampled.resize(original_size, Image.NEAREST)
    ax.imshow(np.array(upscaled), cmap='gray', vmin=0, vmax=255)
    ax.set_title(f'{target_res}×{target_res}', fontsize=10)
    ax.axis('off')

plt.tight_layout()
plt.show()

print("Each lower-resolution image was upscaled back to the original size.")
print("The jagged blocks are NOT new information — they reveal what was lost.")
print()


# ── Algorithm ──────────────────────────────────────────────
# Quantization: reducing bit depth
# 1. Define a function to quantize an image to B bits
# 2. Apply to the cameraman image at 8, 6, 4, 2, 1 bits
# 3. Display side by side
# 4. Show false contours on a smooth gradient
# What to look for: at 4 bits the image still looks recognisable.
#   At 2 bits, false contours appear in smooth regions (forehead, sky).
#   At 1 bit the image is binary — all detail in the midtones is gone.
# ───────────────────────────────────────────────────────────

def quantize_image(image: np.ndarray, num_bits: int) -> np.ndarray:
    """Quantize a grayscale image to the given number of bits.

    Args:
        image:    2D array of uint8 pixel values (0–255).
        num_bits: Target bit depth (1–8).

    Returns:
        Quantized image rescaled back to 0–255 range (uint8).
    """
    num_levels = 2 ** num_bits
    # Map 0–255 to 0–(num_levels-1), round, map back to 0–255
    scale_factor = 255.0 / (num_levels - 1)
    quantized = np.floor(image / scale_factor + 0.5) * scale_factor
    return quantized.clip(0, 255).astype(np.uint8)


bit_depths = [8, 6, 4, 2, 1]
image_array = np.array(original_pil)

fig, axes = plt.subplots(1, len(bit_depths), figsize=(16, 4))
fig.suptitle('Quantization: Reducing Bit Depth Introduces False Contours', fontsize=13)

for ax, num_bits in zip(axes, bit_depths):
    quantized = quantize_image(image_array, num_bits)
    ax.imshow(quantized, cmap='gray', vmin=0, vmax=255)
    num_levels = 2 ** num_bits
    ax.set_title(f'{num_bits}-bit\n({num_levels} levels)', fontsize=10)
    ax.axis('off')

plt.tight_layout()
plt.show()


# False contour demo on a smooth gradient
gradient = np.tile(np.linspace(0, 255, 256).astype(np.uint8), (64, 1))

fig, axes = plt.subplots(1, len(bit_depths), figsize=(16, 3))
fig.suptitle('False Contours on a Smooth Gradient (visible at low bit depth)', fontsize=13)

for ax, num_bits in zip(axes, bit_depths):
    quantized_gradient = quantize_image(gradient, num_bits)
    ax.imshow(quantized_gradient, cmap='gray', vmin=0, vmax=255, aspect='auto')
    ax.set_title(f'{num_bits}-bit', fontsize=10)
    ax.axis('off')

plt.tight_layout()
plt.show()

# Print quantization error statistics
print("Quantization error (max error = Δ/2):")
for num_bits in bit_depths:
    num_levels = 2 ** num_bits
    step_size  = 255.0 / (num_levels - 1)
    max_error  = step_size / 2
    quantized  = quantize_image(image_array, num_bits).astype(float)
    actual_mae = np.mean(np.abs(image_array.astype(float) - quantized))
    print(f"  {num_bits}-bit ({num_levels:4d} levels): "
          f"step Δ={step_size:6.1f}, max error={max_error:5.1f}, "
          f"actual MAE={actual_mae:.1f}")
