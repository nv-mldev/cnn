---
tags: [concept, sensor-physics, artefacts]
sources: [tutorials/00_introduction_to_digital_images/part3_contrast_and_dynamic_range.md, tutorials/02_why_not_pixels/part6_dynamic_range.md]
last_updated: 2026-04-09
---

# Clipping

When pixel values exceed the sensor's measurable range (0 or 255 for 8-bit), they are clamped to the limit. The actual brightness information in clipped regions is lost permanently.

## Why It Matters

Clipping is irreversible information loss. Overexposed highlights become flat white (255); underexposed shadows become flat black (0). No post-processing can recover what was there — the data simply doesn't exist. In high-dynamic-range scenes, clipping is unavoidable with a single exposure, which is why HDR techniques merge multiple exposures.

## Key Ideas

- Overexposure: bright regions clip to maximum → all detail lost in highlights
- Underexposure: dark regions clip to zero → all detail lost in shadows
- In a high-DR scene (e.g., 0–4000 range), no single 8-bit exposure captures everything
- Clipped pixels all have the same value → you can't distinguish between different bright objects
- Prevention: use higher [[dynamic_range]] sensors or HDR techniques
- **Irreversibility defeats normalisation**: clipping destroys the linear affine relationship between images, so even [[pearson_correlation]] fails — clipped regions all map to the same value, collapsing distinct brightnesses

## Related Concepts

- [[dynamic_range]] — clipping occurs at its limits
- [[full_well_capacity|Full-Well Capacity]] — physical cause of highlight clipping
- [[affine_model]] — affine transforms can push values into clipping range
- [[pearson_correlation]] — fails when clipping breaks the linear relationship
- [[normalisation_ceiling]] — clipping can push intensity problems below the ceiling
- [[contrast_stretching]] — careless stretching can introduce clipping

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 3
- [[02_why_not_pixels|Tutorial 02: Why Not Pixels]] — Part 6 (irreversibility and its effect on normalisation)
