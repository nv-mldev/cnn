"""Image I/O utilities — loading and format conversion.

Handles loading images from disk and converting between
PIL (RGB) and OpenCV (BGR) representations.
"""

import numpy as np
from PIL import Image


def pil_to_cv(pil_image: Image.Image) -> np.ndarray:
    """Convert a PIL Image (RGB) to an OpenCV-compatible array (BGR).

    Why BGR? OpenCV uses BGR channel ordering by convention (historical reasons
    from early camera hardware). PIL uses RGB. We need to flip the channels
    so that OpenCV functions like matchTemplate see the correct colors.

    Args:
        pil_image: A PIL Image in RGB mode.

    Returns:
        A numpy array in BGR format, suitable for OpenCV operations.
    """
    # Convert PIL → numpy (RGB), then reverse the channel axis to get BGR
    rgb_array = np.array(pil_image)
    bgr_array = rgb_array[:, :, ::-1].copy()  # .copy() ensures contiguous memory
    return bgr_array


def load_images(
    scene_path: str, template_path: str
) -> tuple[Image.Image, Image.Image]:
    """Load the scene and template images from disk as PIL Images.

    Both images are converted to RGB so that downstream code doesn't need
    to worry about palette or grayscale modes.

    Args:
        scene_path: File path to the scene (haystack) image.
        template_path: File path to the template (needle) image.

    Returns:
        A tuple of (scene_pil, template_pil) in RGB mode.

    Raises:
        FileNotFoundError: If either file doesn't exist on disk.
    """
    scene_pil = Image.open(scene_path).convert("RGB")
    template_pil = Image.open(template_path).convert("RGB")
    return scene_pil, template_pil
