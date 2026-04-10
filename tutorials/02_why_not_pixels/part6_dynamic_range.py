"""
Part 6: Brightness, Contrast, Dynamic Range, and Clipping
==========================================================
Demonstrates brightness (I+b) and contrast (a*I) changes in image terms,
contrast stretching, the clipping problem (histogram spike at 255), and
quantization loss from limited bit depth.
"""

# --- Setup ---
import numpy as np
import matplotlib.pyplot as plt

COLORS = {
    'primary': '#2196F3',
    'secondary': '#4CAF50',
    'result': '#FFC107',
    'highlight': '#F44336',
    'transform': '#9C27B0',
    'gradient': '#FF9800',
}


def pearson_correlation(x: np.ndarray, y: np.ndarray) -> float:
    """Pearson correlation coefficient."""
    return float(np.corrcoef(x, y)[0, 1])


# ── Algorithm ──────────────────────────────────────────────
# 1. Show brightness change (I+b): differences preserved, pattern unchanged
# 2. Show contrast change (a*I): ratios preserved, spread changes
# 3. Compute dynamic range for sample patches
# 4. Contrast stretching: remap [min,max] to [0,255], verify Pearson=1
# 5. Histogram before/after stretching — show gaps
# 6. Clipping: multiply by 2 in 8-bit → values above 255 lost → spike at 255
# 7. Quantization loss: narrow range stretched → large gaps in histogram
# What to look for: stretching = linear transform (Pearson 1.0);
# clipping spike at 255; quantization gaps after stretching narrow range
# ───────────────────────────────────────────────────────────

# --- Brightness change ---
original = np.array([100, 150, 200], dtype=float)
brighter = original + 30
darker   = original - 50

print("=== Brightness Change (I + b) ===")
print(f"Original:     {original.astype(int)}   differences: {np.diff(original).astype(int)}")
print(f"Brighter +30: {brighter.astype(int)}   differences: {np.diff(brighter).astype(int)}")
print(f"Darker -50:   {darker.astype(int)}    differences: {np.diff(darker).astype(int)}")
print("→ Differences between pixels stay the same. Pattern preserved, just shifted up/down.")

# --- Contrast change ---
original = np.array([100, 150, 200], dtype=float)
high_contrast = original * 2
low_contrast  = original * 0.5

print("\n=== Contrast Change (a · I) ===")
print(f"Original:          {original.astype(int)}    spread = {original.max() - original.min():.0f}")
print(f"Contrast ×2:       {high_contrast.astype(int)}    spread = {high_contrast.max() - high_contrast.min():.0f}")
print(f"Contrast ×0.5:     {low_contrast.astype(int)}     spread = {low_contrast.max() - low_contrast.min():.0f}")
print(f"\nRatios preserved? 150/100 = {150/100}, 300/200 = {300/200}  ✓")
print("→ Pattern shape is the same — just stretched or compressed.")

# --- Dynamic range ---
patches = [
    np.array([100, 150, 200], dtype=float),
    np.array([10,  110, 210], dtype=float),
    np.array([0,   128, 255], dtype=float),
]

print("\n=== Dynamic Range = max - min ===")
for patch in patches:
    dynamic_range = patch.max() - patch.min()
    print(f"{patch.astype(int)}  → dynamic range = {dynamic_range:.0f}  "
          f"(using {dynamic_range/255*100:.0f}% of available levels)")

# --- Contrast stretching ---
low_contrast_image = np.array([100, 130, 160], dtype=float)
min_value  = low_contrast_image.min()
max_value  = low_contrast_image.max()
stretched_image = (low_contrast_image - min_value) / (max_value - min_value) * 255

print("\n=== Contrast Stretching ===")
print(f"Original:    {low_contrast_image.astype(int)}   dynamic range = {max_value - min_value:.0f}")
print(f"Stretched:   {stretched_image.astype(int)}     dynamic range = {stretched_image.max() - stretched_image.min():.0f}")

# Still a linear transform → Pearson correlation = 1
r = pearson_correlation(low_contrast_image, stretched_image)
print(f"\nPearson correlation between original and stretched: r = {r:.3f}")
print("→ Contrast stretching is Y = aX + b → Pearson invariant.")

# ── Histogram before/after contrast stretching ─────────────
np.random.seed(42)
low_contrast_pixels = np.random.randint(100, 161, size=1000).astype(float)
min_val = low_contrast_pixels.min()
max_val = low_contrast_pixels.max()
stretched_pixels = (low_contrast_pixels - min_val) / (max_val - min_val) * 255

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(low_contrast_pixels, bins=range(0, 256), color=COLORS['primary'], alpha=0.7)
axes[0].set_xlim(0, 255)
axes[0].set_title(f'Before: Dynamic Range = {max_val - min_val:.0f}', fontsize=13)
axes[0].set_xlabel('Pixel Intensity', fontsize=12)
axes[0].set_ylabel('Count', fontsize=12)
axes[0].axvline(min_val, color=COLORS['highlight'], linestyle='--', label=f'min={min_val:.0f}')
axes[0].axvline(max_val, color=COLORS['highlight'], linestyle='--', label=f'max={max_val:.0f}')
axes[0].legend(fontsize=10)

