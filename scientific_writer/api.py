"""Async API for programmatic scientific document generation."""

import logging
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, AsyncGenerator, Literal

from dotenv import dotenv_values

from claude_agent_sdk import query as claude_query, ClaudeAgentOptions
from claude_agent_sdk.types import HookEvent, HookMatcher

from .core import (
    EFFORT_LEVEL_MODELS,
    create_completion_check_stop_hook,
    create_data_context_message,
    create_output_project,
    get_api_key,
    load_system_instructions,
    ensure_output_folder,
    get_data_files,
    process_data_files,
    resolve_auto_continue,
    setup_claude_skills,
)
from .models import ProgressUpdate, TextUpdate, PaperResult, PaperMetadata, PaperFiles, TokenUsage
from .utils import (
    scan_paper_directory,
    count_citations_in_bib,
    extract_citation_style,
    count_words_in_tex,
    extract_title_from_tex,
)


logger = logging.getLogger(__name__)

PermissionMode = Literal[
    "default",
    "acceptEdits",
    "plan",
    "bypassPermissions",
    "dontAsk",
    "auto",
]


def _build_agent_environment(work_dir: Path, api_key: str | None) -> dict[str, str]:
    """Build an invocation-local environment without mutating process globals."""
    file_values = dotenv_values(work_dir / ".env")
    environment = {
        key: value
        for key, value in file_values.items()
        if value is not None
    }
    environment.update(os.environ)
    environment["ANTHROPIC_API_KEY"] = get_api_key(api_key, environment)
    return environment


