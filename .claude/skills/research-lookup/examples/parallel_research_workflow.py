#!/usr/bin/env python3
"""
Example: Parallel Research Workflow

This example demonstrates the complete workflow:
1. Identify research topics from input text
2. Save topics to file for review
3. Execute parallel research on all topics
4. Save comprehensive results

This approach is 5-10x faster than sequential research.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import research_lookup
sys.path.insert(0, str(Path(__file__).parent.parent))

from research_lookup import ResearchLookup


def example_1_complete_workflow():
    """Example 1: Complete workflow in one call"""
    print("="*80)
    print("Example 1: Complete Workflow (One Call)")
    print("="*80 + "\n")
    
    # Sample research proposal text
    text = """
    We propose to investigate the therapeutic potential of CRISPR-Cas9 gene editing
    for treating sickle cell disease. This research will examine recent clinical trials,
    delivery mechanisms, off-target effects, and regulatory considerations.
    
    Background research is needed on:
    - Current state of CRISPR clinical trials for blood disorders
    - Viral and non-viral delivery methods for hematopoietic stem cells
    - Long-term safety profiles in human patients
    - Comparison with traditional bone marrow transplantation
    - FDA and EMA approval pathways for gene editing therapies
    """
    
    research = ResearchLookup()
    
    # Execute complete workflow
    result = research.identify_and_research(
        text=text,
        topics_file="example_topics.txt",
        parallel=True,
        max_workers=5,
        output_file="example_results.json"
    )
    
    print(f"\n✓ Workflow complete!")
    print(f"  - Topics identified: {len(result['topics'])}")
    print(f"  - Successful queries: {result['successful_queries']}/{result['total_queries']}")
    print(f"  - Topics saved to: example_topics.txt")
    print(f"  - Results saved to: example_results.json")
    
    return result


def example_2_step_by_step():
    """Example 2: Step-by-step workflow with manual review"""
    print("\n" + "="*80)
    print("Example 2: Step-by-Step Workflow")
    print("="*80 + "\n")
    
    research = ResearchLookup()
    
    # Step 1: Identify topics
    print("STEP 1: Identify Research Topics")
    print("-" * 40)
    
    text = """
    This study will explore the use of mRNA vaccines for cancer immunotherapy.
    We need to understand the mechanism of action, compare efficacy with traditional
    vaccines, review clinical trial results, and assess manufacturing scalability.
    """
    
    topics = research.identify_research_topics(
        text=text,
        output_file="step_by_step_topics.txt"
    )
    
    print(f"\nIdentified {len(topics)} topics:")
    for i, topic in enumerate(topics, 1):
        print(f"  {i}. {topic}")
    
    # Step 2: Manual review (simulated)
    print("\n\nSTEP 2: Review and Edit Topics")
    print("-" * 40)
    print("(In practice, you would open step_by_step_topics.txt and edit)")
    print("For this example, we'll use the topics as-is.\n")
    
    # Step 3: Execute parallel research
    print("\nSTEP 3: Execute Parallel Research")
    print("-" * 40)
    
    results = research.parallel_lookup(
        queries=topics,
        max_workers=5
    )
    
    # Display summary
    successful = sum(1 for r in results if r["success"])
    print(f"\n✓ Research complete: {successful}/{len(results)} successful")
    
    return results


def example_3_load_and_research():
    """Example 3: Load topics from existing file and research"""
    print("\n" + "="*80)
    print("Example 3: Load Topics and Research")
    print("="*80 + "\n")
    
    research = ResearchLookup()
    
    # Create a sample topics file
    topics_file = "predefined_topics.txt"
    sample_topics = [
        "Recent advances in quantum computing hardware 2024",
        "Applications of transformer models in drug discovery",
        "Climate change impact on marine biodiversity",
        "Renewable energy storage solutions comparison"
    ]
    
    print("Creating sample topics file...")
    research.save_topics_to_file(sample_topics, topics_file)
    
    # Load topics
    print(f"\nLoading topics from {topics_file}...")
    topics = research.load_topics_from_file(topics_file)
    
    # Research in parallel
    print("\nExecuting parallel research...")
    results = research.batch_lookup(
        queries=topics,
        parallel=True,
        max_workers=5
    )
    
    # Display summary
    print("\nResults Summary:")
    for i, result in enumerate(results, 1):
        status = "✓" if result["success"] else "✗"
        print(f"{status} {i}. {result['query'][:60]}...")
        if result["success"]:
            print(f"   Model: {result.get('model_type', 'unknown')}")
    
    return results


def example_4_sequential_vs_parallel():
    """Example 4: Compare sequential vs parallel execution"""
    print("\n" + "="*80)
    print("Example 4: Sequential vs Parallel Comparison")
    print("="*80 + "\n")
    
    import time
    
    research = ResearchLookup()
    
    queries = [
        "CRISPR gene editing recent advances",
        "mRNA vaccine technology",
        "AI in drug discovery"
    ]
    
    # Sequential execution
    print("Running SEQUENTIAL research...")
    start = time.time()
    sequential_results = research.batch_lookup(queries, parallel=False, delay=0)
    sequential_time = time.time() - start
    
    print(f"Sequential time: {sequential_time:.2f} seconds")
    
    # Parallel execution
    print("\nRunning PARALLEL research...")
    start = time.time()
    parallel_results = research.batch_lookup(queries, parallel=True, max_workers=3)
    parallel_time = time.time() - start
    
    print(f"Parallel time: {parallel_time:.2f} seconds")
    
    # Comparison
    speedup = sequential_time / parallel_time if parallel_time > 0 else 0
    print(f"\n✓ Speedup: {speedup:.2f}x faster with parallel execution")
    print(f"  Time saved: {sequential_time - parallel_time:.2f} seconds")
    
    return {"sequential": sequential_results, "parallel": parallel_results}


def main():
    """Run all examples"""
    print("\n" + "="*80)
    print("PARALLEL RESEARCH WORKFLOW EXAMPLES")
    print("="*80)
    
    # Check for API key
    if not os.getenv("OPENROUTER_API_KEY"):
        print("\n⚠️  Error: OPENROUTER_API_KEY not set")
        print("Please set your OpenRouter API key:")
        print("  export OPENROUTER_API_KEY='your_key_here'")
        return 1
    
    try:
        # Run examples
        print("\nRunning comprehensive examples...")
        print("This will demonstrate the parallel research workflow.\n")
        
        # Example 1: Complete workflow
        example_1_complete_workflow()
        
        # Example 2: Step-by-step
        example_2_step_by_step()
        
        # Example 3: Load from file
        example_3_load_and_research()
        
        # Example 4: Performance comparison
        example_4_sequential_vs_parallel()
        
        print("\n" + "="*80)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("="*80)
        print("\nGenerated files:")
        print("  - example_topics.txt (Example 1)")
        print("  - example_results.json (Example 1)")
        print("  - step_by_step_topics.txt (Example 2)")
        print("  - predefined_topics.txt (Example 3)")
        print("\nYou can review these files and use them as templates.")
        
        return 0
        
    except Exception as e:
        print(f"\n⚠️  Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())

