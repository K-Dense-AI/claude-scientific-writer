# Changelog

All notable changes to the Scientific Writer project will be documented in this file.

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

