from __future__ import annotations

from pathlib import Path
from typing import Optional

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parent
IMAGES = ROOT / "images"
OUT_DIR = ROOT / "out"

#
# Theme (Gestalt-driven, consistent “chrome”)
# - Similarity: same header/footer, same typography, same card framing
# - Proximity: consistent spacing grid and grouping (header/content/footer)
# - Continuation: left alignment and repeated visual rhythm across slides
# - Figure-ground: light background + white cards + dark header for contrast
#
THEME = {
    "bg": RGBColor(0xF7, 0xF8, 0xFA),
    "card_bg": RGBColor(0xFF, 0xFF, 0xFF),
    "border": RGBColor(0xE5, 0xE7, 0xEB),
    "text": RGBColor(0x11, 0x18, 0x27),
    "muted": RGBColor(0x6B, 0x72, 0x80),
    "navy": RGBColor(0x0B, 0x1F, 0x3B),
    "accent": RGBColor(0x1A, 0xA6, 0xB7),
}

GRID = {
    "margin_x": Inches(0.75),
    "margin_top": Inches(0.55),
    "header_h": Inches(0.72),
    "footer_h": Inches(0.35),
    "gutter": Inches(0.28),
}


def _set_slide_background(slide) -> None:
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = THEME["bg"]


def _add_header(slide, prs: Presentation, title: str, *, section: Optional[str] = None) -> None:
    sw = prs.slide_width

    header = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        0,
        0,
        sw,
        GRID["header_h"],
    )
    header.fill.solid()
    header.fill.fore_color.rgb = THEME["navy"]
    header.line.fill.background()

    accent = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        0,
        GRID["header_h"] - Inches(0.06),
        sw,
        Inches(0.06),
    )
    accent.fill.solid()
    accent.fill.fore_color.rgb = THEME["accent"]
    accent.line.fill.background()

    title_box = slide.shapes.add_textbox(GRID["margin_x"], Inches(0.14), sw - 2 * GRID["margin_x"], Inches(0.5))
    tf = title_box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    if section:
        sec_box = slide.shapes.add_textbox(GRID["margin_x"], Inches(0.46), sw - 2 * GRID["margin_x"], Inches(0.3))
        tf2 = sec_box.text_frame
        tf2.clear()
        p2 = tf2.paragraphs[0]
        p2.text = section
        p2.font.size = Pt(12)
        p2.font.color.rgb = THEME["accent"]


def _add_footer(slide, prs: Presentation, *, left_text: str, right_text: str) -> None:
    sw = prs.slide_width
    sh = prs.slide_height

    y = sh - GRID["footer_h"]
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, y, sw, Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = THEME["border"]
    line.line.fill.background()

    left = slide.shapes.add_textbox(GRID["margin_x"], y + Inches(0.05), Inches(8.0), Inches(0.25))
    tf = left.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = left_text
    p.font.size = Pt(10)
    p.font.color.rgb = THEME["muted"]

    right = slide.shapes.add_textbox(sw - GRID["margin_x"] - Inches(2.2), y + Inches(0.05), Inches(2.2), Inches(0.25))
    tf2 = right.text_frame
    tf2.clear()
    p2 = tf2.paragraphs[0]
    p2.text = right_text
    p2.font.size = Pt(10)
    p2.font.color.rgb = THEME["muted"]
    p2.alignment = PP_ALIGN.RIGHT


def add_title_slide(prs: Presentation, title: str, subtitle_lines: list[str]) -> None:
    # Use a blank slide to fully control layout (professional, consistent).
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
    _set_slide_background(slide)

    sw = prs.slide_width
    sh = prs.slide_height

    # Hero band (figure-ground)
    hero = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, sw, Inches(3.2))
    hero.fill.solid()
    hero.fill.fore_color.rgb = THEME["navy"]
    hero.line.fill.background()

    accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(3.2) - Inches(0.08), sw, Inches(0.08))
    accent.fill.solid()
    accent.fill.fore_color.rgb = THEME["accent"]
    accent.line.fill.background()

    # Title
    tbox = slide.shapes.add_textbox(GRID["margin_x"], Inches(1.0), sw - 2 * GRID["margin_x"], Inches(1.4))
    tf = tbox.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    # Authors
    abox = slide.shapes.add_textbox(GRID["margin_x"], Inches(3.65), sw - 2 * GRID["margin_x"], Inches(1.1))
    tf2 = abox.text_frame
    tf2.clear()
    for i, line in enumerate(subtitle_lines):
        p2 = tf2.paragraphs[0] if i == 0 else tf2.add_paragraph()
        p2.text = line
        p2.font.size = Pt(18)
        p2.font.color.rgb = THEME["text"]

    # Small badge (similarity cue)
    badge = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        GRID["margin_x"],
        sh - Inches(0.95),
        Inches(3.1),
        Inches(0.45),
    )
    badge.fill.solid()
    badge.fill.fore_color.rgb = THEME["card_bg"]
    badge.line.color.rgb = THEME["border"]
    btxt = slide.shapes.add_textbox(GRID["margin_x"] + Inches(0.2), sh - Inches(0.88), Inches(2.8), Inches(0.35))
    btf = btxt.text_frame
    btf.clear()
    bp = btf.paragraphs[0]
    bp.text = "Project #543"
    bp.font.size = Pt(12)
    bp.font.bold = True
    bp.font.color.rgb = THEME["navy"]


