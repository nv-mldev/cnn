"""
Manim Visualisations for Vector Projection & Mean Subtraction
==============================================================

Companion to `why_normalisation.md` — 3Blue1Brown-style animations that
teach the geometric intuition behind template matching normalisation.

Each scene follows the skill template structure:
  1. Title card (2s)
  2. Setup (5-10s)
  3. Build intuition (20-40s)
  4. Key insight (5-10s)
  5. Math connection (10-15s)
  6. Summary card (3s)

Render a single scene (low quality preview):
    manim -pql visualise_normalisation.py VectorAsPixels

Render high quality:
    manim -pqh visualise_normalisation.py MeanSubtractionProjection

Render all scenes:
    manim -pql visualise_normalisation.py
"""

from manim import *
import numpy as np

# ---------------------------------------------------------------------------
# Color constants — 3Blue1Brown-inspired palette, consistent across scenes
# ---------------------------------------------------------------------------

VEC_PRIMARY = BLUE          # Original pixel vector
VEC_SECONDARY = GREEN       # [1,1,1] diagonal / secondary vectors
VEC_RESULT = YELLOW         # Result / pattern component after projection
HIGHLIGHT = RED             # Key insights, emphasis
GRADIENT_COLOR = ORANGE     # Shifted / offset vectors
POSITIVE = GREEN            # Positive annotations
NEGATIVE = RED              # Negative annotations

# Pixel values ÷ 100 so [100,150,200] → [1.0, 1.5, 2.0] in Manim coords.
# Without this, vectors would be hundreds of units long and off-screen.
SCALE_FACTOR = 1 / 100


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def scale_pixel_vector(pixel_values: list[float]) -> np.ndarray:
    """Convert raw pixel values to Manim-friendly coordinates.

    Example:
        [100, 150, 200] → [1.0, 1.5, 2.0]
    """
    return np.array(pixel_values) * SCALE_FACTOR


def compute_mean_decomposition(pixel_values: list[float]) -> dict:
    """Decompose a pixel vector into brightness + pattern components.

    Given v = [100, 150, 200]:
        mean = 150
        v_parallel      = 150 * [1,1,1] = [150, 150, 150]   (brightness)
        v_perpendicular = v - v_parallel = [-50, 0, 50]       (pattern)

    Returns a dict with all components in both raw and scaled forms.
    """
    vector = np.array(pixel_values, dtype=float)
    mean_value = np.mean(vector)

    # v_parallel is the projection onto the [1,1,1] direction
    # This is the brightness component — uniform across all pixels
    v_parallel = np.full_like(vector, mean_value)

    # v_perpendicular is what's left after removing brightness
    # This is the pattern — the relative differences between pixels
    v_perpendicular = vector - v_parallel

    return {
        "original": vector,
        "mean": mean_value,
        "v_parallel": v_parallel,
        "v_perpendicular": v_perpendicular,
        "original_scaled": vector * SCALE_FACTOR,
        "v_parallel_scaled": v_parallel * SCALE_FACTOR,
        "v_perpendicular_scaled": v_perpendicular * SCALE_FACTOR,
    }


def make_axes(axis_range: tuple = (-1, 4, 1)) -> ThreeDAxes:
    """Create 3D axes for pixel-space visualization.

    Default range [-1, 4] covers scaled pixel values from -100 to 400.
    """
    return ThreeDAxes(
        x_range=axis_range,
        y_range=axis_range,
        z_range=axis_range,
        x_length=5,
        y_length=5,
        z_length=5,
        axis_config={"include_tip": True, "tip_length": 0.15},
    )


def make_diagonal_line(axes: ThreeDAxes, length: float = 6.0) -> Line3D:
    """Draw the [1,1,1] diagonal — the direction of uniform brightness.

    Every point on this line has all three pixel values equal (e.g., [c,c,c]).
    """
    unit_diagonal = np.array([1, 1, 1]) / np.sqrt(3)
    start = axes.c2p(*(unit_diagonal * -1))
    end = axes.c2p(*(unit_diagonal * length))
    return Line3D(start=start, end=end, color=VEC_SECONDARY)


