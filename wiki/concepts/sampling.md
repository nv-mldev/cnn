---
tags: [concept, sensor-physics, fundamentals]
sources: [tutorials/00_introduction_to_digital_images/part1_sampling_and_sensors.md, "Gonzalez & Woods — Digital Image Processing 3rd ed., Ch. 2"]
last_updated: 2026-04-14
---

# Sampling

Converting a continuous signal into a discrete set of values by measuring it at regular intervals.

## Why It Matters

A camera sensor does not capture a continuous image — it measures brightness at a finite grid of photosites. This grid spacing determines what detail the image can represent. Every digital image is a sampled version of a continuous scene, and the sampling rate sets a hard limit on what information survives.

## Key Ideas

- A digital image is a **2D function sampled on a regular grid** — each sample is one pixel
- Spatial sampling (how many pixels) trades off against storage, processing cost, and detail preservation
- Sampling too coarsely loses detail permanently — no algorithm can recover it
- The minimum sampling rate to preserve a signal is defined by the [[nyquist_criterion]]
- Sampling below the Nyquist rate causes [[aliasing]] — phantom frequencies that weren't in the original scene

## Visualizations

### 1. Grid Density — Same scene, different sampling rates

A concentric circle pattern sampled at 8×8, 20×20, and 60×60 grids. The coarse grid destroys the ring structure entirely; the fine grid reproduces it faithfully.

```python
import numpy as np
import matplotlib.pyplot as plt

# Continuous signal: concentric rings
high_res = 500
x = np.linspace(-1, 1, high_res)
xx, yy = np.meshgrid(x, x)
continuous_signal = np.sin(2 * np.pi * 6 * np.sqrt(xx**2 + yy**2))

# Sample at three grid densities
for grid_size, label in [(8, "Coarse"), (20, "Medium"), (60, "Fine")]:
    sample_points = np.linspace(-1, 1, grid_size)
    sx, sy = np.meshgrid(sample_points, sample_points)
    sampled = np.sin(2 * np.pi * 6 * np.sqrt(sx**2 + sy**2))
    # Display with nearest-neighbour interpolation to show pixel blocks
    plt.imshow(sampled, cmap="gray", interpolation="nearest")
```

![[sampling_grid_density.png]]

### 2. Nyquist & Aliasing — Undersampling creates phantom patterns

A 12-cycle stripe pattern needs at least 24 samples (Nyquist criterion). Below that, a false low-frequency moiré pattern appears that doesn't exist in the scene.

```python
import numpy as np
import matplotlib.pyplot as plt

signal_frequency = 12  # cycles across the domain
nyquist_rate = 2 * signal_frequency  # 24 samples needed

# Sample at three rates: below, at, and above Nyquist
for num_samples in [10, nyquist_rate, 60]:
    sample_x = np.linspace(0, 1, num_samples)
    sx, _ = np.meshgrid(sample_x, sample_x)
    sampled = np.sin(2 * np.pi * signal_frequency * sx)
    plt.imshow(sampled, cmap="gray", interpolation="nearest")
```

![[sampling_nyquist_aliasing.png]]

### 3. Ground Sampling Distance — Pixel size determines what you can see

An industrial inspection example: the same metal plate with bolts and a scratch defect. At coarse GSD (20 mm/pixel), the scratch is sub-pixel and invisible. At fine GSD (4 mm/pixel), it spans multiple pixels and is detectable.

```python
# GSD determines the smallest detectable feature:
# - Coarse GSD (5×5 grid, 20 mm/pixel): bolts ≈ 1 pixel, scratch invisible
# - Fine GSD (25×25 grid, 4 mm/pixel): bolts ≈ 4 pixels, scratch detectable
#
# Rule of thumb for inspection:
#   minimum_pixels_on_defect = defect_size / GSD >= 2-3 pixels
```

![[sampling_gsd.png]]

### 4. The canonical Gonzalez & Woods figure

The classic textbook illustration: a continuous scene → a 1D scan line from A to B → samples taken along that line → each sample quantized to a discrete gray level. Together, sampling (horizontal axis) and quantization (vertical axis) convert the continuous image into a digital one.

![[gw_sampling_quantization_scanline.jpg]]

*Source: Gonzalez & Woods, Digital Image Processing 3rd ed., Fig. 2.16.*

### 5. Continuous image → sensor array → pixelated result

The same object projected onto a sensor grid: each cell integrates light over its area, producing one pixel value. The right panel shows the resulting pixelated image.

![[gw_continuous_to_pixels.jpg]]

*Source: Gonzalez & Woods, Fig. 2.17.*

## Related Concepts

- [[nyquist_criterion]] — the minimum sampling rate to avoid aliasing
- [[aliasing]] — what happens when you sample too slowly
- [[spatial_resolution]] — how many samples (pixels) the image has
- [[photosite]] — the physical element that performs the sampling
- [[quantization]] — the other half of digitisation (intensity discretisation)
- [[downsampling]] — reducing the number of samples after capture

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 1: From Light to Numbers
