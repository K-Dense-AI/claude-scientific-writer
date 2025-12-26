# Publication Specifications for Scientific Figures

> Quick reference for journal-specific requirements, export settings, and pre-submission verification.

## Journal Requirements

| Journal | Single Column | Double Column | Max Height | Notes |
|---------|---------------|---------------|------------|-------|
| **Nature** | 89 mm (3.5") | 183 mm (7.2") | 247 mm | Lowercase panel labels (a, b, c) |
| **Science** | 55 mm (2.2") | 175 mm (6.9") | 230 mm | Uppercase panel labels (A, B, C) |
| **Cell** | 85 mm (3.3") | 178 mm (7.0") | 230 mm | Uppercase panel labels |
| **PLOS** | 83 mm | 173 mm | 230 mm | CC-BY license required |
| **PNAS** | 87 mm | 178 mm | 230 mm | Two-column format |

**Quick sizing reference:**
```python
# Common figure sizes (width in inches)
JOURNAL_WIDTHS = {
    'nature_single': 3.5,
    'nature_double': 7.2,
    'science_single': 2.2,
    'science_double': 6.9,
    'cell_single': 3.3,
    'cell_double': 7.0,
}
```

## Resolution Standards

| Figure Type | Minimum DPI | Recommended | Format |
|-------------|-------------|-------------|--------|
| **Line art** (graphs, plots) | 600 | 1200 | Vector (PDF, EPS, SVG) |
| **Combination** (plots + images) | 600 | 600 | Vector or TIFF |
| **Photographs** | 300 | 300-600 | TIFF, PNG |
| **Microscopy images** | 300 | 300-600 | TIFF (no compression) |

**Key principles:**
- **Vector formats** (PDF, EPS, SVG) are resolution-independent and preferred for all plots
- **TIFF** preferred for raster images (lossless compression)
- **PNG** acceptable for web/preprint
- **Never use JPEG** for scientific figures (lossy compression creates artifacts)

## File Formats

| Format | Best For | Advantages | Limitations |
|--------|----------|------------|-------------|
| **PDF** | Plots, figures | Vector, fonts embedded, universal | Larger file size |
| **EPS** | Plots, legacy systems | Vector, widely supported | Older format |
| **SVG** | Web, interactive | Vector, editable | Limited print support |
| **TIFF** | Photos, microscopy | Lossless, print standard | Large files |
| **PNG** | Web/preprint | Lossless, web-compatible | No CMYK support |

**Export workflow:**
1. Create figure at target journal dimensions
2. Use vector format (PDF/EPS) for all plots and diagrams
3. Use TIFF (LZW compression) for photographs
4. Verify fonts are embedded
5. Check final file meets size limits

## Multi-Panel Figures

### Panel Labeling Conventions

- **Position**: Top-left corner of each panel
- **Style**: Bold, sans-serif font
- **Size**: 8-12 pt at final print size
- **Case**: Check journal (Nature = lowercase, most others = uppercase)

### Alignment Best Practices

- Use GridSpec or subplot mosaic for consistent alignment
- Maintain equal margins between panels
- Align related axes where possible
- Use adequate white space (don't cram panels)

**Implementation:**
```python
from string import ascii_uppercase  # or ascii_lowercase for Nature

fig = plt.figure(figsize=(7, 4))
gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.4)

for i, ax in enumerate([ax1, ax2, ax3, ax4]):
    ax.text(-0.15, 1.05, ascii_uppercase[i],
            transform=ax.transAxes,
            fontsize=10, fontweight='bold', va='top')
```

## Pre-Submission Checklist

Before submitting figures to any journal, verify:

### Technical Requirements
- [ ] Resolution meets journal requirements (300+ DPI for raster)
- [ ] File format is correct (vector for plots, TIFF for images)
- [ ] Figure size matches journal column width specifications
- [ ] File size within journal limits

### Typography
- [ ] All text readable at final size (≥6-7 pt minimum)
- [ ] Fonts consistent across all figures in manuscript
- [ ] Sans-serif fonts used (Arial, Helvetica, Calibri)
- [ ] All axes labeled with units in parentheses

### Accessibility
- [ ] Colors are colorblind-friendly (test with simulator)
- [ ] Figure interpretable in grayscale
- [ ] Redundant encoding used (shapes, patterns, not just color)

### Scientific Rigor
- [ ] Error bars present with type defined in caption (SD, SEM, CI)
- [ ] Sample size (n) stated in figure or caption
- [ ] Statistical significance markers clearly labeled (*, **, ***)
- [ ] Individual data points shown when feasible

### Visual Quality
- [ ] Panel labels present and consistent (A, B, C or a, b, c)
- [ ] No chart junk (unnecessary gridlines, 3D effects, shadows)
- [ ] Legend clear and complete
- [ ] No truncated axes unless scientifically justified

## Common Pitfalls

Avoid these 10 most frequent publication figure issues:

1. **Font too small** — Text unreadable when printed at final column width
2. **JPEG format** — Creates artifacts in graphs; use PDF, PNG, or TIFF
3. **Red-green reliance** — ~8% of males cannot distinguish; use Okabe-Ito palette
4. **Low resolution** — Pixelated figures; verify DPI before export
5. **Missing units** — All axes must include units in parentheses
6. **3D effects** — Distorts perception; always use 2D representations
7. **Chart junk** — Remove unnecessary gridlines, borders, decorations
8. **Truncated axes** — Bar charts should start at zero unless scientifically justified
9. **Inconsistent styling** — Different fonts/colors across figures in same manuscript
10. **No error bars** — Always show uncertainty; specify type in caption

## Workflow Summary

**Recommended workflow for publication figures:**

1. **Plan** — Determine target journal, figure type, and key message
2. **Configure** — Apply journal-specific style (dimensions, fonts, colors)
3. **Create** — Build figure with proper labels, colorblind-safe colors, statistics
4. **Verify** — Check size, fonts, colors, accessibility using checklist above
5. **Export** — Save in required formats with correct DPI
6. **Review** — View at actual print size in manuscript context

**Quick configuration:**
```python
# Example: Configure for Nature single-column figure
fig, ax = plt.subplots(figsize=(3.5, 2.5))  # 89mm width
plt.rcParams['font.size'] = 8
plt.rcParams['font.family'] = 'sans-serif'

# After creating figure, export
fig.savefig('figure1.pdf', dpi=300, bbox_inches='tight')
fig.savefig('figure1.png', dpi=300, bbox_inches='tight')
```

---

*See [visual-design SKILL.md](../SKILL.md) for design philosophy and [plotting-libraries](../../plotting-libraries/SKILL.md) for implementation code.*
