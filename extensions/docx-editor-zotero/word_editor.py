#!/usr/bin/env python3
"""
WordEditor: High-level API for editing Word documents with Zotero preservation

Usage:
    editor = WordEditor("input.docx")
    editor.delete_paragraphs([1, 3, 5])
    editor.move_paragraph(2, 0)
    editor.replace_text("HSG", "Tkk")
    editor.save("output.docx")
"""

import json
import logging
from pathlib import Path
from xml.etree import ElementTree as ET

from zotero_docx_preserver import ZoteroDocxPreserver, NS

logger = logging.getLogger(__name__)


class WordEditor:
    """High-level interface for editing Word documents with Zotero preservation"""

    def __init__(self, docx_path):
        """
        Initialize editor with a Word document

        Args:
            docx_path: Path to .docx file
        """
        self.docx_path = Path(docx_path)
        if not self.docx_path.exists():
            raise FileNotFoundError(f"Document not found: {docx_path}")

        self.preserver = ZoteroDocxPreserver(str(self.docx_path))
        self.analysis = self.preserver.analyze()

        self.operations_log = {
            "deletions": [],
            "movements": [],
            "replacements": []
        }

    # ===========================
    # ANALYSIS & REPORTING
    # ===========================

    def get_summary(self):
        """Get document summary"""
        return {
            "file": str(self.docx_path),
            "paragraphs": self.analysis['total_paragraphs'],
            "citations": self.analysis['total_citations'],
            "citations_list": [c['citationID'] for c in self.analysis['citations']]
        }

    def print_summary(self):
        """Print human-readable summary"""
        summary = self.get_summary()
        print(f"\n📄 Document: {summary['file']}")
        print(f"   Paragraphs: {summary['paragraphs']}")
        print(f"   Zotero citations: {summary['citations']}")
        if summary['citations_list']:
            print(f"   Citations: {', '.join(summary['citations_list'][:5])}")
            if len(summary['citations_list']) > 5:
                print(f"             ... and {len(summary['citations_list']) - 5} more")

    # ===========================
    # PARAGRAPH OPERATIONS
    # ===========================

    def delete_paragraphs(self, indices):
        """
        Delete paragraphs by index

        Args:
            indices: List of paragraph indices to delete [1, 3, 5]

        Returns:
            List of orphaned citation IDs
        """
        if not indices:
            return []

        # Mark and delete
        orphaned = self.preserver.mark_paragraphs_for_deletion(indices)
        self.preserver.delete_paragraphs(indices)

        # Clean orphaned citations
        if orphaned:
            clean_result = self.preserver.clean_orphaned_citations()
            logger.info(f"Removed {clean_result['removed_endnotes']} orphaned endnotes")

        self.operations_log["deletions"].append({
            "indices": sorted(indices),
            "orphaned_citations": orphaned
        })

        return orphaned

    def move_paragraph(self, from_index, to_index):
        """
        Move paragraph from one position to another

        Args:
            from_index: Current paragraph index
            to_index: Target paragraph index
        """
        doc_root = self.preserver.doc_root
        paragraphs = doc_root.findall('.//w:p', NS)

        if not (0 <= from_index < len(paragraphs) and 0 <= to_index < len(paragraphs)):
            raise IndexError(f"Invalid indices: from={from_index}, to={to_index}, total={len(paragraphs)}")

        para_to_move = paragraphs[from_index]

        # Find parent and move
        self._move_element(doc_root, para_to_move, from_index, to_index)

        self.operations_log["movements"].append({
            "from": from_index,
            "to": to_index
        })

        logger.info(f"Moved paragraph {from_index} → {to_index}")

    def _move_element(self, root, element, from_idx, to_idx):
        """Move an element within the document tree"""
        # Find parent
        parent = None
        for p in root.iter():
            if element in list(p):
                parent = p
                break

        if parent is None:
            raise ValueError("Parent not found for element")

        parent.remove(element)

        # Find where to insert
        current_paras = root.findall('.//w:p', NS)
        if to_idx < len(current_paras):
            target_para = current_paras[to_idx]
            target_parent = None
            for p in root.iter():
                if target_para in list(p):
                    target_parent = p
                    break

            if target_parent is parent:
                parent.insert(to_idx, element)
            else:
                # Insert at beginning of target parent
                target_parent.insert(0, element)
        else:
            # Append to parent
            parent.append(element)

    # ===========================
    # TEXT OPERATIONS
    # ===========================

    def replace_text(self, old_text, new_text):
        """
        Replace all occurrences of text in document

        Args:
            old_text: Text to find
            new_text: Text to replace with

        Returns:
            Number of replacements made
        """
        doc_root = self.preserver.doc_root
        count = 0

        for t_elem in doc_root.findall('.//w:t', NS):
            if t_elem.text and old_text in t_elem.text:
                t_elem.text = t_elem.text.replace(old_text, new_text)
                count += 1

        self.operations_log["replacements"].append({
            "old_text": old_text,
            "new_text": new_text,
            "count": count
        })

        logger.info(f"Replaced '{old_text}' with '{new_text}' ({count} times)")
        return count

    def replace_multiple(self, replacements):
        """
        Replace multiple text patterns

        Args:
            replacements: List of (old, new) tuples

        Returns:
            Dict with counts per replacement
        """
        results = {}
        for old_text, new_text in replacements:
            count = self.replace_text(old_text, new_text)
            results[f"{old_text}→{new_text}"] = count
        return results

    # ===========================
    # VALIDATION & SAVING
    # ===========================

    def validate(self):
        """Validate document integrity"""
        return self.preserver.validate()

    def save(self, output_path, log_path=None):
        """
        Validate and save the edited document

        Args:
            output_path: Path for output .docx
            log_path: Optional path for audit log JSON

        Returns:
            True if successful

        Raises:
            ValueError if validation fails
        """
        if not self.validate():
            raise ValueError("Document validation failed - cannot save")

        output_path = Path(output_path)
        self.preserver.save(str(output_path), log_path)

        # Add our operations log to the preserver log
        preserver_log = self.preserver.get_log()
        preserver_log["operations"] = self.operations_log

        # Save combined log
        if log_path is None:
            log_path = str(output_path).replace(".docx", "_log.json")

        with open(log_path, 'w') as f:
            json.dump(preserver_log, f, indent=2)

        logger.info(f"Saved: {output_path}")
        logger.info(f"Log: {log_path}")

        return True

    # ===========================
    # CONTEXT MANAGERS
    # ===========================

    def __enter__(self):
        """Context manager support"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup"""
        if self.preserver.temp_dir:
            self.preserver.temp_dir.cleanup()


