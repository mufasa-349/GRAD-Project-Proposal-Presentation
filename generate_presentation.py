from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parent
IMAGES = ROOT / "images"
OUT_DIR = ROOT / "out"


def _set_title_style(shape) -> None:
    tf = shape.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    run = p.add_run()
    run.font.size = Pt(36)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x11, 0x11, 0x11)


def _set_body_style(shape) -> None:
    tf = shape.text_frame
    tf.word_wrap = True
    for p in tf.paragraphs:
        for r in p.runs:
            r.font.size = Pt(20)


def add_title_slide(prs: Presentation, title: str, subtitle_lines: list[str]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[0])  # Title
    slide.shapes.title.text = title

    subtitle = slide.placeholders[1]
    subtitle.text_frame.clear()
    p = subtitle.text_frame.paragraphs[0]
    p.text = subtitle_lines[0] if subtitle_lines else ""
    p.font.size = Pt(20)

    for line in subtitle_lines[1:]:
        p2 = subtitle.text_frame.add_paragraph()
        p2.text = line
        p2.font.size = Pt(20)


def add_bullets_slide(
    prs: Presentation,
    title: str,
    bullets: list[str],
    *,
    italic_bullets: Optional[set[int]] = None,
    subtitle: Optional[str] = None,
) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[1])  # Title and Content
    slide.shapes.title.text = title

    if subtitle:
        subtitle_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(12.0), Inches(0.5))
        tf = subtitle_box.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = subtitle
        p.font.size = Pt(16)
        p.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    body = slide.shapes.placeholders[1]
    tf = body.text_frame
    tf.clear()
    tf.word_wrap = True

    italic_bullets = italic_bullets or set()

    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = 0
        p.space_after = Pt(2)
        p.font.size = Pt(20)
        p.font.color.rgb = RGBColor(0x11, 0x11, 0x11)
        p.text = ""  # we’ll use a run to support italics reliably
        r = p.add_run()
        r.text = b
        r.font.size = Pt(20)
        r.font.italic = i in italic_bullets


def _add_picture_contain(slide, img_path: Path, left, top, width, height, *, caption: Optional[str] = None):
    if not img_path.exists():
        tb = slide.shapes.add_textbox(left, top, width, height)
        tb.text_frame.text = f"[Missing image: {img_path.name}]"
        tb.text_frame.paragraphs[0].font.size = Pt(16)
        tb.text_frame.paragraphs[0].font.color.rgb = RGBColor(0xAA, 0x00, 0x00)
        return

    pic = slide.shapes.add_picture(str(img_path), left, top, width=width, height=height)

    if caption:
        cap_top = top + height + Inches(0.05)
        cap = slide.shapes.add_textbox(left, cap_top, width, Inches(0.4))
        tf = cap.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = caption
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(0x44, 0x44, 0x44)
        p.alignment = PP_ALIGN.CENTER

    return pic


def add_title_and_image_slide(
    prs: Presentation,
    title: str,
    image_filename: str,
    *,
    caption: Optional[str] = None,
) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Title Only
    slide.shapes.title.text = title

    _add_picture_contain(
        slide,
        IMAGES / image_filename,
        Inches(0.75),
        Inches(1.55),
        Inches(12.0),
        Inches(5.6),
        caption=caption,
    )


def add_two_images_system_overview(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Title only
    slide.shapes.title.text = "System Overview"

    # Pipeline strip
    pipeline = (
        "Raw Spatio-Temporal Data  →  Preprocessing & Cleaning  →  Uncertainty Estimation  →  "
        "Visual Encoding Layer  →  Interactive Dashboard  →  Decision Support"
    )
    pipe_box = slide.shapes.add_textbox(Inches(0.7), Inches(1.15), Inches(12.1), Inches(0.55))
    tf = pipe_box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = pipeline
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    p.alignment = PP_ALIGN.CENTER

    labels = [
        "Raw Data: location + time + observed values",
        "Preprocessing: cleaning, aggregation, temporal alignment",
        "Uncertainty Estimation: confidence, variance, missingness, prediction error",
        "Visual Encoding: opacity, blur, gradients, density-aware views",
        "Dashboard: map, timeline, filters, interaction",
        "Decision Support: identify reliable and uncertain regions",
    ]

    labels_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.5), Inches(1.1))
    tf2 = labels_box.text_frame
    tf2.clear()
    tf2.word_wrap = True
    for i, line in enumerate(labels):
        p2 = tf2.paragraphs[0] if i == 0 else tf2.add_paragraph()
        p2.text = line
        p2.level = 0
        p2.font.size = Pt(14)
        p2.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    # Two screenshots, side-by-side
    left = Inches(0.75)
    top = Inches(3.0)
    w = Inches(5.85)
    h = Inches(3.6)
    gap = Inches(0.3)

    _add_picture_contain(
        slide,
        IMAGES / "dense1.png",
        left,
        top,
        w,
        h,
        caption="Dense raw point data (high density, overplotting risk).",
    )
    _add_picture_contain(
        slide,
        IMAGES / "heatmap1.png",
        left + w + gap,
        top,
        w,
        h,
        caption="Uncertainty-aware aggregated view (density/heatmap encoding).",
    )


