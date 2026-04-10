---
tags: [source, tutorial-01a]
source_path: tutorials/01a_probability_for_cv/
last_updated: 2026-04-05
---

# Tutorial 01a: Probability for Computer Vision

## Summary

This tutorial builds the complete mathematical ladder from random processes to the Central Limit Theorem, grounded in sensor physics and CV applications. It traces the chain **Bernoulli → Binomial → Poisson → Normal → CLT**, showing that each distribution is a limiting case of the previous one. The culmination is the complete image noise model: multiple independent noise sources (Poisson shot, Poisson dark current, Gaussian read noise, Uniform quantization) sum to approximately Gaussian by CLT — explaining why Gaussian assumptions work in CV algorithms like denoising, background subtraction, and feature extraction.

The tutorial takes the empirical observations from Tutorial 00 (sensors are noisy, noise depends on brightness) and derives the exact mathematical models that explain them.

## Key Claims

- Shot noise is **exactly** Poisson — not an approximation, but the physically correct model for photon counting
- Poisson's key property: mean = variance = λ, which gives σ = √λ (signal-dependent noise)
- Poisson(λ) → Normal(λ, λ) for λ > 30 — practical threshold for Gaussian approximation
- CLT: sum of **any** independent random variables → Gaussian, regardless of individual distributions
- A pixel value is a sum of multiple noise sources with different distributions → Gaussian by CLT
- Three noise regimes exist: read-limited (dark), shot-limited (mid-tones), saturated (bright)
- The manifold hypothesis: natural images occupy a thin curved surface in high-dimensional pixel space

## Concepts Introduced

### New Concepts
- [[random_variable]]
- [[probability_distribution]]
- [[bernoulli_distribution]]
- [[binomial_distribution]]
- [[poisson_distribution]]
- [[normal_distribution]]
- [[central_limit_theorem]]
- [[dark_current]]
- [[read_noise]]
- [[noise_budget]]
- [[noise_regimes]]
- [[anscombe_transform]]
- [[manifold_hypothesis]]

### Concepts Deepened (from Tutorial 00)
- [[shot_noise]] — now derived as exact Poisson model, not just observed
- [[signal_to_noise_ratio|Signal-to-Noise Ratio]] — derived from Poisson: SNR = √λ
- [[quantum_efficiency]] — formalised as Bernoulli probability

## Connections to Other Sources

- **Builds on** [[00_introduction_to_digital_images|Tutorial 00]]: takes empirical sensor observations and derives the exact mathematical models
- **Builds toward** [[02_why_not_pixels|Tutorial 02]]: noise model explains why pixel comparison fails even for the same scene
- **Builds toward** [[01b_linear_algebra_for_matching|Tutorial 01b]]: normalisation needs to handle signal-dependent noise
