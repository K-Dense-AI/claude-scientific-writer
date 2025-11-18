# Changelog

All notable changes to the Scientific Writer project will be documented in this file.

## [Unreleased]

---

## [2.7.0] - 2025-01-22

### 🎯 Claude Code Plugin Focus

This release emphasizes using Scientific Writer as a **Claude Code (Cursor) plugin**, making it easier than ever to access scientific writing capabilities directly in your IDE.

### ✨ Added

#### Enhanced Plugin Experience

- **Streamlined Plugin Installation** - Improved documentation and setup process for Claude Code plugin usage
  - Clear step-by-step installation guide
  - Marketplace integration instructions
  - Local development and testing guide
  - Troubleshooting for common plugin issues

- **Optimized Plugin Structure** - Better organization for plugin usage
  - All 19+ skills automatically available when plugin is installed
  - `/scientific-writer:init` command creates comprehensive `CLAUDE.md` configuration
  - Skills accessible directly in IDE without additional setup
  - Template files optimized for plugin context

- **Plugin-First Documentation** - Enhanced README with prominent plugin section
  - Plugin installation prominently featured at the top
  - Clear examples for using skills within Claude Code
  - Plugin testing guide for developers
  - Troubleshooting section for plugin-specific issues

### 🔧 Improvements

#### Better IDE Integration

- **Seamless Skill Access** - All skills work natively within Claude Code
  - No need to switch between CLI and IDE
  - Skills automatically discoverable via `@skill-name` syntax
  - Context-aware skill suggestions
  - Direct file editing and creation within IDE

- **Improved Initialization Command** - Enhanced `/scientific-writer:init` experience
  - Better handling of existing `CLAUDE.md` files
  - Backup and merge options for existing configurations
  - Clear feedback on what was installed
  - Summary of available skills and capabilities

- **Plugin-Optimized Workflows** - Workflows designed for IDE usage
  - File operations work directly in project directory
  - No need for separate data folders - use project structure
  - Skills integrate with IDE's file system
  - Better progress feedback within IDE context

### 📝 Documentation Updates

- **Plugin Quick Start** - New quick start guide for plugin users
- **Plugin Examples** - Real-world examples of using skills in Claude Code
- **Skill Reference** - Complete list of all 19+ available skills
- **Troubleshooting** - Common plugin installation and usage issues

### 🎯 Usage Examples

#### Plugin Installation

```bash
# Add marketplace
/plugin marketplace add https://github.com/K-Dense-AI/claude-scientific-writer

# Install plugin
/plugin install claude-scientific-writer

# Initialize in your project
/scientific-writer:init
```

#### Using Skills in Claude Code

```bash
# Create a paper (skill automatically used)
> Create a Nature paper on CRISPR gene editing

# Use specific skills
> @research-lookup Find recent papers on mRNA vaccines
> @peer-review Evaluate this manuscript
> @clinical-reports Create a case report for this patient

# Generate documents
> Create an NSF grant proposal for quantum computing
> Generate conference slides from my paper
> Create a research poster for NeurIPS
```

### 💡 Key Benefits for Plugin Users

- **No CLI Required** - Everything works directly in Claude Code
- **Instant Access** - All 19+ skills available immediately after installation
- **IDE Integration** - Files created and edited directly in your project
- **Context Aware** - Skills understand your project structure
- **Seamless Workflow** - No switching between tools

### 🚀 Migration from CLI to Plugin

For existing CLI users:
- Plugin provides same functionality with better IDE integration
- Skills work identically in both CLI and plugin modes
- Can use both CLI and plugin in the same project
- Plugin is recommended for IDE-based workflows

### 📦 Plugin Structure

```
claude-scientific-writer/
├── .claude-plugin/          # Plugin metadata (if exists)
├── commands/                 # Plugin commands
│   └── scientific-writer-init.md
├── skills/                   # All 19+ skills
│   ├── research-lookup/
│   ├── peer-review/
│   ├── clinical-reports/
│   └── ... (16 more)
├── templates/                # CLAUDE.md template
│   └── CLAUDE.scientific-writer.md
└── ... (Python package files)
```

### 🎨 Plugin Features

- **19+ Specialized Skills** - Research, writing, review, and more
- **One-Command Setup** - `/scientific-writer:init` configures everything
- **Skill Discovery** - Ask "What skills are available?" to see full list
- **Direct Integration** - Skills work with IDE's file operations
- **Template System** - Professional templates for all document types

---

## [2.6.1] - 2025-11-17

