# Output-Specific Design Guidance

Detailed design guidance for each output format. Load this reference when working with a specific format.

## Figures (matplotlib/seaborn/SVG)

For implementation details and code, see the `plotting-libraries` and `scientific-visualization` skills.

**Journal requirements:**
- Check target journal for figure size limits (typically 3.5" or 7" width)
- Resolution: 300 DPI minimum for print, 150 DPI for screen
- File formats: PDF/EPS for vector, TIFF/PNG for raster
- Font embedding for PDF outputs

## Infographics (SVG)

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

## Report Illustrations (ReportLab)

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

## Presentations (PPTX/Beamer)

**Slide design:**
- **One idea per slide** - if you need bullets, you need more slides
- **Minimal text** - speak the details, show the visual
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
