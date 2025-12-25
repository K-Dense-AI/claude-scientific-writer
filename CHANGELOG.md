# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- `skills/scientific-writing/`: **Refactored for token efficiency** (health score: 52% → 95%, tokens: ~8428 → ~3139)
  - **SKILL.md**:
    - Added frontmatter: `version: 1.0.0`, improved description with trigger verb ("Guides...")
    - Fixed `allowed-tools` format (array → space-separated)
    - Extracted Field-Specific Language section to `references/field_terminology.md` (90 → 12 lines)
    - Extracted Writing Process section to `references/writing_process.md` (108 → 18 lines)
    - Reduced Visual Enhancement section (90 → 25 lines, delegates to scientific-schematics/generate-image)
    - Reduced Section-Specific Writing Guidance (60 → 15 lines, references imrad_structure.md)
    - Reduced Figures and Tables section (47 → 11 lines, references figures_tables.md)
    - Reduced Writing Principles section (28 → 3 lines, references writing_principles.md)
    - Reduced Workflow section (38 → 8 lines)
    - Reduced Pre-Submission Tests section (28 → 7 lines)
    - Fixed 10 broken cross-skill references (scripts → skill invocations, venue-templates paths)
  - **New reference files**:
    - `references/field_terminology.md`: Discipline-specific terminology guides (Biomedical, Molecular Biology, Chemistry, Ecology, Physics, Neuroscience, Social Sciences)
    - `references/writing_process.md`: Two-stage writing process with examples (outline → prose conversion)
  - Removed `IMPLEMENTATION_PLAN.md` after completion (validation cleanup)
- `skills/scientific-writing/`: Major best practices update aligned with modern scientific writing guidelines
  - **SKILL.md**:
    - Added **Core Philosophy** section (reader-centricity, parsimony, logical flow as narrative)
    - Added **Executive Summary vs Abstract** comparison table and guidelines
    - Enhanced **Introduction Development** with visual Funnel Approach diagram (BROAD→NARROW→GAP→SPECIFIC)
    - Added **Message Trumps Beauty** principle to Figures & Tables section
    - Added **Color Strategy** guidelines (accessibility, sequential vs qualitative palettes, avoid red/green)
    - Added **Chart Selection Guide** table with recommended vs avoid columns
    - Added **Pre-Submission Diagnostic Tests** (Elevator Pitch, Independence, "So What?" tests)
  - **references/writing_principles.md**:
    - Added **C-C-C Framework** (Context-Content-Conclusion) for paragraph structure with example
  - **references/figures_tables.md**:
    - Added **Message Trumps Beauty** as Principle 0 (the cardinal rule) with three diagnostic questions
    - Enhanced **Clarity and Simplicity** section with explicit chartjunk elimination list and data-ink ratio guidance
- `skills/visual-design/`: Skill audit and improvements (76% → 90% health score)
  - Added frontmatter: `version: 1.0.0`, `allowed-tools: Read, Glob, Write`
  - Improved description with explicit trigger conditions ("Use when...")
  - Strengthened opening to imperative voice
  - Created `references/` directory with `BRAND_COLORS_v4.md` (copied from docs/template-project/brand/)
  - Updated all internal file references to use local paths
  - Removed weak closing meta-commentary
  - Clarified skill purpose: design philosophy only, delegates code to `plotting-libraries` and `scientific-visualization`
- `README.md`: Complete rewrite with comprehensive project documentation
  - Clear fork identity and purpose (customized skill repository, not a plugin)
  - Key customizations table (skills removed, brand integration, visualization skills added)
  - Updated skill inventory (19 skills organized by category)
  - Project structure overview
  - Getting started guide with prerequisites and installation
  - Development workflow documentation
- `CLAUDE.md`: Updated to reflect current project state
  - Skill count updated from 17 to 19
  - Added new visualization skills to "What Was Added" section (`plotting-libraries`, `scientific-visualization`, `visual-design`)
  - Updated Active Skills table with correct categorization
  - Updated project structure with all 19 skill directories
  - Last Updated date set to 2025-12-25
- `.claude/settings.local.json`: Added `readme-skill` to auto-approved skills

### Added

- `skills/scientific-writing/IMPLEMENTATION_PLAN.md`: Audit-driven improvement plan for scientific-writing skill
  - Comprehensive skill audit using skill-reviewer (health score: 52%)
  - 4-phase implementation strategy targeting 85%+ health score
  - Phase 1: Frontmatter fixes (version, description triggers, allowed-tools format)
  - Phase 2: Fix 10 broken cross-skill references (scripts, venue-templates)
  - Phase 3: Token reduction (~8,428 → ~2,400 tokens) via content extraction
  - New reference files planned: `field_terminology.md`, `writing_process.md`
  - Step-by-step instructions with before/after code snippets
  - Validation commands and rollback plan included
- `skills/venue-templates/REVIEW_AND_IMPROVEMENTS.md`: Comprehensive skill review and improvement plan
  - Current state assessment with gap analysis (75+ venues documented, ~6 templates exist)
  - Priority-ranked improvement proposals (template expansion, script enhancement, documentation)
  - Implementation roadmap with 3 phases and effort estimates
  - Template acquisition strategy with official source URLs
  - Quality metrics (current vs. target coverage)
  - **Section 8: Integration Points Analysis** (new)
    - Current integration map: 5 outbound + 5 inbound skill references documented
    - 11 skills identified WITHOUT venue-templates integration (gaps)
    - Proposed new integrations for scientific-slides, pptx-posters, scientific-schematics, paper-2-web, plotting-libraries, generate-image, visual-design
    - Proposed additions: presentations_formatting.md, figure_requirements_by_venue.md
    - Implementation checklist with 3 phases (A: update other skills, B: expand venue-templates, C: consolidation)
    - Integration architecture diagram showing skill relationships
- `skills/scientific-schematics/IMPLEMENTATION_PLAN_GEMINI_MODELS.md`: Implementation plan for model configuration update
  - Switch default review model from Gemini 3 Pro to Gemini 3 Flash Preview (faster, cheaper)
  - Add `--review-model` CLI flag to allow Pro override for critical work
  - Strengthen review prompts with step-by-step reasoning for Flash optimization
  - Keep Nano Banana Pro for image generation (specialized model, no change)
  - 4-phase implementation plan with file-by-file changes documented
- `skills/plotting-libraries/`: New skill for Python plotting libraries (matplotlib & seaborn)
  - Main `SKILL.md` with decision framework for choosing between libraries
  - `references/matplotlib.md` - comprehensive matplotlib reference
  - `references/seaborn.md` - comprehensive seaborn statistical visualization reference
  - Cross-references to `scientific-visualization` (publication specs) and `visual-design` (aesthetics)
- `skills/visual-design/`: Moved from `docs/template-project/brand/` to canonical skills location
- `skills/scientific-visualization/`: Moved from `docs/template-project/` to canonical skills location
- Cross-references between visualization skills:
  - `scientific-visualization` → links to `visual-design` and `plotting-libraries`
  - `visual-design` → links to `plotting-libraries` for implementation
- `scientific_writer/README.md`: Documentation for the Python package
  - Explains CLI and API usage for programmatic paper generation
  - Added corresponding section in `CLAUDE.md` for quick reference
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
