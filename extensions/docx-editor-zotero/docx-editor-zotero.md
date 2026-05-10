# docx-editor-zotero

**Edit Word documents with full preservation of Zotero citations**

## Description

A powerful skill for editing Word (.docx) files while automatically preserving all Zotero citations. Perfect for:
- Removing paragraphs without losing citations
- Reorganizing document structure
- Replacing text content
- Validating document integrity

**Key feature:** All Zotero field codes, citations, and bibliography references are preserved throughout all modifications.

## Capabilities

- ✅ Delete paragraphs (with orphaned citation detection)
- ✅ Reorder/move paragraphs
- ✅ Replace text content (HSG → Tkk, etc.)
- ✅ Preserve Zotero citations 100%
- ✅ Automatic validation & audit logs
- ✅ Works with complex documents (tables, nested elements)

## Usage

### Basic workflow

```
1. User provides: input.docx + list of operations
2. Skill analyzes: citations, paragraphs, structure
3. Skill applies: modifications while tracking citations
4. Skill validates: document integrity
5. Skill outputs: edited.docx + audit log
```

### Example operations

```
INPUT: my_article.docx

OPERATIONS:
- Delete paragraphs: 2, 5, 7
- Move paragraph 3 to position 1
- Replace "HSG" with "Tkk"

OUTPUT:
✅ my_article_edited.docx (423 paragraphs, 34/36 citations preserved)
✅ my_article_log.json (audit trail)
```

## Implementation

When invoked, this skill:

1. Loads the input .docx file
2. Extracts all Zotero citations and their positions
3. Applies structural modifications (delete, reorder)
4. Applies text replacements
5. Recalculates endnote IDs and removes orphaned citations
6. Validates document integrity
7. Saves output with detailed audit log

## Integration

**Type:** Standalone skill (does not modify scientific-writer)  
**Dependencies:** Python 3.10+, stdlib only  
**Compatible with:** Claude Code, any .docx with Zotero citations  

## Output files

- `*_edited.docx` - Modified Word document
- `*_log.json` - Detailed modification log with:
  - Timestamps
  - Paragraphs deleted
  - Citations orphaned/preserved
  - Text replacements
  - Validation results

## Notes

- After editing, users may need to refresh Zotero fields in Word via Zotero menu
- Works with documents containing tables and complex layouts
- All modifications are reversible (original file untouched)

---

## For Claude to implement:

When user invokes this skill with a .docx file and operations, you should:

1. Import WordEditor class from word_editor.py
2. Parse the requested operations (delete, move, replace)
3. Execute in order: delete → reorder → replace
4. Save with validation
5. Report results and file locations
