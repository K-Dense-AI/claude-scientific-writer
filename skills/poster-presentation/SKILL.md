---
name: poster-presentation
description: Create scientific conference posters as .pptx files using python-pptx. Handles A0/A1 layouts, section placement, figure insertion, and academic color schemes. Exports editable .pptx and PDF.
tools: Read, Write, Bash
version: "1.0.0"
---

# Scientific Conference Poster — PowerPoint (.pptx)

## Overview

This skill creates professional scientific conference posters as editable PowerPoint (.pptx) files using `python-pptx`. It supports standard conference poster sizes (A0, A1), landscape and portrait orientations, structured academic sections, figure insertion with captions, and publication-quality academic color schemes.

The generated `.pptx` is fully editable, allowing researchers to fine-tune layout, fonts, and colors using Microsoft PowerPoint, LibreOffice Impress, or any compatible application. PDF export is available via LibreOffice or PowerPoint.

---

## When to Use This Skill

Use this skill when:
- Creating a poster for an academic conference, symposium, or workshop
- Converting a research paper or manuscript into poster format
- Building a poster template for a research group or institution
- Presenting preliminary results, thesis work, or funded project outcomes
- Needing an editable (non-PDF) poster that collaborators can update

**Trigger phrases:**
- "Create a conference poster as a PowerPoint / .pptx"
- "Make me a scientific poster I can edit in PowerPoint"
- "Generate a poster for my paper / conference / symposium"
- "Build an A0 / A1 poster for [conference name]"
- "Create a research poster with sections for methods, results, conclusions"

---

## Prerequisites

Install required Python packages before running any poster generation code:

```bash
pip install python-pptx Pillow
```

For PDF export from the command line:

```bash
# macOS (via Homebrew)
brew install --cask libreoffice

# Ubuntu / Debian
sudo apt-get install libreoffice

# Windows — download from https://www.libreoffice.org/
```

---

## Standard Poster Dimensions

| Format   | Orientation | Width (cm) | Height (cm) | Width (in) | Height (in) | Common use          |
|----------|-------------|------------|-------------|------------|-------------|---------------------|
| A0       | Portrait    | 84.1       | 118.9       | 33.11      | 46.81       | European conferences|
| A0       | Landscape   | 118.9      | 84.1        | 46.81      | 33.11       | US / mixed format   |
| A1       | Portrait    | 59.4       | 84.1        | 23.39      | 33.11       | Smaller venues      |
| A1       | Landscape   | 84.1       | 59.4        | 33.11      | 23.39       | Departmental events |
| 36×48 in | Portrait    | 91.44      | 121.92      | 36.0       | 48.0        | US conferences      |
| 48×36 in | Landscape   | 121.92     | 91.44       | 48.0       | 36.0        | US conferences      |

**python-pptx uses EMUs (English Metric Units): 1 inch = 914400 EMU, 1 cm = 360000 EMU**

---

## Workflow Phases

### Phase 1: Gather Content

Collect all poster content from the user or source document:

1. **Title** — full paper/poster title
2. **Authors** — list with superscript affiliation numbers
3. **Affiliations** — institution names linked to authors
4. **Contact / corresponding author** email
5. **Abstract** — 150–250 words
6. **Introduction / Background** — key context and motivation (3–5 bullet points or short paragraphs)
7. **Methods** — concise description with optional workflow figure
8. **Results** — key findings, data visualizations, tables
9. **Conclusions** — 4–6 bullet points
10. **Acknowledgements** — funding sources, collaborators
11. **References** — 5–10 key references (abbreviated format)
12. **Figures** — file paths to images/plots to embed
13. **Logo(s)** — institutional/conference logo paths
14. **Color scheme** — preferred colors or institution palette (see schemes below)

### Phase 2: Plan Layout

Standard two- or three-column academic poster layout:

