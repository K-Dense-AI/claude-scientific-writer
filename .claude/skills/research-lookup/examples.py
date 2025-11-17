#!/usr/bin/env python3
"""
Example usage of the Research Lookup skill with automatic model selection
and parallel research workflow.

This script demonstrates:
1. Automatic model selection based on query complexity
2. Manual model override options
3. Batch query processing (sequential and parallel)
4. AI-powered topic identification
5. Complete parallel research workflow
6. Integration with scientific writing workflows
"""

import os
from research_lookup import ResearchLookup


def example_automatic_selection():
    """Demonstrate automatic model selection."""
    print("=" * 80)
    print("EXAMPLE 1: Automatic Model Selection")
    print("=" * 80)
    print()
    
    research = ResearchLookup()
    
    # Simple lookup - will use Sonar Pro
    query1 = "Recent advances in CRISPR gene editing 2024"
    print(f"Query: {query1}")
    print(f"Expected model: Sonar Pro (fast lookup)")
    result1 = research.lookup(query1)
    print(f"Actual model: {result1.get('model')}")
    print()
    
    # Complex analysis - will use Sonar Reasoning Pro
    query2 = "Compare and contrast the efficacy of mRNA vaccines versus traditional vaccines"
    print(f"Query: {query2}")
    print(f"Expected model: Sonar Reasoning Pro (analytical)")
    result2 = research.lookup(query2)
    print(f"Actual model: {result2.get('model')}")
    print()


def example_manual_override():
    """Demonstrate manual model override."""
    print("=" * 80)
    print("EXAMPLE 2: Manual Model Override")
    print("=" * 80)
    print()
    
    # Force Sonar Pro for budget-constrained rapid lookup
    research_pro = ResearchLookup(force_model='pro')
    query = "Explain the mechanism of CRISPR-Cas9"
    print(f"Query: {query}")
    print(f"Forced model: Sonar Pro")
    result = research_pro.lookup(query)
    print(f"Model used: {result.get('model')}")
    print()
    
    # Force Sonar Reasoning Pro for critical analysis
    research_reasoning = ResearchLookup(force_model='reasoning')
    print(f"Query: {query}")
    print(f"Forced model: Sonar Reasoning Pro")
    result = research_reasoning.lookup(query)
    print(f"Model used: {result.get('model')}")
    print()


def example_batch_queries():
    """Demonstrate batch query processing (sequential)."""
    print("=" * 80)
    print("EXAMPLE 3: Batch Query Processing (Sequential)")
    print("=" * 80)
    print()
    
    research = ResearchLookup()
    
    # Mix of simple and complex queries
    queries = [
        "Recent clinical trials for Alzheimer's disease",  # Sonar Pro
        "Compare deep learning vs traditional ML in drug discovery",  # Sonar Reasoning Pro
        "Statistical power analysis methods",  # Sonar Pro
    ]
    
    print("Processing batch queries sequentially...")
    print("Each query will automatically select the appropriate model")
    print()
    
    results = research.batch_lookup(queries, delay=1.0, parallel=False)
    
    for i, result in enumerate(results):
        print(f"Query {i+1}: {result['query'][:50]}...")
        print(f"  Model: {result.get('model')}")
        print(f"  Type: {result.get('model_type')}")
        print()


def example_parallel_queries():
    """Demonstrate parallel batch query processing."""
    print("=" * 80)
    print("EXAMPLE 3B: Parallel Batch Query Processing")
    print("=" * 80)
    print()
    
    research = ResearchLookup()
    
    # Multiple queries that will run in parallel
    queries = [
        "Recent clinical trials for Alzheimer's disease",
        "Compare deep learning vs traditional ML in drug discovery",
        "Statistical power analysis methods",
        "CRISPR applications in cancer therapy 2024",
        "mRNA vaccine mechanism of action",
    ]
    
    print("Processing queries in parallel (much faster!)...")
    print(f"Running {len(queries)} queries with 5 parallel workers")
    print()
    
    results = research.batch_lookup(queries, parallel=True, max_workers=5)
    
    print("\nResults:")
    for i, result in enumerate(results):
        status = "✓" if result.get("success") else "✗"
        print(f"{status} Query {i+1}: {result['query'][:50]}...")
        print(f"  Model: {result.get('model')}")
        print(f"  Type: {result.get('model_type')}")
        print()


def example_topic_identification():
    """Demonstrate AI-powered topic identification."""
    print("=" * 80)
    print("EXAMPLE 4: AI Topic Identification")
    print("=" * 80)
    print()
    
    research = ResearchLookup()
    
    # Sample research proposal text
    text = """
    We propose to investigate the therapeutic potential of CRISPR gene editing
    for treating sickle cell disease. This research will examine clinical trial
    outcomes, delivery mechanisms, off-target effects, and compare results with
    traditional treatments like bone marrow transplantation.
    """
    
    print("Input text:")
    print(text)
    print()
    print("Identifying research topics using AI...")
    
    topics = research.identify_research_topics(text, output_file="identified_topics.txt")
    
    print(f"\nIdentified {len(topics)} research topics:")
    for i, topic in enumerate(topics, 1):
        print(f"  {i}. {topic}")
    print()
    print("Topics saved to: identified_topics.txt")
    print()