async def generate_paper(
    query: str,
    output_dir: str | None = None,
    api_key: str | None = None,
    model: str | None = None,
    effort_level: Literal["low", "medium", "high"] = "medium",
    data_files: list[str] | None = None,
    cwd: str | None = None,
    track_token_usage: bool = False,
    auto_continue: bool = True,
    permission_mode: PermissionMode = "bypassPermissions",
    max_turns: int = 500,
    max_budget_usd: float | None = None,
    max_auto_continuations: int = 1,
    skills: list[str] | Literal["all"] | None = "all",
) -> AsyncGenerator[dict[str, Any], None]:
    """
    Generate a scientific document asynchronously with progress updates.

    This is a stateless async generator that yields progress updates during
    execution and a final comprehensive result with all document details.
    Supports papers, slides, posters, reports, grants, and other document types.

    Args:
        query: The document generation request (e.g., "Create a Nature paper on CRISPR",
               "Generate conference slides on AI", "Create a research poster")
        output_dir: Optional custom output directory (defaults to cwd/writing_outputs)
        api_key: Optional Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        model: Optional explicit Claude model to use. If provided, overrides model selection.
        effort_level: SDK reasoning effort and default model tier:
            - "low": Uses Claude Haiku 4.5 (fastest, most economical)
            - "medium": Uses Claude Opus 4.8 (balanced, premium) [default]
            - "high": Uses Claude Opus 4.8 with higher reasoning effort
        data_files: Optional list of data file paths to include
        cwd: Optional working directory (defaults to the current working directory)
        track_token_usage: If True, track and return token usage in the final result
        auto_continue: Request one bounded completion-verification pass before stopping.
        permission_mode: Claude Agent SDK permission mode. ``bypassPermissions`` is
            retained as the compatibility default; callers can choose a safer mode.
        max_turns: Maximum SDK conversation turns.
        max_budget_usd: Optional hard spend ceiling enforced by the SDK.
        max_auto_continuations: Maximum Stop-hook completion-verification passes.
        skills: Skills exposed through the SDK (default: all project skills).

    Yields:
        Text updates (dict with type="text") as content streams
        Progress updates (dict with type="progress") during execution
        Final result (dict with type="result") containing all document information

    Example:
        ```python
        async for update in generate_paper("Create a NeurIPS paper on transformers"):
            if update["type"] == "text":
                print(update["content"], end="")
            elif update["type"] == "progress":
                print(f"[{update['stage']}] {update['message']}")
            elif update["type"] == "result":
                print(f"Document created: {update['paper_directory']}")
                print(f"PDF: {update['files']['pdf_final']}")

        # With token usage tracking:
        async for update in generate_paper("Create a paper", track_token_usage=True):
            if update["type"] == "result":
                print(f"Token usage: {update.get('token_usage')}")
        ```
    """
    started_at = datetime.now(timezone.utc)

    if effort_level not in EFFORT_LEVEL_MODELS:
        yield _create_error_result(f"Unknown effort level: {effort_level}")
        return
    if max_turns <= 0:
        yield _create_error_result("max_turns must be greater than zero")
        return
    if max_budget_usd is not None and max_budget_usd <= 0:
        yield _create_error_result("max_budget_usd must be greater than zero")
        return
    if max_auto_continuations < 0:
        yield _create_error_result("max_auto_continuations cannot be negative")
        return

    resolved_model = model or EFFORT_LEVEL_MODELS[effort_level]
    work_dir = Path(cwd).expanduser().resolve() if cwd else Path.cwd().resolve()
    if not work_dir.is_dir():
        yield _create_error_result(f"Working directory does not exist: {work_dir}")
        return

    try:
        agent_env = _build_agent_environment(work_dir, api_key)
    except ValueError as exc:
        yield _create_error_result(str(exc))
        return

    package_dir = Path(__file__).parent.absolute()
    setup_claude_skills(package_dir, work_dir)
    output_folder = ensure_output_folder(work_dir, output_dir)
    try:
        output_directory = create_output_project(output_folder, query)
    except OSError as exc:
        yield _create_error_result(f"Could not create output directory: {exc}")
        return

    yield ProgressUpdate(
        message="Initializing document generation",
        stage="initialization",
        details={"output_directory": str(output_directory)},
    ).to_dict()

    system_instructions = load_system_instructions(work_dir)
    system_instructions += "\n\n" + f"""
IMPORTANT - WORKING DIRECTORY:
- Your working directory is: {work_dir}
- The output project has already been created at: {output_directory}
- Write every generated artifact inside that exact project directory.
- Do NOT create or switch to another output project.
- The output root is: {output_folder}

IMPORTANT - CONVERSATION CONTINUITY:
- This invocation owns the project directory above.
- Imported manuscript files in drafts/ indicate an editing task.
"""

    processed_info: dict[str, Any] | None = None
    try:
        data_file_paths = get_data_files(work_dir, data_files) if data_files else []
        if data_file_paths:
            processed_info = process_data_files(
                work_dir,
                data_file_paths,
                str(output_directory),
                delete_originals=False,
            )
    except (OSError, ValueError) as exc:
        yield _create_error_result(
            f"Could not prepare input files: {exc}",
            output_directory=output_directory,
        )
        return

    if data_file_paths:
        processed_count = len(processed_info["all_files"]) if processed_info else 0
        yield ProgressUpdate(
            message=f"Staged {processed_count} input file(s)",
            stage="initialization",
        ).to_dict()

    data_context = create_data_context_message(processed_info)
    contextual_query = f"""[CONTEXT: Work only in {output_directory}]
[INSTRUCTION: Use the staged files below while completing the request.]
{data_context}

User request:
{query}"""

    resolved_auto_continue = resolve_auto_continue(auto_continue, agent_env)
    hooks: dict[HookEvent, list[HookMatcher]] | None = None
    if resolved_auto_continue:
        hooks = {
            "Stop": [
                HookMatcher(
                    matcher=None,
                    hooks=[
                        create_completion_check_stop_hook(
                            auto_continue=True,
                            max_continuations=max_auto_continuations,
                        )
                    ],
                )
            ]
        }

    options = ClaudeAgentOptions(
        system_prompt=system_instructions,
        model=resolved_model,
        effort=effort_level,
        allowed_tools=["Read", "Write", "Edit", "Bash", "WebSearch"],
        permission_mode=permission_mode,
        setting_sources=["project"],
        skills=skills,
        cwd=str(work_dir),
        max_turns=max_turns,
        max_budget_usd=max_budget_usd,
        env=agent_env,
        hooks=hooks,
    )

    current_stage = "initialization"
    last_message = ""
    tool_call_count = 0
    files_written: set[str] = set()
    token_usage = TokenUsage()

    yield ProgressUpdate(
        message="Starting document generation",
        stage="initialization",
        details={
            "query_length": len(query),
            "output_directory": str(output_directory),
        },
    ).to_dict()

    try:
        recent_text = ""
        async for message in claude_query(prompt=contextual_query, options=options):
            if track_token_usage and hasattr(message, "usage") and message.usage:
                token_usage.add_usage(message.usage)

            if hasattr(message, "content") and message.content:
                for block in message.content:
                    if hasattr(block, "text"):
                        text = block.text
                        recent_text = (recent_text + text)[-20_000:]
                        yield TextUpdate(content=text).to_dict()

                        stage, msg = _analyze_progress(recent_text, current_stage)
                        if stage != current_stage and msg and msg != last_message:
                            current_stage = stage
                            last_message = msg
                            yield ProgressUpdate(
                                message=msg,
                                stage=stage,
                            ).to_dict()

                    elif hasattr(block, "type") and block.type == "tool_use":
                        tool_call_count += 1
                        tool_name = getattr(block, "name", "unknown")
                        tool_input = getattr(block, "input", {})

                        if tool_name.lower() == "write":
                            file_path = tool_input.get("file_path", tool_input.get("path", ""))
                            if file_path:
                                files_written.add(file_path)

                        tool_progress = _analyze_tool_use(tool_name, tool_input, current_stage)
                        if tool_progress:
                            stage, msg = tool_progress
                            if msg != last_message:
                                current_stage = stage
                                last_message = msg
                                yield ProgressUpdate(
                                    message=msg,
                                    stage=stage,
                                    details={
                                        "tool": tool_name,
                                        "tool_calls": tool_call_count,
                                        "files_created": len(files_written),
                                    },
                                ).to_dict()

        yield ProgressUpdate(
            message="Scanning output directory",
            stage="complete",
        ).to_dict()

        file_info = scan_paper_directory(output_directory)
        result = _build_paper_result(
            output_directory,
            file_info,
            created_at=started_at,
        )
        if processed_info:
            result.errors.extend(processed_info.get("errors", []))
        if track_token_usage:
            result.token_usage = token_usage

        yield ProgressUpdate(
            message="Document generation complete",
            stage="complete",
        ).to_dict()
        yield result.to_dict()

    except Exception as exc:
        logger.exception("Document generation failed")
        error_result = _create_error_result(
            f"Error during document generation: {exc}",
            output_directory=output_directory,
        )
        if track_token_usage:
            error_result['token_usage'] = token_usage.to_dict()
        yield error_result


