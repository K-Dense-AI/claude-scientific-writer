#!/usr/bin/env python3
"""
ZoteroDocxPreserver: Outil autonome de préservation des citations Zotero dans Word
Gère la suppression/réordering de paragraphes tout en préservant intégralement les citations.

Utilisation:
    from zotero_docx_preserver import ZoteroDocxPreserver
    
    preserver = ZoteroDocxPreserver("input.docx")
    analysis = preserver.analyze()
    print(f"Found {analysis['total_citations']} citations")
    
    # Marquer paragraphes pour suppression
    orphaned = preserver.mark_paragraphs_for_deletion([2, 5, 7])
    print(f"Orphaned citations: {orphaned}")
    
    # Supprimer et nettoyer
    preserver.delete_paragraphs([2, 5, 7])
    cleaning_result = preserver.clean_orphaned_citations()
    
    # Valider et sauvegarder
    if preserver.validate():
        preserver.save("output.docx")
"""

import json
import logging
import re
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from xml.etree import ElementTree as ET

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s'
)
logger = logging.getLogger(__name__)

# Namespaces XML
NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}

# Enregistrer namespaces pour éviter ns0, ns1, etc.
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


class FieldData:
    """Représente une citation Zotero extraite"""
    def __init__(self, citation_id: str, para_index: int, json_payload: dict, 
                 display_text: str, endnote_id: Optional[int] = None):
        self.citation_id = citation_id
        self.para_index = para_index
        self.json_payload = json_payload
        self.display_text = display_text
        self.endnote_id = endnote_id
        self.status = "preserved"
    
    def to_dict(self) -> dict:
        return {
            "citationID": self.citation_id,
            "paragraph_index": self.para_index,
            "endnote_id": self.endnote_id,
            "display_text": self.display_text,
            "status": self.status
        }