def example_complete_workflow():
    """Demonstrate complete parallel research workflow."""
    print("=" * 80)
    print("EXAMPLE 5: Complete Parallel Research Workflow")
    print("=" * 80)
    print()
    
    research = ResearchLookup()
    
    # Sample text with multiple research needs
    text = """
    Background: Recent advances in AI and machine learning have revolutionized
    drug discovery. We need to understand current state-of-art methods, compare
    different approaches, and identify best practices for clinical applications.
    """
    
    print("Step 1: Identify research topics from text")
    print("Step 2: Save topics to file")
    print("Step 3: Execute parallel research")
    print("Step 4: Save comprehensive results")
    print()
    
    result = research.identify_and_research(
        text=text,
        topics_file="workflow_topics.txt",
        parallel=True,
        max_workers=5,
        output_file="workflow_results.json"
    )
    
    print(f"\n✓ Workflow complete!")
    print(f"  Topics identified: {len(result['topics'])}")
    print(f"  Successful queries: {result['successful_queries']}/{result['total_queries']}")
    print(f"  Topics saved to: workflow_topics.txt")
    print(f"  Results saved to: workflow_results.json")
    print()


def example_scientific_writing_workflow():
    """Demonstrate integration with scientific writing workflow."""
    print("=" * 80)
    print("EXAMPLE 6: Scientific Writing Workflow Integration")
    print("=" * 80)
    print()
    
    research = ResearchLookup()
    
    # Literature review phase - gather sources in parallel
    print("PHASE 1: Literature Review (Breadth) - Parallel Research")
    lit_queries = [
        "Recent papers on machine learning in genomics 2024",
        "Clinical applications of AI in radiology",
        "RNA sequencing analysis methods"
    ]
    
    print("Queries:")
    for query in lit_queries:
        print(f"  - {query}")
    
    print("\nRunning in parallel...")
    lit_results = research.parallel_lookup(lit_queries, max_workers=3)
    print(f"✓ Completed {len(lit_results)} literature searches")
    print()
    
    # Discussion phase - analytical queries (may use Reasoning Pro)
    print("PHASE 2: Discussion (Synthesis & Analysis)")
    discussion_queries = [
        "Compare the advantages and limitations of different ML approaches in genomics",
        "Explain the relationship between model interpretability and clinical adoption",
        "Analyze the ethical implications of AI in medical diagnosis"
    ]
    
    print("Queries:")
    for query in discussion_queries:
        print(f"  - {query}")
        # These will automatically use Sonar Reasoning Pro
    
    print("\nRunning in parallel...")
    discussion_results = research.parallel_lookup(discussion_queries, max_workers=3)
    print(f"✓ Completed {len(discussion_results)} analytical queries")
    print()
    
    print(f"Total time saved: ~{(len(lit_queries) + len(discussion_queries)) * 10 - 20} seconds")
    print("(compared to sequential execution)")
    print()


def main():
    """Run all examples (requires OPENROUTER_API_KEY to be set)."""
    
    print("=" * 80)
    print("RESEARCH LOOKUP SKILL - EXAMPLES")
    print("=" * 80)
    print()
    
    if not os.getenv("OPENROUTER_API_KEY"):
        print("⚠️  Note: Set OPENROUTER_API_KEY environment variable to run live queries")
        print("These examples show the structure without making actual API calls")
        print()
        print("To run with actual API calls:")
        print("  export OPENROUTER_API_KEY='your_key_here'")
        print("  python examples.py")
        print()
    
    # Show available examples
    print("Available Examples:")
    print("  1. Automatic Model Selection")
    print("  2. Manual Model Override")
    print("  3. Batch Query Processing (Sequential)")
    print("  3B. Parallel Batch Query Processing ⚡ NEW")
    print("  4. AI Topic Identification 🤖 NEW")
    print("  5. Complete Parallel Research Workflow 🚀 NEW")
    print("  6. Scientific Writing Workflow Integration")
    print()
    
    # Uncomment to run examples (requires API key)
    # print("Running examples with actual API calls...\n")
    # example_automatic_selection()
    # example_manual_override()
    # example_batch_queries()
    # example_parallel_queries()
    # example_topic_identification()
    # example_complete_workflow()
    # example_scientific_writing_workflow()
    
    # Show complexity assessment without API calls
    print("=" * 80)
    print("COMPLEXITY ASSESSMENT DEMO (No API calls required)")
    print("=" * 80)
    print()
    print("This demonstrates how queries are automatically classified:")
    print()
    
    os.environ.setdefault("OPENROUTER_API_KEY", "test")
    research = ResearchLookup()
    
    test_queries = [
        ("Recent CRISPR studies", "pro"),
        ("Compare CRISPR vs TALENs", "reasoning"),
        ("Explain how CRISPR works", "reasoning"),
        ("Western blot protocol", "pro"),
        ("Pros and cons of different sequencing methods", "reasoning"),
        ("Analyze the controversy surrounding gene editing", "reasoning"),
        ("Latest mRNA vaccine publications 2024", "pro"),
    ]
    
    for query, expected in test_queries:
        complexity = research._assess_query_complexity(query)
        model_name = "Sonar Reasoning Pro" if complexity == "reasoning" else "Sonar Pro"
        status = "✓" if complexity == expected else "✗"
        print(f"{status} '{query}'")
        print(f"  → {model_name}")
        print()
    
    print("=" * 80)
    print("To run full examples with API calls, set OPENROUTER_API_KEY and")
    print("uncomment the example function calls in main().")
    print("=" * 80)
    print()
    print("For comprehensive parallel workflow examples, see:")
    print("  examples/parallel_research_workflow.py")
    print()


if __name__ == "__main__":
    main()

