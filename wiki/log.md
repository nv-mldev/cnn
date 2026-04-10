---
tags: [log]
last_updated: 2026-04-10
---

# Wiki Log

## [2026-04-05] init | Wiki created
Initial wiki setup — directory structure, mkdocs config, index, and log.

## [2026-04-05] ingest | Tutorial 00: Introduction to Digital Images
Ingested all 5 parts + exercises from `tutorials/00_introduction_to_digital_images/`.
- Created 1 source summary page
- Created 27 concept pages across 6 categories: sensor physics, sampling, pixels, image formation, interpolation, colour/pipeline
- Created 1 synthesis page: "Why Pixel Values Are Unreliable"
- Key concepts: photosite, shot noise, SNR, sampling, Nyquist, aliasing, quantization, bit depth, affine model, dynamic range, Bayer filter, demosaicing, imaging pipeline
- Central argument: pixel values encode lighting + noise + processing, not just scene content → raw pixel comparison fails

## [2026-04-05] ingest | Tutorial 01a: Probability for Computer Vision
Ingested all 7 parts + exercises from `tutorials/01a_probability_for_cv/`.
- Created 1 source summary page
- Created 13 new concept pages: random variable, probability distribution, Bernoulli, Binomial, Poisson, Normal, CLT, dark current, read noise, noise budget, noise regimes, Anscombe transform, manifold hypothesis
- Updated 3 existing concept pages: shot noise (added Poisson derivation), SNR (added source), quantum efficiency (added Bernoulli model)
- Created 1 new synthesis page: "The Distribution Chain"
- Updated synthesis: "Why Pixels Fail" (added mathematical foundation from 01a)
- Key chain: Bernoulli→Binomial→Poisson→Normal→CLT; each distribution a limiting case of the previous
- Central insight: pixel noise is Gaussian by CLT, justifying all Gaussian-based CV algorithms

## [2026-04-09] ingest | Tutorial 01b: Linear Algebra for Matching
Ingested from `tutorials/01b_linear_algebra_for_matching/`.
- Created 1 source summary page
- Created 10 new concept pages: vector representation, dot product, L2 norm, unit vector, cosine similarity, orthogonality, orthogonal projection, mean subtraction, linear transform, orthogonal transform
- Updated 1 existing concept page: affine model (added vector-space decomposition into brightness and contrast)
- Key insight: mean subtraction + L2 normalisation = orthogonal decomposition isolating pure pattern from brightness and contrast

## [2026-04-09] ingest | Tutorial 02: Why Not Pixels
Ingested from `tutorials/02_why_not_pixels/`.
- Created 1 source summary page
- Created 6 new concept pages: SSD, image formation model, Pearson correlation, contrast stretching, feature hierarchy, normalisation ceiling
- Updated 4 existing concept pages: affine model, dynamic range, clipping, contrast
- Created 1 new synthesis page: "From Normalisation to Features"
- Key argument: physics → affine model → normalisation solves intensity → spatial problems require learned features → CNNs

## [2026-04-10] maintenance | Index restructured
- Reorganised index.md from flat categories to drill-down learning progression
- 8 numbered sections following: sensor physics → noise → probability → sampling → image formation → linear algebra → matching → beyond pixels
- Added all 56 concept pages, 4 source pages, 3 synthesis pages (was missing ~16 concepts, 2 sources, 1 synthesis)
- Added table format for sources with tutorial number, link, and one-line summary
