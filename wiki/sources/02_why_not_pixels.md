---
tags: [source, tutorial-02]
source_path: tutorials/02_why_not_pixels/
last_updated: 2026-04-09
---

# Tutorial 02: Why Not Pixels

## Summary

This tutorial demonstrates why raw pixel comparison fails for template matching and systematically derives the fixes. Starting from the physics of image formation, it builds the affine intensity model, then shows how L2 normalisation, mean subtraction, and Pearson correlation each solve one piece of the problem. The central argument: **physics → affine model → normalisation solves intensity variations → but spatial transforms (rotation, scale, occlusion) require learned features → CNNs.**

The tutorial concludes by defining the "normalisation ceiling" — the boundary between problems solvable by per-pixel normalisation and those requiring spatial features, motivating the transition to feature hierarchies and deep learning.

## Key Claims

- SSD fails under brightness changes, rotation, and scale — brightness is fixable per-pixel, spatial transforms are not
- The image formation model $f(x,y) = i(x,y) \cdot r(x,y)$ means dark pixels are ambiguous: low illumination OR low reflectance
- Under locally uniform illumination, the sensor model simplifies to the affine model $I \approx aT + b$
- L2 normalisation projects vectors onto the unit sphere, handling contrast ($a$) but failing on offset ($b$)
- Mean subtraction is an orthogonal projection that removes the DC/brightness component
- Pearson correlation = centering + normalising = OpenCV `TM_CCOEFF_NORMED`; geometric and statistical views are equivalent
- Contrast stretching is a linear transform so Pearson $r = 1.0$ with the original — no new information created
- Clipping is irreversible: once values are clamped, no normalisation can recover the lost data
- Normalisation solves all intensity problems but cannot handle rotation, scale, occlusion, or deformation
- The feature hierarchy: raw pixels → hand-designed edges → engineered descriptors (SIFT) → learned features (CNNs)

## Part-by-Part Breakdown

### Part 1: SSD Fails
- SSD(T,I) = Σ(I−T)² is the simplest matching metric
- Fails under brightness change (fixable per-pixel), rotation, and scale (not fixable per-pixel)
- Demonstrates the need for better metrics and eventually better representations

### Part 2: Physics of Image Formation
- Image formation: $f(x,y) = i(x,y) \cdot r(x,y)$ — illumination × reflectance
- Sensor model: $g = a \cdot f + b$ (gain and offset)
- Under locally uniform illumination, reduces to affine model: $I \approx aT + b$
- Links physics to the mathematical model that normalisation must handle

### Part 3: L2 Normalisation
- L2 normalisation: $\hat{v} = v / \|v\|$ projects onto unit sphere
- Handles contrast variation (multiplicative factor $a$)
- Fails on brightness offset ($b$) because adding a constant changes direction on the unit sphere

### Part 4: Mean Subtraction
- Subtracting the mean removes the DC component (brightness offset $b$)
- Geometrically: orthogonal projection away from the ones-vector
- Complementary to L2 normalisation — handles what L2 cannot

### Part 5: Pearson Correlation
- Pearson $r = \frac{\sum(I - \bar{I})(T - \bar{T})}{\sqrt{\sum(I - \bar{I})^2} \cdot \sqrt{\sum(T - \bar{T})^2}}$
- = center (remove mean) + normalise (unit length) = `TM_CCOEFF_NORMED`
- Geometric view: cosine of angle between centred vectors
- Statistical view: correlation coefficient measuring linear relationship
- Handles the full affine model: centering removes $b$, normalising removes $a$

### Part 6: Dynamic Range and Clipping
- Contrast stretching: $I' = (I - \min) / (\max - \min) \times 255$ — linear, so $r = 1.0$ with original
- Clipping is irreversible: clamped values lose information permanently
- Quantization adds additional loss at each transformation step
- Even Pearson correlation fails when clipping destroys the linear relationship

### Part 7: The Normalisation Ceiling
- Normalisation solves: brightness, contrast, affine intensity changes
- Normalisation cannot solve: rotation, scale, occlusion, non-rigid deformation
- The "ceiling" separates intensity problems from spatial problems
- Spatial problems require features that encode local structure, not just intensity
- Feature hierarchy: pixels → edges → descriptors (SIFT/HOG) → learned features (CNNs)
- CNNs learn the feature hierarchy from data, removing the need for manual design

## Concepts Introduced

### New Concepts
- [[ssd]] — Sum of Squared Differences matching metric
- [[image_formation_model]] — $f(x,y) = i(x,y) \cdot r(x,y)$
- [[pearson_correlation]] — centering + normalising, handles full affine model
- [[contrast_stretching]] — linear rescaling to full range
- [[feature_hierarchy]] — pixels → edges → descriptors → learned features
- [[normalisation_ceiling]] — boundary between intensity and spatial problems

### Concepts Deepened (from earlier tutorials)
- [[affine_model]] — now derived from physics model, not just observed
- [[dynamic_range]] — connected to contrast stretching and clipping effects on matching
- [[clipping]] — shown as irreversible information loss that defeats normalisation
- [[contrast]] — connected to contrast stretching as a linear (information-preserving) operation

## Connections to Other Sources

- **Builds on** [[00_introduction_to_digital_images|Tutorial 00]]: affine model, dynamic range, clipping from Part 3
- **Builds on** [[01a_probability_for_cv|Tutorial 01a]]: noise model explains why even same-scene pixel comparison fails
- **Builds toward** future CNN tutorials: feature learning as the solution to spatial invariance