class ZoteroDocxPreserver:
    """Préservateur de citations Zotero dans documents Word"""
    
    def __init__(self, docx_path: str):
        self.docx_path = Path(docx_path)
        if not self.docx_path.exists():
            raise FileNotFoundError(f"Document not found: {docx_path}")
        
        self.temp_dir = None
        self.citations_map: Dict[str, FieldData] = {}
        self.orphaned_citations: List[str] = []
        self.paragraphs_to_delete: List[int] = []
        self.doc_tree = None
        self.doc_root = None
        self.endnotes_tree = None
        self.endnotes_root = None
        self.document_xml_path = None
        self.endnotes_xml_path = None
        self.log_data = {
            "execution_timestamp": datetime.now().isoformat() + "Z",
            "input_file": str(self.docx_path),
            "analysis": {},
            "operations": {},
            "validation": {"errors": [], "warnings": []}
        }
    
    def _extract_docx(self):
        """Décompresser le DOCX en répertoire temporaire"""
        self.temp_dir = tempfile.TemporaryDirectory()
        with zipfile.ZipFile(self.docx_path, 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir.name)
        
        self.document_xml_path = Path(self.temp_dir.name) / "word" / "document.xml"
        self.endnotes_xml_path = Path(self.temp_dir.name) / "word" / "endnotes.xml"
        
        if not self.document_xml_path.exists():
            raise FileNotFoundError("word/document.xml not found in DOCX")
        
        logger.info(f"Extracted DOCX to {self.temp_dir.name}")
    
    def _load_xml_trees(self):
        """Charger les arbres XML document et endnotes"""
        self.doc_tree = ET.parse(self.document_xml_path)
        self.doc_root = self.doc_tree.getroot()
        
        if self.endnotes_xml_path.exists():
            self.endnotes_tree = ET.parse(self.endnotes_xml_path)
            self.endnotes_root = self.endnotes_tree.getroot()
        else:
            logger.warning("endnotes.xml not found, no bibliography to clean")
            self.endnotes_root = None
    
    def analyze(self) -> Dict:
        """Phase 1: Analyser et extraire toutes les citations Zotero"""
        logger.info("=== Phase 1: Analysis ===")
        self._extract_docx()
        self._load_xml_trees()
        
        self.citations_map = self._extract_zotero_fields()
        
        # Extraire aussi les endnote IDs
        self._map_endnote_ids()
        
        result = {
            "total_paragraphs": len(self.doc_root.findall('.//w:p', NS)),
            "total_citations": len(self.citations_map),
            "citations": [field.to_dict() for field in self.citations_map.values()]
        }
        
        self.log_data["analysis"] = result
        logger.info(f"Found {result['total_citations']} citations in {result['total_paragraphs']} paragraphs")
        
        return result
    
    def _extract_zotero_fields(self) -> Dict[str, FieldData]:
        """Extraire tous les fields Zotero du document"""
        citations = {}
        paragraphs = self.doc_root.findall('.//w:p', NS)
        
        for para_idx, para in enumerate(paragraphs):
            runs = para.findall('.//w:r', NS)
            i = 0
            while i < len(runs):
                run = runs[i]
                fld_char = run.find('.//w:fldChar', NS)
                
                # Détecter début de field
                if fld_char is not None and fld_char.get(f'{{{NS["w"]}}}fldCharType') == 'begin':
                    # Chercher instrText dans les runs suivants
                    instr_text = None
                    instr_run_idx = None
                    for j in range(i + 1, len(runs)):
                        instr = runs[j].find('.//w:instrText', NS)
                        if instr is not None:
                            instr_text = instr.text
                            instr_run_idx = j
                            break
                    
                    if instr_text and "ADDIN ZOTERO_ITEM" in instr_text:
                        # Extraire JSON
                        try:
                            json_start = instr_text.find('{')
                            json_end = instr_text.rfind('}') + 1
                            if json_start >= 0 and json_end > json_start:
                                json_str = instr_text[json_start:json_end]
                                json_payload = json.loads(json_str)
                                citation_id = json_payload.get('citationID', f'unknown_{para_idx}')
                                
                                # Extraire display text (après separate)
                                display_text = self._extract_field_display_text(runs, instr_run_idx)
                                
                                citations[citation_id] = FieldData(
                                    citation_id=citation_id,
                                    para_index=para_idx,
                                    json_payload=json_payload,
                                    display_text=display_text
                                )
                                logger.debug(f"Found citation {citation_id} at para {para_idx}")
                        except json.JSONDecodeError as e:
                            logger.warning(f"Failed to parse ZOTERO_ITEM JSON at para {para_idx}: {e}")
                    
                    i = instr_run_idx if instr_run_idx else i
                
                i += 1
        
        return citations
    
    def _extract_field_display_text(self, runs: List, instr_run_idx: int) -> str:
        """Extraire le texte affiché d'un field (entre separate et end)"""
        display_text = ""
        for j in range(instr_run_idx + 1, len(runs)):
            fld_char = runs[j].find('.//w:fldChar', NS)
            if fld_char is not None:
                fld_type = fld_char.get(f'{{{NS["w"]}}}fldCharType')
                if fld_type == 'end':
                    break
                elif fld_type == 'separate':
                    # Commencer à collecter le texte
                    for k in range(j + 1, len(runs)):
                        fld_end = runs[k].find('.//w:fldChar', NS)
                        if fld_end is not None and fld_end.get(f'{{{NS["w"]}}}fldCharType') == 'end':
                            break
                        t = runs[k].find('.//w:t', NS)
                        if t is not None and t.text:
                            display_text += t.text
                    break
        
        return display_text.strip()
    
    def _map_endnote_ids(self):
        """Mapper citation_id → endnote_id en parcourant document.xml"""
        if self.endnotes_root is None:
            return
        
        # Chercher tous les endnoteReference dans le document
        for ref in self.doc_root.findall('.//w:endnoteReference', NS):
            ref_id = ref.get(f'{{{NS["w"]}}}id')
            if ref_id:
                # Chercher quel citationID précède cette référence
                # (heuristique: chercher le field le plus proche avant)
                endnote_id = int(ref_id)
                for citation_id, field_data in self.citations_map.items():
                    if field_data.endnote_id is None:
                        # Assigner en ordre d'apparition
                        field_data.endnote_id = endnote_id
    
    def mark_paragraphs_for_deletion(self, para_indices: List[int]) -> List[str]:
        """Phase 2a: Marquer les paragraphes pour suppression et identifier citations orphelines"""
        logger.info(f"Marking {len(para_indices)} paragraphs for deletion")
        self.paragraphs_to_delete = sorted(set(para_indices))
        
        orphaned = []
        for citation_id, field_data in self.citations_map.items():
            if field_data.para_index in self.paragraphs_to_delete:
                orphaned.append(citation_id)
                field_data.status = "orphaned"
        
        self.orphaned_citations = orphaned
        logger.info(f"Identified {len(orphaned)} orphaned citations: {orphaned}")
        
        return orphaned
    
    def delete_paragraphs(self, para_indices: List[int]):
        """Phase 2b: Supprimer les paragraphes du document XML"""
        logger.info(f"Deleting {len(para_indices)} paragraphs from XML")
        
        # Marquer les paragraphes pour suppression
        paragraphs = self.doc_root.findall('.//w:p', NS)
        
        # Supprimer en ordre inverse pour ne pas décaler les indices
        for idx in sorted(set(para_indices), reverse=True):
            if 0 <= idx < len(paragraphs):
                para = paragraphs[idx]
                parent = self.doc_root.find('.//', NS)  # Trouver le parent
                for elem in self.doc_root.iter():
                    if para in list(elem):
                        elem.remove(para)
                        logger.debug(f"Deleted paragraph {idx}")
                        break
    
    def reorder_paragraphs(self, para_index_map: Dict[int, int]):
        """Phase 2c: Réordonner les paragraphes (optionnel)
        
        Args:
            para_index_map: Dict {old_index -> new_index}
        """
        logger.info(f"Reordering {len(para_index_map)} paragraphs")
        
        # Récupérer le parent (w:body)
        body = self.doc_root.find('.//w:body', NS)
        if body is None:
            logger.error("Could not find w:body element")
            return
        
        # Récupérer tous les paragraphes
        paragraphs = list(body.findall('.//w:p', NS))
        
        # Créer une copie réordonnée
        new_order = [None] * len(paragraphs)
        for old_idx, new_idx in para_index_map.items():
            if 0 <= old_idx < len(paragraphs) and 0 <= new_idx < len(paragraphs):
                new_order[new_idx] = paragraphs[old_idx]
        
        # Remplir les trous avec les paragraphes non mappés
        remaining = [p for i, p in enumerate(paragraphs) if i not in para_index_map.keys()]
        remaining_idx = 0
        for i in range(len(new_order)):
            if new_order[i] is None and remaining_idx < len(remaining):
                new_order[i] = remaining[remaining_idx]
                remaining_idx += 1
        
        # Réappliquer l'ordre
        for para in paragraphs:
            body.remove(para)
        for para in new_order:
            if para is not None:
                body.append(para)
        
        logger.info(f"Reordered paragraphs")
    
    def clean_orphaned_citations(self) -> Dict:
        """Phase 3: Nettoyer les endnotes orphelines et recalculer les IDs"""
        logger.info("=== Phase 3: Cleaning ===")
        
        if self.endnotes_root is None:
            logger.warning("No endnotes to clean")
            return {"removed_endnotes": 0, "new_id_mapping": {}}
        
        # Trouver les endnote IDs à supprimer
        endnote_ids_to_remove = []
        for citation_id in self.orphaned_citations:
            if citation_id in self.citations_map:
                endnote_id = self.citations_map[citation_id].endnote_id
                if endnote_id is not None:
                    endnote_ids_to_remove.append(endnote_id)
        
        logger.info(f"Removing {len(endnote_ids_to_remove)} orphaned endnotes")
        
        # Supprimer les endnotes
        for endnote_id in endnote_ids_to_remove:
            endnote = self.endnotes_root.find(f".//w:endnote[@w:id='{endnote_id}']", NS)
            if endnote is not None:
                self.endnotes_root.remove(endnote)
                logger.debug(f"Removed endnote {endnote_id}")
        
        # Recalculer les IDs séquentiels
        id_mapping = self._recalculate_endnote_ids()
        
        result = {
            "removed_endnotes": len(endnote_ids_to_remove),
            "new_id_mapping": id_mapping
        }
        
        self.log_data["operations"] = {
            "paragraphs_deleted": self.paragraphs_to_delete,
            "orphaned_citations": self.orphaned_citations,
            "orphaned_endnotes_removed": len(endnote_ids_to_remove),
            "id_remapping": id_mapping
        }
        
        return result
    
    def _recalculate_endnote_ids(self) -> Dict[str, int]:
        """Recalculer les IDs séquentiels dans endnotes.xml et corriger les références dans document.xml"""
        id_mapping = {}
        
        # Obtenir tous les endnotes restants
        endnotes = self.endnotes_root.findall('.//w:endnote', NS)
        
        # Réassigner les IDs
        for new_id, endnote in enumerate(endnotes, 1):
            old_id = endnote.get(f'{{{NS["w"]}}}id')
            if old_id:
                old_id_int = int(old_id)
                endnote.set(f'{{{NS["w"]}}}id', str(new_id))
                id_mapping[old_id] = new_id
                logger.debug(f"Remapped endnote {old_id_int} → {new_id}")
        
        # Corriger les références dans document.xml
        for ref in self.doc_root.findall('.//w:endnoteReference', NS):
            ref_id = ref.get(f'{{{NS["w"]}}}id')
            if ref_id and ref_id in id_mapping:
                ref.set(f'{{{NS["w"]}}}id', str(id_mapping[ref_id]))
        
        return id_mapping
    
    def validate(self) -> bool:
        """Valider l'intégrité du document"""
        logger.info("=== Validation ===")
        
        errors = []
        warnings = []
        
        # Vérifier qu'aucune citation orpheline n'existe
        remaining_citations = self._extract_zotero_fields()
        for citation_id in self.orphaned_citations:
            if citation_id in remaining_citations:
                errors.append(f"Citation {citation_id} still exists after deletion")
        
        # Vérifier synchronisation endnotes
        if self.endnotes_root is not None:
            endnotes = self.endnotes_root.findall('.//w:endnote', NS)
            endnote_ids = set(int(e.get(f'{{{NS["w"]}}}id')) for e in endnotes)
            
            # Vérifier séquence
            if endnote_ids and endnote_ids != set(range(1, max(endnote_ids) + 1)):
                warnings.append(f"Endnote IDs not sequential: {sorted(endnote_ids)}")
            
            # Vérifier les références
            refs = self.doc_root.findall('.//w:endnoteReference', NS)
            ref_ids = set(int(r.get(f'{{{NS["w"]}}}id')) for r in refs if r.get(f'{{{NS["w"]}}}id}'))
            
            if ref_ids and not ref_ids.issubset(endnote_ids):
                errors.append(f"Dangling references: {ref_ids - endnote_ids}")
        
        self.log_data["validation"]["errors"] = errors
        self.log_data["validation"]["warnings"] = warnings
        self.log_data["validation"]["document_valid"] = len(errors) == 0
        
        if errors:
            logger.error(f"Validation failed: {errors}")
            return False
        
        if warnings:
            for w in warnings:
                logger.warning(w)
        
        logger.info("✓ Document validation passed")
        return True
    
    def save(self, output_path: str, log_path: Optional[str] = None):
        """Repack et sauvegarder le document"""
        logger.info(f"=== Saving to {output_path} ===")
        
        output_path = Path(output_path)
        
        # Sauvegarder les XML modifiés
        self.doc_tree.write(
            str(self.document_xml_path),
            encoding='utf-8',
            xml_declaration=True
        )
        
        if self.endnotes_tree is not None:
            self.endnotes_tree.write(
                str(self.endnotes_xml_path),
                encoding='utf-8',
                xml_declaration=True
            )
        
        # Repack DOCX
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in Path(self.temp_dir.name).rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(self.temp_dir.name)
                    zipf.write(file_path, arcname)
        
        logger.info(f"✓ Saved to {output_path}")
        
        # Sauvegarder le log
        if log_path:
            log_path = Path(log_path)
            with open(log_path, 'w') as f:
                json.dump(self.log_data, f, indent=2)
            logger.info(f"✓ Log saved to {log_path}")
        
        # Nettoyer
        if self.temp_dir:
            self.temp_dir.cleanup()
    
    def get_log(self) -> Dict:
        """Obtenir le log en tant que dictionnaire"""
        return self.log_data


def main():
    """Exemple d'utilisation"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python zotero_docx_preserver.py <input.docx> [output.docx]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output.docx"
    log_file = output_file.replace(".docx", "_log.json")
    
    try:
        preserver = ZoteroDocxPreserver(input_file)
        
        # Analyser
        analysis = preserver.analyze()
        print(f"\n📊 Analysis: {analysis['total_citations']} citations found")
        
        # Exemple: supprimer les paragraphes 2 et 5
        orphaned = preserver.mark_paragraphs_for_deletion([2, 5])
        print(f"🗑️  Marked for deletion: paragraphs [2, 5]")
        if orphaned:
            print(f"⚠️  Orphaned citations: {orphaned}")
        
        # Appliquer suppressions
        preserver.delete_paragraphs([2, 5])
        
        # Nettoyer
        clean_result = preserver.clean_orphaned_citations()
        print(f"✨ Cleaned: {clean_result['removed_endnotes']} endnotes removed")
        
        # Valider
        if preserver.validate():
            preserver.save(output_file, log_file)
            print(f"✅ Success! Output: {output_file}")
        else:
            print("❌ Validation failed")
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
