---
name: scientific-writing
version: 1.0.0
description: "Guides scientific manuscript writing using IMRAD structure, citations (APA/AMA/Vancouver), and reporting guidelines (CONSORT/STROBE/PRISMA). Use when writing research papers, journal submissions, abstracts, or scientific documents requiring structured prose with proper citations."
allowed-tools: Read, Write, Edit, Bash
---

# Scientific Writing

## Overview

**This is the core skill for the deep research and writing tool**—combining AI-driven deep research with well-formatted written outputs. Every document produced is backed by comprehensive literature search and verified citations through the research-lookup skill.

Scientific writing is a process for communicating research with precision and clarity. Write manuscripts using IMRAD structure, citations (APA/AMA/Vancouver), figures/tables, and reporting guidelines (CONSORT/STROBE/PRISMA). Apply this skill for research papers and journal submissions.

**Critical Principle: Always write in full paragraphs with flowing prose. Never submit bullet points in the final manuscript.** Use a two-stage process: first create section outlines with key points using research-lookup, then convert those outlines into complete paragraphs.

## Core Philosophy

Scientific writing is not just recording what was done—it is an **argument designed to persuade** the reader of your findings' validity and significance. Three principles should guide every piece of scientific writing:

### Reader-Centricity

Do not write for yourself; write for the reader. Assume readers are intelligent but lack your specific context. The goal is to transfer information with minimal cognitive load. Every sentence should serve the reader's understanding, not demonstrate the author's expertise.

### The Rule of Parsimony

Less is more. Include only what is necessary to support the conclusion. If a detail (like the weather on the day of the experiment) does not impact the result, remove it. Each paragraph, sentence, and word must earn its place in the manuscript.

### Logical Flow as Narrative

Determine the narrative arc before writing. Experiments may be performed out of order, but the report must present them in a linear logic that builds a coherent argument. The reader should never wonder "why am I reading this?"—every section should connect to the central thesis.

---

## When to Use This Skill

This skill should be used when:
- Writing or revising any section of a scientific manuscript (abstract, introduction, methods, results, discussion)
- Structuring a research paper using IMRAD or other standard formats
- Formatting citations and references in specific styles (APA, AMA, Vancouver, Chicago, IEEE)
- Creating, formatting, or improving figures, tables, and data visualizations
- Applying study-specific reporting guidelines (CONSORT for trials, STROBE for observational studies, PRISMA for reviews)
- Drafting abstracts that meet journal requirements (structured or unstructured)
- Preparing manuscripts for submission to specific journals
- Improving writing clarity, conciseness, and precision
- Ensuring proper use of field-specific terminology and nomenclature
- Addressing reviewer comments and revising manuscripts

## Visual Enhancement with Scientific Schematics

**Every scientific paper should include visual elements.** Use the `scientific-schematics` and `generate-image` skills to create figures.

### Minimum Figure Requirements

| Document Type | Minimum | Recommended |
|--------------|---------|-------------|
| Research Papers | 5 | 6-8 |
| Literature Reviews | 4 | 5-7 |
| Posters | 6 | 8-10 |

### Figure Types by Skill

**Use `scientific-schematics` for**:
- Graphical abstracts (required for every paper)
- Study design flowcharts (CONSORT, PRISMA, STROBE)
- Conceptual frameworks and methodology diagrams
- Biological pathways, system architectures

**Use `generate-image` for**:
- Photorealistic illustrations
- Medical/anatomical visualizations
- Cover images and infographics

For detailed figure creation instructions, consult the respective skill documentation.

---

## Core Capabilities

### 1. Manuscript Structure and Organization

**IMRAD Format**: Guide papers through the standard Introduction, Methods, Results, And Discussion structure used across most scientific disciplines. This includes:
- **Introduction**: Establish research context, identify gaps, state objectives
- **Methods**: Detail study design, populations, procedures, and analysis approaches
- **Results**: Present findings objectively without interpretation
- **Discussion**: Interpret results, acknowledge limitations, propose future directions

For detailed guidance on IMRAD structure, refer to `references/imrad_structure.md`.

**Alternative Structures**: Support discipline-specific formats including:
- Review articles (narrative, systematic, scoping)
- Case reports and case series
- Meta-analyses and pooled analyses
- Theoretical/modeling papers
- Methods papers and protocols

### 2. Section-Specific Writing Guidance

For detailed IMRAD section guidance, refer to `references/imrad_structure.md`.

**Abstract**: 150-300 words as flowing paragraphs (never labeled sections unless journal requires). Cover: context, methods, key findings with numbers, significance.

**Executive Summary vs. Abstract**: Abstracts are neutral paper summaries for academic indexing. Executive summaries lead with conclusions/recommendations for decision-makers.

**Introduction (Funnel Approach)**: Broad context → Specific problem → Knowledge gap → Your study objectives.

**Methods**: Ensure reproducibility—participant descriptions, procedures, statistics, equipment, ethics.

**Results**: Logical flow, integrate figures/tables, statistics with effect sizes, no interpretation.

**Discussion**: Relate to questions, compare literature, acknowledge limitations, implications.

### 3. Citation and Reference Management

Apply citation styles correctly across disciplines. For comprehensive style guides, refer to `references/citation_styles.md`.

**Major Citation Styles:**
- **AMA (American Medical Association)**: Numbered superscript citations, common in medicine
- **Vancouver**: Numbered citations in square brackets, biomedical standard
- **APA (American Psychological Association)**: Author-date in-text citations, common in social sciences
- **Chicago**: Notes-bibliography or author-date, humanities and sciences
- **IEEE**: Numbered square brackets, engineering and computer science

