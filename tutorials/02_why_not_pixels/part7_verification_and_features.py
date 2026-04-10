"""
Part 7: Verification on Real Images, Features, and CNN Motivation
==================================================================
Verifies normalisation fixes on real images via OpenCV template matching,
demonstrates why rotation cannot be fixed by per-pixel math, introduces
hand-designed features as a stepping stone, and visualises pixel space
vs learned feature space.
"""

# --- Setup ---
from pathlib import Path
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

COLORS = {
    'primary': '#2196F3',
    'secondary': '#4CAF50',
    'result': '#FFC107',
    'highlight': '#F44336',
    'transform': '#9C27B0',
    'gradient': '#FF9800',
}

CH02_DIR = Path(__file__).parent / '../../DIP3E_Original_Images_CH02'
CH03_DIR = Path(__file__).parent / '../../DIP3E_Original_Images_CH03'

# ── Algorithm ──────────────────────────────────────────────
# 1. Load image, create template and transformed scenes
# 2. Run TM_SQDIFF_NORMED and TM_CCOEFF_NORMED on all scenes
# 3. Summarise in a comparative bar chart
# 4. Show pixel-level rotation breakdown on a 5×5 patch
# 5. Hand-designed feature (edge count) vs pixel SSD for T-shape / circle
# 6. Conceptual visualisation: pixel space (scattered) vs feature space (clustered)
# What to look for: CCOEFF_NORMED scores ~1.0 for brightness, <1.0 for rotation/scale
# ───────────────────────────────────────────────────────────