def add_bullets_slide(
    prs: Presentation,
    title: str,
    bullets: list[str],
    *,
    italic_bullets: Optional[set[int]] = None,
    subtitle: Optional[str] = None,
    section: Optional[str] = None,
) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank for consistent chrome
    _set_slide_background(slide)
    _add_header(slide, prs, title, section=section)

    if subtitle:
        subtitle_box = slide.shapes.add_textbox(
            GRID["margin_x"],
            GRID["header_h"] + Inches(0.15),
            prs.slide_width - 2 * GRID["margin_x"],
            Inches(0.45),
        )
        tf = subtitle_box.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = subtitle
        p.font.size = Pt(13)
        p.font.color.rgb = THEME["muted"]

    # Content card (proximity + figure-ground)
    content_top = GRID["header_h"] + (Inches(0.7) if subtitle else Inches(0.35))
    content_h = prs.slide_height - content_top - GRID["footer_h"] - Inches(0.2)

    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        GRID["margin_x"],
        content_top,
        prs.slide_width - 2 * GRID["margin_x"],
        content_h,
    )
    card.fill.solid()
    card.fill.fore_color.rgb = THEME["card_bg"]
    card.line.color.rgb = THEME["border"]

    body_box = slide.shapes.add_textbox(
        GRID["margin_x"] + Inches(0.35),
        content_top + Inches(0.25),
        prs.slide_width - 2 * GRID["margin_x"] - Inches(0.7),
        content_h - Inches(0.5),
    )
    tf = body_box.text_frame
    tf.clear()
    tf.word_wrap = True

    italic_bullets = italic_bullets or set()

    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = 0
        p.space_after = Pt(6)
        p.font.size = Pt(19)
        p.font.color.rgb = THEME["text"]
        p.text = ""  # we’ll use a run to support italics reliably
        r = p.add_run()
        r.text = b
        r.font.size = Pt(19)
        r.font.italic = i in italic_bullets
        r.font.color.rgb = THEME["text"]


def _add_picture_contain(slide, img_path: Path, left, top, width, height, *, caption: Optional[str] = None):
    if not img_path.exists():
        tb = slide.shapes.add_textbox(left, top, width, height)
        tb.text_frame.text = f"[Missing image: {img_path.name}]"
        tb.text_frame.paragraphs[0].font.size = Pt(16)
        tb.text_frame.paragraphs[0].font.color.rgb = RGBColor(0xAA, 0x00, 0x00)
        return

    # Card behind image for consistency (similarity) + separation (figure-ground)
    pad = Inches(0.08)
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = THEME["card_bg"]
    card.line.color.rgb = THEME["border"]

    pic = slide.shapes.add_picture(str(img_path), left + pad, top + pad, width=width - 2 * pad, height=height - 2 * pad)

    if caption:
        cap_top = top + height + Inches(0.08)
        cap = slide.shapes.add_textbox(left, cap_top, width, Inches(0.42))
        tf = cap.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = caption
        p.font.size = Pt(12)
        p.font.color.rgb = THEME["muted"]
        p.alignment = PP_ALIGN.CENTER

    return pic


def add_title_and_image_slide(
    prs: Presentation,
    title: str,
    image_filename: str,
    *,
    caption: Optional[str] = None,
    section: Optional[str] = None,
) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank for consistent chrome
    _set_slide_background(slide)
    _add_header(slide, prs, title, section=section)

    content_top = GRID["header_h"] + Inches(0.35)
    _add_picture_contain(
        slide,
        IMAGES / image_filename,
        GRID["margin_x"],
        content_top,
        prs.slide_width - 2 * GRID["margin_x"],
        prs.slide_height - content_top - GRID["footer_h"] - Inches(0.55),
        caption=caption,
    )