### ⚡ Performance

#### Parallel Research Lookup System

- **Dramatic Time Savings** - Parallel execution of research queries reduces lookup time by up to 10x
  - Sequential workflow: N × ~12 seconds per query
  - Parallel workflow: ~15-20 seconds regardless of N (up to worker limit)
  - Example: 20 queries now take ~20 seconds instead of 4 minutes
  
- **AI-Powered Topic Identification** - Automatic extraction of research topics from text
  - Intelligent identification of key research questions
  - Saves time on manual topic extraction
  - Topics saved to reviewable/editable file format
  
- **Flexible Workflow Patterns** - Three usage modes for different scenarios:
  1. **Quick & Automated** - One command for instant results
  2. **Review & Refine** - Two-step process with human review of topics
  3. **Manual Control** - Bring your own topic list
  
- **Smart Query Complexity Assessment** - Automatic model selection
  - Simple queries → Fast 'pro' model
  - Complex queries (comparisons, analysis) → 'reasoning' model
  - Optimizes for both speed and quality

### 🔧 Improvements

#### Enhanced Research Lookup Features

- **Parallel Execution Engine** - Concurrent API calls with ThreadPoolExecutor
  - Configurable worker count (default: 5, max: 10)
  - Intelligent rate limiting and error handling
  - Progress tracking for batch operations
  
- **Topic Management** - File-based topic handling
  - `save_topics_to_file()` - Save identified topics for review
  - `load_topics_from_file()` - Load and process topic lists
  - Human-readable format for easy editing
  
- **New Research Methods**:
  - `identify_research_topics()` - AI-powered topic extraction
  - `parallel_lookup()` - Concurrent research execution
  - `identify_and_research()` - Combined workflow (identify + research)
  - `batch_lookup()` - Enhanced with `parallel` and `max_workers` parameters

### 🎯 Usage Examples

#### CLI - Quick Parallel Research

```bash
# Automatic workflow (one command)
python research_lookup.py --identify input.txt \
    --topics-file topics.txt \
    --parallel --max-workers 10 \
    --output results.json

# ✅ Complete results in < 1 minute (regardless of topic count)
```

#### CLI - Review & Refine Workflow

```bash
# Step 1: Identify topics
python research_lookup.py --identify input.txt \
    --topics-file topics.txt

# Step 2: Review/edit topics.txt manually

# Step 3: Research in parallel
python research_lookup.py --topics-file topics.txt \
    --parallel --max-workers 10 \
    --output results.json
```

#### Programmatic API - Parallel Lookup

```python
from research_lookup import ResearchLookup

research = ResearchLookup()

# Identify and research in one call
results = research.identify_and_research(
    text_file="research_proposal.txt",
    parallel=True,
    max_workers=10,
    output_file="results.json"
)

# Manual topics with parallel execution
topics = ["CRISPR gene editing", "mRNA vaccines", "AI in medicine"]
results = research.parallel_lookup(
    topics, 
    max_workers=10,
    show_progress=True
)
```

### 💡 Key Benefits

- **10x Faster** - Parallel execution dramatically reduces research time
- **Intelligent** - AI-powered topic identification and complexity assessment
- **Flexible** - Multiple workflow patterns for different use cases
- **Scalable** - Handle large research projects efficiently
- **Reliable** - Built-in error handling and rate limiting
- **Human-in-the-Loop** - Review/edit topics before research execution

### 📝 Files Enhanced

- `skills/research-lookup/research_lookup.py` - Added parallel execution engine
- `skills/research-lookup/WORKFLOW_GUIDE.md` - Comprehensive 381-line workflow guide with visual diagrams
- `skills/research-lookup/test_parallel.py` - Test suite for parallel features
- `skills/research-lookup/UPGRADE_SUMMARY.md` - Migration guide for new features

### 🚀 Performance Impact

**Before (Sequential):**
- 5 queries: ~60 seconds
- 10 queries: ~120 seconds
- 20 queries: ~240 seconds

**After (Parallel with 10 workers):**
- 5 queries: ~15 seconds ⚡ 4x faster
- 10 queries: ~18 seconds ⚡ 6.6x faster
- 20 queries: ~20 seconds ⚡ 12x faster

---

## [2.6.0] - 2025-11-17

### ✨ Added

#### Professional Hypothesis Generation Reports

