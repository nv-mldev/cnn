"""
Exercises: Why Not Pixels
==========================
Stub functions for all six exercises.  Fill in the # YOUR CODE HERE sections.
Each function has a docstring explaining the goal and expected output.

Run this script to check your implementations.
"""

# --- Setup ---
from pathlib import Path
import numpy as np
import cv2
import matplotlib.pyplot as plt

CH02_DIR = Path(__file__).parent / '../../DIP3E_Original_Images_CH02'


# ── Exercise 1 ──────────────────────────────────────────────
def verify_orthogonality(vector: np.ndarray) -> float:
    """
    Mean-subtract the vector and return the dot product of the residual
    with [1,1,...,1].

    The result should be 0.0 (or very close to 0 due to floating point)
    for any input vector.

    Args:
        vector: A 1D numpy array of any length.

    Returns:
        The dot product of (vector - mean) with ones(len(vector)).
        Expected: ≈ 0.0 for all inputs.

    Example:
        >>> verify_orthogonality(np.array([10, 20, 30]))
        0.0
    """
    # YOUR CODE HERE
    pass


def exercise_1() -> None:
    """Test verify_orthogonality on 5 vectors of different lengths."""
    test_vectors = [
        np.array([10, 20, 30], dtype=float),
        np.array([255, 0, 128, 64], dtype=float),
        np.array([7.3, 2.1, 9.8], dtype=float),
        np.array([100, 200, 150, 50, 80, 120], dtype=float),
        np.array([1.0, 1.0, 1.0], dtype=float),
    ]
    print("=== Exercise 1: Verify Orthogonality ===")
    for v in test_vectors:
        dot = verify_orthogonality(v)
        status = "PASS ✓" if dot is not None and abs(dot) < 1e-10 else "FAIL ✗ (implement function)"
        print(f"  vector={v}  dot product={dot}  {status}")


# ── Exercise 2 ──────────────────────────────────────────────
def ccoeff_normed(patch: np.ndarray, template: np.ndarray) -> float:
    """
    Compute the CCOEFF_NORMED (Pearson correlation) between two patches.

    Args:
        patch: 1D array of pixel values.
        template: 1D array of pixel values (same length as patch).

    Returns:
        Pearson correlation coefficient in [-1, 1].
    """
    # YOUR CODE HERE
    pass


def exercise_2() -> None:
    """Show that CCOEFF_NORMED fails for non-uniform brightness offsets."""
    template = np.array([100, 150, 200], dtype=float)

    # Uniform offset (should give r = 1.0)
    uniform_patch = template + 50

    # Non-uniform offset (hint: add different amounts to each pixel)
    # YOUR CODE HERE
    non_uniform_patch = None   # replace with your implementation

    r_uniform     = ccoeff_normed(uniform_patch, template)
    r_non_uniform = ccoeff_normed(non_uniform_patch, template) if non_uniform_patch is not None else None

    print("\n=== Exercise 2: When Does CCOEFF_NORMED Fail? ===")
    print(f"  Uniform offset (+50):     r = {r_uniform}  (expected: 1.0)")
    print(f"  Non-uniform offset:       r = {r_non_uniform}  (expected: < 1.0)")


# ── Exercise 3 ──────────────────────────────────────────────
def exercise_3() -> None:
    """
    Run cv2.TM_SQDIFF_NORMED and cv2.TM_CCOEFF_NORMED on four scenes:
    original, brightness ×0.7, rotated 5°, scaled 90%.

    Print a comparison table showing which method handles which transform.

    Hint: For CCOEFF_NORMED, best match is at max_val, not min_val.
    """
    # Load image
    candidates = list(CH02_DIR.glob('*.tif')) + list(CH02_DIR.glob('*.png'))
    if candidates:
        scene = cv2.imread(str(candidates[0]), cv2.IMREAD_GRAYSCALE)
    else:
        row = np.linspace(20, 240, 256)
        col = np.linspace(20, 200, 256)
        scene = (row[np.newaxis, :] * 0.5 + col[:, np.newaxis] * 0.5).astype(np.uint8)

    h, w   = scene.shape
    top    = h // 2 - 32
    left   = w // 2 - 32
    template = scene[top:top + 64, left:left + 64].copy()

    # YOUR CODE HERE
    # 1. Create the four transformed scenes (original, brightness, rotated, scaled)
    # 2. For each scene, run both TM_SQDIFF_NORMED and TM_CCOEFF_NORMED
    # 3. Read the score at (top, left) and print a comparison table

    print("\n=== Exercise 3: CCOEFF_NORMED on All Transforms ===")
    print("  (implement the function body)")


