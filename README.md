# Claude Scientific Writer Fork

A customized fork of [K-Dense-AI/claude-scientific-writer](https://github.com/K-Dense-AI/claude-scientific-writer) (v2.10.0), adapted as a personal skill repository for scientific and biotech writing workflows.

> **Note**: This is a working project for personal/organizational use. It is **not intended to be installed as a Claude Code plugin**. For the production-ready version, use the [upstream repository](https://github.com/K-Dense-AI/claude-scientific-writer).

## What This Is

This fork serves as a **customized skill repository** built on top of the Claude Scientific Writer foundation. Rather than using it as an installable plugin, I use this as a working project directory where:

- Skills are customized for my specific scientific writing needs
- Oligon brand standards are integrated for document generation
- Clinical/business-focused skills have been removed to maintain a pure scientific focus
- New visualization and design skills have been added

### Key Customizations

| Change | Description |
|--------|-------------|
| **Skills Streamlined** | Removed 5 clinical/business skills (`research-grants`, `clinical-decision-support`, `clinical-reports`, `market-research-reports`, `treatment-plans`) |
| **Brand Integration** | Added Oligon brand standards for PDF generation and visual identity |
| **Visualization Skills** | Added `plotting-libraries`, `scientific-visualization`, and `visual-design` skills |
| **Single Source of Truth** | Consolidated skills to one location (`skills/`) instead of three |

## Skills (19 total)

| Category | Skills |
|----------|--------|
| **Writing** | `scientific-writing`, `literature-review`, `hypothesis-generation` |
| **Presentations** | `scientific-slides`, `latex-posters`, `pptx-posters` |
| **Research** | `research-lookup`, `citation-management`, `peer-review`, `scholar-evaluation` |
| **Visuals** | `scientific-schematics`, `generate-image`, `plotting-libraries`, `scientific-visualization`, `visual-design` |
| **Documents** | `markitdown`, `venue-templates` |
| **Analysis** | `scientific-critical-thinking` |
| **Conversion** | `paper-2-web` |

## Project Structure

```
claude-scientific-writer_fork/
├── skills/                  # Canonical skill definitions (19 skills)
├── .claude/
│   └── WRITER.md            # Agent system instructions
├── src/oligon_reports/      # Branded PDF generation (ReportLab)
├── docs/
│   ├── original/            # Archived upstream documentation
│   └── template-project/    # Oligon brand standards
├── scientific_writer/       # Python package (CLI/API)
├── templates/               # Document templates
├── examples/                # Working examples
├── CLAUDE.md                # Development documentation
├── CHANGELOG.md             # Fork development history
└── INTEGRATION_ANALYSIS.md  # Template merge roadmap
```

## Getting Started

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager
- LaTeX distribution (MacTeX, TeX Live, or MiKTeX)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/claude-scientific-writer_fork.git
cd claude-scientific-writer_fork

# Install dependencies with uv
uv sync
```

### Usage

This project is designed to be used as a **working directory with Claude Code**, not as an installed plugin.

1. Open this directory in Claude Code
2. The skills in `skills/` provide specialized capabilities for scientific writing
3. Invoke skills as needed during your writing workflow

For programmatic usage outside Claude Code:

```bash
# CLI interface
uv run scientific-writer

# Or use the Python API
from scientific_writer import generate_paper
```

## Development

### Package Manager

```bash
uv sync                    # Install dependencies
uv run python <script>     # Run scripts in correct environment
uv run ruff check .        # Lint code
uv run ty                  # Type check
```

### Editing Skills

All skill edits happen in the `skills/` directory. Each skill has:
- `SKILL.md` - Skill definition and capabilities
- `scripts/` - Optional automation scripts
- `references/` - Optional reference materials
- `assets/` - Optional static assets

### Documentation

| Document | Description |
|----------|-------------|
| `CLAUDE.md` | Development documentation and workflow |
| `CHANGELOG.md` | Fork customization history |
| `INTEGRATION_ANALYSIS.md` | Template-project merge roadmap |
| `.claude/WRITER.md` | Scientific writing agent instructions |

## Upstream Reference

This fork is based on [K-Dense-AI/claude-scientific-writer](https://github.com/K-Dense-AI/claude-scientific-writer) v2.10.0.

For the production-ready Claude Scientific Writer plugin, visit the upstream repository.

## License

MIT (inherited from upstream)
