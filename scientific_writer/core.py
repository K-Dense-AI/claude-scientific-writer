"""Core utilities for scientific writer."""

from collections import defaultdict
from collections.abc import Mapping
from datetime import datetime
import logging
import os
import re
import shutil
import zipfile
from pathlib import Path
from typing import Any

from claude_agent_sdk.types import HookContext, StopHookInput

logger = logging.getLogger(__name__)

# Single source of truth for effort-level model selection (used by both API and CLI).
# Project policy: Claude Opus 4.8 is the top tier for both medium and high effort.
EFFORT_LEVEL_MODELS = {
    "low": "claude-haiku-4-5",
    "medium": "claude-opus-4-8",
    "high": "claude-opus-4-8",
}


def create_completion_check_stop_hook(
    auto_continue: bool = True,
    max_continuations: int = 1,
):
    """Create a bounded Stop hook that requests one final completion check."""
    continuation_count = 0

    async def completion_check_stop_hook(
        hook_input: StopHookInput,
        tool_use_id: str | None,
        context: HookContext,
    ) -> dict[str, Any]:
        del tool_use_id, context
        nonlocal continuation_count

        if (
            not auto_continue
            or max_continuations <= 0
            or continuation_count >= max_continuations
            or hook_input.get("stop_hook_active", False)
        ):
            return {}

        continuation_count += 1
        return {
            "decision": "block",
            "reason": (
                "Before stopping, verify that every requested deliverable and validation "
                "step is complete. Finish any missing work, then provide the final result. "
                "If everything is already complete, summarize it and stop."
            ),
        }

    return completion_check_stop_hook


def resolve_auto_continue(requested: bool, env: Mapping[str, str] | None = None) -> bool:
    """Resolve auto-continue, with an explicit environment override when present."""
    environment = os.environ if env is None else env
    value = environment.get("SCIENTIFIC_WRITER_AUTO_CONTINUE")
    if value is None:
        return requested
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes", "on"}:
        return True
    if normalized in {"false", "0", "no", "off"}:
        return False
    logger.warning(
        "Ignoring invalid SCIENTIFIC_WRITER_AUTO_CONTINUE value %r; using %s",
        value,
        requested,
    )
    return requested


def setup_claude_skills(package_dir: Path, work_dir: Path) -> None:
    """
    Set up skills, provenance lock, and WRITER.md from the packaged .claude directory.

    If work_dir already has a .claude directory, the bundled WRITER.md and each
    bundled skill are refreshed in place (so upgrades take effect), while any
    user-owned files there — settings, custom skills — are left untouched.
    Bundled skill directories are replaced wholesale on refresh, so local edits
    to them will be overwritten.

    Failures are logged (never raised or silently swallowed); output stays off
    stdout so API consumers only see ProgressUpdate messages.

    Args:
        package_dir: Package installation directory containing .claude/
        work_dir: User's working directory where .claude/ should be copied
    """
    source_claude = package_dir / ".claude"
    dest_claude = work_dir / ".claude"

    if not source_claude.exists():
        logger.warning(
            "Bundled .claude directory not found at %s; skills and WRITER.md unavailable",
            source_claude,
        )
        return

    try:
        if not dest_claude.exists():
            shutil.copytree(source_claude, dest_claude)
            return

        # .claude already exists: refresh bundled content, preserve user files.
        source_writer = source_claude / "WRITER.md"
        if source_writer.exists():
            shutil.copyfile(source_writer, dest_claude / "WRITER.md")

        source_lock = source_claude / "skills.lock.json"
        if source_lock.exists():
            shutil.copyfile(source_lock, dest_claude / "skills.lock.json")

        source_skills = source_claude / "skills"
        if source_skills.is_dir():
            dest_skills = dest_claude / "skills"
            dest_skills.mkdir(exist_ok=True)
            for entry in source_skills.iterdir():
                dest_entry = dest_skills / entry.name
                if entry.is_dir():
                    if dest_entry.exists():
                        shutil.rmtree(dest_entry)
                    shutil.copytree(entry, dest_entry)
                else:
                    shutil.copyfile(entry, dest_entry)
    except Exception:
        logger.warning(
            "Failed to set up bundled Claude skills in %s", dest_claude, exc_info=True
        )


