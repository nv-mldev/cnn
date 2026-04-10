"""
Part 1: From Light to Numbers — Sampling and Sensors

Demonstrates how a camera converts a continuous scene into a discrete grid of numbers.
Covers the 1D sampling analogy, sensor physics (photosite size, well capacity, shot noise),
and the SNR difference between phone and DSLR sensors.

Run: python part1_sampling_and_sensors.py
"""

# --- Setup ---
import numpy as np
import matplotlib.pyplot as plt

COLORS = {
    'primary':   '#2196F3',
    'secondary': '#4CAF50',
    'result':    '#FFC107',
    'highlight': '#F44336',
    'transform': '#9C27B0',
    'gradient':  '#FF9800',
}

np.random.seed(42)
print("Part 1: Sampling and Sensors")
print("=" * 40)


# ── Algorithm ──────────────────────────────────────────────
# 1D sampling analogy
# 1. Create a high-resolution continuous sine wave (ground truth scene)
# 2. Draw samples at several sampling rates (high, medium, low)
# 3. Reconstruct by connecting samples and compare to original
# What to look for: at low sampling rates the reconstructed shape diverges
#   from the original — this is aliasing. The Nyquist rate (2 samples per
#   period) is the minimum for lossless reconstruction.
# ───────────────────────────────────────────────────────────

# Ground truth: continuous 1 Hz sine wave sampled at 1000 points
num_continuous_points = 1000
t_continuous = np.linspace(0, 1, num_continuous_points)   # 1 second
signal_frequency = 3                                        # 3 cycles per second
y_continuous = np.sin(2 * np.pi * signal_frequency * t_continuous)

# Three sampling rates to compare
sampling_rates = {
    'High (30 samples)':    30,
    'Medium (8 samples)':   8,
    'Low (5 samples)':      5,   # below Nyquist for a 3 Hz signal (need >= 6)
}

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
fig.suptitle('1D Sampling Analogy: Same Scene, Different Sample Rates', fontsize=13)

for ax, (label, num_samples) in zip(axes, sampling_rates.items()):
    t_sampled = np.linspace(0, 1, num_samples)
    y_sampled = np.sin(2 * np.pi * signal_frequency * t_sampled)

    ax.plot(t_continuous, y_continuous, color=COLORS['primary'],
            linewidth=1.5, label='True signal', alpha=0.5)
    ax.plot(t_sampled, y_sampled, 'o-', color=COLORS['highlight'],
            linewidth=2, markersize=6, label=f'{num_samples} samples')
    ax.set_title(label, fontsize=11)
    ax.set_xlabel('Time', fontsize=10)
    ax.set_ylabel('Amplitude', fontsize=10)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-1.4, 1.4)

plt.tight_layout()
plt.show()

print(f"Signal frequency: {signal_frequency} Hz")
print(f"Nyquist rate: {2 * signal_frequency} samples/second minimum")
print(f"Low-rate test: 5 samples — below Nyquist. Reconstruction is wrong.")
print()


# ── Algorithm ──────────────────────────────────────────────
# Sensor physics: photosite size and photon counting
# 1. Define sensor parameters for a phone and DSLR
# 2. Compute expected electron signal for a range of scene brightness values
# 3. Add Poisson shot noise (variance = mean signal) and read noise
# 4. Compute SNR = signal / total_noise for each brightness level
# 5. Plot SNR vs scene brightness for both sensors
# What to look for: DSLR SNR is consistently higher because each photosite
#   collects more photons. The gap is largest in dim light.
# ───────────────────────────────────────────────────────────

# Sensor parameters (simplified model)
sensor_params = {
    'Phone sensor\n(small photosite ~1 µm²)': {
        'photosite_area_um2':  1.0,    # µm²
        'full_well_capacity':  1000,   # electrons
        'read_noise_electrons': 3.0,   # e⁻ RMS
        'quantum_efficiency':  0.5,    # fraction of photons → electrons
        'color': COLORS['highlight'],
    },
    'DSLR sensor\n(large photosite ~25 µm²)': {
        'photosite_area_um2':  25.0,
        'full_well_capacity':  50000,
        'read_noise_electrons': 5.0,
        'quantum_efficiency':  0.7,
        'color': COLORS['primary'],
    },
}

