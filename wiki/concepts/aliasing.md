---
tags: [concept, signal-processing, artefacts]
sources: [tutorials/00_introduction_to_digital_images/part4_zoom_and_aliasing.md]
last_updated: 2026-04-05
---

# Aliasing

When a signal is sampled below the Nyquist rate, high-frequency components fold back and appear as phantom lower-frequency patterns that weren't in the original scene.

## Why It Matters

Aliasing is one of the most common artefacts in digital imaging. It appears as moiré patterns on fine textures (brick walls, fabric weaves), jagged edges on diagonal lines, and colour fringing on Bayer sensor images. Once aliased, the phantom frequencies are indistinguishable from real content — the information is corrupted, not just missing.

## Key Ideas

- Occurs when $f_{signal} > f_{Nyquist} = f_s / 2$
- High frequencies "fold back" below Nyquist — they don't disappear, they become wrong frequencies
- In images: moiré patterns, jagged diagonals, phantom stripes
- A checkerboard at 1 pixel/square (exactly Nyquist) is the canonical test case — downsampling 2× produces a completely wrong pattern
- **Irreversible** — once aliased, you cannot separate real from phantom frequencies
- Prevention: apply an [[anti_aliasing_filter|Anti-Aliasing Filter]] before downsampling

## Code Example

```python
import numpy as np
from PIL import Image

# Checkerboard at Nyquist frequency (1 px per square)
checker = np.zeros((128, 128), dtype=np.uint8)
checker[::2, ::2] = 255
checker[1::2, 1::2] = 255

# Raw downsample 2× — aliased (wrong pattern)
aliased = checker[::2, ::2]  # Takes every other pixel

# Proper downsample with anti-aliasing
from PIL import Image
img = Image.fromarray(checker)
proper = img.resize((64, 64), Image.LANCZOS)  # Produces grey (correct)
```

## Related Concepts

- [[nyquist_criterion]] — the rule that predicts when aliasing occurs
- [[anti_aliasing_filter|Anti-Aliasing Filter]] — low-pass filter applied before downsampling to prevent aliasing
- [[downsampling]] — the operation that commonly triggers aliasing
- [[sampling]] — the fundamental process where aliasing originates

## Sources

- [[00_introduction_to_digital_images|Tutorial 00: Introduction to Digital Images]] — Part 4: Zoom and Aliasing