# ── Exercise 4 ──────────────────────────────────────────────
def gradient_magnitude_histogram(image: np.ndarray, n_bins: int = 10) -> np.ndarray:
    """
    Compute a histogram of gradient magnitudes for an image patch.

    This is a simple rotation-robust feature: rotation changes where the
    gradients are, but not how many of each magnitude exist.

    Args:
        image: 2D grayscale image patch (float32 or float64).
        n_bins: Number of histogram bins.

    Returns:
        Normalised histogram array of shape (n_bins,).
    """
    # Compute gradient magnitude
    # Hint: use np.diff on both axes, pad back to same size, then sqrt(gx^2 + gy^2)

    # YOUR CODE HERE
    pass


def exercise_4() -> None:
    """
    Test gradient_magnitude_histogram on T shapes at 0°, 15°, 45° and a circle.
    Show that T-shape histograms are similar and the circle differs.
    """
    def make_T_shape(size: int = 15, angle: float = 0.0) -> np.ndarray:
        img = np.zeros((size, size), dtype=np.float32)
        img[3, 3:12] = 200
        img[4, 3:12] = 200
        img[3:12, 7] = 200
        img[3:12, 8] = 200
        if angle != 0:
            centre = (size // 2, size // 2)
            M = cv2.getRotationMatrix2D(centre, angle, 1.0)
            img = cv2.warpAffine(img, M, (size, size), flags=cv2.INTER_LINEAR)
        return img

    t_0   = make_T_shape(angle=0)
    t_15  = make_T_shape(angle=15)
    t_45  = make_T_shape(angle=45)
    circle = np.zeros((15, 15), dtype=np.float32)
    cv2.circle(circle, (7, 7), 5, 200, 2)

    shapes = [(t_0, 'T (0°)'), (t_15, 'T (15°)'), (t_45, 'T (45°)'), (circle, 'Circle')]

    print("\n=== Exercise 4: Gradient Magnitude Histograms ===")
    histograms = {}
    for img, name in shapes:
        hist = gradient_magnitude_histogram(img)
        histograms[name] = hist
        print(f"  {name}: {hist}")

    # YOUR CODE HERE — also plot the histograms side by side


# ── Exercise 5 ──────────────────────────────────────────────
def exercise_5() -> None:
    """
    Compute pairwise SSD distance matrix for 5 shapes:
    T at 0°, 30°, 60°, L-shape, circle.

    Visualise as a heatmap and observe that pixel distance ≠ semantic distance.
    """
    def make_T_shape(size: int = 15, angle: float = 0.0) -> np.ndarray:
        img = np.zeros((size, size), dtype=np.float32)
        img[3, 3:12] = 200; img[4, 3:12] = 200
        img[3:12, 7] = 200; img[3:12, 8] = 200
        if angle != 0:
            M = cv2.getRotationMatrix2D((size // 2, size // 2), angle, 1.0)
            img = cv2.warpAffine(img, M, (size, size), flags=cv2.INTER_LINEAR)
        return img

    # YOUR CODE HERE
    # 1. Create t_0, t_30, t_60, l_shape, circle (all 15×15 float32)
    # 2. Compute 5×5 pairwise SSD matrix
    # 3. Plot as heatmap with labels
    # 4. Print observation: T shapes are not closer to each other than to other shapes

    print("\n=== Exercise 5: Pairwise SSD Distance Matrix ===")
    print("  (implement the function body)")


# ── Exercise 6 ──────────────────────────────────────────────
def exercise_6() -> None:
    """
    Quantize a continuous [0, 1] signal to 8-bit, 12-bit, and 16-bit.
    Count unique values and plot histograms.

    Expected: 8-bit retains ~256 unique values; 12-bit and 16-bit retain all 1000.
    """
    signal = np.linspace(0.0, 1.0, 1000, dtype=np.float32)

    print("\n=== Exercise 6: Quantization vs Bit Depth ===")
    for bits in [8, 12, 16]:
        # YOUR CODE HERE
        # quantized = ?
        # unique_count = ?
        quantized    = None
        unique_count = None
        print(f"  {bits}-bit ({2**bits} levels): unique values preserved = {unique_count}")

    # YOUR CODE HERE — also plot three histograms side by side


# ── Run all exercises ───────────────────────────────────────
if __name__ == '__main__':
    exercise_1()
    exercise_2()
    exercise_3()
    exercise_4()
    exercise_5()
    exercise_6()
