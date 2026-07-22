#!/usr/bin/env python3
"""
Scientific Writer CLI Tool
A command-line interface for scientific writing.
"""

import argparse
import os
import sys
import asyncio
from pathlib import Path
from typing import Literal
from dotenv import load_dotenv

from claude_agent_sdk import query, ClaudeAgentOptions
from claude_agent_sdk.types import HookEvent, HookMatcher

from .core import (
    EFFORT_LEVEL_MODELS,
    create_completion_check_stop_hook,
    create_output_project,
    get_api_key,
    load_system_instructions,
    ensure_output_folder,
    get_data_files,
    process_data_files,
    create_data_context_message,
    resolve_auto_continue,
    setup_claude_skills,
)
from .utils import find_existing_papers, detect_paper_reference, scan_paper_directory
from .models import TokenUsage


PermissionMode = Literal[
    "default",
    "acceptEdits",
    "plan",
    "bypassPermissions",
    "dontAsk",
    "auto",
]


def _resolve_model(effort_level: str = "medium") -> str:
    """Resolve the Claude model for an effort level, defaulting to medium."""
    return EFFORT_LEVEL_MODELS.get(effort_level, EFFORT_LEVEL_MODELS["medium"])


def _input_signature(path: Path) -> tuple[int, int]:
    stat = path.stat()
    return stat.st_size, stat.st_mtime_ns


def _remember_processed_inputs(
    processed_info: dict | None,
    signatures: dict[Path, tuple[int, int]],
) -> None:
    """Avoid re-importing unchanged inbox files on every interactive prompt."""
    if not processed_info:
        return
    for record in processed_info.get("all_files", []):
        original = Path(record["original"])
        if original.is_file():
            signatures[original.resolve()] = _input_signature(original)