```
┌──────────────────────────────────────────────────────────┐
│  LOGO  │           TITLE / AUTHORS / AFFILIATIONS         │  LOGO │
├─────────────────┬────────────────┬────────────────────────┤
│  Introduction   │   Methods      │   Results              │
│                 │                │                        │
│  Background     │   Workflow     │   Figure 1             │
│                 │   Figure       │                        │
├─────────────────┴────────────────┤   Figure 2             │
│  [Optional middle spanning row]  │                        │
├─────────────────┬────────────────┼────────────────────────┤
│  Conclusions    │ Acknowledgements│  References            │
└─────────────────┴────────────────┴────────────────────────┘
```

### Phase 3: Generate .pptx

Use the code templates below to build the poster programmatically.

### Phase 4: Export

- Save as `.pptx` (primary deliverable — fully editable)
- Export to PDF via LibreOffice or PowerPoint (see export section)
- Verify layout at 100% zoom before delivering

---

## Core Code: Poster Foundation

```python
"""
scientific_poster.py — Generate A0 landscape conference poster as .pptx
Requires: python-pptx, Pillow
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import os


# ── Dimensions ────────────────────────────────────────────────────────────────
# A0 Landscape: 118.9 cm × 84.1 cm
POSTER_WIDTH_CM  = 118.9
POSTER_HEIGHT_CM = 84.1

def cm(value):
    """Convert centimetres to EMUs."""
    return Cm(value)


def create_poster(output_path: str = "poster.pptx") -> Presentation:
    """Create and return a blank poster Presentation at A0 landscape size."""
    prs = Presentation()
    prs.slide_width  = cm(POSTER_WIDTH_CM)
    prs.slide_height = cm(POSTER_HEIGHT_CM)

    # Remove all default placeholder layouts — use blank slide
    slide_layout = prs.slide_layouts[6]  # index 6 = blank
    slide = prs.slides.add_slide(slide_layout)

    return prs, slide
```

---

## Academic Color Schemes

```python
# ── Color Palettes ────────────────────────────────────────────────────────────

SCHEMES = {
    "classic_blue": {
        "header_bg":    RGBColor(0x1A, 0x3A, 0x5C),   # dark navy
        "header_text":  RGBColor(0xFF, 0xFF, 0xFF),   # white
        "section_bg":   RGBColor(0xD6, 0xE4, 0xF0),   # light blue
        "section_header": RGBColor(0x1A, 0x3A, 0x5C),
        "body_text":    RGBColor(0x1A, 0x1A, 0x1A),
        "accent":       RGBColor(0xE8, 0x8A, 0x00),   # amber
        "background":   RGBColor(0xF5, 0xF7, 0xFA),
    },
    "green_academic": {
        "header_bg":    RGBColor(0x1B, 0x4B, 0x36),   # forest green
        "header_text":  RGBColor(0xFF, 0xFF, 0xFF),
        "section_bg":   RGBColor(0xD8, 0xED, 0xE3),   # light green
        "section_header": RGBColor(0x1B, 0x4B, 0x36),
        "body_text":    RGBColor(0x1A, 0x1A, 0x1A),
        "accent":       RGBColor(0xC0, 0x39, 0x2B),   # red
        "background":   RGBColor(0xF4, 0xF9, 0xF6),
    },
    "crimson_grey": {
        "header_bg":    RGBColor(0x8B, 0x00, 0x00),   # crimson
        "header_text":  RGBColor(0xFF, 0xFF, 0xFF),
        "section_bg":   RGBColor(0xF0, 0xE8, 0xE8),   # blush
        "section_header": RGBColor(0x8B, 0x00, 0x00),
        "body_text":    RGBColor(0x1A, 0x1A, 0x1A),
        "accent":       RGBColor(0x2C, 0x3E, 0x50),   # slate
        "background":   RGBColor(0xFA, 0xF9, 0xF9),
    },
    "purple_modern": {
        "header_bg":    RGBColor(0x4A, 0x14, 0x8C),   # deep purple
        "header_text":  RGBColor(0xFF, 0xFF, 0xFF),
        "section_bg":   RGBColor(0xED, 0xE7, 0xF6),   # lavender
        "section_header": RGBColor(0x4A, 0x14, 0x8C),
        "body_text":    RGBColor(0x1A, 0x1A, 0x1A),
        "accent":       RGBColor(0xF5, 0x7C, 0x00),   # orange
        "background":   RGBColor(0xFA, 0xF8, 0xFF),
    },
    "monochrome": {
        "header_bg":    RGBColor(0x21, 0x21, 0x21),
        "header_text":  RGBColor(0xFF, 0xFF, 0xFF),
        "section_bg":   RGBColor(0xEE, 0xEE, 0xEE),
        "section_header": RGBColor(0x21, 0x21, 0x21),
        "body_text":    RGBColor(0x1A, 0x1A, 0x1A),
        "accent":       RGBColor(0x75, 0x75, 0x75),
        "background":   RGBColor(0xFF, 0xFF, 0xFF),
    },
}

DEFAULT_SCHEME = "classic_blue"
```

