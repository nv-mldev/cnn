# 01b — Linear Algebra Prerequisites for Template Matching

This series bridges the linear algebra gap between basic Python and
Stanford CS231n. Every concept is grounded in the sensor/signal/noise domain
and motivated by a concrete imaging problem: normalised template matching.

**Master objective:** understand the linear algebra that underpins
`TM_CCOEFF_NORMED` — vectors, norms, dot products, orthogonality, and
projections — from first principles.

---

## Structure

| File | Topic | Cells |
|------|-------|-------|
| [part1_vectors_and_dot_product](part1_vectors_and_dot_product.md) | Pixels as vectors, dot product definition and geometric meaning | 0–11 |
| [part2_norms_and_similarity](part2_norms_and_similarity.md) | L2 norm, unit vectors, cosine similarity, brightness-offset blind spot | 11–22 |
| [part3_orthogonality_and_projection](part3_orthogonality_and_projection.md) | Orthogonality, mean subtraction as projection, decomposition | 22–31 |
| [part4_linear_transforms](part4_linear_transforms.md) | Lighting model I = aT + b, orthogonal transforms, DFT, Parseval's theorem | 31–41 |
| [exercises](exercises.md) | Three practice exercises | 41–48 |

Each part has a paired `.py` file that runs standalone:

```bash
python part1_vectors_and_dot_product.py
python part2_norms_and_similarity.py
python part3_orthogonality_and_projection.py
python part4_linear_transforms.py
python exercises.py
```

---

## Concept Map

```
Image patch
  └── flatten → n-dimensional vector
        ├── L2 norm          → energy / brightness
        ├── unit vector      → pattern (brightness removed)
        ├── dot product      → pixel-by-pixel agreement
        └── cosine similarity → angle between patterns
              ├── handles contrast scaling ✓
              └── fails on brightness offset ✗
                    └── fix: mean subtraction
                          = orthogonal projection onto [1,1,...,1]
                          = brightness component removed
                          = pattern component preserved
```

---

## Prerequisites

- Basic Python and NumPy
- Completed notebook `00_intro_to_digital_images.ipynb`
- Completed notebook `01a_probability_for_sensors.ipynb`

## What comes next

`02_why_not_pixels.ipynb` — uses all these concepts to explain exactly how
`TM_SQDIFF_NORMED` and `TM_CCOEFF_NORMED` work in OpenCV template matching
and why raw pixel comparison fails.