def make_perp_plane(
    axes: ThreeDAxes,
    center: np.ndarray = np.array([0, 0, 0]),
    size: float = 3.0,
) -> Surface:
    """Create the plane perpendicular to [1,1,1] passing through a point.

    This plane is where all mean-subtracted vectors live. Any vector on
    this plane has elements that sum to zero — only pattern, no brightness.

    Basis vectors for the plane (both ⊥ to [1,1,1]):
        e1 = [1, -1, 0] / √2
        e2 = [1, 1, -2] / √6
    """
    e1 = np.array([1, -1, 0]) / np.sqrt(2)
    e2 = np.array([1, 1, -2]) / np.sqrt(6)
    half = size / 2

    def parametric_plane(u, v):
        point = center + u * e1 + v * e2
        return axes.c2p(*point)

    surface = Surface(
        lambda u, v: parametric_plane(u, v),
        u_range=[-half, half],
        v_range=[-half, half],
        resolution=(8, 8),
    )
    surface.set_fill_by_value(
        axes=axes,
        colorscale=[(VEC_RESULT, -1), (VEC_RESULT, 1)],
        axis=2,
    )
    surface.set_opacity(0.15)
    return surface


def make_arrow_with_label(
    scene: ThreeDScene,
    axes: ThreeDAxes,
    end_coords: np.ndarray,
    label_tex: str,
    color,
    label_direction=UP + RIGHT,
    font_size: int = 20,
) -> tuple:
    """Create an Arrow3D with a 3b1b-style label at the tip.

    The label lives in 3D space (moves with camera rotation) but always
    faces the camera (readable from any angle). This is the 3Blue1Brown
    approach: `add_fixed_orientation_mobjects` instead of
    `add_fixed_in_frame_mobjects`.

    Returns (arrow, label) tuple.
    """
    arrow = Arrow3D(
        start=axes.c2p(0, 0, 0),
        end=axes.c2p(*end_coords),
        color=color,
    )

    label = MathTex(label_tex, font_size=font_size, color=color)
    # Position label in 3D space near the arrow tip — not pinned to a
    # screen corner. This is the key difference from the old code.
    label.next_to(arrow.get_end(), label_direction, buff=0.15)

    # add_fixed_orientation_mobjects: label lives at a 3D position but
    # always faces the camera. Contrast with add_fixed_in_frame_mobjects
    # which pins the label to screen coordinates (ignoring 3D space).
    scene.add_fixed_orientation_mobjects(label)

    return arrow, label


def make_title_card(
    scene: ThreeDScene,
    title_text: str,
    subtitle_text: str,
) -> tuple:
    """Create a 3b1b-style title card: big title + smaller subtitle.

    Shows for 2 seconds then fades out. Returns nothing — self-contained.
    """
    title = Text(title_text, font_size=48)
    subtitle = Text(subtitle_text, font_size=24, color=GREY)
    subtitle.next_to(title, DOWN, buff=0.3)
    group = VGroup(title, subtitle)

    # Title cards are always screen-pinned (they appear before 3D content)
    scene.add_fixed_in_frame_mobjects(group)

    scene.play(Write(title), FadeIn(subtitle))
    scene.wait(2)
    scene.play(FadeOut(group))


def make_summary_card(scene: ThreeDScene, text: str) -> None:
    """Show a one-sentence summary at the end of the scene (3s)."""
    summary = Text(text, font_size=32, color=WHITE)
    scene.add_fixed_in_frame_mobjects(summary)
    scene.play(Write(summary))
    scene.wait(3)
    scene.play(FadeOut(summary))


# ===========================================================================
# Scene 1: VectorAsPixels
# ===========================================================================
# A pixel patch [100, 150, 200] is just a point (vector) in 3D space.
# Duration target: ~30s

