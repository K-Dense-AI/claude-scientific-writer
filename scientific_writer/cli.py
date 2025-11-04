#!/usr/bin/env python3
"""
Scientific Writer CLI Tool
A command-line interface for scientific writing powered by Claude Code.
"""

import os
import sys
import time
import asyncio
from pathlib import Path
from typing import Optional

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
from .utils import find_existing_papers, detect_paper_reference


async def main():
    """Main CLI loop for the scientific writer."""
    # Get API key (verify it exists)
    try:
        get_api_key()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Get the current working directory (user's directory) and package directory
    cwd = Path.cwd()  # User's current working directory
    package_dir = Path(__file__).parent.absolute()  # Package installation directory (scientific_writer/)
    
    # Set up Claude skills in the working directory
    setup_claude_skills(package_dir, cwd)
    
    # Ensure paper_outputs folder exists in user's directory
    output_folder = ensure_output_folder(cwd)
    
    # Load system instructions from package CLAUDE.md
    system_instructions = load_system_instructions(package_dir)
    
    # Add conversation continuity instruction  
    # Note: The Python CLI handles session tracking via current_paper_path
    # These instructions only apply WITHIN a single CLI session, not across different chat sessions
    system_instructions += "\n\n" + """
IMPORTANT - CONVERSATION CONTINUITY:
- The user will provide context in their prompt if they want to continue working on an existing paper
- If the prompt includes [CONTEXT: You are currently working on a paper in: ...], continue editing that paper
- If no such context is provided, this is a NEW paper request - create a new paper directory
- Do NOT assume there's an existing paper unless explicitly told in the prompt context
- Each new chat session should start with a new paper unless context says otherwise
"""
    
    # Configure the Claude agent options
    options = ClaudeAgentOptions(
        system_prompt=system_instructions,
        model="claude-sonnet-4-20250514",  # Always use Claude Sonnet 4.5
        allowed_tools=["Read", "Write", "Edit", "Bash", "research-lookup"],  # Default Claude Code tools + research lookup
        permission_mode="bypassPermissions",  # Execute immediately without approval prompts
        setting_sources=["project"],  # Load skills from project .claude directory
        cwd=str(cwd),  # Set working directory to user's current directory
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
    print("\n🤖 Intelligent Paper Detection:")
    print("  • I automatically detect when you're referring to a previous paper")
    print("  • Continue: 'continue', 'update', 'edit', 'the paper', etc.")
    print("  • Search: 'look for', 'find', 'show me', 'where is', etc.")
    print("  • Or reference the paper topic (e.g., 'find the acoustics paper')")
    print("  • Say 'new paper' to explicitly start a fresh paper")
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
                _print_help()
                continue
            
            if not user_input:
                continue
            
            # Get all existing papers
            existing_papers = find_existing_papers(output_folder)
            
            # Check if user wants to start a new paper
            new_paper_keywords = ["new paper", "start fresh", "start afresh", "create new", "different paper", "another paper"]
            is_new_paper_request = any(keyword in user_input.lower() for keyword in new_paper_keywords)
            
            # Try to detect reference to existing paper
            detected_paper_path = None
            if not is_new_paper_request:
                detected_paper_path = detect_paper_reference(user_input, existing_papers)
                
                # If we detected a paper reference and it's different from current, update it
                if detected_paper_path and str(detected_paper_path) != current_paper_path:
                    current_paper_path = str(detected_paper_path)
                    print(f"\n🔍 Detected reference to existing paper: {detected_paper_path.name}")
                    print(f"📂 Working on: {current_paper_path}\n")
                elif detected_paper_path and str(detected_paper_path) == current_paper_path:
                    # Already working on the right paper, just confirm
                    print(f"📂 Continuing with: {Path(current_paper_path).name}\n")
            
            # Check for data files and process them if we have a current paper
            data_context = ""
            data_files = get_data_files(cwd)
            
            if data_files and current_paper_path and not is_new_paper_request:
                print(f"📦 Found {len(data_files)} file(s) in data folder. Processing...")
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
                # Only update if it was modified in the last 10 seconds (indicating it was just created)
                try:
                    paper_dirs = [d for d in output_folder.iterdir() if d.is_dir()]
                    if paper_dirs:
                        most_recent = max(paper_dirs, key=lambda d: d.stat().st_mtime)
                        time_since_modification = time.time() - most_recent.stat().st_mtime
                        
                        # Only set as current paper if it was modified very recently (within last 10 seconds)
                        if time_since_modification < 10:
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


def _print_help():
    """Print help information."""
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
    print("\n🔄 Intelligent Paper Detection:")
    print("  • I automatically detect when you're referring to a previous paper")
    print("  • Continue working: 'continue the paper', 'update my paper', 'edit the poster'")
    print("  • Search/find: 'look for the X paper', 'find the paper about Y'")
    print("  • Or mention the paper topic: 'show me the acoustics paper'")
    print("  • Keywords like 'continue', 'update', 'edit', 'look for', 'find' trigger detection")
    print("  • I'll find the most relevant paper based on topic matching")
    print("  • Say 'new paper' or 'start fresh' to explicitly begin a new one")
    print("  • Current working paper is tracked throughout the session")
    print("=" * 70)


def cli_main():
    """Entry point for the CLI script."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)


if __name__ == "__main__":
    cli_main()