**Best Practices:**
- Cite primary sources when possible
- Include recent literature (last 5-10 years for active fields)
- Balance citation distribution across introduction and discussion
- Verify all citations against original sources
- Use reference management software (Zotero, Mendeley, EndNote)

### 4. Figures and Tables

Create effective data visualizations that enhance comprehension. For detailed best practices, refer to `references/figures_tables.md`.

**Core Principle**: Every figure must have a clear one-sentence message. If it doesn't support a specific conclusion, delete it.

**Quick Reference:**
- **Tables**: Precise numerical data, exact values needed
- **Figures**: Trends, patterns, relationships, visual comparisons
- **Colors**: Never red/green; use Viridis, Magma, or ColorBrewer
- **Format**: Always vector (PDF, SVG) for scalability

### 5. Reporting Guidelines by Study Type

Ensure completeness and transparency by following established reporting standards. For comprehensive guideline details, refer to `references/reporting_guidelines.md`.

**Key Guidelines:**
- **CONSORT**: Randomized controlled trials
- **STROBE**: Observational studies (cohort, case-control, cross-sectional)
- **PRISMA**: Systematic reviews and meta-analyses
- **STARD**: Diagnostic accuracy studies
- **TRIPOD**: Prediction model studies
- **ARRIVE**: Animal research
- **CARE**: Case reports
- **SQUIRE**: Quality improvement studies
- **SPIRIT**: Study protocols for clinical trials
- **CHEERS**: Economic evaluations

Each guideline provides checklists ensuring all critical methodological elements are reported.

### 6. Writing Principles and Style

Apply fundamental scientific writing principles. For detailed guidance, refer to `references/writing_principles.md`.

**Four pillars**: Clarity (precise language, defined terms), Conciseness (eliminate redundancy, 15-20 word sentences), Accuracy (exact values, consistent terminology), Objectivity (unbiased, acknowledge limitations).

### 7. Writing Process: From Outline to Full Paragraphs

**CRITICAL: Always write in full paragraphs, never submit bullet points in scientific papers.**

Use the two-stage writing process:

**Stage 1: Create Section Outlines**
- Use research-lookup to gather relevant literature
- Create structured outlines with bullet points marking main arguments, key studies, data points
- These bullets are scaffolding, NOT the final manuscript

**Stage 2: Convert to Full Paragraphs**
- Transform bullet points into complete sentences
- Add transitions between ideas (however, moreover, subsequently)
- Integrate citations naturally within sentences
- Ensure logical flow from sentence to sentence

For detailed examples, the outline-to-prose conversion guide, common mistakes, and when lists are acceptable, see `references/writing_process.md`.

### 8. Journal-Specific Formatting

Adapt manuscripts to journal requirements:
- Follow author guidelines for structure, length, and format
- Apply journal-specific citation styles
- Meet figure/table specifications (resolution, file formats, dimensions)
- Include required statements (funding, conflicts of interest, data availability, ethical approval)
- Adhere to word limits for each section
- Format according to template requirements when provided

### 9. Field-Specific Language and Terminology

Adapt language, terminology, and conventions to match the target scientific discipline. Each field has established vocabulary, preferred phrasings, and domain-specific conventions.

**Key principles**:
- Match audience expertise level (specialized vs. broad-impact journals)
- Define technical terms strategically (at first use, appropriate for audience)
- Maintain terminology consistency throughout the manuscript
- Avoid field-mixing errors (don't import terms incorrectly from adjacent fields)

For detailed discipline-specific guides covering Biomedical, Molecular Biology, Chemistry, Ecology, Physics, Neuroscience, and Social Sciences, see `references/field_terminology.md`.

### 10. Common Pitfalls to Avoid

**Top rejection reasons**: Poor statistics, over-interpretation, irreproducible methods, inadequate samples, poor writing, weak literature review, unclear figures, missing reporting guidelines.

**Writing issues**: Tense mixing (past for methods/results, present for facts), undefined jargon, disrupted flow, missing transitions.

## Workflow for Manuscript Development

**Stage 1: Planning** — Identify journal, determine reporting guideline, outline IMRAD structure, plan figures/tables.

**Stage 2: Drafting** — Start with figures/tables, then write sections using two-stage process (outline → prose). Order: Methods → Results → Discussion → Introduction → Abstract → Title.

**Stage 3: Revision** — Check flow, consistency, figure clarity, guideline adherence, citations, word counts, proofread.

**Stage 4: Final Preparation** — Format for journal, prepare supplementary materials, write cover letter, complete checklists.

### Pre-Submission Diagnostic Tests

Run three tests before submission:
1. **Elevator Pitch**: Can someone grasp the main finding from Title + Abstract alone?
2. **Independence**: Do figures/captions tell the complete story without main text?
3. **So What?**: Does Discussion explicitly state why findings matter?

**Quick checks**: Acronyms defined, citations consistent, figures legible (fonts ≥8pt).

---

## Integration with Other Skills

**Related skills**: research-lookup (literature), scientific-schematics/generate-image (figures), venue-templates (journal-specific styles).

**Workflow**: Use this skill for general principles (IMRAD, citations, clarity), then consult `venue-templates` for venue-specific style adaptation (Nature/Science, Cell Press, medical journals, ML/CS conferences).

## References

Load as needed: `references/imrad_structure.md`, `references/citation_styles.md`, `references/figures_tables.md`, `references/reporting_guidelines.md`, `references/writing_principles.md`, `references/field_terminology.md`, `references/writing_process.md`.
