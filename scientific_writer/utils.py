"""Utility functions for scientific writer."""

import logging
from pathlib import Path
import re
from typing import Any


logger = logging.getLogger(__name__)

PRIMARY_ARTIFACT_EXTENSIONS = {
    ".csv",
    ".docx",
    ".html",
    ".jpeg",
    ".jpg",
    ".md",
    ".pdf",
    ".png",
    ".pptx",
    ".svg",
    ".tex",
    ".webp",
    ".xlsx",
}
FIGURE_EXTENSIONS = {
    ".bmp",
    ".eps",
    ".gif",
    ".jpeg",
    ".jpg",
    ".pdf",
    ".png",
    ".svg",
    ".tif",
    ".tiff",
    ".webp",
}


def find_existing_papers(output_folder: Path) -> list[dict[str, Any]]:
    """
    Get all existing paper directories with their metadata.

    Args:
        output_folder: Path to the paper outputs folder.

    Returns:
        List of dicts with path, name, and timestamp info.
    """
    papers: list[dict[str, Any]] = []
    if not output_folder.exists():
        return papers

    for paper_dir in output_folder.iterdir():
        if paper_dir.is_dir():
            papers.append({
                'path': paper_dir,
                'name': paper_dir.name,
                'mtime': paper_dir.stat().st_mtime
            })

    # Sort by modification time (most recent first)
    papers.sort(key=lambda x: x['mtime'], reverse=True)
    return papers


def detect_paper_reference(
    user_input: str,
    existing_papers: list[dict[str, Any]],
) -> Path | None:
    """
    Try to detect if the user is referring to an existing paper.

    Args:
        user_input: User's input text.
        existing_papers: List of existing paper dictionaries.

    Returns:
        The paper path if found, None otherwise.
    """
    if not existing_papers:
        return None

    user_input_lower = user_input.lower()

    # Keywords that suggest continuing with existing work
    continuation_keywords = [
        "continue", "update", "edit", "revise", "modify", "change",
        "add to", "fix", "improve", "review", "the paper", "this paper",
        "my paper", "current paper", "previous paper", "last paper",
        "poster", "the poster", "my poster", "presentation", "the presentation",
        "my presentation", "previous presentation", "last presentation",
        "compile", "generate pdf"
    ]

    # Keywords that suggest searching for/looking up an existing paper
    search_keywords = [
        "look for", "find", "search for", "where is", "which paper",
        "show me", "open", "locate", "get"
    ]

    # Keywords that explicitly indicate a new paper
    new_paper_keywords = [
        "new paper", "start fresh", "start afresh", "create new",
        "different paper", "another paper", "write a new",
        "new presentation", "new poster", "different presentation", "another presentation"
    ]

    # If user explicitly wants a new paper, return None
    if any(keyword in user_input_lower for keyword in new_paper_keywords):
        return None

    # Check if user mentions continuation or search keywords
    has_continuation_keyword = any(keyword in user_input_lower for keyword in continuation_keywords)
    has_search_keyword = any(keyword in user_input_lower for keyword in search_keywords)

    # Try to find paper by name/topic keywords
    best_match = None
    best_match_score = 0

    for paper in existing_papers:
        paper_name = paper['name'].lower()
        # Extract topic from directory name (format: YYYYMMDD_HHMMSS_topic)
        parts = paper_name.split('_', 2)
        if len(parts) >= 3:
            topic = parts[2].replace('_', ' ')
            # Check if topic words appear in user input
            topic_words = topic.split()
            matches = sum(1 for word in topic_words if len(word) > 3 and word in user_input_lower)

            # Keep track of best match
            if matches > best_match_score:
                best_match_score = matches
                best_match = paper['path']

            # If we have a strong match (2+ topic words), return it
            # This is especially important for search keywords
            if matches >= 2 and (has_search_keyword or has_continuation_keyword):
                return paper['path']

    # If we found any match with search keywords, return the best one
    if has_search_keyword and best_match_score > 0:
        return best_match

    # If user used continuation keywords but no specific match, use most recent paper
    if has_continuation_keyword and existing_papers:
        return existing_papers[0]['path']

    return None


