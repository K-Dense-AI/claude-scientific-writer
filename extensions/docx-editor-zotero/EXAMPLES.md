# docx-editor-zotero: Examples

## Example 1: Basic Editing (Article Revision)

**Scenario:** You want to remove an outdated introduction and reorganize your article.

### Using in Claude Code

```
/docx-editor-zotero

I need to edit my research article (radiography_article.docx):
- Delete the 2nd paragraph (outdated introduction)
- Move the 3rd paragraph to be first
- Replace all "HSG" (Hysterosalpingography) with "Tkk" (new terminology)
```

**Claude will:**
1. Analyze the document (456 paragraphs, 36 citations)
2. Delete paragraph 2
3. Move paragraph 3 to position 0
4. Replace 37 instances of "HSG" with "Tkk"
5. Save as `radiography_article_edited.docx`
6. Generate audit log

**Result:**
```
✅ radiography_article_edited.docx (455 paragraphs, 36/36 citations preserved)
✅ radiography_article_log.json
```

---

## Example 2: Bulk Text Replacement

**Scenario:** Journal requests terminology updates across multiple sections.

### Python code

```python
from word_editor import WordEditor

editor = WordEditor("manuscript.docx")
editor.print_summary()

# Multiple replacements
replacements = [
    ("HSG", "Tkk"),
    ("VR", "Virtual Reality"),
    ("IVF", "In-Vitro Fertilization"),
    ("ICSI", "Intracytoplasmic Sperm Injection")
]

results = editor.replace_multiple(replacements)
for replacement, count in results.items():
    print(f"{replacement}: {count} occurrences")

# Save with audit
editor.save("manuscript_updated.docx", "manuscript_audit.json")
```

**Output:**
```
📄 Document: manuscript.docx
   Paragraphs: 420
   Zotero citations: 28

HSG→Tkk: 37 occurrences
VR→Virtual Reality: 12 occurrences
IVF→In-Vitro Fertilization: 8 occurrences
ICSI→Intracytoplasmic Sperm Injection: 4 occurrences

✅ Saved: manuscript_updated.docx
✅ Log: manuscript_audit.json
```

---

## Example 3: Removing Methods Section

**Scenario:** Preparing a short abstract version without detailed methodology.

### Python code

```python
from word_editor import WordEditor

editor = WordEditor("full_article.docx")

# Identify which paragraphs contain "Method" section
# Let's say paragraphs 15-25 are the Methods section
orphaned = editor.delete_paragraphs(list(range(15, 26)))

if orphaned:
    print(f"Warning: Removed {len(orphaned)} citations from Methods")
    print(f"Affected citations: {', '.join(orphaned)}")

editor.save("article_abstract.docx")
```

**Result:**
```
Warning: Removed 7 citations from Methods
Affected citations: methodA2023, methodB2023, methodC2023, ...

✅ Saved: article_abstract.docx (with 7 fewer citations)
```

---

## Example 4: Restructuring Document

**Scenario:** Reorganize sections in order: Results → Discussion → Methods → References

### Python code

```python
from word_editor import WordEditor

editor = WordEditor("disorganized_paper.docx")

# Assuming original order: Methods (1-10), Results (11-20), Discussion (21-30)
# Target order: Results (11-20) → Discussion (21-30) → Methods (1-10)

# Move Results to first position
for i in range(11, 21):  # Move 10 paragraph group
    editor.move_paragraph(11, 0)  # Always move first of group to start

# Document structure now: Results → Discussion → Methods

editor.save("reorganized_paper.docx")
print("✅ Document restructured successfully")
```

---

## Example 5: Batch Processing with Audit Trail

**Scenario:** Process multiple files with the same modifications.

### Python code

```python
from word_editor import edit_document
from pathlib import Path

# List of files to process
files = [
    "article_1.docx",
    "article_2.docx",
    "article_3.docx"
]

# Define operations
operations = [
    {"type": "delete", "indices": [2, 5]},
    {"type": "replace", "old": "HSG", "new": "Tkk"}
]

# Process each file
for input_file in files:
    if Path(input_file).exists():
        output = input_file.replace(".docx", "_edited.docx")
        success = edit_document(input_file, output, operations)
        
        if success:
            print(f"✅ {input_file} → {output}")
        else:
            print(f"❌ Failed: {input_file}")
```

---

