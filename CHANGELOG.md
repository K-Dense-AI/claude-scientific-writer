# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Skills consolidation: `skills/` is now the single canonical location
  - Removed duplicate `.claude/skills/` (was 17 skill directories)
  - Removed duplicate `scientific_writer/.claude/skills/` (was installable package copy)
  - Updated `CLAUDE.md` with clear skills development guidance
  - Cleaned up `.claude/settings.local.json` (removed verbose git commit permission)
- `docs/template-project/brand/visual-design-SKILL.md`: Design philosophy skill for scientific visuals
  - Adapted from frontend-design-SKILL.md for scientific outputs (figures, infographics, reports, presentations, posters)
  - Design thinking framework, typography principles, color philosophy, composition guidelines
  - Anti-pattern guidance ("avoiding default syndrome")
  - Cross-references to implementation skills (scientific-schematics, scientific-slides, etc.)
  - Quality checklist for visual outputs
- `docs/template-project/scientific-visualization-SKILL.md`: Comprehensive matplotlib/seaborn implementation guide
  - Publication-quality figure creation with code examples
  - Journal-specific specifications (Nature, Science, Cell, etc.)
  - Colorblind-safe palettes and accessibility guidance
  - Multi-panel figure layouts and export settings
  - Cross-reference to visual-design for design philosophy
- `INTEGRATION_ANALYSIS.md` Section 11: Future visual design skill architecture (Option D)
  - Documents parent-child refactoring plan for visual output skills
  - Phase D.1-D.4 implementation steps with effort estimates
  - Files affected, success criteria, and execution triggers
- `CLAUDE.md`: Root project documentation for the fork
  - Project overview and fork identity (not production-ready notice)
  - Quick reference (uv commands, key files, 17 active skills)
  - Project structure with known architectural issues (skill duplication)
  - Human-in-the-loop development workflow preferences
  - Implementation document guidelines for substantial changes
  - Integration roadmap reference and upstream links
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

- `INTEGRATION_ANALYSIS.md`: Added Section 10 documenting completed skill removal procedure with phases, rationale, and resulting skill count
- `.claude/settings.local.json`: Removed stale bash permission rules from skill removal process
- **Additional cleanup (Phase 4 verification):** Removed skill references from files not covered in original plan
  - `commands/scientific-writer-init.md`: Updated skill count (17 skills), removed clinical/grant examples, added hypothesis-generation
  - `templates/CLAUDE.scientific-writer.md`: Removed market-research-reports section (~55 lines), clinical-decision-support section (~190 lines), updated figure requirements table and checklists
  - `scientific_writer/.claude/skills/venue-templates/SKILL.md`: Refactored "Research Grants" section to standalone grant template guidance
  - `scientific_writer/.claude/skills/hypothesis-generation/assets/FORMATTING_GUIDE.md`: Removed treatment-plans reference
- **Main documentation updated (Phase 3):** Removed skill references from active documentation
  - `.claude/WRITER.md` and `scientific_writer/.claude/WRITER.md`: Removed 4 rows from "Special Document Types" table and 3 rows from "MINIMUM Figure Requirements" table
  - `INTEGRATION_ANALYSIS.md`: Updated Section 1 (removed skill mappings) and Section 5 (changed "Clinical/grant/poster specialized skills" to "Poster specialized skills")
  - `docs/original/SKILLS.md`: Added fork customization note listing removed skills
  - `docs/original/README.md`: Added fork customization note
  - `docs/original/DOCUMENTATION_INDEX.md`: Added fork customization note
  - `docs/original/DEVELOPMENT.md`: Added fork customization note
- **Cross-skill references updated (Phase 2):** Removed references to deleted skills
  - `venue-templates/SKILL.md`: Removed "Research Grants" subsection referencing `research-grants` skill
  - `hypothesis-generation/assets/FORMATTING_GUIDE.md`: Removed `treatment-plans` skill reference
  - Updates applied to both `.claude/skills/` and `skills/` directories
- Reorganized `docs/` folder to separate documentation by origin:
  - `docs/original/` - Documentation from upstream scientific-writer project
    - Core docs: API.md, DEVELOPMENT.md, FEATURES.md, SKILLS.md, etc.
    - `archived/` - Original files with .original suffix
    - `examples/` - Scientific writing examples (grants, posters, slides, etc.)
  - `docs/template-project/` - Documentation from Oligon template_project
    - `brand/` - Brand standards and visual identity specs

### Removed

- `docs/template-project/brand/frontend-design-SKILL.md`: Web UI design template no longer needed after extracting concepts into visual-design-SKILL.md
- `SKILL_REMOVAL_PLAN.md`: Deleted after completion (content preserved in CHANGELOG.md and INTEGRATION_ANALYSIS.md)
- **Skill directories removed (Phase 1):** 15 directories containing clinical/business-focused skills
  - `.claude/skills/`: research-grants, clinical-decision-support, clinical-reports, market-research-reports, treatment-plans
  - `skills/`: duplicate copies of the above 5 skills
  - `scientific_writer/.claude/skills/`: nested duplicate copies of the above 5 skills
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