def get_api_key(
    api_key: str | None = None,
    env: Mapping[str, str] | None = None,
) -> str:
    """
    Get the Anthropic API key.

    Args:
        api_key: Optional API key to use. If not provided, reads from environment.

    Returns:
        The API key.

    Raises:
        ValueError: If API key is not found.
    """
    if api_key:
        return api_key

    environment = os.environ if env is None else env
    env_key = environment.get("ANTHROPIC_API_KEY")
    if not env_key:
        raise ValueError(
            "ANTHROPIC_API_KEY not found. Either pass api_key parameter or set "
            "ANTHROPIC_API_KEY environment variable."
        )
    return env_key


def load_system_instructions(work_dir: Path) -> str:
    """
    Load system instructions from .claude/WRITER.md in the working directory.

    Args:
        work_dir: Working directory containing .claude/WRITER.md.

    Returns:
        System instructions string.
    """
    instructions_file = work_dir / ".claude" / "WRITER.md"

    if instructions_file.exists():
        return instructions_file.read_text(encoding="utf-8")

    logger.warning("System instructions not found at %s; using minimal fallback", instructions_file)
    return (
        "You are a scientific writing assistant. Follow best practices for "
        "scientific communication and always present a plan before execution."
    )


def ensure_output_folder(cwd: Path, custom_dir: str | None = None) -> Path:
    """
    Ensure the writing_outputs folder exists.

    Args:
        cwd: Current working directory (project root).
        custom_dir: Optional custom output directory path.

    Returns:
        Path to the output folder.
    """
    if custom_dir:
        configured = Path(custom_dir).expanduser()
        output_folder = (
            configured.resolve()
            if configured.is_absolute()
            else (cwd / configured).resolve()
        )
    else:
        output_folder = cwd / "writing_outputs"

    output_folder.mkdir(exist_ok=True, parents=True)
    return output_folder


def create_output_project(
    output_folder: Path,
    query: str,
    now: datetime | None = None,
) -> Path:
    """Atomically create one standard output project for an invocation."""
    local_now = (now or datetime.now().astimezone()).astimezone()
    timestamp = local_now.strftime("%Y%m%d_%H%M%S")
    words = re.findall(r"[a-z0-9]+", query.lower())
    slug = "_".join(words[:8])[:64].strip("_") or "document"
    base_name = f"{timestamp}_{slug}"

    for index in range(1, 10_000):
        suffix = "" if index == 1 else f"_{index}"
        candidate = output_folder / f"{base_name}{suffix}"
        try:
            candidate.mkdir(parents=False, exist_ok=False)
        except FileExistsError:
            continue
        for directory in ("drafts", "final", "references", "figures", "data", "sources"):
            (candidate / directory).mkdir()
        return candidate

    raise FileExistsError(f"Could not create a unique project in {output_folder}")


