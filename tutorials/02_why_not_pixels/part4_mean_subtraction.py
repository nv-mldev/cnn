"""
Part 4: Fixing the Brightness Offset — Mean Subtraction
=========================================================
Proves that mean subtraction is an orthogonal decomposition: it separates a
vector into a brightness component (along [1,1,...,1]) and a pattern component
(perpendicular to [1,1,...,1]).  Demonstrates that uniform brightness offsets
vanish after mean subtraction, while non-uniform offsets do not.
"""

# --- Setup ---
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

COLORS = {
    'primary': '#2196F3',
    'secondary': '#4CAF50',
    'result': '#FFC107',
    'highlight': '#F44336',
    'transform': '#9C27B0',
    'gradient': '#FF9800',
}

# ── Algorithm ──────────────────────────────────────────────
# Step 1: Decompose a vector into mean component + residual
# Step 2: Verify residual sums to zero (for any vector, any length)
# Step 3: Prove orthogonality — dot product of residual with [1,1,1] = 0
# Step 4: Visualise the orthogonal decomposition in 3D
# Step 5: Show same-pattern vectors have identical centered forms
# Step 6: Visualise on a 2D image patch (DC + AC = original)
# Step 7: Show failure case — non-uniform offset not fully removed
# What to look for: sum(residual)=0 always; dot(residual,[1,1,1])=0 always
# ───────────────────────────────────────────────────────────

# --- Step 1: Decompose a vector ---
vector = np.array([130, 180, 230], dtype=float)
mean_value = np.mean(vector)

mean_component = mean_value * np.ones(3)       # the [1,1,1] part (brightness)
residual       = vector - mean_component        # the pattern part

print(f"Vector v:         {vector.astype(int)}")
print(f"Mean:             {mean_value:.0f}")
print(f"Mean component:   {mean_component.astype(int)}  = {mean_value:.0f} · [1,1,1]")
print(f"Residual:         {residual.astype(int)}  = v - mean·[1,1,1]")
print(f"\nReconstruct:      {(mean_component + residual).astype(int)}  ✓")

# --- Step 2: Residual always sums to zero ---
print(f"\nResidual: {residual.astype(int)}")
print(f"Sum of residual elements: {np.sum(residual):.1f}  ← always zero")

test_vectors = [
    np.array([10, 20, 30, 40, 50], dtype=float),
    np.array([255, 0, 128, 64], dtype=float),
    np.array([7.3, 2.1, 9.8], dtype=float),
]
print()
for test_vector in test_vectors:
    test_residual = test_vector - np.mean(test_vector)
    print(f"{test_vector} → residual {test_residual.round(2)} → sum = {np.sum(test_residual):.10f}")

# --- Step 3: Prove orthogonality ---
ones_vector = np.ones(3)
dot_product = np.dot(residual, ones_vector)
print(f"\nResidual:           {residual.astype(int)}")
print(f"[1,1,1]:            {ones_vector.astype(int)}")
print(f"Dot product:        ({residual[0]:.0f})(1) + ({residual[1]:.0f})(1) + ({residual[2]:.0f})(1) = {dot_product:.1f}")
print("\nThe dot product with [1,1,1] is just the sum of the elements.")
print("We proved the sum is always zero → the residual is ALWAYS orthogonal to [1,1,1].")

# --- Step 4: Visualise orthogonal decomposition in 3D ---
origin = [0, 0, 0]
scale  = 1.0 / np.linalg.norm(vector)

# Recompute for visualisation
vector_vis        = np.array([130, 180, 230], dtype=float)
mean_val_vis      = np.mean(vector_vis)
mean_comp_vis     = mean_val_vis * np.ones(3)
residual_vis      = vector_vis - mean_comp_vis

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Original vector
ax.quiver(*origin, *(vector_vis * scale), color=COLORS['primary'],
          arrow_length_ratio=0.06, linewidth=2.5, label=f'v = {vector_vis.astype(int)}')

# Mean component (along [1,1,1])
ax.quiver(*origin, *(mean_comp_vis * scale), color=COLORS['gradient'],
          arrow_length_ratio=0.08, linewidth=2.5, label=f'v∥ = {mean_val_vis:.0f}·[1,1,1] (brightness)')

# Residual (from tip of mean component to tip of original vector)
ax.quiver(*(mean_comp_vis * scale), *(residual_vis * scale), color=COLORS['secondary'],
          arrow_length_ratio=0.15, linewidth=2.5, label=f'v⊥ = {residual_vis.astype(int)} (pattern)')

