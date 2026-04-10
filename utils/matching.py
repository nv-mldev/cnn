"""Template matching utilities — core matching and result annotation.

Wraps OpenCV's matchTemplate with a clean interface and provides
a helper to draw bounding boxes + score text on the result image.
"""

import cv2
import numpy as np


def run_template_match(
    scene_bgr: np.ndarray,
    template_bgr: np.ndarray,
) -> tuple[float, tuple[int, int]]:
    """Run template matching and return the best match score and location.

    Uses TM_SQDIFF_NORMED — the squared difference between template and each
    patch in the scene, normalized to [0, 1]. Lower score = better match.
    The best match is at the global minimum (not maximum).

    Args:
        scene_bgr: The scene image in BGR format (OpenCV convention).
        template_bgr: The template image in BGR format.

    Returns:
        A tuple of (match_score, top_left_corner):
            - match_score (float): The SQDIFF_NORMED value (0 = perfect match).
            - top_left_corner (tuple[int, int]): (x, y) of the best match location.
    """
    result = cv2.matchTemplate(scene_bgr, template_bgr, cv2.TM_SQDIFF_NORMED)

    # For SQDIFF methods, the best match is at the minimum value
    min_val, _, min_loc, _ = cv2.minMaxLoc(result)

    return min_val, min_loc


def annotate_match(
    scene_bgr: np.ndarray,
    top_left: tuple[int, int],
    template_width: int,
    template_height: int,
    match_score: float,
    box_color: tuple[int, int, int] = (0, 255, 0),
) -> np.ndarray:
    """Draw a bounding box and score label on the scene image.

    Modifies the image in-place AND returns it for convenience.

    Args:
        scene_bgr: The scene image (BGR). Will be modified in-place.
        top_left: (x, y) of the match's top-left corner.
        template_width: Width of the template in pixels.
        template_height: Height of the template in pixels.
        match_score: The SQDIFF_NORMED score to display.
        box_color: BGR color for the rectangle and text. Default green.

    Returns:
        The annotated scene image (same reference as input).
    """
    bottom_right = (top_left[0] + template_width, top_left[1] + template_height)

    # Draw the bounding box around the detected region
    cv2.rectangle(scene_bgr, top_left, bottom_right, box_color, 3)

    # Put the score text just above the bounding box
    score_text = f"Score (SQDIFF_NORMED): {match_score:.4f}"
    cv2.putText(
        scene_bgr,
        score_text,
        (top_left[0], top_left[1] - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.4,
        (255, 0, 0),  # blue in BGR
        1,
    )

    return scene_bgr
