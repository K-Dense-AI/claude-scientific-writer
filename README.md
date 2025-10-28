# Claude Scientific Writer

A powerful Python package and CLI for scientific writing powered by Claude Sonnet 4.5 and the Claude Agents SDK. Generate complete scientific papers programmatically or through an interactive command-line interface.

**Version 2.0** introduces a programmatic API while maintaining full backward compatibility with the CLI.

**For more advanced and specialized writing, analysis and autonomous research capabilities, go to [k-dense.ai](https://k-dense.ai)**

## 📚 Documentation

- **[API Reference](API_REFERENCE.md)** - Complete API documentation with examples
- **[Migration Guide](MIGRATION_GUIDE.md)** - Upgrading from v1.x to v2.0
- **[Example Code](example_api_usage.py)** - Programmatic usage examples
- **[Skills Guide](Docs/SKILLS.md)** - Available writing and research skills

## Features

- 🔬 **Scientific Writing**: Generate complete scientific papers following IMRaD structure with proper citations and formatting
- 📚 **Literature Review**: Conduct comprehensive literature reviews with citation management
- 🔍 **Research Lookup**: Real-time research information using Perplexity's Sonar Pro model via OpenRouter
- 📝 **Peer Review**: Receive constructive feedback on scientific drafts
- 📄 **Document Conversion**: Convert 15+ file formats to Markdown using MarkItDown (PDF, DOCX, PPTX, XLSX, images, audio, etc.)
- 🖼️ **AI-Enhanced Processing**: AI-powered image descriptions and document analysis using Claude Sonnet 4.5
- 🤖 **LaTeX Support**: Generates publication-ready LaTeX documents with BibTeX citations
- 📊 **Progress Tracking**: Real-time logging and transparent workflow execution
- 📦 **Data File Integration**: Automatically process and incorporate data files and images into your papers

## What You Can Do

**Write Papers for Any Venue**
- ✨ Generate papers for **any conference or journal** with publicly available LaTeX templates (NeurIPS, ICML, Nature, Science, IEEE, ACM, arXiv, etc.)
- 🎯 Automatically tailor writing style, structure, and citations to match venue requirements
- 📏 Respect page limits, formatting constraints, and specific submission guidelines

**Intelligent Writing Assistant**
- 🔬 Adapt technical depth and terminology based on your specific **research subtopic** (e.g., computer vision vs. NLP, molecular biology vs. ecology)
- 💡 Get **strategic recommendations** for strengthening your paper (additional experiments, missing comparisons, literature gaps)
- 🎨 Receive suggestions for impactful visualizations and figure improvements
- ✍️ Refine arguments, improve clarity, and enhance scientific rigor

**Convert & Repurpose Content**
- 📄➡️📊 **Transform papers into conference posters** with optimized layout and visual design
- 📑 Convert between formats: full paper ↔ short paper ↔ extended abstract ↔ poster
- 🔄 Adapt existing work for different venues (e.g., workshop paper → main conference submission)

**Comprehensive Workflow Support**
- 📚 Conduct systematic **literature reviews** with citation management
- 🔍 Perform **real-time research lookups** for the latest developments in your field
- 👥 Get **peer review feedback** before submission to identify weaknesses
- 📝 Generate **LaTeX posters** (A0, A1, 36×48") with professional design

**Document Processing & Analysis**
- 🗂️ Convert research PDFs, presentations, and documents to clean Markdown
- 🖼️ Extract and describe figures from papers using Claude Sonnet 4.5 vision
- 📊 Process experimental data and integrate it into your manuscript
- 🎤 Transcribe research talks and convert slides to written content

**Smart Automation**
- ⚡ Automatically format references in any citation style (APA, MLA, Chicago, Nature, IEEE, etc.)
- 🔗 Verify and validate citations against reporting standards
- 📋 Generate complete BibTeX bibliographies with proper formatting
- 🎯 Ensure compliance with CONSORT, PRISMA, STROBE, and other reporting guidelines

## Quick Start

### Prerequisites

- Python 3.10 or later
- [uv](https://docs.astral.sh/uv/) - Fast Python package installer
- An [Anthropic API key](https://console.anthropic.com/)
- An [OpenRouter API key](https://openrouter.ai/) (for research lookup functionality)

### Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/yourusername/claude-scientific-writer.git
   cd claude-scientific-writer
   ```

2. **Install uv (if not already installed):**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   
   After installation, restart your shell or run:
   ```bash
   source $HOME/.cargo/env
   ```

3. **Install dependencies with uv:**
   
   Create a virtual environment and install dependencies:
   ```bash
   uv sync
   ```
   
   Or install into your current Python environment:
   ```bash
   uv pip install -e .
   ```

4. **Set up your API keys:**

   Create a `.env` file in the project root:
   ```bash
   echo "ANTHROPIC_API_KEY=your_anthropic_api_key_here" > .env
   echo "OPENROUTER_API_KEY=your_openrouter_api_key_here" >> .env
   ```

   Or export them in your shell:
   ```bash
   export ANTHROPIC_API_KEY='your_anthropic_api_key_here'
   export OPENROUTER_API_KEY='your_openrouter_api_key_here'
   ```

### Usage

#### CLI Usage

Run the scientific writer CLI:

**If you used `uv sync`:**
```bash
uv run scientific-writer
```

**If you installed with `uv pip install -e .`:**
```bash
scientific-writer
```

#### Programmatic API Usage

You can also use the scientific writer as a Python library in your own code:

```python
import asyncio
from scientific_writer import generate_paper

async def main():
    query = "Create a Nature paper on CRISPR gene editing"
    
    async for update in generate_paper(query):
        if update["type"] == "progress":
            print(f"[{update['percentage']}%] {update['message']}")
        else:
            # Final result with comprehensive information
            result = update
            print(f"✓ Paper created: {result['paper_directory']}")
            print(f"✓ PDF: {result['files']['pdf_final']}")
            print(f"✓ TeX: {result['files']['tex_final']}")
            print(f"✓ Citations: {result['citations']['count']}")
            print(f"✓ Figures: {result['figures_count']}")
            
            # Access all generated files
            for draft_pdf in result['files']['pdf_drafts']:
                print(f"  Draft: {draft_pdf}")

asyncio.run(main())
```

**API Parameters:**

- `query` (str, required): The paper generation request
- `output_dir` (str, optional): Custom output directory (defaults to `./paper_outputs`)
- `api_key` (str, optional): Anthropic API key (defaults to `ANTHROPIC_API_KEY` env var)
- `model` (str, optional): Claude model to use (default: `claude-sonnet-4-20250514`)
- `data_files` (list, optional): List of file paths to include in the paper
- `cwd` (str, optional): Working directory (defaults to package parent directory)

**Return Value:**

The `generate_paper()` function is an async generator that yields:
1. **Progress updates** (dict with `type="progress"`) during execution
2. **Final result** (dict with `type="result"`) containing comprehensive paper information

See the [API Response Format](#api-response-format) section below for the complete JSON structure.

**Advanced Example with Custom Options:**

```python
import asyncio
from scientific_writer import generate_paper

async def create_neurips_paper():
    # Generate a paper with custom data files
    data_files = ["results.csv", "figures/attention_map.png"]
    
    async for update in generate_paper(
        query="Create a NeurIPS paper on efficient transformers",
        output_dir="./my_papers",
        data_files=data_files,
        model="claude-sonnet-4-20250514"
    ):
        if update["type"] == "progress":
            print(f"[{update['stage']}] {update['message']}")
        else:
            # Save result to JSON
            import json
            with open("paper_result.json", "w") as f:
                json.dump(update, f, indent=2)
            
            print(f"Paper complete! Status: {update['status']}")
            if update['compilation_success']:
                print(f"PDF available at: {update['files']['pdf_final']}")

asyncio.run(create_neurips_paper())
```

### API Response Format

The `generate_paper()` async generator yields two types of updates:

#### Progress Update

Yielded periodically during paper generation:

```json
{
  "type": "progress",
  "timestamp": "2024-10-28T14:30:22Z",
  "message": "Writing paper sections",
  "stage": "writing",
  "percentage": 50
}
```

**Stages:** `initialization` → `research` → `writing` → `compilation` → `complete`

#### Final Result

The last yield contains comprehensive paper information:

```json
{
  "type": "result",
  "status": "success",
  "paper_directory": "/path/to/paper_outputs/20241028_143022_topic/",
  "paper_name": "20241028_143022_topic",
  "metadata": {
    "title": "Efficient Attention Mechanisms for Transformer Models",
    "created_at": "2024-10-28T14:30:22Z",
    "topic": "efficient transformers",
    "word_count": 5200
  },
  "files": {
    "pdf_final": "/path/to/final/manuscript.pdf",
    "tex_final": "/path/to/final/manuscript.tex",
    "pdf_drafts": ["/path/to/drafts/v1_draft.pdf"],
    "tex_drafts": ["/path/to/drafts/v1_draft.tex"],
    "bibliography": "/path/to/references/references.bib",
    "figures": [
      "/path/to/figures/attention_map.png",
      "/path/to/figures/performance_comparison.png"
    ],
    "data": ["/path/to/data/results.csv"],
    "progress_log": "/path/to/progress.md",
    "summary": "/path/to/SUMMARY.md"
  },
  "citations": {
    "count": 42,
    "style": "BibTeX",
    "file": "/path/to/references/references.bib"
  },
  "figures_count": 2,
  "compilation_success": true,
  "errors": []
}
```

**Status Values:**
- `success`: Paper fully generated with PDF
- `partial`: TeX created but PDF compilation failed
- `failed`: Generation failed

### Intelligent Paper Detection

The tool automatically detects when you're referring to a previous paper and continues working on it. You don't need to manually specify which paper to work on!

**How It Works:**
- 🔍 **Automatic Detection**: Analyzes your prompt for references to existing papers
- 📝 **Keyword Matching**: Recognizes continuation keywords like "continue", "update", "edit", "revise", "fix"
- 🎯 **Topic Recognition**: Matches paper topics mentioned in your prompt (e.g., "acoustics paper", "biology review")
- 🔄 **Context Switching**: Automatically switches between papers based on your intent

**Example Usage:**

```bash
# First session - create a new paper
> Write a Nature review paper on AI in biology

# Later session - automatically continues the same paper
> Update the paper with more recent citations

# Reference a specific paper by topic
> Fix the acoustics paper poster

# Edit the most recent paper
> Continue working on the paper

# Explicitly start a new paper
> Create a new paper on quantum computing
```

**Detection Keywords:**
- Continuation: `continue`, `update`, `edit`, `revise`, `modify`, `change`, `fix`, `improve`
- Paper references: `the paper`, `my paper`, `current paper`, `previous paper`, `last paper`
- Poster work: `poster`, `the poster`, `my poster`
- Compilation: `compile`, `generate pdf`

**Note**: If you want to explicitly start a new paper, just say "new paper" or "start fresh".

## How It Works

### Workflow

1. **You Make a Request**: Describe what you need (e.g., "Create a NeurIPS paper on transformer attention")
2. **Brief Plan & Execution**: The assistant presents a plan and immediately starts working
3. **Real-Time Updates**: Continuous progress updates throughout execution
4. **Organized Output**: All files saved to `paper_outputs/<timestamp>_<description>/`

### Output Structure

```
paper_outputs/20241027_143022_neurips_attention/
├── progress.md              # Real-time progress log
├── SUMMARY.md               # Final summary and instructions
├── drafts/
│   ├── v1_draft.tex        # LaTeX source
│   ├── v1_draft.pdf        # Compiled PDF
│   └── v2_draft.tex        # Revised version
├── references/
│   └── references.bib      # BibTeX bibliography
├── figures/                 # Images copied from data/ folder
│   ├── figure_01.png       # Your image files
│   └── plot_results.svg
├── data/                    # Data files copied from data/ folder
│   ├── dataset.csv         # Your data files
│   └── results.json
└── final/
    ├── manuscript.pdf      # Final compiled PDF
    └── manuscript.tex      # Final LaTeX source
```

## Example Use Cases

### Writing a Scientific Paper

```
> Create a NeurIPS paper on efficient attention mechanisms in transformers
```

**Important**: Place your experimental results, figures, plots, and any project documentation in the `data/` folder before starting. The writer will not download data or perform experiments/analysis by itself - it requires you to provide these materials.

The assistant will:
- Create a complete LaTeX document following NeurIPS format
- Perform literature research for each section
- Write Introduction, Methods, Results, Discussion sections based on your provided data
- Incorporate your figures and results from the `data/` folder
- Generate proper BibTeX citations
- Compile to PDF
- Provide real-time progress updates

### Literature Review

```
> Conduct a literature review on CRISPR applications in agriculture
```

### Research Lookup

```
> Research the latest developments in quantum computing from 2024
```

### Peer Review

```
> Review my methods section in draft.txt and provide constructive feedback
```

### Citation Formatting

```
> Format these 10 citations in IEEE style: [paste citations]
```

### Document Conversion

```
> Convert all PDFs in the literature folder to Markdown
```

```
> Convert this PowerPoint presentation to Markdown with AI-enhanced image descriptions
```

## OpenRouter Integration

The Scientific Writer uses **OpenRouter** for AI-enhanced features, providing access to 100+ AI models through a unified API:

### What is OpenRouter?

OpenRouter is an API gateway that provides:
- **Access to Multiple Models**: GPT-4, Claude, Gemini, and 100+ other models
- **Unified Interface**: OpenAI-compatible API for easy integration
- **Flexible Choice**: Choose the best model for each task
- **Competitive Pricing**: Often better rates than direct access

### Where OpenRouter is Used

1. **Research Lookup**: Perplexity Sonar Pro for real-time research queries
2. **AI-Enhanced Document Conversion**: Claude Sonnet 4.5 (recommended), GPT-4o, or Gemini for detailed image descriptions in PDFs and presentations

### Setup

OpenRouter is configured alongside your Anthropic API key:

```bash
# Add to your .env file
echo "OPENROUTER_API_KEY=your_openrouter_api_key_here" >> .env
```

Get your API key at: https://openrouter.ai/keys

### Popular Models for Different Tasks

| Task | Recommended Model | Provider |
|------|-------------------|----------|
| Research Lookup | `perplexity/sonar-pro` | Perplexity |
| Scientific Image Analysis | `anthropic/claude-sonnet-4.5` | Anthropic |
| Presentation Conversion | `anthropic/claude-sonnet-4.5` | Anthropic |
| Cost-Effective OCR | `google/gemini-pro-vision` | Google |

**💡 Cost-Saving Tip**: To save costs on Perplexity research lookups, you can specify cheaper Sonar models (like `perplexity/sonar` or `perplexity/sonar-reasoning`) in your prompts. For example: "Use sonar model to research..." instead of the default Sonar Pro.

See the complete model list at: https://openrouter.ai/models

### Example Usage

When converting documents with AI enhancement, you can specify which model to use:

```
> Convert this research paper PDF to Markdown using Claude for image analysis
```

The assistant will automatically use the appropriate OpenRouter model for optimal results.

## Data File Integration

**Important**: The scientific writer does **not** download data, run experiments, or perform statistical analysis. You must provide all experimental results, figures, plots, and supporting documentation yourself.

The scientific writer can automatically process and incorporate data files and images from the `data/` folder at the project root. This feature makes it easy to include your research data, plots, and figures in your papers.

### How It Works

1. **Place Files in the Data Folder**: Add any files (CSV, JSON, images, etc.) to the `data/` folder in the project root
2. **Automatic Detection**: The tool automatically detects files when you start or continue working on a paper
3. **Smart Routing**: 
   - **Data files** (CSV, TXT, JSON, Excel, etc.) → copied to `paper_outputs/<paper>/data/`
   - **Images** (PNG, JPG, SVG, GIF, etc.) → copied to `paper_outputs/<paper>/figures/`
4. **Context Integration**: File information is automatically provided to Claude as context
5. **Auto-Cleanup**: Original files are deleted from the `data/` folder after successful copying

### Supported File Types

**Images** (automatically placed in `figures/`):
- PNG, JPG/JPEG, GIF, SVG, BMP, TIFF, WebP, ICO

**Data Files** (automatically placed in `data/`):
- CSV, TSV, Excel (XLSX, XLS)
- JSON, XML
- TXT, MD
- Any other non-image files

### Example Workflow

```bash
# 1. Add your files to the data folder
cp my_plot.png data/
cp results.csv data/
cp analysis.json data/

# 2. Run the scientific writer
python scientific_writer.py

# 3. Start or continue a paper
> Continue working on the paper, incorporate the new data

# The tool will automatically:
# - Detect the 3 files
# - Copy my_plot.png to figures/
# - Copy results.csv and analysis.json to data/
# - Delete the originals from data/
# - Inform Claude about available files
```

### Console Output

When files are processed, you'll see:

```
📦 Found 3 file(s) in data folder. Processing...
   ✓ Copied 2 data file(s) to data/
   ✓ Copied 1 image(s) to figures/
   ✓ Deleted original files from data folder
```

### Tips

- **Use descriptive filenames**: Claude will see the filenames, so use clear, descriptive names
- **Images as figures**: Images are automatically recognized and can be referenced in your paper
- **Data context**: Claude will be aware of data files and can help analyze or describe them
- **Batch processing**: Add multiple files at once - they'll all be processed together

## Available Skills

The CLI comes with specialized skills loaded from `.claude/skills/`:

### Scientific Writing
- IMRaD structure guidance
- Citation styles (APA, MLA, Chicago, Nature, IEEE, etc.)
- Figures and tables best practices
- Reporting guidelines for various study types

### Literature Review
- Database search strategies
- Citation management and verification
- Review template generation

### Peer Review
- Common issues identification
- Reporting standards verification
- Constructive feedback generation

### Research Lookup
- Real-time research using Perplexity Sonar Pro
- Automatic citation of sources
- Current literature access

### Document Skills

#### MarkItDown - Universal File Converter
- Convert 15+ file formats to Markdown (PDF, DOCX, PPTX, XLSX, images, audio, YouTube URLs)
- AI-enhanced image descriptions using Claude Sonnet 4.5 (via OpenRouter)
- OCR for scanned documents
- Speech-to-text transcription
- Batch processing with parallel execution
- Optimized for LLM processing and scientific workflows

#### Traditional Document Manipulation
- **DOCX**: Create and edit Word documents
- **PDF**: Extract information, fill forms
- **PPTX**: Create and modify PowerPoint presentations
- **XLSX**: Work with Excel spreadsheets

For detailed skill documentation, see [SKILLS.md](SKILLS.md).

## Commands

- **Regular prompts**: Type your request and press Enter
- **`help`**: Display usage tips and examples
- **`exit` or `quit`**: End the session

## Tips for Best Results

1. **Be specific**: Mention the target journal/conference (e.g., "Nature", "NeurIPS")
2. **Provide context**: Include field of study, specific requirements, page limits
3. **Specify format**: Citation style preferences, document format
4. **Iterate**: Ask for revisions or clarifications as needed
5. **Use files**: Reference existing files for review or editing tasks
6. **Prepare your data first**: The writer does NOT run experiments or download data - place all your experimental results, figures, plots, and documentation in the `data/` folder before starting
7. **Convert documents**: Convert PDFs, presentations, and other documents to Markdown for easy processing
8. **Choose AI models**: Specify preferred models for AI-enhanced features (default: Claude Sonnet 4.5 for vision)

## Configuration

### Permission Modes

The tool uses `bypassPermissions` mode by default, which means:
- ✅ Brief plan shown before execution
- ✅ Immediate execution without approval delays
- ✅ Continuous progress updates
- ✅ Can interrupt with Ctrl+C if needed

To change permission modes, edit `scientific_writer.py` line 81:

```python
permission_mode="bypassPermissions"  # Options: "bypassPermissions", "acceptEdits", "default"
```

### System Instructions

The agent's behavior is defined in `CLAUDE.md`, which includes:
- Workflow protocols
- File organization standards
- Progress logging requirements
- Quality checklists

Modify this file to customize the agent's behavior.

## Project Structure

```
claude-scientific-writer/
├── .claude/
│   └── skills/                  # Specialized skills
│       ├── scientific-writing/
│       ├── literature-review/
│       ├── peer-review/
│       ├── research-lookup/
│       ├── latex-posters/
│       ├── markitdown/          # Universal file converter
│       └── document-skills/
├── data/                        # Place your data files here (auto-processed)
├── paper_outputs/               # Generated papers (auto-created)
├── scientific_writer.py         # Main CLI application
├── pyproject.toml               # Python dependencies (managed by uv)
├── CLAUDE.md                    # System instructions
├── SKILLS.md                    # Detailed skills documentation
├── .env                         # API keys (create this)
└── README.md                    # This file
```

## Troubleshooting

### API Key Issues

If you see an error about missing API key:
```
Error: ANTHROPIC_API_KEY environment variable not set.
```

Make sure you've either:
1. Created a `.env` file with your API keys, or
2. Exported the environment variables in your shell

### Import Errors

Ensure all dependencies are installed:
```bash
uv sync
```

Or if installing without a virtual environment:
```bash
uv pip install -e .
```

### Permission Errors

Check:
1. File permissions
2. Files aren't locked by other applications
3. You're running from the correct directory

### LaTeX Compilation Issues

If PDF generation fails:
1. Ensure you have a LaTeX distribution installed (TeX Live, MiKTeX)
2. Check `progress.md` for specific error messages
3. The `.tex` source file is always created even if PDF compilation fails

## Contributing

Contributions are welcome! To add or modify skills:

1. Navigate to `.claude/skills/`
2. Add or modify skill directories with `SKILL.md` files
3. The agent will automatically load them on next run

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with the [Claude Agents SDK](https://docs.claude.com/en/docs/claude-code/sdk/sdk-overview)
- Powered by Anthropic's Claude Sonnet 4.5
- Research lookup powered by Perplexity Sonar Pro via [OpenRouter](https://openrouter.ai)
- Document conversion powered by [MarkItDown](https://github.com/microsoft/markitdown) (Microsoft, MIT License)
- AI-enhanced features via OpenRouter (GPT-4, Claude, Gemini, and 100+ models)

## Support

For issues or questions:
- Open an issue on GitHub
- Check the [SKILLS.md](SKILLS.md) documentation
- Review `progress.md` files in your paper outputs for debugging

## Example Session

**Before starting**: Add your experimental results, figures, and documentation to the `data/` folder:
```bash
cp my_attention_results.csv data/
cp attention_heatmap.png data/
cp performance_comparison.png data/
cp experimental_notes.txt data/
```

**Note**: The writer does not download data, run experiments, or perform analysis. You must provide all experimental results, figures, and supporting materials in the `data/` folder.

```
> Create a NeurIPS paper on sparse attention mechanisms

I'll create a complete NeurIPS conference paper on sparse attention mechanisms...

APPROACH:
- Format: LaTeX (using NeurIPS template)
- Structure: IMRaD with 8-page format
- Citations: BibTeX with ~30-40 references
- Style: NeurIPS citation style
- Data: Will incorporate your experimental results and figures from data/

OUTPUT: paper_outputs/20241027_143022_neurips_sparse_attention/

Starting execution now...

[14:30:22] STARTING: NeurIPS sparse attention paper
[14:30:23] CREATED: paper_outputs/20241027_143022_neurips_sparse_attention/
[14:30:24] CREATED: Folder structure (drafts/, references/, figures/, final/)
[14:30:25] DETECTED: 4 files in data/ folder - processing...
[14:30:26] COPIED: 2 images to figures/, 2 data files to data/
[14:30:27] CREATED: LaTeX document skeleton
[14:30:45] RESEARCH: Literature search for Introduction
[14:31:30] WRITING: Introduction section...
[14:33:15] COMPLETED: Introduction - 750 words, 6 citations ✅
[14:35:20] WRITING: Methods section with your experimental setup...
[14:38:45] WRITING: Results section incorporating your data and figures...
[14:42:10] INCLUDED: attention_heatmap.png as Figure 1
[14:43:25] INCLUDED: performance_comparison.png as Figure 2
...
[14:51:18] COMPILE: Build successful - no errors ✅
[14:51:40] ✅ PROJECT COMPLETE

All files available in: paper_outputs/20241027_143022_neurips_sparse_attention/
```

---

**Ready to revolutionize your scientific writing workflow? Get started now!**