class VectorAsPixels(ThreeDScene):
    """A 3-pixel patch is a single vector in 3D space."""

    def construct(self):
        # --- 1. Title card (2s) ---
        make_title_card(
            self,
            "Pixels as Vectors",
            "A 3-pixel patch lives in 3D space",
        )

        # --- 2. Setup: axes + camera ---
        axes = make_axes()
        axis_labels = axes.get_axis_labels(
            x_label=MathTex("p_1", font_size=20),
            y_label=MathTex("p_2", font_size=20),
            z_label=MathTex("p_3", font_size=20),
        )
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        self.play(Create(axes), Write(axis_labels), run_time=1.5)
        self.wait(1)

        # --- 3. Build intuition: draw the vector ---
        # The patch [100, 150, 200] becomes the point (1.0, 1.5, 2.0)
        scaled = scale_pixel_vector([100, 150, 200])

        arrow, label = make_arrow_with_label(
            self, axes, scaled,
            label_tex=r"[100, 150, 200]",
            color=VEC_PRIMARY,
        )
        dot = Dot3D(point=axes.c2p(*scaled), color=VEC_PRIMARY, radius=0.06)

        self.play(Create(arrow), FadeIn(dot), Write(label), run_time=1.5)
        self.wait(1)

        # Rotate camera — the label tracks the arrow tip in 3D space
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(3)
        self.stop_ambient_camera_rotation()

        # --- 4. Key insight ---
        insight = Text(
            "Each pixel value = one coordinate",
            font_size=28, color=HIGHLIGHT,
        )
        self.add_fixed_in_frame_mobjects(insight)
        insight.to_edge(UP)
        self.play(Write(insight))
        self.wait(2)

        # --- 5. Math connection ---
        formula = MathTex(
            r"\vec{v} = \begin{bmatrix} 100 \\ 150 \\ 200 \end{bmatrix}"
            r"\xrightarrow{\div 100}"
            r"\begin{bmatrix} 1.0 \\ 1.5 \\ 2.0 \end{bmatrix}",
            font_size=22, color=WHITE,
        )
        self.add_fixed_in_frame_mobjects(formula)
        formula.to_edge(DOWN)
        self.play(Write(formula))
        self.wait(2)

        self.play(FadeOut(insight), FadeOut(formula))

        # --- 6. Summary card (3s) ---
        self.play(
            FadeOut(arrow), FadeOut(dot), FadeOut(label),
            FadeOut(axes), FadeOut(axis_labels),
        )
        make_summary_card(
            self,
            "A pixel patch is just a point in n-dimensional space",
        )


# ===========================================================================
# Scene 2: BrightnessOffset
# ===========================================================================
# Adding a constant brightness offset (+30 to all pixels) shifts the
# vector toward the [1,1,1] diagonal, changing its direction.
# Duration target: ~45s

