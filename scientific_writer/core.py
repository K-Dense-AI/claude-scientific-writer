"""Core utilities for scientific writer."""

import os
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


def setup_claude_skills(package_dir: Path, work_dir: Path) -> None:
    """
    Set up Claude skills by copying from package to working directory.
    
    Args:
        package_dir: Package installation directory containing .claude/
        work_dir: User's working directory where .claude/ should be copied
    """
    source_claude = package_dir / ".claude"
    dest_claude = work_dir / ".claude"
    
    # Only copy if source exists and destination doesn't
    if source_claude.exists() and not dest_claude.exists():
        try:
            shutil.copytree(source_claude, dest_claude)
            print(f"✓ Initialized Claude skills in {dest_claude}")
        except Exception as e:
            print(f"Warning: Could not copy Claude skills: {e}")
    elif not source_claude.exists():
        print(f"Warning: Skills directory not found in package: {source_claude}")


def get_api_key(api_key: Optional[str] = None) -> str:
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
    
    env_key = os.getenv("ANTHROPIC_API_KEY")
    if not env_key:
        raise ValueError(
            "ANTHROPIC_API_KEY not found. Either pass api_key parameter or set "
            "ANTHROPIC_API_KEY environment variable."
        )
    return env_key


def load_system_instructions(package_dir: Path) -> str:
    """
    Load system instructions from package's CLAUDE.md file.
    
    Args:
        package_dir: Package installation directory containing CLAUDE.md.
        
    Returns:
        System instructions string.
    """
    instructions_file = package_dir / "CLAUDE.md"
    
    if instructions_file.exists():
        with open(instructions_file, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        # Fallback if CLAUDE.md doesn't exist in package
        return (
            "You are a scientific writing assistant. Follow best practices for "
            "scientific communication and always present a plan before execution."
        )


def ensure_output_folder(cwd: Path, custom_dir: Optional[str] = None) -> Path:
    """
    Ensure the paper_outputs folder exists.
    
    Args:
        cwd: Current working directory (project root).
        custom_dir: Optional custom output directory path.
        
    Returns:
        Path to the output folder.
    """
    if custom_dir:
        output_folder = Path(custom_dir).resolve()
    else:
        output_folder = cwd / "paper_outputs"
    
    output_folder.mkdir(exist_ok=True, parents=True)
    return output_folder


def get_image_extensions() -> set:
    """Return a set of common image file extensions."""
    return {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif', '.svg', '.webp', '.ico'}


def get_data_files(cwd: Path, data_files: Optional[List[str]] = None) -> List[Path]:
    """
    Get data files either from provided list or from data folder.
    
    Args:
        cwd: Current working directory (project root).
        data_files: Optional list of file paths. If not provided, reads from data/ folder.
        
    Returns:
        List of Path objects for data files.
    """
    if data_files:
        return [Path(f).resolve() for f in data_files]
    
    data_folder = cwd / "data"
    if not data_folder.exists():
        return []
    
    files = []
    for file_path in data_folder.iterdir():
        if file_path.is_file():
            files.append(file_path)
    
    return files


def process_data_files(
    cwd: Path, 
    data_files: List[Path], 
    paper_output_path: str,
    delete_originals: bool = True
) -> Optional[Dict[str, Any]]:
    """
    Process data files by copying them to the paper output folder.
    Images go to figures/, other files go to data/.
    
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
    
    # Ensure output directories exist
    data_output.mkdir(parents=True, exist_ok=True)
    figures_output.mkdir(parents=True, exist_ok=True)
    
    image_extensions = get_image_extensions()
    processed_info = {
        'data_files': [],
        'image_files': [],
        'all_files': []
    }
    
    for file_path in data_files:
        file_ext = file_path.suffix.lower()
        file_name = file_path.name
        
        # Determine destination based on file type
        if file_ext in image_extensions:
            destination = figures_output / file_name
            file_type = 'image'
            processed_info['image_files'].append({
                'name': file_name,
                'path': str(destination),
                'original': str(file_path)
            })
        else:
            destination = data_output / file_name
            file_type = 'data'
            processed_info['data_files'].append({
                'name': file_name,
                'path': str(destination),
                'original': str(file_path)
            })
        
        # Copy the file
        try:
            shutil.copy2(file_path, destination)
            processed_info['all_files'].append({
                'name': file_name,
                'type': file_type,
                'destination': str(destination)
            })
            
            # Delete the original file after successful copy if requested
            if delete_originals:
                file_path.unlink()
            
        except Exception as e:
            print(f"Warning: Could not process {file_name}: {str(e)}")
    
    return processed_info


def create_data_context_message(processed_info: Optional[Dict[str, Any]]) -> str:
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
    
    if processed_info['data_files']:
        context_parts.append("\nData files (in data/ folder):")
        for file_info in processed_info['data_files']:
            context_parts.append(f"  - {file_info['name']}: {file_info['path']}")
    
    if processed_info['image_files']:
        context_parts.append("\nImage files (in figures/ folder):")
        for file_info in processed_info['image_files']:
            context_parts.append(f"  - {file_info['name']}: {file_info['path']}")
        context_parts.append("\nNote: These images can be referenced as figures in the paper.")
    
    context_parts.append("[END DATA FILES]\n")
    
    return "\n".join(context_parts)

