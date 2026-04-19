# 00: Introduction to Digital Images

Each part is a paired `.md` (theory) + `.py` (runnable code) covering one concept in the chain:
digitisation → sensor physics → pixels → contrast → zoom/aliasing → colour.

## Parts

| File pair | Description |
|-----------|-------------|
| `part1_digitisation` | **What is sampling?** 1D signals, Nyquist theorem, phase offset fragility, aliasing as frequency folding, 1D→2D extension, moiré |
| `part2_sensor_physics` | Inside the sensor: photosites, well capacity, shot noise, phone vs DSLR SNR |
| `part3_pixels_and_resolution` | What a pixel actually is; spatial resolution and ground sampling distance; quantization and false contours |
| `part4_contrast_and_dynamic_range` | Contrast and the affine model I₂ = a·I₁ + b; dynamic range limits; Einstein contrast example |
| `part5_zoom_and_aliasing` | Nearest-neighbour vs bilinear zoom; downsampling information loss; checkerboard aliasing demo |
| `part6_colour_and_pipeline` | RGB channel decomposition; luminance formula; the full imaging pipeline; tungsten filament shading |
| `exercises` | Practice problems: downsampling MAE, quantization SSD, template matching with resolution mismatch |

## Pedagogical order

```
Sampling & Nyquist (theory)
  ↓
Sensor physics (what physically executes the sampling)
  ↓
Pixels & resolution (what sampling produces)
  ↓
Contrast & dynamic range (what the pixel values mean)
  ↓
Zoom & aliasing (practical consequences of sampling limits)
  ↓
Colour & pipeline (putting it all together)
```

## Running

```bash
uv run python part1_digitisation.py
uv run python part2_sensor_physics.py
uv run python part3_pixels_and_resolution.py
uv run python part4_contrast_and_dynamic_range.py
uv run python part5_zoom_and_aliasing.py
uv run python part6_colour_and_pipeline.py
uv run python exercises.py   # stub — complete the exercises first
```

## Image paths

DIP3E images are resolved relative to this folder:

```
../../DIP3E_Original_Images_CH02/
```

Images used:
- `Fig0219(rose1024).tif` — colour image for channel decomposition (Part 6)
- `Fig0220(a)(chronometer 3692x2812  2pt25 inch 1250 dpi).tif` — high-resolution detail for downsampling demo (Part 5)
- `Fig0222(b)(cameraman).tif` — primary grayscale reference image (Parts 3, 5, Exercises)
- `Fig0229(a)(tungsten_filament_shaded).tif` — shading artefact demo (Part 6)
- `Fig0229(b)(tungsten_sensor_shading).tif` — sensor shading pattern (Part 6)
- `Fig0241(a)(einstein low contrast).tif` — contrast demo (Part 4)
- `Fig0241(b)(einstein med contrast).tif` — contrast demo (Part 4)
- `Fig0241(c)(einstein high contrast).tif` — contrast demo (Part 4)

## Next

After completing this series, continue to:

- `../02_why_not_pixels/` — where these effects cause pixel comparison to fail in
  practice, and what normalisation can do about it.
