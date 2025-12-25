# Venue-Templates Skill: Review and Improvement Plan

> Review Date: 2025-12-25
> Status: Planning Document
> Priority: Low (for future enhancement)

---

## 1. Executive Summary

The venue-templates skill is a comprehensive publication preparation toolkit providing LaTeX templates, formatting requirements, and writing style guides for 75+ academic venues. This document identifies gaps, proposes improvements, and outlines implementation priorities for future enhancement.

**Current State**: Functional with strong documentation, but template coverage lags behind documented capabilities.

**Key Finding**: The skill documents 75+ venues but only includes ~6 actual template files. The reference documentation is excellent; the asset library needs expansion.

---

## 2. Current State Assessment

### 2.1 What Works Well

| Component | Assessment | Notes |
|-----------|------------|-------|
| **SKILL.md** | Excellent | Comprehensive 681-line documentation |
| **Writing Style Guides** | Excellent | 11 reference documents covering major venue types |
| **Style Spectrum Concept** | Excellent | Clear framework (accessible → technical) |
| **Venue Coverage Docs** | Good | Covers Nature, Science, Cell, ML conferences, medical journals |
| **Python Scripts** | Good | Functional query, customize, validate tools |
| **Cross-Skill Integration** | Good | Clear references to scientific-writing, peer-review, etc. |

### 2.2 Identified Gaps

| Gap | Severity | Impact |
|-----|----------|--------|
| **Template-Documentation Mismatch** | High | 75+ venues documented, only ~6 templates exist |
| **Missing Conference Templates** | High | ICML, ICLR, CVPR, CHI mentioned but not provided |
| **Stale Template Dates** | Medium | Templates marked "2024" - need version tracking |
| **Script Functionality** | Medium | `validate_format.py` may be incomplete |
| **Missing tikzposter Template** | Low | Referenced in SKILL.md but file doesn't exist |

### 2.3 File Inventory

**Actual Templates Present:**

| Type | File | Status |
|------|------|--------|
| Journal | `nature_article.tex` | Present |
| Journal | `neurips_article.tex` | Present |
| Journal | `plos_one.tex` | Present |
| Grant | `nih_specific_aims.tex` | Present |
| Grant | `nsf_proposal_template.tex` | Present |
| Poster | `beamerposter_academic.tex` | Present |

**Templates Documented but Missing:**

- ICML, ICLR, CVPR conference templates
- Science, Cell Press journal templates
- IEEE, ACM transaction templates
- tikzposter, baposter poster templates
- DOE, DARPA grant templates

---

## 3. Proposed Improvements

### 3.1 Priority 1: Template Expansion (High Impact)

**Goal**: Align template library with documented coverage

#### Phase 1A: Core ML/AI Conference Templates
Add templates for the most commonly used venues:

```
assets/journals/
├── icml_article.tex          # ICML 2025 format
├── iclr_article.tex          # ICLR 2025 format
├── cvpr_article.tex          # CVPR 2025 format
├── aaai_article.tex          # AAAI format
└── emnlp_article.tex         # EMNLP/ACL format
```

**Source Strategy**:
- Download official style files from conference websites
- Create wrapper templates with placeholder guidance
- Include anonymization instructions

#### Phase 1B: High-Impact Journal Templates

```
assets/journals/
├── science_article.tex       # Science family
├── cell_article.tex          # Cell Press
├── lancet_article.tex        # Medical - Lancet
├── nejm_article.tex          # Medical - NEJM
├── ieee_trans.tex            # IEEE Transactions
└── acm_article.tex           # ACM journals
```

#### Phase 1C: Additional Poster Templates

```
assets/posters/
├── tikzposter_research.tex   # Modern colorful design
├── baposter_multicolumn.tex  # Box-based layout
├── a0poster_portrait.tex     # Simple A0 template
└── landscape_48x36.tex       # US landscape format
```

### 3.2 Priority 2: Script Enhancement (Medium Impact)

**Goal**: Improve automation and validation capabilities

#### 2A: Enhance `validate_format.py`

