# Changelog

All notable changes to the Scientific Writer project will be documented in this file.

## [Unreleased]

---

## [2.10.0] - 2025-12-21

### 📝 Comprehensive Venue Writing Style Guides

Major enhancement to writing skills with comprehensive venue-specific style guides for crafting publication-ready manuscripts.

### ✨ Added

#### Venue Writing Style System

- **Master Style Guide** (`venue_writing_styles.md`) - Complete overview of how writing style varies across publication venues
  - Style spectrum from accessible (Nature/Science) to technical (specialized journals)
  - Quick reference table for tone, voice, and abstract style by venue type
  - Guidance on adapting between venue types

- **Nature/Science Style Guide** (`nature_science_style.md`) - 400+ line comprehensive guide
  - Audience and tone guidelines for broad-impact journals
  - Flowing paragraph abstract format with examples
  - Introduction, Results, Discussion structure guidance
  - Figure design principles and citation style
  - Common rejection reasons and pre-submission checklist

- **Cell Press Style Guide** (`cell_press_style.md`) - Cell family journal conventions
  - Summary (abstract), Highlights, eTOC blurb, and In Brief formats
  - Graphical abstract requirements and design guidelines
  - STAR Methods and Key Resources Table formatting
  - Declarative subheading style

- **Medical Journal Style Guide** (`medical_journal_styles.md`) - NEJM, Lancet, JAMA, BMJ
  - Structured abstract format (the one venue requiring labeled sections)
  - Evidence language conventions by study design
  - Reporting guidelines compliance (CONSORT, STROBE, PRISMA)
  - Journal-specific requirements and word limits

- **ML Conference Style Guide** (`ml_conference_style.md`) - NeurIPS, ICML, ICLR, CVPR
  - Contribution bullet list format (critical for ML papers)
  - Ablation study expectations
  - Reproducibility requirements
  - Limitations section guidance

- **CS Conference Style Guide** (`cs_conference_style.md`) - ACL, CHI, SIGKDD
  - NLP conference requirements (human evaluation, error analysis)
  - HCI paper structure (user-centered, design implications)
  - Data mining emphasis (scalability, industry applications)

- **Reviewer Expectations Guide** (`reviewer_expectations.md`) - What reviewers look for by venue
  - Evaluation criteria and priority weights
  - Common rejection reasons by venue type
  - Sample reviewer concerns and effective responses
  - Rebuttal strategies and templates

#### Abstract Formatting Standard

- **Flowing Paragraph Default** - Abstracts now default to flowing paragraph style
  - Updated `scientific-writing/SKILL.md` with explicit abstract formatting rules
  - Updated `imrad_structure.md` with correct vs. incorrect examples
  - Only use structured abstracts when explicitly required by journal (e.g., medical journals)

#### Concrete Examples

- **Nature Abstract Examples** (`nature_abstract_examples.md`) - 5 complete examples across disciplines
  - Molecular biology, neuroscience, climate science, physics, ecology
  - Analysis of what makes each example effective

- **NeurIPS Introduction Example** (`neurips_introduction_example.md`) - Full ML paper introduction
  - Paragraph-by-paragraph breakdown
  - Contribution bullet templates
  - Common mistakes to avoid

- **Cell Summary Examples** (`cell_summary_example.md`) - Complete Cell Press elements
  - Summary, Highlights, eTOC blurb, In Brief
  - Character counting for highlights (≤85 chars)
  - Graphical abstract descriptions

- **Medical Structured Abstract Examples** (`medical_structured_abstract.md`)
  - NEJM, Lancet, JAMA, BMJ examples
  - Journal-specific formatting differences

### 🔧 Improvements

- **Cross-Skill Integration** - All relevant skills now reference venue style guides
  - Updated `scientific-writing/SKILL.md`
  - Updated `literature-review/SKILL.md`
  - Updated `clinical-decision-support/SKILL.md`
  - Updated `peer-review/SKILL.md`
  - Updated `treatment-plans/SKILL.md`
  - Updated `hypothesis-generation/SKILL.md`
  - Updated `research-grants/SKILL.md`
  - Updated `market-research-reports/SKILL.md`
  - Updated `venue-templates/SKILL.md`

- **Synchronized Skills** - Both skill directories updated
  - `skills/` directory (project root)
  - `scientific_writer/.claude/skills/` directory (package)

### 📝 Files Added