async def main(
    track_token_usage: bool = False,
    effort_level: Literal["low", "medium", "high"] = "medium",
    permission_mode: PermissionMode = "bypassPermissions",
    max_turns: int = 500,
    max_budget_usd: float | None = None,
    max_auto_continuations: int = 1,
    consume_inputs: bool = False,
) -> TokenUsage | None:
    """
    Main CLI loop for the scientific writer.

    Args:
        track_token_usage: If True, track and return token usage statistics
        effort_level: Effort level ("low", "medium", "high") that selects the model
        permission_mode: Claude Agent SDK permission mode
        max_turns: Maximum SDK turns per query
        max_budget_usd: Optional SDK budget ceiling per query
        max_auto_continuations: Bounded completion-verification passes
        consume_inputs: Delete source files after they are safely copied

    Returns:
        TokenUsage object if track_token_usage is True, None otherwise
    """
    # Explicitly load .env file from current working directory
    # This ensures API keys are available in the shell environment
    cwd_resolved = Path.cwd().resolve()
    env_file = cwd_resolved / ".env"
    if env_file.exists():
        load_dotenv(dotenv_path=env_file, override=False)

    # Get API key (verify it exists)
    try:
        resolved_api_key = get_api_key()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Get the current working directory (user's directory) and package directory
    # Capture and resolve the current working directory at CLI invocation time
    cwd = Path.cwd().resolve()  # User's current working directory (absolute path)
    package_dir = Path(__file__).parent.absolute()  # Package installation directory (scientific_writer/)

    # Set up Claude skills in the working directory (includes WRITER.md)
    setup_claude_skills(package_dir, cwd)

    # Ensure writing_outputs folder exists in user's directory
    output_folder = ensure_output_folder(cwd)

    # Load system instructions from .claude/WRITER.md in working directory
    system_instructions = load_system_instructions(cwd)

    # Add conversation continuity instruction
    # Note: The Python CLI handles session tracking via current_paper_path
    # These instructions only apply WITHIN a single CLI session, not across different chat sessions
    system_instructions += "\n\n" + f"""
IMPORTANT - WORKING DIRECTORY:
- Your working directory is: {cwd}
- ALWAYS create writing_outputs folder in this directory: {cwd}/writing_outputs/
- NEVER write to /tmp/ or any other temporary directory
- All paper outputs MUST go to: {cwd}/writing_outputs/<timestamp>_<description>/

IMPORTANT - CONVERSATION CONTINUITY:
- The user will provide context in their prompt if they want to continue working on an existing paper
- If the prompt includes [CONTEXT: You are currently working on a paper in: ...], continue editing that paper
- If no such context is provided, this is a NEW paper request - create a new paper directory
- Do NOT assume there's an existing paper unless explicitly told in the prompt context
- Each new chat session should start with a new paper unless context says otherwise
"""

    auto_continue = resolve_auto_continue(True)
    hooks: dict[HookEvent, list[HookMatcher]] | None = None
    if auto_continue:
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
        model=_resolve_model(effort_level),
        effort=effort_level,
        allowed_tools=["Read", "Write", "Edit", "Bash", "WebSearch"],
        permission_mode=permission_mode,
        setting_sources=["project"],
        skills="all",
        cwd=str(cwd),
        max_turns=max_turns,
        max_budget_usd=max_budget_usd,
        env={**os.environ, "ANTHROPIC_API_KEY": resolved_api_key},
        hooks=hooks,
    )

    # Track conversation state
    current_paper_path = None
    processed_input_signatures: dict[Path, tuple[int, int]] = {}

    # Token usage tracking (accumulated across all queries in session)
    total_usage = TokenUsage()

    # Print welcome message
    print("=" * 70)
    print("Scientific Writer CLI")
    print("=" * 70)
    print("\nWelcome! I'm your scientific writing assistant.")
    print("\nI can help you with:")
    print("  • Writing scientific papers (IMRaD structure)")
    print("  • Literature reviews and citation management")
    print("  • Peer review feedback")
    print("  • Real-time research lookup using Parallel web search")
    print("  • Native web search for current information")
    print("  • Document manipulation (docx, pdf, pptx, xlsx)")
    print("\n📋 Workflow:")
    print("  1. I'll present a brief plan and immediately start execution")
    print("  2. I'll provide continuous updates during the process")
    print("  3. All outputs saved to: writing_outputs/<timestamp_description>/")
    print("  4. Progress tracked in real-time in progress.md")
    print(f"\n📁 Working directory: {cwd}")
    print(f"📁 Output folder: {output_folder}")
    print("\n📦 Data Files:")
    print("  • Place files in the 'data/' folder to include them in your paper")
    print("  • Manuscript files (.tex) → copied to drafts/ for EDITING")
    print("  • Context files (.md, .docx, .pdf) → copied to sources/ for REFERENCE")
    print("  • Data files (csv, txt, json, etc.) → copied to paper's data/ folder")
    print("  • Images (png, jpg, svg, etc.) → copied to paper's figures/ folder")
    print("  • Other files → copied to sources/ for CONTEXT")
    print("  • Original files are preserved by default")
    print("\n🤖 Intelligent Paper Detection:")
    print("  • I automatically detect when you're referring to a previous paper/presentation")
    print("  • Continue: 'continue', 'update', 'edit', 'the paper', 'the presentation', etc.")
    print("  • Search: 'look for', 'find', 'show me', 'where is', etc.")
    print("  • Or reference the topic (e.g., 'find the acoustics paper')")
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
                if track_token_usage:
                    return total_usage
                return None

            if user_input.lower() == "help":
                _print_help()
                continue

            if not user_input:
                continue

            # Get all existing papers
            existing_papers = find_existing_papers(output_folder)

            # Check if user wants to start a new paper
            new_paper_keywords = [
                "new paper", "start fresh", "start afresh", "create new", "different paper", "another paper",
                "new presentation", "new poster", "different presentation", "another presentation"
            ]
            is_new_paper_request = any(keyword in user_input.lower() for keyword in new_paper_keywords)

            # Try to detect reference to existing paper
            detected_paper_path = None
            if not is_new_paper_request:
                detected_paper_path = detect_paper_reference(user_input, existing_papers)

                # If we detected a paper reference and it's different from current, update it
                if detected_paper_path and str(detected_paper_path) != current_paper_path:
                    current_paper_path = str(detected_paper_path)
                    print(f"\n🔍 Detected reference to existing paper: {detected_paper_path.name}")
                    print(f"📂 Working on: {current_paper_path}")

                    # Show what files exist in this paper
                    paper_info = scan_paper_directory(detected_paper_path)
                    file_count = sum([
                        1 if paper_info['tex_final'] else 0,
                        1 if paper_info['pdf_final'] else 0,
                        len(paper_info['tex_drafts']),
                        len(paper_info['pdf_drafts']),
                        len(paper_info['figures']),
                        len(paper_info['data']),
                        len(paper_info['sources']),
                        1 if paper_info['bibliography'] else 0,
                        1 if paper_info['progress_log'] else 0,
                        1 if paper_info['summary'] else 0,
                    ])
                    print(f"📄 Found {file_count} file(s) in this directory\n")

                elif detected_paper_path and str(detected_paper_path) == current_paper_path:
                    # Already working on the right paper, just confirm
                    print(f"📂 Continuing with: {Path(current_paper_path).name}\n")

            # Check for data files and process them if we have a current paper
            data_context = ""
            data_files = [
                path
                for path in get_data_files(cwd)
                if processed_input_signatures.get(path.resolve()) != _input_signature(path)
            ]

            # PHASE 1: Handle new paper with data files - create directory first
            if data_files and not current_paper_path and (is_new_paper_request or not current_paper_path):
                print(f"\n📦 Found {len(data_files)} file(s) in data folder.")
                print("📝 Starting a new paper...")
                print("⏳ Step 1/2: Creating paper directory...\n")

                project_dir = create_output_project(output_folder, user_input)
                current_paper_path = str(project_dir)
                print(f"✓ Directory created: {project_dir.name}\n")

                # PHASE 2: Process data files before continuing
                if current_paper_path:
                    print("⏳ Step 2/2: Processing and copying data files...")
                    processed_info = process_data_files(
                        cwd,
                        data_files,
                        current_paper_path,
                        delete_originals=consume_inputs,
                    )
                    if processed_info:
                        _remember_processed_inputs(processed_info, processed_input_signatures)
                        data_context = create_data_context_message(processed_info)
                        manuscript_count = len(processed_info.get('manuscript_files', []))
                        source_count = len(processed_info.get('source_files', []))
                        data_count = len(processed_info.get('data_files', []))
                        image_count = len(processed_info.get('image_files', []))
                        if manuscript_count > 0:
                            print(f"   ✓ Copied {manuscript_count} .tex manuscript(s) to drafts/ [EDITING MODE]")
                        if source_count > 0:
                            print(f"   ✓ Copied {source_count} source/context file(s) to sources/")
                        if data_count > 0:
                            print(f"   ✓ Copied {data_count} data file(s) to data/")
                        if image_count > 0:
                            print(f"   ✓ Copied {image_count} image(s) to figures/")
                        action = "Removed" if consume_inputs else "Preserved"
                        print(f"   ✓ {action} original files in data folder\n")
                        print("✅ Files processed. Now starting paper generation...\n")

                # Update prompt to continue with paper generation
                contextual_prompt = f"""[CONTEXT: You are working on a paper in: {current_paper_path}]
[FILES HAVE BEEN PROCESSED AND COPIED - see details below]
{data_context}

Now continue with the actual paper generation for the user's request:
{user_input}"""

            elif data_files and current_paper_path and not is_new_paper_request:
                # Existing paper with data files - process immediately
                print(f"📦 Found {len(data_files)} file(s) in data folder. Processing...")
                processed_info = process_data_files(
                    cwd,
                    data_files,
                    current_paper_path,
                    delete_originals=consume_inputs,
                )
                if processed_info:
                    _remember_processed_inputs(processed_info, processed_input_signatures)
                    data_context = create_data_context_message(processed_info)
                    manuscript_count = len(processed_info.get('manuscript_files', []))
                    source_count = len(processed_info.get('source_files', []))
                    data_count = len(processed_info.get('data_files', []))
                    image_count = len(processed_info.get('image_files', []))
                    if manuscript_count > 0:
                        print(f"   ✓ Copied {manuscript_count} .tex manuscript(s) to drafts/ [EDITING MODE]")
                    if source_count > 0:
                        print(f"   ✓ Copied {source_count} source/context file(s) to sources/")
                    if data_count > 0:
                        print(f"   ✓ Copied {data_count} data file(s) to data/")
                    if image_count > 0:
                        print(f"   ✓ Copied {image_count} image(s) to figures/")
                    action = "Removed" if consume_inputs else "Preserved"
                    print(f"   ✓ {action} original files in data folder\n")

                # Build contextual prompt for existing paper
                contextual_prompt = f"""[CONTEXT: You are currently working on a paper in: {current_paper_path}]
[INSTRUCTION: Continue editing this existing paper. Do NOT create a new paper directory.]
{data_context}
User request: {user_input}"""

            elif is_new_paper_request and not data_files:
                # New document without input files.
                project_dir = create_output_project(output_folder, user_input)
                current_paper_path = str(project_dir)
                print("📝 Starting a new paper...\n")
                contextual_prompt = f"""[CONTEXT: Work only in {current_paper_path}]
[INSTRUCTION: The project directory already exists. Do not create another one.]
User request: {user_input}"""

            elif current_paper_path and not data_files:
                # Detected existing paper without new data files - provide context about what exists
                paper_info = scan_paper_directory(Path(current_paper_path))

                # Build a context message about the paper's current state
                context_parts = [
                    f"[CONTEXT: You are currently working on a paper in: {current_paper_path}]",
                    "[INSTRUCTION: Continue working on this existing paper. Do NOT create a new paper directory.]",
                    "\n📁 Current paper contents:"
                ]

                # Add information about what files exist
                if paper_info['tex_final']:
                    context_parts.append(f"  • Final LaTeX: {Path(paper_info['tex_final']).name}")
                if paper_info['pdf_final']:
                    context_parts.append(f"  • Final PDF: {Path(paper_info['pdf_final']).name}")
                if paper_info['tex_drafts']:
                    context_parts.append(f"  • Draft LaTeX files: {len(paper_info['tex_drafts'])} file(s)")
                    for draft in paper_info['tex_drafts']:
                        context_parts.append(f"    - {Path(draft).name}")
                if paper_info['pdf_drafts']:
                    context_parts.append(f"  • Draft PDF files: {len(paper_info['pdf_drafts'])} file(s)")
                if paper_info['figures']:
                    context_parts.append(f"  • Figures: {len(paper_info['figures'])} file(s)")
                if paper_info['data']:
                    context_parts.append(f"  • Data files: {len(paper_info['data'])} file(s)")
                if paper_info['sources']:
                    context_parts.append(f"  • Source/context files: {len(paper_info['sources'])} file(s)")
                if paper_info['bibliography']:
                    context_parts.append(f"  • Bibliography: {Path(paper_info['bibliography']).name}")
                if paper_info['progress_log']:
                    context_parts.append("  • Progress log: progress.md")
                if paper_info['summary']:
                    context_parts.append("  • Summary: SUMMARY.md")

                context_parts.append(f"\nUser request: {user_input}")
                contextual_prompt = "\n".join(context_parts)

            else:
                # No existing document was referenced: create an invocation-owned project.
                project_dir = create_output_project(output_folder, user_input)
                current_paper_path = str(project_dir)
                contextual_prompt = f"""[CONTEXT: Work only in {current_paper_path}]
[INSTRUCTION: The project directory already exists. Do not create another one.]
User request: {user_input}"""

            # Send query
            print()  # Add blank line before response
            async for message in query(prompt=contextual_prompt, options=options):
                if track_token_usage and hasattr(message, "usage") and message.usage:
                    total_usage.add_usage(message.usage)

                # Handle AssistantMessage with content blocks
                if hasattr(message, "content") and message.content:
                    for block in message.content:
                        if hasattr(block, "text"):
                            print(block.text, end="", flush=True)

            print()  # Add blank line after response

        except KeyboardInterrupt:
            print("\n\nInterrupted. Type 'exit' to quit or continue with a new prompt.")
            continue
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again or type 'exit' to quit.")

    # Return token usage if tracking was enabled (fallback for any exit path)
    if track_token_usage:
        return total_usage
    return None


