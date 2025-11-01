# Available Skills

This document provides an overview of all skills available in the Scientific Writer CLI.

## Writing Skills

### 1. Scientific Writing
**Location**: `.claude/skills/scientific-writing/`

**Capabilities**:
- IMRaD structure guidance (Introduction, Methods, Results, and Discussion)
- Citation styles (APA, MLA, Chicago, Nature, Science, etc.)
- Figure and table formatting best practices
- Reporting guidelines for various study types
- Writing principles for clarity, precision, and scientific rigor

**References**:
- `citation_styles.md`: Comprehensive guide to major citation formats
- `figures_tables.md`: Best practices for presenting data
- `imrad_structure.md`: Detailed guidance on each section
- `reporting_guidelines.md`: Standards for clinical trials, observational studies, etc.
- `writing_principles.md`: Core principles of scientific communication

---

### 2. Literature Review
**Location**: `.claude/skills/literature-review/`

**Capabilities**:
- Conducting systematic literature searches
- Database search strategies (PubMed, Web of Science, etc.)
- Citation management and verification
- Review synthesis and organization
- PDF generation for literature summaries

**References**:
- `citation_styles.md`: Citation formatting guidelines
- `database_strategies.md`: Effective search strategies

**Scripts**:
- `search_databases.py`: Automated database searching
- `verify_citations.py`: Citation verification tools
- `generate_pdf.py`: PDF generation for reviews

**Assets**:
- `review_template.md`: Template for literature review documents

---

### 3. Peer Review
**Location**: `.claude/skills/peer-review/`

**Capabilities**:
- Identifying common issues in scientific manuscripts
- Evaluating reporting standards compliance
- Providing constructive feedback
- Assessing methodology and statistical analysis
- Checking adherence to journal guidelines

**References**:
- `common_issues.md`: Frequently found problems in manuscripts
- `reporting_standards.md`: Required elements for different study types

---

### 4. Scholar Evaluation
**Location**: `.claude/skills/scholar-evaluation/`

**Capabilities**:
- Systematic quantitative evaluation across 8 dimensions using ScholarEval framework
- Scoring research papers, proposals, and literature reviews (1-5 scale)
- Assessing publication readiness for target venues
- Providing prioritized, actionable feedback with evidence-based recommendations
- Identifying strengths and weaknesses across problem formulation, literature review, methodology, data collection, analysis, results, writing quality, and citations
- Generating comprehensive evaluation reports with dimension scores

**References**:
- `evaluation_framework.md`: Detailed rubrics and quality indicators for all 8 evaluation dimensions

**Scripts**:
- `calculate_scores.py`: Calculate aggregate scores from dimension ratings, generate evaluation reports

**Features**:
- Research-backed framework (ScholarEval methodology from arXiv:2510.16234)
- Quantitative scoring (1-5 scale per dimension) with weighted averaging
- Dimension-specific rubrics for consistent evaluation
- Publication readiness assessment
- Strengths/weaknesses identification
- Prioritized recommendations by impact
- Contextual adjustments for work stage, venue, and discipline

**When to Use**:
- As a complement to peer review for quantitative assessment
- Evaluating publication readiness before submission
- Tracking improvement across multiple revisions
- Benchmarking research quality against established criteria
- Providing structured feedback for academic work

**Key Guidance**:
- Complements peer-review skill with systematic quantitative approach
- Evaluates across 8 dimensions: Problem Formulation, Literature Review, Methodology, Data Collection, Analysis, Results, Writing Quality, Citations
- Scores range from 1 (Poor) to 5 (Excellent)
- Overall assessment thresholds: 4.5+ (Exceptional/Top-tier), 4.0-4.4 (Strong/Minor revisions), 3.5-3.9 (Good/Major revisions), 3.0-3.4 (Acceptable/Significant revisions), <3.0 (Needs major rework)

---

### 5. Research Grants
**Location**: `.claude/skills/research-grants/`

