"""Scene transformation utilities — rotation, scaling, brightness.

These transforms simulate realistic conditions that break naive
pixel-perfect template matching, demonstrating why we need
feature-based approaches.
"""

import numpy as np
from PIL import Image


def rotate_scene(
    scene_pil: Image.Image,
    angle_degrees: float = 5.0,
) -> Image.Image:
    """Rotate the scene by a given angle without expanding the canvas.

    Why this breaks matching: Rotation changes the pixel grid alignment.
    Even a tiny rotation shifts every pixel to a new location, so the
    template's pixel pattern no longer lines up with the scene.

    Args:
        scene_pil: The original scene as a PIL Image.
        angle_degrees: Rotation angle in degrees (counter-clockwise).

    Returns:
        A new PIL Image with the scene rotated.
    """
    return scene_pil.rotate(angle_degrees, expand=False, resample=Image.BICUBIC)


def scale_scene(
    scene_pil: Image.Image,
    scale_factor: float = 0.9,
) -> Image.Image:
    """Scale (resize) the entire scene by a given factor.

    Why this breaks matching: The template was extracted at the original
    resolution. When the scene is scaled, the object appears at a
    different size, so the pixel-by-pixel comparison fails.

    Args:
        scene_pil: The original scene as a PIL Image.
        scale_factor: Multiplier for width and height (e.g., 0.9 = 90%).

    Returns:
        A new PIL Image with the scene scaled.
    """
    original_width, original_height = scene_pil.size
    scaled_width = int(original_width * scale_factor)
    scaled_height = int(original_height * scale_factor)
    return scene_pil.resize((scaled_width, scaled_height), Image.LANCZOS)


def adjust_brightness(
    scene_pil: Image.Image,
    brightness_factor: float = 0.7,
) -> Image.Image:
    """Adjust the brightness of the entire scene.

    Why this breaks matching: Template matching computes pixel differences.
    When brightness changes, every pixel value shifts, inflating the
    difference score even though the spatial pattern is unchanged.

    Args:
        scene_pil: The original scene as a PIL Image.
        brightness_factor: Multiplier for pixel values (< 1 = darker, > 1 = brighter).

    Returns:
        A new PIL Image with adjusted brightness.
    """
    scene_array = np.array(scene_pil, dtype=np.float32)
    scene_array *= brightness_factor
    # Clip to valid [0, 255] range before converting back to uint8
    return Image.fromarray(np.clip(scene_array, 0, 255).astype(np.uint8))


def generate_transformed_scenes(
    scene_pil: Image.Image,
) -> dict[str, Image.Image]:
    """Generate a dictionary of transformed scenes for testing.

    Creates three common real-world perturbations to demonstrate
    the fragility of pixel-perfect template matching.

    Args:
        scene_pil: The original scene as a PIL Image.

    Returns:
        A dict mapping descriptive names to transformed PIL Images.
    """
    transformed_scenes = {
        "Rotated Scene (5 degrees)": rotate_scene(scene_pil, angle_degrees=5.0),
        "Scaled Scene (90%)": scale_scene(scene_pil, scale_factor=0.9),
        "Brightness-Altered Scene": adjust_brightness(scene_pil, brightness_factor=0.7),
    }
    return transformed_scenes
