"""
Part 1: Pixel Matching Failure
==============================
Demonstrates that raw pixel comparison (SSD / TM_SQDIFF_NORMED) breaks under
three transforms that occur constantly in real-world imaging: rotation, scale,
and brightness change.

Runs on any scene image. Falls back to a synthetic gradient if no image is found.
"""

# --- Setup ---
from pathlib import Path
import numpy as np
import cv2
import matplotlib.pyplot as plt

COLORS = {
    'primary': '#2196F3',
    'secondary': '#4CAF50',
    'result': '#FFC107',
    'highlight': '#F44336',
    'transform': '#9C27B0',
    'gradient': '#FF9800',
}

# Image paths — DIP3E images relative to this file's folder
CH02_DIR = Path(__file__).parent / '../../DIP3E_Original_Images_CH02'
CH03_DIR = Path(__file__).parent / '../../DIP3E_Original_Images_CH03'

# ── Algorithm ──────────────────────────────────────────────
# 1. Load a grayscale image (fall back to synthetic if not found)
# 2. Crop a template patch from the centre of the image
# 3. Apply three transforms to create altered scene images:
#    - Rotation (5°): warp the entire scene
#    - Scale (90%): resize down then pad back to original size
#    - Brightness ×0.7: multiply all pixel values
# 4. Run cv2.matchTemplate (TM_SQDIFF_NORMED) on each scene
# 5. Read the score at the known correct location
# What to look for: near-zero score for original, high scores for transforms
# ───────────────────────────────────────────────────────────

def load_image(fallback_size: int = 256) -> np.ndarray:
    """Load a DIP3E image or create a synthetic gradient fallback."""
    candidates = list(CH02_DIR.glob('*.tif')) + list(CH02_DIR.glob('*.png'))
    if candidates:
        img = cv2.imread(str(candidates[0]), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            print(f"Loaded: {candidates[0].name}")
            return img
    # Synthetic gradient fallback
    print("No DIP3E image found — using synthetic gradient.")
    row = np.linspace(20, 240, fallback_size)
    col = np.linspace(20, 200, fallback_size)
    grid = (row[np.newaxis, :] * 0.5 + col[:, np.newaxis] * 0.5).astype(np.uint8)
    return grid


def crop_template(scene: np.ndarray, size: int = 64) -> tuple[np.ndarray, tuple[int, int]]:
    """Crop a square patch from the centre of the scene."""
    h, w = scene.shape
    top = h // 2 - size // 2
    left = w // 2 - size // 2
    template = scene[top:top + size, left:left + size].copy()
    return template, (top, left)


def apply_transforms(scene: np.ndarray) -> dict[str, np.ndarray]:
    """Return a dict of transformed scene images."""
    h, w = scene.shape

    # Rotation 5°
    centre = (w / 2, h / 2)
    rot_matrix = cv2.getRotationMatrix2D(centre, 5, 1.0)
    rotated = cv2.warpAffine(scene, rot_matrix, (w, h), flags=cv2.INTER_LINEAR)

    # Scale 90% — resize then pad
    new_w, new_h = int(w * 0.9), int(h * 0.9)
    shrunk = cv2.resize(scene, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    scaled = np.zeros_like(scene)
    scaled[:new_h, :new_w] = shrunk

    # Brightness ×0.7
    bright = np.clip(scene.astype(float) * 0.7, 0, 255).astype(np.uint8)

    return {
        'Original': scene,
        'Rotated 5°': rotated,
        'Scaled 90%': scaled,
        'Brightness ×0.7': bright,
    }


def match_score(scene: np.ndarray,
                template: np.ndarray,
                top_left: tuple[int, int]) -> float:
    """Run TM_SQDIFF_NORMED and return the score at the known location."""
    result = cv2.matchTemplate(scene, template, cv2.TM_SQDIFF_NORMED)
    row, col = top_left
    # Result map is smaller than scene by (template_h-1, template_w-1)
    r = min(row, result.shape[0] - 1)
    c = min(col, result.shape[1] - 1)
    return float(result[r, c])


# ── Main ────────────────────────────────────────────────────

scene = load_image()
template, top_left = crop_template(scene)
print(f"Scene size: {scene.shape}  |  Template size: {template.shape}")

scenes = apply_transforms(scene)
results: dict[str, float] = {}

for name, altered_scene in scenes.items():
    score = match_score(altered_scene, template, top_left)
    results[name] = score
    status = "PASS ✓" if score < 0.01 else "FAIL ✗"
    print(f"{name:20s}  SQDIFF_NORMED = {score:.4f}  {status}")

# ── Visualisation: bar chart of scores ─────────────────────
fig, ax = plt.subplots(figsize=(10, 5))

names = list(results.keys())
scores = list(results.values())
bar_colors = [COLORS['secondary'] if s < 0.01 else
              COLORS['result'] if s < 0.1 else
              COLORS['highlight'] for s in scores]

bars = ax.barh(range(len(names)), scores, color=bar_colors, alpha=0.85)
ax.set_yticks(range(len(names)))
ax.set_yticklabels(names, fontsize=11)
ax.set_xlabel('SQDIFF_NORMED Score (lower = better match)', fontsize=12)
ax.set_title('Template Matching Scores Under Real-World Transforms', fontsize=14)
ax.axvline(x=0.01, color='gray', linestyle='--', alpha=0.5, label='Good match threshold')
ax.legend(fontsize=10)

for i, (bar, score) in enumerate(zip(bars, scores)):
    ax.text(score + 0.005, i, f'{score:.4f}', va='center', fontsize=10)

ax.invert_yaxis()
plt.tight_layout()
plt.show()

print("\nEvery real-world transform degrades the pixel match.")
print("But brightness is DIFFERENT from rotation/scale — we can fix brightness mathematically.")