def load_image(fallback_size: int = 256) -> np.ndarray:
    """Load a DIP3E image or create a synthetic gradient fallback."""
    candidates = list(CH02_DIR.glob('*.tif')) + list(CH02_DIR.glob('*.png'))
    if candidates:
        img = cv2.imread(str(candidates[0]), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            return img
    row = np.linspace(20, 240, fallback_size)
    col = np.linspace(20, 200, fallback_size)
    return (row[np.newaxis, :] * 0.5 + col[:, np.newaxis] * 0.5).astype(np.uint8)


def crop_template(scene: np.ndarray, size: int = 64) -> tuple[np.ndarray, tuple[int, int]]:
    """Crop a square template from the centre of the scene."""
    h, w = scene.shape
    top  = h // 2 - size // 2
    left = w // 2 - size // 2
    return scene[top:top + size, left:left + size].copy(), (top, left)


def apply_transforms(scene: np.ndarray) -> dict[str, np.ndarray]:
    """Return transformed scene images."""
    h, w = scene.shape
    centre      = (w / 2, h / 2)
    rot_matrix  = cv2.getRotationMatrix2D(centre, 5, 1.0)
    rotated     = cv2.warpAffine(scene, rot_matrix, (w, h), flags=cv2.INTER_LINEAR)
    new_w, new_h = int(w * 0.9), int(h * 0.9)
    shrunk      = cv2.resize(scene, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    scaled      = np.zeros_like(scene)
    scaled[:new_h, :new_w] = shrunk
    bright      = np.clip(scene.astype(float) * 0.7, 0, 255).astype(np.uint8)
    return {
        'Original': scene,
        'Rotated 5°': rotated,
        'Scaled 90%': scaled,
        'Brightness ×0.7': bright,
    }


# ── 1. Real-image verification ──────────────────────────────
scene    = load_image()
template, top_left = crop_template(scene)
scenes   = apply_transforms(scene)

results_sqdiff  = {}
results_ccoeff  = {}

for name, altered in scenes.items():
    # TM_SQDIFF_NORMED (lower = better, 0 = perfect)
    res_sq = cv2.matchTemplate(altered, template, cv2.TM_SQDIFF_NORMED)
    r, c   = min(top_left[0], res_sq.shape[0] - 1), min(top_left[1], res_sq.shape[1] - 1)
    results_sqdiff[name] = float(res_sq[r, c])

    # TM_CCOEFF_NORMED (higher = better, 1 = perfect)
    res_cc = cv2.matchTemplate(altered, template, cv2.TM_CCOEFF_NORMED)
    r2, c2 = min(top_left[0], res_cc.shape[0] - 1), min(top_left[1], res_cc.shape[1] - 1)
    results_ccoeff[name] = float(res_cc[r2, c2])

print("=== Template Matching: All Methods on All Transforms ===")
print(f"{'Scene':20s}  {'SQDIFF_N (↓0)':>14s}  {'CCOEFF_N (↑1)':>14s}")
print("─" * 55)
for name in scenes:
    sq  = results_sqdiff[name]
    cc  = results_ccoeff[name]
    print(f"{name:20s}  {sq:>14.4f}  {cc:>14.4f}")

# ── Bar chart ──────────────────────────────────────────────
names   = list(scenes.keys())
sq_vals = [results_sqdiff[n] for n in names]
cc_vals = [results_ccoeff[n] for n in names]

x     = np.arange(len(names))
width = 0.35

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

bars1 = axes[0].bar(x, sq_vals, width, color=COLORS['primary'], alpha=0.85)
axes[0].set_title('TM_SQDIFF_NORMED (lower = better)', fontsize=12)
axes[0].set_xticks(x); axes[0].set_xticklabels(names, rotation=15, ha='right', fontsize=9)
axes[0].axhline(y=0.01, color='gray', linestyle='--', alpha=0.5, label='threshold')
axes[0].set_ylabel('Score'); axes[0].legend(fontsize=9)

bars2 = axes[1].bar(x, cc_vals, width, color=COLORS['secondary'], alpha=0.85)
axes[1].set_title('TM_CCOEFF_NORMED (higher = better)', fontsize=12)
axes[1].set_xticks(x); axes[1].set_xticklabels(names, rotation=15, ha='right', fontsize=9)
axes[1].axhline(y=0.99, color='gray', linestyle='--', alpha=0.5, label='good match')
axes[1].set_ylabel('Score'); axes[1].legend(fontsize=9)

plt.suptitle('Normalisation Fixes Brightness — Cannot Fix Spatial Transforms', fontsize=13)
plt.tight_layout()
plt.show()

# ── 2. Why rotation breaks pixels ─────────────────────────
small_pattern = np.zeros((5, 5), dtype=float)
small_pattern[1, 1:4] = 200
small_pattern[2, 2]   = 255
small_pattern[3, 1:4] = 200

centre_rot    = (2, 2)
rotation_mat  = cv2.getRotationMatrix2D(centre_rot, 15, 1.0)
rotated_patt  = cv2.warpAffine(small_pattern.astype(np.float32),
                                rotation_mat, (5, 5), flags=cv2.INTER_LINEAR)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].imshow(small_pattern, cmap='gray', vmin=0, vmax=255)
for i in range(5):
    for j in range(5):
        axes[0].text(j, i, f'{small_pattern[i,j]:.0f}', ha='center', va='center',
                     color='yellow' if small_pattern[i,j] < 128 else 'red', fontsize=9)
axes[0].set_title('Original Pattern', fontsize=12)
axes[0].set_xticks(range(5)); axes[0].set_yticks(range(5))

axes[1].imshow(rotated_patt, cmap='gray', vmin=0, vmax=255)
for i in range(5):
    for j in range(5):
        axes[1].text(j, i, f'{rotated_patt[i,j]:.0f}', ha='center', va='center',
                     color='yellow' if rotated_patt[i,j] < 128 else 'red', fontsize=9)
axes[1].set_title('Rotated 15° (interpolated)', fontsize=12)
axes[1].set_xticks(range(5)); axes[1].set_yticks(range(5))

diff = np.abs(small_pattern - rotated_patt)
axes[2].imshow(diff, cmap='hot', vmin=0, vmax=255)
for i in range(5):
    for j in range(5):
        axes[2].text(j, i, f'{diff[i,j]:.0f}', ha='center', va='center',
                     color='white', fontsize=9)
axes[2].set_title('|Original - Rotated|', fontsize=12)
axes[2].set_xticks(range(5)); axes[2].set_yticks(range(5))

plt.suptitle('Rotation: Pixels Move to New Positions → Per-Pixel Comparison Meaningless', fontsize=13)
plt.tight_layout()
plt.show()

print(f"SSD between original and rotated: {np.sum(diff**2):.0f}")
print("Every pixel has changed. No per-pixel operation can undo this.")
print("The problem is SPATIAL, not INTENSITY.")

# ── 3. Hand-designed feature vs pixel SSD ─────────────────

def make_T_shape(size: int = 15, angle: float = 0.0) -> np.ndarray:
    """Create a T-shaped pattern, optionally rotated."""
    img = np.zeros((size, size), dtype=np.float32)
    img[3, 3:12] = 200
    img[4, 3:12] = 200
    img[3:12, 7] = 200
    img[3:12, 8] = 200
    if angle != 0:
        centre = (size // 2, size // 2)
        M = cv2.getRotationMatrix2D(centre, angle, 1.0)
        img = cv2.warpAffine(img, M, (size, size), flags=cv2.INTER_LINEAR)
    return img


t_0   = make_T_shape(angle=0)
t_15  = make_T_shape(angle=15)
t_45  = make_T_shape(angle=45)
not_t = np.zeros((15, 15), dtype=np.float32)
cv2.circle(not_t, (7, 7), 5, 200, 2)

shapes = [(t_0, 'T (0°)'), (t_15, 'T (15°)'), (t_45, 'T (45°)'), (not_t, 'Circle')]

fig, axes = plt.subplots(2, 4, figsize=(16, 8))

for ax, (img, title) in zip(axes[0], shapes):
    ax.imshow(img, cmap='gray', vmin=0, vmax=255)
    ax.set_title(title, fontsize=12)
    ax.axis('off')

ssd_scores  = []
edge_counts = []
for img, _ in shapes:
    ssd_score = float(np.sum((img - t_0) ** 2))
    ssd_scores.append(ssd_score)

    gradient_x = np.diff(img, axis=1)
    gradient_y = np.diff(img, axis=0)
    gx = np.zeros_like(img); gx[:, :-1] = gradient_x
    gy = np.zeros_like(img); gy[:-1, :] = gradient_y
    gradient_magnitude = np.sqrt(gx**2 + gy**2)
    edge_counts.append(int(np.sum(gradient_magnitude > 50)))

names_shapes    = [s[1] for s in shapes]
bar_colors_ssd  = [COLORS['secondary'], COLORS['result'], COLORS['highlight'], COLORS['highlight']]
bar_colors_edge = [COLORS['secondary'], COLORS['secondary'], COLORS['secondary'], COLORS['highlight']]

axes[1, 0].bar(range(4), ssd_scores, color=bar_colors_ssd, alpha=0.8)
axes[1, 0].set_xticks(range(4)); axes[1, 0].set_xticklabels(names_shapes, fontsize=9)
axes[1, 0].set_title('Pixel SSD vs T(0°)', fontsize=11)
axes[1, 0].set_ylabel('SSD (lower=similar)')

axes[1, 1].bar(range(4), edge_counts, color=bar_colors_edge, alpha=0.8)
axes[1, 1].set_xticks(range(4)); axes[1, 1].set_xticklabels(names_shapes, fontsize=9)
axes[1, 1].set_title('Edge Count (feature)', fontsize=11)
axes[1, 1].set_ylabel('# edge pixels')

axes[1, 2].axis('off')
axes[1, 3].axis('off')
axes[1, 2].text(0.1, 0.5,
    'Pixel SSD: T(15°) looks as different\n'
    "as the circle — it can't tell rotation\n"
    'from a different shape!\n\n'
    'Edge count: all T shapes have similar\n'
    'edge counts, circle is different.\n'
    'A simple FEATURE already works better\n'
    'than raw pixels for rotation invariance.',
    transform=axes[1, 2].transAxes, fontsize=11,
    verticalalignment='center',
    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.suptitle('Pixels vs Features: Which Can Handle Rotation?', fontsize=14, y=1.02)
plt.tight_layout()
plt.show()

# ── 4. Pixel space vs feature space (conceptual) ──────────
np.random.seed(42)
t_positions_pixel   = np.array([[2, 8], [7, 3], [5, 9], [1, 4], [8, 7]])
c_positions_pixel   = np.array([[3, 5], [6, 6], [4, 2], [9, 4]])
t_positions_feature = np.array([[2, 7], [2.3, 7.5], [1.8, 7.2], [2.5, 6.8], [2.1, 7.3]])
c_positions_feature = np.array([[7, 2.5], [7.3, 2.2], [6.8, 2.8], [7.1, 2.3]])

fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Pixel space
axes[0].scatter(t_positions_pixel[:, 0], t_positions_pixel[:, 1],
                s=200, c=COLORS['primary'], marker='s', label='T shapes (various rotations)', zorder=5)
axes[0].scatter(c_positions_pixel[:, 0], c_positions_pixel[:, 1],
                s=200, c=COLORS['highlight'], marker='o', label='Circles', zorder=5)
for i, pos in enumerate(t_positions_pixel):
    axes[0].annotate(f'T({i*15}°)', pos, textcoords='offset points', xytext=(8, 8), fontsize=9)
for i, pos in enumerate(c_positions_pixel):
    axes[0].annotate(f'C{i+1}', pos, textcoords='offset points', xytext=(8, 8), fontsize=9)
axes[0].set_title('Pixel Space\n(SSD distance)', fontsize=13)
axes[0].set_xlabel('Pixel dimension 1', fontsize=11)
axes[0].set_ylabel('Pixel dimension 2', fontsize=11)
axes[0].legend(fontsize=10)
axes[0].set_xlim(0, 10); axes[0].set_ylim(0, 10)
axes[0].grid(True, alpha=0.3)
axes[0].text(5, 0.5, "T shapes scattered among circles!\nSSD can't tell them apart.",
             ha='center', fontsize=10, color=COLORS['highlight'],
             bbox=dict(facecolor='white', alpha=0.8))

# Feature space
axes[1].scatter(t_positions_feature[:, 0], t_positions_feature[:, 1],
                s=200, c=COLORS['primary'], marker='s', label='T shapes (clustered!)', zorder=5)
axes[1].scatter(c_positions_feature[:, 0], c_positions_feature[:, 1],
                s=200, c=COLORS['highlight'], marker='o', label='Circles (clustered!)', zorder=5)
t_ellipse = Ellipse((2.1, 7.2), 1.5, 1.5, fill=False,
                     edgecolor=COLORS['primary'], linewidth=2, linestyle='--')
c_ellipse = Ellipse((7.05, 2.45), 1.2, 1.2, fill=False,
                     edgecolor=COLORS['highlight'], linewidth=2, linestyle='--')
axes[1].add_patch(t_ellipse)
axes[1].add_patch(c_ellipse)
axes[1].set_title('Feature Space (learned by CNN)\n(semantic distance)', fontsize=13)
axes[1].set_xlabel('Feature dimension 1', fontsize=11)
axes[1].set_ylabel('Feature dimension 2', fontsize=11)
axes[1].legend(fontsize=10)
axes[1].set_xlim(0, 10); axes[1].set_ylim(0, 10)
axes[1].grid(True, alpha=0.3)
axes[1].text(5, 0.5, 'Same shape = nearby, different shape = far apart.\nDistance = semantic similarity!',
             ha='center', fontsize=10, color=COLORS['secondary'],
             bbox=dict(facecolor='white', alpha=0.8))

plt.suptitle('The Promise of Deep Learning: A Space Where Distance = Meaning', fontsize=14, y=1.02)
plt.tight_layout()
plt.show()

print("In pixel space: T(0°) and T(15°) are as far apart as T(0°) and a circle.")
print("In feature space: all T shapes cluster together, far from circles.")
print("\nThis is what a CNN learns — a coordinate system where distance = similarity.")
