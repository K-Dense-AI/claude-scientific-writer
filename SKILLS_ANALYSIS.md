# Skills Folder Analysis Report

> Generated: 2025-12-26
> Scope: Review of `/skills/` folder for redundancies and consolidation opportunities

## Executive Summary

The skills folder contains **19 skills** that are generally well-organized with minimal redundancy. The skills cover the complete research lifecycle from literature discovery through publication and dissemination.

**Key Finding**: One consolidation opportunity identified in the review/evaluation skill group.

---

## Skills Inventory

### By Category

| Category | Skills | Count |
|----------|--------|-------|
| **Writing** | `scientific-writing`, `literature-review`, `hypothesis-generation` | 3 |
| **Presentations** | `scientific-slides`, `latex-posters`, `pptx-posters` | 3 |
| **Research** | `research-lookup`, `citation-management`, `peer-review`, `scholar-evaluation` | 4 |
| **Visuals** | `scientific-schematics`, `generate-image`, `plotting-libraries`, `visual-design` | 4 |
| **Documents** | `markitdown`, `venue-templates`, `document-skills` | 3 |
| **Analysis** | `scientific-critical-thinking` | 1 |
| **Conversion** | `paper-2-web` | 1 |

### Structure Summary

| Skill | SKILL.md | scripts/ | references/ | assets/ | Complexity |
|-------|:--------:|:--------:|:-----------:|:-------:|------------|
| scientific-writing | ✓ | | ✓ | | Medium |
| literature-review | ✓ | ✓ | ✓ | ✓ | Medium-High |
| hypothesis-generation | ✓ | ✓ | ✓ | ✓ | High |
| scientific-slides | ✓ | ✓ | ✓ | ✓ | Very High |
| latex-posters | ✓ | ✓ | ✓ | ✓ | High |
| pptx-posters | ✓ | | ✓ | ✓ | Medium |
| research-lookup | ✓ | ✓ | | | Medium-High |
| citation-management | ✓ | ✓ | ✓ | ✓ | Medium |
| peer-review | ✓ | | ✓ | | High |
| scholar-evaluation | ✓ | ✓ | | | Medium-High |
| scientific-schematics | ✓ | ✓ | ✓ | | Very High |
| generate-image | ✓ | ✓ | | | Medium |
| plotting-libraries | ✓ | | ✓ | | Medium |
| visual-design | ✓ | | ✓ | | Medium |
| markitdown | ✓ | ✓ | ✓ | ✓ | Medium-High |
| paper-2-web | ✓ | | ✓ | | Very High |
| venue-templates | ✓ | ✓ | ✓ | ✓ | High |
| scientific-critical-thinking | ✓ | | ✓ | | Medium-High |
| document-skills | ❌ | | | | Container |

---

## Identified Redundancies

### 1. Review/Evaluation Skills (Primary Concern) ⚠️

Three skills have overlapping functionality in research quality assessment:

| Skill | Purpose | Key Features |
|-------|---------|--------------|
| `peer-review` | Formal manuscript/grant evaluation | Section-by-section systematic review, reproducibility assessment |
| `scholar-evaluation` | Structured quality scoring | 8-dimension framework with quantitative scores |
| `scientific-critical-thinking` | Research rigor analysis | Bias detection, statistical validity, evidence quality (GRADE/Cochrane), logical fallacy identification |

**Overlap Analysis**:

- `scientific-critical-thinking` provides critical analysis capabilities that conceptually overlap with methodology assessment in both other skills
- All three evaluate research quality but from slightly different angles
- `peer-review` and `scholar-evaluation` have clearer distinct purposes (formal review vs. structured scoring)

**Recommendation**:

Merge `scientific-critical-thinking` into `peer-review` as a "Critical Analysis Framework" subsection.

| Before | After |
|--------|-------|
| 3 skills | 2 skills |
| `peer-review` | `peer-review` (enhanced with critical thinking framework) |
| `scholar-evaluation` | `scholar-evaluation` (unchanged) |
| `scientific-critical-thinking` | (absorbed into peer-review) |

---

## Non-Redundant Skill Groups

### Visual Generation (3 skills) ✓ Keep Separate

| Skill | Use Case | Backend | Output |
|-------|----------|---------|--------|
| `scientific-schematics` | Technical diagrams (flowcharts, circuits, pathways) | Nano Banana Pro + Gemini review | Publication-quality diagrams |
| `generate-image` | Artistic/photorealistic imagery | FLUX.2 Pro, Gemini 3 Pro | PNG images |
| `plotting-libraries` | Data-driven charts/plots | matplotlib/seaborn | Python code |

**Verdict**: Keep separate - clear purpose boundaries, different tooling, different quality control mechanisms.

### Poster Skills (2 skills) ✓ Keep Separate

| Skill | Format | Use Case |
|-------|--------|----------|
| `latex-posters` | PDF via LaTeX | High control, academic standard, precise layout |
| `pptx-posters` | PowerPoint | Easier editing, collaboration, iterative design |

**Verdict**: Keep separate - different output formats serve different user workflows and preferences.

### Design Guidance (Layered Architecture) ✓ Keep Separate

