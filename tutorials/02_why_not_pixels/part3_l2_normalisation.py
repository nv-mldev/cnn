"""
Part 3: Fixing the Scaling Factor — L2 Normalisation
======================================================
Demonstrates that dividing by the L2 norm (unit vector) removes the
multiplicative contrast factor a in the affine model I = a*T + b.
Uses 3D vector visualisations to show the unit sphere geometry.
"""

# --- Setup ---
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers 3D projection)

COLORS = {
    'primary': '#2196F3',
    'secondary': '#4CAF50',
    'result': '#FFC107',
    'highlight': '#F44336',
    'transform': '#9C27B0',
    'gradient': '#FF9800',
}

# ── Algorithm ──────────────────────────────────────────────
# 1. Show that the L2 norm measures the "length" of a pixel vector
# 2. Divide by L2 norm → unit vector (length = 1 always)
# 3. Show that scaled versions of a patch all land on the same unit vector
# 4. Visualise: 3D vectors from origin, all pointing in the same direction
#    after scaling → land on the same point on the unit sphere
# 5. Show that offset CHANGES the direction → L2 norm alone can't fix it
# What to look for: scaled vectors = same unit vector; offset = different unit vector
# ───────────────────────────────────────────────────────────

# --- L2 norm basics ---
vector = np.array([100, 150, 200], dtype=float)
l2_norm = np.sqrt(np.sum(vector ** 2))
print(f"Vector: {vector}")
print(f"L2 norm: √(100² + 150² + 200²) = √{np.sum(vector**2):.0f} ≈ {l2_norm:.1f}")

unit_vector = vector / l2_norm
print(f"\nUnit vector: {unit_vector.round(3)}")
print(f"Length of unit vector: {np.linalg.norm(unit_vector):.1f}  (always 1)")

# --- Scaled versions map to the same unit vector ---
dim_patch    = np.array([10, 20, 30],   dtype=float)   # dark
bright_patch = np.array([100, 200, 300], dtype=float)   # 10× brighter

dim_unit    = dim_patch    / np.linalg.norm(dim_patch)
bright_unit = bright_patch / np.linalg.norm(bright_patch)

print(f"\nDim patch:       {dim_patch.astype(int)}  →  unit: {dim_unit.round(4)}")
print(f"Bright patch:    {bright_patch.astype(int)}  →  unit: {bright_unit.round(4)}")
print(f"Same unit vector? {np.allclose(dim_unit, bright_unit)}  ← should be True")

# --- Offset changes the direction ---
template_vector = np.array([100, 150, 200], dtype=float)
offset = 30
shifted_vector  = template_vector + offset

template_direction = template_vector / np.linalg.norm(template_vector)
shifted_direction  = shifted_vector  / np.linalg.norm(shifted_vector)

print(f"\nTemplate:    {template_vector.astype(int)}  → direction: {template_direction.round(3)}")
print(f"Shifted +30: {shifted_vector.astype(int)}  → direction: {shifted_direction.round(3)}")
print(f"Same direction? {np.allclose(template_direction, shifted_direction)}")
print("\nThe offset nudges the vector toward [1,1,1], changing its direction.")

# ── Visualisation 1: scaling preserves direction; offset changes it ─────
template_vec = np.array([10, 20, 30], dtype=float)
origin = [0, 0, 0]

fig = plt.figure(figsize=(14, 6))

# Left: scaling — same direction, different length
ax1 = fig.add_subplot(121, projection='3d')
for scale, color, label in [(1.0, COLORS['primary'], 'Template (1×)'),
                             (10.0, COLORS['secondary'], 'Scaled 10×'),
                             (20.0, COLORS['gradient'], 'Scaled 20×')]:
    vec = scale * template_vec
    s = 1.0 / 700
    ax1.quiver(*origin, *(vec * s), color=color,
               arrow_length_ratio=0.08, linewidth=2, label=label)

ax1.set_title('Scaling (a·T):\nSame Direction → Cosine Handles It ✓', fontsize=11)
ax1.set_xlabel('P0'); ax1.set_ylabel('P1'); ax1.set_zlabel('P2')
ax1.legend(fontsize=8)

# Right: offset — direction changes
ax2 = fig.add_subplot(122, projection='3d')
for offset_val, color, label in [(0, COLORS['primary'], 'Template'),
                                  (190, COLORS['gradient'], 'T + 190'),
                                  (990, COLORS['highlight'], 'T + 990')]:
    vec = template_vec + offset_val
    s = 1.0 / 1200
    ax2.quiver(*origin, *(vec * s), color=color,
               arrow_length_ratio=0.08, linewidth=2, label=label)

# [1,1,1] direction
diag = np.ones(3) / np.linalg.norm(np.ones(3)) * 0.9
ax2.plot([0, diag[0]], [0, diag[1]], [0, diag[2]], '--', color='gray', alpha=0.5, label='[1,1,1]')

ax2.set_title('Offset (T+b):\nDirection Changes → Cosine Fails ✗', fontsize=11)
ax2.set_xlabel('P0'); ax2.set_ylabel('P1'); ax2.set_zlabel('P2')
ax2.legend(fontsize=8)

plt.tight_layout()
plt.show()

print("Scaling: same direction, different length → L2 normalisation fixes it")
print("Offset: direction shifts toward [1,1,1] → need mean subtraction")

# ── Visualisation 2: unit sphere ────────────────────────────
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Draw the unit sphere (first octant wireframe)
phi_angles   = np.linspace(0, np.pi / 2, 30)
theta_angles = np.linspace(0, np.pi / 2, 30)
phi_grid, theta_grid = np.meshgrid(phi_angles, theta_angles)
sphere_x = np.sin(phi_grid) * np.cos(theta_grid)
sphere_y = np.sin(phi_grid) * np.sin(theta_grid)
sphere_z = np.cos(phi_grid)
ax.plot_wireframe(sphere_x, sphere_y, sphere_z, alpha=0.1, color='gray')

# Scale factor for visualisation (shrink vectors to fit)
scale = 1.0 / np.linalg.norm(bright_patch)

# Draw vectors from origin
ax.quiver(*origin, *(dim_patch    * scale), color=COLORS['primary'],
          arrow_length_ratio=0.08, linewidth=2, label=f'Dim    {dim_patch.astype(int)}')
ax.quiver(*origin, *(bright_patch * scale), color=COLORS['highlight'],
          arrow_length_ratio=0.05, linewidth=2, label=f'Bright {bright_patch.astype(int)}')

# Mark the unit vector point (same for both)
ax.scatter(*dim_unit, s=100, color=COLORS['secondary'], zorder=5,
           label=f'Unit sphere point {dim_unit.round(2)}')

ax.set_xlabel('Pixel 1', fontsize=11)
ax.set_ylabel('Pixel 2', fontsize=11)
ax.set_zlabel('Pixel 3', fontsize=11)
ax.set_title('Same Pattern, Different Brightness → Same Direction\n(Both land on same point on unit sphere)', fontsize=12)
ax.legend(loc='upper left', fontsize=9)
plt.tight_layout()
plt.show()
