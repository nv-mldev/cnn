---
tags: [synthesis, critical]
sources: [tutorials/00_introduction_to_digital_images/, tutorials/01a_probability_for_cv/]
last_updated: 2026-04-05
---

# Why Pixel Values Are Unreliable — The Cumulative Argument

Tutorial 00 builds a systematic case across five parts that raw pixel comparison is fundamentally flawed. Each part adds another source of error between scene content and pixel value.

## The Error Stack

| Part | Error Source | Type | Reversible? |
|------|-------------|------|-------------|
| 1 | [[shot_noise]] | Random (Poisson, σ=√S) | No — fundamental physics |
| 2 | [[quantization]] | Deterministic (±Δ/2) | No — precision lost |
| 3 | [[affine_model]] | Systematic (a, b change with lighting) | Correctable if a, b are known |
| 4 | [[aliasing]] / [[downsampling]] | Irreversible frequency corruption | No — information destroyed |
| 5 | [[imaging_pipeline]] + [[shading]] | Multiple non-linear stages | Partially, with calibration |

## The Key Insight

A pixel value encodes **at least six things** simultaneously:
1. Scene content (what you want)
2. Lighting conditions (affine parameters a, b)
3. Sensor physics (noise, spectral response, QE)
4. Spatial position (shading/vignetting)
5. ISP processing (white balance, tone mapping, sharpening)
6. Compression codec (JPEG quantization)

Any algorithm that compares pixel values directly (SSD, SAD, MAE) treats all six as if they were one signal. This is why pixel matching fails across different cameras, lighting conditions, or even different positions in the same image.

## What Comes Next

- **Tutorial 01a** (Probability): Formalises the noise model — why sensor noise is Gaussian (CLT), noise budgets
- **Tutorial 01b** (Linear Algebra): The math behind normalisation — how to undo the affine transformation
- **Tutorial 02** (Why Not Pixels): Puts it all together — demonstrates pixel matching failure and introduces normalisation as the fix

## The Mathematical Foundation (Tutorial 01a)

Tutorial 01a provides the **exact mathematical models** for the noise observed in Tutorial 00:

- [[shot_noise]] is exactly [[poisson_distribution|Poisson]](λ) — derived from the Bernoulli→Binomial→Poisson chain
- σ = √λ (signal-dependent noise) explains why dark regions are relatively noisier
- Multiple noise sources (Poisson + Poisson + Gaussian + Uniform) sum to Gaussian by [[central_limit_theorem|CLT]]
- This justifies why denoising algorithms (NLM, BM3D, Wiener) assume Gaussian noise
- The [[manifold_hypothesis]] provides the deeper reason: pixel distance ≠ semantic distance

The [[noise_budget]] quantifies all sources; the [[noise_regimes]] tell you which dominates and what strategy to use.

## The Path to Features

The logical chain:
1. Pixels are unreliable (Tutorial 00) →
2. The noise is mathematically characterised (Tutorial 01a) →
3. Normalisation partially fixes the affine problem (Tutorials 01b, 02) →
4. But normalisation has limits (Tutorial 02) →
5. We need **learned features** that are invariant to these transformations →
6. Natural images lie on a low-dimensional manifold — features map to that manifold →
7. CNNs learn such features (future tutorials, CS231n territory)
