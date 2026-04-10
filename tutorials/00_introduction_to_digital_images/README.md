# 00: Introduction to Digital Images

Extracted from `../00_introduction_to_digital_images.ipynb`. Each part is a paired
`.md` (theory) + `.py` (runnable code) file covering one concept in the chain:
light → sensor → pixel → resolution → quantization → contrast → zoom → aliasing → colour.

## Parts

| File pair | Description |
|-----------|-------------|
| `part1_sampling_and_sensors` | 1D sampling analogy; sensor physics (photosites, well capacity, shot noise); phone vs DSLR SNR comparison |
| `part2_pixels_and_resolution` | What a pixel actually is; spatial resolution and ground sampling distance; quantization and false contours |
| `part3_contrast_and_dynamic_range` | Contrast and the affine model I₂ = a·I₁ + b; dynamic range limits; the Einstein low/medium/high contrast example |
| `part4_zoom_and_aliasing` | Nearest-neighbour vs bilinear zoom; downsampling information loss; checkerboard aliasing demo |
| `part5_colour_and_pipeline` | RGB channel decomposition; luminance formula; the full imaging pipeline; tungsten filament shading example |
| `exercises` | Three practice problems: downsampling MAE, quantization SSD, template matching with resolution mismatch |

## Running

Each `.py` file is standalone:

```bash
python part1_sampling_and_sensors.py
python part2_pixels_and_resolution.py
python part3_contrast_and_dynamic_range.py
python part4_zoom_and_aliasing.py
python part5_colour_and_pipeline.py
python exercises.py   # stub — complete the exercises first
```

## Image paths

DIP3E images are resolved relative to this folder:

```
../../DIP3E_Original_Images_CH02/
```

Images used:
- `Fig0219(rose1024).tif` — colour image for channel decomposition (Part 5)
- `Fig0220(a)(chronometer 3692x2812  2pt25 inch 1250 dpi).tif` — high-resolution detail for downsampling demo (Part 4)
- `Fig0222(b)(cameraman).tif` — primary grayscale reference image (Parts 2, 4, Exercises)
- `Fig0229(a)(tungsten_filament_shaded).tif` — shading artefact demo (Part 5)
- `Fig0229(b)(tungsten_sensor_shading).tif` — sensor shading pattern (Part 5)
- `Fig0241(a)(einstein low contrast).tif` — contrast demo (Part 3)
- `Fig0241(b)(einstein med contrast).tif` — contrast demo (Part 3)
- `Fig0241(c)(einstein high contrast).tif` — contrast demo (Part 3)

## Next

After completing this series, continue to:

- `../02_why_not_pixels.ipynb` — where these effects cause pixel comparison to fail in
  practice, and what normalisation can do about it.