def add_two_images_system_overview(prs: Presentation) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank for consistent chrome
    _set_slide_background(slide)
    _add_header(slide, prs, "System Overview", section="Pipeline + prototype views")

    # Pipeline strip
    pipeline = (
        "Raw Spatio-Temporal Data  →  Preprocessing & Cleaning  →  Uncertainty Estimation  →  "
        "Visual Encoding Layer  →  Interactive Dashboard  →  Decision Support"
    )
    pipe_box = slide.shapes.add_textbox(GRID["margin_x"], GRID["header_h"] + Inches(0.18), prs.slide_width - 2 * GRID["margin_x"], Inches(0.55))
    tf = pipe_box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = pipeline
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = THEME["text"]
    p.alignment = PP_ALIGN.CENTER

    labels = [
        "Raw Data: location + time + observed values",
        "Preprocessing: cleaning, aggregation, temporal alignment",
        "Uncertainty Estimation: confidence, variance, missingness, prediction error",
        "Visual Encoding: opacity, blur, gradients, density-aware views",
        "Dashboard: map, timeline, filters, interaction",
        "Decision Support: identify reliable and uncertain regions",
    ]

    labels_box = slide.shapes.add_textbox(GRID["margin_x"], GRID["header_h"] + Inches(0.78), prs.slide_width - 2 * GRID["margin_x"], Inches(1.15))
    tf2 = labels_box.text_frame
    tf2.clear()
    tf2.word_wrap = True
    for i, line in enumerate(labels):
        p2 = tf2.paragraphs[0] if i == 0 else tf2.add_paragraph()
        p2.text = line
        p2.level = 0
        p2.font.size = Pt(12)
        p2.font.color.rgb = THEME["muted"]

    # Two screenshots, side-by-side
    left = GRID["margin_x"]
    top = GRID["header_h"] + Inches(2.15)
    w = (prs.slide_width - 2 * GRID["margin_x"] - GRID["gutter"]) / 2
    h = prs.slide_height - top - GRID["footer_h"] - Inches(0.75)
    gap = GRID["gutter"]

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
        section="Context + goal",
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
        section="Literature",
    )
    add_title_and_image_slide(
        prs,
        "Related Works — Design Space (Padilla et al., 2022)",
        "padilla1.png",
        caption="Uncertainty visualization techniques and encodings (overview figure).",
        section="Literature",
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
        section="Literature",
    )
    add_title_and_image_slide(
        prs,
        "Related Works — Spatial Uncertainty Example",
        "from-report1.png",
        caption="Example of spatial uncertainty depiction for decision-making contexts.",
        section="Literature",
    )

    # 4) System Overview (pipeline + 2 images)
    add_two_images_system_overview(prs)

    # 5) Data Flow Diagram (2 slides)
    add_title_and_image_slide(
        prs,
        "Data Flow Diagram — Data Insertion",
        "data-workflow1.png",
        caption="End-to-end ingestion flow: raw logs → parsing → storage/indexing.",
        section="Architecture",
    )
    add_title_and_image_slide(
        prs,
        "Data Flow Diagram — Operations / Interaction Workflow",
        "operation-workflow.png",
        caption="User operations: filtering, mode selection, comparison, and visual updates.",
        section="Architecture",
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
        section="Implementation",
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
        section="Quality",
    )

    # 8) Demo (4 slides)
    add_title_and_image_slide(
        prs,
        "Demo — Reference vs Raw GNSS Comparison",
        "dashboard1.png",
        caption="Comparison of reference track vs raw GNSS; chart shows distance deviation (meters).",
        section="Demo",
    )
    add_title_and_image_slide(
        prs,
        "Demo — Deviations in Stationary Data",
        "dashboard2.png",
        caption="Observed drift/deviation patterns while device is stable.",
        section="Demo",
    )
    add_title_and_image_slide(
        prs,
        "Demo — Uncertainty in Stationary Data (Density / Heatmap)",
        "dashboard3.png",
        caption="Density-based encoding for stationary uncertainty patterns.",
        section="Demo",
    )
    add_title_and_image_slide(
        prs,
        "Demo — Uncertainty in Stationary Data (Heatmap)",
        "dashboard4.png",
        caption="Heatmap encoding for stationary uncertainty patterns.",
        section="Demo",
    )
    add_title_and_image_slide(
        prs,
        "Demo — Walking Data",
        "dashboard5.png",
        caption="Behavior of density/heatmap uncertainty views on walking traces.",
        section="Demo",
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
        section="Wrap-up",
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
        section="Wrap-up",
    )

    # 11) Thanks
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
    _set_slide_background(slide)
    _add_header(slide, prs, "Thank you", section="Q&A")
    box = slide.shapes.add_textbox(GRID["margin_x"], Inches(2.65), prs.slide_width - 2 * GRID["margin_x"], Inches(1.2))
    tf = box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = "Thank you."
    p.font.size = Pt(52)
    p.font.bold = True
    p.font.color.rgb = THEME["navy"]
    p.alignment = PP_ALIGN.CENTER

    # Apply footers (slide numbers) after all slides exist
    total = len(prs.slides)
    for idx, s in enumerate(prs.slides, start=1):
        if idx == 1:
            # Keep title slide clean (no footer)
            continue
        _add_footer(
            s,
            prs,
            left_text="Project #543 — Visualizing Spatio-Temporal Uncertainty",
            right_text=f"{idx}/{total}",
        )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "Project_543_Uncertainty_Visualization.pptx"
    prs.save(str(out_path))
    return out_path


if __name__ == "__main__":
    path = build_presentation()
    print(f"Saved: {path}")

