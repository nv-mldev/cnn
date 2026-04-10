# utils package — helper modules for the template matching tutorial
#
# Modules:
#   image_io      — loading images, PIL ↔ OpenCV conversion
#   matching       — template matching and result annotation
#   transforms     — scene transformations (rotate, scale, brightness)
#   visualization  — matplotlib display helpers

from utils.image_io import load_images, pil_to_cv
from utils.matching import run_template_match, annotate_match
from utils.transforms import generate_transformed_scenes
from utils.visualization import show_match_result