---

## Helper Functions

```python
# ── Drawing helpers ────────────────────────────────────────────────────────────

from pptx.oxml.ns import qn
from lxml import etree


def set_background_color(slide, color: RGBColor):
    """Fill the slide background with a solid color."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_filled_rectangle(slide, left, top, width, height,
                          fill_color: RGBColor, line_color=None, line_width_pt=0):
    """Add a solid filled rectangle shape (used for section boxes and header)."""
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color

    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(line_width_pt)
    else:
        shape.line.fill.background()  # no border

    return shape


def add_textbox(slide, left, top, width, height, text: str,
                font_size: int, font_color: RGBColor,
                bold=False, italic=False, alignment=PP_ALIGN.LEFT,
                word_wrap=True, font_name="Calibri"):
    """Add a text box with specified formatting."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = word_wrap

    p = tf.paragraphs[0]
    p.alignment = alignment
    run = p.add_run()
    run.text = text

    font = run.font
    font.name = font_name
    font.size = Pt(font_size)
    font.color.rgb = font_color
    font.bold = bold
    font.italic = italic

    return txBox


def add_multiline_textbox(slide, left, top, width, height, lines: list,
                           font_size: int, font_color: RGBColor,
                           bold_first=False, font_name="Calibri",
                           bullet=False, line_spacing_pt=None):
    """
    Add a text box with multiple paragraphs (one per item in `lines`).
    If bullet=True, prepends '• ' to each line.
    """
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True

    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()

        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        prefix = "• " if bullet else ""
        run.text = prefix + line

        font = run.font
        font.name = font_name
        font.size = Pt(font_size)
        font.color.rgb = font_color
        font.bold = (bold_first and i == 0)

        if line_spacing_pt:
            from pptx.util import Pt as pPt
            from pptx.oxml.ns import qn
            pPr = p._pPr
            if pPr is None:
                pPr = p._p.get_or_add_pPr()
            lnSpc = etree.SubElement(pPr, qn("a:lnSpc"))
            spcPts = etree.SubElement(lnSpc, qn("a:spcPts"))
            spcPts.set("val", str(int(line_spacing_pt * 100)))

    return txBox


def add_image(slide, image_path: str, left, top, width, height=None):
    """
    Insert an image at the specified position.
    If height is None, python-pptx preserves the aspect ratio.
    """
    if not os.path.exists(image_path):
        print(f"[WARNING] Image not found: {image_path} — skipping.")
        return None

    if height is None:
        pic = slide.shapes.add_picture(image_path, left, top, width=width)
    else:
        pic = slide.shapes.add_picture(image_path, left, top, width, height)

    return pic


def add_section_header(slide, left, top, width, height,
                        title: str, scheme: dict, font_size=24):
    """Draw a colored section header bar with white text."""
    add_filled_rectangle(slide, left, top, width, height,
                         fill_color=scheme["section_header"])
    add_textbox(slide, left + Cm(0.3), top, width - Cm(0.3), height,
                text=title,
                font_size=font_size,
                font_color=scheme["header_text"],
                bold=True,
                alignment=PP_ALIGN.LEFT)
```