def scan_paper_directory(paper_dir: Path) -> dict[str, Any]:
    """
    Scan a paper directory and collect all file information.

    Args:
        paper_dir: Path to the paper directory.

    Returns:
        Dictionary with comprehensive file information.
    """
    result: dict[str, Any] = {
        'pdf_final': None,
        'tex_final': None,
        'pdf_drafts': [],
        'tex_drafts': [],
        'bibliography': None,
        'figures': [],
        'data': [],
        'sources': [],
        'final_artifacts': [],
        'draft_artifacts': [],
        'artifacts': [],
        'progress_log': None,
        'summary': None,
    }

    if not paper_dir.exists():
        return result

    # Scan final/ directory
    final_dir = paper_dir / "final"
    if final_dir.exists():
        final_files = sorted(file for file in final_dir.iterdir() if file.is_file())
        result['final_artifacts'] = [
            str(file)
            for file in final_files
            if file.suffix.lower() in PRIMARY_ARTIFACT_EXTENSIONS
        ]
        final_pdfs = [file for file in final_files if file.suffix.lower() == '.pdf']
        final_tex = [file for file in final_files if file.suffix.lower() == '.tex']
        if final_pdfs:
            preferred = next(
                (file for file in final_pdfs if file.name.lower() == "manuscript.pdf"),
                final_pdfs[0],
            )
            result['pdf_final'] = str(preferred)
        if final_tex:
            preferred = next(
                (file for file in final_tex if file.name.lower() == "manuscript.tex"),
                final_tex[0],
            )
            result['tex_final'] = str(preferred)

    # Scan drafts/ directory
    drafts_dir = paper_dir / "drafts"
    if drafts_dir.exists():
        for file in sorted(drafts_dir.iterdir()):
            if file.is_file():
                if file.suffix.lower() in PRIMARY_ARTIFACT_EXTENSIONS:
                    result['draft_artifacts'].append(str(file))
                if file.suffix.lower() == '.pdf':
                    result['pdf_drafts'].append(str(file))
                elif file.suffix.lower() == '.tex':
                    result['tex_drafts'].append(str(file))

    # Scan references/ directory
    references_dir = paper_dir / "references"
    if references_dir.exists():
        bib_file = references_dir / "references.bib"
        if bib_file.exists():
            result['bibliography'] = str(bib_file)

    # Scan figures/ directory
    figures_dir = paper_dir / "figures"
    if figures_dir.exists():
        for file in sorted(figures_dir.iterdir()):
            if file.is_file() and file.suffix.lower() in FIGURE_EXTENSIONS:
                result['figures'].append(str(file))

    # Scan data/ directory
    data_dir = paper_dir / "data"
    if data_dir.exists():
        for file in sorted(data_dir.iterdir()):
            if file.is_file():
                result['data'].append(str(file))

    # Scan sources/ directory
    sources_dir = paper_dir / "sources"
    if sources_dir.exists():
        for file in sorted(sources_dir.iterdir()):
            if file.is_file():
                result['sources'].append(str(file))

    # Check for progress.md and SUMMARY.md
    progress_file = paper_dir / "progress.md"
    if progress_file.exists():
        result['progress_log'] = str(progress_file)

    summary_file = paper_dir / "SUMMARY.md"
    if summary_file.exists():
        result['summary'] = str(summary_file)

    result['artifacts'] = [
        str(file)
        for file in sorted(paper_dir.rglob("*"))
        if file.is_file()
    ]

    return result


def count_citations_in_bib(bib_file: str | None) -> int:
    """
    Count the number of citations in a BibTeX file.

    Args:
        bib_file: Path to the .bib file.

    Returns:
        Number of citations found.
    """
    if not bib_file or not Path(bib_file).exists():
        return 0

    try:
        with open(bib_file, 'r', encoding='utf-8') as f:
            content = f.read()
            entry_types = re.findall(r'@([a-zA-Z]+)\s*[\{\(]', content)
            directives = {"comment", "preamble", "string"}
            return sum(1 for entry_type in entry_types if entry_type.lower() not in directives)
    except Exception:
        logger.warning("Could not count citations in %s", bib_file, exc_info=True)
        return 0