def get_image_extensions() -> set[str]:
    """Return a set of common image file extensions."""
    return {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif', '.svg', '.webp', '.ico'}


def get_manuscript_extensions() -> set[str]:
    """Return a set of manuscript file extensions that should go to drafts/ folder."""
    return {'.tex'}


def get_source_extensions() -> set[str]:
    """Return a set of source/context file extensions that should go to sources/ folder."""
    return {'.md', '.docx', '.pdf'}


def get_data_extensions() -> set[str]:
    """Return a set of data file extensions that should go to data/ folder."""
    return {'.csv', '.json', '.txt', '.xlsx', '.xls', '.tsv', '.xml', '.yaml', '.yml', '.sql'}


def get_data_files(cwd: Path, data_files: list[str] | None = None) -> list[Path]:
    """
    Get data files either from provided list or from data folder.

    Args:
        cwd: Current working directory (project root).
        data_files: Optional list of file paths. If not provided, reads from data/ folder.

    Returns:
        List of Path objects for data files.
    """
    if data_files:
        resolved: list[Path] = []
        for value in data_files:
            path = Path(value).expanduser()
            if not path.is_absolute():
                path = cwd / path
            path = path.resolve()
            if not path.is_file():
                raise FileNotFoundError(f"Input file not found: {path}")
            resolved.append(path)
        return resolved

    data_folder = cwd / "data"
    if not data_folder.exists():
        return []

    files: list[Path] = []
    for file_path in sorted(data_folder.iterdir()):
        if file_path.is_file():
            files.append(file_path)

    return files


def _unique_destination(destination: Path) -> Path:
    """Return a collision-free destination without overwriting existing data."""
    if not destination.exists():
        return destination
    for index in range(2, 10_000):
        candidate = destination.with_name(
            f"{destination.stem}_{index}{destination.suffix}"
        )
        if not candidate.exists():
            return candidate
    raise FileExistsError(f"Could not find a free destination for {destination}")


def extract_images_from_docx(
    docx_path: Path,
    figures_output: Path,
) -> list[dict[str, Any]]:
    """
    Extract all images from a .docx file and copy them to the figures folder.

    A .docx file is a ZIP archive containing images in the word/media/ directory.
    This function extracts all image files and copies them to the specified output directory.

    Args:
        docx_path: Path to the .docx file.
        figures_output: Path to the figures output directory.

    Returns:
        List of dictionaries containing information about extracted images.
        Each dict has 'name', 'path', and 'source_docx' keys.
    """
    extracted_images: list[dict[str, Any]] = []
    image_extensions = get_image_extensions()

    try:
        with zipfile.ZipFile(docx_path, 'r') as zip_ref:
            # List all files in the archive
            all_files = zip_ref.namelist()

            # Filter for files in word/media/ directory that are images
            media_files = [f for f in all_files if f.startswith('word/media/')]

            for media_file in media_files:
                # Get the filename from the path
                file_name = Path(media_file).name
                file_ext = Path(media_file).suffix.lower()

                # Only extract if it's an image file
                if file_ext in image_extensions:
                    # Extract to figures folder
                    output_path = _unique_destination(figures_output / file_name)

                    # Read the file from the zip and write it to the output
                    with zip_ref.open(media_file) as source:
                        with open(output_path, 'wb') as target:
                            target.write(source.read())

                    extracted_images.append({
                        'name': output_path.name,
                        'path': str(output_path),
                        'source_docx': docx_path.name
                    })

    except zipfile.BadZipFile:
        logger.warning("%s is not a valid .docx file (ZIP archive)", docx_path.name)
    except Exception:
        logger.warning("Could not extract images from %s", docx_path.name, exc_info=True)

    return extracted_images


def process_data_files(
    cwd: Path,
    data_files: list[Path],
    paper_output_path: str,
    delete_originals: bool = False,
) -> dict[str, Any] | None:
    """
    Process data files by copying them to the paper output folder.
    Manuscript files (.tex) go to drafts/,
    Source files (.md, .docx, .pdf) go to sources/,
    images go to figures/,
    data files (csv, json, etc.) go to data/,
    everything else goes to sources/.

    Args:
        cwd: Current working directory (project root).
        data_files: List of file paths to process.
        paper_output_path: Path to the paper output directory.
        delete_originals: Whether to delete original files after copying.

    Returns:
        Dictionary with information about processed files, or None if no files.
    """
    if not data_files:
        return None

    paper_output = Path(paper_output_path)
    data_output = paper_output / "data"
    figures_output = paper_output / "figures"
    drafts_output = paper_output / "drafts"
    sources_output = paper_output / "sources"

    # Ensure output directories exist
    data_output.mkdir(parents=True, exist_ok=True)
    figures_output.mkdir(parents=True, exist_ok=True)
    drafts_output.mkdir(parents=True, exist_ok=True)
    sources_output.mkdir(parents=True, exist_ok=True)

    image_extensions = get_image_extensions()
    manuscript_extensions = get_manuscript_extensions()
    source_extensions = get_source_extensions()
    data_extensions = get_data_extensions()

    processed_info: dict[str, Any] = {
        'data_files': [],
        'image_files': [],
        'manuscript_files': [],
        'source_files': [],
        'all_files': [],
        'errors': [],
    }

    for original_path in data_files:
        file_path = original_path.expanduser()
        if not file_path.is_absolute():
            file_path = cwd / file_path
        file_path = file_path.resolve()
        if not file_path.is_file():
            message = f"Input file not found: {file_path}"
            logger.warning(message)
            processed_info["errors"].append(message)
            continue

        file_ext = file_path.suffix.lower()
        file_name = file_path.name

        # Determine destination based on file type
        # Priority: manuscript (.tex) → drafts/, images → figures/,
        # data files → data/, source files → sources/, everything else → sources/

        if file_ext in manuscript_extensions:
            # CRITICAL: Only .tex files go to drafts/ folder for editing workflow
            destination = _unique_destination(drafts_output / file_name)
            file_type = 'manuscript'
            category = 'manuscript_files'
            file_record = {
                'name': destination.name,
                'path': str(destination),
                'original': str(file_path),
                'extension': file_ext
            }
        elif file_ext in image_extensions:
            destination = _unique_destination(figures_output / file_name)
            file_type = 'image'
            category = 'image_files'
            file_record = {
                'name': destination.name,
                'path': str(destination),
                'original': str(file_path)
            }
        elif file_ext in data_extensions:
            destination = _unique_destination(data_output / file_name)
            file_type = 'data'
            category = 'data_files'
            file_record = {
                'name': destination.name,
                'path': str(destination),
                'original': str(file_path)
            }
        elif file_ext in source_extensions:
            destination = _unique_destination(sources_output / file_name)
            file_type = 'source'
            category = 'source_files'
            file_record = {
                'name': destination.name,
                'path': str(destination),
                'original': str(file_path),
                'extension': file_ext,
            }
        else:
            # Unknown files are preserved as source/context rather than discarded.
            destination = _unique_destination(sources_output / file_name)
            file_type = 'source'
            category = 'source_files'
            file_record = {
                'name': destination.name,
                'path': str(destination),
                'original': str(file_path),
                'extension': file_ext
            }

        # Copy the file
        try:
            shutil.copy2(file_path, destination)
            processed_info[category].append(file_record)
            processed_info['all_files'].append({
                'name': destination.name,
                'type': file_type,
                'destination': str(destination),
                'original': str(file_path),
            })

            # If it's a .docx file, extract images to figures folder
            if file_ext == '.docx':
                extracted_images = extract_images_from_docx(file_path, figures_output)
                if extracted_images:
                    for img_info in extracted_images:
                        processed_info['image_files'].append(img_info)

            # Delete the original file after successful copy if requested
            if delete_originals:
                file_path.unlink()

        except Exception as exc:
            message = f"Could not process {file_name}: {exc}"
            logger.warning(message, exc_info=True)
            processed_info["errors"].append(message)

    return processed_info


def create_data_context_message(processed_info: dict[str, Any] | None) -> str:
    """
    Create a context message about available data files.

    Args:
        processed_info: Dictionary with processed file information.

    Returns:
        Context message string.
    """
    if not processed_info or not processed_info['all_files']:
        return ""

    context_parts = ["\n[DATA FILES AVAILABLE]"]

    # CRITICAL: If manuscript files (.tex) are present, this is an EDITING task
    if processed_info.get('manuscript_files'):
        context_parts.append("\n⚠️  EDITING MODE - Manuscript files (.tex) detected!")
        context_parts.append("\nManuscript files (in drafts/ folder for editing):")
        for file_info in processed_info['manuscript_files']:
            context_parts.append(f"  - {file_info['name']} ({file_info['extension']}): {file_info['path']}")
        context_parts.append("\n🔧 TASK: This is an EDITING task, not creating from scratch.")
        context_parts.append("   → Read the existing manuscript from drafts/")
        context_parts.append("   → Apply the requested changes/improvements")
        context_parts.append("   → Create new version following version numbering protocol")
        context_parts.append("   → Document changes in revision_notes.md")

    if processed_info.get('source_files'):
        context_parts.append("\nSource/Context files (in sources/ folder for reference):")
        for file_info in processed_info['source_files']:
            ext = file_info.get('extension', '')
            context_parts.append(f"  - {file_info['name']} ({ext}): {file_info['path']}")
        context_parts.append("\nNote: These files are available as reference/context material.")

    if processed_info.get('data_files'):
        context_parts.append("\nData files (in data/ folder):")
        for file_info in processed_info['data_files']:
            context_parts.append(f"  - {file_info['name']}: {file_info['path']}")

    if processed_info.get('image_files'):
        # Separate images by source (direct vs extracted from docx)
        direct_images = [img for img in processed_info['image_files'] if 'source_docx' not in img]
        extracted_images = [img for img in processed_info['image_files'] if 'source_docx' in img]

        context_parts.append("\nImage files (in figures/ folder):")

        if direct_images:
            context_parts.append("  Directly provided:")
            for file_info in direct_images:
                context_parts.append(f"    - {file_info['name']}: {file_info['path']}")

        if extracted_images:
            # Group extracted images by source docx
            images_by_docx = defaultdict(list)
            for img in extracted_images:
                images_by_docx[img['source_docx']].append(img)

            context_parts.append("  Extracted from .docx files:")
            for docx_name, images in images_by_docx.items():
                img_names = ', '.join([img['name'] for img in images])
                context_parts.append(f"    - From {docx_name}: {img_names}")

        context_parts.append("\nNote: These images can be referenced as figures in the paper.")

    context_parts.append("[END DATA FILES]\n")

    return "\n".join(context_parts)

