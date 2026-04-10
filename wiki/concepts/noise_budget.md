---
tags: [concept, sensor-physics, noise, critical]
sources: [tutorials/01a_probability_for_cv/part6_putting_it_together.md]
last_updated: 2026-04-05
---

# Noise Budget

The complete accounting of all noise sources in a sensor measurement, their distributions, and their combined effect.

## Why It Matters

Understanding the noise budget tells you **where** the noise comes from and **which source dominates** at different signal levels. This determines denoising strategy — you can't fix what you don't understand. By [[central_limit_theorem|CLT]], the sum of all sources is approximately Gaussian, which is why Gaussian denoising algorithms work.

## Key Ideas

**The four noise sources:**

| Source | Distribution | Parameters | Signal-dependent? |
|--------|-------------|------------|-------------------|
| [[shot_noise]] | Poisson(λ) | λ = expected photons | Yes — σ = √λ |
| [[dark_current]] | Poisson(λ_d) | λ_d = dark electrons | No (constant for given T, t) |
| [[read_noise]] | Normal(0, σ_r²) | σ_r ≈ 1–5 e⁻ | No (constant) |
| Quantization | Uniform(−Δ/2, Δ/2) | Δ = full_well / 2^bits | No (constant) |

**Total signal:**

$$\mu = \lambda + \lambda_d$$
$$\sigma^2 = \lambda + \lambda_d + \sigma_r^2 + \frac{\Delta^2}{12}$$

By CLT → approximately $\mathcal{N}(\mu, \sigma^2)$

**The complete signal chain:**

1. Photon arrival → Poisson(λ)
2. Quantum efficiency → Binomial(n_photons, QE)
3. Dark current → + Poisson(λ_d)
4. Saturation → clip to [0, full_well_capacity]
5. Read noise → + Normal(0, σ_r²)
6. ADC → quantize to [0, 2^bits] integers

## Related Concepts

- [[noise_regimes]] — which budget term dominates at each signal level
- [[shot_noise]], [[dark_current]], [[read_noise]] — the three main sources
- [[central_limit_theorem]] — justifies Gaussian approximation of total
- [[signal_to_noise_ratio|Signal-to-Noise Ratio]] — computed from the budget

## Sources

- [[01a_probability_for_cv|Tutorial 01a: Probability for CV]] — Part 6