# Scene brightness: photon flux in photons per µm² per second
# Range: 1 (very dim) to 10,000 (bright sunlight)
photon_flux_range = np.logspace(0, 4, 200)   # photons / µm²

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for sensor_name, params in sensor_params.items():
    # Electrons collected = photons × area × QE
    mean_signal_electrons = (
        photon_flux_range
        * params['photosite_area_um2']
        * params['quantum_efficiency']
    )
    # Clip to full-well capacity (saturation)
    mean_signal_electrons = np.clip(mean_signal_electrons, 0, params['full_well_capacity'])

    # Total noise: shot noise (Poisson: σ = √signal) + read noise in quadrature
    shot_noise = np.sqrt(mean_signal_electrons)
    total_noise = np.sqrt(shot_noise**2 + params['read_noise_electrons']**2)

    # SNR
    snr = mean_signal_electrons / total_noise

    axes[0].plot(photon_flux_range, snr,
                 label=sensor_name, color=params['color'], linewidth=2)
    axes[1].plot(photon_flux_range, mean_signal_electrons,
                 label=sensor_name, color=params['color'], linewidth=2)

axes[0].set_xscale('log')
axes[0].set_yscale('log')
axes[0].set_xlabel('Scene brightness (photons / µm²)', fontsize=11)
axes[0].set_ylabel('Signal-to-Noise Ratio (SNR)', fontsize=11)
axes[0].set_title('SNR vs Scene Brightness\n(DSLR wins in dim light)', fontsize=12)
axes[0].legend(fontsize=9)
axes[0].grid(True, alpha=0.3, which='both')

axes[1].set_xscale('log')
axes[1].set_yscale('log')
axes[1].set_xlabel('Scene brightness (photons / µm²)', fontsize=11)
axes[1].set_ylabel('Mean signal (electrons)', fontsize=11)
axes[1].set_title('Electron Signal vs Scene Brightness\n(DSLR collects ~25× more photons)', fontsize=12)
axes[1].legend(fontsize=9)
axes[1].grid(True, alpha=0.3, which='both')

plt.suptitle('Phone vs DSLR: Same Scene → Different Pixel Statistics', fontsize=13, y=1.02)
plt.tight_layout()
plt.show()

# Print summary statistics at two brightness levels
print("Sensor comparison at dim scene (100 photons/µm²):")
for sensor_name, params in sensor_params.items():
    signal = 100 * params['photosite_area_um2'] * params['quantum_efficiency']
    noise = np.sqrt(signal + params['read_noise_electrons']**2)
    print(f"  {sensor_name.splitlines()[0]}: signal={signal:.0f} e⁻, "
          f"noise={noise:.1f} e⁻, SNR={signal/noise:.1f}")
print()


# ── Algorithm ──────────────────────────────────────────────
# Shot noise visualisation: simulate photon counting across a flat scene
# 1. Define a uniform scene (constant photon flux at every pixel)
# 2. Simulate N pixels each independently sampling from Poisson(λ)
# 3. Show the resulting image — it should look uniform but noisy
# 4. Plot the pixel value histogram and overlay the Poisson PMF
# What to look for: even a perfectly flat scene produces non-uniform pixel
#   values. The spread (σ = √λ) is fundamental — not an instrument defect.
# ───────────────────────────────────────────────────────────

image_height = 128
image_width  = 128

# Two exposure levels: bright vs dim
for label, mean_photons in [('Bright scene (λ=200)', 200), ('Dim scene (λ=20)', 20)]:
    flat_scene = np.random.poisson(mean_photons, size=(image_height, image_width))

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    fig.suptitle(f'Shot Noise Simulation — {label}', fontsize=12)

    axes[0].imshow(flat_scene, cmap='gray',
                   vmin=mean_photons * 0.5, vmax=mean_photons * 1.5)
    axes[0].set_title('Simulated sensor output\n(uniform scene, Poisson noise)', fontsize=11)
    axes[0].axis('off')

    axes[1].hist(flat_scene.ravel(), bins=40, color=COLORS['primary'],
                 edgecolor='white', linewidth=0.5, density=True)
    axes[1].axvline(mean_photons, color=COLORS['highlight'], linewidth=2,
                    linestyle='--', label=f'True mean λ={mean_photons}')
    axes[1].axvline(flat_scene.mean(), color=COLORS['secondary'], linewidth=2,
                    linestyle=':', label=f'Sample mean={flat_scene.mean():.1f}')
    axes[1].set_xlabel('Pixel value (electrons)', fontsize=11)
    axes[1].set_ylabel('Frequency', fontsize=11)
    axes[1].set_title(f'Histogram  σ={flat_scene.std():.1f}  '
                      f'(theory: √λ={np.sqrt(mean_photons):.1f})', fontsize=11)
    axes[1].legend(fontsize=9)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
    print(f"{label}: mean={flat_scene.mean():.1f}, "
          f"std={flat_scene.std():.1f}, SNR={flat_scene.mean()/flat_scene.std():.1f}")

print()
print("Key takeaway: SNR = mean / std ≈ √λ")
print("Double the photons → SNR improves by √2 ≈ 41%")
