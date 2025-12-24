---
name: visual-design
description: Create distinctive, publication-quality scientific visuals with high design quality. Use this skill when creating figures, charts, infographics, report illustrations, posters, or presentation slides. Generates polished visuals that avoid generic defaults and communicate science effectively.
license: Internal use - Oligon brand standards apply
---

This skill guides creation of distinctive, publication-quality scientific visuals that avoid generic "default matplotlib" aesthetics. Apply intentional design thinking to every visual output.

The user provides visualization requirements: a figure, chart, infographic, poster, or presentation to create. They may include context about the audience, publication venue, or technical constraints.

## Design Thinking

Before creating visuals, understand the context and commit to a clear aesthetic direction:

- **Story**: What single insight should the viewer take away? Every visual tells one story.
- **Audience**: Journal reviewers (precise, restrained)? Conference attendees (bold, scannable)? Internal team (functional, clear)? General public (accessible, engaging)?
- **Constraints**: Journal figure specs, color count limits, file format requirements, accessibility needs, brand guidelines.
- **Differentiation**: What makes this visual memorable? What element will someone recall tomorrow?

**CRITICAL**: Choose a clear visual direction and execute it with precision. Scientific visuals can be bold OR restrained - the key is intentionality. A striking conference poster and an elegant journal figure both succeed through deliberate choices.

## Output Formats

This skill applies to:

| Output | Tools | Typical Use |
|--------|-------|-------------|
| **Figures** | matplotlib, seaborn, plotly, SVG | Journal papers, reports |
| **Infographics** | SVG, Illustrator-ready output | Summaries, educational content |
| **Report illustrations** | ReportLab, PDF components | Internal reports, branded documents |
| **Presentations** | PPTX (python-pptx), Beamer/LaTeX | Talks, seminars, conferences |
| **Posters** | LaTeX (tikzposter, beamerposter), PPTX | Conference presentations |

## Visual Design Principles

### Typography

Scientific visuals demand legible, professional typography:

**Hierarchy matters:**
- **Titles**: Bold, larger, establish context immediately
- **Axis labels**: Clear, readable at final reproduction size
- **Annotations**: Smaller but never sacrificed for aesthetics
- **Legends**: Positioned to not obscure data

**Font selection:**
- Use Oligon brand fonts when available (see brand standards)
- For figures: sans-serif for labels (Helvetica, Arial, Source Sans Pro)
- For posters/slides: pair a distinctive display font with a clean body font
- **Test at final size**: A beautiful font that's illegible at 8pt fails

**Anti-patterns to avoid:**
- Default matplotlib fonts without customization
- Inconsistent font sizes across panels
- Decorative fonts that sacrifice legibility
- ALL CAPS for long text strings

### Color

Color communicates data and establishes visual identity:

**Brand integration:**
- Use Oligon color palette as the foundation (see `BRAND_COLORS_v4.md`)
- Primary colors for main data series
- Accent colors for highlights and callouts
- Neutral palette for backgrounds, axes, gridlines

**Data visualization principles:**
- Sequential palettes for continuous data (light→dark)
- Diverging palettes for data with meaningful center (e.g., fold change)
- Categorical palettes for discrete groups (max 7-8 distinguishable colors)
- **Always check colorblind accessibility** (use colorblind-safe palettes)

**Color hierarchy:**
- Dominant color draws attention to the key insight
- Supporting colors provide context without competing
- Background colors create depth without distraction

