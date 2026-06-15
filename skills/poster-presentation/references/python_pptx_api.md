# python-pptx API Quick Reference

Key API reference for building conference posters with `python-pptx`.

---

## Installation

```bash
pip install python-pptx Pillow
```

---

## Presentation and Slide Setup

```python
from pptx import Presentation
from pptx.util import Cm, Inches, Pt, Emu

# Create presentation
prs = Presentation()

# Set slide dimensions (A0 landscape)
prs.slide_width  = Cm(118.9)
prs.slide_height = Cm(84.1)

# Add a blank slide (layout index 6 = blank)
slide_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(slide_layout)

# Save
prs.save("poster.pptx")
```

### Unit Conversions

| Unit | Class | Example | Notes |
|------|-------|---------|-------|
| Centimetres | `Cm(n)` | `Cm(10.5)` | Most intuitive for poster dimensions |
| Inches | `Inches(n)` | `Inches(4)` | Common in US |
| Points | `Pt(n)` | `Pt(24)` | Font sizes, line widths |
| EMU (raw) | `Emu(n)` | `Emu(914400)` | 914400 EMU = 1 inch; 360000 EMU = 1 cm |

---

## Shapes

### Rectangle / Filled Box

```python
from pptx.util import Cm
from pptx.dml.color import RGBColor

shape = slide.shapes.add_shape(
    1,           # 1 = rectangle (MSO_SHAPE_TYPE.RECTANGLE)
    Cm(2),       # left
    Cm(3),       # top
    Cm(20),      # width
    Cm(10)       # height
)

# Fill
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0x1A, 0x3A, 0x5C)

# Border
shape.line.color.rgb = RGBColor(0x00, 0x00, 0x00)
shape.line.width = Pt(1.5)

# No border
shape.line.fill.background()
```

### Text Box

```python
from pptx.enum.text import PP_ALIGN

txBox = slide.shapes.add_textbox(Cm(2), Cm(3), Cm(20), Cm(5))
tf = txBox.text_frame
tf.word_wrap = True

# First paragraph
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.CENTER   # LEFT, CENTER, RIGHT, JUSTIFY
run = p.add_run()
run.text = "Section Title"

font = run.font
font.name = "Calibri"
font.size = Pt(32)
font.bold = True
font.italic = False
font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

# Additional paragraphs
p2 = tf.add_paragraph()
p2.alignment = PP_ALIGN.LEFT
run2 = p2.add_run()
run2.text = "Body text content here."
run2.font.size = Pt(20)
```

### Image

```python
pic = slide.shapes.add_picture(
    "figures/result.png",  # file path
    Cm(5),     # left
    Cm(15),    # top
    Cm(30),    # width  — height auto-computed to preserve aspect ratio
)

# Specify both dimensions (may distort if aspect ratio differs)
pic = slide.shapes.add_picture(
    "figures/result.png",
    Cm(5), Cm(15),
    width=Cm(30), height=Cm(20)
)
```

---

## Slide Background

```python
background = slide.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = RGBColor(0xF5, 0xF7, 0xFA)
```

---

## Text Frame Formatting

### Line Spacing

```python
from pptx.oxml.ns import qn
from lxml import etree

p = tf.paragraphs[0]
pPr = p._p.get_or_add_pPr()

# Set line spacing to 1.5× (150%)
lnSpc = etree.SubElement(pPr, qn("a:lnSpc"))
spcPct = etree.SubElement(lnSpc, qn("a:spcPct"))
spcPct.set("val", "150000")  # 100000 = 100%

# OR set exact spacing in points (e.g., 24pt)
lnSpc2 = etree.SubElement(pPr, qn("a:lnSpc"))
spcPts = etree.SubElement(lnSpc2, qn("a:spcPts"))
spcPts.set("val", "2400")    # value = points × 100
```

### Space Before / After Paragraph

```python
pPr = p._p.get_or_add_pPr()

# Space before paragraph (in points × 100)
spcBef = etree.SubElement(pPr, qn("a:spcBef"))
spcPts = etree.SubElement(spcBef, qn("a:spcPts"))
spcPts.set("val", "600")    # 6pt before
```

---

## Colors

```python
from pptx.dml.color import RGBColor

# Specify as hex bytes
color = RGBColor(0x1A, 0x3A, 0x5C)

# From a hex string
def hex_to_rgb(hex_str: str) -> RGBColor:
    hex_str = hex_str.lstrip("#")
    r, g, b = int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)
    return RGBColor(r, g, b)

navy = hex_to_rgb("#1A3A5C")
```

### Common Academic Colors

| Name | Hex | RGBColor |
|------|-----|----------|
| Navy blue | `#1A3A5C` | `RGBColor(0x1A, 0x3A, 0x5C)` |
| Forest green | `#1B4B36` | `RGBColor(0x1B, 0x4B, 0x36)` |
| Crimson | `#8B0000` | `RGBColor(0x8B, 0x00, 0x00)` |
| Deep purple | `#4A148C` | `RGBColor(0x4A, 0x14, 0x8C)` |
| White | `#FFFFFF` | `RGBColor(0xFF, 0xFF, 0xFF)` |
| Light blue bg | `#D6E4F0` | `RGBColor(0xD6, 0xE4, 0xF0)` |
| Off-white bg | `#F5F7FA` | `RGBColor(0xF5, 0xF7, 0xFA)` |
| Dark text | `#1A1A1A` | `RGBColor(0x1A, 0x1A, 0x1A)` |

---

## Shape Z-Order

Shapes are stacked in order of creation (last added = on top). To reorder:

```python
from pptx.oxml.ns import qn

# Move shape to front (last in spTree)
sp_tree = slide.shapes._spTree
sp_tree.append(shape._element)

# Move shape to back (first in spTree, after cNvGrpSpPr and grpSpPr)
sp_tree.insert(2, shape._element)
```

---

## Accessing and Modifying Existing Shapes

```python
# Iterate all shapes on a slide
for shape in slide.shapes:
    print(shape.shape_type, shape.name, shape.left, shape.top)

# Move a shape
shape.left = Cm(10)
shape.top  = Cm(5)

# Resize
shape.width  = Cm(30)
shape.height = Cm(15)
```

---

## Fonts Available on Most Systems

Use these font names (cross-platform safe):

| Preferred | Fallback (Linux/LibreOffice) |
|-----------|------------------------------|
| Calibri | Liberation Sans |
| Times New Roman | Liberation Serif |
| Arial | Liberation Sans |
| Courier New | Liberation Mono |

For scientific posters, **Calibri** (sans-serif) or **Garamond/Times New Roman** (serif) are most common.

---

## python-pptx Version Notes

- Requires python-pptx ≥ 0.6.21
- `Presentation.slide_layouts[6]` is typically the blank layout; verify with:
  ```python
  for i, layout in enumerate(prs.slide_layouts):
      print(i, layout.name)
  ```
- EMU arithmetic: always use `Cm()`, `Inches()`, or `Pt()` helpers; never add raw integers to EMU values.

---

## Useful Links

- Official docs: https://python-pptx.readthedocs.io/
- OOXML spec (ECMA-376): https://www.ecma-international.org/publications-and-standards/standards/ecma-376/
- Issue tracker: https://github.com/scanny/python-pptx/issues
