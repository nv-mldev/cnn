---
tags: [concept, colour, sensor-physics]
sources: [tutorials/00_introduction_to_digital_images/part5_colour_and_pipeline.md]
last_updated: 2026-04-05
---

# Bayer Filter

A colour filter array (CFA) placed over the sensor where each photosite is covered by a red, green, or blue filter in an RGGB pattern — 2× more green than red or blue.

## Why It Matters

Most camera sensors are physically monochrome — each [[photosite]] just counts photons. The Bayer filter makes each photosite sensitive to only one colour. This means at each pixel position, only one of three colour channels is actually measured — the other two must be interpolated by [[demosaicing]]. Colour images are partially real, partially computed.

## Key Ideas

- Pattern: RGGB — in each 2×2 block, 1 red, 2 green, 1 blue
- Green is oversampled (2×) because human vision is most sensitive to green
- Each pixel only has one real colour measurement — the other two are interpolated
- Raw images before demosaicing look like a mosaic, not a colour image
- Alternative patterns exist (X-Trans, RGBW) but Bayer is by far the most common

## Related Concepts

- [[demosaicing]] — interpolates the missing colour channels
- [[photosite]] — the element behind each filter
- [[luminance]] — green dominance in luminance formula reflects Bayer's green bias
- [[imaging_pipeline]] — Bayer to RGB is an early pipeline stage

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 5
