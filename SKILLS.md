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

## Document Manipulation Skills

### 4. DOCX (Word Documents)
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

### 5. PDF Documents
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

### 6. PPTX (PowerPoint Presentations)
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

### 7. XLSX (Excel Spreadsheets)
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

### Using Peer Review Skill
```
> Review my discussion section for logical flow and adherence to reporting standards
```
Claude will use the peer-review skill to provide constructive feedback.

## Adding Custom Skills

To add your own skills:

1. Create a new directory in `.claude/skills/`
2. Add a `SKILL.md` file with your skill definition
3. Optionally add `references/`, `scripts/`, and `assets/` subdirectories
4. Restart the CLI

The new skill will be automatically loaded and available.

