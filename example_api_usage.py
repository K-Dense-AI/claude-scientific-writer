#!/usr/bin/env python3
"""
Example: Using the Scientific Writer programmatic API

This example demonstrates how to use the scientific_writer package
to generate papers programmatically in your own Python code.

Make sure you have set your ANTHROPIC_API_KEY environment variable
or pass it as a parameter to generate_paper().
"""

import asyncio
import json
from scientific_writer import generate_paper


async def simple_example():
    """Simple example: Generate a paper with live text streaming."""
    print("=" * 70)
    print("Simple Example: Generate a Paper with Live Text Streaming")
    print("=" * 70)
    print()
    
    query = "Create a short 2-page LaTeX paper on quantum computing basics"
    
    async for update in generate_paper(query):
        if update["type"] == "text":
            # Stream Scientific-Writer's live text output
            print(update["content"], end="", flush=True)
        elif update["type"] == "progress":
            # Print progress updates on new line
            print(f"\n[{update['stage']:12s}] {update['message']}")
        elif update["type"] == "result":
            # Final result
            print("\n" + "=" * 70)
            print("Paper Generation Complete!")
            print("=" * 70)
            print(f"\n✓ Status: {update['status']}")
            print(f"✓ Directory: {update['paper_directory']}")
            print(f"✓ Paper name: {update['paper_name']}")
            
            if update['files']['pdf_final']:
                print(f"\n📄 Final PDF: {update['files']['pdf_final']}")
            if update['files']['tex_final']:
                print(f"📝 Final TeX: {update['files']['tex_final']}")
            
            print(f"\n📚 Citations: {update['citations']['count']}")
            print(f"🖼️  Figures: {update['figures_count']}")
            
            if update['metadata']['word_count']:
                print(f"📊 Word count: {update['metadata']['word_count']}")


async def progress_only_example():
    """Example: Show only progress updates, ignore text streaming."""
    print("=" * 70)
    print("Progress-Only Example: Structured Updates Without Text")
    print("=" * 70)
    print()
    
    query = "Create a short paper on machine learning basics"
    
    async for update in generate_paper(query):
        if update["type"] == "text":
            # Skip text updates - only show progress
            pass
        elif update["type"] == "progress":
            print(f"[{update['stage']:12s}] {update['message']}")
        elif update["type"] == "result":
            print(f"\n✓ Done! PDF: {update['files']['pdf_final']}")


async def advanced_example():
    """Advanced example: Generate with custom options and save result to JSON."""
    print("=" * 70)
    print("Advanced Example: Custom Options + JSON Export")
    print("=" * 70)
    print()
    
    # You can provide custom data files
    data_files = []  # Add your files here: ["data.csv", "figure.png"]
    
    query = "Create a NeurIPS paper on transformer attention mechanisms"
    
    result_data = None
    
    async for update in generate_paper(
        query=query,
        output_dir="./my_custom_papers",  # Custom output directory
        data_files=data_files,
        model="claude-sonnet-4-20250514"
    ):
        if update["type"] == "text":
            # Stream live output
            print(update["content"], end="", flush=True)
        elif update["type"] == "progress":
            print(f"\n[{update['stage']:12s}] {update['message']}")
        elif update["type"] == "result":
            result_data = update
    
    if result_data:
        # Save the complete result to JSON for later reference
        output_file = "paper_result.json"
        with open(output_file, "w") as f:
            json.dump(result_data, f, indent=2)
        
        print(f"\n✓ Result saved to: {output_file}")
        print(f"✓ Paper directory: {result_data['paper_directory']}")


async def error_handling_example():
    """Example: Proper error handling with text streaming."""
    print("=" * 70)
    print("Error Handling Example")
    print("=" * 70)
    print()
    
    try:
        query = "Create a conference paper on machine learning"
        
        async for update in generate_paper(query):
            if update["type"] == "text":
                print(update["content"], end="", flush=True)
            elif update["type"] == "progress":
                print(f"\n[{update['stage']:12s}] {update['message']}")
            elif update["type"] == "result":
                # Check for errors
                if update['status'] == 'failed':
                    print(f"\n❌ Paper generation failed!")
                    if update['errors']:
                        print(f"Errors: {update['errors']}")
                elif update['status'] == 'partial':
                    print(f"\n⚠️  Partial success - TeX created but PDF compilation failed")
                    print(f"TeX file: {update['files']['tex_final']}")
                else:
                    print(f"\n✓ Success! PDF: {update['files']['pdf_final']}")
    
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Make sure ANTHROPIC_API_KEY is set!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def token_tracking_example():
    """Example: Track token usage with text streaming."""
    print("=" * 70)
    print("Token Tracking Example")
    print("=" * 70)
    print()
    
    query = "Create a short abstract on neural networks"
    
    async for update in generate_paper(query, track_token_usage=True):
        if update["type"] == "text":
            print(update["content"], end="", flush=True)
        elif update["type"] == "progress":
            print(f"\n[{update['stage']:12s}] {update['message']}")
        elif update["type"] == "result":
            print(f"\n✓ Status: {update['status']}")
            
            # Show token usage
            if "token_usage" in update:
                usage = update["token_usage"]
                print(f"\n📊 Token Usage:")
                print(f"   Input tokens: {usage['input_tokens']}")
                print(f"   Output tokens: {usage['output_tokens']}")
                print(f"   Total tokens: {usage['total_tokens']}")


async def main():
    """Run the examples."""
    print("\nScientific Writer - Programmatic API Examples\n")
    print("Choose an example to run:")
    print("  1. Simple example (live text streaming)")
    print("  2. Progress-only example (structured updates)")
    print("  3. Advanced example (custom options + JSON export)")
    print("  4. Error handling example")
    print("  5. Token tracking example")
    print("  0. Run all examples")
    print()
    
    # For demonstration, we'll just print instructions
    # Uncomment the following to actually run examples:
    
    # choice = input("Enter choice (0-5): ").strip()
    # 
    # if choice == "1":
    #     await simple_example()
    # elif choice == "2":
    #     await progress_only_example()
    # elif choice == "3":
    #     await advanced_example()
    # elif choice == "4":
    #     await error_handling_example()
    # elif choice == "5":
    #     await token_tracking_example()
    # elif choice == "0":
    #     await simple_example()
    #     print("\n\n")
    #     await progress_only_example()
    #     print("\n\n")
    #     await advanced_example()
    #     print("\n\n")
    #     await error_handling_example()
    #     print("\n\n")
    #     await token_tracking_example()
    
    print("NOTE: To actually run examples, uncomment the code in main()")
    print("      and ensure ANTHROPIC_API_KEY is set in your environment.")
    print()
    print("Quick start:")
    print("  1. Set your API key: export ANTHROPIC_API_KEY='your_key'")
    print("  2. Edit this file and uncomment the example code")
    print("  3. Run: python example_api_usage.py")
    print()
    print("Update Types:")
    print("  - 'text': Live streaming of Scientific-Writer's responses (content field)")
    print("  - 'progress': Structured stage updates (stage, message fields)")
    print("  - 'result': Final result with all paper details")


if __name__ == "__main__":
    asyncio.run(main())
