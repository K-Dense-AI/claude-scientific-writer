# Changelog

All notable changes to the Scientific Writer project will be documented in this file.

## [Unreleased]

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