def _analyze_progress(text: str, current_stage: str) -> tuple[str, str | None]:
    """
    Minimal fallback for progress detection from text.

    Primary progress updates come from tool usage analysis (_analyze_tool_use).
    This function only detects major stage transitions when no tool updates available.

    Returns:
        Tuple of (stage, message) - returns current stage if no transition detected
    """
    text_lower = text.lower()

    # Stage order for progression tracking
    stage_order = ["initialization", "planning", "research", "writing", "compilation", "complete"]
    current_idx = stage_order.index(current_stage) if current_stage in stage_order else 0

    # Only detect major stage transitions - let tool analysis handle specifics
    # Check for compilation indicators (most definitive)
    if current_idx < stage_order.index("compilation"):
        if "pdflatex" in text_lower or "latexmk" in text_lower or "compiling" in text_lower:
            return "compilation", "Compiling document"

    # Check for completion indicators
    if current_idx < stage_order.index("complete"):
        if "successfully compiled" in text_lower or "pdf generated" in text_lower:
            return "complete", "Finalizing output"

    # No stage transition detected - return current stage without message change
    return current_stage, None


def _detect_document_type(file_path: str) -> str:
    """Detect document type from file path."""
    path_lower = file_path.lower()
    if "slide" in path_lower or "presentation" in path_lower or "beamer" in path_lower:
        return "slides"
    elif "poster" in path_lower:
        return "poster"
    elif "report" in path_lower:
        return "report"
    elif "grant" in path_lower or "proposal" in path_lower:
        return "grant"
    return "document"


def _get_section_from_filename(filename: str) -> str | None:
    """Extract section name from filename for more descriptive messages."""
    name_lower = filename.lower().replace('.tex', '').replace('.md', '')

    section_mappings = {
        'abstract': 'abstract',
        'intro': 'introduction',
        'introduction': 'introduction',
        'method': 'methods',
        'methods': 'methods',
        'methodology': 'methodology',
        'result': 'results',
        'results': 'results',
        'discussion': 'discussion',
        'conclusion': 'conclusion',
        'conclusions': 'conclusions',
        'background': 'background',
        'related': 'related work',
        'experiment': 'experiments',
        'experiments': 'experiments',
        'evaluation': 'evaluation',
        'appendix': 'appendix',
        'supplement': 'supplementary material',
    }

    for key, section in section_mappings.items():
        if key in name_lower:
            return section
    return None


