# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `SKILL_REMOVAL_PLAN.md` - Detailed plan for removing 5 clinical/business-focused skills:
  - Skills targeted: `research-grants`, `clinical-decision-support`, `clinical-reports`, `market-research-reports`, `treatment-plans`
  - Inventory of 15 directories to delete across 3 locations
  - 9 files requiring cross-reference updates
  - 6-phase execution plan with verification steps
- uv package manager setup with `uv sync` for environment management
- `reportlab>=4.0` dependency for PDF generation in oligon_reports module
- `INTEGRATION_ANALYSIS.md` - Comprehensive cross-reference analysis of template-project design vs scientific-writer skill system
  - Document type mapping (12 template types to existing skills)
  - Architectural comparison of both approaches
  - Merged architecture strategy with 5-phase implementation plan
  - Target file organization structure
- New README.md with warning callout indicating fork is not ready for end-user use
- Documentation pointing users to upstream repository for production use
- Synthesized assets from Oligon template_project repository:
  - `src/oligon_reports/` - Python package for branded PDF report generation
    - `brand_colors.py` - Oligon color palette and typography constants
    - `components.py` - Reusable visual components (MetricCard, CalloutBox, Timeline, etc.)
    - `report_generator.py` - Main PDF generation orchestrator
  - `docs/brand/` - Brand standards documentation
    - `BRAND_COLORS_v4.md` - Comprehensive visual identity specification
    - `DOCUMENT_TEMPLATING_SYSTEM.md` - Document templating system design
    - `ROADMAP.md` - Development roadmap
  - `references/` - Templates and guides
    - `Oligon_Template.pot` - PowerPoint master template
    - `pdf_python_guide.md` - PDF generation reference
  - `examples/` - Working report examples
    - `basic_report.py` - Basic report example
    - `pareto_reports.py` - Pareto analysis reports

### Changed

- Reorganized `docs/` folder to separate documentation by origin:
  - `docs/original/` - Documentation from upstream scientific-writer project
    - Core docs: API.md, DEVELOPMENT.md, FEATURES.md, SKILLS.md, etc.
    - `archived/` - Original files with .original suffix
    - `examples/` - Scientific writing examples (grants, posters, slides, etc.)
  - `docs/template-project/` - Documentation from Oligon template_project
    - `brand/` - Brand standards and visual identity specs

### Removed

- Cursor IDE configuration files (`.cursor/`, `.cursorignore`)

## [0.1.0] - 2024-12-23

### Added

- Forked from [K-Dense-AI/claude-scientific-writer](https://github.com/K-Dense-AI/claude-scientific-writer) v2.10.0
- This changelog to track customizations and development

### Changed

- Archived original end-user documentation to `docs/` for reference:
  - `CLAUDE.md` → `docs/CLAUDE.original.md`
  - `README.md` → `docs/README.original.md`
  - `CHANGELOG.md` → `docs/CHANGELOG.original.md`
  - `TESTING_INSTRUCTIONS.md` → `docs/TESTING_INSTRUCTIONS.original.md`
  - `example_api_usage.py` → `docs/example_api_usage.original.py`
  - `test-marketplace-example.json` → `docs/test-marketplace-example.original.json`

### Notes

This fork is being customized for personal/organizational use cases. The original
documentation was oriented toward end-users of the published plugin and CLI tool.
Archiving these files provides a clean foundation for development while preserving
the upstream documentation for reference.

**Upstream baseline:** v2.10.0 (2025-12-21)

---

For the original project's changelog, see `docs/CHANGELOG.original.md`.