axes[1].hist(stretched_pixels, bins=range(0, 256), color=COLORS['secondary'], alpha=0.7)
axes[1].set_xlim(0, 255)
axes[1].set_title('After Contrast Stretching: Dynamic Range = 255', fontsize=13)
axes[1].set_xlabel('Pixel Intensity', fontsize=12)
axes[1].set_ylabel('Count', fontsize=12)

plt.tight_layout()
plt.show()
print("Notice the histogram spreads out but has GAPS — no new values are created.")

# ── Clipping problem ────────────────────────────────────────
original_clip = np.array([100, 200, 150, 250, 180], dtype=float)
multiplied    = original_clip * 2
clipped       = np.clip(multiplied, 0, 255)

print("\n=== Multiplying by 2 in 8-bit ===")
print(f"Original:    {original_clip.astype(int)}")
print(f"× 2:         {multiplied.astype(int)}")
print(f"Clipped:     {clipped.astype(int)}")
print("\n200×2=400 and 250×2=500 both clipped to 255.")
print("Two different values collapsed → information LOST.")

np.random.seed(42)
image_pixels  = np.random.randint(50, 220, size=2000).astype(float)
doubled_pixels = np.clip(image_pixels * 2, 0, 255)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(image_pixels, bins=range(0, 256), color=COLORS['primary'], alpha=0.7)
axes[0].set_xlim(0, 260)
axes[0].set_title('Original Image Histogram', fontsize=13)
axes[0].set_xlabel('Pixel Intensity', fontsize=12)
axes[0].set_ylabel('Count', fontsize=12)

axes[1].hist(doubled_pixels, bins=range(0, 256), color=COLORS['highlight'], alpha=0.7)
axes[1].set_xlim(0, 260)
axes[1].set_title('After ×2 (Clipped to [0, 255])', fontsize=13)
axes[1].set_xlabel('Pixel Intensity', fontsize=12)
axes[1].set_ylabel('Count', fontsize=12)

clipped_count = np.sum(doubled_pixels == 255)
axes[1].annotate(f'{clipped_count} pixels\npiled at 255',
                 xy=(255, clipped_count), fontsize=11,
                 xytext=(200, clipped_count + 20),
                 arrowprops=dict(arrowstyle='->', color=COLORS['gradient']),
                 color=COLORS['gradient'], fontweight='bold')

plt.tight_layout()
plt.show()

# ── Quantization loss ───────────────────────────────────────
narrow_range = np.array([100, 101, 102, 103], dtype=float)
min_val_q    = narrow_range.min()
max_val_q    = narrow_range.max()
stretched_q  = (narrow_range - min_val_q) / (max_val_q - min_val_q) * 255

print("\n=== Quantization Loss ===")
print(f"Original (4 distinct values): {narrow_range.astype(int)}")
print(f"Stretched to [0, 255]:        {stretched_q.astype(int)}")
print(f"\nOnly 4 values spread across 256 levels.")
print(f"Gaps in the histogram: nothing at 1, 2, 3, ... 84, 86, ... etc.")
print(f"You can't invent the 252 missing values — the information was never there.")
print(f"\nThis is why HDR/medical imaging uses 12-bit, 16-bit, or float32.")
print(f"  8-bit:  {2**8:>6d} levels")
print(f" 12-bit:  {2**12:>6d} levels")
print(f" 16-bit:  {2**16:>6d} levels")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].bar(narrow_range, [1, 1, 1, 1], width=0.5, color=COLORS['primary'], alpha=0.8)
axes[0].set_xlim(98, 105)
axes[0].set_title('Original: 4 Values in [100, 103]', fontsize=13)
axes[0].set_xlabel('Pixel Intensity', fontsize=12)
axes[0].set_ylabel('Count', fontsize=12)

axes[1].bar(stretched_q, [1, 1, 1, 1], width=3, color=COLORS['secondary'], alpha=0.8)
axes[1].set_xlim(-10, 265)
axes[1].set_title('Stretched to [0, 255]: Gaps Everywhere', fontsize=13)
axes[1].set_xlabel('Pixel Intensity', fontsize=12)
axes[1].set_ylabel('Count', fontsize=12)

for i in range(len(stretched_q) - 1):
    gap_start = stretched_q[i] + 1
    gap_end   = stretched_q[i + 1] - 1
    mid = (gap_start + gap_end) / 2
    axes[1].annotate(f'gap\n({int(gap_end - gap_start)} empty levels)',
                     xy=(mid, 0.5), fontsize=9, ha='center',
                     color=COLORS['highlight'])

plt.tight_layout()
plt.show()