- **Scientific Hypothesis Generation Skill** - Comprehensive framework for developing testable scientific hypotheses
  - Systematic workflow from observations to testable predictions
  - Evidence-based approach with literature synthesis
  - Generates 3-5 competing mechanistic hypotheses
  - Professional LaTeX reports with beautiful colored boxes
  - Structured as concise main text (8-14 pages) with comprehensive appendices

- **Hypothesis Report Features**
  - **Colored Box System** - Visual organization with custom LaTeX environments:
    - 5 distinct hypothesis boxes (blue, green, purple, teal, orange)
    - Prediction boxes for testable predictions (amber)
    - Comparison boxes for distinguishing hypotheses (steel gray)
    - Evidence boxes for highlighting key support (light blue)
    - Summary boxes for executive overview
  - **Professional Structure**:
    - Executive Summary - One-page high-level overview
    - Competing Hypotheses - Each in dedicated colored box with mechanism, evidence, and assumptions
    - Testable Predictions - Specific, measurable predictions for each hypothesis
    - Critical Comparisons - How to experimentally distinguish between hypotheses
  - **Comprehensive Appendices**:
    - Appendix A: Literature Review (40-60+ citations)
    - Appendix B: Detailed Experimental Designs
    - Appendix C: Quality Assessment Tables
    - Appendix D: Supplementary Evidence and Analogous Systems

