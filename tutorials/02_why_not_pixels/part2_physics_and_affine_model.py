"""
Part 2: Physics of Image Formation and the Affine Model
=========================================================
Simulates the physical image formation model f = i * r and the sensor model
g = a*f + b.  Demonstrates that under locally uniform illumination, the
relationship between two captures collapses to the affine model I = a*T + b.
Also shows the failure cases where the approximation breaks.
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
# 1. Define a reflectance map r(x,y) — the "true" object pattern
# 2. Apply two different illumination scalars i_T and i_I to simulate
#    two different captures (different lighting, exposure, or gain)
# 3. Show that query / template = constant (the affine collapse)
# 4. Demonstrate failure: vary illumination spatially (shadow) and
#    show the affine model no longer holds
# What to look for: uniform illumination → constant ratio;
# non-uniform illumination → varying ratio (affine breaks)
# ───────────────────────────────────────────────────────────

# Simulate a 1D reflectance profile (5 pixels, same pattern)
reflectance = np.array([0.2, 0.5, 0.8, 0.4, 0.6])   # r(x) in [0, 1]

# Two different capture conditions
illumination_template = 200.0   # i_T  (bright studio light)
illumination_query    = 120.0   # i_I  (dimmer ambient light)
gain_template         = 1.0     # a_T
gain_query            = 1.5     # a_I  (higher ISO)
bias_template         = 5.0     # b_T  (dark current)
bias_query            = 10.0    # b_I  (different ADC offset)

# Compute pixel values using the full physics model
template_pixels = gain_template * (illumination_template * reflectance) + bias_template
query_pixels    = gain_query    * (illumination_query    * reflectance) + bias_query

print("=== Physical Image Formation: g = a * (i * r) + b ===")
print(f"Reflectance r:    {reflectance}")
print(f"Template pixels:  {template_pixels.round(1)}")
print(f"Query pixels:     {query_pixels.round(1)}")

# ── Verify the affine collapse ──────────────────────────────
# Under uniform illumination, I = a*T + b analytically
alpha_T = gain_template * illumination_template
alpha_I = gain_query * illumination_query

affine_a = alpha_I / alpha_T
affine_b = bias_query - affine_a * bias_template

predicted_query = affine_a * template_pixels + affine_b

print("\n=== Affine Collapse: I = a*T + b ===")
print(f"a = alpha_I / alpha_T = {alpha_I:.1f} / {alpha_T:.1f} = {affine_a:.4f}")
print(f"b = b_I - a*b_T       = {bias_query} - {affine_a:.4f}*{bias_template} = {affine_b:.4f}")
print(f"\nPredicted query (affine): {predicted_query.round(3)}")
print(f"Actual query:             {query_pixels.round(3)}")
print(f"Max error: {np.max(np.abs(predicted_query - query_pixels)):.6f}  ← should be 0")

# ── Failure case: non-uniform illumination (shadow) ─────────
print("\n=== Failure Case: Non-Uniform Illumination (Shadow) ===")
# Illumination drops on the right half — simulating a shadow edge
illumination_nonuniform = np.array([120.0, 120.0, 120.0, 40.0, 40.0])
query_shadowed = gain_query * (illumination_nonuniform * reflectance) + bias_query

# The ratio I/T is no longer constant
ratio = query_shadowed / template_pixels
print(f"Template pixels:  {template_pixels.round(1)}")
print(f"Shadowed query:   {query_shadowed.round(1)}")
print(f"Ratio I/T:        {ratio.round(3)}  ← NOT constant (affine model breaks)")
print("A single scalar 'a' cannot capture a spatially varying illumination change.")

# ── Visualisation ───────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Left: reflectance and pixel values
x = np.arange(len(reflectance))
axes[0].plot(x, reflectance, 'o-', color=COLORS['gradient'], linewidth=2, label='Reflectance r')
axes[0].plot(x, template_pixels / template_pixels.max(), 's--',
             color=COLORS['primary'], linewidth=2, label='Template (normalised)')
axes[0].plot(x, query_pixels / query_pixels.max(), '^--',
             color=COLORS['secondary'], linewidth=2, label='Query (normalised)')
axes[0].set_title('Uniform Illumination\n(affine model holds)', fontsize=12)
axes[0].set_xlabel('Pixel index')
axes[0].set_ylabel('Value (normalised)')
axes[0].legend(fontsize=9)
axes[0].grid(True, alpha=0.3)

# Middle: ratio is constant under uniform illumination
axes[1].plot(x, query_pixels / template_pixels, 'o-',
             color=COLORS['result'], linewidth=2.5, label='I/T ratio')
axes[1].axhline(y=affine_a, color='gray', linestyle='--', alpha=0.7, label=f'Expected a={affine_a:.3f}')
axes[1].set_title('Ratio I/T Under Uniform Illumination\n(should be constant)', fontsize=12)
axes[1].set_xlabel('Pixel index')
axes[1].set_ylabel('Ratio')
axes[1].legend(fontsize=9)
axes[1].grid(True, alpha=0.3)
axes[1].set_ylim(0, 1.5)

# Right: ratio is NOT constant under shadow
axes[2].plot(x, query_shadowed / template_pixels, 'o-',
             color=COLORS['highlight'], linewidth=2.5, label='I/T ratio (shadow)')
axes[2].axhline(y=affine_a, color='gray', linestyle='--', alpha=0.7, label=f'Expected a={affine_a:.3f}')
axes[2].set_title('Ratio I/T Under Non-Uniform Illumination\n(affine breaks — ratio varies!)', fontsize=12)
axes[2].set_xlabel('Pixel index')
axes[2].set_ylabel('Ratio')
axes[2].legend(fontsize=9)
axes[2].grid(True, alpha=0.3)
axes[2].set_ylim(0, 1.5)

plt.suptitle('Physics Model: f = i·r  |  Sensor: g = a·f + b  |  Affine collapse', fontsize=13, y=1.02)
plt.tight_layout()
plt.show()

print("\nKey insight: uniform illumination → constant ratio → affine model valid.")
print("Non-uniform illumination → varying ratio → affine model invalid.")
print("This is the core assumption behind TM_CCOEFF_NORMED working in practice.")
