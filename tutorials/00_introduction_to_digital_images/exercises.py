"""
Exercises: Introduction to Digital Images

Three practice problems connecting sampling, quantization, and interpolation
to pixel-level comparison failures.

Complete each stub function (replace # YOUR CODE HERE with your implementation),
then run the script to check your results.

Run: python exercises.py
"""

# --- Setup ---
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

COLORS = {
    'primary':   '#2196F3',
    'secondary': '#4CAF50',
    'result':    '#FFC107',
    'highlight': '#F44336',
    'transform': '#9C27B0',
    'gradient':  '#FF9800',
}

DIP_CH02 = Path(__file__).parent / '../../DIP3E_Original_Images_CH02'

np.random.seed(42)
print("Exercises: Introduction to Digital Images")
print("=" * 50)


# ── Shared helper ───────────────────────────────────────────
def quantize_image(image: np.ndarray, num_bits: int) -> np.ndarray:
    """Quantize a grayscale image to the given number of bits.

    Args:
        image:    2D array of uint8 pixel values (0–255).
        num_bits: Target bit depth (1–8).

    Returns:
        Quantized image rescaled back to 0–255 range (uint8).
    """
    num_levels   = 2 ** num_bits
    scale_factor = 255.0 / (num_levels - 1)
    quantized    = np.floor(image / scale_factor + 0.5) * scale_factor
    return quantized.clip(0, 255).astype(np.uint8)


# ══════════════════════════════════════════════════════════════
# Exercise 1: Downsampling and Interpolation Error
# ══════════════════════════════════════════════════════════════

def exercise1_downsampling_mae() -> None:
    """Downsample to 32×32, upsample back with two methods, compare MAE.

    Steps:
      1. Load the cameraman image and convert to grayscale.
      2. Record the original size.
      3. Downsample to 32×32 using Image.NEAREST.
      4. Upsample back to original size using Image.NEAREST.
      5. Upsample back to original size using Image.BILINEAR.
      6. Compute MAE between original and each upscaled version.
      7. Display the three images side by side with MAE in the title.
      8. Print the MAE values and a short explanation.
    """
    # YOUR CODE HERE
    # Downsample to 32×32, upsample back with two methods, compare MAE
    pass


# ══════════════════════════════════════════════════════════════
# Exercise 2: Quantization and SSD
# ══════════════════════════════════════════════════════════════

def exercise2_quantization_ssd() -> None:
    """Quantize a 64×64 crop to 4-bit and 2-bit, compute SSD vs original.

    Steps:
      1. Load the cameraman image and convert to grayscale.
      2. Crop the top-left 64×64 region.
      3. Quantize the crop to 8-bit, 4-bit, and 2-bit using quantize_image().
      4. Compute SSD between the original 8-bit crop and each quantized version.
      5. Display the three quantized crops side by side with SSD in the title.
      6. Print SSD values for each bit depth.

    Hint:
      SSD = np.sum((a.astype(float) - b.astype(float)) ** 2)
    """
    # YOUR CODE HERE
    # Quantize a crop to different bit depths, compute SSD against original
    pass


# ══════════════════════════════════════════════════════════════
# Exercise 3: Template Matching with Mismatched Resolutions
# ══════════════════════════════════════════════════════════════

def exercise3_template_matching_resolution() -> None:
    """Template matching when the query image has a different resolution.

    Steps:
      1. Load the cameraman image and convert to grayscale.
      2. Crop a 32×32 template from a known location (e.g. row=60, col=90).
      3. Create a "query image" by downsampling the full image to half size
         (NEAREST) then upsampling back to original size (NEAREST).
      4. Slide the template over the query image and compute SSD at each
         valid position. Build a 2D SSD map.
      5. Find the minimum SSD position and compare to the known template origin.
      6. Display: original image, query image, SSD map (with true and found
         locations marked).
      7. Print the true origin, best-match location, and minimum SSD.

    Hint:
      for row in range(0, query.shape[0] - template.shape[0] + 1):
          for col in range(0, query.shape[1] - template.shape[1] + 1):
              patch = query[row:row+th, col:col+tw]
              ssd_map[row, col] = np.sum((patch.astype(float)
                                          - template.astype(float)) ** 2)
    """
    # YOUR CODE HERE
    # Template matching with mismatched resolutions
    pass


# ── Run all exercises ───────────────────────────────────────
print("\n--- Exercise 1: Downsampling and MAE ---")
exercise1_downsampling_mae()

print("\n--- Exercise 2: Quantization and SSD ---")
exercise2_quantization_ssd()

print("\n--- Exercise 3: Template Matching with Mismatched Resolution ---")
exercise3_template_matching_resolution()
