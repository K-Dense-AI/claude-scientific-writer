# Claude Scientific Writer

[![PyPI version](https://img.shields.io/pypi/v/scientific-writer.svg)](https://pypi.org/project/scientific-writer/)
[![Total Downloads](https://static.pepy.tech/badge/scientific-writer)](https://pepy.tech/project/scientific-writer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python package and CLI for generating publication-ready scientific papers, reports, posters, grant proposals, and more academic documents with Claude Sonnet 4.5. Features real-time research lookup, intelligent paper detection, and comprehensive document conversion. Version 2.0 adds a fully typed, programmatic API while keeping the CLI 100% backward compatible.

**✨ What's New in v2.0+**
- Programmatic Python API with async support
- Research lookup with Perplexity Sonar Pro
- Intelligent paper detection (auto-resume editing)
- Clinical reports (case reports, diagnostic reports, trial reports, HIPAA compliance)
- Grant proposal generation (NSF, NIH, DOE, DARPA)
- Research posters with LaTeX
- Scientific schematics (CONSORT, circuits, pathways)
- Document conversion (15+ formats with MarkItDown)
- ScholarEval peer review framework

## Quick Start

### Prerequisites
- Python 3.10-3.12
- ANTHROPIC_API_KEY (required), OPENROUTER_API_KEY (optional for research lookup)

### Install

#### Option 1: Install from PyPI (Recommended)
```bash
pip install scientific-writer
```

#### Option 2: Install from source with uv
```bash
git clone https://github.com/yourusername/claude-scientific-writer.git
cd claude-scientific-writer
uv sync
```

### Configure API keys
```bash
# .env file (recommended)
echo "ANTHROPIC_API_KEY=your_key" > .env
echo "OPENROUTER_API_KEY=your_openrouter_key" >> .env
# or export in your shell
export ANTHROPIC_API_KEY='your_key'
```

### Use the CLI
```bash
# If installed via pip
scientific-writer

# If installed from source with uv
uv run scientific-writer
```

### Use the Python API
```python
import asyncio
from scientific_writer import generate_paper

async def main():
    async for update in generate_paper("Create a Nature paper on CRISPR gene editing"):
        if update["type"] == "progress":
            print(f"[{update['percentage']}%] {update['message']}")
        else:
            print(f"PDF: {update['files']['pdf_final']}")

asyncio.run(main())
```

## Features

### 📝 Document Generation
- **Scientific papers** with IMRaD structure (Nature, Science, NeurIPS, etc.)
- **Clinical reports** (case reports, diagnostic reports, trial reports, patient documentation)
- **Research posters** using LaTeX (beamerposter, tikzposter, baposter)
- **Grant proposals** (NSF, NIH, DOE, DARPA) with agency-specific formatting
- **Literature reviews** with systematic citation management
- **Scientific schematics** (CONSORT diagrams, circuit diagrams, biological pathways)

### 🤖 AI-Powered Capabilities
- **Real-time research lookup** using Perplexity Sonar Pro (via OpenRouter)
- **Intelligent paper detection** - automatically identifies references to existing papers
- **Peer review feedback** with quantitative ScholarEval framework (8-dimension scoring)
- **Iterative editing** with context-aware revision suggestions

### 🔧 Developer-Friendly
- **Programmatic API** - Full async Python API with type hints
- **CLI interface** - Interactive command-line tool with progress tracking
- **Progress streaming** - Real-time updates during generation
- **Comprehensive results** - JSON output with metadata, file paths, citations

### 📦 Data & File Integration
- **Automatic data handling** - Drop files in `data/`, auto-sorted to `figures/` or `data/`
- **Document conversion** - PDF, DOCX, PPTX, XLSX to Markdown with MarkItDown
- **Bibliography management** - Automatic BibTeX generation and citation formatting
- **Figure integration** - Images automatically referenced and organized

## Typical Workflow

### CLI Usage
1. Place figures and data in `data/` at the project root (images → `figures/`, files → `data/` automatically)
2. Run `scientific-writer` and describe what you want
3. Follow progress updates; outputs saved to `paper_outputs/<timestamp>_<topic>/`

```bash
# Start a new paper
> Create a Nature paper on CRISPR gene editing with 5 key references

# Continue editing (automatically detected)
> Add a methods section about the experimental setup

# Reference existing paper by topic
> Find the acoustics paper and add a conclusion section

# Generate a grant proposal
> Write an NSF proposal for quantum computing research

# Create a research poster
> Generate a conference poster from my paper
```

### API Usage
```python
import asyncio
from scientific_writer import generate_paper

async def main():
    async for update in generate_paper(
        query="Create a NeurIPS paper on transformers",
        data_files=["results.csv", "figure.png"],
        output_dir="./my_papers"
    ):
        if update["type"] == "progress":
            print(f"[{update['percentage']}%] {update['message']}")
        else:
            print(f"✓ PDF: {update['files']['pdf_final']}")

asyncio.run(main())
```

## Quick Reference

### Common Commands

| Task | Command Example |
|------|----------------|
| **Scientific Paper** | `> Create a Nature paper on CRISPR gene editing` |
| **Clinical Report** | `> Create a clinical case report for rare disease presentation` |
| **Grant Proposal** | `> Write an NSF proposal for quantum computing research` |
| **Research Poster** | `> Generate a conference poster from my paper` |
| **Literature Review** | `> Create a literature review on machine learning in healthcare` |
| **Peer Review** | `> Evaluate this paper using the ScholarEval framework` |
| **Continue Editing** | `> Add a methods section` (automatically continues current paper) |
| **Find Existing Paper** | `> Find the acoustics paper and add a conclusion` |
| **New Paper** | `> new paper on climate change` (explicitly start fresh) |

### Research Lookup Examples

```bash
# Recent research (auto-triggers research lookup)
> Create a paper on recent advances in quantum computing (2024)

# Fact verification
> What are the current success rates for CAR-T therapy?

# Literature search
> Find 10 recent papers on transformer architectures from 2023-2024
```

### Document Types

| Type | Example |
|------|---------|
| **Papers** | Nature, Science, NeurIPS, ICML, IEEE, ACM |
| **Clinical Reports** | Case reports, diagnostic reports, trial reports, patient notes |
| **Grants** | NSF, NIH R01/R21/K, DOE, DARPA |
| **Posters** | Conference posters (A0, A1, custom sizes) |
| **Reviews** | Systematic literature reviews |
| **Schematics** | CONSORT diagrams, circuits, biological pathways |

### File Handling

```bash
# 1. Drop files in data/ folder
cp results.csv ~/Documents/claude-scientific-writer/data/
cp figure.png ~/Documents/claude-scientific-writer/data/

# 2. Files are auto-sorted:
#    Images (png, jpg, svg) → figures/
#    Data (csv, json, txt) → data/

# 3. Reference in paper
> Create a paper analyzing the experimental results in results.csv
```

### API Quick Start

```python
import asyncio
from scientific_writer import generate_paper

# Simple usage
async for update in generate_paper("Create a Nature paper on CRISPR"):
    if update["type"] == "result":
        print(f"PDF: {update['files']['pdf_final']}")

# With data files
async for update in generate_paper(
    query="Analyze experimental results",
    data_files=["results.csv", "figure.png"],
    output_dir="./papers"
):
    if update["type"] == "progress":
        print(f"[{update['percentage']}%] {update['message']}")
```

## Documentation

### User Guides
- [📖 Complete Features Guide](docs/FEATURES.md) - Comprehensive overview of all capabilities
- [🔧 API Reference](docs/API.md) - Full programmatic API documentation
- [🎯 Skills Overview](docs/SKILLS.md) - All available skills and tools
- [🐛 Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions

### Developer Resources
- [💻 Development Guide](docs/DEVELOPMENT.md) - Contributing and development setup
- [📦 Releasing Guide](docs/RELEASING.md) - Versioning and publishing
- [📋 Release Notes](CHANGELOG.md) - Version history and updates
- [🤖 System Instructions](CLAUDE.md) - Agent instructions (advanced)

## Versioning and Publishing (short)
Use `uv` and the helper scripts:
- Bump version (keeps pyproject + __init__ in sync): `uv run scripts/bump_version.py [patch|minor|major]`
- Build and publish: `uv run scripts/publish.py` (or `--bump patch|minor|major`)
See [docs/RELEASING.md](docs/RELEASING.md) for prerequisites, dry runs, tagging, and verification.

## Migration (v1.x -> v2.0)
- CLI remains unchanged (scientific-writer).
- New programmatic API: from scientific_writer import generate_paper.
- Legacy single-file script is replaced by a proper package; no action needed for CLI users.

## License
MIT - see LICENSE.

## Support
- Open an issue on GitHub
- See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common problems

## ⭐ Show Your Support

If you find this project helpful for your research or work, please consider giving it a star on GitHub! It helps others discover the tool and motivates continued development. Thank you! 🙏

![GitHub stars](https://img.shields.io/github/stars/K-Dense-AI/claude-scientific-writer?style=social)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=K-Dense-AI/claude-scientific-writer&type=Date)](https://star-history.com/#K-Dense-AI/claude-scientific-writer&Date)