- `skills/venue-templates/references/venue_writing_styles.md`
- `skills/venue-templates/references/nature_science_style.md`
- `skills/venue-templates/references/cell_press_style.md`
- `skills/venue-templates/references/medical_journal_styles.md`
- `skills/venue-templates/references/ml_conference_style.md`
- `skills/venue-templates/references/cs_conference_style.md`
- `skills/venue-templates/references/reviewer_expectations.md`
- `skills/venue-templates/assets/examples/nature_abstract_examples.md`
- `skills/venue-templates/assets/examples/neurips_introduction_example.md`
- `skills/venue-templates/assets/examples/cell_summary_example.md`
- `skills/venue-templates/assets/examples/medical_structured_abstract.md`

### 💡 Key Benefits

- **Publication-Ready Papers** - Papers now match the style of target venues
- **Correct Abstract Format** - Flowing paragraphs by default, structured only when required
- **Reviewer Alignment** - Understand what reviewers expect at each venue
- **Cross-Venue Adaptation** - Guidance on converting between venue types
- **Concrete Examples** - Real examples to follow, not just rules

---

## [2.9.5] - 2025-12-10

### 🎨 Scientific Slides Skill Enhancements

- **Professional Minimalism** - Enhanced Nano Banana Pro system prompts for cleaner slides
  - Minimal extra elements - no decorative borders, shadows, or flourishes
  - Generic, simple images - avoid overly specific or detailed imagery
  - Professional, corporate/academic aesthetic with restraint
  - Default author set to "K-Dense" for all presentations

- **Formatting Consistency Protocol** - New workflow for unified slide design
  - Define a Formatting Goal (color scheme, typography, visual style) in EVERY prompt
  - Always attach the previous slide using `--attach` for visual continuity
  - Include citations directly in prompts (e.g., `CITATIONS: Include at bottom: (Author et al., Year)`)
  - Attach existing figures/data for results slides from working directory

- **Results Slide Integration** - New guidelines for data-driven presentations
  - Check for existing figures in `figures/`, `results/`, `plots/`, `images/` directories
  - Attach actual data figures to Nano Banana Pro using `--attach`
  - Multiple figures support: `--attach fig1.png --attach fig2.png`
  - Describe how to incorporate attached figures in the prompt

- **Clean Output** - Only one image file saved per slide
  - Intermediate iterations saved to temp files and cleaned up
  - No `_v1`, `_v2`, or `_review_log.json` files left behind
  - Final image saved directly to specified output path

### 🔧 Technical Changes

- `generate_slide_image_ai.py`: Updated FULL_SLIDE_GUIDELINES with professional minimalism
- `generate_slide_image_ai.py`: Updated VISUAL_ONLY_GUIDELINES with generic imagery preference
- `generate_slide_image_ai.py`: Refactored to use temp files and only save final output
- `SKILL.md`: Added Formatting Consistency Protocol with 5-point checklist
- `SKILL.md`: Added examples with figure attachments for results slides
- `SKILL.md`: Updated Quick Start Guide with new workflow

---

## [2.9.0] - 2025-12-05

### 🚀 Release

- **Version 2.9.0** - Major release with enhanced citation verification and research workflows
  - Upgraded Sonar Pro to Sonar Pro Search for improved research lookup accuracy
  - Enhanced citation verification process with WebSearch tool integration
  - Improved metadata verification for academic citations
  - Better documentation for output directory organization

### 🔧 Improvements

- **Citation Verification** - Enhanced process using WebSearch for metadata validation
- **Research Lookup** - Updated to use Sonar Pro Search for more accurate results
- **Documentation** - Updated output directory references throughout codebase

---

## [2.8.9] - 2025-12-02

### 🔒 Privacy & Identity Protection

- **Model Identity Concealment** - Scientific-Writer never reveals underlying model or tool identity
  - Changed all author attributions from "Claude" to "Scientific-Writer" in Word tracked changes
  - Updated default author name in DOCX/PPTX editing from "Claude" to "Scientific-Writer"
  - Updated default initials from "C" to "SW" in document editing features
  - Removed model-specific branding from user-facing documentation
  - Package descriptions now reference "Scientific-Writer" instead of underlying models

### ✨ Enhanced Scientific Schematic Generation

