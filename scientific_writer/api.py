"""Async API for programmatic scientific document generation."""

import asyncio
import time
from pathlib import Path
from typing import Optional, List, Dict, Any, AsyncGenerator, Union
from datetime import datetime
from dotenv import load_dotenv

from claude_agent_sdk import query as claude_query, ClaudeAgentOptions

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
    Generate a scientific document asynchronously with progress updates.
    
    This is a stateless async generator that yields progress updates during
    execution and a final comprehensive result with all document details.
    Supports papers, slides, posters, reports, grants, and other document types.
    
    Args:
        query: The document generation request (e.g., "Create a Nature paper on CRISPR",
               "Generate conference slides on AI", "Create a research poster")
        output_dir: Optional custom output directory (defaults to cwd/paper_outputs)
        api_key: Optional Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        model: Claude model to use (default: claude-sonnet-4-20250514)
        data_files: Optional list of data file paths to include
        cwd: Optional working directory (defaults to package parent directory)
    
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
        message="Initializing document generation",
        stage="initialization",
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
            # We'll need to process these after the output directory is created
            yield ProgressUpdate(
                message=f"Found {len(data_file_paths)} data file(s) to process",
                stage="initialization",
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
    output_directory = None
    last_message = ""  # Track last message to avoid duplicates
    tool_call_count = 0
    files_written = []
    
    yield ProgressUpdate(
        message="Starting document generation with Claude",
        stage="initialization",
        details={"model": model, "query_length": len(query)},
    ).to_dict()
    
    # Execute query with Claude
    try:
        accumulated_text = ""
        async for message in claude_query(prompt=query, options=options):
            if hasattr(message, "content") and message.content:
                for block in message.content:
                    # Handle text blocks - analyze for progress indicators
                    if hasattr(block, "text"):
                        text = block.text
                        accumulated_text += text
                        
                        # Analyze text for progress indicators
                        stage, msg = _analyze_progress(accumulated_text, current_stage)
                        
                        if stage != current_stage and msg != last_message:
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
            yield _create_error_result("Output directory not found after generation")
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
        
        yield ProgressUpdate(
            message="Document generation complete",
            stage="complete",
        ).to_dict()
        
        # Final result
        yield result.to_dict()
        
    except Exception as e:
        yield _create_error_result(f"Error during document generation: {str(e)}")


def _analyze_progress(text: str, current_stage: str) -> tuple:
    """
    Analyze accumulated text to determine current progress stage.
    
    Returns:
        Tuple of (stage, message)
    """
    text_lower = text.lower()
    
    # Stage order for progression tracking
    stage_order = ["initialization", "planning", "research", "writing", "compilation", "complete"]
    current_idx = stage_order.index(current_stage) if current_stage in stage_order else 0
    
    # Progress indicators with specific messages (stage, message, keywords)
    progress_indicators = [
        # Planning stage
        ("planning", "Creating outline and structure", 
         ["outline", "structure", "plan", "sections"]),
        ("planning", "Analyzing requirements and scope",
         ["analyzing", "requirements", "scope"]),
        
        # Research stage
        ("research", "Searching literature databases",
         ["searching", "pubmed", "arxiv", "scholar", "database"]),
        ("research", "Gathering relevant publications",
         ["publications", "references", "citations"]),
        ("research", "Synthesizing research findings",
         ["synthesiz", "review", "findings"]),
        
        # Writing stage
        ("writing", "Writing abstract",
         ["abstract"]),
        ("writing", "Writing introduction section",
         ["introduction", "background"]),
        ("writing", "Writing methods section",
         ["methods", "methodology", "materials"]),
        ("writing", "Writing results section",
         ["results", "findings", "analysis"]),
        ("writing", "Writing discussion section",
         ["discussion", "implications"]),
        ("writing", "Writing conclusion",
         ["conclusion", "concluding", "summary"]),
        ("writing", "Formatting bibliography",
         ["bibliography", "bibtex", "references.bib"]),
        
        # Compilation stage
        ("compilation", "Creating LaTeX document",
         ["\\documentclass", "\\begin{document}", ".tex"]),
        ("compilation", "Running pdflatex compilation",
         ["pdflatex", "latexmk", "compiling"]),
        ("compilation", "Processing bibliography with BibTeX",
         ["bibtex", "processing citations"]),
        ("compilation", "Final PDF compilation",
         ["final compilation", "recompiling"]),
        
        # Finalization stage
        ("complete", "Verifying output files",
         ["verifying", "checking", "output"]),
        ("complete", "Organizing output directory",
         ["organizing", "directory", "files"]),
    ]
    
    # Find the most advanced matching indicator
    best_match = None
    best_idx = current_idx
    for stage, message, keywords in progress_indicators:
        if any(kw in text_lower for kw in keywords):
            stage_idx = stage_order.index(stage) if stage in stage_order else 0
            if stage_idx > best_idx:
                best_match = (stage, message)
                best_idx = stage_idx
    
    if best_match:
        return best_match
    
    # Fallback to simple keyword detection
    if "research" in text_lower or "literature" in text_lower:
        if current_idx < stage_order.index("research"):
            return "research", "Conducting literature research"
    
    if "writing" in text_lower:
        if current_idx < stage_order.index("writing"):
            return "writing", "Writing document sections"
    
    if "compil" in text_lower or "latex" in text_lower or "pdf" in text_lower:
        if current_idx < stage_order.index("compilation"):
            return "compilation", "Compiling LaTeX to PDF"
    
    if "complete" in text_lower or "finished" in text_lower or "done" in text_lower:
        if current_idx < stage_order.index("complete"):
            return "complete", "Finalizing document"
    
    # No change detected
    return current_stage, "Processing..."


def _analyze_tool_use(tool_name: str, tool_input: Dict[str, Any], current_stage: str) -> tuple:
    """
    Analyze tool usage to provide detailed progress updates.
    
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
    
    # Read tool - detect what's being read
    if tool_name.lower() == "read":
        if ".bib" in file_path:
            return ("writing", f"Reading bibliography: {Path(file_path).name}")
        elif ".tex" in file_path:
            return ("compilation", f"Reading LaTeX file: {Path(file_path).name}")
        elif ".pdf" in file_path or ".csv" in file_path or ".json" in file_path:
            return ("research", f"Reading data file: {Path(file_path).name}")
        else:
            return (current_stage, f"Reading: {Path(file_path).name}")
    
    # Write tool - detect what's being written
    elif tool_name.lower() == "write":
        if ".bib" in file_path:
            return ("writing", f"Creating bibliography: {Path(file_path).name}")
        elif ".tex" in file_path:
            filename = Path(file_path).name
            if "main" in filename.lower() or current_idx < stage_order.index("writing"):
                return ("writing", f"Writing LaTeX document: {filename}")
            else:
                return ("compilation", f"Updating LaTeX: {filename}")
        elif ".md" in file_path:
            return ("writing", f"Writing document: {Path(file_path).name}")
        else:
            return (current_stage, f"Writing: {Path(file_path).name}")
    
    # Edit tool
    elif tool_name.lower() == "edit":
        if ".tex" in file_path:
            return ("writing", f"Editing LaTeX: {Path(file_path).name}")
        else:
            return (current_stage, f"Editing: {Path(file_path).name}")
    
    # Bash tool - detect compilation and other commands
    elif tool_name.lower() == "bash":
        if "pdflatex" in command or "latexmk" in command:
            return ("compilation", "Compiling LaTeX to PDF")
        elif "bibtex" in command:
            return ("compilation", "Processing bibliography with BibTeX")
        elif "mkdir" in command:
            return ("initialization", "Creating output directory")
        elif "cp " in command or "mv " in command:
            return ("complete", "Organizing output files")
        else:
            return (current_stage, f"Running: {command[:50]}...")
    
    # Research lookup tool
    elif "research" in tool_name.lower() or "lookup" in tool_name.lower():
        query_text = tool_input.get("query", "")[:40]
        return ("research", f"Researching: {query_text}...")
    
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

