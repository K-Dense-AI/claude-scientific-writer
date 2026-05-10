# docx-editor-zotero

**Edit Word documents while preserving Zotero citations**

A Claude skill for modifying Word (.docx) files with complete preservation of Zotero field codes, citations, and bibliography references.

## ✨ Features

- ✅ **Delete paragraphs** without losing citations
- ✅ **Reorder paragraphs** while maintaining document structure
- ✅ **Replace text** (HSG → Tkk, etc.) throughout document
- ✅ **100% Zotero preservation** - all citations remain intact
- ✅ **Automatic validation** - detects orphaned citations
- ✅ **Audit logs** - JSON logs track all changes
- ✅ **Complex documents** - handles tables, nested elements
- ✅ **Zero dependencies** - uses Python stdlib only

## 🎯 Use Cases

- Remove or reorganize article sections while keeping citations
- Edit/revise papers with automatic citation preservation
- Bulk text replacement (terminology updates, etc.)
- Restructure documents without losing research references

## 📦 Installation

### Option 1: Copy to Claude Code skills directory

```bash
mkdir -p ~/.claude/skills/docx-editor-zotero/
cp docx-editor-zotero.md ~/.claude/skills/docx-editor-zotero/
cp word_editor.py ~/.claude/skills/docx-editor-zotero/
cp zotero_docx_preserver.py ~/.claude/skills/docx-editor-zotero/
```

### Option 2: Add to existing project

```bash
cp word_editor.py /your/project/
cp zotero_docx_preserver.py /your/project/
```

## 🚀 Usage

### In Claude Code (using the skill)

```
/docx-editor-zotero

I need to edit my Word document (article.docx):
1. Delete the 2nd paragraph
2. Move the 3rd paragraph to the beginning
3. Replace all "HSG" with "Tkk"
```

### As Python module

```python
from word_editor import WordEditor

# Create editor
editor = WordEditor("article.docx")

# Show summary
editor.print_summary()
# Output:
#   📄 Document: article.docx
#   Paragraphs: 456
#   Zotero citations: 36

# Delete paragraphs
orphaned = editor.delete_paragraphs([1, 5, 7])
print(f"Orphaned citations: {orphaned}")

# Move paragraph
editor.move_paragraph(3, 0)  # Move para 3 to position 0

# Replace text
count = editor.replace_text("HSG", "Tkk")
print(f"Replaced {count} occurrences")

# Save
editor.save("article_edited.docx", "article_log.json")
```

### As standalone script

```bash
python word_editor.py article.docx \
  --delete 2 5 7 \
  --move 3 0 \
  --replace HSG Tkk
```

## 📋 Operation Types

### 1. Delete Paragraphs

```python
# Single deletion
editor.delete_paragraphs([1])  # Delete 2nd paragraph (0-indexed)

# Multiple deletions
editor.delete_paragraphs([1, 5, 7])  # Delete 2nd, 6th, 8th paragraphs

# Returns: List of orphaned citation IDs
orphaned = editor.delete_paragraphs([2])
# Output: ['citation_id_1', 'citation_id_2']
```

### 2. Move Paragraphs

```python
# Move 3rd paragraph to 1st position
editor.move_paragraph(2, 0)

# Move paragraph to end (if 10 paragraphs total)
editor.move_paragraph(5, 9)
```

### 3. Replace Text

```python
# Single replacement
editor.replace_text("HSG", "Tkk")  # Returns: 37

# Multiple replacements
replacements = [
    ("HSG", "Tkk"),
    ("VR", "Virtual Reality"),
    ("IVF", "In-Vitro Fertilization")
]
editor.replace_multiple(replacements)
```

## 📊 Output Files

### Primary output
- `*_edited.docx` - Modified Word document with all changes applied

### Audit log
- `*_log.json` - Detailed modification record:

```json
{
  "execution_timestamp": "2026-05-10T18:20:35Z",
  "input_file": "article.docx",
  "analysis": {
    "total_paragraphs": 456,
    "total_citations": 36,
    "citations": [
      {
        "citationID": "smith2023",
        "paragraph_index": 14,
        "endnote_id": 1,
        "status": "preserved"
      }
    ]
  },
  "operations": {
    "deletions": [
      {
        "indices": [1],
        "orphaned_citations": []
      }
    ],
    "movements": [
      {
        "from": 2,
        "to": 0
      }
    ],
    "replacements": [
      {
        "old_text": "HSG",
        "new_text": "Tkk",
        "count": 37
      }
    ]
  },
  "validation": {
    "document_valid": true,
    "errors": [],
    "warnings": []
  }
}
```

## ⚠️ Important Notes

### Zotero Integration

After editing a document with this skill, you may need to **refresh Zotero fields** in Word:

1. Open the edited .docx in Microsoft Word
2. Go to **Zotero > Refresh** (or use keyboard shortcut)
3. This recalculates citation numbering

This is normal and not a bug - it's how Zotero handles external modifications.

### Orphaned Citations

If you delete a paragraph containing Zotero citations, those citations become "orphaned" and are automatically removed from the bibliography:

```python
orphaned = editor.delete_paragraphs([5])
# If paragraph 5 contained citations, they're in orphaned list
# Their endnotes are automatically removed
# Bibliography is recalculated
```

### Document Validation

The skill automatically validates the document before saving:

```python
if editor.validate():
    editor.save("output.docx")
else:
    print("Validation failed - document may be corrupted")
    # Check the log for details
```

## 🔧 Advanced Usage

### Context Manager

```python
with WordEditor("article.docx") as editor:
    editor.delete_paragraphs([2])
    editor.replace_text("old", "new")
    editor.save("output.docx")
# Automatically cleans up temporary files
```

### Batch Operations

```python
operations = [
    {"type": "delete", "indices": [2, 5]},
    {"type": "move", "from": 3, "to": 1},
    {"type": "replace", "old": "HSG", "new": "Tkk"},
    {"type": "replace", "old": "IVF", "new": "In-Vitro Fertilization"}
]

from word_editor import edit_document
edit_document("input.docx", "output.docx", operations)
```

### Get Document Info

```python
summary = editor.get_summary()
print(summary)
# Output:
# {
#   'file': '/path/to/article.docx',
#   'paragraphs': 456,
#   'citations': 36,
#   'citations_list': ['smith2023', 'jones2021', ...]
# }
```

## 🐛 Troubleshooting

### "Parent not found" error

**Cause:** The paragraph is in a nested location (table, text box)  
**Solution:** This is handled automatically in most cases

### Citations appear as codes after editing

**Cause:** Zotero fields need refresh  
**Solution:** Open in Word and use Zotero > Refresh

### "Endnote IDs not sequential" warning

**Cause:** Document had non-sequential endnote numbering  
**Solution:** This is automatically corrected during save

### Document validation fails

**Cause:** Structural corruption detected  
**Solution:** Check the log JSON for details, review modifications

## 📚 API Reference

### WordEditor class

```python
class WordEditor:
    def __init__(self, docx_path: str)
    def get_summary() -> dict
    def print_summary() -> None
    def delete_paragraphs(indices: List[int]) -> List[str]
    def move_paragraph(from_index: int, to_index: int) -> None
    def replace_text(old_text: str, new_text: str) -> int
    def replace_multiple(replacements: List[Tuple[str, str]]) -> dict
    def validate() -> bool
    def save(output_path: str, log_path: str = None) -> bool
```

## 📄 License

Standalone skill based on ZoteroDocxPreserver  
Compatible with scientific-writer (K-Dense-AI)  
Python 3.10+ required

## 🤝 Contributing

This skill is designed to be:
- **Independent** of scientific-writer updates
- **Maintainable** - single-purpose tool
- **Extensible** - easy to add new operations
- **Non-invasive** - doesn't modify existing code

Feel free to fork/extend for your use case!

---

**Created for:** Editing academic papers while preserving Zotero citations  
**Tested with:** Articles with 36+ citations, complex tables, nested elements