---

## Poster Header Section

```python
def build_header(slide, scheme: dict,
                 title: str,
                 authors: str,
                 affiliations: str,
                 logo_left_path: str = None,
                 logo_right_path: str = None,
                 poster_width_cm: float = POSTER_WIDTH_CM):
    """
    Build the full-width header: logos on left/right, title/authors/affiliations centre.
    Header height = ~15% of poster height.
    """
    HEADER_HEIGHT = cm(12)
    LOGO_WIDTH    = cm(12)
    PADDING       = cm(1)

    # Background bar
    add_filled_rectangle(slide,
                         left=cm(0), top=cm(0),
                         width=cm(poster_width_cm), height=HEADER_HEIGHT,
                         fill_color=scheme["header_bg"])

    # Left logo
    if logo_left_path and os.path.exists(logo_left_path):
        add_image(slide, logo_left_path,
                  left=PADDING, top=cm(1),
                  width=LOGO_WIDTH, height=cm(10))

    # Right logo
    if logo_right_path and os.path.exists(logo_right_path):
        add_image(slide, logo_right_path,
                  left=cm(poster_width_cm) - LOGO_WIDTH - PADDING,
                  top=cm(1),
                  width=LOGO_WIDTH, height=cm(10))

    # Title — centered
    text_left  = LOGO_WIDTH + PADDING * 2
    text_width = cm(poster_width_cm) - (LOGO_WIDTH + PADDING) * 2

    add_textbox(slide,
                left=text_left, top=cm(1),
                width=text_width, height=cm(5),
                text=title,
                font_size=52,
                font_color=scheme["header_text"],
                bold=True,
                alignment=PP_ALIGN.CENTER)

    add_textbox(slide,
                left=text_left, top=cm(6),
                width=text_width, height=cm(2.5),
                text=authors,
                font_size=28,
                font_color=scheme["header_text"],
                bold=False,
                alignment=PP_ALIGN.CENTER)

    add_textbox(slide,
                left=text_left, top=cm(8.5),
                width=text_width, height=cm(2),
                text=affiliations,
                font_size=22,
                font_color=scheme["header_text"],
                italic=True,
                alignment=PP_ALIGN.CENTER)
```

---

## Section Building Blocks

```python
def build_text_section(slide, left, top, width, height,
                        section_title: str,
                        content_lines: list,
                        scheme: dict,
                        header_height_cm: float = 2.0,
                        font_size: int = 20,
                        bullet: bool = True):
    """
    Draw a complete section box: colored header + white body with text lines.
    """
    HDR = cm(header_height_cm)

    # Section background
    add_filled_rectangle(slide, left, top, width, height,
                         fill_color=scheme["section_bg"],
                         line_color=scheme["section_header"],
                         line_width_pt=1.5)

    # Section header bar
    add_section_header(slide, left, top, width, HDR,
                       title=section_title, scheme=scheme)

    # Body text
    add_multiline_textbox(slide,
                          left=left + cm(0.5),
                          top=top + HDR + cm(0.3),
                          width=width - cm(1),
                          height=height - HDR - cm(0.5),
                          lines=content_lines,
                          font_size=font_size,
                          font_color=scheme["body_text"],
                          bullet=bullet)


def build_figure_section(slide, left, top, width, height,
                          section_title: str,
                          image_path: str,
                          caption: str,
                          scheme: dict,
                          header_height_cm: float = 2.0,
                          caption_height_cm: float = 2.5):
    """
    Draw a section box containing a figure + caption below it.
    """
    HDR     = cm(header_height_cm)
    CAPTION = cm(caption_height_cm)
    PAD     = cm(0.4)

    # Background
    add_filled_rectangle(slide, left, top, width, height,
                         fill_color=scheme["section_bg"],
                         line_color=scheme["section_header"],
                         line_width_pt=1.5)

    # Header
    add_section_header(slide, left, top, width, HDR,
                       title=section_title, scheme=scheme)

    # Image area
    img_top    = top + HDR + PAD
    img_height = height - HDR - CAPTION - PAD * 2

    if image_path:
        add_image(slide, image_path,
                  left=left + PAD,
                  top=img_top,
                  width=width - PAD * 2,
                  height=img_height)
    else:
        # Placeholder grey box when no image provided
        add_filled_rectangle(slide,
                             left=left + PAD, top=img_top,
                             width=width - PAD * 2, height=img_height,
                             fill_color=RGBColor(0xCC, 0xCC, 0xCC))

    # Caption
    add_textbox(slide,
                left=left + PAD,
                top=top + HDR + PAD + img_height,
                width=width - PAD * 2,
                height=CAPTION,
                text=caption,
                font_size=18,
                font_color=scheme["body_text"],
                italic=True,
                alignment=PP_ALIGN.CENTER)
```

