# Venue Templates

## Overview

Access comprehensive LaTeX templates, formatting requirements, and submission guidelines for major scientific publication venues, academic conferences, research posters, and grant proposals. This skill provides ready-to-use templates and detailed specifications for successful academic submissions across disciplines.

Use this skill when preparing manuscripts for journal submission, conference papers, research posters, or grant proposals and need venue-specific formatting requirements and templates.

## When to Use This Skill

This skill should be used when:
- Preparing a manuscript for submission to a specific journal (Nature, Science, PLOS, IEEE, etc.)
- Writing a conference paper with specific formatting requirements (NeurIPS, ICML, CHI, etc.)
- Creating an academic research poster for conferences
- Drafting grant proposals for federal agencies (NSF, NIH, DOE, DARPA) or private foundations
- Checking formatting requirements and page limits for target venues
- Customizing templates with author information and project details
- Verifying document compliance with venue specifications

## Core Capabilities

### 1. Journal Article Templates

Access LaTeX templates and formatting guidelines for 50+ major scientific journals across disciplines:

**Nature Portfolio**:
- Nature, Nature Methods, Nature Biotechnology, Nature Machine Intelligence
- Nature Communications, Nature Protocols
- Scientific Reports

**Science Family**:
- Science, Science Advances, Science Translational Medicine
- Science Immunology, Science Robotics

**PLOS (Public Library of Science)**:
- PLOS ONE, PLOS Biology, PLOS Computational Biology
- PLOS Medicine, PLOS Genetics

**Cell Press**:
- Cell, Neuron, Immunity, Cell Reports
- Molecular Cell, Developmental Cell

**IEEE Publications**:
- IEEE Transactions (various disciplines)
- IEEE Access, IEEE Journal templates

**ACM Publications**:
- ACM Transactions, Communications of the ACM
- ACM conference proceedings

**Other Major Publishers**:
- Springer journals (various disciplines)
- Elsevier journals (custom templates)
- Wiley journals
- BMC journals
- Frontiers journals

### 2. Conference Paper Templates

Conference-specific templates with proper formatting for major academic conferences:

**Machine Learning & AI**:
- NeurIPS (Neural Information Processing Systems)
- ICML (International Conference on Machine Learning)
- ICLR (International Conference on Learning Representations)
- CVPR (Computer Vision and Pattern Recognition)
- AAAI (Association for the Advancement of Artificial Intelligence)

**Computer Science**:
- ACM CHI (Human-Computer Interaction)
- SIGKDD (Knowledge Discovery and Data Mining)
- EMNLP (Empirical Methods in Natural Language Processing)
- SIGIR (Information Retrieval)
- USENIX conferences

**Biology & Bioinformatics**:
- ISMB (Intelligent Systems for Molecular Biology)
- RECOMB (Research in Computational Molecular Biology)
- PSB (Pacific Symposium on Biocomputing)

**Engineering**:
- IEEE conference templates (various disciplines)
- ASME, AIAA conferences

### 3. Research Poster Templates

Academic poster templates for conference presentations:

**Standard Formats**:
- A0 (841 × 1189 mm / 33.1 × 46.8 in)
- A1 (594 × 841 mm / 23.4 × 33.1 in)
- 36" × 48" (914 × 1219 mm) - Common US size
- 42" × 56" (1067 × 1422 mm)
- 48" × 36" (landscape orientation)

**Template Packages**:
- **beamerposter**: Classic academic poster template
- **tikzposter**: Modern, colorful poster design
- **baposter**: Structured multi-column layout

**Design Features**:
- Optimal font sizes for readability at distance
- Color schemes (colorblind-safe palettes)
- Grid layouts and column structures
- QR code integration for supplementary materials

### 4. Grant Proposal Templates

Templates and formatting requirements for major funding agencies:

**NSF (National Science Foundation)**:
- Full proposal template (15-page project description)
- Project Summary (1 page: Overview, Intellectual Merit, Broader Impacts)
- Budget and budget justification
- Biographical sketch (3-page limit)
- Facilities, Equipment, and Other Resources
- Data Management Plan

**NIH (National Institutes of Health)**:
- R01 Research Grant (multi-year)
- R21 Exploratory/Developmental Grant
- K Awards (Career Development)
- Specific Aims Page (1 page, most critical component)
- Research Strategy (Significance, Innovation, Approach)
- Biographical sketches (5-page limit)

**DOE (Department of Energy)**:
- Office of Science proposals
- ARPA-E templates
- Technology Readiness Level (TRL) descriptions
- Commercialization and impact sections

