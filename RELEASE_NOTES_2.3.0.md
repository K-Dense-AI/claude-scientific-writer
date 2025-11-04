# Scientific Writer v2.3.0 - Edit Papers Anywhere 📝

## 🎉 Write & Edit Scientific Papers Anywhere

This release introduces **Manuscript Editing Mode** - a powerful new workflow that lets you edit existing papers from anywhere! Simply place your manuscript file (`.tex`, `.md`, `.docx`, `.pdf`) in the `data/` folder, and the system automatically recognizes it as an editing task.

## ✨ What's New

### Automatic Editing Mode Detection

The system now intelligently routes files based on their type:

| 📄 File Type | 📁 Destination | 🎯 Purpose |
|-------------|---------------|-----------|
| **Manuscript files** (`.tex`, `.md`, `.docx`, `.pdf`) | `drafts/` | Editing existing manuscripts |
| **Image files** (`.png`, `.jpg`, `.svg`, etc.) | `figures/` | Figures for your paper |
| **Data files** (`.csv`, `.txt`, `.json`, etc.) | `data/` | Data for analysis |

### How It Works

```bash
# 1. Place your manuscript in the data folder
cp my_research_paper.tex data/

# 2. Run scientific writer
scientific-writer

# The system automatically:
# ✓ Detects it's a manuscript file
# ✓ Copies it to drafts/ folder
# ✓ Displays [EDITING MODE] indicator
# ✓ Treats this as an editing task

# 3. Request your edits
> "Improve the introduction and add 5 more citations to the methods section"

# Result:
# - Original manuscript preserved
# - New version created (v2_my_research_paper.tex)
# - All changes documented in revision_notes.md
```

### Clear Visual Feedback

When editing mode is active, you'll see clear indicators:

```
⚠️  EDITING MODE - Manuscript files detected!

📦 Processing files...
   ✓ Copied 1 manuscript file(s) to drafts/ [EDITING MODE]
   ✓ Copied 2 image(s) to figures/
   ✓ Deleted original files from data folder

🔧 TASK: This is an EDITING task, not creating from scratch.
```

## 🚀 Key Features

### 1. **Works with Multiple Formats**
- LaTeX (`.tex`) - Your complete paper
- Markdown (`.md`) - Research notes or drafts
- Word (`.docx`) - Documents from collaborators
- PDF (`.pdf`) - Existing publications to revise

### 2. **Smart File Organization**
- Manuscripts automatically go to `drafts/` folder
- Images automatically go to `figures/` folder
- Data files stay in `data/` folder
- No manual organization needed!

### 3. **Version Control Built-In**
- Original manuscript preserved
- New versions created (v2, v3, etc.)
- Changes documented in `revision_notes.md`
- Full audit trail of all edits

### 4. **Works in Both CLI and API**
- Same behavior in interactive CLI mode
- Same behavior when using programmatic API
- Consistent experience everywhere

## 💡 Use Cases

### Edit a Paper from a Collaborator
```bash
# Collaborator sends you draft.docx
cp draft.docx data/
scientific-writer
> "Convert to LaTeX and add citations for all claims in the introduction"
```

### Improve an Existing LaTeX Paper
```bash
# Working on your submission
cp neurips_submission.tex data/
scientific-writer
> "Address reviewer comments: strengthen methods section and add ablation study"
```

### Revise Based on Feedback
```bash
# Got feedback from advisor
cp thesis_chapter.tex data/
scientific-writer
> "Rewrite the discussion section to address concerns about generalizability"
```

## 🔧 Technical Details

### Files Modified
- `scientific_writer/.claude/WRITER.md` - Added manuscript editing workflow instructions
- `scientific_writer/core.py` - Added manuscript detection and routing logic
- `scientific_writer/cli.py` - Updated UI with editing mode indicators
- `scientific_writer/api.py` - Enhanced progress reporting for manuscripts

### New Functions
- `get_manuscript_extensions()` - Defines manuscript file types
- Enhanced `process_data_files()` - Routes files intelligently
- Enhanced `create_data_context_message()` - Provides editing mode context

### Backward Compatibility
✅ **100% backward compatible**
- All existing functionality preserved
- New behavior only activates for manuscript files
- No breaking changes to API or CLI
- Existing workflows continue to work

## 📦 Installation

```bash
# Update to the latest version
cd claude-scientific-writer
git pull origin main
uv sync

# Verify installation
scientific-writer --version  # Should show 2.3.0
```

## 📚 Documentation

For detailed information, see:
- [CHANGELOG.md](CHANGELOG.md) - Complete version history
- [WRITER.md](scientific_writer/.claude/WRITER.md) - System instructions
- [README.md](README.md) - Full documentation

## 🎯 Example Workflow

Here's a complete workflow showing the power of editing mode:

```bash
# You receive a paper draft from a colleague
cp colleague_draft.docx data/

# Start scientific writer
scientific-writer

# Request comprehensive edits
> "Please:
1. Convert this Word document to LaTeX
2. Improve the introduction with better flow
3. Add 10 more recent citations (2023-2024)
4. Strengthen the methods section
5. Create a new figure summarizing the results
6. Format for Nature journal submission"

# The system will:
# ✓ Recognize this as an editing task
# ✓ Read the existing document
# ✓ Apply all requested changes
# ✓ Create properly versioned outputs
# ✓ Document all changes
# ✓ Generate publication-ready LaTeX
```

## 🙏 What This Means for You

### Before v2.3.0
- Had to manually specify you're editing
- Files could go to wrong folders
- No clear indication of editing vs. creation
- Manual file organization required

### After v2.3.0
- ✨ Automatic detection of editing tasks
- ✨ Smart file routing by type
- ✨ Clear visual feedback throughout
- ✨ Zero manual organization needed
- ✨ Edit papers from **anywhere**!

## 🎊 Summary

Version 2.3.0 makes it effortless to edit scientific papers from any source:
- Drop manuscript files in `data/` folder
- System automatically recognizes editing mode
- Smart routing to correct folders
- Clear feedback and version control
- Works with LaTeX, Markdown, Word, and PDF

**Write and edit scientific papers anywhere! 🚀**

---

**Full Changelog**: [CHANGELOG.md](CHANGELOG.md)

**Questions or Issues?** Open an issue on GitHub or check the [documentation](README.md).