# ===========================
# CONVENIENCE FUNCTIONS
# ===========================

def edit_document(input_docx, output_docx, operations):
    """
    Convenience function to edit a document with a list of operations

    Args:
        input_docx: Input .docx path
        output_docx: Output .docx path
        operations: List of operation dicts:
            - type: "delete" | "move" | "replace"
            - indices: [1, 2, 3] (for delete)
            - from: int, to: int (for move)
            - old: str, new: str (for replace)

    Returns:
        Success boolean

    Example:
        operations = [
            {"type": "delete", "indices": [2, 5]},
            {"type": "move", "from": 3, "to": 1},
            {"type": "replace", "old": "HSG", "new": "Tkk"}
        ]
        edit_document("input.docx", "output.docx", operations)
    """
    editor = WordEditor(input_docx)

    try:
        for op in operations:
            op_type = op.get("type")

            if op_type == "delete":
                orphaned = editor.delete_paragraphs(op.get("indices", []))
                print(f"  Deleted {len(op.get('indices', []))} paragraphs")
                if orphaned:
                    print(f"  Orphaned citations: {orphaned}")

            elif op_type == "move":
                editor.move_paragraph(op.get("from"), op.get("to"))
                print(f"  Moved paragraph {op.get('from')} → {op.get('to')}")

            elif op_type == "replace":
                count = editor.replace_text(op.get("old"), op.get("new"))
                print(f"  Replaced '{op.get('old')}' with '{op.get('new')}' ({count}x)")

        editor.save(output_docx)
        print(f"\n✅ Saved: {output_docx}")
        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python word_editor.py <input.docx> <operations>")
        print("\nExample:")
        print("  python word_editor.py article.docx --delete 2 5 --move 3 1 --replace HSG Tkk")
        sys.exit(1)

    input_file = sys.argv[1]

    # Parse operations from command line
    operations = []
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--delete":
            indices = []
            i += 1
            while i < len(sys.argv) and sys.argv[i][0] != "-":
                indices.append(int(sys.argv[i]))
                i += 1
            operations.append({"type": "delete", "indices": indices})
            continue
        elif arg == "--move":
            i += 1
            from_idx = int(sys.argv[i])
            i += 1
            to_idx = int(sys.argv[i])
            operations.append({"type": "move", "from": from_idx, "to": to_idx})
        elif arg == "--replace":
            i += 1
            old_text = sys.argv[i]
            i += 1
            new_text = sys.argv[i]
            operations.append({"type": "replace", "old": old_text, "new": new_text})
        i += 1

    output_file = input_file.replace(".docx", "_edited.docx")
    edit_document(input_file, output_file, operations)