---

## Full Poster Assembly — Three-Column A0 Landscape

```python
def build_a0_landscape_poster(
    title: str,
    authors: str,
    affiliations: str,
    abstract_lines: list,
    intro_lines: list,
    methods_lines: list,
    results_lines: list,
    conclusions_lines: list,
    acknowledgements: str,
    references_lines: list,
    figure1_path: str = None,
    figure1_caption: str = "Figure 1.",
    figure2_path: str = None,
    figure2_caption: str = "Figure 2.",
    methods_figure_path: str = None,
    methods_figure_caption: str = "Workflow.",
    logo_left: str = None,
    logo_right: str = None,
    color_scheme: str = "classic_blue",
    output_path: str = "poster.pptx"
):
    """
    Build a complete three-column A0 landscape scientific poster.

    Layout (all measurements in cm from top-left origin):
      Header:  full width, 0–12 cm
      Column 1 (left):   0–38 cm wide,  12–82 cm tall
      Column 2 (middle): 40–78 cm wide, 12–82 cm tall
      Column 3 (right):  80–118 cm wide, 12–82 cm tall
      Footer:  full width, 82–84.1 cm
    """
    scheme = SCHEMES.get(color_scheme, SCHEMES[DEFAULT_SCHEME])
    prs, slide = create_poster(output_path)

    # Poster background
    set_background_color(slide, scheme["background"])

    # ── HEADER ──────────────────────────────────────────────────────────────
    build_header(slide, scheme,
                 title=title, authors=authors, affiliations=affiliations,
                 logo_left_path=logo_left, logo_right_path=logo_right)

    # ── LAYOUT CONSTANTS ────────────────────────────────────────────────────
    COL_TOP    = cm(12.5)
    COL_BOTTOM = cm(82)
    COL_HEIGHT = COL_BOTTOM - COL_TOP
    GAP        = cm(1.5)

    C1_LEFT  = cm(1)
    C1_WIDTH = cm(37)
    C2_LEFT  = C1_LEFT + C1_WIDTH + GAP
    C2_WIDTH = cm(37)
    C3_LEFT  = C2_LEFT + C2_WIDTH + GAP
    C3_WIDTH = cm(POSTER_WIDTH_CM) - C3_LEFT - cm(1)

    # ── COLUMN 1: Abstract + Introduction ───────────────────────────────────
    ABSTRACT_H = cm(22)
    build_text_section(slide,
                       left=C1_LEFT, top=COL_TOP,
                       width=C1_WIDTH, height=ABSTRACT_H,
                       section_title="Abstract",
                       content_lines=abstract_lines,
                       scheme=scheme, bullet=False, font_size=19)

    INTRO_H = COL_HEIGHT - ABSTRACT_H - GAP
    build_text_section(slide,
                       left=C1_LEFT, top=COL_TOP + ABSTRACT_H + GAP,
                       width=C1_WIDTH, height=INTRO_H,
                       section_title="Introduction & Background",
                       content_lines=intro_lines,
                       scheme=scheme, bullet=True, font_size=20)

    # ── COLUMN 2: Methods + Methods Figure ──────────────────────────────────
    METHODS_TEXT_H  = cm(28)
    METHODS_FIG_H   = COL_HEIGHT - METHODS_TEXT_H - GAP

    build_text_section(slide,
                       left=C2_LEFT, top=COL_TOP,
                       width=C2_WIDTH, height=METHODS_TEXT_H,
                       section_title="Methods",
                       content_lines=methods_lines,
                       scheme=scheme, bullet=True, font_size=20)

    build_figure_section(slide,
                          left=C2_LEFT,
                          top=COL_TOP + METHODS_TEXT_H + GAP,
                          width=C2_WIDTH, height=METHODS_FIG_H,
                          section_title="Workflow",
                          image_path=methods_figure_path,
                          caption=methods_figure_caption,
                          scheme=scheme)

    # ── COLUMN 3: Results (2 figures) + Conclusions ─────────────────────────
    FIG1_H        = cm(26)
    FIG2_H        = cm(22)
    CONCLUSIONS_H = COL_HEIGHT - FIG1_H - FIG2_H - GAP * 2

    build_figure_section(slide,
                          left=C3_LEFT, top=COL_TOP,
                          width=C3_WIDTH, height=FIG1_H,
                          section_title="Results",
                          image_path=figure1_path,
                          caption=figure1_caption,
                          scheme=scheme)

    build_figure_section(slide,
                          left=C3_LEFT, top=COL_TOP + FIG1_H + GAP,
                          width=C3_WIDTH, height=FIG2_H,
                          section_title="",
                          image_path=figure2_path,
                          caption=figure2_caption,
                          scheme=scheme)

    build_text_section(slide,
                       left=C3_LEFT,
                       top=COL_TOP + FIG1_H + FIG2_H + GAP * 2,
                       width=C3_WIDTH, height=CONCLUSIONS_H,
                       section_title="Conclusions",
                       content_lines=conclusions_lines,
                       scheme=scheme, bullet=True, font_size=20)

    # ── FOOTER: Acknowledgements + References ───────────────────────────────
    FOOTER_TOP = cm(82.5)
    FOOTER_H   = cm(POSTER_HEIGHT_CM) - FOOTER_TOP
    HALF_W     = (cm(POSTER_WIDTH_CM) - cm(2)) / 2

    build_text_section(slide,
                       left=cm(1), top=FOOTER_TOP,
                       width=HALF_W, height=FOOTER_H,
                       section_title="Acknowledgements",
                       content_lines=[acknowledgements],
                       scheme=scheme, bullet=False, font_size=16)

    build_text_section(slide,
                       left=cm(1) + HALF_W + GAP, top=FOOTER_TOP,
                       width=HALF_W - GAP, height=FOOTER_H,
                       section_title="References",
                       content_lines=references_lines,
                       scheme=scheme, bullet=False, font_size=15)

    # ── SAVE ────────────────────────────────────────────────────────────────
    prs.save(output_path)
    print(f"[OK] Poster saved: {output_path}")
    return output_path
```

