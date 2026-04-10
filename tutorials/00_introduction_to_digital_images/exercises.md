# Exercises: Introduction to Digital Images

Three practice problems that connect the theory from Parts 1–5 to pixel-level
comparison failures. Complete `exercises.py` to solve each one.

---

## Exercise 1: Downsampling and Interpolation Error

**Task:** Load `Fig0222(b)(cameraman).tif`. Downsample it to 32×32 pixels using
nearest-neighbour, then upsample it back to the original size using two methods:
nearest-neighbour and bilinear. Compute the Mean Absolute Error (MAE) between
the original image and each upscaled version.

**Hint:** Use PIL's `Image.resize()` with `Image.NEAREST` and `Image.BILINEAR`.
MAE = `np.mean(np.abs(original.astype(float) - reconstructed.astype(float)))`.

**Expected output:**
- Bilinear MAE will be lower than nearest-neighbour MAE — bilinear blending
  reduces the blockiness artefact.
- Both MAE values will be large (>10) — downsampling to 32×32 permanently
  destroys most of the image information. No upsampling method can recover it.

---

## Exercise 2: Quantization and SSD

**Task:** Take a 64×64 crop from `Fig0222(b)(cameraman).tif`. Quantize it to
4-bit and 2-bit versions using the `quantize_image` function from Part 2.
Compute the Sum of Squared Differences (SSD) between the original 8-bit crop
and each quantized version. How does quantization error scale with bit depth?

**Hint:** SSD = `np.sum((image_a.astype(float) - image_b.astype(float)) ** 2)`.

**Expected output:** SSD grows dramatically as bits decrease — quantization alone
can make identical images look "different" to a pixel comparator. Even 6-bit
quantization (which looks nearly identical to the eye) produces a non-zero SSD.

---

## Exercise 3: Template Matching with Mismatched Resolutions

**Task:** Using `Fig0222(b)(cameraman).tif`, crop a 32×32 template from the
top-left region. Create a "query image" by downsampling the full image to half
resolution and then upsampling back. Try to locate the template in the query image
using SSD at every position. Does the template match at the expected location?
How does resolution mismatch affect the match quality?

**Hint:** Slide the template over the query image and compute SSD at each position.
The location of the minimum SSD is the best match.

**Expected output:** The minimum SSD location will be shifted or wrong compared
to the known template origin, because the half-resolution round-trip changes pixel
values even though the content is the same. This demonstrates that pixel comparison
is sensitive to resolution, not just scene content.
