#!/usr/bin/env python3
"""
Scientific Writer CLI Tool
A command-line interface for scientific writing powered by Claude Code.
"""

import os
import sys
import asyncio
import shutil
from pathlib import Path
from dotenv import load_dotenv
from claude_agent_sdk import query, ClaudeAgentOptions

# Load environment variables from .env file if it exists
load_dotenv()


def get_api_key():
    """Get the Anthropic API key from environment variables."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        print("Please set it in a .env file or export it in your shell:")
        print("  export ANTHROPIC_API_KEY='your_api_key_here'")
        sys.exit(1)
    return api_key


def load_system_instructions(cwd):
    """Load system instructions from claude.md file."""
    instructions_file = cwd / "claude.md"
    
    if instructions_file.exists():
        with open(instructions_file, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        # Fallback if claude.md doesn't exist
        return (
            "You are a scientific writing assistant. Follow best practices for "
            "scientific communication and always present a plan before execution."
        )


def ensure_output_folder(cwd):
    """Ensure the paper_outputs folder exists."""
    output_folder = cwd / "paper_outputs"
    output_folder.mkdir(exist_ok=True)
    return output_folder


def get_image_extensions():
    """Return a set of common image file extensions."""
    return {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif', '.svg', '.webp', '.ico'}


def get_data_files(cwd):
    """Get all files from the data folder."""
    data_folder = cwd / "data"
    if not data_folder.exists():
        return []
    
    data_files = []
    for file_path in data_folder.iterdir():
        if file_path.is_file():
            data_files.append(file_path)
    
    return data_files


def process_data_files(cwd, data_files, paper_output_path):
    """
    Process data files by copying them to the paper output folder.
    Images go to figures/, other files go to data/.
    Returns a dictionary with information about processed files.
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
            
            # Delete the original file after successful copy
            file_path.unlink()
            
        except Exception as e:
            print(f"Warning: Could not process {file_name}: {str(e)}")
    
    return processed_info


def create_data_context_message(processed_info):
    """Create a context message about available data files."""
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