# The [1,1,1] diagonal extended
diagonal_line      = np.linspace(0, 1.2, 50)
diagonal_direction = np.ones(3) / np.linalg.norm(np.ones(3))
ax.plot(diagonal_line * diagonal_direction[0],
        diagonal_line * diagonal_direction[1],
        diagonal_line * diagonal_direction[2],
        '--', color='gray', alpha=0.5, label='[1,1,1] direction')

ax.set_xlabel('Pixel 1', fontsize=11)
ax.set_ylabel('Pixel 2', fontsize=11)
ax.set_zlabel('Pixel 3', fontsize=11)
ax.set_title('Orthogonal Decomposition: v = v∥ (brightness) + v⊥ (pattern)', fontsize=13)
ax.legend(loc='upper left', fontsize=9)
plt.tight_layout()
plt.show()

# Verify orthogonality numerically
print(f"\nDot product of v∥ and v⊥: {np.dot(mean_comp_vis, residual_vis):.1f}  ← zero = orthogonal ✓")

# --- Step 5: Same pattern, different brightness — identical centered form ---
vectors_with_same_pattern = [
    np.array([100, 150, 200], dtype=float),
    np.array([130, 180, 230], dtype=float),   # +30 offset
    np.array([500, 550, 600], dtype=float),   # +400 offset
]

print("\nVector                    Mean    Centered (pattern)")
print("─" * 60)
for v in vectors_with_same_pattern:
    mean_v   = np.mean(v)
    centered = v - mean_v
    print(f"{v.astype(int)}          {mean_v:>5.0f}    {centered.astype(int)}")

print("\nAll three have the SAME centered pattern [-50, 0, 50].")
print("Brightness gone. Pattern preserved.")

# --- Step 6: 2D image patch decomposition ---

def make_gradient_patch(size: int, start: float, end: float) -> np.ndarray:
    """Create a size×size gradient patch."""
    row = np.linspace(start, end, size)
    return np.tile(row, (size, 1))

original = make_gradient_patch(size=5, start=80, end=220)
brighter = original + 60  # uniform brightness offset

fig, axes = plt.subplots(2, 3, figsize=(15, 9))

for row_idx, (patch, label) in enumerate([(original, 'Original'),
                                           (brighter, 'Brighter (+60)')]):
    mean_val   = np.mean(patch)
    brightness = np.full_like(patch, mean_val)
    pattern    = patch - brightness

    axes[row_idx, 0].imshow(np.clip(patch, 0, 255), cmap='gray', vmin=0, vmax=280)
    axes[row_idx, 0].set_title(f'{label}\nmean = {mean_val:.0f}', fontsize=12)
    axes[row_idx, 0].set_xticks([]); axes[row_idx, 0].set_yticks([])

    axes[row_idx, 1].imshow(brightness, cmap='gray', vmin=0, vmax=280)
    axes[row_idx, 1].set_title(f'DC = {mean_val:.0f}·[1,1,...,1]', fontsize=12)
    axes[row_idx, 1].set_xticks([]); axes[row_idx, 1].set_yticks([])

    axes[row_idx, 2].imshow(pattern, cmap='RdBu_r', vmin=-100, vmax=100)
    axes[row_idx, 2].set_title('AC (pattern)', fontsize=12,
                                color=COLORS['secondary'], fontweight='bold')
    axes[row_idx, 2].set_xticks([]); axes[row_idx, 2].set_yticks([])

axes[0, 0].set_ylabel('Original', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('Brighter +60', fontsize=12, fontweight='bold')

plt.suptitle('Mean Subtraction: Different DC → Same AC (Pattern)', fontsize=14, y=1.02)
plt.tight_layout()
plt.show()

pattern_original = original - np.mean(original)
pattern_brighter = brighter - np.mean(brighter)
print(f"\nPattern components identical? {np.allclose(pattern_original, pattern_brighter)} ✓")
print("The DC (mean) is different. The AC (pattern) is the SAME.")

# --- Step 7: Failure — non-uniform brightness ---
template_vector   = np.array([100, 150, 200], dtype=float)
non_uniform_offset = np.array([30, 0, 10], dtype=float)  # NOT aligned with [1,1,1]
shadowed_patch    = template_vector + non_uniform_offset

template_centered = template_vector - np.mean(template_vector)
shadowed_centered = shadowed_patch  - np.mean(shadowed_patch)

print(f"\nTemplate:         {template_vector.astype(int)}  → centered: {template_centered.round(1)}")
print(f"Shadowed (+{non_uniform_offset.astype(int)}): {shadowed_patch.astype(int)}  → centered: {shadowed_centered.round(1)}")
print(f"\nSame after centering? {np.allclose(template_centered, shadowed_centered)}")
print("Non-uniform offset is NOT fully removed by mean subtraction.")