- **Rigorous Quality Framework** - Seven-dimensional evaluation system:
  - **Testability** - Can be empirically tested with current methods
  - **Falsifiability** - Clear conditions that would disprove hypothesis
  - **Parsimony** - Simplest explanation fitting the evidence (Occam's Razor)
  - **Explanatory Power** - Accounts for substantial portion of observations
  - **Scope** - Range of phenomena and contexts covered
  - **Consistency** - Alignment with established knowledge
  - **Novelty** - New insights beyond restating known facts

- **Comprehensive Resources**
  - `hypothesis_generation.sty` - Professional LaTeX style package with colored boxes
  - `hypothesis_report_template.tex` - Complete template with main text and appendices
  - `hypothesis_quality_criteria.md` - Detailed evaluation framework (200+ lines)
  - `experimental_design_patterns.md` - Common approaches across domains
  - `literature_search_strategies.md` - Effective search techniques
  - `FORMATTING_GUIDE.md` - Quick reference for all formatting features

### 🔧 Improvements

#### Enhanced Scientific Workflow

- **Literature Integration** - Dual search strategy:
  - PubMed for biomedical topics
  - General web search for broader scientific domains
  - Synthesis of 50+ references per report (15-20 main text, 40-60+ appendix)
  - Evidence-based hypothesis development

- **Mechanistic Focus** - Emphasis on explanatory mechanisms:
  - Each hypothesis explains HOW and WHY (not just WHAT)
  - Multiple levels of explanation (molecular, cellular, systemic, population)
  - Novel combinations of known mechanisms
  - Challenge of assumptions in existing explanations

- **Experimental Design** - Practical testing strategies:
  - Laboratory experiments (in vitro, in vivo, computational)
  - Observational studies (cross-sectional, longitudinal, case-control)
  - Clinical trials (where applicable)
  - Natural experiments and quasi-experimental designs

### 🎯 Usage Examples

#### CLI - Generate Hypothesis Report

```bash
scientific-writer
> Generate competing hypotheses for why NAD+ levels decline with aging

# The system will:
# ✓ Search biomedical literature via PubMed and web
# ✓ Synthesize current understanding
# ✓ Generate 3-5 mechanistic hypotheses
# ✓ Evaluate each hypothesis on 7 quality dimensions
# ✓ Design experiments to test predictions
# ✓ Create professional LaTeX report with colored boxes
# ✓ Compile to beautiful PDF
```

#### API - Programmatic Hypothesis Generation

```python
import asyncio
from scientific_writer import generate_paper

async def main():
    async for update in generate_paper(
        "What mechanisms could explain the obesity paradox in heart failure patients?"
    ):
        if update["type"] == "progress":
            print(f"[{update['percentage']}%] {update['message']}")
        else:
            print(f"Report: {update['files']['pdf_final']}")

asyncio.run(main())
```

#### Research Applications

```bash
# Cancer biology
> Why do some tumors respond to immunotherapy while others don't?

# Neuroscience
> What mechanisms could explain the therapeutic effect of ketamine in depression?

# Climate science
> Generate hypotheses for accelerated ice sheet melting in Greenland

# Materials science
> Why does this novel catalyst show unexpected selectivity?
```

### 💡 Key Features

- **Evidence-Based** - All hypotheses grounded in literature with extensive citations
- **Mechanistic** - Focus on explanatory mechanisms, not just descriptive patterns
- **Testable** - Specific, measurable predictions for each hypothesis
- **Comprehensive** - Multiple competing explanations systematically evaluated
- **Beautiful** - Professional LaTeX formatting with colored visual organization
- **Rigorous** - Seven-dimensional quality assessment framework
- **Practical** - Detailed experimental designs ready for implementation

### 📝 Files Added

- `skills/hypothesis-generation/` - Complete hypothesis generation skill
  - `SKILL.md` - Comprehensive workflow documentation (200+ lines)
  - `assets/hypothesis_generation.sty` - LaTeX style package with colored boxes
  - `assets/hypothesis_report_template.tex` - Professional report template
  - `assets/FORMATTING_GUIDE.md` - Quick reference for formatting
  - `references/hypothesis_quality_criteria.md` - Evaluation framework
  - `references/experimental_design_patterns.md` - Design strategies
  - `references/literature_search_strategies.md` - Search techniques

### 🎨 Report Structure

The hypothesis generation system creates beautifully formatted reports:

**Main Text (Concise):**
- Executive Summary (1 page)
- Competing Hypotheses (3-5 hypotheses in colored boxes)
- Testable Predictions (amber boxes)
- Critical Comparisons (gray boxes)

**Appendices (Comprehensive):**
- Literature Review (40-60+ citations)
- Experimental Designs (detailed protocols)
- Quality Assessment (systematic evaluation)
- Supplementary Evidence (supporting data)

### 🔬 Scientific Rigor

The system ensures high-quality hypotheses through:

1. **Systematic Literature Search** - Comprehensive review of existing evidence
2. **Multiple Hypotheses** - 3-5 competing explanations, not just one
3. **Quality Evaluation** - Seven-dimensional assessment framework
4. **Experimental Tests** - Detailed designs to distinguish hypotheses
5. **Clear Predictions** - Specific, quantitative, falsifiable predictions
6. **Professional Presentation** - Publication-ready LaTeX reports

---

## [2.5.0] - 2025-11-11

### ✨ Added

#### Scientific Slides & Presentation System

- **Professional Presentation Generation** - Create high-quality scientific slides directly from research papers or topics
  - Support for academic conferences, research seminars, and institutional presentations
  - Beautiful LaTeX Beamer templates with modern, professional designs
  - Automatic content structuring optimized for scientific communication
  - Integration with existing paper workflows

- **Comprehensive Presentation Skill** - New `scientific-slides` skill with extensive resources
  - **Design Guidelines** - 663-line comprehensive guide covering:
    - Visual hierarchy and layout principles
    - Color theory and accessibility (WCAG 2.1 compliance)
    - Typography best practices for presentations
    - Data visualization guidelines
    - Animation and transition recommendations
    - Venue-specific formatting (conference dimensions, aspect ratios)
  - **LaTeX Beamer Templates** - Multiple professional themes ready to use
  - **Presentation Assets** - Icons, diagrams, and visual elements
  - **Example Scripts** - Python automation for presentation creation
  - **Reference Materials** - Best practices for scientific presentations

- **PowerPoint Conversion Support** - Generate both LaTeX and PowerPoint formats
  - Python-based conversion scripts using `python-pptx`
  - Preservation of layout, formatting, and design elements
  - Support for complex slide structures and animations
  - Export to multiple formats (PDF, PPTX)

### 🔧 Improvements

#### Enhanced Document Generation Workflow

- **Intelligent Presentation Detection** - Automatic recognition of presentation requests
  - Detects keywords like "presentation", "slides", "PowerPoint", "deck"
  - Routes to appropriate templates and formatting
  - Optimizes content structure for visual delivery

- **Better Template Organization** - Improved skill system architecture
  - Clear separation of document types (papers, posters, slides, grants, reports)
  - Easier access to venue-specific templates
  - Enhanced metadata and tagging for template discovery

#### Output Organization

- **Presentation-Specific Directories** - Organized output structure
  - `drafts/` - LaTeX source files and initial versions
  - `final/` - Compiled PDFs and PowerPoint files
  - `figures/` - Presentation graphics and diagrams
  - `references/` - Bibliography files
  - `slide_images/` - Individual slide exports

### 🎯 Usage Examples

#### CLI - Generate Scientific Presentation

```bash
scientific-writer
> Create a conference presentation on The AI Scientist framework by Sakana AI

# The system will:
# ✓ Generate professional Beamer slides
# ✓ Structure content for visual delivery
# ✓ Include diagrams and figures
# ✓ Compile to PDF
# ✓ Optionally convert to PowerPoint
```

#### API - Programmatic Presentation Generation

```python
import asyncio
from scientific_writer import generate_paper

async def main():
    async for update in generate_paper(
        "Create a research seminar presentation on CRISPR applications in agriculture"
    ):
        if update["type"] == "progress":
            print(f"[{update['percentage']}%] {update['message']}")
        else:
            print(f"Presentation: {update['files']['pdf_final']}")

asyncio.run(main())
```

#### Convert Paper to Slides

```bash
# Place your paper in the data folder
cp my_paper.pdf data/

scientific-writer
> Convert this paper into a 20-minute conference presentation

# The system will:
# ✓ Extract key findings from the paper
# ✓ Structure slides for time limit
# ✓ Create visual representations
# ✓ Generate speaker notes
```

### 💡 Key Features

- **Professional Quality** - Publication-ready slides following best practices
- **Scientific Accuracy** - Maintains rigor while optimizing for visual communication
- **Flexible Formats** - LaTeX Beamer, PDF, and PowerPoint output
- **Accessibility** - WCAG 2.1 compliant color schemes and layouts
- **Time Optimization** - Automatic content pacing for different presentation lengths
- **Visual Design** - Modern, clean aesthetics appropriate for academic settings

### 📝 Files Added/Modified

- `scientific_writer/.claude/skills/scientific-slides/` - Complete presentation skill directory
  - `assets/powerpoint_design_guide.md` - Comprehensive 663-line design guide
  - Additional templates, scripts, and references
- Documentation updates reflecting new presentation capabilities

### 🎨 Design Philosophy

The scientific slides system follows evidence-based design principles:
- **Cognitive Load Theory** - Minimizing extraneous information
- **Dual Coding Theory** - Combining verbal and visual information
- **Evidence-Based Medicine Presentation** - CONSORT/PRISMA diagram standards
- **Academic Communication Best Practices** - Nature, Science, Cell presentation guidelines

---

## [2.4.0] - 2025-11-07

### ✨ Added

#### Smart File Routing System

- **Intelligent File Categorization** - Automatic routing of files based on type and purpose
  - **Manuscript files** (.tex only) → `drafts/` folder [EDITING MODE triggered]
  - **Source/Context files** (.md, .docx, .pdf) → `sources/` folder [REFERENCE materials]
  - **Image files** (.png, .jpg, .svg, etc.) → `figures/` folder
  - **Data files** (.csv, .json, .xlsx, .txt, etc.) → `data/` folder
  - **Other files** → `sources/` folder [CONTEXT]

- **New Sources Directory** - Dedicated folder for reference and context materials
  - Separate location for .md, .docx, .pdf files used as reference
  - Clear distinction between editable manuscripts and supporting materials
  - Better organization of project resources

### 🔧 Improvements

#### Enhanced Manuscript Editing Workflow

- **Refined EDITING MODE Detection** - Only .tex files in drafts/ trigger EDITING MODE
  - Previous behavior: .tex, .md, .docx, .pdf all triggered editing mode
  - New behavior: Only .tex files are treated as editable manuscripts
  - .md, .docx, .pdf files are now reference materials in sources/
  - Clearer user experience with more predictable behavior

- **Improved File Processing** - Better error handling and user feedback
  - Enhanced progress reporting during file copying operations
  - Separate counters for manuscripts, sources, data, and images
  - Clear indicators showing where each file type is being copied
  - More informative CLI output throughout the file processing workflow

- **Updated Documentation** - Comprehensive updates to system instructions
  - Clarified file routing rules in WRITER.md
  - Updated CLI help text with new file categorization
  - Enhanced welcome message explaining file handling
  - Better examples demonstrating the workflow

### 🗑️ Removed

- **CLAUDE.md** - Consolidated system instructions
  - Removed redundant CLAUDE.md file from project root
  - All system instructions now centralized in `.claude/WRITER.md` and `scientific_writer/.claude/WRITER.md`
  - Reduces confusion and maintenance overhead

### 📝 Files Modified

- `scientific_writer/cli.py` - Enhanced file routing and user feedback
- `scientific_writer/core.py` - New file categorization functions and processing logic
- `scientific_writer/utils.py` - Added sources/ directory scanning
- `.claude/WRITER.md` - Updated file routing documentation
- `scientific_writer/.claude/WRITER.md` - Updated file routing rules

### 🎯 Usage Example

```bash
# Place various files in the data folder
cp my_paper.tex data/           # → drafts/ (EDITING MODE)
cp background.pdf data/          # → sources/ (REFERENCE)
cp dataset.csv data/             # → data/
cp figure1.png data/             # → figures/

# Run scientific writer
scientific-writer

# The system will:
# ✓ Route .tex to drafts/ and activate EDITING MODE
# ✓ Copy .pdf to sources/ as reference material
# ✓ Copy .csv to data/ folder
# ✓ Copy .png to figures/ folder
# ✓ Provide clear feedback for each operation

> "Improve the introduction using the background material"
```

### 💡 Key Benefits

- **Better Organization** - Clear separation between manuscripts, sources, data, and figures
- **Predictable Behavior** - Consistent file routing based on file types
- **Enhanced Clarity** - Users know exactly where their files will go
- **Improved Workflow** - Easier to manage complex projects with multiple file types
- **Better Context** - Reference materials clearly separated from editable content

---

## [2.3.2] - 2025-11-06

### 🔧 Improvements

- Package maintenance and version update

---

## [2.3.1] - 2025-11-05

### 🔧 Improvements

- Package maintenance and version update

---

## [2.3.0] - 2025-11-04

### ✨ Added

#### Manuscript Editing Workflow

- **Automatic Editing Mode Detection** - Smart file routing based on file type
  - Manuscript files (`.tex`, `.md`, `.docx`, `.pdf`) automatically copied to `drafts/` folder
  - Image files routed to `figures/` folder
  - Data files routed to `data/` folder
  - System recognizes manuscripts in drafts/ as editing tasks, not creation from scratch
  
- **EDITING MODE Context** - Clear feedback and instructions
  - Prominent `⚠️ EDITING MODE` warning displayed when manuscripts detected
  - Agent receives explicit instructions to edit existing manuscript
  - Visual `[EDITING MODE]` indicators in CLI output
  - Progress messages show manuscript file counts separately
  
- **Enhanced File Processing** - Improved data file handling
  - New `get_manuscript_extensions()` function in `core.py`
  - Updated `process_data_files()` to handle three file categories
  - Updated `create_data_context_message()` with editing mode detection
  - Manuscript files tracked separately in processed_info dictionary

### 🔧 Improvements

- **System Instructions (WRITER.md)** - Added comprehensive manuscript editing workflow section
  - Clear instructions for handling manuscript files from data folder
  - Defined file routing rules by file type
  - Detailed editing workflow for the agent
  - Example scenarios demonstrating the workflow
  
- **CLI User Experience** - Better visibility into file processing
  - Welcome message explains manuscript file routing
  - File processing shows separate counts for manuscripts, data, and images
  - Help text updated with manuscript editing information
  - Consistent `[EDITING MODE]` indicators throughout
  
- **API Progress Updates** - Enhanced feedback in programmatic mode
  - Progress messages report manuscript files separately
  - Clear indication when manuscripts are copied to drafts/
  - Better tracking of file processing stages

### 📝 Files Modified

- `scientific_writer/.claude/WRITER.md` - Added "CRITICAL: Manuscript Editing Workflow" section
- `scientific_writer/core.py` - Added manuscript detection and routing logic
- `scientific_writer/cli.py` - Updated UI to show editing mode indicators
- `scientific_writer/api.py` - Enhanced progress reporting for manuscript files

### 🎯 Usage Example

```bash
# Place a manuscript file in the data folder
cp my_paper.tex data/

# Run scientific writer
scientific-writer

# The system will:
# ✓ Detect my_paper.tex as a manuscript file
# ✓ Copy it to drafts/ folder (not data/)
# ✓ Display [EDITING MODE] indicator
# ✓ Treat the task as editing, not creation

> "Improve the introduction and add 5 more citations"
```

---

## [2.2.1] - 2025-11-04

### 🔧 Improvements

- Minor bug fixes and stability improvements
- Documentation updates
- Enhanced error handling

---

## [2.2.0] - 2025-11-04

### ✨ Added

#### New Skills & Capabilities

- **Clinical Reports Skill** - Comprehensive clinical documentation system
  - Four major report types: case reports, diagnostic reports, clinical trial reports, patient documentation
  - CARE-compliant case report writing for journal publication
  - Diagnostic reports (radiology/ACR, pathology/CAP, laboratory/CLSI)
  - Clinical trial documentation (SAE reports, CSRs following ICH-E3)
  - Patient clinical notes (SOAP, H&P, discharge summaries, consultations)
  - 12 professional templates based on industry standards
  - 8 comprehensive reference guides (570-745 lines each)
  - 8 validation and automation Python scripts
  - HIPAA compliance and de-identification tools
  - Regulatory compliance (FDA 21 CFR Part 11, ICH-GCP)
  - Medical terminology standards (SNOMED-CT, LOINC, ICD-10, CPT)
  - Quality assurance checklists
  - Integration with scientific-writing and peer-review skills

### 🔧 Improvements

- Enhanced medical and clinical documentation capabilities
- Expanded document generation beyond academic papers to clinical settings
- Added healthcare regulatory compliance features
- Improved template library with industry-standard medical formats

### 📝 Documentation

- Updated README.md to include clinical reports in document generation
- Updated docs/SKILLS.md with comprehensive clinical-reports skill documentation
- Updated docs/FEATURES.md with clinical reports examples
- Added clinical-reports/README.md with quick start guide

---

## [2.1.0] - 2025-11-01

### ✨ Added

#### New Skills

- **Citation Management Skill** - Advanced citation quality control system
  - Validates all citation metadata for completeness and accuracy
  - Checks for proper author names, titles, venues, DOIs, and URLs
  - Reduces AI hallucinations in bibliographic references
  - Ensures citations meet publication standards
  - Helps avoid citation-related desk rejects

- **Venue Templates Skill** - Comprehensive academic submission templates
  - Journal templates (Nature, Science, Cell, PNAS, etc.)
  - Conference templates (NeurIPS, ICML, CVPR, ACL, etc.)
  - Poster templates with venue-specific dimensions and styles
  - Grant proposal templates (NSF, NIH, DOE, DARPA)
  - Venue-specific formatting guidelines and requirements
  - Reference documents with submission best practices
  - Example usage scripts for common venues

### 🔧 Improvements

- Enhanced citation accuracy through automated metadata validation
- Streamlined academic submission workflow with ready-to-use templates
- Better support for multiple publication venues and formats

### 📝 Documentation

- Added comprehensive documentation for citation management workflows
- Included venue template examples and usage guides
- Updated skills documentation with new capabilities

---

## [2.0.1] - 2025-10-30

### 📝 Documentation Updates

#### Added
- **[FEATURES.md](docs/FEATURES.md)** - Comprehensive features guide covering:
  - Document generation (papers, posters, grants, reviews, schematics)
  - AI-powered capabilities (research lookup, peer review, iterative editing)
  - Intelligent paper detection system
  - Data & file integration workflows
  - Document conversion with MarkItDown
  - Developer features and API patterns

#### Enhanced
- **README.md** - Reorganized with improved feature highlights:
  - Categorized features (Document Generation, AI Capabilities, Developer Tools)
  - Expanded CLI and API usage examples
  - Added workflow examples for common use cases
  - Better visual organization with emojis and sections
  
- **API.md** - Added advanced documentation:
  - Research lookup setup and usage
  - Data file processing details
  - Intelligent paper detection explanation
  - Custom output organization patterns
  - Metadata extraction examples
  - Progress monitoring patterns (progress bars, stage-based, logging)
  - Multiple paper generation (sequential and parallel)
  
- **Documentation organization** - Restructured into:
  - User Guides (Features, API, Skills, Troubleshooting)
  - Developer Resources (Development, Releasing, Changelog, System Instructions)

### Key Highlights

This update significantly improves documentation coverage for:
- ✨ **Research lookup** - Real-time literature search with Perplexity Sonar Pro
- ✨ **Intelligent paper detection** - Automatic context tracking in CLI
- ✨ **Grant proposals** - NSF, NIH, DOE, DARPA with agency-specific guidance
- ✨ **Scientific schematics** - CONSORT diagrams, circuits, pathways
- ✨ **Document conversion** - 15+ formats with MarkItDown
- ✨ **ScholarEval framework** - 8-dimension quantitative paper evaluation

---

## [2.0.0] - 2025-10-28

### 🎉 Major Release: Programmatic API

This release transforms Scientific Writer from a CLI-only tool into a complete Python package with both programmatic API and CLI interfaces.

### ✨ Added

#### Programmatic API
- **New `generate_paper()` async function** - Generate papers programmatically in your own Python code
- **Real-time progress updates** - Async generator yields progress information during execution
- **Comprehensive JSON results** - Complete paper metadata, file paths, citations, and more
- **Type hints throughout** - Full type annotations for better IDE support and development experience
- **Flexible configuration** - Override API keys, output directories, models, and more

#### Package Structure
- **Modular architecture** - Clean separation into `api.py`, `cli.py`, `core.py`, `models.py`, `utils.py`
- **Proper Python package** - Installable via pip/uv with entry points
- **Data models** - `ProgressUpdate`, `PaperResult`, `PaperMetadata`, `PaperFiles` dataclasses

#### Documentation
- **[API_REFERENCE.md](API_REFERENCE.md)** - Complete API documentation with examples
- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Guide for upgrading from v1.x
- **[example_api_usage.py](example_api_usage.py)** - Practical code examples
- **Updated README** - Comprehensive documentation for both API and CLI usage

### 🔄 Changed

- **Package name**: `claude-scientific-writer` → `scientific-writer` (in pyproject.toml)
- **Version**: `1.1.1` → `2.0.0`
- **CLI entry point**: Now calls `scientific_writer.cli:cli_main` instead of standalone script
- **File structure**: Moved from single `scientific_writer.py` to package directory

### ✅ Backward Compatibility

- **100% CLI compatibility** - All existing CLI commands work identically
- **Same output structure** - Paper directories and files organized the same way
- **Same features** - All skills, tools, and capabilities preserved
- **Same configuration** - `.env` files, system instructions, and skills unchanged

### 🗑️ Removed

- `scientific_writer.py` - Replaced by `scientific_writer/` package directory

### 📦 Package Details

**New file structure:**
```
scientific_writer/
├── __init__.py      # Package exports and version
├── api.py           # Async API implementation
├── cli.py           # CLI interface (refactored)
├── core.py          # Core utilities (API keys, instructions, etc.)
├── models.py        # Data models for API responses
└── utils.py         # Helper functions (paper detection, file scanning)
```

**Public API exports:**
```python
from scientific_writer import (
    generate_paper,    # Main API function
    ProgressUpdate,    # Progress update model
    PaperResult,       # Final result model
    PaperMetadata,     # Paper metadata model
    PaperFiles,        # Paper files model
)
```

### 🔧 Technical Details

#### API Response Format

**Progress Update:**
```json
{
  "type": "progress",
  "timestamp": "2024-10-28T14:30:22Z",
  "message": "Writing paper sections",
  "stage": "writing",
  "percentage": 50
}
```

**Final Result:**
```json
{
  "type": "result",
  "status": "success",
  "paper_directory": "/path/to/paper_outputs/20241028_topic/",
  "paper_name": "20241028_topic",
  "metadata": {...},
  "files": {...},
  "citations": {...},
  "figures_count": 5,
  "compilation_success": true,
  "errors": []
}
```

#### Progress Stages
- `initialization` - Setting up paper generation
- `research` - Conducting literature research
- `writing` - Writing paper sections
- `compilation` - Compiling LaTeX to PDF
- `complete` - Finalizing and scanning results

### 📝 Usage Examples

#### CLI (unchanged)
```bash
scientific-writer
> Create a Nature paper on CRISPR gene editing
```

#### Programmatic API (new)
```python
import asyncio
from scientific_writer import generate_paper

async def main():
    async for update in generate_paper("Create a Nature paper on CRISPR"):
        if update["type"] == "progress":
            print(f"[{update['percentage']}%] {update['message']}")
        else:
            print(f"PDF: {update['files']['pdf_final']}")

asyncio.run(main())
```

### 🧪 Testing

- ✅ Package imports work correctly
- ✅ API signature validated
- ✅ Data models instantiate properly
- ✅ CLI entry point functions
- ✅ All required files present
- ✅ Version information correct

### 📊 Migration Path

For users upgrading from v1.x:
1. Pull latest changes: `git pull origin main`
2. Reinstall: `uv sync`
3. Continue using CLI as before, or start using the new API

See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for detailed migration instructions.

### 🙏 Acknowledgments

This release maintains all the great features from v1.x while adding powerful new capabilities for programmatic use. The CLI experience remains unchanged for existing users.

---

## [1.1.1] - 2024-10-27

### Previous Version
- CLI-only interface
- Single `scientific_writer.py` file
- Manual session management
- All features working as documented

---

**Legend:**
- ✨ Added - New features
- 🔄 Changed - Changes in existing functionality
- 🗑️ Removed - Removed features
- 🔧 Fixed - Bug fixes
- 📝 Documentation - Documentation changes

