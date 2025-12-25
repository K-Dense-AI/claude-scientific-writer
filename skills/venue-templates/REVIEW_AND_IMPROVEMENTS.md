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

## 8. Change Log

| Date | Change | Author |
|------|--------|--------|
| 2025-12-25 | Initial review document created | Claude |

---

## 9. References

- SKILL.md (current skill documentation)
- references/ (11 style and formatting guides)
- assets/ (current template inventory)
- Related skills: scientific-writing, peer-review, citation-management, latex-posters

---

*This document should be updated as improvements are implemented.*