def build_presentation() -> Path:
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 widescreen
    prs.slide_height = Inches(7.5)

    # 1) Title
    add_title_slide(
        prs,
        "Project #543\nVisualizing Spatio-Temporal Uncertainty in High-Density Data",
        ["Mustafa Bozyel", "Senih Kırmaç", "Ömer Mert Özel"],
    )

    # 2) Problem & Motivation
    add_bullets_slide(
        prs,
        "Problem & Motivation",
        bullets=[
            "Real-world spatio-temporal data is inherently uncertain (sensor noise, missingness, drift).",
            "Standard dashboards often present values as deterministic, masking uncertainty.",
            "Goal: visualize uncertainty to support safer, more informed decision-making.",
            "Key challenge: communicate uncertainty in high-density data without visual overload.",
            "*Example (to validate): on a city-scale GNSS trace, accuracy varies over time; a single line can hide drift, while uncertainty-aware encodings reveal low-confidence segments.*",
        ],
        italic_bullets={4},
    )

    # 3) Related Works (max 2 slides)
    add_bullets_slide(
        prs,
        "Related Works — Uncertainty Visualization Design Space",
        bullets=[
            "Padilla, Kay, and Hullman (2022): design space of uncertainty visualization techniques.",
            "Distributional graphics (e.g., quantile dot plots, ensemble plots) vs. direct visual encodings.",
            "For high-density spatio-temporal data: prefer density-aware encodings (opacity, blur, gradients) to reduce clutter.",
            "MacEachren et al. (2012): visual semiotics—blur, transparency, fuzziness, and size effectively communicate uncertainty.",
        ],
    )
    add_title_and_image_slide(
        prs,
        "Related Works — Design Space (Padilla et al., 2022)",
        "padilla1.png",
        caption="Uncertainty visualization techniques and encodings (overview figure).",
    )

    add_bullets_slide(
        prs,
        "Related Works — Spatial Uncertainty & Decision-Oriented Views",
        bullets=[
            "McKenzie et al. (spatial uncertainty examples): uncertainty in map/mobile interfaces.",
            "Common approach: positional uncertainty regions (e.g., circles), enriched with contextual cues.",
            "Risk: hard boundaries can imply false certainty; continuous uncertainty should avoid rigid borders.",
            "Liu et al. (2016): representative sampling / ensemble visualization for multiple possible outcomes.",
            "Implication: uncertainty views must balance clarity, density, and user interpretation.",
        ],
    )
    add_title_and_image_slide(
        prs,
        "Related Works — Spatial Uncertainty Example",
        "from-report1.png",
        caption="Example of spatial uncertainty depiction for decision-making contexts.",
    )

    # 4) System Overview (pipeline + 2 images)
    add_two_images_system_overview(prs)

    # 5) Data Flow Diagram (2 slides)
    add_title_and_image_slide(
        prs,
        "Data Flow Diagram — Data Insertion",
        "data-workflow1.png",
        caption="End-to-end ingestion flow: raw logs → parsing → storage/indexing.",
    )
    add_title_and_image_slide(
        prs,
        "Data Flow Diagram — Operations / Interaction Workflow",
        "operation-workflow.png",
        caption="User operations: filtering, mode selection, comparison, and visual updates.",
    )

    # 6) Methodology (GNSS Fix Visualization)
    add_bullets_slide(
        prs,
        "Methodology — GNSS Fix Visualization (Leaflet + D3)",
        bullets=[
            "Ingest Android GNSS Logger data; keep only “Fix,” rows → *_FixOnly.txt (CSV-like).",
            "Optionally load OSM GPX reference exported as *_latlon_by_time.txt (TSV: ISO_TIME, LAT, LON).",
            "Parse Fix fields (lat/lon/alt/speed/accuracy/bearing/UnixTimeMillis/VerticalAccuracyMeters) in a web app via fetch().",
            "Compute derived metrics: Haversine distance-from-first, Δlat/Δlon, and Δalt.",
            "Render multiple views: point map (color=distance, size=accuracy), heatmaps (grid/soft density; 30 m stationary threshold; hover window i±7), and uncertainty rings (radius=AccuracyMeters).",
            "Compare mode: align GNSS vs OSM reference; compute nearest-neighbor deviation and signed cross-track deviation; show on map + D3 chart.",
            "Tools/Tech: Leaflet, D3.js, JavaScript (fetch), and Python preprocessing utilities as needed.",
            "Outputs: interactive map, linked chart (Lon vs Alt / Lon vs deviation), and summary stats panel.",
        ],
    )

    # 7) Validation & Testing
    add_bullets_slide(
        prs,
        "Validation & Testing — GNSS Fix Visualization (Leaflet + D3)",
        bullets=[
            "Test data / scenarios: stationary and walking traces; with/without OSM reference track; varying fix density and accuracy.",
            "Input validation: accept only well-formed Fix lines (len ≥ 13); skip non-finite lat/lon/alt; treat missing fields as null.",
            "Loading checks: relative URLs (./data/...) for GitHub Pages or local HTTP server; manual upload fallback verified.",
            "Metric sanity: Haversine distance ranges and monotonic distance-from-first checks; validate Δlat/Δlon/Δalt against raw fields.",
            "Visualization testing: Original / Heatmap (mono & BGR) / Uncertainty modes render without errors; 30 m moving threshold enforced; hover i±7 preview stable.",
            "Compare-mode validation: nearest-neighbor and signed cross-track deviation consistent across hover and chart; chart clipping ±3 m applied correctly.",
            "Acceptance criteria: no runtime errors; consistent stats panel ranges; map selection fields match chart values for the same fix index.",
        ],
    )

    # 8) Demo (4 slides)
    add_title_and_image_slide(
        prs,
        "Demo — Reference vs Raw GNSS Comparison",
        "dashboard1.png",
        caption="Comparison of reference track vs raw GNSS; chart shows distance deviation (meters).",
    )
    add_title_and_image_slide(
        prs,
        "Demo — Deviations in Stationary Data",
        "dashboard2.png",
        caption="Observed drift/deviation patterns while device is stable.",
    )
    add_title_and_image_slide(
        prs,
        "Demo — Uncertainty in Stationary Data (Density / Heatmap)",
        "dashboard3.png",
        caption="Density-based encoding for stationary uncertainty patterns.",
    )
    add_title_and_image_slide(
        prs,
        "Demo — Uncertainty in Stationary Data (Heatmap)",
        "dashboard4.png",
        caption="Heatmap encoding for stationary uncertainty patterns.",
    )
    add_title_and_image_slide(
        prs,
        "Demo — Walking Data",
        "dashboard5.png",
        caption="Behavior of density/heatmap uncertainty views on walking traces.",
    )

    # 9) Conclusion
    add_bullets_slide(
        prs,
        "Conclusion",
        bullets=[
            "Built an interactive GNSS fix analysis tool (Leaflet map + D3 chart) for visual exploration.",
            "Parsed and cleaned Android GNSS Logger Fix records; computed derived metrics (distance-from-first, deltas).",
            "Provided multiple perspectives: point view, density/heatmaps, and uncertainty rings.",
            "Enabled reference-based evaluation using OSM track comparison (nearest-neighbor + cross-track deviation).",
            "Improved interpretability of accuracy, drift, and route-level behavior through linked interactions (hover/click).",
        ],
    )

    # 10) Future Work
    add_bullets_slide(
        prs,
        "Future Work",
        bullets=[
            "Large-scale validation on dense, high-frequency, long-duration datasets (city-scale, many tracks).",
            "Performance: mitigate browser memory pressure and UI lag (many markers / heavy heat computations).",
            "Visualization scaling: address overplotting, zoom-dependent density bias, and detail loss (clustering/tiling).",
            "Data quality: handle time misalignment, outliers/multipath effects, and missing accuracy fields robustly.",
            "Next steps: spatial indexing (grid/k-d tree), vector tiling, incremental/streamed loading, and outlier filtering.",
        ],
    )

    # 11) Thanks
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
    box = slide.shapes.add_textbox(Inches(0.5), Inches(2.6), Inches(12.3), Inches(1.4))
    tf = box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = "Thank you."
    p.font.size = Pt(54)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "Project_543_Uncertainty_Visualization.pptx"
    prs.save(str(out_path))
    return out_path


if __name__ == "__main__":
    path = build_presentation()
    print(f"Saved: {path}")