**Capabilities**:
- Writing competitive research proposals for NSF, NIH, DOE, and DARPA
- Agency-specific formatting and requirements
- Review criteria understanding (Intellectual Merit, Broader Impacts, Significance, Innovation)
- Budget preparation and justification
- Specific Aims pages (NIH)
- Project Summaries (NSF)
- Broader Impacts strategies
- Technology transition planning (DOE, DARPA)
- Resubmission strategies

**Focus Agencies**:
- **NSF**: National Science Foundation (Intellectual Merit + Broader Impacts)
- **NIH**: National Institutes of Health (R01, R21, K awards, etc.)
- **DOE**: Department of Energy (Office of Science, ARPA-E, EERE)
- **DARPA**: Defense Advanced Research Projects Agency (BAAs, SBIR)

**References**:
- `nsf_guidelines.md`: NSF proposal structure, broader impacts, review criteria
- `nih_guidelines.md`: NIH mechanisms, specific aims, research strategy
- `doe_guidelines.md`: DOE programs, TRLs, cost sharing, lab partnerships
- `darpa_guidelines.md`: DARPA structure, Heilmeier Catechism, PM engagement
- `broader_impacts.md`: Comprehensive NSF broader impacts strategies
- `specific_aims_guide.md`: Complete guide to NIH Specific Aims page

**Assets/Templates**:
- `nsf_project_summary_template.md`: NSF Project Summary with Overview, Intellectual Merit, Broader Impacts
- `nih_specific_aims_template.md`: NIH Specific Aims page template
- `budget_justification_template.md`: Budget justification with agency-specific examples

**Features**:
- Agency-specific review criteria and scoring systems
- Success rates and funding trends by agency
- Timeline planning and milestone development
- Budget preparation with personnel, equipment, travel, supplies
- Broader impacts with measurable outcomes (NSF)
- Preliminary data integration (NIH)
- National laboratory collaboration (DOE)
- Technology transition and commercialization (DOE, DARPA)
- Resubmission and reviewer response strategies

**Key Guidance**:
- NSF: Equally weighted Intellectual Merit and Broader Impacts (must be substantive)
- NIH: Specific Aims page is the most critical component (1 page)
- DOE: Energy relevance, TRLs, cost sharing, commercialization pathway
- DARPA: High-risk/high-reward, Heilmeier Catechism, PM engagement essential

---

### 6. LaTeX Research Posters
**Location**: `.claude/skills/latex-posters/`