- **Smart Iteration with Quality Thresholds** - Only regenerate if quality is below document-type threshold
  - Document-type aware quality thresholds:
    * `journal`: 8.5/10 (Nature, Science, peer-reviewed)
    * `conference`, `thesis`, `grant`: 8.0/10
    * `preprint`, `report`: 7.5/10
    * `poster`: 7.0/10
    * `presentation`: 6.5/10
  - **Gemini 3 Pro for Quality Review** - Superior vision and analysis for diagram evaluation
  - Early stop when quality threshold is met (saves API calls and time)
  - Structured review with 5 criteria: Scientific Accuracy, Clarity, Labels, Layout, Professional Appearance
  - Automatic ACCEPTABLE/NEEDS_IMPROVEMENT verdict based on threshold

- **New `--doc-type` Flag** - Specify document type for appropriate quality standards
  - `python scripts/generate_schematic.py "diagram" -o out.png --doc-type journal`
  - Review log now includes `doc_type`, `quality_threshold`, `needs_improvement`, `early_stop`, and `early_stop_reason`

### 📝 Updated Skills & Documentation

- **Scientific Schematics Skill** - Complete documentation update
  - Smart iteration workflow with flowchart
  - Quality threshold table for all document types
  - Updated examples showing `--doc-type` usage
  - Early stop behavior and benefits explained

- **MarkItDown Skill** - Updated model references to generic descriptions
  - Changed "Claude Sonnet 4.5" references to "advanced vision models"
  - Model identifiers preserved for API compatibility

### 🔧 Technical Changes

- **Document Editing** - Consistent authorship across all skills
  - `skills/document-skills/docx/scripts/document.py`: Default author "Scientific-Writer" 
  - `skills/document-skills/docx/ooxml/scripts/validation/redlining.py`: Updated validation messages
  - `skills/document-skills/pptx/ooxml/scripts/validation/redlining.py`: Updated validation messages
  - All XML examples updated in documentation

- **Scientific Schematic Generation** - Enhanced AI review system
  - `scripts/generate_schematic_ai.py`: Gemini 3 Pro review integration
  - `scripts/generate_schematic.py`: Document type support
  - Quality threshold constants in generator class
  - Enhanced review prompt with structured 5-criteria evaluation

---

## [2.8.8] - 2025-12-01

### ✨ New Features

- **Live Text Streaming** - Stream Scientific-Writer's actual responses through the API in real-time
  - New `TextUpdate` model for live text output from Scientific-Writer
  - API now yields `{"type": "text", "content": "..."}` for each text block
  - Enables displaying Scientific-Writer's reasoning and explanations as they happen
  - Works alongside existing progress updates - no breaking changes

### 📝 API Changes

- New `TextUpdate` model exported from `scientific_writer`
- `generate_paper()` now yields three update types:
  - `"text"`: Live streaming of Scientific-Writer's text responses
  - `"progress"`: Structured stage updates (unchanged)
  - `"result"`: Final result with all paper details (unchanged)

### 🎯 Example Usage

```python
from scientific_writer import generate_paper

async for update in generate_paper("Create a paper on AI"):
    if update["type"] == "text":
        # Stream Scientific-Writer's live output
        print(update["content"], end="", flush=True)
    elif update["type"] == "progress":
        # Structured progress updates
        print(f"\n[{update['stage']}] {update['message']}")
    elif update["type"] == "result":
        print(f"\nPaper created: {update['paper_directory']}")
```

To show only progress updates (no text streaming):

```python
async for update in generate_paper("Create a paper"):
    if update["type"] == "text":
        pass  # Skip text updates
    elif update["type"] == "progress":
        print(f"[{update['stage']}] {update['message']}")
```

---

## [2.8.7] - 2025-11-26

### ✨ New Features

- **Token Usage Tracking** - Track input/output tokens during document generation
  - New `track_token_usage` parameter for `generate_paper()` API
  - Returns `token_usage` in final result with detailed token breakdown
  - Tracks: `input_tokens`, `output_tokens`, `total_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`
  - Silent tracking (no terminal output) - purely returned as data for programmatic use

### 📝 API Changes

- New `TokenUsage` model exported from `scientific_writer`
- `generate_paper()` accepts optional `track_token_usage: bool = False` parameter
- When enabled, final result includes `token_usage` field with token statistics
- Token usage also included in error results when tracking is enabled
- CLI `main()` function now accepts `track_token_usage` parameter and returns `TokenUsage`

### 🎯 Example Usage