Current state: Basic structure, may not fully validate all requirements.

Proposed enhancements:
- PDF page count validation
- Margin measurement (using PyPDF2 or pdfplumber)
- Font size detection
- Figure resolution checking
- Citation format validation
- Anonymization checker (for double-blind venues)

```python
# Proposed validation checks
class VenueValidator:
    def check_page_count(self, pdf_path, venue) -> ValidationResult
    def check_margins(self, pdf_path, venue) -> ValidationResult
    def check_fonts(self, pdf_path, venue) -> ValidationResult
    def check_figure_resolution(self, pdf_path, min_dpi=300) -> ValidationResult
    def check_anonymization(self, pdf_path) -> ValidationResult
    def generate_report(self) -> str
```

#### 2B: Enhance `query_template.py`

Add features:
- Fuzzy venue name matching
- Template recommendation based on discipline
- Deadline/submission cycle information
- Direct links to official author guidelines

#### 2C: Add New Script: `sync_requirements.py`

Automated tool to:
- Fetch latest author guidelines from venue websites
- Compare against stored requirements
- Flag outdated information
- Generate update reports

### 3.3 Priority 3: Documentation Improvements (Medium Impact)

#### 3A: Add Template Version Tracking

Create `assets/TEMPLATE_VERSIONS.md`:

```markdown
# Template Versions

| Template | Version | Last Updated | Official Source | Notes |
|----------|---------|--------------|-----------------|-------|
| nature_article.tex | 2024.1 | 2024-06-15 | nature.com/authors | |
| neurips_article.tex | 2024 | 2024-09-01 | neurips.cc | Anonymous submission |
```

#### 3B: Add Venue Quick Reference Card

Create `references/VENUE_QUICK_REFERENCE.md`:

One-page reference with:
- Page limits at a glance
- Citation style summary
- Key formatting requirements
- Submission deadlines (typical cycles)

#### 3C: Improve Examples Coverage

Add examples for:
- IEEE abstract format
- ACM CCS concepts example
- Grant-specific aims examples (multiple styles)
- Structured vs. unstructured abstract comparison

### 3.4 Priority 4: Integration Enhancements (Lower Priority)

#### 4A: Tighter latex-posters Integration

- Share poster templates between skills
- Unified poster size specifications
- Cross-reference poster design principles

#### 4B: Citation Style Integration with citation-management

- Link venue citation requirements to citation-management BibTeX styles
- Provide venue-specific .bst files where applicable

#### 4C: Add scientific-schematics Figure Specs

Include venue-specific figure requirements:
- Resolution requirements per venue
- Color space requirements (RGB vs CMYK)
- Accepted formats per venue
- Figure size limits

---

## 4. Implementation Roadmap

### Phase 1: Template Expansion (Estimated: 2-3 sessions)

| Task | Priority | Effort | Dependencies |
|------|----------|--------|--------------|
| Add ICML template | P1 | Low | Download from icml.cc |
| Add ICLR template | P1 | Low | Download from iclr.cc |
| Add CVPR template | P1 | Low | Download from cvpr.thecvf.com |
| Add Science template | P1 | Medium | Adapt from Nature |
| Add Cell template | P1 | Medium | Cell Press guidelines |
| Add tikzposter template | P2 | Low | CTAN package |
| Add baposter template | P2 | Low | CTAN package |
| Create TEMPLATE_VERSIONS.md | P2 | Low | None |

### Phase 2: Script Enhancement (Estimated: 1-2 sessions)

| Task | Priority | Effort | Dependencies |
|------|----------|--------|--------------|
| Enhance validate_format.py | P2 | Medium | PyPDF2/pdfplumber |
| Add fuzzy matching to query | P3 | Low | None |
| Create sync_requirements.py | P3 | High | Web scraping setup |

### Phase 3: Documentation Polish (Estimated: 1 session)

| Task | Priority | Effort | Dependencies |
|------|----------|--------|--------------|
| VENUE_QUICK_REFERENCE.md | P2 | Medium | None |
| Additional examples | P3 | Low | None |
| Cross-skill integration docs | P3 | Low | None |