---

## Example Usage

```python
if __name__ == "__main__":
    build_a0_landscape_poster(
        title="Deep Learning for Early Detection of Alzheimer's Disease\nUsing Multimodal Neuroimaging",
        authors="J. Smith¹, A. Patel², R. Müller¹, L. Chen³",
        affiliations="¹Dept. of Neuroscience, University of Example | ²Brain Imaging Centre, City Hospital | ³ML Lab, Tech Institute",

        abstract_lines=[
            "Alzheimer's disease (AD) affects over 55 million people worldwide. "
            "Early and accurate diagnosis remains a significant clinical challenge. "
            "We present a multimodal deep learning framework integrating structural MRI, "
            "FDG-PET, and cerebrospinal fluid biomarkers to improve early AD detection. "
            "Our model achieves 94.2% accuracy on the ADNI dataset, outperforming "
            "unimodal baselines by 8.3 percentage points. These results suggest "
            "multimodal fusion substantially improves pre-clinical AD diagnosis."
        ],

        intro_lines=[
            "Alzheimer's disease is the leading cause of dementia, with costs exceeding $300B/year in the US alone.",
            "Current diagnostic methods rely on late-stage symptom presentation, missing the critical early treatment window.",
            "Neuroimaging biomarkers (MRI atrophy, PET hypometabolism) show promise but are typically analysed in isolation.",
            "Deep learning enables automated feature extraction from high-dimensional neuroimaging data.",
            "We hypothesise that multimodal fusion will significantly outperform single-modality approaches for early AD classification.",
        ],

        methods_lines=[
            "Dataset: 1,200 subjects from ADNI (400 CN, 400 MCI, 400 AD).",
            "Modalities: T1-weighted MRI (3T), FDG-PET, CSF Aβ42/tau ratios.",
            "Preprocessing: FreeSurfer cortical parcellation, SPM12 PET normalisation.",
            "Architecture: Three-stream CNN encoders with cross-modal attention fusion.",
            "Training: 5-fold cross-validation, AdamW optimiser, cosine LR schedule.",
            "Evaluation: Accuracy, AUC-ROC, sensitivity/specificity for CN vs. MCI vs. AD.",
        ],

        results_lines=[
            "94.2% overall accuracy (vs. 86.1% MRI-only baseline).",
            "AUC-ROC: 0.97 for AD vs. CN; 0.89 for MCI vs. CN.",
            "Cross-modal attention identified hippocampus, entorhinal cortex, and precuneus as most predictive.",
            "Model generalises across APOE-ε4 carrier subgroups (p > 0.05 for subgroup differences).",
        ],

        conclusions_lines=[
            "Multimodal deep learning significantly improves early AD detection over single-modality approaches.",
            "Cross-modal attention provides interpretable biomarker importance maps consistent with known AD pathology.",
            "The framework is scanner-agnostic and generalises across genetic risk subgroups.",
            "Future work: longitudinal modelling, external validation, prospective clinical study.",
        ],

        acknowledgements="Funded by NIH R01-AG012345 and the Alzheimer's Association Research Grant #AARG-22-000123. "
                         "Data provided by the Alzheimer's Disease Neuroimaging Initiative (ADNI). "
                         "Computing resources from the National Center for Supercomputing Applications.",

        references_lines=[
            "[1] Jack et al. (2018). NIA-AA Research Framework. Alzheimer's & Dementia, 14, 535–562.",
            "[2] Litjens et al. (2017). A survey on deep learning in medical image analysis. Med. Im. Analysis, 42, 60–88.",
            "[3] Ngiam et al. (2011). Multimodal deep learning. ICML 2011.",
            "[4] Zhang et al. (2022). Multimodal neuroimaging fusion for AD. NeuroImage, 249, 118907.",
            "[5] Petersen et al. (2014). ADNI: 10 years. Arch Neurol, 71, 806–813.",
        ],

        figure1_path="figures/roc_curves.png",
        figure1_caption="Figure 1. ROC curves for AD vs. CN (AUC = 0.97), MCI vs. CN (AUC = 0.89), and AD vs. MCI (AUC = 0.91).",
        figure2_path="figures/attention_map.png",
        figure2_caption="Figure 2. Cross-modal attention heatmaps overlaid on MRI showing hippocampal and entorhinal activation.",
        methods_figure_path="figures/architecture.png",
        methods_figure_caption="Figure 3. Three-stream CNN architecture with cross-modal attention fusion module.",

        logo_left="logos/university_logo.png",
        logo_right="logos/funder_logo.png",
        color_scheme="classic_blue",
        output_path="poster_ad_multimodal.pptx"
    )
```

