"""
Part 4: Zoom and Aliasing — What Pixels Really Look Like

Demonstrates nearest-neighbour vs bilinear zoom, downsampling artefacts,
and the checkerboard aliasing example.

Run: python part4_zoom_and_aliasing.py
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
print("Part 4: Zoom and Aliasing")
print("=" * 40)


# ── Algorithm ──────────────────────────────────────────────
# Zoom reveals the pixel grid
# 1. Load the cameraman image and crop a small region (e.g., 16×16 face area)
# 2. Zoom in using nearest-neighbour (PIL NEAREST) to 256×256
# 3. Zoom in using bilinear (PIL BILINEAR) to 256×256
# 4. Display the original crop and both zoomed versions side by side
# What to look for: nearest-neighbour produces hard block edges — each original
#   pixel maps to a solid rectangle. Bilinear blends neighbouring values and
#   looks smoother but blurry. Neither method recovers real detail.
# ───────────────────────────────────────────────────────────

cameraman_path = DIP_CH02 / 'Fig0222(b)(cameraman).tif'
cameraman_pil  = Image.open(cameraman_path).convert('L')
cameraman_arr  = np.array(cameraman_pil)

# Crop a small region (top-left area of the face)
crop_row_start, crop_col_start = 60, 90
crop_size = 20
tiny_crop_arr = cameraman_arr[crop_row_start:crop_row_start + crop_size,
                              crop_col_start:crop_col_start + crop_size]
tiny_crop_pil = Image.fromarray(tiny_crop_arr)

target_display_size = (200, 200)
zoomed_nearest  = tiny_crop_pil.resize(target_display_size, Image.NEAREST)
zoomed_bilinear = tiny_crop_pil.resize(target_display_size, Image.BILINEAR)

fig, axes = plt.subplots(1, 3, figsize=(13, 4))
fig.suptitle('Zoom Comparison: Nearest-Neighbour vs Bilinear Interpolation', fontsize=13)

axes[0].imshow(tiny_crop_arr, cmap='gray', vmin=0, vmax=255, interpolation='nearest')
axes[0].set_title(f'Original crop\n{crop_size}×{crop_size} pixels', fontsize=11)
axes[0].axis('off')

axes[1].imshow(np.array(zoomed_nearest), cmap='gray', vmin=0, vmax=255)
axes[1].set_title(f'Nearest-neighbour zoom\n{target_display_size[0]}×{target_display_size[1]}\n'
                  f'(blocky — pixel grid visible)', fontsize=11)
axes[1].axis('off')

axes[2].imshow(np.array(zoomed_bilinear), cmap='gray', vmin=0, vmax=255)
axes[2].set_title(f'Bilinear zoom\n{target_display_size[0]}×{target_display_size[1]}\n'
                  f'(smooth — but blurry)', fontsize=11)
axes[2].axis('off')

plt.tight_layout()
plt.show()

print("Both methods invent pixels. Neither recovers detail that was never captured.")
print()


# ── Algorithm ──────────────────────────────────────────────
# Downsampling information loss
# 1. Load the chronometer (high-detail) image
# 2. Downsample to several sizes with and without anti-aliasing filter
# 3. Upsample back to original size for visual comparison
# What to look for: without anti-aliasing, fine details produce moiré / aliasing
#   artefacts. With anti-aliasing (LANCZOS), fine details are smoothly blurred out
#   instead. In both cases, the detail is gone — only the failure mode differs.
# ───────────────────────────────────────────────────────────

chrono_path = DIP_CH02 / 'Fig0220(a)(chronometer 3692x2812  2pt25 inch 1250 dpi).tif'
chrono_pil  = Image.open(chrono_path).convert('L')

# Work with a 512×512 crop from the centre to keep runtime manageable
chrono_w, chrono_h = chrono_pil.size
crop_w, crop_h = 512, 512
left   = (chrono_w - crop_w) // 2
top    = (chrono_h - crop_h) // 2
chrono_crop = chrono_pil.crop((left, top, left + crop_w, top + crop_h))
original_size = chrono_crop.size

target_resolutions = [256, 128, 64]

fig, axes = plt.subplots(2, len(target_resolutions) + 1, figsize=(16, 9))
fig.suptitle('Downsampling: With vs Without Anti-Aliasing Filter\n'
             '(both lose detail — only artefact type differs)', fontsize=13)

axes[0, 0].imshow(np.array(chrono_crop), cmap='gray')
axes[0, 0].set_title(f'Original\n{original_size[0]}×{original_size[1]}', fontsize=10)
axes[0, 0].axis('off')
axes[1, 0].axis('off')

for col, target_res in enumerate(target_resolutions, start=1):
    # No anti-aliasing: nearest-neighbour downsample
    downsampled_nearest = chrono_crop.resize((target_res, target_res), Image.NEAREST)
    upscaled_nearest    = downsampled_nearest.resize(original_size, Image.NEAREST)

    # With anti-aliasing: LANCZOS (low-pass filter before downsampling)
    downsampled_lanczos = chrono_crop.resize((target_res, target_res), Image.LANCZOS)
    upscaled_lanczos    = downsampled_lanczos.resize(original_size, Image.NEAREST)

    axes[0, col].imshow(np.array(upscaled_nearest), cmap='gray')
    axes[0, col].set_title(f'{target_res}×{target_res}\nNo AA (aliasing)', fontsize=10)
    axes[0, col].axis('off')

    axes[1, col].imshow(np.array(upscaled_lanczos), cmap='gray')
    axes[1, col].set_title(f'{target_res}×{target_res}\nWith LANCZOS AA (smooth blur)', fontsize=10)
    axes[1, col].axis('off')

plt.tight_layout()
plt.show()


# ── Algorithm ──────────────────────────────────────────────
# Checkerboard aliasing: the canonical example
# 1. Create a checkerboard at the Nyquist frequency (1 pixel per square)
# 2. Downsample by 2× without filtering (simple slice every other row/col)
# 3. Downsample by 2× with low-pass filter (LANCZOS)
# 4. Display original and both downsampled versions
# What to look for: raw downsampling of a Nyquist-frequency pattern produces
#   a completely wrong result (solid grey or inverted pattern). LANCZOS produces
#   a smooth grey — correct, since there is no real low-frequency content.
# ───────────────────────────────────────────────────────────

checkerboard_size = 128   # 128×128 pixels
# Create: even+even rows = white, even+odd = black, etc.
row_indices = np.arange(checkerboard_size)
col_indices = np.arange(checkerboard_size)
row_grid, col_grid = np.meshgrid(row_indices, col_indices, indexing='ij')
checkerboard = ((row_grid + col_grid) % 2 * 255).astype(np.uint8)
checkerboard_pil = Image.fromarray(checkerboard)

# Downsample by 2× without any filtering (just take every other pixel)
downsampled_raw   = checkerboard[::2, ::2]
# Downsample with LANCZOS (anti-aliasing)
half_size         = checkerboard_size // 2
downsampled_aa    = np.array(
    checkerboard_pil.resize((half_size, half_size), Image.LANCZOS)
)

fig, axes = plt.subplots(1, 3, figsize=(12, 4))
fig.suptitle('Checkerboard Aliasing: Nyquist-Frequency Pattern\n'
             'Downsampled 2× — With and Without Anti-Aliasing', fontsize=13)

axes[0].imshow(checkerboard, cmap='gray', vmin=0, vmax=255, interpolation='nearest')
axes[0].set_title(f'Original\n{checkerboard_size}×{checkerboard_size}\n'
                  f'(1 px/square — at Nyquist)', fontsize=11)
axes[0].axis('off')

axes[1].imshow(downsampled_raw, cmap='gray', vmin=0, vmax=255, interpolation='nearest')
axes[1].set_title(f'Downsampled 2× — no AA\n{half_size}×{half_size}\n'
                  f'mean={downsampled_raw.mean():.0f}', fontsize=11)
axes[1].axis('off')

axes[2].imshow(downsampled_aa, cmap='gray', vmin=0, vmax=255, interpolation='nearest')
axes[2].set_title(f'Downsampled 2× — LANCZOS AA\n{half_size}×{half_size}\n'
                  f'mean={downsampled_aa.mean():.0f}', fontsize=11)
axes[2].axis('off')

plt.tight_layout()
plt.show()

print("Checkerboard aliasing demo:")
print(f"  Original: min={checkerboard.min()}, max={checkerboard.max()}, "
      f"mean={checkerboard.mean():.0f}")
print(f"  Raw 2× downsample: min={downsampled_raw.min()}, max={downsampled_raw.max()}, "
      f"mean={downsampled_raw.mean():.0f}")
print(f"  LANCZOS downsample: min={downsampled_aa.min()}, max={downsampled_aa.max()}, "
      f"mean={downsampled_aa.mean():.0f}")
print()
print("Raw downsample aliases the checkerboard to a wrong pattern.")
print("LANCZOS correctly smooths to grey (the signal is all high-frequency).")