def _print_help():
    """Print help information."""
    print("\n" + "=" * 70)
    print("HELP - Scientific Writer CLI")
    print("=" * 70)
    print("\n📝 What I Can Do:")
    print("  • Create complete scientific papers (LaTeX, Word, Markdown)")
    print("  • Literature reviews with citation management")
    print("  • Peer review feedback on drafts")
    print("  • Real-time research lookup using Parallel web search")
    print("  • Native web search for current events and general information")
    print("  • Format citations in any style (APA, IEEE, Nature, etc.)")
    print("  • Document manipulation (docx, pdf, pptx, xlsx)")
    print("\n🔄 How I Work:")
    print("  1. You describe what you need")
    print("  2. I present a brief plan and start execution immediately")
    print("  3. I provide continuous progress updates")
    print("  4. All files organized in writing_outputs/ folder")
    print("\n💡 Example Requests:")
    print("  'Create a NeurIPS paper on transformer attention mechanisms'")
    print("  'Write a literature review on CRISPR gene editing'")
    print("  'Review my methods section in draft.docx'")
    print("  'Research recent advances in quantum computing 2024'")
    print("  'Create a Nature paper on climate change impacts'")
    print("  'Format 20 citations in IEEE style'")
    print("\n📁 File Organization:")
    print("  All work saved to: writing_outputs/<timestamp>_<description>/")
    print("  - drafts/ - Working versions")
    print("  - final/ - Completed documents")
    print("  - references/ - Bibliography files")
    print("  - figures/ - Images and charts")
    print("  - data/ - Data files for the paper")
    print("  - sources/ - Context/reference materials")
    print("  - progress.md - Real-time progress log")
    print("  - SUMMARY.md - Project summary and instructions")
    print("\n📦 Data Files:")
    print("  Place files in the 'data/' folder at project root:")
    print("  • Manuscript files (.tex) → copied to drafts/ for EDITING")
    print("  • Context files (.md, .docx, .pdf) → copied to sources/ for REFERENCE")
    print("  • Data files (csv, txt, json, etc.) → copied to paper's data/")
    print("  • Images (png, jpg, svg, etc.) → copied to paper's figures/")
    print("  • Other files → copied to sources/ for CONTEXT")
    print("  • Files are used as context for the paper")
    print("  • Original files are preserved unless --consume-inputs is used")
    print("\n🎯 Pro Tips:")
    print("  • Be specific about journal/conference (e.g., 'Nature', 'NeurIPS')")
    print("  • Mention citation style if you have a preference")
    print("  • I'll make smart defaults if you don't specify details")
    print("  • Check progress.md for detailed execution logs")
    print("\n🔄 Intelligent Paper Detection:")
    print("  • I automatically detect when you're referring to a previous paper/presentation")
    print("  • Continue working: 'continue the paper', 'update my presentation', 'edit the poster'")
    print("  • Search/find: 'look for the X paper', 'find the presentation about Y'")
    print("  • Or mention the topic: 'show me the acoustics paper'")
    print("  • Keywords like 'continue', 'update', 'edit', 'look for', 'find' trigger detection")
    print("  • I'll find the most relevant paper/presentation based on topic matching")
    print("  • Say 'new paper' or 'start fresh' to explicitly begin a new one")
    print("  • Current working paper/presentation is tracked throughout the session")
    print("=" * 70)


