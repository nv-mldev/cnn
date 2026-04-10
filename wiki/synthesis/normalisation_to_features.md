---
tags: [synthesis, critical]
sources: [tutorials/02_why_not_pixels/, tutorials/00_introduction_to_digital_images/, tutorials/01a_probability_for_cv/]
last_updated: 2026-04-09
---

# From Normalisation to Features — The Complete Progression

Tutorial 02 completes the argument that began in Tutorial 00: raw pixels are unreliable, normalisation fixes the intensity problem, but spatial problems require a fundamentally different approach — learned features.

## The Full Chain

1. **Physics** — Image formation is multiplicative: $f(x,y) = i(x,y) \cdot r(x,y)$
2. **Sensor** — Adds gain and offset: $g = a \cdot f + b$
3. **Affine model** — Under locally uniform illumination: $I \approx aT + b$
4. **Normalisation** — Centering removes $b$, normalising removes $a$ → [[pearson_correlation]]
5. **Ceiling** — All intensity problems solved; spatial problems untouched
6. **Features** — Edges → descriptors (SIFT) → learned features (CNNs)
7. **Deep learning** — CNNs learn the entire [[feature_hierarchy]] from data

## Problem Classification

### Intensity Problems (above the normalisation ceiling)

These are per-pixel, affect all pixels similarly, and are fully handled by normalisation.

| Problem | Cause | Fix | Method |
|---------|-------|-----|--------|
| Brightness change | Different $b$ | Mean subtraction | Remove DC component |
| Contrast change | Different $a$ | L2 normalisation | Project to unit sphere |
| Full affine | Different $a$ and $b$ | Pearson correlation | Center + normalise |
| Contrast stretching | Linear rescaling | Already handled | $r = 1.0$ with original |

### Spatial Problems (below the normalisation ceiling)

These change pixel positions or visibility — no per-pixel operation can fix them.

| Problem | Why Per-Pixel Fails | Required Solution |
|---------|--------------------|-------------------|
| Rotation | Pixel positions change | Rotation-invariant features (SIFT) |
| Scale | Template size changes | Multi-scale detection |
| Occlusion | Part of object hidden | Part-based models |
| Deformation | Non-rigid spatial warping | Deformable models / CNNs |
| Viewpoint | 3D projection changes | 3D-aware features or massive augmentation |

### Destructive Problems (move from above to below the ceiling)

| Problem | Mechanism | Consequence |
|---------|-----------|-------------|
| [[clipping]] | Values clamped to 0 or 255 | Linear relationship destroyed → Pearson fails |
| Heavy quantization | Precision lost | Distinct values collapse → correlation degrades |

## The Normalisation Ceiling

The [[normalisation_ceiling]] is the sharp boundary:

- **Above**: intensity problems — solvable by [[pearson_correlation]], which handles $I = aT + b$ exactly
- **Below**: spatial problems — require representations that encode structure, not just intensity
- **Edge case**: [[clipping]] pushes intensity problems below the ceiling by destroying the affine relationship

## The Feature Hierarchy as the Solution

The [[feature_hierarchy]] shows how the field progressed:

| Era | Representation | Handles |
|-----|---------------|---------|
| Pre-2000s | Raw pixels + normalisation | Intensity only |
| 2000s | SIFT, HOG, SURF | Rotation, scale (hand-designed) |
| 2012+ | CNNs | Everything (learned from data) |

Each level is strictly more powerful — but the jump from hand-designed to learned features is qualitative. Instead of spending years designing one descriptor, you define an architecture and let gradient descent find the features.

## Why This Matters for CS231n

This progression is the missing foundation that CS231n assumes:
- CS231n starts with "why not compare pixels?" and moves quickly to CNNs
- This tutorial series provides the **detailed why**: physics → affine model → normalisation → ceiling → features
- Understanding the ceiling means understanding exactly what problem CNNs solve and why simpler methods are insufficient

## Connections

- [[why_pixels_fail]] — the error stack that motivates normalisation
- [[00_introduction_to_digital_images|Tutorial 00]] — empirical observation of pixel unreliability
- [[01a_probability_for_cv|Tutorial 01a]] — noise model adds another reason pixels fail
- [[02_why_not_pixels|Tutorial 02]] — the complete normalisation → features argument
