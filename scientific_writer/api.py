"""Async API for programmatic scientific paper generation."""

import asyncio
import time
from pathlib import Path
from typing import Optional, List, Dict, Any, AsyncGenerator, Union
from datetime import datetime
from dotenv import load_dotenv

from claude_agent_sdk import query, ClaudeAgentOptions

from .core import (
    get_api_key,
    load_system_instructions,
    ensure_output_folder,
    get_data_files,
    process_data_files,
    create_data_context_message,
    setup_claude_skills,
)
from .models import ProgressUpdate, PaperResult, PaperMetadata, PaperFiles
from .utils import (
    scan_paper_directory,
    count_citations_in_bib,
    extract_citation_style,
    count_words_in_tex,
    extract_title_from_tex,
)


async def generate_paper(
    query: str,
    output_dir: Optional[str] = None,
    api_key: Optional[str] = None,
    model: str = "claude-sonnet-4-20250514",
    data_files: Optional[List[str]] = None,
    cwd: Optional[str] = None,
) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Generate a scientific paper asynchronously with progress updates.
    
    This is a stateless async generator that yields progress updates during
    execution and a final comprehensive result with all paper details.
    
    Args:
        query: The paper generation request (e.g., "Create a Nature paper on CRISPR")
        output_dir: Optional custom output directory (defaults to cwd/paper_outputs)
        api_key: Optional Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        model: Claude model to use (default: claude-sonnet-4-20250514)
        data_files: Optional list of data file paths to include
        cwd: Optional working directory (defaults to package parent directory)
    
    Yields:
        Progress updates (dict with type="progress") during execution
        Final result (dict with type="result") containing all paper information
        
    Example:
        ```python
        async for update in generate_paper("Create a NeurIPS paper on transformers"):
            if update["type"] == "progress":
                print(f"[{update['percentage']}%] {update['message']}")
            else:
                print(f"Paper created: {update['paper_directory']}")
                print(f"PDF: {update['files']['pdf_final']}")
        ```
    """
    # Initialize
    start_time = time.time()
    
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
        message="Initializing paper generation",
        stage="initialization",
        percentage=0,
    ).to_dict()
    
    # Load system instructions from .claude/WRITER.md in working directory
    system_instructions = load_system_instructions(work_dir)
    
    # Add conversation continuity instruction
    system_instructions += "\n\n" + f"""
IMPORTANT - WORKING DIRECTORY:
- Your working directory is: {work_dir}
- ALWAYS create paper_outputs folder in this directory: {work_dir}/paper_outputs/
- NEVER write to /tmp/ or any other temporary directory
- All paper outputs MUST go to: {work_dir}/paper_outputs/<timestamp>_<description>/

IMPORTANT - CONVERSATION CONTINUITY:
- This is a NEW paper request - create a new paper directory
- Create a unique timestamped directory in the paper_outputs folder
- Do NOT assume there's an existing paper unless explicitly told in the prompt context
"""
    
    # Process data files if provided
    data_context = ""
    temp_paper_path = None
    
    if data_files:
        data_file_paths = get_data_files(work_dir, data_files)
        if data_file_paths:
            # We'll need to process these after the paper directory is created
            yield ProgressUpdate(
                message=f"Found {len(data_file_paths)} data file(s) to process",
                stage="initialization",
                percentage=5,
            ).to_dict()
    
    # Configure Claude agent options
    options = ClaudeAgentOptions(
        system_prompt=system_instructions,
        model=model,
        allowed_tools=["Read", "Write", "Edit", "Bash", "research-lookup"],
        permission_mode="bypassPermissions",
        setting_sources=["project"],  # Load skills from project .claude directory
        cwd=str(work_dir),  # User's working directory
    )
    
    # Track progress through message analysis
    current_stage = "initialization"
    current_percentage = 10
    paper_directory = None
    
    yield ProgressUpdate(
        message="Starting paper generation with Claude",
        stage="initialization",
        percentage=10,
    ).to_dict()
    
    # Execute query with Claude
    try:
        accumulated_text = ""
        async for message in query(prompt=query, options=options):
            if hasattr(message, "content") and message.content:
                for block in message.content:
                    if hasattr(block, "text"):
                        text = block.text
                        accumulated_text += text
                        
                        # Analyze text for progress indicators
                        stage, percentage, msg = _analyze_progress(accumulated_text, current_stage, current_percentage)
                        
                        if stage != current_stage or percentage != current_percentage:
                            current_stage = stage
                            current_percentage = percentage
                            
                            yield ProgressUpdate(
                                message=msg,
                                stage=stage,
                                percentage=percentage,
                            ).to_dict()
        
        # Paper generation complete - now scan for results
        yield ProgressUpdate(
            message="Scanning paper output directory",
            stage="complete",
            percentage=95,
        ).to_dict()
        
        # Find the most recently created paper directory
        paper_directory = _find_most_recent_paper(output_folder, start_time)
        
        if not paper_directory:
            yield _create_error_result("Paper directory not found after generation")
            return
        
        # Process any data files now if we have a paper directory
        if data_files:
            data_file_paths = get_data_files(work_dir, data_files)
            if data_file_paths:
                processed_info = process_data_files(
                    work_dir, 
                    data_file_paths, 
                    str(paper_directory),
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
                        percentage=97,
                    ).to_dict()
        
        # Scan the paper directory for all files
        file_info = scan_paper_directory(paper_directory)
        
        # Build comprehensive result
        result = _build_paper_result(paper_directory, file_info)
        
        yield ProgressUpdate(
            message="Paper generation complete",
            stage="complete",
            percentage=100,
        ).to_dict()
        
        # Final result
        yield result.to_dict()
        
    except Exception as e:
        yield _create_error_result(f"Error during paper generation: {str(e)}")


def _analyze_progress(text: str, current_stage: str, current_percentage: int) -> tuple:
    """
    Analyze accumulated text to determine current progress stage.
    
    Returns:
        Tuple of (stage, percentage, message)
    """
    text_lower = text.lower()
    
    # Check for various progress indicators
    if "research" in text_lower or "literature" in text_lower or "searching" in text_lower:
        if current_stage != "research":
            return "research", 30, "Conducting literature research"
    
    if "writing" in text_lower or "introduction" in text_lower or "methods" in text_lower:
        if current_stage != "writing":
            return "writing", 50, "Writing paper sections"
        elif current_percentage < 70:
            return "writing", min(current_percentage + 10, 70), "Writing paper sections"
    
    if "compil" in text_lower or "latex" in text_lower or "pdf" in text_lower:
        if current_stage != "compilation":
            return "compilation", 80, "Compiling LaTeX to PDF"
    
    if "complete" in text_lower or "finished" in text_lower or "done" in text_lower:
        return "complete", 90, "Finalizing paper"
    
    # No change detected
    return current_stage, current_percentage, "Processing..."


def _find_most_recent_paper(output_folder: Path, start_time: float) -> Optional[Path]:
    """
    Find the most recently created/modified paper directory.
    
    Args:
        output_folder: Path to paper_outputs folder
        start_time: Start time of generation (to filter relevant directories)
    
    Returns:
        Path to paper directory or None
    """
    try:
        paper_dirs = [d for d in output_folder.iterdir() if d.is_dir()]
        if not paper_dirs:
            return None
        
        # Filter to only directories modified after start_time
        recent_dirs = [
            d for d in paper_dirs 
            if d.stat().st_mtime >= start_time - 5  # 5 second buffer
        ]
        
        if not recent_dirs:
            # Fallback to most recent directory overall
            recent_dirs = paper_dirs
        
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

