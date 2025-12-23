# Oligon PDF Report Generator - Project Summary & Roadmap

## Current Implementation (v0.1.0)

### What Was Built

A Python package for generating professional scientific PDF reports with Oligon brand styling, using `reportlab` as the PDF engine.

### Package Structure

```
src/oligon_reports/
├── __init__.py           # Package exports
├── brand_colors.py       # Color palette, typography, layout constants
├── components.py         # Visual components (Flowables)
└── report_generator.py   # Main ReportGenerator orchestrator
```

### Core Components

| Component | Purpose | Visual Style |
|-----------|---------|--------------|
| `MetricCard` | Display key statistics | Brand Blue rounded box with large white text |
| `MetricCardRow` | Row of multiple metrics | Auto-spaced horizontal layout |
| `CalloutBox` | Highlight findings/alerts | Colored left border, subtle gray background |
| `Timeline` | Show project milestones | Horizontal bar with progress markers |
| `SectionDivider` | Separate major sections | Brand accent line with optional title |
| `FigurePlaceholder` | Reserve space for figures | Dashed border with caption area |

### Brand Integration

All colors and typography extracted from `BRAND_COLORS_v4.md`:

- **Primary**: Brand Blue `#2DB2E8`
- **Contrast**: Orange `#E8622D`
- **Neutrals**: Dark `#222222`, Medium `#666666`, Muted `#999999`
- **Typography**: Helvetica, 10pt body, hierarchical heading sizes

### Current Usage Pattern

```python
from src.oligon_reports import ReportGenerator

report = ReportGenerator("Title", author="Author", subtitle="Subtitle")
report.add_executive_summary("Summary...", metrics=[("95%", "Accuracy")])
report.add_section("Methods", content="Description...")
report.add_timeline([{"label": "Phase 1", "date": "Jan", "completed": True}])
report.add_callout("Important note", title="Note", box_type="warning")
report.add_table([["Col1", "Col2"], ["A", "B"]])
report.build("output.pdf")
```

### Limitations

1. **Programmatic only** - Requires Python code to build reports
2. **Fixed component set** - Limited to predefined visual elements
3. **No markdown support** - Cannot parse existing documents
4. **No templates** - Each report built from scratch

---

## Planned Enhancements (v0.2.0+)

Based on requirements for greater adaptability with markdown documents and varying content structures.

### 1. Markdown Input Support

**Why**: Enable non-programmers to create branded reports from standard markdown files, and allow reuse of existing documentation.

**How it will work**:

```markdown
---
template: research_report
title: Study Results
author: Research Team
---

# Executive Summary

Key findings from our analysis...

:::metrics
- 48 | Participants
- 92% | Completion Rate
- 12 wk | Duration
:::

## Methods

Standard markdown content here...

:::callout info "Key Finding"
This is an important callout box.
:::

:::timeline
- [x] Protocol | Jan 2024
- [x] Enrollment | Mar 2024
- [ ] Analysis | Jun 2024
:::
```

**Implementation approach**:
- Use `markdown-it` or `mistune` for parsing
- Custom syntax extensions for components (fenced blocks with `:::`)
- YAML front matter for metadata and template selection
- Heading levels map to section hierarchy

### 2. Report Templates

**Why**: Standardize report structures across the organization, ensure consistency, reduce repetitive setup.

**How it will work**:

```yaml
# templates/research_report.yaml
name: Research Report
description: Standard scientific research report format

sections:
  - name: cover
    required: true

  - name: executive_summary
    required: true
    components: [metrics, key_findings]

  - name: background
    required: false

  - name: methods
    required: true
    subsections: [study_design, participants, analysis]

  - name: results
    required: true
    components: [figures, tables]

  - name: discussion
    required: true

  - name: next_steps
    required: false
    components: [timeline, callout]

styles:
  heading1_color: dark_gray
  accent_color: brand_blue
```

**Planned templates**:
- `research_report` - Full scientific report with methods, results, discussion
- `progress_update` - Timeline-focused status report
- `technical_brief` - Concise technical documentation
- `executive_summary` - Single-page overview with metrics

**Usage**:
```python
from src.oligon_reports import MarkdownReport

report = MarkdownReport.from_file("study_results.md", template="research_report")
report.build("output.pdf")
```

### 3. Custom Components

**Why**: Enable creation of domain-specific visual elements without modifying core package.

**How it will work**:

```python
from src.oligon_reports.components import BaseComponent, register_component

@register_component("risk_matrix")
class RiskMatrix(BaseComponent):
    """Custom 3x3 risk assessment matrix."""

    def __init__(self, risks: list[dict]):
        super().__init__()
        self.risks = risks

    def draw(self):
        # Custom drawing logic using self.canv
        pass

    @classmethod
    def from_markdown(cls, content: str):
        """Parse markdown syntax into component."""
        # Parse custom markdown block
        pass
```

**Then usable in markdown**:
```markdown
:::risk_matrix
- high | Security vulnerability | Immediate
- medium | Performance regression | Q2
- low | UI inconsistency | Backlog
:::
```

**Base component features**:
- Standard sizing and positioning
- Access to brand colors and typography
- Automatic markdown syntax registration
- Validation hooks

### 4. Content Extraction

**Why**: Pull specific sections from larger documents, combine content from multiple sources, filter content by relevance.

**How it will work**:

```python
from src.oligon_reports import ContentExtractor

# Extract specific sections
extractor = ContentExtractor("full_document.md")

methods = extractor.section("Methods")
results = extractor.section("Results")
figures = extractor.sections_matching("Figure *")

# Extract by heading level
all_h2 = extractor.by_level(2)

# Extract between markers
summary = extractor.between("## Summary", "## Methods")

# Combine into report
report = ReportGenerator("Extracted Report")
report.add_section("Methods", content=methods.text)
report.add_section("Results", content=results.text)
report.build("extracted.pdf")
```

**Extraction capabilities**:
- By heading name (exact or pattern match)
- By heading level (H1, H2, H3)
- By content markers (start/end patterns)
- By component type (tables, code blocks, images)
- Multi-file extraction and merging

---

## Implementation Priority

| Phase | Feature | Effort | Value |
|-------|---------|--------|-------|
| 1 | Basic markdown parsing | Medium | High |
| 2 | Report templates | Medium | High |
| 3 | Content extraction | Low | Medium |
| 4 | Custom components | Medium | Medium |

### Phase 1: Markdown Parsing (Recommended First)

This unlocks the most value by allowing:
- Existing markdown docs → branded PDFs
- Non-programmers to create reports
- Faster iteration on report content

**Dependencies to add**:
```bash
uv add mistune pyyaml
```

---

## Example: Future Workflow

```bash
# Create report from markdown
uv run python -m oligon_reports convert study.md -o study.pdf --template research_report

# Extract and combine
uv run python -m oligon_reports extract docs/*.md --sections "Results" -o combined_results.pdf

# Validate against template
uv run python -m oligon_reports validate study.md --template research_report
```

---

## Files Reference

| File | Purpose |
|------|---------|
| `BRAND_COLORS_v4.md` | Source of truth for all visual standards |
| `src/oligon_reports/` | Python package |
| `main.py` | Example report generation |
| `example_report.pdf` | Generated sample output |
| `pyproject.toml` | Dependencies and project config |
| `CLAUDE.md` | Development guidance |