---

## 5. Template Acquisition Strategy

### 5.1 Official Sources

| Venue | Official Template Source |
|-------|-------------------------|
| NeurIPS | https://neurips.cc/Conferences/2025/PaperInformation/StyleFiles |
| ICML | https://icml.cc/Conferences/2025/StyleAuthorInstructions |
| ICLR | https://iclr.cc/Conferences/2025/CallForPapers |
| CVPR | https://cvpr.thecvf.com/Conferences/2025/AuthorGuidelines |
| ACL/EMNLP | https://github.com/acl-org/acl-style-files |
| IEEE | https://www.ieee.org/conferences/publishing/templates.html |
| ACM | https://www.acm.org/publications/proceedings-template |

### 5.2 Template Creation Guidelines

When creating or adapting templates:

1. **Start from official sources** - Always use the venue's official .sty/.cls files
2. **Add helpful comments** - Mark placeholder sections clearly
3. **Include compilation instructions** - Document required packages
4. **Test compilation** - Verify clean build with pdflatex/xelatex
5. **Document version** - Note template version and date
6. **Preserve license** - Maintain original license headers

### 5.3 Maintenance Considerations

Templates require annual updates:
- Conference templates change yearly (NeurIPS 2024 → 2025)
- Journal templates update less frequently
- Grant templates update with agency policy changes

Consider:
- GitHub Actions to check for template updates
- Annual review cycle before major conference seasons
- User feedback mechanism for reporting outdated templates

---

## 6. Quality Metrics

### 6.1 Coverage Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Journal templates | 3 | 15+ |
| Conference templates | 1 (NeurIPS) | 10+ |
| Poster templates | 1 | 4+ |
| Grant templates | 2 | 5+ |
| Writing style guides | 11 | 11 (complete) |

### 6.2 Functionality Metrics

| Metric | Current | Target |
|--------|---------|--------|
| validate_format.py checks | ~3 | 8+ |
| query_template.py venues | ~10 | 50+ |
| Example documents | 4 | 10+ |

### 6.3 Integration Metrics

| Integration | Current | Target |
|-------------|---------|--------|
| Skills with cross-references | 4 | 6+ |
| Shared resources | 0 | 2+ (posters, citations) |

---

## 7. Notes and Considerations

### 7.1 Licensing

- Most conference/journal templates are freely distributable
- Some may have specific license requirements (check IEEE, ACM)
- Maintain attribution in template headers

### 7.2 Scope Boundaries

Keep venue-templates focused on:
- Templates and formatting requirements
- Writing style guidance
- Validation tools

Delegate to other skills:
- Content creation → scientific-writing
- Citation handling → citation-management
- Figure creation → scientific-schematics
- Poster design → latex-posters

### 7.3 User Workflow Considerations

The skill should support these common workflows:

1. **"I need to submit to Nature"** → Template + requirements + style guide
2. **"What's the page limit for NeurIPS?"** → Quick lookup
3. **"Adapt my ICML paper for JMLR"** → Style transformation guidance
4. **"Is my paper formatted correctly?"** → Validation script

---

## 8. Integration Points Analysis

This section documents all current and proposed integration points between venue-templates and other skills in the repository.

### 8.1 Current Integration Map

#### Outbound References (FROM venue-templates TO other skills)

| Target Skill | Integration Type | Location in SKILL.md | Purpose |
|--------------|------------------|---------------------|---------|
| **scientific-schematics** | Visual enhancement | Lines 26-57 | Generate figures meeting venue specs |
| **scientific-writing** | Content guidance | Lines 323-326 | IMRaD structure, clarity principles |
| **literature-review** | Citation synthesis | Lines 328-330 | Apply venue citation styles |
| **peer-review** | Quality evaluation | Lines 332-336 | Verify formatting compliance |
| **latex-posters** | Poster templates | Lines 338-341 | Conference poster requirements |

#### Inbound References (FROM other skills TO venue-templates)