| Skill | Level | Scope |
|-------|-------|-------|
| `visual-design` | Philosophy/principles | All visual outputs |
| `plotting-libraries` | Decision framework | Data visualization |
| `scientific-slides` | Implementation | Presentations |
| `latex-posters` | Implementation | Posters |

**Verdict**: Intentional layering - `visual-design` provides principles, others implement for specific formats.

---

## Dependency Patterns

### High-Dependency Skills

These skills are required or referenced by many others:

#### 1. `scientific-schematics` (Most Referenced)

Marked as **MANDATORY** in:
- `hypothesis-generation` — 1-2 figures minimum required
- `latex-posters` — 2-3 figures required (40-50% of poster area)
- `scientific-slides` — Essential for technical diagrams
- `paper-2-web` — Methodology/pipeline diagrams

Also referenced by: `markitdown`, `peer-review`, `venue-templates`

#### 2. `research-lookup` (Critical Infrastructure)

Required by:
- `scientific-slides` — 8-15 papers for citations
- `literature-review` — Primary tool for finding sources
- `hypothesis-generation` — Literature synthesis phase
- `scientific-writing` — Background/context research

#### 3. `visual-design` (Philosophy Layer)

Referenced by:
- `plotting-libraries` — Styling integration
- `scientific-slides` — Design philosophy
- `latex-posters` — Design principles
- `paper-2-web` — Visual requirements

### Workflow Chains

```
Research Initiation:
research-lookup → literature-review → hypothesis-generation → scientific-writing

Presentation:
scientific-writing → scientific-slides → [scientific-schematics + research-lookup]

Publication:
venue-templates → scientific-writing → peer-review/scholar-evaluation → citation-management

Dissemination:
scientific-writing → paper-2-web → [web/video/poster outputs]
```

---

## Structural Issues

### 1. Missing SKILL.md

`document-skills/` is a container directory with subdirectories (`docx/`, `pdf/`, `pptx/`, `xlsx/`) but lacks a `SKILL.md` file.

**Options**:
- Add a `SKILL.md` explaining the container structure
- Split into 4 separate skills with individual `SKILL.md` files
- Merge into `markitdown` if functionality overlaps

### 2. Complexity Imbalance

Some skills are significantly more complex than others:

| High Complexity | Reason |
|-----------------|--------|
| `scientific-slides` | Covers 3 distinct workflows (Nano Banana Pro, PowerPoint, LaTeX Beamer) |
| `latex-posters` | Multiple LaTeX packages, extensive templates, quality control workflow |
| `scientific-schematics` | Two-stage AI pipeline with quality thresholds |
| `paper-2-web` | Autonomous multi-output pipeline |

**Consideration**: `scientific-slides` could potentially be split into 3 sub-skills by workflow type.

### 3. Scattered MANDATORY Requirements

Figure requirements are documented in multiple places without central coordination:

- `hypothesis-generation`: "1-2 figures minimum"
- `latex-posters`: "2-3 figures, 40-50% of area"
- `scientific-slides`: "figures/diagrams essential"

**Recommendation**: Document all mandatory requirements in a central location or create a dependency map.

---

## Recommendations

### Priority Actions

| Priority | Action | Impact |
|----------|--------|--------|
| **High** | Merge `scientific-critical-thinking` into `peer-review` | Reduces skill count, eliminates conceptual overlap |
| Medium | Add `SKILL.md` to `document-skills/` | Structural consistency |
| Medium | Create skill dependency diagram | Improves discoverability |
| Low | Consider splitting `scientific-slides` | Reduces per-skill complexity |

### Consolidation Summary

| Current State | Proposed State | Change |
|---------------|----------------|--------|
| 19 skills | 18 skills | -1 |
| 3 review skills | 2 review skills | Merge critical-thinking → peer-review |

### What NOT to Consolidate

| Skills | Reason to Keep Separate |
|--------|------------------------|
| `scientific-schematics` + `generate-image` | Different backends, quality controls, use cases |
| `latex-posters` + `pptx-posters` | Different output formats, user preferences |
| `plotting-libraries` + `visual-design` | Different abstraction levels (how vs. why) |

---

## Appendix: Skill Purposes

| Skill | One-Line Purpose |
|-------|------------------|
| `scientific-writing` | Write research papers (IMRaD structure) |
| `literature-review` | Conduct systematic literature reviews |
| `hypothesis-generation` | Develop testable scientific hypotheses |
| `scientific-slides` | Create research presentations |
| `latex-posters` | Create LaTeX-based academic posters |
| `pptx-posters` | Create PowerPoint-based posters |
| `research-lookup` | Real-time research lookup via Perplexity |
| `citation-management` | Organize and format citations |
| `peer-review` | Systematic manuscript/grant evaluation |
| `scholar-evaluation` | 8-dimension scholarly work assessment |
| `scientific-schematics` | AI-powered technical diagram generation |
| `generate-image` | General-purpose AI image generation |
| `plotting-libraries` | Python plotting library decision framework |
| `visual-design` | Design philosophy for scientific visuals |
| `markitdown` | Convert documents to Markdown |
| `paper-2-web` | Transform papers to web/video/poster |
| `venue-templates` | Publication venue templates and formatting |
| `scientific-critical-thinking` | Research rigor and claim evaluation |
| `document-skills` | Document format conversion (container) |

---

*Analysis conducted by Claude Opus 4.5*
