---
tags: [concept, sensor-physics, noise]
sources: [tutorials/00_introduction_to_digital_images/part1_sampling_and_sensors.md, tutorials/01a_probability_for_cv/part3_poisson.md]
last_updated: 2026-04-05
---

# Shot Noise

Random variation in the number of photons arriving at a photosite during exposure, following a Poisson distribution with standard deviation $\sigma = \sqrt{S}$ where $S$ is the mean signal.

## Why It Matters

Shot noise is the fundamental physical limit on image quality. Even a perfect sensor with zero electronic noise would still produce noisy images because photon arrivals are inherently random. A flat, uniformly lit surface does not produce uniform pixel values — each pixel fluctuates around the mean. This means pixel values are always approximations, never exact measurements of scene brightness.

## Key Ideas

- Follows Poisson distribution: if mean signal is $S$ photons, the std deviation is $\sqrt{S}$
- **Signal-dependent**: brighter areas have more absolute noise but better SNR
- At high signal: $SNR \approx \sqrt{S}$ — doubling SNR requires 4× more photons
- Cannot be eliminated by better electronics — it's a property of light itself
- Dominant noise source in well-lit scenes; [[signal_to_noise_ratio|Read Noise]] dominates in dim scenes

## Code Example

```python
import numpy as np

# Simulate shot noise on a uniform scene
mean_photons = 100  # uniform illumination
sensor_row = np.random.poisson(lam=mean_photons, size=200)

# Expected: mean ≈ 100, std ≈ √100 = 10
print(f"Mean: {sensor_row.mean():.1f}, Std: {sensor_row.std():.1f}")
```

## Mathematical Model

Shot noise is **exactly** [[poisson_distribution|Poisson]] — not an approximation. An LED emits ~10¹⁸ photons/second (huge n), probability any specific photon hits a 6µm photosite is ~10⁻¹⁸ (tiny p), but λ = np = tens to thousands. This IS the Poisson regime by definition.

- $SNR = \lambda / \sqrt{\lambda} = \sqrt{\lambda}$
- Dark pixels (λ=5): σ ≈ 2.2, relative noise 45%
- Bright pixels (λ=200): σ ≈ 14.1, relative noise 7%
- For λ > 30: well-approximated by [[normal_distribution|Normal]](λ, λ)

## Related Concepts

- [[poisson_distribution]] — the exact statistical model for shot noise
- [[signal_to_noise_ratio|Signal-to-Noise Ratio]] — quantifies the impact of shot noise
- [[photosite]] — the element where shot noise originates
- [[pixel]] — the value that inherits shot noise after ADC conversion
- [[quantum_efficiency]] — affects how many photons contribute to the signal
- [[dark_current]] — the other Poisson noise source
- [[read_noise]] — electronic noise (constant, unlike shot noise)
- [[noise_budget]] — shot noise is the dominant term at typical signal levels
- [[noise_regimes]] — shot noise dominates the mid-tone regime
- [[anscombe_transform]] — stabilises signal-dependent variance for denoising

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 1 (empirical observation)
- [[01a_probability_for_cv|Tutorial 01a: Probability for CV]] — Part 3 (exact Poisson derivation)