| Source Skill | Reference Type | What They Use | Notes |
|--------------|---------------|---------------|-------|
| **peer-review** | `reviewer_expectations.md` | Calibrate review standards by venue | Line 24 of peer-review SKILL.md |
| **hypothesis-generation** | Writing style guides | Publication style adaptation | Line 290 of hypothesis-generation SKILL.md |
| **scientific-writing** | Venue-specific styles | Tone, voice, abstract format | Lines 534-565 of scientific-writing SKILL.md |
| **citation-management** | Citation requirements | BibTeX styles by venue | Lines 991-993 of citation-management SKILL.md |
| **literature-review** | Publication style guides | Writing for specific venues | Lines 515-519 of literature-review SKILL.md |

### 8.2 Skills WITHOUT venue-templates Integration (Gaps)

The following skills could benefit from venue-templates integration but currently have none:

| Skill | Missing Integration | Potential Value |
|-------|---------------------|-----------------|
| **scientific-slides** | Conference presentation formats | Talk duration by venue, slide count norms |
| **pptx-posters** | Poster size requirements | Conference-specific poster specs |
| **paper-2-web** | Publication venue context | Adapt transformations to venue expectations |
| **scientific-schematics** | Figure requirements by venue | Resolution, format, color space specs |
| **scientific-visualization** | Journal figure specs | Already has inline specs - could centralize |
| **generate-image** | Publication figure requirements | Output quality matching venue needs |
| **scholar-evaluation** | Reviewer expectations | Venue-specific evaluation criteria |
| **research-lookup** | Venue context for searches | Target venue when finding literature |
| **markitdown** | Formatting preservation | Venue-aware document conversion |
| **plotting-libraries** | Export specifications | Journal-ready figure export settings |
| **visual-design** | Venue aesthetic expectations | Brand consistency by publisher |

### 8.3 Proposed New Integrations

#### Priority 1: High-Value Additions to Other Skills

**1. scientific-slides → venue-templates**

Add to `scientific-slides/SKILL.md`:
```markdown
## Venue-Specific Presentation Guidelines

For conference presentations, consult the **venue-templates** skill for:
- Standard talk durations by venue (NeurIPS: 5-20 min, CHI: 10-20 min)
- Expected slide counts and pacing
- Venue-specific presentation norms (demo expectations, Q&A format)
- Writing style guides for adapting paper content to oral presentations

Reference: `venue-templates/references/conferences_formatting.md`
```

**2. pptx-posters → venue-templates**

Add to `pptx-posters/SKILL.md`:
```markdown
## Conference Poster Specifications

Before creating a poster, consult **venue-templates** for:
- Required poster dimensions by conference
- Size specifications (A0, A1, 36×48", etc.)
- Conference-specific design guidelines
- QR code and supplementary material conventions

Reference: `venue-templates/references/posters_guidelines.md`
```

**3. scientific-schematics → venue-templates**

Add to `scientific-schematics/SKILL.md`:
```markdown
## Venue-Specific Figure Requirements

When generating figures for publication, consult **venue-templates** for:
- Resolution requirements by venue (Nature: 300+ dpi, IEEE: 300+ dpi)
- Accepted formats per venue (TIFF, EPS, PDF)
- Color space requirements (RGB vs CMYK)
- Figure size limits and caption requirements

Reference: `venue-templates/references/journals_formatting.md`
```

**4. paper-2-web → venue-templates**

Add to `paper-2-web/SKILL.md`:
```markdown
## Venue-Aware Transformations

When converting papers, consider target venue context from **venue-templates**:
- Adapt transformation style to match venue conventions
- Use venue writing style guides for content adaptation
- Include venue-appropriate metadata in generated outputs

Reference: `venue-templates/references/venue_writing_styles.md`
```

#### Priority 2: Medium-Value Additions

**5. scientific-visualization → venue-templates (Consolidation)**

The scientific-visualization skill currently contains inline journal specifications. Consider:
- Moving detailed specs to venue-templates
- Cross-referencing for single source of truth
- Keeping quick-reference inline, detailed specs in venue-templates