```python
from scientific_writer import generate_paper

async for update in generate_paper("Create a paper", track_token_usage=True):
    if update["type"] == "result":
        if "token_usage" in update:
            usage = update["token_usage"]
            print(f"Input tokens: {usage['input_tokens']}")
            print(f"Output tokens: {usage['output_tokens']}")
            print(f"Total tokens: {usage['total_tokens']}")
```

---

## [2.8.5] - 2025-11-25

### ✨ Enhanced

- **Smarter context-aware progress messages** - Progress updates are now more intelligent and descriptive
  - Detects document type (slides, poster, report, grant) from file paths
  - Extracts section names from filenames (introduction, methods, results, etc.)
  - Messages like "Writing introduction section" instead of "Writing file.tex"

- **Cleaner progress output** - Reduced noise in progress updates
  - Inspection commands (ls, cat) no longer generate progress updates
  - Text-based progress analysis is now minimal fallback only
  - Tool usage drives primary progress updates

- **Enhanced tool analysis** - More detailed messages for all tool types
  - Read: "Analyzing PDF", "Loading data from file.csv", "Reading introduction section"
  - Write: "Creating main document structure", "Writing methods section", "Creating bibliography with references"
  - Edit: "Refining introduction section", "Updating bibliography"
  - Bash: "Running full LaTeX compilation pipeline", "Processing bibliography citations", "Copying final PDF to output"
  - Research: "Searching: [query preview]", "Web search: [query preview]"

### 🔧 Improvements

- **Document type detection** - New `_detect_document_type()` identifies:
  - Slides/presentations (beamer)
  - Posters
  - Reports
  - Grants/proposals
  - Generic documents

- **Section name extraction** - New `_get_section_from_filename()` recognizes:
  - abstract, introduction, methods, results, discussion, conclusion
  - background, related work, experiments, evaluation
  - appendix, supplementary material

- **Simplified text analysis** - `_analyze_progress()` now only detects major stage transitions
  - Compilation indicators (pdflatex, latexmk)
  - Completion indicators (successfully compiled, pdf generated)
  - Returns `None` message when no transition detected

---

## [2.8.4] - 2025-11-25

### 🔄 Changed

- **Removed percentage from progress updates** - Progress updates now use stage-based tracking instead of percentages
  - Cleaner API response without arbitrary percentage values
  - Progress is tracked via stages: `initialization` → `planning` → `research` → `writing` → `compilation` → `complete`

- **Generic document terminology** - Replaced "paper" with "document" throughout the API
  - Supports all document types: papers, slides, posters, reports, grants, etc.
  - Messages now say "document generation" instead of "paper generation"
  - More accurate for the tool's actual capabilities

### 📝 API Changes

- `ProgressUpdate` model no longer has a `percentage` field
- Progress updates now return only: `type`, `timestamp`, `message`, `stage`, and optional `details`
- `_analyze_progress()` returns `(stage, message)` tuple instead of `(stage, percentage, message)`
- `_analyze_tool_use()` returns `(stage, message)` tuple instead of `(stage, percentage, message)`

### 🎯 Example Output

```python
async for update in generate_paper("Create conference slides on AI"):
    if update["type"] == "progress":
        print(f"[{update['stage']:12}] {update['message']}")
```

Output:
```
[initialization] Starting document generation with Claude
[research     ] Searching literature databases
[research     ] Researching: machine learning applications...
[writing      ] Writing introduction section
[writing      ] Writing LaTeX document: main.tex
[compilation  ] Compiling LaTeX to PDF
[complete     ] Document generation complete
```

---

## [2.8.3] - 2025-11-25

### ✨ Enhanced

- **Detailed API Progress Updates** - Significantly improved progress tracking in the programmatic API
  - **Tool-aware progress tracking** - Detects and reports on specific tool usage (Read, Write, Edit, Bash)
  - **File operation tracking** - Reports when files are being read, written, or edited with file names
  - **Compilation detection** - Identifies pdflatex, bibtex, and latexmk commands with specific messages
  - **Research lookup tracking** - Shows when research queries are being executed
  - **25+ detailed progress indicators** - Granular messages for each stage of paper generation:
    - Planning: outline creation, requirements analysis
    - Research: database searching, publication gathering, synthesis
    - Writing: abstract, introduction, methods, results, discussion, conclusion, bibliography
    - Compilation: LaTeX creation, pdflatex passes, bibtex processing
    - Finalization: file verification, directory organization
  - **New `details` field** - Progress updates now include optional context:
    - `tool`: Name of the tool being used
    - `tool_calls`: Count of tool invocations
    - `files_created`: Number of files written
  - **Non-duplicate filtering** - Avoids repeating the same progress message