---

## Portrait Poster (A0 / A1)

For portrait orientation, adjust dimensions and use a two-column layout:

```python
# A0 Portrait: 84.1 cm × 118.9 cm
def create_portrait_poster(output_path="poster_portrait.pptx"):
    prs = Presentation()
    prs.slide_width  = Cm(84.1)
    prs.slide_height = Cm(118.9)
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    return prs, slide

# A1 Landscape: 84.1 cm × 59.4 cm
def create_a1_landscape(output_path="poster_a1.pptx"):
    prs = Presentation()
    prs.slide_width  = Cm(84.1)
    prs.slide_height = Cm(59.4)
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    return prs, slide
```

---

## PDF Export

### Via LibreOffice (command line — cross-platform)

```bash
# Export .pptx to PDF using LibreOffice headless mode
libreoffice --headless --convert-to pdf poster_ad_multimodal.pptx --outdir ./

# Or specify output directory
libreoffice --headless --convert-to pdf:impress_pdf_Export poster.pptx --outdir output/
```

### Via Python subprocess

```python
import subprocess
import os

def export_to_pdf(pptx_path: str, output_dir: str = ".") -> str:
    """Convert .pptx to PDF using LibreOffice."""
    os.makedirs(output_dir, exist_ok=True)
    result = subprocess.run(
        ["libreoffice", "--headless", "--convert-to", "pdf",
         pptx_path, "--outdir", output_dir],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"LibreOffice conversion failed:\n{result.stderr}")

    pdf_name = os.path.splitext(os.path.basename(pptx_path))[0] + ".pdf"
    pdf_path = os.path.join(output_dir, pdf_name)
    print(f"[OK] PDF exported: {pdf_path}")
    return pdf_path
```