**6. plotting-libraries → venue-templates**

Add to `plotting-libraries/SKILL.md`:
```markdown
## Publication-Ready Export

For journal submissions, consult **venue-templates** for export specifications:
- DPI and resolution requirements by venue
- Accepted file formats per journal
- Color mode requirements (RGB/CMYK/Grayscale)

See: `venue-templates/references/journals_formatting.md` → Figure Requirements section
```

**7. generate-image → venue-templates**

Add to `generate-image/SKILL.md`:
```markdown
## Publication Figure Standards

When generating images for manuscripts, use **venue-templates** for:
- Output resolution matching venue requirements
- Color palette recommendations (colorblind-safe per venue)
- Format specifications for submission

Reference: `venue-templates/references/journals_formatting.md`
```

#### Priority 3: Lower-Value Additions

**8. scholar-evaluation → venue-templates**

```markdown
## Venue-Calibrated Evaluation

For scholar evaluation, consult **venue-templates/references/reviewer_expectations.md** to:
- Understand venue-specific evaluation criteria
- Calibrate quality assessments to venue standards
- Recognize venue-appropriate methodologies
```

**9. research-lookup → venue-templates**

```markdown
## Venue-Targeted Literature Search

When searching for publication venues, use **venue-templates** to:
- Understand writing style expectations of target venues
- Identify appropriate journals for specific research types
- Find venue-specific citation style requirements
```

### 8.4 Proposed Additions TO venue-templates

#### 8.4A: Add Presentation/Slides Section

Add to `venue-templates/SKILL.md`:
```markdown
### 5. Presentation Formats

Presentation specifications for major conferences:

**Talk Durations**:
| Venue | Contributed Talk | Spotlight | Invited |
|-------|-----------------|-----------|---------|
| NeurIPS | 5 min | 5 min | 20-45 min |
| ICML | 5 min | 5 min | 30-60 min |
| CHI | 10-20 min | - | 30-60 min |
| CVPR | 5 min | - | 20-30 min |

**Slide Recommendations**:
- 1 slide per minute is typical
- Include slide numbers for Q&A references
- Use venue-appropriate color schemes
```

Add reference file: `references/presentations_formatting.md`

#### 8.4B: Enhance Figure Requirements Documentation

Expand `references/journals_formatting.md` or create `references/figure_requirements_by_venue.md`:
```markdown
# Figure Requirements by Venue

## High-Impact Journals

### Nature
- Resolution: 300+ dpi (1200 dpi for line art)
- Formats: TIFF, EPS, PDF preferred
- Color: RGB or CMYK
- Width: Single column (89 mm), double column (183 mm), full page (183 mm)
- Max file size: 10 MB per figure

### Science
- Resolution: 300+ dpi
- Formats: TIFF, PDF
- Color: RGB
- Width: 1-column (5.5 cm), 2-column (12 cm), full-width (18 cm)

### Cell Press
- Resolution: 300 dpi minimum, 600+ dpi preferred
- Formats: PDF, EPS, TIFF
- Color: RGB
- Width: Single (85 mm), 1.5-column (114 mm), 2-column (174 mm)
- Graphical abstract: 1200×600 pixels, 300 dpi

## ML Conferences

### NeurIPS/ICML/ICLR
- Resolution: 300+ dpi recommended
- Formats: PDF, PNG
- Color: RGB, colorblind-safe palettes recommended
- Width: Column width in template
- Note: Figures included in page count
```

#### 8.4C: Add Cross-Reference Section to SKILL.md

Add to venue-templates SKILL.md (Integration section):
```markdown
## Related Skills

| Skill | Use For | Reference in venue-templates |
|-------|---------|------------------------------|
| **scientific-writing** | Content creation | Use with writing style guides |
| **citation-management** | Bibliography formatting | Citation styles by venue |
| **scientific-schematics** | Figure generation | Figure requirements section |
| **scientific-visualization** | Data plots | Journal figure specs |
| **latex-posters** | Poster creation | Poster size specifications |
| **pptx-posters** | PowerPoint posters | Poster guidelines |
| **scientific-slides** | Presentations | Presentation formats (proposed) |
| **peer-review** | Manuscript evaluation | reviewer_expectations.md |
| **literature-review** | Citation synthesis | Citation style requirements |
| **hypothesis-generation** | Research design | Writing style adaptation |
| **paper-2-web** | Paper transformation | Venue-aware adaptation |
```

