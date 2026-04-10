"""Visualization utilities — displaying match results with matplotlib.

Provides a single function to convert BGR → RGB and display
an annotated scene image with a title.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


def show_match_result(
    scene_bgr: np.ndarray,
    title: str,
    figsize: tuple[int, int] = (10, 8),
) -> None:
    """Display an annotated scene image using matplotlib.

    Converts from OpenCV's BGR to matplotlib's expected RGB,
    then shows the image in a non-blocking figure.

    Args:
        scene_bgr: The annotated scene image in BGR format.
        title: Title string displayed above the plot.
        figsize: Figure dimensions in inches (width, height).
    """
    # OpenCV stores images as BGR; matplotlib expects RGB
    image_rgb = cv2.cvtColor(scene_bgr, cv2.COLOR_BGR2RGB)

    plt.figure(figsize=figsize)
    plt.imshow(image_rgb)
    plt.title(title)
    plt.axis("off")
    plt.show()
