"""
Part 3: Contrast and Dynamic Range

Demonstrates what contrast means numerically, the affine relationship between
exposures, dynamic range limits, and the Einstein low/medium/high contrast example.

Run: python part3_contrast_and_dynamic_range.py
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
print("Part 3: Contrast and Dynamic Range")
print("=" * 40)


# ── Algorithm ──────────────────────────────────────────────
# Contrast levels: Einstein low / medium / high contrast
# 1. Load the three Einstein images from the DIP database
# 2. Display them side by side
# 3. Plot their histograms overlaid on the same axes
# 4. Compute and print per-image statistics
# What to look for: the images have identical spatial content but very
#   different pixel value distributions. This is the core problem for
#   pixel-level comparison: same object → different numbers.
# ───────────────────────────────────────────────────────────

einstein_low    = np.array(Image.open(DIP_CH02 / 'Fig0241(a)(einstein low contrast).tif'))
einstein_med    = np.array(Image.open(DIP_CH02 / 'Fig0241(b)(einstein med contrast).tif'))
einstein_high   = np.array(Image.open(DIP_CH02 / 'Fig0241(c)(einstein high contrast).tif'))

contrast_images = [
    ('Low contrast',    einstein_low,  COLORS['primary']),
    ('Medium contrast', einstein_med,  COLORS['secondary']),
    ('High contrast',   einstein_high, COLORS['highlight']),
]

fig, axes = plt.subplots(2, 3, figsize=(14, 9))
fig.suptitle('Same Face — Three Contrast Levels\n'
             '(pixel values change; content does not)', fontsize=13)

for col, (label, image, color) in enumerate(contrast_images):
    axes[0, col].imshow(image, cmap='gray', vmin=0, vmax=255)
    axes[0, col].set_title(f'{label}\nmean={image.mean():.0f}  '
                           f'std={image.std():.0f}', fontsize=11)
    axes[0, col].axis('off')

    axes[1, col].hist(image.ravel(), bins=64, range=(0, 255),
                      color=color, alpha=0.7, edgecolor='white', linewidth=0.3)
    axes[1, col].set_xlim(0, 255)
    axes[1, col].set_xlabel('Pixel value', fontsize=10)
    axes[1, col].set_ylabel('Count', fontsize=10)
    axes[1, col].set_title(f'Histogram — {label}', fontsize=10)
    axes[1, col].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("Einstein contrast comparison:")
for label, image, _ in contrast_images:
    print(f"  {label:18s}: min={image.min():3d}  max={image.max():3d}  "
          f"mean={image.mean():5.1f}  std={image.std():5.1f}")
print()
print("Same spatial content — pixel values differ by up to 100 grey levels.")
print()


# ── Algorithm ──────────────────────────────────────────────
# The affine model: I2 = a * I1 + b
# 1. Take the medium-contrast Einstein as the reference image
# 2. Synthesise versions by applying different (a, b) pairs
# 3. Show that the pixel values change but the image looks the same content
# 4. Compute the pixel-wise difference and SSD against the original
# What to look for: a small change in a or b (realistic lighting change)
#   produces large SSD values. Pixel comparison declares the images "different"
#   even though the content is identical.
# ───────────────────────────────────────────────────────────

reference = einstein_med.astype(float)

affine_variants = [
    ('Original (a=1, b=0)',   1.0,  0),
    ('Brighter (a=1, b=40)',  1.0, 40),
    ('Lower contrast (a=0.5, b=64)', 0.5, 64),
    ('Higher contrast (a=1.5, b=-40)', 1.5, -40),
]

fig, axes = plt.subplots(2, len(affine_variants), figsize=(16, 8))
fig.suptitle('Affine Transform: I₂ = a·I₁ + b  (same content, different pixel values)',
             fontsize=13)

for col, (label, a, b) in enumerate(affine_variants):
    transformed = np.clip(a * reference + b, 0, 255).astype(np.uint8)
    pixel_diff  = np.abs(transformed.astype(float) - reference)
    ssd         = np.sum((transformed.astype(float) - reference) ** 2)

    axes[0, col].imshow(transformed, cmap='gray', vmin=0, vmax=255)
    axes[0, col].set_title(f'{label}\nSSD={ssd:.0f}', fontsize=9)
    axes[0, col].axis('off')

    axes[1, col].hist(transformed.ravel(), bins=64, range=(0, 255),
                      color=COLORS['primary'], alpha=0.6, label='Transformed')
    axes[1, col].hist(reference.ravel(), bins=64, range=(0, 255),
                      color=COLORS['highlight'], alpha=0.4, label='Original')
    axes[1, col].set_xlim(0, 255)
    axes[1, col].set_xlabel('Pixel value', fontsize=9)
    axes[1, col].legend(fontsize=8)
    axes[1, col].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("Affine transform effect on SSD (pixel-level comparison):")
for label, a, b in affine_variants:
    transformed = np.clip(a * reference + b, 0, 255)
    ssd = np.sum((transformed - reference) ** 2)
    mae = np.mean(np.abs(transformed - reference))
    print(f"  {label:40s}: SSD={ssd:12.0f}  MAE={mae:.1f}")
print()
print("Even a modest lighting change (brighter) produces large SSD.")
print("This is why raw pixel comparison fails in uncontrolled conditions.")
print()


# ── Algorithm ──────────────────────────────────────────────
# Dynamic range clipping demonstration
# 1. Create a synthetic scene with a large dynamic range (0–4000 photon counts)
# 2. Map it to an 8-bit sensor (only captures ~0–255 without clipping)
# 3. Show what is lost when we clip vs when we expose for dark vs bright regions
# What to look for: no single exposure setting captures both the bright and
#   dark regions. Detail is permanently lost in the clipped areas.
# ───────────────────────────────────────────────────────────

# Simulate a high-dynamic-range scene (e.g., window in a dark room)
scene_height = 256
scene_width  = 512
hdr_scene = np.zeros((scene_height, scene_width), dtype=float)

# Dark room region: values 0–50
hdr_scene[:, :256] = np.random.uniform(0, 50, (scene_height, 256))
# Bright window region: values 1000–4000
hdr_scene[:, 256:] = np.random.uniform(1000, 4000, (scene_height, 256))

def clip_to_8bit(scene: np.ndarray, exposure_factor: float) -> np.ndarray:
    """Apply an exposure (multiply) then clip to 0–255."""
    return np.clip(scene * exposure_factor, 0, 255).astype(np.uint8)

exposure_settings = [
    ('Expose for window\n(factor=0.05)',  0.05),
    ('Middle exposure\n(factor=0.1)',     0.10),
    ('Expose for room\n(factor=0.5)',     0.50),
]

fig, axes = plt.subplots(1, len(exposure_settings) + 1, figsize=(16, 4))
fig.suptitle('Dynamic Range: High-DR Scene — One Exposure Cannot Capture Everything',
             fontsize=13)

# Show the "true" HDR scene (normalised for display)
hdr_display = (hdr_scene / hdr_scene.max() * 255).astype(np.uint8)
axes[0].imshow(hdr_display, cmap='gray')
axes[0].set_title('True HDR scene\n(normalised for display)', fontsize=10)
axes[0].axis('off')

for ax, (label, factor) in zip(axes[1:], exposure_settings):
    captured = clip_to_8bit(hdr_scene, factor)
    # Count clipped pixels
    num_clipped = np.sum(captured == 255) + np.sum(captured == 0)
    pct_clipped = 100 * num_clipped / captured.size

    ax.imshow(captured, cmap='gray', vmin=0, vmax=255)
    ax.set_title(f'{label}\n{pct_clipped:.0f}% pixels clipped', fontsize=10)
    ax.axis('off')

plt.tight_layout()
plt.show()

print("Dynamic range clipping:")
for label, factor in exposure_settings:
    captured = clip_to_8bit(hdr_scene, factor)
    pct_clipped = 100 * (np.sum(captured == 255) + np.sum(captured == 0)) / captured.size
    print(f"  {label.splitlines()[0]:35s}: {pct_clipped:.0f}% pixels clipped")
print()
print("High-DR scenes require HDR capture or exposure bracketing.")
print("Any single 8-bit capture loses information in the over/underexposed regions.")
