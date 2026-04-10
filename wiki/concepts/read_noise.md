---
tags: [concept, sensor-physics, noise]
sources: [tutorials/01a_probability_for_cv/part6_putting_it_together.md]
last_updated: 2026-04-05
---

# Read Noise

Electronic noise added during the amplification and analog-to-digital conversion of the signal, following a [[normal_distribution|Normal]] distribution $\mathcal{N}(0, \sigma_r^2)$.

## Why It Matters

Read noise is the sensor's electronic noise floor — it exists even for zero-photon measurements. Unlike [[shot_noise]] (which grows with signal), read noise is constant. It dominates in dark regions where photon counts are low, defining the [[noise_regimes|read-noise-limited regime]]. Modern sensors have read noise of 1–5 electrons.

## Key Ideas

- Distribution: $\mathcal{N}(0, \sigma_r^2)$ — inherently Gaussian (electronics)
- Typical values: phone ~3 e⁻, DSLR ~5 e⁻, scientific cameras ~1 e⁻
- **Constant** — does not depend on signal level (unlike shot noise)
- Dominates in dark pixels where $\lambda < \sigma_r^2$
- Can be reduced by averaging frames: $\sigma_{r,avg} = \sigma_r / \sqrt{n}$

## Related Concepts

- [[shot_noise]] — signal-dependent noise (the other main source)
- [[dark_current]] — another noise source (thermal)
- [[noise_budget]] — read noise is one of four terms
- [[noise_regimes]] — read noise dominates in the dark regime
- [[normal_distribution]] — read noise is inherently Gaussian

## Sources

- [[01a_probability_for_cv|Tutorial 01a: Probability for CV]] — Part 6
