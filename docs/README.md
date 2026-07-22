# Scientific Writer Documentation

Welcome to the Scientific Writer documentation! **Scientific Writer is a deep research and writing tool** that combines the power of AI-driven deep research with well-formatted written outputs of various forms—from scientific papers and grant proposals to clinical reports and conference presentations.

This guide will help you navigate the available resources.

## 📚 Documentation Overview

> 💡 **New!** Check out the [Complete Documentation Index](DOCUMENTATION_INDEX.md) for a comprehensive navigation guide with learning paths and quick reference.

### For New Users

Start here to get up and running quickly:

1. **[Main README](../README.md)** - Quick start, installation, and basic usage
2. **[Complete Features Guide](FEATURES.md)** - Comprehensive overview of all capabilities
3. **[Skills Overview](SKILLS.md)** - Available skills and what they can do
4. **[Plugin Installation](../README.md#-use-as-a-claude-code-plugin-recommended)** - Claude Code plugin setup (recommended)

### For Developers

Integrate Scientific Writer into your Python projects:

1. **[API Reference](API.md)** - Full programmatic API documentation
2. **[Contributing Guide](../CONTRIBUTING.md)** - Dev setup, tests, and PR guidelines
3. **[Development Guide](DEVELOPMENT.md)** - Architecture and plugin development
4. **[Skill Authoring Guide](SKILL_AUTHORING.md)** - How to write and register a new skill
5. **[Releasing Guide](RELEASING.md)** - Versioning and publishing workflow

### For Troubleshooting

Having issues? Check these resources:

1. **[Troubleshooting Guide](TROUBLESHOOTING.md)** - Common issues and solutions
2. **[Changelog](../CHANGELOG.md)** - Version history and breaking changes

## 🎯 Usage Modes

Scientific Writer can be used in three ways:

1. **🌟 Claude Code Plugin (Recommended)** - Use directly in your IDE
   - One-command setup: `/claude-scientific-writer:scientific-writer-init`
   - All 26 selected skills available immediately
   - No CLI required
   - See: [Plugin Installation Guide](../README.md#-use-as-a-claude-code-plugin-recommended)

2. **💻 Command Line Interface (CLI)** - Interactive scientific writing
   - Run: `scientific-writer` or `uv run scientific-writer`
   - Full-featured interactive mode
   - See: [CLI Quick Start](../README.md#use-the-cli)

3. **🔧 Python API** - Programmatic integration
   - Import: `from scientific_writer import generate_paper`
   - Async API with progress streaming
   - See: [API Reference](API.md)

## 🎯 Quick Navigation by Task

### I Want to Generate a...

| Document Type | Start Here |
|--------------|------------|
| **Scientific Paper** | [README Quick Start](../README.md#quick-start) → [Features: Scientific Papers](FEATURES.md#scientific-papers) |
| **Grant Proposal** | [Features: Grant Proposals](FEATURES.md#grant-proposals) → [Skills: Research Grants](SKILLS.md#5-research-grants) |
| **Research Poster** | [Features: Research Posters](FEATURES.md#research-posters) → [Skills: LaTeX Posters](SKILLS.md#8-latex-research-posters-default) |
| **Literature Review** | [Features: Literature Reviews](FEATURES.md#literature-reviews) → [Skills: Literature Review](SKILLS.md#2-literature-review) |
| **Scientific Diagram** | [Features: Scientific Schematics](FEATURES.md#scientific-schematics) → [Skills: Scientific Schematics](SKILLS.md#10-scientific-schematics-and-diagrams) |

### I Want to...

| Task | Documentation |
|------|---------------|
| **Use the Python API** | [API Reference](API.md) → [README: API Usage](../README.md#api-usage) |
| **Understand research lookup** | [Features: Real-Time Research Lookup](FEATURES.md#real-time-research-lookup) → [API: Research Lookup](API.md#research-lookup) |
| **Auto-detect existing papers** | [Features: Intelligent Paper Detection](FEATURES.md#intelligent-paper-detection) |
| **Process data files** | [Features: Data & File Integration](FEATURES.md#data--file-integration) → [README: File Handling](../README.md#file-handling) |
| **Convert documents** | [Features: Document Conversion](FEATURES.md#document-conversion) → [Skills: MarkItDown](SKILLS.md#14-markitdown---universal-file-to-markdown-converter) |
| **Get peer review** | [Features: Peer Review with ScholarEval](FEATURES.md#peer-review-with-scholareval) → [Skills: Scholar Evaluation](SKILLS.md#4-scholar-evaluation) |
| **Fix an issue** | [Troubleshooting Guide](TROUBLESHOOTING.md) |
| **Contribute code** | [Development Guide](DEVELOPMENT.md) |

## 📖 Complete Documentation Index

### User Documentation

1. **[README.md](../README.md)** - Main package documentation
   - Quick Start
   - Installation
   - Features Overview
   - Basic Usage (CLI and API)
   - Quick Reference
   - Examples

2. **[FEATURES.md](FEATURES.md)** - Complete features guide
   - Document Generation (papers, posters, grants, reviews, schematics)
   - AI-Powered Capabilities (research lookup, peer review, editing)
   - Intelligent Paper Detection
   - Data & File Integration
   - Document Conversion
   - Developer Features

3. **[API.md](API.md)** - Programmatic API reference
   - API Functions
   - Data Models
   - Usage Patterns
   - Advanced Features
   - Environment Variables
   - Error Handling
   - Best Practices

4. **[SKILLS.md](SKILLS.md)** - Available skills and capabilities
   - Writing Skills (scientific writing, literature review, peer review, scholar evaluation, grants, posters, schematics)
   - Document Manipulation Skills (MarkItDown, DOCX, PDF, PPTX, XLSX)
   - Usage Examples

5. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
   - Installation issues
   - LaTeX compilation errors
   - API key problems
   - Runtime errors
   - Performance issues

### Developer Documentation

6. **[DEVELOPMENT.md](DEVELOPMENT.md)** - Development and contributing
   - Setting up development environment
   - Code structure
   - Testing
   - Contributing guidelines

7. **[RELEASING.md](RELEASING.md)** - Version management and publishing
   - Versioning strategy
   - Release process
   - Publishing to PyPI
   - Git tagging

8. **[CHANGELOG.md](../CHANGELOG.md)** - Version history
   - Release notes
   - Breaking changes
   - New features
   - Bug fixes

### Advanced

9. **[CLAUDE.md](../CLAUDE.md)** - System instructions for the agent
   - Agent behavior guidelines
   - Skill integration
   - Tool usage patterns

## 🔍 Search Tips

When looking for specific information:

### By Topic
- **API usage**: Search in [API.md](API.md)
- **CLI commands**: Search in [README.md](../README.md) and [FEATURES.md](FEATURES.md)
- **Skills/capabilities**: Search in [SKILLS.md](SKILLS.md)
- **Errors/issues**: Search in [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Recent changes**: Check [CHANGELOG.md](../CHANGELOG.md)

### By Keywords
- `generate_paper()` → [API.md](API.md)
- `scientific-writer` → [README.md](../README.md)
- `NSF`/`NIH`/`DOE`/`DARPA` → [SKILLS.md](SKILLS.md#5-research-grants)
- `CONSORT`/`circuit`/`pathway` → [SKILLS.md](SKILLS.md#10-scientific-schematics-and-diagrams)
- `MarkItDown` → [SKILLS.md](SKILLS.md#14-markitdown---universal-file-to-markdown-converter)
- `ScholarEval` → [SKILLS.md](SKILLS.md#4-scholar-evaluation)
- `data files` → [FEATURES.md](FEATURES.md#automatic-data-handling)
- `research lookup` → [FEATURES.md](FEATURES.md#real-time-research-lookup)

## 💡 Getting Help

If you can't find what you're looking for:

1. **Check the [Troubleshooting Guide](TROUBLESHOOTING.md)**
2. **Search the [Changelog](../CHANGELOG.md)** for recent updates
3. **Review the [Skills Overview](SKILLS.md)** to see all capabilities
4. **Open an issue on GitHub** with your question

## 🚀 Quick Links

- [Installation](../README.md#installation-options)
- [CLI Quick Start](../README.md#use-the-cli)
- [API Quick Start](../README.md#use-the-python-api)
- [Common Commands](../README.md#common-commands)
- [Example Code](../example_api_usage.py)
- [PyPI Package](https://pypi.org/project/scientific-writer/)

---

**Last Updated**: July 4, 2026 (v2.15.1)

