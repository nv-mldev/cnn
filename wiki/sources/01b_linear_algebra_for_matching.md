---
tags: [source, tutorial-01b]
source_path: tutorials/01b_linear_algebra_for_matching/
last_updated: 2026-04-09
---

# Tutorial 01b: Linear Algebra for Matching

## Summary

This tutorial develops the linear algebra foundations needed for normalised template matching, grounded in the image matching problem. It starts by showing that flattening image patches into vectors unlocks the entire linear algebra toolkit, then builds through dot products, norms, cosine similarity, orthogonality, and orthogonal transforms. The central argument: **normalised template matching works because mean subtraction + L2 normalisation = orthogonal decomposition into brightness and pattern components**. Mean subtraction is revealed to be projection onto the $[1,1,\ldots,1]$ direction (removing brightness), and L2 normalisation removes contrast — together they isolate the pure pattern for comparison.

The tutorial connects the affine imaging model $I = aT + b$ from Tutorial 00 to the vector space framework, showing that brightness offset ($b$) shifts vectors along the $[1,1,\ldots,1]$ direction while contrast ($a$) scales vector magnitude. Orthogonal transforms (DFT, DCT, Hadamard) are introduced as energy-preserving rotations, with Parseval's theorem guaranteeing that distances in the transform domain equal distances in pixel space.

## Key Claims

- A $3 \times 3$ image patch is a point in 9-dimensional space — all linear algebra operations apply directly
- Dot product measures pixel-by-pixel agreement but is magnitude-dependent (conflates brightness with pattern)
- Cosine similarity handles contrast scaling ($a$) but fails on brightness offset ($b$)
- Mean subtraction IS orthogonal projection: projecting out the $[1,1,\ldots,1]/\sqrt{n}$ component removes brightness offset entirely
- The residual after mean subtraction is orthogonal to the brightness direction — no brightness offset can affect pattern comparison
- Mean subtraction + L2 normalisation = full normalisation against affine changes
- Orthogonal transforms satisfy $Q^TQ = I$ and preserve vector norms: $\|Qx\| = \|x\|$ (Parseval's theorem)
- DFT, DCT, and Hadamard are orthogonal transforms — distances computed in transform domain equal pixel-space distances

## Concepts Introduced

### New Concepts
- [[vector_representation]]
- [[dot_product]]
- [[l2_norm]]
- [[unit_vector]]
- [[cosine_similarity]]
- [[orthogonality]]
- [[orthogonal_projection]]
- [[mean_subtraction]]
- [[linear_transform]]
- [[orthogonal_transform]]

### Concepts Deepened (from Tutorial 00)
- [[affine_model]] — now decomposed into brightness ($b$ along $[1,\ldots,1]$) and contrast ($a$ as magnitude scaling) in vector space

## Connections to Other Sources

- **Builds on** [[00_introduction_to_digital_images|Tutorial 00]]: takes the affine model and pixel comparison failure, provides the mathematical fix
- **Builds on** [[01a_probability_for_cv|Tutorial 01a]]: noise model motivates why normalisation alone isn't enough — noise corrupts pattern too
- **Builds toward** [[02_why_not_pixels|Tutorial 02]]: normalised matching handles affine changes but still fails on geometric/structural changes — motivating learned features
