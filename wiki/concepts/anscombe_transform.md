---
tags: [concept, signal-processing, denoising]
sources: [tutorials/01a_probability_for_cv/exercises.md]
last_updated: 2026-04-05
---

# Anscombe Transform

A variance-stabilising transform that converts [[poisson_distribution|Poisson]]-distributed data (signal-dependent noise) into approximately unit-variance Gaussian data, enabling standard Gaussian denoisers.

$$f(x) = 2\sqrt{x + 3/8}$$

## Why It Matters

Poisson noise has signal-dependent variance (σ = √λ) — brighter pixels are noisier in absolute terms. Standard denoisers (NLM, BM3D, Wiener) assume constant-variance Gaussian noise. The Anscombe transform bridges this gap: apply it, denoise with a Gaussian denoiser, then apply the inverse transform. Used in fluorescence microscopy, astronomy, and any low-light imaging.

## Key Ideas

- Input: Poisson(λ) data with variance = λ (signal-dependent)
- Output: approximately Normal with variance ≈ 1 (constant)
- Workflow: Anscombe → Gaussian denoiser → inverse Anscombe
- Works well for λ > 10; less accurate for very low counts
- Inverse: $x = (f/2)^2 - 3/8$

## Related Concepts

- [[poisson_distribution]] — the noise model this transform handles
- [[normal_distribution]] — what the output approximates
- [[noise_regimes]] — needed in the shot-noise regime
- [[shot_noise]] — the signal-dependent noise this addresses

## Sources

- [[01a_probability_for_cv|Tutorial 01a: Probability for CV]] — Exercise 2
