# Complete Features Guide

This guide provides a comprehensive overview of all features available in Scientific Writer v2.0.

## Table of Contents

1. [Document Generation](#document-generation)
2. [AI-Powered Capabilities](#ai-powered-capabilities)
3. [Intelligent Paper Detection](#intelligent-paper-detection)
4. [Data & File Integration](#data--file-integration)
5. [Document Conversion](#document-conversion)
6. [Developer Features](#developer-features)

---

## Document Generation

### Scientific Papers

Generate publication-ready papers in LaTeX with proper IMRaD structure.

**Supported Venues:**
- **Nature, Science** - High-impact journals with specific formatting
- **NeurIPS, ICML, ICLR** - Machine learning conferences
- **IEEE, ACM** - Engineering and computer science
- **Custom venues** - Describe any journal or conference

**Example Requests:**
```bash
> Create a Nature paper on CRISPR gene editing
> Write a NeurIPS paper on transformer architectures
> Generate an IEEE paper on signal processing
```

**Output Structure:**
```
paper_outputs/20241030_<topic>/
├── drafts/
│   ├── v1_draft.tex
│   ├── v1_draft.pdf
│   └── v2_draft.tex
├── final/
│   ├── manuscript.tex
│   └── manuscript.pdf
├── references/
│   └── references.bib
├── figures/
│   └── *.png, *.pdf
├── data/
│   └── *.csv, *.json
└── progress.md
```

### Research Posters

Professional conference posters using LaTeX beamerposter, tikzposter, or baposter.

**Features:**
- Full-page layouts with minimal margins
- Color schemes and visual design
- Accessibility and colorblind-safe palettes
- Standard sizes (A0, A1, 36×48")
- Quality control scripts

**Example:**
```bash
> Create a conference poster about my transformer paper
> Generate an A0 poster for NeurIPS with blue color scheme
```

### Grant Proposals

Agency-specific formatting for major U.S. funding sources.

**Supported Agencies:**

| Agency | Focus Areas | Key Components |
|--------|-------------|----------------|
| **NSF** | Basic research, education | Intellectual Merit + Broader Impacts |
| **NIH** | Biomedical research | Specific Aims (1 page), Research Strategy |
| **DOE** | Energy, physical sciences | TRLs, cost sharing, lab partnerships |
| **DARPA** | High-risk/high-reward | Heilmeier Catechism, PM engagement |

**Example:**
```bash
> Write an NSF proposal for quantum computing research
> Generate NIH R01 Specific Aims for cancer immunotherapy
> Create a DOE proposal for renewable energy storage
```

**Key Features:**
- Budget preparation and justification
- Review criteria alignment
- Timeline and milestone planning
- Broader impacts strategies (NSF)
- Preliminary data integration (NIH)

### Literature Reviews

Systematic literature reviews with citation management.

**Features:**
- Database search strategies (PubMed, Web of Science)
- Citation verification and formatting
- Synthesis and organization
- Multiple citation styles (APA, IEEE, Nature, etc.)

**Example:**
```bash
> Create a literature review on machine learning in healthcare
> Synthesize recent papers on quantum computing from 2023-2024
```

### Clinical Reports

Comprehensive clinical documentation with regulatory compliance.

**Report Types:**
- **Case Reports** - CARE-compliant reports for medical journals
- **Diagnostic Reports** - Radiology, pathology, laboratory reports
- **Clinical Trial Reports** - SAE reports, Clinical Study Reports (ICH-E3)
- **Patient Documentation** - SOAP notes, H&P, discharge summaries

**Features:**
- 12 professional templates based on industry standards
- HIPAA compliance and de-identification tools
- Regulatory compliance (FDA, ICH-GCP)
- Medical terminology validation
- 8 automated validation scripts

**Example:**
```bash
> Create a clinical case report for a rare disease presentation
> Generate a radiology report template for chest CT
> Write an SAE report for clinical trial adverse event
> Create a discharge summary for heart failure patient
```

### Scientific Schematics

Publication-quality diagrams and visualizations.

**Diagram Types:**
- **CONSORT flowcharts** - Clinical trial participant flow
- **Circuit diagrams** - Electrical schematics with CircuitikZ
- **Biological pathways** - Signaling cascades, metabolic networks
- **System architecture** - Block diagrams, data flow
- **Process flows** - Methodology diagrams, decision trees

**Features:**
- Vector graphics (TikZ/LaTeX)
- Colorblind-safe Okabe-Ito palette
- Programmatic generation with Python
- Publication-ready PDF/SVG/PNG output

**Example:**
```bash
> Create a CONSORT diagram for my clinical trial
> Generate a circuit diagram for an RC low-pass filter
> Design a biological pathway showing MAPK signaling
```

---

## AI-Powered Capabilities

### Real-Time Research Lookup

Powered by Perplexity Sonar Pro via OpenRouter API.

**Features:**
- Live internet search during paper generation
- Recent publications and preprints
- Fact-checking and verification
- Up-to-date statistics and data

**Setup:**
```bash
# Add to .env file
echo "OPENROUTER_API_KEY=your_key" >> .env
```

**Automatic Usage:**
The research lookup is automatically invoked when:
- You request recent research (e.g., "papers from 2024")
- Claude needs to verify facts or statistics
- Literature search is needed
- Current events or recent developments are mentioned

**Example:**
```bash
> Create a paper on recent advances in quantum computing (2024)
# Automatically searches for latest research

> What are the current success rates for CAR-T therapy?
# Looks up latest clinical data
```

### Peer Review with ScholarEval

Systematic quantitative evaluation framework based on research (arXiv:2510.16234).

**8 Evaluation Dimensions:**
1. **Problem Formulation** - Clarity, significance, novelty
2. **Literature Review** - Coverage, synthesis, gaps
3. **Methodology** - Rigor, validity, reproducibility
4. **Data Collection** - Quality, appropriateness, ethics
5. **Analysis** - Statistical rigor, interpretation
6. **Results** - Clarity, completeness, visualization
7. **Writing Quality** - Structure, clarity, grammar
8. **Citations** - Relevance, recency, completeness

**Scoring:**
- 1-5 scale per dimension
- Overall score thresholds:
  - **4.5+** - Exceptional (top-tier ready)
  - **4.0-4.4** - Strong (minor revisions)
  - **3.5-3.9** - Good (major revisions)
  - **3.0-3.4** - Acceptable (significant revisions)
  - **<3.0** - Needs major rework

**Example:**
```bash
> Evaluate this paper using the ScholarEval framework
> Assess publication readiness for Nature Machine Intelligence
> Review the methods section for rigor and completeness
```

### Iterative Editing

Context-aware revision suggestions that understand your paper's structure and content.

**Features:**
- Maintains consistency across sections
- Preserves your writing style
- Tracks changes between versions
- Suggests improvements based on venue requirements

**Example:**
```bash
> Improve the introduction to better motivate the problem
> Make the discussion more concise
> Add transition sentences between paragraphs in the results
```

---

## Intelligent Paper Detection

Automatically identifies when you're referring to existing papers without needing to specify paths.

### How It Works

The system analyzes your input for:
1. **Continuation keywords**: "continue", "update", "edit", "the paper"
2. **Search keywords**: "find", "look for", "show me", "where is"
3. **Topic matching**: Keywords from paper directory names
4. **Temporal context**: Defaults to most recent paper when ambiguous

### Continuation Keywords

Automatically resumes work on the current or most recent paper:

```bash
> continue
> update the paper
> edit my paper
> add a conclusion section
> fix the references
> compile the poster
> generate the PDF
```

### Search Keywords

Finds specific papers by topic:

```bash
> find the acoustics paper
> look for the quantum computing paper
> show me the CRISPR paper
> where is the transformer paper
```

### Topic Matching

Matches based on directory names (format: `YYYYMMDD_HHMMSS_topic`):

```bash
# Finds 20241027_090109_acoustics_vinayak_agarwal/
> update the acoustics paper

# Finds 20251029_130950_transformers_ai_paper/
> continue working on the transformers paper
```

### Starting a New Paper

Explicitly start fresh:

```bash
> new paper on climate change
> start fresh with a different topic
> create a new paper about quantum computing
```

---

## Data & File Integration

### Automatic Data Handling

Simply drop files into the `data/` folder at the project root.

**File Routing:**
- **Images** (png, jpg, svg, etc.) → `figures/`
- **Data files** (csv, json, txt, xlsx) → `data/`
- **Original files** automatically deleted after copying

**Supported Image Formats:**
`.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.tiff`, `.svg`, `.webp`, `.ico`

**Example Workflow:**
```bash
# 1. Copy your files
cp experiment_results.csv ~/Documents/claude-scientific-writer/data/
cp performance_graph.png ~/Documents/claude-scientific-writer/data/

# 2. Start the CLI
scientific-writer

# 3. Files are automatically detected and processed
> Create a paper analyzing the experimental results
# ✓ Files copied to paper's data/ and figures/
# ✓ Original files deleted from data/
```

### Programmatic Data Files

Use the API to specify data files explicitly:

```python
async for update in generate_paper(
    query="Analyze the experimental results",
    data_files=[
        "./experiment_results.csv",
        "./figures/performance.png",
        "./supplementary_data.json"
    ]
):
    # Files are processed and included
    pass
```

**Note:** When using the API, original files are **not** deleted (for safety).

### File Context

All included files are:
- Copied to appropriate directories
- Made available as context to Claude
- Can be referenced in the paper
- Listed in the data files message

---

## Document Conversion

### MarkItDown - Universal File Converter

Convert 15+ file formats to Markdown for LLM processing.

**Supported Formats:**
- **Documents**: PDF, DOCX, PPTX, XLSX
- **Media**: Images (with AI descriptions), Audio (transcription)
- **Web**: HTML, YouTube (video transcription)
- **Data**: CSV, JSON, XML
- **Code**: Various programming languages

**Features:**
- AI-enhanced image descriptions using Claude Sonnet 4.5
- OCR for scanned documents
- Speech-to-text for audio files
- Batch processing with parallel execution
- Scientific literature metadata extraction

**Example:**
```bash
> Convert all PDFs in the literature folder to Markdown
> Extract data from this Excel spreadsheet
> Transcribe the interview audio file
> Convert this PowerPoint to Markdown with AI descriptions
```

### Document Manipulation

#### DOCX (Word Documents)
- Create and edit Word documents programmatically
- Manage comments and track changes
- Validate document structure
- Work with templates

#### PDF Documents
- Extract text and metadata
- Analyze PDF layout and bounding boxes
- Fill PDF forms
- Convert PDFs to images

#### PPTX (PowerPoint)
- Create and modify presentations
- Convert HTML to PowerPoint
- Generate thumbnails
- Manage slides and layouts

#### XLSX (Excel)
- Read and write Excel files
- Recalculate formulas
- Handle complex spreadsheet operations

---

## Developer Features

### Programmatic API

Full async Python API with comprehensive type hints.

**Core Function:**
```python
from scientific_writer import generate_paper

async def generate_paper(
    query: str,
    output_dir: Optional[str] = None,
    api_key: Optional[str] = None,
    model: str = "claude-sonnet-4-20250514",
    data_files: Optional[List[str]] = None,
    cwd: Optional[str] = None,
) -> AsyncGenerator[Dict[str, Any], None]
```

**Type-Safe Models:**
```python
from scientific_writer import (
    ProgressUpdate,  # Progress information
    PaperResult,     # Final result with all paper info
    PaperMetadata,   # Paper metadata (title, date, word count)
    PaperFiles,      # All file paths (PDF, TeX, BibTeX, etc.)
)
```

### Progress Streaming

Real-time updates during generation:

```python
async for update in generate_paper("Create a paper"):
    if update["type"] == "progress":
        # Progress update
        stage = update["stage"]        # initialization|research|writing|compilation|complete
        percentage = update["percentage"]  # 0-100
        message = update["message"]     # Human-readable message
        
        print(f"[{percentage}%] {message}")
```

### Comprehensive Results

Final result includes everything about the generated paper:

```python
if update["type"] == "result":
    # Status
    status = update["status"]  # success|partial|failed
    
    # Files
    pdf = update["files"]["pdf_final"]
    tex = update["files"]["tex_final"]
    bib = update["files"]["bibliography"]
    figures = update["files"]["figures"]  # List of figure paths
    
    # Metadata
    title = update["metadata"]["title"]
    word_count = update["metadata"]["word_count"]
    
    # Citations
    citation_count = update["citations"]["count"]
    
    # Compilation
    compiled = update["compilation_success"]
    
    # Errors (if any)
    errors = update["errors"]
```

### Error Handling

Graceful error handling with detailed information:

```python
try:
    async for update in generate_paper(query):
        if update["type"] == "result":
            if update["status"] == "failed":
                print(f"Errors: {update['errors']}")
            elif update["status"] == "partial":
                print("TeX created but PDF compilation failed")
            else:
                print("Success!")
except ValueError as e:
    print(f"Configuration error: {e}")
```

### Custom Configuration

Override defaults for your use case:

```python
async for update in generate_paper(
    query="Create a paper",
    output_dir="./my_custom_directory",
    api_key="sk-ant-custom-key",
    model="claude-sonnet-4-20250514",
    data_files=["data.csv"],
    cwd="/path/to/project"
):
    pass
```

---

## See Also

- [API Reference](API.md) - Complete API documentation
- [Skills Overview](SKILLS.md) - All available skills and capabilities
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues and solutions
- [Development Guide](DEVELOPMENT.md) - Contributing and development
- [Changelog](../CHANGELOG.md) - Version history and updates

