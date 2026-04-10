# Exercises: Why Not Pixels

Work through these exercises after reading Parts 1–7. Each one deepens understanding
of a specific concept.

---

## Exercise 1: Verify Orthogonality for Any Vector

**Task:** Write a function that takes any vector, mean-subtracts it, and verifies the
residual is orthogonal to $[1,1,...,1]$ by checking the dot product. Test it on 5
different vectors of different lengths.

**Hint:** `np.ones(len(vector))` gives you $[1,1,...,1]$ of the right size.

**Expected output:** Dot product should be 0 (or very close to 0 due to floating point)
for every vector.

---

## Exercise 2: When Does CCOEFF_NORMED Fail?

**Task:** Create a template and a scene patch where the pattern is the same but a
**non-uniform** brightness change has been applied (e.g., a gradient shadow). Compute
`ccoeff_normed` and show that it is no longer 1.0.

**Hint:** Add different offsets to different pixels: `patch = template + np.array([10, 30, 50])`.

**Expected output:** $r < 1.0$ — mean subtraction cannot remove non-uniform offsets.

---

## Exercise 3: CCOEFF_NORMED on All Transforms

**Task:** Run `cv2.TM_CCOEFF_NORMED` on the original, brightness-altered, rotated, and
scaled scenes. Compare scores with `TM_SQDIFF_NORMED`. Which transforms does each method
handle?

**Hint:** For CCOEFF_NORMED, best match is at `max_val` (use `max_loc`), not `min_val`.

**Expected output:** CCOEFF_NORMED fixes brightness but still fails on rotation/scale.

---

## Exercise 4: Design a Rotation-Robust Feature

**Task:** Create a simple feature that is invariant to rotation. Idea: compute the
**histogram of gradient magnitudes** (not orientations) for a patch. Since rotation
changes *where* gradients are but not *how many* of each magnitude, the histogram should
be similar.

Test it: create a T shape at 0°, 15°, 45° and a circle. Compute the gradient magnitude
histogram for each. Show that T shapes have similar histograms while the circle differs.

**Hint:** Use `np.histogram(gradient_magnitudes, bins=10, range=(0, 255))`

**Expected output:** T-shape histograms cluster together, circle histogram is different.

---

## Exercise 5: Pixel Distance vs Semantic Distance

**Task:** Create 5 synthetic images: T at 0°, T at 30°, T at 60°, an L-shape, and a
circle. Compute the pairwise SSD between all pairs (a 5×5 distance matrix). Visualise as
a heatmap. Does SSD distance reflect semantic similarity?

**Hint:** Use `np.sum((img_a - img_b)**2)` for each pair. `plt.imshow(distance_matrix,
cmap='viridis')` for the heatmap.

**Expected output:** The distance matrix shows T shapes are NOT consistently closer to
each other than to other shapes — pixel distance ≠ semantic distance.

---

## Exercise 6: Quantization vs Bit Depth

**Task:** Take a float32 signal with 1000 evenly spaced values between 0.0 and 1.0.
Quantize it to 8-bit (256 levels), 12-bit (4096 levels), and 16-bit (65536 levels).
For each, count how many unique values survive after quantization. Plot the three
histograms side by side.

**Hint:** To quantize: `quantized = np.round(signal * (2**bits - 1)).astype(int)`.

**Expected output:** 8-bit retains ~256 unique values, 12-bit ~1000 (all of them),
16-bit ~1000.
