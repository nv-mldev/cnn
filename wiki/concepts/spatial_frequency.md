---
tags: [concept, frequency-domain, fundamentals, bridge-concept]
sources: ["Gonzalez & Woods — Digital Image Processing 3rd ed., Ch. 2 & Ch. 4"]
last_updated: 2026-04-14
---

# Spatial Frequency

How quickly pixel intensity changes as you move across the image.

## Why It Matters

Most people meet "frequency" first in the time domain — sound waves, heartbeats, signals per second. Cameras and images have no time axis, so the word *frequency* feels out of place. But every concept in computer vision that mentions "low-pass filter," "Nyquist," "aliasing," "Fourier," "JPEG compression," or "blur" is built on spatial frequency. Without this bridge, a huge chunk of CV is opaque.

This page translates the time-domain frequency intuition into the spatial domain — how it applies to images.

## The Bridge from Time to Space

| Time domain (audio, signals) | Spatial domain (images) |
|------------------------------|-------------------------|
| Signal is $f(t)$ — amplitude vs. time | Image is $f(x, y)$ — intensity vs. position |
| Frequency = cycles per **second** (Hz) | Frequency = cycles per **pixel** or **per image** |
| High frequency = rapid fluctuations | High frequency = rapid brightness changes (edges, textures) |
| Low frequency = slow drift | Low frequency = smooth regions, gradients |
| Sampling rate: samples per second | Sampling rate: pixels per unit length |
| Nyquist: $f_s > 2 f_{\max}$ | Same rule, applied to spatial frequency |

**The core mental swap:** replace "time" with "position on the image." Everything else carries over.

## What Does Spatial Frequency Look Like?

![[spatial_frequency_intuition.png]]

```python
import numpy as np
import matplotlib.pyplot as plt

size = 200
x = np.linspace(0, 1, size)
xx, _ = np.meshgrid(x, x)

# One cycle across the image = low frequency
low = np.sin(2 * np.pi * 1 * xx)
# Many cycles across the image = high frequency
high = np.sin(2 * np.pi * 25 * xx)
```

- **Low-frequency content:** smooth gradients, broad regions, slow lighting variation
- **High-frequency content:** sharp edges, fine textures, pixel-to-pixel noise

When you look at a photograph:
- A clear sky → mostly low-frequency
- A brick wall's mortar lines → high-frequency
- A human face → low-frequency (cheek) + high-frequency (eyelashes, hair)

## Images Are 2D — So Frequency Has a Direction

Unlike 1D audio, an image has frequency in **two directions**. A pattern can have:
- Frequency along the x-axis ($f_x$, cycles across the width)
- Frequency along the y-axis ($f_y$, cycles down the height)

![[spatial_frequency_2d_basis.png]]

```python
# 2D sinusoidal pattern with independent x and y frequencies
pattern = np.sin(2 * np.pi * (fx * xx + fy * yy))

# fx=10, fy=0  → horizontal stripes, high frequency
# fx=0,  fy=10 → vertical stripes
# fx=10, fy=10 → diagonal stripes
```

**The foundational fact:** every image — no matter how complex — can be written as a weighted sum of 2D sinusoidal patterns like the ones above. This is the 2D Fourier Transform. The coefficients tell you how much of each frequency (and direction) is present.

## Decomposing an Image by Frequency

If we split an image into "slow-changing" (low-frequency) and "fast-changing" (high-frequency) components, we get two very different pictures:

![[spatial_frequency_decomposition.png]]

```python
from scipy import ndimage

# Low-pass: Gaussian blur keeps only the slow, smooth parts
low_pass = ndimage.gaussian_filter(original, sigma=5)

# High-pass: what's left when you remove the low frequencies = edges + texture
high_pass = original - low_pass
```

- **Low-pass filter** → blur → keeps overall shape and lighting, removes fine detail
- **High-pass filter** → edges → keeps fine detail and boundaries, removes smooth regions

This decomposition is the foundation of:
- **Blur / denoising:** remove high frequencies (noise is mostly high-freq)
- **Edge detection:** remove low frequencies (edges are high-freq)
- **JPEG compression:** throw away high frequencies humans don't notice
- **Image pyramids:** represent an image at multiple frequency scales
- **Convolutional filters** in CNNs: the early layers learn local high-pass / low-pass operators

## Connecting to Things You Already Know

Now the DSP-heavy vocabulary should click:

| Concept | What it means in image-land |
|---------|----------------------------|
| [[nyquist_criterion]] | Must sample ≥ 2× the highest spatial frequency in the scene |
| [[aliasing]] | A high spatial frequency gets undersampled → shows up as a phantom low-frequency pattern (moiré) |
| [[anti_aliasing_filter]] | Optical/digital low-pass filter applied **before** sampling to kill unreproducible frequencies |
| Gaussian blur | A low-pass filter on the image |
| Sobel / Laplacian | High-pass filters — isolate edges |
| JPEG | Splits image into 8×8 blocks, transforms to frequency domain (DCT), discards small high-freq coefficients |
| Image pyramid | Successive low-pass filtering → multi-scale representation |

## The 2D Fourier Transform (Brief)

Every image $f(x, y)$ can be written as:

$$f(x, y) = \sum_{f_x} \sum_{f_y} F(f_x, f_y) \cdot e^{i 2\pi (f_x x + f_y y)}$$

where $F(f_x, f_y)$ is a complex number whose magnitude tells you **how much** of that frequency pattern is in the image, and whose phase tells you **where** it sits (shift).

Visualizing $|F(f_x, f_y)|$ shows the **frequency spectrum** — a map where the center is low frequency and the edges are high frequency. Bright spots away from the center mean strong high-frequency content in that direction.

```python
import numpy as np

# 2D FFT of an image
spectrum = np.fft.fftshift(np.fft.fft2(image))
magnitude = np.log(1 + np.abs(spectrum))  # log scale for display
# plt.imshow(magnitude, cmap="gray")
```

A deep dive into the 2D FFT is its own notebook — this page just plants the flag that **spatial frequency is real, visual, and carries over cleanly from the time-domain intuition**.

## Why CS231n Skips This

Deep learning courses tend to skip frequency analysis because CNNs *learn* their own frequency-like filters end-to-end. But understanding frequency still matters:
- Data augmentation: understanding what blur, noise, and downsampling do
- Anti-aliasing in strided convolutions (a real 2020s research topic)
- Diffusion models: the noise schedule is literally adding Gaussian noise (which is white across all frequencies)
- Image synthesis quality: GANs and diffusion models sometimes fail to match the high-frequency spectrum of real images

## Related Concepts

- [[sampling]] — the sampling rate must exceed twice the highest spatial frequency
- [[nyquist_criterion]] — the exact spatial-frequency version of the classic theorem
- [[aliasing]] — what happens when high spatial frequencies are undersampled
- [[anti_aliasing_filter]] — low-pass filtering to prevent aliasing
- [[downsampling]] — removes high spatial frequencies (whether you want it to or not)

## Sources

- Gonzalez & Woods, *Digital Image Processing*, 3rd ed., Chapter 4 (Filtering in the Frequency Domain)
- Analogy with 1D DSP concepts standard in signal processing texts