def _analyze_tool_use(
    tool_name: str, tool_input: dict[str, Any], current_stage: str
) -> tuple[str, str] | None:
    """
    Analyze tool usage to provide dynamic, context-aware progress updates.

    Args:
        tool_name: Name of the tool being used
        tool_input: Input parameters to the tool
        current_stage: Current progress stage

    Returns:
        Tuple of (stage, message) or None if no update needed
    """
    # Stage order for progression
    stage_order = ["initialization", "planning", "research", "writing", "compilation", "complete"]
    current_idx = stage_order.index(current_stage) if current_stage in stage_order else 0

    # Extract relevant info from tool input
    file_path = tool_input.get("file_path", tool_input.get("path", ""))
    command = tool_input.get("command", "")
    filename = Path(file_path).name if file_path else ""
    doc_type = _detect_document_type(file_path)

    # Read tool - detect what's being read
    if tool_name.lower() == "read":
        if ".bib" in file_path:
            return ("writing", f"Reading bibliography: {filename}")
        elif ".tex" in file_path:
            section = _get_section_from_filename(filename)
            if section:
                return ("writing", f"Reading {section} section")
            return ("writing", f"Reading {filename}")
        elif ".pdf" in file_path:
            return ("research", f"Analyzing PDF: {filename}")
        elif ".csv" in file_path:
            return ("research", f"Loading data from {filename}")
        elif ".json" in file_path:
            return ("research", f"Reading configuration: {filename}")
        elif ".md" in file_path:
            return ("planning", f"Reading {filename}")
        elif file_path:
            return (current_stage, f"Reading {filename}")
        return None

    # Write tool - detect what's being written
    elif tool_name.lower() == "write":
        if ".bib" in file_path:
            return ("writing", "Creating bibliography with references")
        elif ".tex" in file_path:
            section = _get_section_from_filename(filename)
            if section:
                return ("writing", f"Writing {section} section")
            elif "main" in filename.lower():
                return ("writing", f"Creating main {doc_type} structure")
            elif current_idx < stage_order.index("writing"):
                return ("writing", f"Writing {doc_type}: {filename}")
            else:
                return ("compilation", f"Updating {filename}")
        elif ".md" in file_path:
            if "progress" in filename.lower():
                return ("writing", "Updating progress log")
            elif "readme" in filename.lower():
                return ("complete", "Creating documentation")
            return ("writing", f"Writing {filename}")
        elif ".sty" in file_path:
            return ("writing", f"Creating style file: {filename}")
        elif ".cls" in file_path:
            return ("writing", f"Creating document class: {filename}")
        elif file_path:
            return (current_stage, f"Creating {filename}")
        return None

    # Edit tool
    elif tool_name.lower() == "edit":
        if ".tex" in file_path:
            section = _get_section_from_filename(filename)
            if section:
                return ("writing", f"Refining {section} section")
            return ("writing", f"Editing {filename}")
        elif ".bib" in file_path:
            return ("writing", "Updating bibliography")
        elif file_path:
            return (current_stage, f"Editing {filename}")
        return None

    # Bash tool - detect compilation and other commands
    elif tool_name.lower() == "bash":
        if "pdflatex" in command:
            # Try to extract filename from command
            if "-output-directory" in command:
                return ("compilation", "Compiling PDF with output directory")
            return ("compilation", "Compiling LaTeX to PDF")
        elif "latexmk" in command:
            return ("compilation", "Running full LaTeX compilation pipeline")
        elif "bibtex" in command:
            return ("compilation", "Processing bibliography citations")
        elif "makeindex" in command:
            return ("compilation", "Building document index")
        elif "mkdir" in command:
            # Try to extract directory purpose
            if "writing_outputs" in command or "output" in command.lower():
                return ("initialization", "Creating output directory")
            elif "figures" in command.lower():
                return ("initialization", "Setting up figures directory")
            elif "drafts" in command.lower():
                return ("initialization", "Setting up drafts directory")
            return ("initialization", "Creating directory structure")
        elif "cp " in command:
            if ".pdf" in command:
                return ("complete", "Copying final PDF to output")
            elif ".tex" in command:
                return ("complete", "Archiving LaTeX source")
            return ("complete", "Organizing files")
        elif "mv " in command:
            return ("complete", "Moving files to final location")
        elif "ls " in command or "cat " in command:
            return None  # Don't report on inspection commands
        elif command:
            # Truncate long commands intelligently
            cmd_preview = command.split()[0] if command.split() else command[:30]
            return (current_stage, f"Running {cmd_preview}")
        return None

    # Research lookup tool
    elif "research" in tool_name.lower() or "lookup" in tool_name.lower():
        query_text = tool_input.get("query", "")
        if query_text:
            # Truncate but keep meaningful content
            truncated = query_text[:50] + "..." if len(query_text) > 50 else query_text
            return ("research", f"Searching: {truncated}")
        return ("research", "Searching literature databases")

    # Web search or similar tools
    elif "search" in tool_name.lower() or "web" in tool_name.lower():
        query_text = tool_input.get("query", tool_input.get("search_term", ""))
        if query_text:
            truncated = query_text[:40] + "..." if len(query_text) > 40 else query_text
            return ("research", f"Web search: {truncated}")
        return ("research", "Searching online resources")

    return None


