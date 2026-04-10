---
tags: [concept, sensor-physics, noise, critical]
sources: [tutorials/01a_probability_for_cv/part6_putting_it_together.md]
last_updated: 2026-04-05
---

# Noise Regimes

Three distinct operating regions of a sensor where different noise sources dominate, each requiring a different denoising strategy.

## Why It Matters

Applying the wrong denoising strategy wastes effort or makes things worse. In the read-noise regime, averaging frames helps; in the shot-noise regime, you need signal-dependent denoising (Anscombe + Gaussian denoiser); in saturation, information is irreversibly lost. Knowing which regime you're in tells you what to do.

## Key Ideas

| Regime | Signal Level | Dominant Noise | SNR Behaviour | Strategy |
|--------|-------------|----------------|---------------|----------|
| **Read-noise limited** | Dark pixels (λ < σ_r²) | Electronics (σ_r) | SNR ∝ signal (linear) | Average frames |
| **Shot-noise limited** | Mid-tones (σ_r² < λ < FWC) | Physics (√λ) | SNR ∝ √signal | [[anscombe_transform]] + Gaussian denoiser |
| **Saturation** | Bright pixels (λ ≥ FWC) | Well is full | SNR collapses | Information lost — adjust exposure |

**Crossover point**: shot noise exceeds read noise when $\sqrt{\lambda} > \sigma_r$, i.e., $\lambda > \sigma_r^2$. For σ_r = 4 e⁻, crossover at λ = 16 photons.

## Related Concepts

- [[noise_budget]] — the complete accounting of all noise sources
- [[shot_noise]] — dominates in the mid-tone regime
- [[read_noise]] — dominates in the dark regime
- [[clipping]] — what happens in the saturation regime
- [[full_well_capacity|Full-Well Capacity]] — defines the saturation boundary
- [[anscombe_transform]] — tool for the shot-noise regime

## Sources

- [[01a_probability_for_cv|Tutorial 01a: Probability for CV]] — Part 6
