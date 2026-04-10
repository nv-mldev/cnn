"""The Fragility of Pixel-Perfect Matching — Tutorial Script.

This script demonstrates why naive template matching (pixel-by-pixel
comparison) breaks under real-world conditions like rotation, scaling,
and lighting changes. It motivates the need for feature-based methods.

Flow:
  1. Load scene and template images
  2. Part 1: Run template matching on the original (ideal) scene
  3. Part 2: Generate transformed scenes and show how matching degrades
  4. Part 3: Discussion questions leading to feature-based thinking
"""

import sys
from pathlib import Path

# Add project root to path so we can import utils
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.image_io import load_images, pil_to_cv
from utils.matching import run_template_match, annotate_match
from utils.transforms import generate_transformed_scenes
from utils.visualization import show_match_result

# --- Configuration ---
INPUT_SCENE_PATH = str(Path(__file__).resolve().parent.parent / "images" / "image.webp")
INPUT_TEMPLATE_PATH = str(Path(__file__).resolve().parent.parent / "images" / "logo.webp")


def main() -> None:
    print("--- Assignment: The Fragility of Pixel-Perfect Matching (In-Memory Version) ---\n")
    print("NOTE: Close each plot window to continue to the next step.\n")

    # ── Step 1: Load images ──────────────────────────────────────────
    print(f"Loading '{INPUT_SCENE_PATH}' and '{INPUT_TEMPLATE_PATH}' into memory...")

    try:
        scene_original_pil, template_pil = load_images(INPUT_SCENE_PATH, INPUT_TEMPLATE_PATH)
    except FileNotFoundError:
        print(f"Error: Make sure '{INPUT_SCENE_PATH}' and '{INPUT_TEMPLATE_PATH}' are in the same directory.")
        return

    template_width, template_height = template_pil.size
    print("Images loaded successfully.\n")

    # ── Step 2 — Part 1: Ideal case (perfect match) ──────────────────
    print("** Part 1: The Ideal Case - A Perfect Match **")
    print("Performing template matching on the original in-memory scene...")

    scene_original_bgr = pil_to_cv(scene_original_pil)
    template_bgr = pil_to_cv(template_pil)

    # Run matching and annotate the result
    match_score_ideal, match_top_left = run_template_match(scene_original_bgr, template_bgr)
    annotate_match(
        scene_original_bgr, match_top_left,
        template_width, template_height,
        match_score_ideal,
        box_color=(0, 255, 0),  # green = good match
    )

    print(f"  - Best match score: {match_score_ideal:.4f} (closer to 0 is perfect)")
    print(f"  - Match location (top-left): {match_top_left}")
    print("  - Displaying result for original scene...\n")
    show_match_result(scene_original_bgr, "Part 1: Ideal Case - Perfect Match (Original Scene)")

    # ── Step 3 — Part 2: Transformed scenes ──────────────────────────
    print("** Part 2: The Realistic Cases - Generating Transformed Scenes in Memory **")
    scenes_to_test = generate_transformed_scenes(scene_original_pil)
    for name in scenes_to_test:
        print(f"  - {name} created in memory.")
    print()

    print("** Part 2: The Realistic Cases - Matching Transformed Scenes **")

    for title, scene_pil in scenes_to_test.items():
        print(f"Performing template matching on '{title}'...")

        current_scene_bgr = pil_to_cv(scene_pil)
        # Re-convert template each iteration to keep it clean (no prior annotations)
        template_bgr = pil_to_cv(template_pil)

        # Guard: template must fit inside the (possibly smaller) scene
        if (template_bgr.shape[0] > current_scene_bgr.shape[0]
                or template_bgr.shape[1] > current_scene_bgr.shape[1]):
            print("  - SKIPPING: Template is larger than the scaled scene.")
            print("    This demonstrates a limitation where the template must fit within the search image.\n")
            continue

        match_score, top_left = run_template_match(current_scene_bgr, template_bgr)
        annotate_match(
            current_scene_bgr, top_left,
            template_width, template_height,
            match_score,
            box_color=(0, 0, 255),  # red = degraded match
        )

        print(f"  - Best match score: {match_score:.4f}")
        print(f"  - Match location (top-left): {top_left}")
        print("  - Displaying result image...\n")
        show_match_result(current_scene_bgr, f"Part 2: Matching {title}")

    # ── Step 4 — Part 3: Discussion questions ────────────────────────
    print("\n--- Assignment Complete ---")
    print("You have seen how even minor changes to the scene can drastically affect template matching scores.")
    print("\n**Discussion Questions (Part 3):**")
    print("1. Why did a simple 5-degree rotation cause the match to fail so drastically?")
    print("2. What do these results tell you about using a fixed grid of pixels as the 'definition' of an object?")
    print("3. If you couldn't use a pixel-perfect template, how would you describe the logo? (This leads to the concept of features).")


if __name__ == "__main__":
    main()