async def main():
    """Main CLI loop for the scientific writer."""
    # Get API key (verify it exists)
    get_api_key()
    
    # Get the current working directory (project root)
    cwd = Path(__file__).parent.absolute()
    
    # Ensure paper_outputs folder exists
    output_folder = ensure_output_folder(cwd)
    
    # Load system instructions from claude.md
    system_instructions = load_system_instructions(cwd)
    
    # Add conversation continuity instruction
    system_instructions += "\n\n" + """
IMPORTANT - CONVERSATION CONTINUITY:
When working in a chat session, you MUST continue editing the same paper across multiple messages.
- If a paper has already been started in this session, subsequent messages should edit that same paper
- Do NOT create a new paper directory unless explicitly asked to start a new paper
- Track the current working directory and continue work there
- If the user asks to modify, improve, or add to content, work on the existing paper
- Only start a new paper if the user explicitly says "new paper", "start a new paper", or gives a completely unrelated topic
"""
    
    # Configure the Claude agent options
    options = ClaudeAgentOptions(
        system_prompt=system_instructions,
        model="claude-sonnet-4-20250514",  # Always use Claude Sonnet 4.5
        allowed_tools=["Read", "Write", "Edit", "Bash", "research-lookup"],  # Default Claude Code tools + research lookup
        permission_mode="bypassPermissions",  # Execute immediately without approval prompts
        setting_sources=["project"],  # Load skills from .claude/skills/
        cwd=str(cwd),  # Set working directory to project root
    )
    
    # Track conversation state
    current_paper_path = None
    conversation_history = []
    
    # Print welcome message
    print("=" * 70)
    print("Scientific Writer CLI - Powered by Claude Sonnet 4.5")
    print("=" * 70)
    print("\nWelcome! I'm your scientific writing assistant.")
    print("\nI can help you with:")
    print("  • Writing scientific papers (IMRaD structure)")
    print("  • Literature reviews and citation management")
    print("  • Peer review feedback")
    print("  • Real-time research lookup using Perplexity Sonar Pro")
    print("  • Document manipulation (docx, pdf, pptx, xlsx)")
    print("\n📋 Workflow:")
    print("  1. I'll present a brief plan and immediately start execution")
    print("  2. I'll provide continuous updates during the process")
    print("  3. All outputs saved to: paper_outputs/<timestamp_description>/")
    print("  4. Progress tracked in real-time in progress.md")
    print(f"\n📁 Output folder: {output_folder}")
    print(f"\n📦 Data Files:")
    print("  • Place files in the 'data/' folder to include them in your paper")
    print("  • Data files → copied to paper's data/ folder")
    print("  • Images → copied to paper's figures/ folder")
    print("  • Original files are automatically deleted after copying")
    print("\n💡 Chat Session Tips:")
    print("  • Subsequent messages will continue editing the same paper")
    print("  • Say 'new paper' or 'start fresh' to begin a different paper")
    print("\nType 'exit' or 'quit' to end the session.")
    print("Type 'help' for usage tips.")
    print("=" * 70)
    print()
    
    # Main loop
    while True:
        try:
            # Get user input
            user_input = input("\n> ").strip()
            
            # Handle special commands
            if user_input.lower() in ["exit", "quit"]:
                print("\nThank you for using Scientific Writer CLI. Goodbye!")
                break
            
            if user_input.lower() == "help":
                print("\n" + "=" * 70)
                print("HELP - Scientific Writer CLI")
                print("=" * 70)
                print("\n📝 What I Can Do:")
                print("  • Create complete scientific papers (LaTeX, Word, Markdown)")
                print("  • Literature reviews with citation management")
                print("  • Peer review feedback on drafts")
                print("  • Real-time research lookup using Perplexity Sonar Pro")
                print("  • Format citations in any style (APA, IEEE, Nature, etc.)")
                print("  • Document manipulation (docx, pdf, pptx, xlsx)")
                print("\n🔄 How I Work:")
                print("  1. You describe what you need")
                print("  2. I present a brief plan and start execution immediately")
                print("  3. I provide continuous progress updates")
                print("  4. All files organized in paper_outputs/ folder")
                print("\n💡 Example Requests:")
                print("  'Create a NeurIPS paper on transformer attention mechanisms'")
                print("  'Write a literature review on CRISPR gene editing'")
                print("  'Review my methods section in draft.docx'")
                print("  'Research recent advances in quantum computing 2024'")
                print("  'Create a Nature paper on climate change impacts'")
                print("  'Format 20 citations in IEEE style'")
                print("\n📁 File Organization:")
                print("  All work saved to: paper_outputs/<timestamp>_<description>/")
                print("  - drafts/ - Working versions")
                print("  - final/ - Completed documents")
                print("  - references/ - Bibliography files")
                print("  - figures/ - Images and charts")
                print("  - data/ - Data files for the paper")
                print("  - progress.md - Real-time progress log")
                print("  - SUMMARY.md - Project summary and instructions")
                print("\n📦 Data Files:")
                print("  Place files in the 'data/' folder at project root:")
                print("  • Data files (csv, txt, json, etc.) → copied to paper's data/")
                print("  • Images (png, jpg, svg, etc.) → copied to paper's figures/")
                print("  • Files are used as context for the paper")
                print("  • Original files automatically deleted after copying")
                print("\n🎯 Pro Tips:")
                print("  • Be specific about journal/conference (e.g., 'Nature', 'NeurIPS')")
                print("  • Mention citation style if you have a preference")
                print("  • I'll make smart defaults if you don't specify details")
                print("  • Check progress.md for detailed execution logs")
                print("\n🔄 Conversation Continuity:")
                print("  • Subsequent messages continue editing the same paper")
                print("  • Say 'new paper' or 'start fresh' to begin a different paper")
                print("  • I'll track your current working paper automatically")
                print("=" * 70)
                continue
            
            if not user_input:
                continue
            
            # Check if user wants to start a new paper
            new_paper_keywords = ["new paper", "start fresh", "create new", "different paper", "another paper"]
            is_new_paper_request = any(keyword in user_input.lower() for keyword in new_paper_keywords)
            
            # Check for data files and process them if we have a current paper
            data_context = ""
            data_files = get_data_files(cwd)
            
            if data_files and current_paper_path and not is_new_paper_request:
                print(f"\n📦 Found {len(data_files)} file(s) in data folder. Processing...")
                processed_info = process_data_files(cwd, data_files, current_paper_path)
                if processed_info:
                    data_context = create_data_context_message(processed_info)
                    data_count = len(processed_info['data_files'])
                    image_count = len(processed_info['image_files'])
                    if data_count > 0:
                        print(f"   ✓ Copied {data_count} data file(s) to data/")
                    if image_count > 0:
                        print(f"   ✓ Copied {image_count} image(s) to figures/")
                    print("   ✓ Deleted original files from data folder\n")
            elif data_files and not current_paper_path:
                # Store data files info for later processing once paper is created
                print(f"\n📦 Found {len(data_files)} file(s) in data folder.")
                print("   They will be processed once the paper directory is created.\n")
            
            # Build contextual prompt
            contextual_prompt = user_input
            
            # Add context about current paper if one exists and not starting new
            if current_paper_path and not is_new_paper_request:
                contextual_prompt = f"""[CONTEXT: You are currently working on a paper in: {current_paper_path}]
[INSTRUCTION: Continue editing this existing paper. Do NOT create a new paper directory.]
{data_context}
User request: {user_input}"""
            elif is_new_paper_request:
                # Reset paper tracking when explicitly starting new
                current_paper_path = None
                print("📝 Starting a new paper...\n")
            
            # Send query to Claude
            print()  # Add blank line before response
            async for message in query(prompt=contextual_prompt, options=options):
                # Handle AssistantMessage with content blocks
                if hasattr(message, "content") and message.content:
                    for block in message.content:
                        if hasattr(block, "text"):
                            print(block.text, end="", flush=True)
            
            print()  # Add blank line after response
            
            # Try to detect if a new paper directory was created
            if not current_paper_path or is_new_paper_request:
                # Look for the most recently modified directory in paper_outputs
                try:
                    paper_dirs = [d for d in output_folder.iterdir() if d.is_dir()]
                    if paper_dirs:
                        most_recent = max(paper_dirs, key=lambda d: d.stat().st_mtime)
                        current_paper_path = str(most_recent)
                        print(f"\n📂 Working on: {most_recent.name}")
                        
                        # Process any remaining data files now that we have a paper path
                        remaining_data_files = get_data_files(cwd)
                        if remaining_data_files:
                            print(f"\n📦 Processing {len(remaining_data_files)} data file(s)...")
                            processed_info = process_data_files(cwd, remaining_data_files, current_paper_path)
                            if processed_info:
                                data_count = len(processed_info['data_files'])
                                image_count = len(processed_info['image_files'])
                                if data_count > 0:
                                    print(f"   ✓ Copied {data_count} data file(s) to data/")
                                if image_count > 0:
                                    print(f"   ✓ Copied {image_count} image(s) to figures/")
                                print("   ✓ Deleted original files from data folder")
                except Exception:
                    pass  # Silently fail if we can't detect the directory
            
        except KeyboardInterrupt:
            print("\n\nInterrupted. Type 'exit' to quit or continue with a new prompt.")
            continue
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again or type 'exit' to quit.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)