### 📝 API Changes

- `ProgressUpdate` model now includes optional `details: Dict[str, Any]` field
- New `planning` stage added to progress stages
- Progress percentages are now more granular (22%, 28%, 35%, etc. vs just 30%, 50%, 80%)

### 🎯 Example Output

```python
async for update in generate_paper("Create a paper on AI"):
    if update["type"] == "progress":
        print(f"[{update['percentage']:3d}%] {update['message']}")
        if update.get('details'):
            print(f"       Tool: {update['details'].get('tool')}")
```

Output:
```
[ 10%] Starting paper generation with Claude
[ 22%] Searching literature databases
[ 30%] Researching: quantum computing applications...
[ 45%] Writing introduction section
[ 55%] Writing LaTeX document: main.tex
[ 68%] Creating bibliography: references.bib
[ 78%] Compiling LaTeX to PDF
[ 82%] Processing bibliography with BibTeX
[ 92%] Verifying output files
[100%] Paper generation complete
```

---

## [2.8.2] - 2025-11-24

### 🔧 Fixed

- **API Critical Bug Fix** - Fixed parameter naming conflict in `generate_paper()` function
  - The `query` parameter was shadowing the imported `query` function from `claude_agent_sdk`
  - Renamed SDK import to `claude_query` to avoid the conflict
  - API now works correctly for programmatic paper generation

---

## [2.8.1] - 2025-11-24

### 🔧 Changed

- **Output Directory Renamed** - Changed default output directory from `paper_outputs/` to `writing_outputs/` to better reflect the broader scope of document types supported (papers, slides, posters, reports, etc.)
  - Updated all documentation and templates to reference `writing_outputs/`
  - Added `writing_outputs/` to `.gitignore`

---

## [2.8.0] - 2025-11-20

### 🎨 Headline Feature: Nano Banana Pro for Scientific Diagrams

This release introduces **Nano Banana Pro**, a revolutionary AI-powered system for generating publication-quality scientific diagrams from natural language descriptions.

### ✨ Added

#### AI-Powered Scientific Schematics

- **Nano Banana Pro Integration** - Generate any scientific diagram by describing it in natural language
  - No coding required - just describe what you want
  - No templates needed - AI understands your intent
  - No manual drawing - automatic generation from description
  - Publication-quality output following scientific standards
  
- **Iterative Refinement System** - Automatic quality improvement through intelligent review cycles
  - 3 iterations by default (configurable 1-10)
  - AI quality review after each iteration (0-10 score + detailed critique)
  - Progressive improvement addressing specific issues
  - Transparent review process with detailed JSON logs
  
- **Comprehensive Output** - Multiple versions plus quality assessment
  - Three image versions (v1, v2, v3) showing progression
  - Final polished image ready for publication
  - Detailed review log with scores and critiques
  - Quality metrics: clarity, labels, accuracy, accessibility
  
- **Built-In Scientific Standards** - Automatic adherence to best practices
  - Clean white/light backgrounds
  - High contrast for readability (WCAG 2.1 compliant)
  - Professional typography (minimum 10pt fonts, sans-serif)
  - Colorblind-friendly color palettes (Okabe-Ito scheme)
  - Proper spacing, scale bars, legends, and axes
  - Standard scientific notation and symbols

#### Universal Diagram Support

- **Clinical & Medical** - CONSORT flowcharts, clinical trials, diagnostic algorithms, patient pathways
- **Computational & AI** - Neural networks (CNNs, Transformers, RNNs), algorithms, system architectures
- **Biological & Chemical** - Signaling pathways (MAPK, PI3K/AKT), metabolic pathways, protein structures
- **Engineering & Physics** - Circuit diagrams, block diagrams, experimental setups, signal processing
- **And More** - Study designs, conceptual frameworks, process diagrams, timelines, organizational charts

#### Comprehensive Documentation

- **README.md** - Quick start guide with installation, usage, examples (340+ lines)
- **QUICK_REFERENCE.md** - One-page cheat sheet for common tasks (209 lines)
- **SKILL.md** - Complete documentation with extensive examples (737 lines)
- **IMPLEMENTATION_SUMMARY.md** - Technical details and architecture (372 lines)
- **Example Scripts** - `example_usage.sh` with practical demonstrations
- **Test Suite** - `test_ai_generation.py` with 6 comprehensive tests