---

## Verification Checklist

Before delivering the poster:

- [ ] Title, authors, affiliations render correctly in header
- [ ] All sections have content (no empty boxes)
- [ ] All referenced image files exist and load without warnings
- [ ] Text is not clipped or overflowing section boxes (check at 100% zoom)
- [ ] Font sizes are legible at the target print size (≥18pt for body, ≥24pt for section headers)
- [ ] Color scheme is consistent throughout
- [ ] .pptx opens correctly in both PowerPoint and LibreOffice
- [ ] PDF export renders without distortion

---

## Common Issues and Fixes

| Problem | Likely cause | Fix |
|---------|-------------|-----|
| Text overflows section box | Font size too large / too many lines | Reduce font size or split into two sections |
| Image not inserted | File path wrong or file missing | Check `os.path.exists(path)` before calling `add_image` |
| Wrong poster size | `slide_width`/`slide_height` set in inches, not EMUs | Use `Cm()` or `Inches()` wrappers, not raw integers |
| Logo appears stretched | Width and height both specified with wrong aspect ratio | Set only `width=` and let python-pptx auto-compute height |
| PDF looks different from .pptx | Font not installed on LibreOffice machine | Embed fonts or use system fonts (Calibri → Liberation Sans) |
| Columns misaligned | Arithmetic error in column left/width calculations | Print all `left`, `top`, `width`, `height` values and verify sum |

---

## Integration with Scientific Schematics

For high-quality figures to embed in the poster, use the `scientific-schematics` skill before generating the poster:

```bash
# Generate workflow diagram for Methods section
python scripts/generate_schematic.py \
  "Three-stream CNN architecture: MRI encoder, PET encoder, CSF encoder feeding into cross-modal attention fusion with final classification layer" \
  -o figures/architecture.png

# Generate results figure
python scripts/generate_schematic.py \
  "ROC curves for three-class neuroimaging classification showing AD vs CN AUC 0.97, MCI vs CN AUC 0.89" \
  -o figures/roc_curves.png
```

Then pass the generated file paths as `figure1_path`, `figure2_path`, or `methods_figure_path` arguments to the poster builder.

---

## File Naming Conventions

```
posters/
└── YYYYMMDD_<short_title>/
    ├── poster.pptx          # Primary deliverable
    ├── poster.pdf           # PDF export
    ├── generate_poster.py   # Generation script (reproducible)
    └── figures/             # Embedded images
        ├── fig1_results.png
        ├── fig2_attention.png
        └── fig3_architecture.png
```
