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
    """Simple example: Generate a paper and print progress."""
    print("=" * 70)
    print("Simple Example: Generate a Paper")
    print("=" * 70)
    print()
    
    query = "Create a short 2-page LaTeX paper on quantum computing basics"
    
    async for update in generate_paper(query):
        if update["type"] == "progress":
            # Print progress updates
            print(f"[{update['percentage']:3d}%] [{update['stage']:15s}] {update['message']}")
        else:
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
        if update["type"] == "progress":
            print(f"[{update['stage']:15s}] {update['message']}")
        else:
            result_data = update
    
    if result_data:
        # Save the complete result to JSON for later reference
        output_file = "paper_result.json"
        with open(output_file, "w") as f:
            json.dump(result_data, f, indent=2)
        
        print(f"\n✓ Result saved to: {output_file}")
        print(f"✓ Paper directory: {result_data['paper_directory']}")


async def error_handling_example():
    """Example: Proper error handling."""
    print("=" * 70)
    print("Error Handling Example")
    print("=" * 70)
    print()
    
    try:
        query = "Create a conference paper on machine learning"
        
        async for update in generate_paper(query):
            if update["type"] == "progress":
                print(f"[{update['percentage']:3d}%] {update['message']}")
            else:
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


async def main():
    """Run the examples."""
    import sys
    
    print("\nScientific Writer - Programmatic API Examples\n")
    print("Choose an example to run:")
    print("  1. Simple example (basic usage)")
    print("  2. Advanced example (custom options + JSON export)")
    print("  3. Error handling example")
    print("  0. Run all examples")
    print()
    
    # For demonstration, we'll just print instructions
    # Uncomment the following to actually run examples:
    
    # choice = input("Enter choice (0-3): ").strip()
    # 
    # if choice == "1":
    #     await simple_example()
    # elif choice == "2":
    #     await advanced_example()
    # elif choice == "3":
    #     await error_handling_example()
    # elif choice == "0":
    #     await simple_example()
    #     print("\n\n")
    #     await advanced_example()
    #     print("\n\n")
    #     await error_handling_example()
    
    print("NOTE: To actually run examples, uncomment the code in main()")
    print("      and ensure ANTHROPIC_API_KEY is set in your environment.")
    print()
    print("Quick start:")
    print("  1. Set your API key: export ANTHROPIC_API_KEY='your_key'")
    print("  2. Edit this file and uncomment the example code")
    print("  3. Run: python example_api_usage.py")


if __name__ == "__main__":
    asyncio.run(main())

