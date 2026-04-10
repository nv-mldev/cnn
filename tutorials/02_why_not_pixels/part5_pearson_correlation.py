"""
Part 5: Combining Both Fixes — Pearson Correlation (CCOEFF_NORMED)
===================================================================
Shows that mean subtraction + L2 normalisation together produce the Pearson
correlation coefficient, which is invariant to any positive linear transform
I = a*T + b.  Compares SSD, SQDIFF_NORMED, and CCOEFF_NORMED on a table of
test patches, and verifies against numpy's built-in corrcoef.
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

# ── Algorithm ──────────────────────────────────────────────
# 1. Define three matching metrics: SSD, SQDIFF_NORMED, CCOEFF_NORMED
# 2. Run all three on a table of test patches (identical, brightness-shifted,
#    contrast-scaled, both transforms, different pattern)
# 3. Show CCOEFF_NORMED gives 1.0 for any aX+b of the template
# 4. Demonstrate the step-by-step algebra: centering removes b, norm removes a
# 5. Show statistical equivalence: variance = squared L2 norm / n
# 6. Verify CCOEFF_NORMED equals numpy corrcoef
# What to look for: CCOEFF_NORMED = 1.0 for all affine-related patches,
# <1.0 for different pattern
# ───────────────────────────────────────────────────────────

# --- Define metrics ---
def ssd(patch: np.ndarray, template: np.ndarray) -> float:
    """Raw sum of squared differences."""
    return float(np.sum((patch - template) ** 2))


def ssd_normed(patch: np.ndarray, template: np.ndarray) -> float:
    """SSD normalised by L2 norms (equivalent to TM_SQDIFF_NORMED)."""
    numerator   = np.sum((patch - template) ** 2)
    denominator = np.sqrt(np.sum(patch ** 2)) * np.sqrt(np.sum(template ** 2))
    return float(numerator / denominator)


def ccoeff_normed(patch: np.ndarray, template: np.ndarray) -> float:
    """Cross-correlation of centred, normalised vectors (TM_CCOEFF_NORMED = Pearson r)."""
    patch_centered    = patch    - np.mean(patch)
    template_centered = template - np.mean(template)
    numerator   = np.sum(patch_centered * template_centered)
    denominator = (np.sqrt(np.sum(patch_centered ** 2)) *
                   np.sqrt(np.sum(template_centered ** 2)))
    return float(numerator / denominator)


def pearson_correlation(x: np.ndarray, y: np.ndarray) -> float:
    """Pearson r via numpy corrcoef (reference implementation)."""
    return float(np.corrcoef(x, y)[0, 1])


# --- Comparison table ---
template = np.array([100, 150, 200], dtype=float)

test_cases = [
    ("Identical",          np.array([100, 150, 200], dtype=float)),
    ("Brightness +30",     np.array([130, 180, 230], dtype=float)),
    ("Contrast ×2",        np.array([200, 300, 400], dtype=float)),
    ("Both (×2 + 30)",     np.array([230, 330, 430], dtype=float)),
    ("Different pattern",  np.array([200, 100, 180], dtype=float)),
]

print(f"Template: {template.astype(int)}")
print("─" * 80)
print(f"{'Patch':20s}  {'Values':18s}  {'SSD':>8s}  {'SQDIFF_N':>8s}  {'CCOEFF_N':>8s}")
print("─" * 80)
for name, patch in test_cases:
    raw_ssd  = ssd(patch, template)
    normed   = ssd_normed(patch, template)
    ccoeff   = ccoeff_normed(patch, template)
    print(f"{name:20s}  {str(patch.astype(int)):18s}  {raw_ssd:>8.0f}  {normed:>8.3f}  {ccoeff:>+8.3f}")

print("─" * 80)
print("\nSSD: lower = better (0 = perfect).  Raw values are not comparable across patches.")
print("SQDIFF_NORMED: normalised but NOT brightness-invariant.")
print("CCOEFF_NORMED: normalised AND brightness/contrast invariant (Pearson r).")

# --- Step-by-step algebra ---
template = np.array([100, 150, 200], dtype=float)
scale_factor      = 2.0
brightness_offset = 30.0
transformed = scale_factor * template + brightness_offset   # Y = aX + b

print("\n=== Step 1: Centering removes b ===")
template_centered    = template    - np.mean(template)
transformed_centered = transformed - np.mean(transformed)
print(f"Template centered:    {template_centered.astype(int)}")
print(f"Transformed centered: {transformed_centered.astype(int)}")
print(f"Ratio:                {(transformed_centered / template_centered).round(1)}")
print(f"→ After centering, transformed = {scale_factor} × template_centered (b is gone!)")

print("\n=== Step 2: Normalising removes a ===")
template_std    = np.std(template)
transformed_std = np.std(transformed)
print(f"σ(template):    {template_std:.2f}")
print(f"σ(transformed): {transformed_std:.2f}")
print(f"Ratio σ_Y/σ_X:  {transformed_std / template_std:.1f}  = a = {scale_factor}")
print(f"→ Dividing by σ cancels the scale factor a.")

template_standardized    = template_centered    / np.linalg.norm(template_centered)
transformed_standardized = transformed_centered / np.linalg.norm(transformed_centered)
print(f"\nTemplate standardized:    {template_standardized.round(4)}")
print(f"Transformed standardized: {transformed_standardized.round(4)}")
print(f"Identical? {np.allclose(template_standardized, transformed_standardized)}  → r = 1.0")

# --- Variance ↔ squared L2 norm ---
vector = np.array([100, 150, 200], dtype=float)
centered = vector - np.mean(vector)

variance          = np.var(vector)           # uses 1/n
squared_l2_norm   = np.sum(centered ** 2)
number_of_elements = len(vector)

print(f"\nVector:                 {vector.astype(int)}")
print(f"Centered:               {centered.astype(int)}")
print(f"\nVariance (1/n · Σ):     {variance:.2f}")
print(f"Squared L2 norm (Σ):    {squared_l2_norm:.2f}")
print(f"\nVariance × n:           {variance * number_of_elements:.2f}")
print(f"Squared L2 norm:        {squared_l2_norm:.2f}")
print(f"\nThey differ by a factor of n = {number_of_elements}. Same quantity, different scaling.")
print(f"\nStandard deviation σ = √Var = {np.std(vector):.2f}")
print(f"L2 norm of centered    = ‖v_c‖ = {np.linalg.norm(centered):.2f}")
print(f"σ × √n = {np.std(vector) * np.sqrt(number_of_elements):.2f}  =  ‖v_c‖  ✓")

# --- Verify against numpy corrcoef ---
template_v = np.array([100, 150, 200], dtype=float)
test_cases_verify = [
    ("Brightness +30", np.array([130, 180, 230], dtype=float)),
    ("Contrast ×2",    np.array([200, 300, 400], dtype=float)),
    ("Both (×2 + 30)", np.array([230, 330, 430], dtype=float)),
]

print("\n=== Verify: CCOEFF_NORMED vs numpy corrcoef ===")
for name, patch in test_cases_verify:
    our_r   = ccoeff_normed(patch, template_v)
    numpy_r = pearson_correlation(patch, template_v)
    print(f"{name}: our={our_r:.6f}  numpy={numpy_r:.6f}  match={np.isclose(our_r, numpy_r)}")

# ── Visualisation: bar chart comparing all three methods on all cases ───────
template = np.array([100, 150, 200], dtype=float)
test_cases_plot = [
    ("Identical",          np.array([100, 150, 200], dtype=float)),
    ("Brightness +30",     np.array([130, 180, 230], dtype=float)),
    ("Contrast ×2",        np.array([200, 300, 400], dtype=float)),
    ("Both (×2 + 30)",     np.array([230, 330, 430], dtype=float)),
    ("Different pattern",  np.array([200, 100, 180], dtype=float)),
]

names      = [t[0] for t in test_cases_plot]
ccoeff_v   = [ccoeff_normed(t[1], template) for t in test_cases_plot]
sqdiff_v   = [1.0 - ssd_normed(t[1], template) for t in test_cases_plot]  # invert for comparison

x = np.arange(len(names))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 6))
bars1 = ax.bar(x - width / 2, ccoeff_v, width, label='CCOEFF_NORMED (Pearson r)',
               color=COLORS['secondary'], alpha=0.85)
bars2 = ax.bar(x + width / 2, sqdiff_v, width, label='1 - SQDIFF_NORMED',
               color=COLORS['primary'], alpha=0.85)

ax.set_xlabel('Test Patch', fontsize=12)
ax.set_ylabel('Score (higher = more similar)', fontsize=12)
ax.set_title('CCOEFF_NORMED vs SQDIFF_NORMED: Invariance to Affine Transforms', fontsize=13)
ax.set_xticks(x)
ax.set_xticklabels(names, fontsize=10, rotation=15, ha='right')
ax.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label='Perfect match = 1')
ax.legend(fontsize=10)
ax.set_ylim(-0.1, 1.2)

plt.tight_layout()
plt.show()
