# CLAUDE.md

> Claude Scientific Writer Fork - Development Documentation
> Forked from: [K-Dense-AI/claude-scientific-writer](https://github.com/K-Dense-AI/claude-scientific-writer) v2.10.0
> Last Updated: 2025-12-24

## Project Overview

This is a **customized fork** of the Claude Scientific Writer plugin, adapted for personal/organizational scientific research writing. It is **not production-ready** and should not be installed as a Claude Code plugin.

### What This Fork Is

- A scientific research writing assistant with 17 specialized skills
- Integrated with Oligon brand standards for document generation
- Focused on academic papers, literature reviews, posters, and presentations
- Uses LaTeX with BibTeX as the default output format

### What Was Removed

Clinical and business-focused skills removed to streamline scientific focus:
- `research-grants`, `clinical-decision-support`, `clinical-reports`
- `market-research-reports`, `treatment-plans`

### What Was Added

- `src/oligon_reports/` - Python package for branded PDF generation (ReportLab)
- `docs/template-project/brand/` - Oligon brand standards and visual identity
- `INTEGRATION_ANALYSIS.md` - Roadmap for template-project merge

---

## Quick Reference

### Package Manager

```bash
uv sync                    # Install dependencies
uv run python <script>     # Run scripts in correct environment
uv run ruff check .        # Lint code
uv run ty                  # Type check
```

### Key Files

| File | Purpose |
|------|---------|
| `skills/` | ⭐ Canonical skill definitions (edit skills here) |
| `.claude/WRITER.md` | Agent instructions for scientific writing |
| `CHANGELOG.md` | Fork customization history |
| `INTEGRATION_ANALYSIS.md` | Template-project merge roadmap |
| `docs/original/` | Archived upstream documentation |

### Active Skills (17)

| Category | Skills |
|----------|--------|
| **Writing** | `scientific-writing`, `literature-review`, `hypothesis-generation` |
| **Presentations** | `scientific-slides`, `latex-posters`, `pptx-posters` |
| **Research** | `research-lookup`, `citation-management`, `peer-review` |
| **Visuals** | `scientific-schematics`, `generate-image` |
| **Documents** | `document-skills`, `markitdown`, `venue-templates` |
| **Analysis** | `scientific-critical-thinking`, `scholar-evaluation` |
| **Conversion** | `paper-2-web` |

---

## Project Structure

```
claude-scientific-writer_fork/
├── skills/                  # ⭐ CANONICAL skill definitions (17 skills)
│   ├── citation-management/
│   ├── document-skills/
│   ├── generate-image/
│   ├── hypothesis-generation/
│   ├── latex-posters/
│   ├── literature-review/
│   ├── markitdown/
│   ├── paper-2-web/
│   ├── peer-review/
│   ├── pptx-posters/
│   ├── research-lookup/
│   ├── scholar-evaluation/
│   ├── scientific-critical-thinking/
│   ├── scientific-schematics/
│   ├── scientific-slides/
│   ├── scientific-writing/
│   └── venue-templates/
├── .claude/
│   ├── WRITER.md            # Agent system instructions
│   └── settings.local.json  # Local Claude Code settings
├── src/
│   └── oligon_reports/      # Branded PDF generation package
│       ├── brand_colors.py  # Color palette constants
│       ├── components.py    # Visual components (MetricCard, CalloutBox, etc.)
│       └── report_generator.py  # PDF orchestrator
├── docs/
│   ├── original/            # Archived upstream documentation
│   └── template-project/
│       └── brand/           # Oligon brand standards
├── scientific_writer/       # Python package (CLI/API - see README inside)
├── scripts/                 # Utility scripts (pdf_to_images, etc.)
├── templates/               # Document templates
├── commands/                # Slash command definitions
├── examples/                # Working examples
├── references/              # Reference materials
├── CHANGELOG.md             # Fork development history
├── INTEGRATION_ANALYSIS.md  # Template merge roadmap
└── pyproject.toml           # uv/Python project config
```

## ⚠️ Skills Development - IMPORTANT

**The `skills/` folder at project root is the ONLY canonical location for skill definitions.**

### Ground Truth

| Location | Status | Action |
|----------|--------|--------|
| `skills/` | ✅ **Canonical** | Edit skills here |
| `.claude/skills/` | ❌ Removed | Was duplicate from upstream |
| `scientific_writer/.claude/skills/` | ❌ Removed | Was installable package copy |

### Why This Matters

The original upstream repo was designed as an installable Claude Code plugin with skills in three locations. Since we're using this as a working project (not installing it), we consolidated to a single source of truth.

### Skill Development Workflow

1. **All skill edits happen in `skills/`**
2. Each skill has a `SKILL.md` defining its capabilities
3. Skills may include `scripts/`, `references/`, `assets/` subdirectories
4. Cross-reference related skills (e.g., scientific-writing → venue-templates)

---

## Python Package (`scientific_writer/`)

A standalone Python package for programmatic paper generation **outside of Claude Code**. Not needed when working directly in Claude Code.

- **CLI**: `uv run scientific-writer` - Interactive terminal interface
- **API**: `from scientific_writer import generate_paper` - For automation
- **Docs**: See `scientific_writer/README.md` for usage details

Uses `claude-agent-sdk` to call Claude with WRITER.md instructions.

---

## Development Workflow

### Human-in-the-Loop Approach

**I prefer to be actively involved in development decisions.** Please follow these guidelines:

- **Don't auto-implement**: Do not start changing files without discussing the plan first
- **Plan before coding**: For substantial changes, create an implementation document or plan
- **Discuss trade-offs**: Present options and let me make architectural decisions
- **Incremental progress**: Break large tasks into reviewable steps

### Implementation Documents

For substantial changes or new features, create a planning document first:

1. **Problem statement**: What are we solving?
2. **Proposed approach**: How will we solve it?
3. **Files affected**: What will change?
4. **Trade-offs**: What are the alternatives and their pros/cons?
5. **Execution phases**: Break into manageable steps

Examples of documents created for this fork:
- `INTEGRATION_ANALYSIS.md` - Template-project merge strategy
- `SKILL_REMOVAL_PLAN.md` - Clinical skill removal (completed, archived to CHANGELOG)

### Making Changes

1. Discuss changes before implementation
2. Create planning docs for substantial work
3. Update `CHANGELOG.md` for significant changes
4. Use conventional commit messages with Claude Code attribution

### Git Workflow

```bash
# Standard commit format
git commit -m "type: description

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Integration Roadmap

See `INTEGRATION_ANALYSIS.md` for the 5-phase plan to merge template-project concepts:

1. **Phase 1**: Template infrastructure (schemas, markdown templates)
2. **Phase 2**: Component extension (FindingCard, StatusTable, etc.)
3. **Phase 3**: Skill creation (`markdown-to-pdf` unified skill)
4. **Phase 4**: Document type expansion (meeting-notes, project-status, etc.)
5. **Phase 5**: Integration polish and testing

---

## Key Documentation

| Document | Description |
|----------|-------------|
| `.claude/WRITER.md` | Scientific writing agent instructions |
| `INTEGRATION_ANALYSIS.md` | Template-project merge analysis |
| `docs/template-project/brand/BRAND_COLORS_v4.md` | Visual identity spec |
| `docs/template-project/brand/DOCUMENT_TEMPLATING_SYSTEM.md` | Templating design |
| `docs/original/SKILLS.md` | Original upstream skills reference |

---

## Upstream Reference

For the original, production-ready Claude Scientific Writer:
- Repository: https://github.com/K-Dense-AI/claude-scientific-writer
- Baseline version: v2.10.0 (2025-12-21)

---

*Fork maintained for personal/organizational scientific writing workflows.*