**DARPA (Defense Advanced Research Projects Agency)**:
- BAA (Broad Agency Announcement) responses
- Heilmeier Catechism framework
- Technical approach and milestones
- Transition planning

**Private Foundations**:
- Gates Foundation
- Wellcome Trust
- Howard Hughes Medical Institute (HHMI)
- Chan Zuckerberg Initiative (CZI)

## Workflow: Finding and Using Templates

### Step 1: Identify Target Venue

Determine the specific publication venue, conference, or funding agency:

```
Example queries:
- "I need to submit to Nature"
- "What are the requirements for NeurIPS 2025?"
- "Show me NSF proposal formatting"
- "I'm creating a poster for ISMB"
```

### Step 2: Query Template and Requirements

Access venue-specific templates and formatting guidelines:

**For Journals**:
```bash
# Load journal formatting requirements
Reference: references/journals_formatting.md
Search for: "Nature" or specific journal name

# Retrieve template
Template: assets/journals/nature_article.tex
```

**For Conferences**:
```bash
# Load conference formatting
Reference: references/conferences_formatting.md
Search for: "NeurIPS" or specific conference

# Retrieve template
Template: assets/journals/neurips_article.tex
```

**For Posters**:
```bash
# Load poster guidelines
Reference: references/posters_guidelines.md

# Retrieve template
Template: assets/posters/beamerposter_academic.tex
```

**For Grants**:
```bash
# Load grant requirements
Reference: references/grants_requirements.md
Search for: "NSF" or specific agency

# Retrieve template
Template: assets/grants/nsf_proposal_template.tex
```

### Step 3: Review Formatting Requirements

Check critical specifications before customizing:

**Key Requirements to Verify**:
- Page limits (varies by venue)
- Font size and family
- Margin specifications
- Line spacing
- Citation style (APA, Vancouver, Nature, etc.)
- Figure/table requirements
- File format (PDF, Word, LaTeX source)
- Anonymization (for double-blind review)
- Supplementary material limits

### Step 4: Customize Template

Use helper scripts or manual customization:

**Option 1: Helper Script (Recommended)**:
```bash
python scripts/customize_template.py \
  --template assets/journals/nature_article.tex \
  --title "Your Paper Title" \
  --authors "First Author, Second Author" \
  --affiliations "University Name" \
  --output my_nature_paper.tex
```

**Option 2: Manual Editing**:
- Open template file
- Replace placeholder text (marked with comments)
- Fill in title, authors, affiliations, abstract
- Add your content to each section

### Step 5: Validate Format

Check compliance with venue requirements:

```bash
python scripts/validate_format.py \
  --file my_paper.pdf \
  --venue "Nature" \
  --check-all
```

**Validation Checks**:
- Page count within limits
- Font sizes correct
- Margins meet specifications
- References formatted correctly
- Figures meet resolution requirements

### Step 6: Compile and Review

Compile LaTeX and review output:

```bash
# Compile LaTeX
pdflatex my_paper.tex
bibtex my_paper
pdflatex my_paper.tex
pdflatex my_paper.tex

# Or use latexmk for automated compilation
latexmk -pdf my_paper.tex
```

Review checklist:
- [ ] All sections present and properly formatted
- [ ] Citations render correctly
- [ ] Figures appear with proper captions
- [ ] Page count within limits
- [ ] Author guidelines followed
- [ ] Supplementary materials prepared (if needed)

## Integration with Other Skills

This skill works seamlessly with other scientific skills:

### Scientific Writing
- Use **scientific-writing** skill for content guidance (IMRaD structure, clarity, precision)
- Apply venue-specific templates from this skill for formatting
- Combine for complete manuscript preparation

### Literature Review
- Use **literature-review** skill for systematic literature search and synthesis
- Apply appropriate citation style from venue requirements
- Format references according to template specifications

### Peer Review
- Use **peer-review** skill to evaluate manuscript quality
- Use this skill to verify formatting compliance
- Ensure adherence to reporting guidelines (CONSORT, STROBE, etc.)

### Research Grants
- Cross-reference with **research-grants** skill for content strategy
- Use this skill for agency-specific templates and formatting
- Combine for comprehensive grant proposal preparation

### LaTeX Posters
- This skill provides venue-agnostic poster templates
- Use for conference-specific poster requirements
- Integrate with visualization skills for figure creation

## Template Categories

### By Document Type