def _find_most_recent_output(output_folder: Path, start_time: float) -> Path | None:
    """
    Find the most recently created/modified output directory.

    Args:
        output_folder: Path to output folder
        start_time: Start time of generation (to filter relevant directories)

    Returns:
        Path to output directory or None
    """
    try:
        output_dirs = [d for d in output_folder.iterdir() if d.is_dir()]
        if not output_dirs:
            return None

        # Filter to only directories modified after start_time
        recent_dirs = [
            d for d in output_dirs
            if d.stat().st_mtime >= start_time - 5  # 5 second buffer
        ]

        if not recent_dirs:
            return None

        # Return the most recent
        most_recent = max(recent_dirs, key=lambda d: d.stat().st_mtime)
        return most_recent
    except OSError:
        logger.warning("Could not inspect output folder %s", output_folder, exc_info=True)
        return None


def _build_paper_result(
    paper_dir: Path,
    file_info: dict[str, Any],
    created_at: datetime | None = None,
) -> PaperResult:
    """
    Build a comprehensive PaperResult from scanned files.

    Args:
        paper_dir: Path to paper directory
        file_info: Dictionary of file information from scan_paper_directory

    Returns:
        PaperResult object
    """
    # Extract metadata
    tex_file = file_info['tex_final'] or (file_info['tex_drafts'][0] if file_info['tex_drafts'] else None)

    title = extract_title_from_tex(tex_file)
    word_count = count_words_in_tex(tex_file)

    # Extract topic from directory name
    topic = ""
    parts = paper_dir.name.split('_', 2)
    if len(parts) >= 3:
        topic = parts[2].replace('_', ' ')

    if created_at is None:
        try:
            local_created_at = datetime.strptime(
                paper_dir.name[:15],
                "%Y%m%d_%H%M%S",
            ).astimezone()
            created_at = local_created_at.astimezone(timezone.utc)
        except ValueError:
            created_at = datetime.fromtimestamp(
                paper_dir.stat().st_mtime,
                tz=timezone.utc,
            )

    metadata = PaperMetadata(
        title=title,
        created_at=created_at.astimezone(timezone.utc).isoformat(),
        topic=topic,
        word_count=word_count,
    )

    # Build files object
    files = PaperFiles(
        pdf_final=file_info['pdf_final'],
        tex_final=file_info['tex_final'],
        pdf_drafts=file_info['pdf_drafts'],
        tex_drafts=file_info['tex_drafts'],
        bibliography=file_info['bibliography'],
        figures=file_info['figures'],
        data=file_info['data'],
        sources=file_info['sources'],
        final_artifacts=file_info['final_artifacts'],
        draft_artifacts=file_info['draft_artifacts'],
        artifacts=file_info['artifacts'],
        progress_log=file_info['progress_log'],
        summary=file_info['summary'],
    )

    # Citations info
    citation_count = count_citations_in_bib(file_info['bibliography'])
    citation_style = extract_citation_style(file_info['bibliography'], tex_file=tex_file)

    citations = {
        'count': citation_count,
        'style': citation_style,
        'file': file_info['bibliography'],
    }

    # Determine status
    compilation_success = file_info['pdf_final'] is not None
    errors: list[str] = []
    if file_info['final_artifacts']:
        status = "success"
    elif file_info['draft_artifacts']:
        status = "partial"
        errors.append("No final artifact was produced")
    else:
        status = "failed"
        errors.append("No final or draft document artifact was produced")

    result = PaperResult(
        status=status,
        paper_directory=str(paper_dir),
        paper_name=paper_dir.name,
        metadata=metadata,
        files=files,
        citations=citations,
        figures_count=len(file_info['figures']),
        compilation_success=compilation_success,
        errors=errors,
    )

    return result


def _create_error_result(
    error_message: str,
    output_directory: Path | None = None,
) -> dict[str, Any]:
    """
    Create an error result dictionary.

    Args:
        error_message: Error message string

    Returns:
        Dictionary with error information
    """
    result = PaperResult(
        status="failed",
        paper_directory=str(output_directory) if output_directory else "",
        paper_name=output_directory.name if output_directory else "",
        errors=[error_message],
    )
    return result.to_dict()