class BrightnessOffset(ThreeDScene):
    """Brightness offset = adding c*[1,1,1], which changes direction."""

    def construct(self):
        # --- 1. Title card (2s) ---
        make_title_card(
            self,
            "Brightness Offset",
            "Adding a constant shifts direction toward [1,1,1]",
        )

        # --- 2. Setup ---
        axes = make_axes()
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)
        self.play(Create(axes), run_time=1)
        self.wait(1)

        # Draw the [1,1,1] diagonal first — it's the reference line
        diagonal = make_diagonal_line(axes, length=5.0)
        diag_label = MathTex(
            r"[1,1,1]", font_size=20, color=VEC_SECONDARY,
        )
        diag_label.next_to(diagonal.get_end(), UP, buff=0.15)
        self.add_fixed_orientation_mobjects(diag_label)
        self.play(Create(diagonal), Write(diag_label), run_time=1)
        self.wait(1)

        # --- 3. Build intuition ---
        # Original vector: [100, 150, 200]
        original = scale_pixel_vector([100, 150, 200])
        arrow_orig, lbl_orig = make_arrow_with_label(
            self, axes, original,
            label_tex=r"[100, 150, 200]",
            color=VEC_PRIMARY,
            label_direction=RIGHT,
        )
        self.play(Create(arrow_orig), Write(lbl_orig), run_time=1)
        self.wait(1)

        # Shifted vector: [130, 180, 230] = original + 30*[1,1,1]
        shifted = scale_pixel_vector([130, 180, 230])
        arrow_shifted, lbl_shifted = make_arrow_with_label(
            self, axes, shifted,
            label_tex=r"[130, 180, 230]",
            color=GRADIENT_COLOR,
            label_direction=UP,
        )
        self.play(Create(arrow_shifted), Write(lbl_shifted), run_time=1)
        self.wait(1)

        # --- Zoom into the region where the offset arrow connects tips ---
        # The offset arrow is small (only 30 pixels = 0.3 units), so we
        # zoom in to make it clearly visible. We center on the midpoint
        # between the two arrow tips.
        offset = scale_pixel_vector([30, 30, 30])
        midpoint = axes.c2p(*(original + offset / 2))
        self.move_camera(
            frame_center=midpoint,
            zoom=2.5,
            run_time=1.5,
        )
        self.wait(0.5)

        # Show the offset vector connecting the two tips
        # Now zoomed in, the viewer can clearly see the shift along [1,1,1]
        arrow_offset = Arrow3D(
            start=axes.c2p(*original),
            end=axes.c2p(*(original + offset)),
            color=HIGHLIGHT,
        )
        lbl_offset = MathTex(
            r"+30 \cdot [1,1,1]",
            font_size=20, color=HIGHLIGHT,
        )
        lbl_offset.next_to(arrow_offset.get_end(), RIGHT, buff=0.15)
        self.add_fixed_orientation_mobjects(lbl_offset)
        self.play(Create(arrow_offset), Write(lbl_offset), run_time=1)
        self.wait(1)

        # --- Zoom back out to see the full picture ---
        self.move_camera(
            frame_center=ORIGIN,
            zoom=1,
            run_time=1.5,
        )
        self.wait(0.5)

        # --- 4. Key insight ---
        insight = Text(
            "Same pattern, different direction!",
            font_size=28, color=HIGHLIGHT,
        )
        self.add_fixed_in_frame_mobjects(insight)
        insight.to_edge(UP)
        self.play(Write(insight))
        self.wait(2)

        # --- 5. Math connection ---
        formula = MathTex(
            r"\vec{v}' = \vec{v} + c \cdot \mathbf{1}"
            r"\quad \Rightarrow \quad"
            r"\hat{v}' \neq \hat{v}",
            font_size=22, color=WHITE,
        )
        self.add_fixed_in_frame_mobjects(formula)
        formula.to_edge(DOWN)
        self.play(Write(formula))
        self.wait(2)

        # Brief rotation to see the geometry from another angle
        self.begin_ambient_camera_rotation(rate=0.25)
        self.wait(3)
        self.stop_ambient_camera_rotation()

        self.play(
            FadeOut(insight), FadeOut(formula),
            FadeOut(arrow_orig), FadeOut(lbl_orig),
            FadeOut(arrow_shifted), FadeOut(lbl_shifted),
            FadeOut(arrow_offset), FadeOut(lbl_offset),
            FadeOut(diagonal), FadeOut(diag_label),
            FadeOut(axes),
        )

        # --- 6. Summary card (3s) ---
        make_summary_card(
            self,
            "Brightness offset changes vector direction — normalisation alone can't fix it",
        )


# ===========================================================================
# Scene 3: MeanSubtractionProjection
# ===========================================================================
# The core scene. Decomposes v = v_parallel + v_perpendicular, shows the
# perpendicular plane, and proves orthogonality via dot product.
# Duration target: ~60s