| Category | Template Count | Common Venues |
|----------|---------------|---------------|
| **Journal Articles** | 30+ | Nature, Science, PLOS, IEEE, ACM, Cell Press |
| **Conference Papers** | 20+ | NeurIPS, ICML, CVPR, CHI, ISMB |
| **Research Posters** | 10+ | A0, A1, 36×48, various packages |
| **Grant Proposals** | 15+ | NSF, NIH, DOE, DARPA, foundations |

### By Discipline

| Discipline | Supported Venues |
|------------|------------------|
| **Life Sciences** | Nature, Cell Press, PLOS, ISMB, RECOMB |
| **Physical Sciences** | Science, Physical Review, ACS, APS |
| **Engineering** | IEEE, ASME, AIAA, ACM |
| **Computer Science** | ACM, IEEE, NeurIPS, ICML, ICLR |
| **Medicine** | NEJM, Lancet, JAMA, BMJ |
| **Interdisciplinary** | PNAS, Nature Communications, Science Advances |

## Helper Scripts

### query_template.py

Search and retrieve templates by venue name, type, or keywords:

```bash
# Find templates for a specific journal
python scripts/query_template.py --venue "Nature" --type "article"

# Search by keyword
python scripts/query_template.py --keyword "machine learning"

# List all available templates
python scripts/query_template.py --list-all

# Get requirements for a venue
python scripts/query_template.py --venue "NeurIPS" --requirements
```

### customize_template.py

Customize templates with author and project information:

```bash
# Basic customization
python scripts/customize_template.py \
  --template assets/journals/nature_article.tex \
  --output my_paper.tex

# With author information
python scripts/customize_template.py \
  --template assets/journals/nature_article.tex \
  --title "Novel Approach to Protein Folding" \
  --authors "Jane Doe, John Smith, Alice Johnson" \
  --affiliations "MIT, Stanford, Harvard" \
  --email "[email protected]" \
  --output my_paper.tex

# Interactive mode
python scripts/customize_template.py --interactive
```

### validate_format.py

Check document compliance with venue requirements:

```bash
# Validate a compiled PDF
python scripts/validate_format.py \
  --file my_paper.pdf \
  --venue "Nature" \
  --check-all

# Check specific aspects
python scripts/validate_format.py \
  --file my_paper.pdf \
  --venue "NeurIPS" \
  --check page-count,margins,fonts

# Generate validation report
python scripts/validate_format.py \
  --file my_paper.pdf \
  --venue "Science" \
  --report validation_report.txt
```

## Best Practices

### Template Selection
1. **Verify currency**: Check template date and compare with latest author guidelines
2. **Check official sources**: Many journals provide official LaTeX classes
3. **Test compilation**: Compile template before adding content
4. **Read comments**: Templates include helpful inline comments

### Customization
1. **Preserve structure**: Don't remove required sections or packages
2. **Follow placeholders**: Replace marked placeholder text systematically
3. **Maintain formatting**: Don't override venue-specific formatting
4. **Keep backups**: Save original template before customization

### Compliance
1. **Check page limits**: Verify before final submission
2. **Validate citations**: Use correct citation style for venue
3. **Test figures**: Ensure figures meet resolution requirements
4. **Review anonymization**: Remove identifying information if required

### Submission
1. **Follow instructions**: Read complete author guidelines
2. **Include all files**: LaTeX source, figures, bibliography
3. **Generate properly**: Use recommended compilation method
4. **Check output**: Verify PDF matches expectations

## Common Formatting Requirements

### Page Limits (Typical)

| Venue Type | Typical Limit | Notes |
|------------|---------------|-------|
| **Nature Article** | 5 pages | ~3000 words excluding refs |
| **Science Report** | 5 pages | Figures count toward limit |
| **PLOS ONE** | No limit | Unlimited length |
| **NeurIPS** | 8 pages | + unlimited refs/appendix |
| **ICML** | 8 pages | + unlimited refs/appendix |
| **NSF Proposal** | 15 pages | Project description only |
| **NIH R01** | 12 pages | Research strategy |

### Citation Styles by Venue

| Venue | Citation Style | Format |
|-------|---------------|--------|
| **Nature** | Numbered (superscript) | Nature style |
| **Science** | Numbered (superscript) | Science style |
| **PLOS** | Numbered (brackets) | Vancouver |
| **Cell Press** | Author-year | Cell style |
| **ACM** | Numbered | ACM style |
| **IEEE** | Numbered (brackets) | IEEE style |
| **APA journals** | Author-year | APA 7th |

### Figure Requirements