### 8.5 Integration Implementation Checklist

#### Phase A: Update Other Skills (Add TO venue-templates references)

| Skill | Action | Effort | Files to Modify |
|-------|--------|--------|-----------------|
| scientific-slides | Add venue-templates reference | Low | SKILL.md |
| pptx-posters | Add poster specs reference | Low | SKILL.md |
| scientific-schematics | Add figure requirements reference | Low | SKILL.md |
| paper-2-web | Add venue context reference | Low | SKILL.md |
| plotting-libraries | Add export specs reference | Low | SKILL.md |
| generate-image | Add publication standards reference | Low | SKILL.md |
| visual-design | Add venue aesthetic reference | Low | SKILL.md |

#### Phase B: Expand venue-templates Content

| Content | Action | Effort | New Files |
|---------|--------|--------|-----------|
| Presentation formats | Add section + reference doc | Medium | `references/presentations_formatting.md` |
| Figure requirements | Expand existing or new file | Medium | `references/figure_requirements_by_venue.md` |
| Cross-reference table | Add to SKILL.md | Low | None |

#### Phase C: Consolidation Opportunities

| Opportunity | Current State | Proposed |
|-------------|---------------|----------|
| Journal figure specs | Duplicated in scientific-visualization + venue-templates | Single source in venue-templates, cross-ref from others |
| Poster sizes | In both latex-posters and venue-templates | Canonical in venue-templates, reference from poster skills |
| Citation styles | In both citation-management and venue-templates | Venue-templates for requirements, citation-management for implementation |

### 8.6 Integration Architecture Diagram

```
                           ┌─────────────────────┐
                           │   venue-templates   │
                           │                     │
                           │  • Templates        │
                           │  • Requirements     │
                           │  • Style guides     │
                           │  • Validation       │
                           └──────────┬──────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              │                       │                       │
              ▼                       ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
    │  Content Skills │     │  Visual Skills  │     │ Format Skills   │
    ├─────────────────┤     ├─────────────────┤     ├─────────────────┤
    │ scientific-     │     │ scientific-     │     │ latex-posters   │
    │   writing       │     │   schematics    │     │ pptx-posters    │
    │ literature-     │     │ scientific-     │     │ scientific-     │
    │   review        │     │   visualization │     │   slides        │
    │ hypothesis-     │     │ plotting-       │     │ paper-2-web     │
    │   generation    │     │   libraries     │     │ markitdown      │
    │ peer-review     │     │ generate-image  │     │                 │
    │ citation-       │     │ visual-design   │     │                 │
    │   management    │     │                 │     │                 │
    └─────────────────┘     └─────────────────┘     └─────────────────┘

LEGEND:
  ──────► Current integration (documented cross-reference)
  - - - ► Proposed integration (to be added)

Current Inbound:  scientific-writing, literature-review, peer-review,
                  citation-management, hypothesis-generation

Current Outbound: scientific-schematics, scientific-writing,
                  literature-review, peer-review, latex-posters

Proposed New:     scientific-slides, pptx-posters, paper-2-web,
                  scientific-visualization, plotting-libraries,
                  generate-image, visual-design, scholar-evaluation
```

---

## 9. Change Log

| Date | Change | Author |
|------|--------|--------|
| 2025-12-25 | Added Section 8: Integration Points Analysis with current/proposed integrations | Claude |
| 2025-12-25 | Initial review document created | Claude |

---

## 10. References

- SKILL.md (current skill documentation)
- references/ (11 style and formatting guides)
- assets/ (current template inventory)
- Related skills: scientific-writing, peer-review, citation-management, latex-posters

---

*This document should be updated as improvements are implemented.*