class MeanSubtractionProjection(ThreeDScene):
    """Decompose a vector into brightness (parallel) + pattern (perpendicular)."""

    def construct(self):
        # --- 1. Title card (2s) ---
        make_title_card(
            self,
            "Mean Subtraction",
            "Projecting out the brightness component",
        )

        # --- 2. Setup ---
        axes = make_axes(axis_range=(-2, 4, 1))
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
        self.play(Create(axes), run_time=1)

        # Draw the [1,1,1] diagonal
        diagonal = make_diagonal_line(axes, length=5.0)
        self.play(Create(diagonal), run_time=0.5)
        self.wait(1)

        # --- 3. Build intuition: step-by-step decomposition ---
        decomp = compute_mean_decomposition([100, 150, 200])
        v_orig = decomp["original_scaled"]       # [1.0, 1.5, 2.0]
        v_par = decomp["v_parallel_scaled"]       # [1.5, 1.5, 1.5]
        v_perp = decomp["v_perpendicular_scaled"] # [-0.5, 0.0, 0.5]

        # Step A: Show the original vector
        arrow_v, lbl_v = make_arrow_with_label(
            self, axes, v_orig,
            label_tex=r"\vec{v}",
            color=VEC_PRIMARY,
            label_direction=RIGHT,
            font_size=24,
        )
        self.play(Create(arrow_v), Write(lbl_v), run_time=1)
        self.wait(1)

        # Step B: Show v_parallel — the brightness component along [1,1,1]
        arrow_par, lbl_par = make_arrow_with_label(
            self, axes, v_par,
            label_tex=r"\vec{v}_{\parallel}",
            color=GRADIENT_COLOR,
            label_direction=LEFT + DOWN,
            font_size=24,
        )
        self.play(Create(arrow_par), Write(lbl_par), run_time=1)
        self.wait(1)

        # Step C: Show v_perpendicular — the pattern component
        arrow_perp, lbl_perp = make_arrow_with_label(
            self, axes, v_perp,
            label_tex=r"\vec{v}_{\perp}",
            color=VEC_RESULT,
            label_direction=DOWN + RIGHT,
            font_size=24,
        )
        self.play(Create(arrow_perp), Write(lbl_perp), run_time=1)
        self.wait(1)

        # --- Zoom into the parallelogram region to see the decomposition ---
        # Center on the original vector's tip — the parallelogram vertex
        self.move_camera(
            frame_center=axes.c2p(*v_orig),
            zoom=2,
            run_time=1.5,
        )
        self.wait(0.5)

        # Step D: Show the parallelogram — v = v_parallel + v_perp
        # Connector from tip of v_parallel to tip of v (translated v_perp)
        connector_1 = DashedLine(
            start=axes.c2p(*v_par),
            end=axes.c2p(*v_orig),
            color=VEC_RESULT,
        )
        # Connector from tip of v_perp to tip of v (translated v_parallel)
        connector_2 = DashedLine(
            start=axes.c2p(*v_perp),
            end=axes.c2p(*v_orig),
            color=GRADIENT_COLOR,
        )
        self.play(Create(connector_1), Create(connector_2), run_time=1)
        self.wait(1)

        # --- Zoom back out to reveal the full plane ---
        self.move_camera(
            frame_center=ORIGIN,
            zoom=1,
            run_time=1.5,
        )
        self.wait(0.5)

        # Step E: Show the perpendicular plane through the origin
        plane = make_perp_plane(axes, center=np.array([0, 0, 0]))
        plane_label = MathTex(
            r"\text{Pattern plane} \perp [1,1,1]",
            font_size=20, color=VEC_RESULT,
        )
        self.add_fixed_in_frame_mobjects(plane_label)
        plane_label.to_edge(UP)
        self.play(FadeIn(plane), Write(plane_label), run_time=1)
        self.wait(1)

        # --- 4. Key insight: dot product = 0 proves orthogonality ---
        insight = MathTex(
            r"[-50, 0, 50] \cdot [1,1,1] = 0 \;\checkmark",
            font_size=24, color=HIGHLIGHT,
        )
        self.add_fixed_in_frame_mobjects(insight)
        insight.next_to(plane_label, DOWN, buff=0.3)
        self.play(Write(insight))
        self.wait(2)

        # --- 5. Math connection ---
        formula = MathTex(
            r"\vec{v} = \underbrace{\bar{v} \cdot \mathbf{1}}"
            r"_{\text{brightness}}"
            r"+ \underbrace{(\vec{v} - \bar{v} \cdot \mathbf{1})}"
            r"_{\text{pattern}}",
            font_size=20, color=WHITE,
        )
        self.add_fixed_in_frame_mobjects(formula)
        formula.to_edge(DOWN)
        self.play(Write(formula))
        self.wait(2)

        # Brief rotation to see the plane from different angles
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)
        self.stop_ambient_camera_rotation()

        self.play(
            FadeOut(plane_label), FadeOut(insight), FadeOut(formula),
            FadeOut(arrow_v), FadeOut(lbl_v),
            FadeOut(arrow_par), FadeOut(lbl_par),
            FadeOut(arrow_perp), FadeOut(lbl_perp),
            FadeOut(connector_1), FadeOut(connector_2),
            FadeOut(plane), FadeOut(diagonal), FadeOut(axes),
        )

        # --- 6. Summary card (3s) ---
        make_summary_card(
            self,
            "Mean subtraction projects onto the plane where only pattern survives",
        )


# ===========================================================================
# Scene 4: MultipleVectorsSamePattern
# ===========================================================================
# Three brightness-shifted versions of the same pattern all collapse to
# the same point [-50, 0, 50] after mean subtraction.
# Duration target: ~50s