| Venue | Resolution | Format | Color |
|-------|-----------|--------|-------|
| **Nature** | 300+ dpi | TIFF, EPS, PDF | RGB or CMYK |
| **Science** | 300+ dpi | TIFF, PDF | RGB |
| **PLOS** | 300-600 dpi | TIFF, EPS | RGB |
| **IEEE** | 300+ dpi | EPS, PDF | RGB or Grayscale |

## Resources

### Bundled Resources

**References** (in `references/`):
- `journals_formatting.md`: Comprehensive journal formatting requirements
- `conferences_formatting.md`: Conference paper specifications
- `posters_guidelines.md`: Research poster design and sizing
- `grants_requirements.md`: Grant proposal requirements by agency

**Templates** (in `assets/`):
- `journals/`: Journal article LaTeX templates
- `posters/`: Research poster templates
- `grants/`: Grant proposal templates

**Scripts** (in `scripts/`):
- `query_template.py`: Search and retrieve templates
- `customize_template.py`: Customize with author info
- `validate_format.py`: Check compliance with requirements

### External Resources

**Journal Author Guidelines**:
- Nature: https://www.nature.com/nature/for-authors
- Science: https://www.science.org/content/page/instructions-authors
- PLOS: https://plos.org/resources/for-authors/
- Cell Press: https://www.cell.com/author-guidelines

**Conference Formatting**:
- NeurIPS: https://neurips.cc/Conferences/2024/CallForPapers
- ICML: https://icml.cc/Conferences/2024/StyleAuthorInstructions
- CVPR: https://cvpr.thecvf.com/Conferences/2024/AuthorGuidelines

**Grant Resources**:
- NSF PAPPG: https://www.nsf.gov/publications/pub_summ.jsp?ods_key=pappg
- NIH Forms: https://grants.nih.gov/grants/how-to-apply-application-guide.html
- DOE Funding: https://science.osti.gov/grants

## Example Usage

### Example 1: Nature Article Submission

```markdown
User: "I need to prepare a manuscript for Nature"

Response:
1. Load Nature formatting requirements (references/journals_formatting.md)
2. Retrieve Nature template (assets/journals/nature_article.tex)
3. Key requirements:
   - Length: ~3000 words, ~5 pages
   - Format: Single column, 12pt font
   - Citations: Numbered superscript (Nature style)
   - Figures: 300+ dpi, RGB color
4. Customize template with your title, authors, affiliations
5. Compile and validate against requirements
```

### Example 2: NeurIPS Conference Paper

```markdown
User: "What are the formatting requirements for NeurIPS?"

Response:
From references/conferences_formatting.md:
- Page limit: 8 pages main text + unlimited references/appendix
- Format: Two-column, 10pt font
- Template: neurips_2024.sty (official style file)
- Anonymization: Required for initial submission
- Citations: Numbered (brackets)
- Figures: High resolution, colorblind-safe recommended
```

### Example 3: NSF Proposal

```markdown
User: "Help me format an NSF proposal"

Response:
NSF requirements (from references/grants_requirements.md):
- Project Description: 15 pages maximum
- Project Summary: 1 page (Overview, Intellectual Merit, Broader Impacts)
- Budget Justification: 3-5 pages
- Biographical Sketch: 3 pages per senior personnel
- Font: Minimum 10pt, Times Roman or similar
- Margins: 1 inch all sides
Template: assets/grants/nsf_proposal_template.tex
```

### Example 4: Conference Poster

```markdown
User: "I need to create a poster for ISMB"

Response:
ISMB poster specifications:
- Size: Typically A0 portrait (33.1 × 46.8 inches)
- Recommended template: beamerposter or tikzposter
- Font sizes: Title 60-85pt, Headers 36-48pt, Body 24-32pt
- Include: QR code for paper/supplementary materials
Available templates:
- assets/posters/beamerposter_academic.tex
- assets/posters/tikzposter_research.tex
```

## Updates and Maintenance

**Template Currency**:
- Templates updated annually or when venues release new guidelines
- Last updated: 2024
- Check official venue sites for most current requirements

**Reporting Issues**:
- Template compilation errors
- Outdated formatting requirements
- Missing venue templates
- Incorrect specifications

## Summary

The venue-templates skill provides comprehensive access to:

1. **50+ publication venue templates** across disciplines
2. **Detailed formatting requirements** for journals, conferences, posters, grants
3. **Helper scripts** for template discovery, customization, and validation
4. **Integration** with other scientific writing skills
5. **Best practices** for successful academic submissions

Use this skill whenever you need venue-specific formatting guidance or templates for academic publishing.