**Capabilities**:
- Creating professional research posters using LaTeX (beamerposter, tikzposter, baposter)
- Conference poster design and layout
- Full-page poster templates with proper spacing
- Color schemes and visual design principles
- Typography and readability optimization
- PDF generation and quality control
- Accessibility and inclusive design
- Poster size configuration (A0, A1, 36×48", etc.)

**References**:
- `latex_poster_packages.md`: Detailed comparison of beamerposter, tikzposter, and baposter
- `poster_design_principles.md`: Typography, color theory, visual hierarchy, and accessibility
- `poster_layout_design.md`: Grid systems, spatial organization, and visual flow
- `poster_content_guide.md`: Content strategy, writing style, and section-specific guidance

**Scripts**:
- `review_poster.sh`: Automated PDF quality check script

**Assets**:
- `beamerposter_template.tex`: Classic academic poster template
- `tikzposter_template.tex`: Modern, colorful poster template
- `baposter_template.tex`: Structured multi-column poster template
- `poster_quality_checklist.md`: Comprehensive pre-printing checklist

**Features**:
- Ensures posters span the full page without excessive margins
- PDF review and quality control guidelines
- Automated checking scripts for page size, fonts, and images
- Reduced-scale print testing instructions
- Color contrast and accessibility verification
- Common issues troubleshooting guide

---

### 6. Scientific Schematics and Diagrams
**Location**: `.claude/skills/scientific-schematics/`

**Capabilities**:
- Create methodology flowcharts (CONSORT diagrams for clinical trials)
- Generate circuit diagrams and electrical schematics
- Visualize biological pathways and signaling cascades
- Design system architecture and block diagrams
- Create process flow diagrams and decision trees
- Network diagrams and graph visualizations
- Publication-quality vector graphics with TikZ/LaTeX
- Programmatic diagram generation with Python (Schemdraw, NetworkX, Matplotlib)

**References**:
- `tikz_guide.md`: Comprehensive TikZ syntax, positioning, styles, and techniques
- `diagram_types.md`: Catalog of scientific diagram types with use cases and examples
- `best_practices.md`: Publication standards, accessibility, and colorblind-safe design
- `python_libraries.md`: Guide to Schemdraw, NetworkX, and Matplotlib for programmatic generation

**Scripts**:
- `generate_flowchart.py`: Convert text descriptions to TikZ flowcharts
- `circuit_generator.py`: Generate circuit diagrams using Schemdraw
- `pathway_diagram.py`: Create biological pathway diagrams with Matplotlib
- `compile_tikz.py`: Standalone TikZ compilation utility (PDF/PNG output)

**Assets**:
- `tikz_styles.tex`: Reusable style definitions with Okabe-Ito colorblind-safe palette
- `flowchart_template.tex`: CONSORT-style methodology flowchart template
- `circuit_template.tex`: Electrical circuit diagram template with CircuitikZ
- `pathway_template.tex`: Biological pathway diagram template
- `block_diagram_template.tex`: System architecture diagram template

**Features**:
- Colorblind-safe Okabe-Ito color palette throughout
- Vector graphics for infinite scalability
- LaTeX integration for consistent typography
- Automated flowchart generation from numbered lists
- Publication-ready output (PDF, SVG, PNG)
- Accessible design following WCAG standards
- Grayscale compatibility verification

**Use Cases**:
- **CONSORT diagrams**: Participant flow for clinical trials
- **Electronics papers**: Circuit schematics and signal processing diagrams
- **Biology papers**: Signaling cascades, metabolic pathways, gene networks
- **Engineering papers**: System architecture, data flow, block diagrams
- **Methodology sections**: Study design, data processing pipelines
- **Conceptual frameworks**: Process flows, decision trees

---

## Document Manipulation Skills

### 7. MarkItDown - Universal File to Markdown Converter
**Location**: `.claude/skills/markitdown/`

**Capabilities**:
- Convert 15+ file formats to Markdown (PDF, DOCX, PPTX, XLSX, images, audio, etc.)
- AI-enhanced image descriptions using Claude Sonnet 4.5
- OCR for scanned documents and images
- Speech-to-text transcription for audio files
- YouTube video transcription extraction
- Batch processing with parallel execution
- Azure Document Intelligence integration for complex PDFs
- Plugin system for custom converters

**References**:
- `api_reference.md`: Complete API documentation and class references
- `file_formats.md`: Format-specific conversion guides and best practices

**Scripts**:
- `batch_convert.py`: Parallel batch conversion of multiple files
- `convert_with_ai.py`: AI-enhanced conversions with custom prompts
- `convert_literature.py`: Scientific literature conversion with metadata extraction

**Assets**:
- `example_usage.md`: Comprehensive examples for common use cases

**Features**:
- Token-efficient Markdown output optimized for LLM processing
- Supports optional dependencies for specific file formats
- Custom prompts for scientific, medical, and data visualization contexts
- Metadata extraction and organization
- Error handling and robust batch processing
- Integration with scientific workflows

**Source**: https://github.com/microsoft/markitdown (MIT License)

---

### 8. DOCX (Word Documents)
**Location**: `.claude/skills/document-skills/docx/`

**Capabilities**:
- Create and edit Word documents programmatically
- Work with OOXML format
- Manage comments and track changes
- Validate document structure
- Handle templates

**Scripts**:
- `document.py`: Core document manipulation
- `utilities.py`: Helper functions
- OOXML validation and manipulation tools

**References**:
- `docx-js.md`: JavaScript integration guide
- `ooxml.md`: OOXML format specification

---

### 9. PDF Documents
**Location**: `.claude/skills/document-skills/pdf/`

**Capabilities**:
- Extract text and metadata from PDFs
- Check bounding boxes and layout
- Work with fillable PDF forms
- Convert PDFs to images
- Extract form field information

**Scripts**:
- `check_bounding_boxes.py`: Analyze PDF layout
- `check_fillable_fields.py`: Identify form fields
- `fill_fillable_fields.py`: Populate PDF forms
- `convert_pdf_to_images.py`: PDF to image conversion
- `extract_form_field_info.py`: Extract form metadata

**References**:
- `forms.md`: Working with PDF forms
- `reference.md`: PDF manipulation reference

---

### 10. PPTX (PowerPoint Presentations)
**Location**: `.claude/skills/document-skills/pptx/`

**Capabilities**:
- Create and modify PowerPoint presentations
- Convert HTML to PowerPoint
- Manage slides and layouts
- Work with OOXML format
- Generate thumbnails

**Scripts**:
- `html2pptx.js`: HTML to PowerPoint conversion
- `inventory.py`: Presentation inventory management
- `rearrange.py`: Slide reordering
- `replace.py`: Content replacement
- `thumbnail.py`: Thumbnail generation

**References**:
- `html2pptx.md`: HTML conversion guide
- `ooxml.md`: OOXML format specification

---

### 11. XLSX (Excel Spreadsheets)
**Location**: `.claude/skills/document-skills/xlsx/`

**Capabilities**:
- Read and write Excel files
- Manage formulas and calculations
- Handle complex spreadsheet operations
- Recalculate formulas

**Scripts**:
- `recalc.py`: Formula recalculation utility

---

## How Skills Are Used

When you interact with the Scientific Writer CLI, Claude automatically:

1. **Detects relevant skills**: Based on your request, Claude identifies which skills to use
2. **Loads resources**: Accesses reference materials, scripts, and templates
3. **Applies best practices**: Follows the guidelines and standards in each skill
4. **Executes tools**: Uses scripts when needed for document manipulation or data processing

## Skill Integration

All skills are loaded from the `.claude/skills/` directory and are automatically available when you run the CLI. You don't need to manually select or activate them - Claude will use the appropriate skills based on your requests.

## Example Usage

### Using Scientific Writing Skill
```
> Help me structure a methods section for a randomized controlled trial
```
Claude will use the scientific-writing skill to provide IMRaD-compliant guidance.

### Using Literature Review Skill
```
> Create a literature review on CRISPR gene editing in agriculture
```
Claude will use literature-review skill to structure a comprehensive review.

### Using Document Skills
```
> Extract the data from Table 1 in results.pdf and create a summary
```
Claude will use the PDF skill to extract data and potentially the XLSX skill to organize it.

### Using MarkItDown Skill
```
> Convert all PDFs in the literature folder to Markdown
```
Claude will use the markitdown skill to batch convert files.

```
> Convert this PowerPoint presentation to Markdown with AI-generated descriptions
```
Claude will use markitdown with AI enhancement for detailed image descriptions.

### Using Peer Review Skill
```
> Review my discussion section for logical flow and adherence to reporting standards
```
Claude will use the peer-review skill to provide constructive feedback.

### Using Scholar Evaluation Skill
```
> Evaluate this paper using the ScholarEval framework
```
Claude will use the scholar-evaluation skill to provide systematic quantitative evaluation across 8 dimensions.

```
> Assess publication readiness for Nature Machine Intelligence
```
Claude will evaluate the paper and provide scores and recommendations for submission readiness.

### Using Research Grants Skill
```
> Help me write an NSF proposal for my computational neuroscience research
```
Claude will use the research-grants skill to provide NSF-specific guidance.

```
> I need to draft NIH Specific Aims for my cancer immunotherapy R01
```
Claude will help structure your 1-page specific aims using NIH best practices.

```
> What should I include in broader impacts for an NSF Materials Research proposal?
```
Claude will provide substantive broader impacts strategies aligned with NSF criteria.

### Using Scientific Schematics Skill
```
> Create a CONSORT flowchart for my clinical trial showing participant flow from screening (n=500) through randomization to final analysis
```
Claude will generate a methodology flowchart following CONSORT guidelines.

```
> Generate a circuit diagram for an RC low-pass filter
```
Claude will create an electrical circuit schematic using CircuitikZ or Schemdraw.

```
> Create a biological pathway diagram showing the MAPK signaling cascade from receptor to gene expression
```
Claude will visualize the signaling pathway with properly styled proteins and activation arrows.

```
> Design a block diagram showing the architecture of my data acquisition system with sensor, ADC, microcontroller, and wireless transmission
```
Claude will create a system architecture diagram with labeled components and data flow.

### 7. Venue Templates
**Location**: `.claude/skills/venue-templates/`

**Capabilities**:
- Query LaTeX templates for 50+ major journals and conferences
- Access grant proposal templates (NSF, NIH, DOE, DARPA)
- Retrieve poster templates for academic conferences
- View formatting requirements and submission guidelines
- Customize templates with author and project information
- Validate document formatting against venue requirements

**References**:
- `journals_formatting.md`: Requirements for Nature, Science, PLOS, IEEE, ACM, Cell Press, and other major journals
- `conferences_formatting.md`: ML, CS, biology conference paper formats (NeurIPS, ICML, ICLR, CVPR, CHI, ISMB, etc.)
- `posters_guidelines.md`: Poster design, sizes, layout principles, and best practices
- `grants_requirements.md`: Federal and private grant proposal formats (NSF, NIH, DOE, DARPA)

**Scripts**:
- `query_template.py`: Search and retrieve templates by venue name or keywords
- `customize_template.py`: Customize templates with author information
- `validate_format.py`: Check document compliance with venue requirements

**Assets**:
- `journals/`: LaTeX templates for Nature, Science, PLOS ONE, NeurIPS, and other major venues
- `posters/`: Academic poster templates (beamerposter, tikzposter, baposter)
- `grants/`: Grant proposal templates (NSF, NIH Specific Aims, DOE, DARPA)

**Features**:
- Comprehensive formatting guidelines for major publication venues
- Ready-to-use LaTeX templates with proper structure
- Helper scripts for template discovery and customization
- Formatting validation tools
- Integration with scientific writing workflow

**Use Cases**:
- **Journal submission**: Get proper formatting for Nature, Science, PLOS, IEEE, ACM journals
- **Conference papers**: Templates for NeurIPS, ICML, CVPR, CHI, and other major conferences
- **Research posters**: Professional poster templates for A0, A1, and US sizes
- **Grant proposals**: NSF, NIH R01, DOE, DARPA proposal templates with requirements
- **Format validation**: Check if your document meets venue specifications

**Example Usage**:

### Query Template for a Journal
```
> I need to submit to Nature
```
Claude will provide the Nature article template and formatting requirements.

### Get Conference Paper Template
```
> Show me the NeurIPS paper template
```
Claude will provide the NeurIPS conference paper template with anonymization guidelines.

### Grant Proposal Template
```
> I need an NSF proposal template
```
Claude will provide the NSF proposal template with all required sections and formatting.

### Conference Poster
```
> Create a research poster for ISMB conference
```
Claude will provide poster template and size specifications for the conference.

### Format Validation
```
> Check if my paper meets Nature's requirements
```
Claude can guide you through using the validation script to check formatting compliance.

---

## Adding Custom Skills

To add your own skills:

1. Create a new directory in `.claude/skills/`
2. Add a `SKILL.md` file with your skill definition
3. Optionally add `references/`, `scripts/`, and `assets/` subdirectories
4. Restart the CLI

The new skill will be automatically loaded and available.