## Example 6: Command Line Usage

**Scenario:** Use from terminal or scripts.

```bash
# Simple edit
python word_editor.py article.docx --delete 2 --replace HSG Tkk

# Multiple operations
python word_editor.py article.docx \
  --delete 2 5 7 \
  --move 3 0 \
  --replace HSG Tkk

# Output files
# - article_edited.docx
# - article_edited_log.json
```

---

## Example 7: With Context Manager

**Scenario:** Automatic cleanup of temporary files.

```python
from word_editor import WordEditor

with WordEditor("paper.docx") as editor:
    editor.delete_paragraphs([2])
    editor.replace_text("old_term", "new_term")
    editor.save("paper_revised.docx")
    # Temporary files cleaned up automatically

print("✅ Done")
```

---

## Example 8: Validation and Error Handling

**Scenario:** Robust editing with error checking.

```python
from word_editor import WordEditor

try:
    editor = WordEditor("important_document.docx")
    
    # Show what will be deleted
    summary = editor.get_summary()
    print(f"Document has {summary['citations']} citations")
    
    # Careful deletion
    orphaned = editor.delete_paragraphs([2])
    if orphaned:
        print(f"⚠️ WARNING: {len(orphaned)} citations will be removed")
        response = input("Continue? (yes/no): ")
        if response != "yes":
            print("Aborted")
            exit()
    
    # More operations...
    editor.replace_text("HSG", "Tkk")
    
    # Validate before saving
    if editor.validate():
        editor.save("important_document_revised.docx")
        print("✅ Successfully saved")
    else:
        print("❌ Validation failed - not saved")
        
except Exception as e:
    print(f"❌ Error: {e}")
```

---

## Example 9: Extracting Citation Information

**Scenario:** Get all citations from a document.

```python
from word_editor import WordEditor

editor = WordEditor("bibliography_heavy_article.docx")
summary = editor.get_summary()

print("All citations in document:")
for i, citation_id in enumerate(summary['citations_list'], 1):
    print(f"{i}. {citation_id}")

print(f"\nTotal: {len(summary['citations_list'])} citations")
```

---

## Example 10: Iterative Editing

**Scenario:** Edit document step-by-step, checking results at each step.

```python
from word_editor import WordEditor

editor = WordEditor("article.docx")

# Step 1: Preview
editor.print_summary()

# Step 2: First batch of deletions
print("\nDeleting outdated sections...")
orphaned1 = editor.delete_paragraphs([2, 5])

# Step 3: Reorganize
print("Reorganizing...")
editor.move_paragraph(3, 0)

# Step 4: Terminology update
print("Updating terminology...")
count = editor.replace_text("HSG", "Tkk")

# Step 5: Validate and save
print("\nFinal validation...")
if editor.validate():
    editor.save("article_v2.docx", "article_v2_log.json")
    print("✅ All done!")
else:
    print("❌ Issues detected - check log")
```

---

## Tips & Tricks

### Tip 1: Always check summary first
```python
editor = WordEditor("document.docx")
editor.print_summary()  # See what you're working with
```

### Tip 2: Understand orphaned citations
```python
orphaned = editor.delete_paragraphs([5])
if orphaned:
    print(f"These citations are now removed: {orphaned}")
    # Check if this was intentional!
```

### Tip 3: Test with copy first
```bash
cp important.docx important_BACKUP.docx
python word_editor.py important.docx --delete 2  # Test on backup first
```

### Tip 4: Review the audit log
```json
// article_edited_log.json
{
  "operations": {
    "deletions": [...],
    "movements": [...],
    "replacements": [...]
  },
  "validation": {
    "document_valid": true,
    "errors": [],
    "warnings": []
  }
}
```

### Tip 5: Multiple replacements together
```python
# More efficient than separate calls
replacements = [
    ("old1", "new1"),
    ("old2", "new2"),
    ("old3", "new3")
]
results = editor.replace_multiple(replacements)
```

---

## Common Issues

### Issue: "Parent not found"
**Solution:** Usually means paragraph is in a table - should be handled automatically

### Issue: Zotero shows field codes after editing
**Solution:** Open in Word and use Zotero > Refresh

### Issue: More citations than original
**Solution:** Shouldn't happen - report if it does!

### Issue: Document won't open after editing
**Solution:** Check the validation errors in the log, try recovering from backup