**Anti-patterns to avoid:**
- Rainbow colormaps for sequential data (perceptually uneven)
- Too many colors competing for attention
- Pure black on pure white (harsh; use soft blacks like #1a1a1a)
- Colors that clash with brand identity

### Composition & Layout

Spatial arrangement guides the viewer's eye:

**Visual hierarchy:**
- Most important element gets most visual weight (size, color, position)
- Guide the eye: top-left → bottom-right (Western reading order)
- Group related elements; separate distinct concepts with whitespace

**Figure panels:**
- Consistent sizing across multi-panel figures
- Aligned axes when comparing related data
- Clear panel labels (A, B, C or descriptive titles)
- Shared legends when appropriate to reduce redundancy

**Whitespace:**
- Generous margins prevent cramped appearance
- Space between elements creates visual breathing room
- Don't fill every pixel - emptiness is a design choice

**Posters and slides:**
- Scannable in 3 seconds: title → key figure → conclusion
- Limit text density; visuals carry the message
- Create visual flow that guides through the narrative

**Anti-patterns to avoid:**
- Cramming too much into one figure
- Misaligned elements across panels
- Inconsistent spacing
- Text-heavy slides that could be a document

### Data Visualization Best Practices

**Chart selection:**
| Data Type | Recommended | Avoid |
|-----------|-------------|-------|
| Comparison (few categories) | Bar chart, dot plot | Pie chart (hard to compare) |
| Comparison (many categories) | Horizontal bar, heatmap | 3D charts |
| Time series | Line chart, area chart | Bar charts (implies discrete) |
| Distribution | Histogram, violin, box plot | Bar chart of means only |
| Relationship | Scatter plot, bubble chart | Connected scatter (implies order) |
| Part-to-whole | Stacked bar, treemap | Pie chart (if >5 segments) |

**Clarity principles:**
- Data-ink ratio: maximize data, minimize chartjunk
- Label directly on the plot when possible (reduces legend lookups)
- Use consistent scales when comparing panels
- Show uncertainty (error bars, confidence intervals) when relevant

**Anti-patterns to avoid:**
- 3D effects that distort perception
- Dual y-axes (often misleading)
- Truncated axes that exaggerate differences
- Excessive gridlines, borders, backgrounds

## Avoiding Generic Defaults

Scientific visuals suffer from "default syndrome" - using tool defaults without intentional design.

**The problem:**
- Default matplotlib: gray background, thin lines, small fonts, cramped spacing
- Default Excel: garish colors, 3D effects, excessive gridlines
- Default PowerPoint: clip art, WordArt, busy templates

**The solution:**
Every visual choice should be intentional:
- "Why this color?" → Brand palette, colorblind-safe, emphasizes key data
- "Why this font size?" → Legible at final reproduction size
- "Why this layout?" → Guides viewer to the key insight

**Before finalizing, ask:**
1. Could this be mistaken for a default output? If yes, refine.
2. Does every element serve the story? If not, remove.
3. Would I recognize this as "ours"? Brand consistency matters.

## Output-Specific Guidance

### Figures (matplotlib/seaborn/SVG)

```python
# Example: Oligon-styled matplotlib configuration
import matplotlib.pyplot as plt

# Brand-aligned defaults
plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': '#333333',
    'axes.labelcolor': '#1a1a1a',
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Helvetica', 'Arial', 'Source Sans Pro'],
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': False,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})
```

**Journal requirements:**
- Check target journal for figure size limits (typically 3.5" or 7" width)
- Resolution: 300 DPI minimum for print, 150 DPI for screen
- File formats: PDF/EPS for vector, TIFF/PNG for raster
- Font embedding for PDF outputs

### Infographics (SVG)

Infographics distill complex information into scannable visuals:

- **One clear message** per infographic
- **Visual metaphors** that aid understanding (not just decoration)
- **Data callouts** with key statistics prominently displayed
- **Minimal text** - let visuals carry the narrative
- **Consistent iconography** aligned with brand

SVG output enables:
- Infinite scaling without quality loss
- Easy editing in vector software (Illustrator, Inkscape)
- Web embedding with interactivity potential

### Report Illustrations (ReportLab)

For branded PDF reports using the `oligon_reports` package:

**Available components:**
- `MetricCard`: Key statistics with labels
- `CalloutBox`: Highlighted insights
- `SectionHeader`: Branded section dividers
- `DataTable`: Formatted tabular data

**Design principles:**
- Consistent margins and spacing throughout
- Brand colors applied to headers, accents, callouts
- Professional typography hierarchy
- Visual breaks between sections

### Presentations (PPTX/Beamer)

**Slide design:**
- **One idea per slide** - if you need bullets, you need more slides
- **Minimal text** - speak the details, show the visually
- **Large fonts** - minimum 24pt for body text, 36pt+ for titles
- **High-contrast** - visible from the back of the room

**Figure adaptation:**
- Simplify journal figures for slides (remove fine details)
- Increase line weights and font sizes
- Use animation sparingly and purposefully
- Ensure colors work on projectors (avoid subtle gradients)

**Poster design:**
- Scannable hierarchy: title (3 sec), key figure (10 sec), details (60 sec)
- Limited color palette (3-4 colors maximum)
- Generous whitespace guides the eye
- QR code for additional resources

## Brand Integration

This skill operates within the Oligon visual identity system:

| Resource | Purpose |
|----------|---------|
| `BRAND_COLORS_v4.md` | Color palette definitions |
| `oligon-brand` skill | Brand application guidance |
| `src/oligon_reports/` | Python components for branded PDFs |

When creating visuals:
1. Start with brand color palette
2. Apply brand typography where appropriate
3. Maintain consistency across outputs
4. Deviate intentionally, not accidentally

## Quality Checklist

Before delivering any visual:

- [ ] **Story**: Does it communicate one clear insight?
- [ ] **Audience**: Is it appropriate for the target viewer?
- [ ] **Legibility**: Readable at final reproduction size?
- [ ] **Accessibility**: Colorblind-safe? Sufficient contrast?
- [ ] **Brand**: Aligned with Oligon visual identity?
- [ ] **Intentionality**: Every choice deliberate, not default?
- [ ] **Technical**: Correct resolution, format, dimensions?

## Related Skills

This skill provides the **design philosophy layer**. For implementation details, see:

| Skill | Use For |
|-------|---------|
| `scientific-visualization` | matplotlib/seaborn code, journal specs, export settings |
| `scientific-schematics` | AI-generated diagrams (Nano Banana Pro) |
| `scientific-slides` | Presentation creation (PPTX/Beamer) |
| `latex-posters` / `pptx-posters` | Conference poster creation |
| `generate-image` | AI image generation (FLUX/Gemini) |

**Workflow**: Start here for design decisions → use implementation skills for execution.

---

*Remember: Claude is capable of extraordinary creative work. Apply these principles to create visuals that are both scientifically rigorous and visually distinctive.*
