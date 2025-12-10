"""Async API for programmatic scientific document generation."""

import asyncio
import os
import time
from pathlib import Path
from typing import Optional, List, Dict, Any, AsyncGenerator, Union, Literal
from datetime import datetime
from dotenv import load_dotenv

from claude_agent_sdk import query as claude_query, ClaudeAgentOptions
from claude_agent_sdk.types import HookMatcher, StopHookInput, HookContext

from .core import (
    get_api_key,
    load_system_instructions,
    ensure_output_folder,
    get_data_files,
    process_data_files,
    create_data_context_message,
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

# Model mapping for effort levels
EFFORT_LEVEL_MODELS = {
    "low": "claude-haiku-4-5",
    "medium": "claude-sonnet-4-5",
    "high": "claude-opus-4-5",
}


def create_completion_check_stop_hook(auto_continue: bool = True):
    """
    Create a stop hook that optionally forces continuation.
    
    Args:
        auto_continue: If True, always continue (never stop on agent's own).
                      If False, allow normal stopping behavior.
    """
    async def completion_check_stop_hook(
        hook_input: StopHookInput,
        matcher: str | None,
        context: HookContext,
    ) -> dict:
        """
        Stop hook that checks if the task is complete before allowing stop.
        
        When auto_continue is True, this returns continue_=True to force
        the agent to continue working instead of stopping.
        """
        if auto_continue:
            # Force continuation - the agent should not stop on its own
            return {"continue_": True}
        
        # Allow the stop
        return {"continue_": False}
    
    return completion_check_stop_hook


async def generate_paper(
    query: str,
    output_dir: Optional[str] = None,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    effort_level: Literal["low", "medium", "high"] = "medium",
    data_files: Optional[List[str]] = None,
    cwd: Optional[str] = None,
    track_token_usage: bool = False,
    auto_continue: bool = True,
) -> AsyncGenerator[Dict[str, Any], None]:
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
        model: Optional explicit Claude model to use. If provided, overrides effort_level.
        effort_level: Effort level that determines the model to use (default: "medium"):
            - "low": Uses Claude Haiku 4.5 (fastest, most economical)
            - "medium": Uses Claude Sonnet 4.5 (balanced) [default]
            - "high": Uses Claude Opus 4.5 (most capable)
        data_files: Optional list of data file paths to include
        cwd: Optional working directory (defaults to package parent directory)
        track_token_usage: If True, track and return token usage in the final result
        auto_continue: If True (default), the agent will not stop on its own and will
            continue working until the task is complete. Set to False to allow
            normal stopping behavior.
    
    Yields:
        Progress updates (dict with type="progress") during execution
        Final result (dict with type="result") containing all document information
        
    Example:
        ```python
        async for update in generate_paper("Create a NeurIPS paper on transformers"):
            if update["type"] == "progress":
                print(f"[{update['stage']}] {update['message']}")
            else:
                print(f"Document created: {update['paper_directory']}")
                print(f"PDF: {update['files']['pdf_final']}")
        
        # With token usage tracking:
        async for update in generate_paper("Create a paper", track_token_usage=True):
            if update["type"] == "result":
                print(f"Token usage: {update.get('token_usage')}")
        ```
    """
    # Initialize
    start_time = time.time()
    
    # Resolve model: explicit model parameter takes precedence, otherwise use effort_level
    if model is None:
        model = EFFORT_LEVEL_MODELS[effort_level]
    
    # Explicitly load .env file from working directory
    # Determine working directory first
    if cwd:
        work_dir = Path(cwd).resolve()
    else:
        work_dir = Path.cwd().resolve()
    
    # Load .env from working directory
    env_file = work_dir / ".env"
    if env_file.exists():
        load_dotenv(dotenv_path=env_file, override=True)
    
    # Get API key
    try:
        api_key_value = get_api_key(api_key)
    except ValueError as e:
        yield _create_error_result(str(e))
        return
    
    # Get package directory for copying skills to working directory
    package_dir = Path(__file__).parent.absolute()  # scientific_writer/ directory
    
    # Set up Claude skills in the working directory (includes WRITER.md)
    setup_claude_skills(package_dir, work_dir)
    
    # Ensure output folder exists in user's directory
    output_folder = ensure_output_folder(work_dir, output_dir)
    
    # Initial progress update
    yield ProgressUpdate(
        message="Initializing document generation",
        stage="initialization",
    ).to_dict()
    
    # Load system instructions from .claude/WRITER.md in working directory
    system_instructions = load_system_instructions(work_dir)
    
    # Add conversation continuity instruction
    system_instructions += "\n\n" + f"""
IMPORTANT - WORKING DIRECTORY:
- Your working directory is: {work_dir}
- ALWAYS create writing_outputs folder in this directory: {work_dir}/writing_outputs/
- NEVER write to /tmp/ or any other temporary directory
- All paper outputs MUST go to: {work_dir}/writing_outputs/<timestamp>_<description>/

IMPORTANT - CONVERSATION CONTINUITY:
- This is a NEW paper request - create a new paper directory
- Create a unique timestamped directory in the writing_outputs folder
- Do NOT assume there's an existing paper unless explicitly told in the prompt context
"""
    
    # Process data files if provided
    data_context = ""
    temp_paper_path = None
    
    if data_files:
        data_file_paths = get_data_files(work_dir, data_files)
        if data_file_paths:
            # We'll need to process these after the output directory is created
            yield ProgressUpdate(
                message=f"Found {len(data_file_paths)} data file(s) to process",
                stage="initialization",
            ).to_dict()
    
    # Check if auto-continue is enabled (parameter takes precedence over env var)
    # Environment variable can override if parameter is True (default)
    env_auto_continue = os.environ.get("SCIENTIFIC_WRITER_AUTO_CONTINUE", "").lower()
    if env_auto_continue in ("false", "0", "no"):
        auto_continue = False
    
    # Configure Claude agent options with stop hook for completion checking
    options = ClaudeAgentOptions(
        system_prompt=system_instructions,
        model=model,
        allowed_tools=["Read", "Write", "Edit", "Bash", "WebSearch", "research-lookup"],
        permission_mode="bypassPermissions",
        setting_sources=["project"],  # Load skills from project .claude directory
        cwd=str(work_dir),  # User's working directory
        max_turns=500,  # Allow many turns for long document generation
        hooks={
            "Stop": [
                HookMatcher(
                    matcher=None,  # Match all stop events
                    hooks=[create_completion_check_stop_hook(auto_continue=auto_continue)],
                )
            ]
        },
    )
    
    # Track progress through message analysis
    current_stage = "initialization"
    output_directory = None
    last_message = ""  # Track last message to avoid duplicates
    tool_call_count = 0
    files_written = []
    
    # Token usage tracking (when enabled)
    total_input_tokens = 0
    total_output_tokens = 0
    total_cache_creation_tokens = 0
    total_cache_read_tokens = 0
    
    yield ProgressUpdate(
        message="Starting document generation",
        stage="initialization",
        details={"query_length": len(query)},
    ).to_dict()
    
    # Execute query
    try:
        accumulated_text = ""
        async for message in claude_query(prompt=query, options=options):
            # Track token usage if enabled
            if track_token_usage and hasattr(message, "usage") and message.usage:
                usage = message.usage
                total_input_tokens += getattr(usage, "input_tokens", 0)
                total_output_tokens += getattr(usage, "output_tokens", 0)
                total_cache_creation_tokens += getattr(usage, "cache_creation_input_tokens", 0)
                total_cache_read_tokens += getattr(usage, "cache_read_input_tokens", 0)
            
            if hasattr(message, "content") and message.content:
                for block in message.content:
                    # Handle text blocks - stream live and analyze for progress
                    if hasattr(block, "text"):
                        text = block.text
                        accumulated_text += text
                        
                        # Yield live text update - stream Scientific-Writer's actual response
                        yield TextUpdate(content=text).to_dict()
                        
                        # Analyze text for major stage transitions (fallback)
                        stage, msg = _analyze_progress(accumulated_text, current_stage)
                        
                        # Only yield progress if we have a stage change with a message
                        if stage != current_stage and msg and msg != last_message:
                            current_stage = stage
                            last_message = msg
                            
                            yield ProgressUpdate(
                                message=msg,
                                stage=stage,
                            ).to_dict()
                    
                    # Handle tool use blocks - provide detailed progress on actions
                    elif hasattr(block, "type") and block.type == "tool_use":
                        tool_call_count += 1
                        tool_name = getattr(block, "name", "unknown")
                        tool_input = getattr(block, "input", {})
                        
                        # Track files being written
                        if tool_name.lower() == "write":
                            file_path = tool_input.get("file_path", tool_input.get("path", ""))
                            if file_path:
                                files_written.append(file_path)
                        
                        # Analyze tool usage for progress
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
        
        # Document generation complete - now scan for results
        yield ProgressUpdate(
            message="Scanning output directory",
            stage="complete",
        ).to_dict()
        
        # Find the most recently created output directory
        output_directory = _find_most_recent_output(output_folder, start_time)
        
        if not output_directory:
            error_result = _create_error_result("Output directory not found after generation")
            if track_token_usage:
                error_result['token_usage'] = TokenUsage(
                    input_tokens=total_input_tokens,
                    output_tokens=total_output_tokens,
                    cache_creation_input_tokens=total_cache_creation_tokens,
                    cache_read_input_tokens=total_cache_read_tokens,
                ).to_dict()
            yield error_result
            return
        
        # Process any data files now if we have an output directory
        if data_files:
            data_file_paths = get_data_files(work_dir, data_files)
            if data_file_paths:
                processed_info = process_data_files(
                    work_dir, 
                    data_file_paths, 
                    str(output_directory),
                    delete_originals=False  # Don't delete when using programmatic API
                )
                if processed_info:
                    manuscript_count = len(processed_info.get('manuscript_files', []))
                    message = f"Processed {len(processed_info['all_files'])} file(s)"
                    if manuscript_count > 0:
                        message += f" ({manuscript_count} manuscript(s) copied to drafts/)"
                    yield ProgressUpdate(
                        message=message,
                        stage="complete",
                    ).to_dict()
        
        # Scan the output directory for all files
        file_info = scan_paper_directory(output_directory)
        
        # Build comprehensive result
        result = _build_paper_result(output_directory, file_info)
        
        # Add token usage if tracking is enabled
        if track_token_usage:
            result.token_usage = TokenUsage(
                input_tokens=total_input_tokens,
                output_tokens=total_output_tokens,
                cache_creation_input_tokens=total_cache_creation_tokens,
                cache_read_input_tokens=total_cache_read_tokens,
            )
        
        yield ProgressUpdate(
            message="Document generation complete",
            stage="complete",
        ).to_dict()
        
        # Final result
        yield result.to_dict()
        
    except Exception as e:
        error_result = _create_error_result(f"Error during document generation: {str(e)}")
        # Include token usage even on error if tracking was enabled
        if track_token_usage:
            error_result['token_usage'] = TokenUsage(
                input_tokens=total_input_tokens,
                output_tokens=total_output_tokens,
                cache_creation_input_tokens=total_cache_creation_tokens,
                cache_read_input_tokens=total_cache_read_tokens,
            ).to_dict()
        yield error_result


def _analyze_progress(text: str, current_stage: str) -> tuple:
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


def _get_section_from_filename(filename: str) -> str:
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


def _analyze_tool_use(tool_name: str, tool_input: Dict[str, Any], current_stage: str) -> tuple:
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
            return ("writing", f"Creating bibliography with references")
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


def _find_most_recent_output(output_folder: Path, start_time: float) -> Optional[Path]:
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
            # Fallback to most recent directory overall
            recent_dirs = output_dirs
        
        # Return the most recent
        most_recent = max(recent_dirs, key=lambda d: d.stat().st_mtime)
        return most_recent
    except Exception:
        return None


def _build_paper_result(paper_dir: Path, file_info: Dict[str, Any]) -> PaperResult:
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
    
    metadata = PaperMetadata(
        title=title,
        created_at=datetime.fromtimestamp(paper_dir.stat().st_ctime).isoformat() + "Z",
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
        progress_log=file_info['progress_log'],
        summary=file_info['summary'],
    )
    
    # Citations info
    citation_count = count_citations_in_bib(file_info['bibliography'])
    citation_style = extract_citation_style(file_info['bibliography'])
    
    citations = {
        'count': citation_count,
        'style': citation_style,
        'file': file_info['bibliography'],
    }
    
    # Determine status
    status = "success"
    compilation_success = file_info['pdf_final'] is not None
    
    if not compilation_success:
        if file_info['tex_final']:
            status = "partial"  # TeX created but PDF failed
        else:
            status = "failed"
    
    result = PaperResult(
        status=status,
        paper_directory=str(paper_dir),
        paper_name=paper_dir.name,
        metadata=metadata,
        files=files,
        citations=citations,
        figures_count=len(file_info['figures']),
        compilation_success=compilation_success,
        errors=[],
    )
    
    return result


def _create_error_result(error_message: str) -> Dict[str, Any]:
    """
    Create an error result dictionary.
    
    Args:
        error_message: Error message string
    
    Returns:
        Dictionary with error information
    """
    result = PaperResult(
        status="failed",
        paper_directory="",
        paper_name="",
        errors=[error_message],
    )
    return result.to_dict()

