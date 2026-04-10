---
tags: [concept, image-formation]
sources: [tutorials/02_why_not_pixels/part6_dynamic_range.md]
last_updated: 2026-04-09
---

# Contrast Stretching

Linear rescaling of pixel values to fill the full available range:

$$I' = \frac{I - I_{min}}{I_{max} - I_{min}} \times 255$$

## Why It Matters

Contrast stretching is a common preprocessing step that makes images visually clearer by spreading pixel values across the full 0-255 range. The critical insight is that it is a **linear transform** — it changes $a$ and $b$ in the affine model but creates no new information. Pearson correlation between an image and its contrast-stretched version is exactly $r = 1.0$. This means contrast stretching helps human viewers but adds nothing for a properly normalised matching algorithm.

## Key Ideas

- Pure linear operation: $I' = a \cdot I + b$ where $a = 255 / (I_{max} - I_{min})$ and $b = -I_{min} \cdot a$
- No new information created — just a change of scale
- Pearson $r = 1.0$ between original and stretched — normalisation already handles this
- Useful for visualisation and display, not for improving matching
- Can introduce [[clipping]] if applied carelessly to already-full-range images
- Different from histogram equalisation, which is non-linear and does change information content

## Code Example

```python
import numpy as np

def contrast_stretch(image: np.ndarray) -> np.ndarray:
    """Linear rescale to [0, 255]."""
    image_min = image.min()
    image_max = image.max()
    return (image - image_min) / (image_max - image_min) * 255

# Low-contrast image spanning only [80, 160]
low_contrast = np.array([80, 100, 120, 160], dtype=float)
stretched = contrast_stretch(low_contrast)  # [0, 63.75, 127.5, 255]

# Pearson r = 1.0 — no new information
r = np.corrcoef(low_contrast, stretched)[0, 1]
print(f"r = {r:.4f}")  # 1.0000
```

## Related Concepts

- [[contrast]] — what contrast stretching aims to increase
- [[dynamic_range]] — contrast stretching maps values to the full representable range
- [[affine_model]] — contrast stretching is itself an affine transform
- [[pearson_correlation]] — invariant to contrast stretching ($r = 1.0$)
- [[clipping]] — if stretching overshoots the range, clipping causes irreversible loss

## Sources

- [[02_why_not_pixels|Tutorial 02: Why Not Pixels]] — Part 6
