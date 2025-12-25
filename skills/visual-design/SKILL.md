---
name: visual-design
description: Provides design philosophy for publication-quality scientific visuals. Use when the user needs guidance on figures, charts, infographics, posters, or slides. Triggers on questions about typography, color, layout, accessibility, or visual best practices for science communication. Delivers principles, not code—delegates implementation to scientific-visualization and plotting-libraries skills.
version: 1.0.0
license: Internal use - Oligon brand standards apply
allowed-tools: Read, Glob, Write
---

Apply intentional design thinking to create publication-quality scientific visuals that avoid generic "default matplotlib" aesthetics.

Analyze the user's visualization requirements—figure, chart, infographic, poster, or presentation—considering their audience, publication venue, and technical constraints.

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
| **Figures** | matplotlib, seaborn, plotly, SVG | Journal papers, reports (see [plotting-libraries](../plotting-libraries/SKILL.md)) |
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

**Typography rules:**
- **Maximum 2 font families** - One for headings, one for body; create variation through weight/size
- **High contrast required** - Dark text on light backgrounds (or vice versa); minimum 4.5:1 ratio
- **Consistent sizing** - Establish a type scale and stick to it across all panels/slides

**Anti-patterns to avoid:**
- Default matplotlib fonts without customization
- Inconsistent font sizes across panels
- Decorative fonts that sacrifice legibility
- ALL CAPS for long text strings

### Color

Color communicates data and establishes visual identity:

**Brand integration:**
- Use Oligon color palette as the foundation (see `references/BRAND_COLORS_v4.md`)
- Primary colors for main data series
- Accent colors for highlights and callouts
- Neutral palette for backgrounds, axes, gridlines

**Data visualization principles:**
- Sequential palettes for continuous data (light→dark)
- Diverging palettes for data with meaningful center (e.g., fold change)
- Categorical palettes for discrete groups (max 7-8 distinguishable colors)

**Accessibility essentials:**
- **Avoid red/green contrast alone** - ~8% of males are red-green colorblind; use blue/orange or magenta/green instead
- **Redundant coding** - Never rely on color alone; add shapes, patterns, or direct labels to convey meaning
- **Greyscale test** - Convert your design to black & white; if meaning is lost, contrast is insufficient
- **Colorblind-safe palettes** - Verify with simulators (e.g., Coblis, Color Oracle) before finalizing
- **Sufficient contrast** - WCAG recommends 4.5:1 ratio for text; avoid light-on-light or dark-on-dark

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

**Gestalt principles** (how the brain groups visual elements):
- **Proximity** - Elements placed close together are perceived as related; use spacing to create logical groups
- **Similarity** - Elements sharing color, shape, or size are seen as belonging together
- **Alignment** - Use a grid system; misaligned elements look unprofessional and confuse relationships

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

For detailed format-specific guidance, see `references/OUTPUT_FORMATS.md`. Key formats:
- **Figures**: Journal specs, resolution, vector vs raster
- **Infographics**: SVG best practices, visual metaphors
- **Reports**: ReportLab components (MetricCard, CalloutBox, etc.)
- **Presentations**: Slide design, poster hierarchy

## Brand Integration

This skill operates within the Oligon visual identity system:

| Resource | Purpose |
|----------|---------|
| `references/BRAND_COLORS_v4.md` | Color palette definitions |
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