class MultipleVectorsSamePattern(ThreeDScene):
    """Three brightness-shifted vectors collapse to one pattern vector."""

    def construct(self):
        # --- 1. Title card (2s) ---
        make_title_card(
            self,
            "Brightness Invariance",
            "All brightness shifts collapse to the same pattern",
        )

        # --- 2. Setup ---
        axes = make_axes(axis_range=(-2, 7, 1))
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)
        self.play(Create(axes), run_time=1)

        # Draw the diagonal and perpendicular plane
        diagonal = make_diagonal_line(axes, length=8.0)
        plane = make_perp_plane(axes, center=np.array([0, 0, 0]), size=4.0)
        self.play(Create(diagonal), FadeIn(plane), run_time=0.5)
        self.wait(1)

        # --- 3. Build intuition: draw three vectors with the same pattern ---
        vectors_data = [
            {"raw": [100, 150, 200], "color": VEC_PRIMARY,
             "tex": r"[100, 150, 200]", "dir": RIGHT},
            {"raw": [130, 180, 230], "color": GRADIENT_COLOR,
             "tex": r"[130, 180, 230]", "dir": UP + RIGHT},
            {"raw": [500, 550, 600], "color": PURPLE,
             "tex": r"[500, 550, 600]", "dir": UP},
        ]

        arrows = []
        labels = []

        # Animate ONE thing at a time — show each vector sequentially
        for data in vectors_data:
            scaled = scale_pixel_vector(data["raw"])
            arrow, label = make_arrow_with_label(
                self, axes, scaled,
                label_tex=data["tex"],
                color=data["color"],
                label_direction=data["dir"],
            )
            self.play(Create(arrow), Write(label), run_time=0.8)
            self.wait(0.5)
            arrows.append(arrow)
            labels.append(label)

        self.wait(1)

        # --- 4. Key insight: mean subtraction collapses all three ---
        insight = Text(
            "Subtract the mean from each...",
            font_size=28, color=HIGHLIGHT,
        )
        self.add_fixed_in_frame_mobjects(insight)
        insight.to_edge(UP)
        self.play(Write(insight))
        self.wait(1)

        # All three collapse to [-50, 0, 50]
        pattern_scaled = scale_pixel_vector([-50, 0, 50])
        pattern_arrow, pattern_label = make_arrow_with_label(
            self, axes, pattern_scaled,
            label_tex=r"[-50, 0, 50]",
            color=VEC_RESULT,
            label_direction=DOWN + RIGHT,
            font_size=24,
        )
        pattern_dot = Dot3D(
            point=axes.c2p(*pattern_scaled),
            color=VEC_RESULT, radius=0.08,
        )

        # Fade out the three originals, fade in the single collapsed result
        self.play(
            *[FadeOut(a) for a in arrows],
            *[FadeOut(l) for l in labels],
            Create(pattern_arrow),
            FadeIn(pattern_dot),
            Write(pattern_label),
            run_time=2,
        )
        self.wait(1)

        # --- 5. Math connection ---
        # Replace insight text with the decomposition equations
        self.play(FadeOut(insight))

        formula = MathTex(
            r"[100,150,200] &= 150\!\cdot\![1,1,1] + [-50,0,50]\\",
            r"[130,180,230] &= 180\!\cdot\![1,1,1] + [-50,0,50]\\",
            r"[500,550,600] &= 550\!\cdot\![1,1,1] + [-50,0,50]",
            font_size=20, color=WHITE,
        )
        self.add_fixed_in_frame_mobjects(formula)
        formula.to_edge(UP)
        self.play(Write(formula))
        self.wait(2)

        # Rotate to see the collapsed point from all angles
        self.begin_ambient_camera_rotation(rate=0.25)
        self.wait(4)
        self.stop_ambient_camera_rotation()

        self.play(
            FadeOut(formula),
            FadeOut(pattern_arrow), FadeOut(pattern_dot), FadeOut(pattern_label),
            FadeOut(plane), FadeOut(diagonal), FadeOut(axes),
        )

        # --- 6. Summary card (3s) ---
        make_summary_card(
            self,
            "Mean subtraction makes template matching brightness-invariant",
        )