def cli_main():
    """Entry point for the CLI script."""
    parser = argparse.ArgumentParser(
        prog="scientific-writer",
        description="Deep research and scientific writing assistant.",
    )
    parser.add_argument(
        "--effort",
        choices=sorted(EFFORT_LEVEL_MODELS),
        default="medium",
        help="reasoning effort and default model tier (default: medium)",
    )
    parser.add_argument(
        "--track-token-usage",
        action="store_true",
        help="print aggregate token usage when the session exits",
    )
    parser.add_argument(
        "--permission-mode",
        choices=["default", "acceptEdits", "plan", "bypassPermissions", "dontAsk", "auto"],
        default="bypassPermissions",
        help="Claude Agent SDK permission mode (default: bypassPermissions)",
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        default=500,
        help="maximum SDK turns per request (default: 500)",
    )
    parser.add_argument(
        "--max-budget-usd",
        type=float,
        default=None,
        help="optional SDK budget ceiling per request",
    )
    parser.add_argument(
        "--max-auto-continuations",
        type=int,
        default=1,
        help="bounded completion-verification passes (default: 1)",
    )
    parser.add_argument(
        "--consume-inputs",
        action="store_true",
        help="delete files from data/ after a successful copy",
    )
    args = parser.parse_args()
    if args.max_turns <= 0:
        parser.error("--max-turns must be greater than zero")
    if args.max_budget_usd is not None and args.max_budget_usd <= 0:
        parser.error("--max-budget-usd must be greater than zero")
    if args.max_auto_continuations < 0:
        parser.error("--max-auto-continuations cannot be negative")
    try:
        usage = asyncio.run(
            main(
                track_token_usage=args.track_token_usage,
                effort_level=args.effort,
                permission_mode=args.permission_mode,
                max_turns=args.max_turns,
                max_budget_usd=args.max_budget_usd,
                max_auto_continuations=args.max_auto_continuations,
                consume_inputs=args.consume_inputs,
            )
        )
        if usage is not None:
            print(
                "Token usage: "
                f"input={usage.input_tokens:,}, "
                f"output={usage.output_tokens:,}, "
                f"total={usage.total_tokens:,}, "
                f"cache_read={usage.cache_read_input_tokens:,}"
            )
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)


if __name__ == "__main__":
    cli_main()