### 🔧 Improvements

#### Prompt Engineering System

- **Effective Prompt Guidelines** - Best practices for getting quality results
  - Specify layout and structure (vertical/horizontal flow, positioning)
  - Include quantitative details (numbers, dimensions, parameters)
  - Describe visual style (minimalist, detailed, technical)
  - Request specific labels and annotations
  - Mention color and accessibility requirements
  
- **Quality Assessment Framework** - Seven-dimension evaluation system
  - Scientific accuracy - correctness of representation
  - Clarity of elements - easy to understand
  - Label readability - fonts, sizes, placement
  - Layout and composition - visual hierarchy
  - Accessibility - colorblind-friendly, high contrast
  - Professional quality - publication-ready appearance
  - Completeness - all required elements present

#### Developer Experience

- **Python API** - Programmatic access to Nano Banana Pro
  ```python
  from scripts.generate_schematic_ai import ScientificSchematicGenerator
  
  generator = ScientificSchematicGenerator(api_key="your_key", verbose=True)
  results = generator.generate_iterative(
      user_prompt="CONSORT flowchart",
      output_path="figures/consort.png",
      iterations=3
  )
  print(f"Final score: {results['final_score']}/10")
  ```

- **Command-Line Interface** - Simple, intuitive usage
  ```bash
  python scripts/generate_schematic.py "diagram description" -o output.png
  ```

- **Flexible Configuration** - Multiple options for customization
  - `--iterations N` - Control refinement cycles (1-10)
  - `--method ai|code` - Choose generation method
  - `-v, --verbose` - Detailed progress output
  - `--api-key KEY` - Override environment variable

### 🎯 Usage Examples

#### CONSORT Flowchart
```bash
python scripts/generate_schematic.py \
  "CONSORT participant flow: screened n=500, excluded n=150, randomized n=350" \
  -o consort.png
```

#### Neural Network Architecture
```bash
python scripts/generate_schematic.py \
  "Transformer architecture with encoder and decoder, show attention mechanism" \
  -o transformer.png
```

#### Biological Pathway
```bash
python scripts/generate_schematic.py \
  "MAPK signaling pathway: EGFR → RAS → RAF → MEK → ERK → nucleus" \
  -o mapk.png
```

### 💡 Key Benefits

- **Fast**: Results in 1-2 minutes (3 iterations)
- **Easy**: Natural language descriptions only
- **Quality**: Automatic review and refinement
- **Universal**: Works for all diagram types
- **Publication-Ready**: High-quality output immediately
- **Affordable**: $0.10-0.50 per diagram
- **Accessible**: Colorblind-friendly, high contrast
- **Documented**: Comprehensive guides and examples

### 📦 New Files

- `skills/scientific-schematics/`
  - `scripts/generate_schematic_ai.py` - AI generation engine with iterative refinement
  - `scripts/generate_schematic.py` - Unified entry point (AI + code methods)
  - `README.md` - Quick start and comprehensive guide
  - `QUICK_REFERENCE.md` - One-page cheat sheet
  - `IMPLEMENTATION_SUMMARY.md` - Technical details
  - `test_ai_generation.py` - Verification test suite
  - `example_usage.sh` - Usage demonstrations

### 🔄 Backward Compatibility

- ✅ All existing code-based generation still available via `--method code`
- ✅ Graphviz, TikZ, schemdraw, and other tools unchanged
- ✅ All existing templates and scripts preserved
- ✅ Classic workflow accessible for users who prefer it

### 🧪 Testing

Run verification tests:
```bash
python skills/scientific-schematics/test_ai_generation.py
# Expected: "6/6 tests passed"
```

### 📊 Performance

- **Generation Time**: 1-2 minutes for 3 iterations
- **Cost**: $0.10-0.50 per diagram (3 iterations)
- **Quality Scores**: Typically 7-9.5/10 by final iteration
- **Success Rate**: High quality on diverse diagram types

### 🌟 Example Outputs

See `figures/` directory for real examples:
- `google_gemini_architecture.png` - Complex AI system architecture
- `gemini_moe_architecture.png` - Mixture-of-Experts diagram
- `test_nano_banana.png` - Test diagram
- `*_review_log.json` - Quality assessment logs

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

