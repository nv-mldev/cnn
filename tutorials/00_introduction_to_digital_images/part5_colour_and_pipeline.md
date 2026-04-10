# Part 5: Colour Channels and the Imaging Pipeline

## Learning Objective

Understand how a camera captures colour, what the three-channel RGB representation
means, how the full imaging pipeline works end-to-end, and what non-uniform lighting
(shading) does to pixel values.

---

## 5.1 From Grayscale to Colour

A grayscale image has one value per pixel: intensity. A colour image has **three
values per pixel** — one for each of the red, green, and blue colour channels.

```
Image shape (grayscale): (H, W)         — 2D array
Image shape (colour):    (H, W, 3)      — 3D array
```

Each channel is an independent grayscale image. The colour we perceive comes from
the relative intensities of the three channels at each pixel.

---

## 5.2 The Bayer Filter and Demosaicing

Most camera sensors are physically grayscale. Each photosite records the total number
of photons, not their wavelength. To capture colour, a **Bayer filter mosaic** is
placed over the sensor:

```
R  G  R  G  R  G
G  B  G  B  G  B
R  G  R  G  R  G
G  B  G  B  G  B
```

Each photosite records only one colour channel. The other two channels at each pixel
are **interpolated** from neighbouring photosites. This interpolation step is called
**demosaicing**.

Consequences:
- There are **2× more green photosites** than red or blue (humans are more sensitive
  to green).
- Demosaicing is itself an approximation — it can introduce colour fringing at sharp
  edges.
- The RGB values in a camera JPEG are not raw photon counts; they have been processed
  by the camera's image signal processor (ISP).

---

## 5.3 Each Channel Obeys the Same Physics

Every channel is still a spatial sample of a continuous function, and every channel
is still quantized. All the problems from Parts 1–4 apply to each channel independently:

- Shot noise affects each channel separately (Poisson per channel)
- Contrast changes apply per channel (different $a$ and $b$ per channel are possible)
- Downsampling aliases each channel independently
- White balance adjustments multiply each channel by a different scalar

---

## 5.4 Colour vs Grayscale: When Does Colour Matter?

| Situation | Colour needed? |
|-----------|---------------|
| Shape detection, edge detection | No — luminance channel is enough |
| Object classification by texture | No |
| Distinguishing red vs green objects | Yes |
| Skin tone detection | Yes |
| Industrial inspection (colour defects) | Yes |

For many computer vision tasks, converting to grayscale (luminance) loses little
relevant information and reduces data volume by 3×.

**Luminance formula (perceptual):**

$$L = 0.2126 \cdot R + 0.7152 \cdot G + 0.0722 \cdot B$$

The large coefficient on green matches the human visual system's sensitivity peak.

---

## 5.5 The Full Imaging Pipeline

Every digital image passes through this chain:

```
Scene (continuous light)
  ↓  Lens focuses light
Sensor (photosites collect photons)
  ↓  Shot noise added (Poisson)
Bayer filter (one colour per photosite)
  ↓  ADC: voltage → integer
Raw image (one channel, 12–16 bit)
  ↓  Demosaicing, white balance, tone mapping
RGB image (3 channels, 8–16 bit)
  ↓  JPEG/PNG compression
Stored image (2D array, 8-bit uint8)
```

Every arrow in this pipeline introduces an approximation or an irreversible
transformation. The pixel values in the final stored image reflect:

1. The scene content (what we want)
2. The lighting conditions
3. The sensor physics (noise, spectral response)
4. The ISP processing choices (white balance, sharpening, tone curve)
5. The compression codec

Items 2–5 are **nuisances** for pixel-level comparison. They change the pixel values
without changing the scene content.

---

## 5.6 Non-Uniform Lighting: Shading

Even when the **scene** is uniform (the same material everywhere), the **pixel values**
vary across the image if the illumination is not uniform. This is called **shading** or
**vignetting**.

The tungsten filament example from Gonzalez & Woods (Fig 0229) shows:
- A tungsten filament photographed with a sensor that has non-uniform response.
- The centre of the image is brighter than the edges — not because the filament is
  brighter there, but because the sensor responds more strongly at the centre.
- An intensity profile across the middle row of both images shows this clearly.

The mathematical model for a shaded image is:

$$I(i, j) = T(i, j) \cdot S(i, j)$$

where $T(i, j)$ is the true reflectance and $S(i, j)$ is the shading field.

**Consequence for template matching:** a template extracted from the bright centre
of a shaded image will not match the same material at the darker edges. The affine
model $I = aT + b$ only applies locally in the presence of shading — the values of
$a$ and $b$ change across the image.

---

## Summary: Why Pixel Values Are Not Scene Content

Collecting all the effects we have seen:

| Effect | Mechanism | Changes pixel values without changing scene |
|--------|-----------|---------------------------------------------|
| Shot noise | Poisson photon counting | Yes — random |
| Read noise | Electronic | Yes — random |
| Quantization | ADC rounding | Yes — deterministic |
| Contrast change | Global $a$ change | Yes |
| Brightness change | Global $b$ change | Yes |
| Shading | Spatially varying gain | Yes — position-dependent |
| White balance | Per-channel scaling | Yes |
| JPEG compression | DCT quantization | Yes |

**Next notebook:** `02_why_not_pixels.ipynb` — where we see these effects cause
pixel comparison to fail in practice, and what normalisation can do about it.