def extract_citation_style(bib_file: str | None, tex_file: str | None = None) -> str:
    """
    Try to extract the citation style used by the paper.

    Looks in the LaTeX source for \\bibliographystyle{...} or a biblatex
    style=... option, since the .bib file itself carries no style information.

    Args:
        bib_file: Path to the .bib file (currently unused, kept for API stability).
        tex_file: Optional path to the main .tex file to inspect.

    Returns:
        The declared style name (e.g. "ieeetr", "apa"), or "BibTeX" if unknown.
    """
    if tex_file and Path(tex_file).exists():
        try:
            content = Path(tex_file).read_text(encoding='utf-8')
            match = re.search(r'\\bibliographystyle\s*\{([^}]+)\}', content)
            if match:
                return match.group(1).strip()
            match = re.search(r'\\usepackage\s*\[([^\]]*)\]\s*\{biblatex\}', content)
            if match:
                for option in match.group(1).split(','):
                    key, _, value = option.partition('=')
                    if key.strip() == 'style' and value.strip():
                        return value.strip()
        except Exception:
            logger.warning("Could not inspect citation style in %s", tex_file, exc_info=True)
    return "BibTeX"


def count_words_in_tex(tex_file: str | None) -> int | None:
    """
    Estimate word count in a LaTeX file.

    Args:
        tex_file: Path to the .tex file.

    Returns:
        Estimated word count, or None if file doesn't exist.
    """
    if not tex_file or not Path(tex_file).exists():
        return None

    try:
        content = Path(tex_file).read_text(encoding='utf-8')
        document_match = re.search(
            r'\\begin\s*\{document\}(.*?)\\end\s*\{document\}',
            content,
            flags=re.DOTALL,
        )
        if document_match:
            content = document_match.group(1)

        content = re.sub(r'(?<!\\)%.*$', '', content, flags=re.MULTILINE)
        content = re.sub(
            r'\\begin\s*\{(?:equation\*?|align\*?|math|displaymath|verbatim)\}'
            r'.*?\\end\s*\{(?:equation\*?|align\*?|math|displaymath|verbatim)\}',
            ' ',
            content,
            flags=re.DOTALL,
        )
        content = re.sub(r'\$\$.*?\$\$|\$.*?\$|\\\[.*?\\\]', ' ', content, flags=re.DOTALL)

        non_text_commands = (
            "addbibresource",
            "bibliography",
            "bibliographystyle",
            "cite",
            "citep",
            "citet",
            "includegraphics",
            "label",
            "pageref",
            "ref",
            "url",
        )
        for command in non_text_commands:
            content = re.sub(
                rf'\\{command}\*?(?:\[[^\]]*\])?\{{(?:[^{{}}]|\{{[^{{}}]*\}})*\}}',
                ' ',
                content,
            )

        # Remove command names and optional arguments while retaining ordinary
        # braced text, e.g. ``\textbf{important result}``.
        content = re.sub(r'\\[a-zA-Z@]+\*?(?:\[[^\]]*\])?', ' ', content)
        content = re.sub(r'[{}&_^~#\\]', ' ', content)
        words = re.findall(r"\b[\w]+(?:[-'][\w]+)*\b", content, flags=re.UNICODE)
        return len(words)
    except Exception:
        logger.warning("Could not count words in %s", tex_file, exc_info=True)
        return None


def _extract_braced_group(content: str, opening_brace: int) -> str | None:
    """Extract a balanced braced group starting at ``opening_brace``."""
    if opening_brace >= len(content) or content[opening_brace] != "{":
        return None
    depth = 0
    escaped = False
    for index in range(opening_brace, len(content)):
        char = content[index]
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return content[opening_brace + 1:index]
    return None


def extract_title_from_tex(tex_file: str | None) -> str | None:
    """
    Extract title from a LaTeX file.

    Args:
        tex_file: Path to the .tex file.

    Returns:
        Title string, or None if not found.
    """
    if not tex_file or not Path(tex_file).exists():
        return None

    try:
        content = Path(tex_file).read_text(encoding='utf-8')
        match = re.search(r'\\title\s*\{', content)
        if match:
            title = _extract_braced_group(content, match.end() - 1)
            if title is not None:
                title = re.sub(r'\\[a-zA-Z@]+\*?(?:\[[^\]]*\])?', '', title)
                title = re.sub(r'[{}]', '', title)
                return " ".join(title.split())
    except Exception:
        logger.warning("Could not extract title from %s", tex_file, exc_info=True)

    return None

