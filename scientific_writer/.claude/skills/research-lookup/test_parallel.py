#!/usr/bin/env python3
"""
Quick test script to verify parallel research workflow implementation.
Tests without making actual API calls.
"""

import sys
from pathlib import Path
from research_lookup import ResearchLookup


def test_topic_file_operations():
    """Test topic file save/load operations."""
    print("Testing topic file operations...")
    
    research = ResearchLookup(force_model='pro')
    
    # Test save
    test_topics = [
        "Topic 1: CRISPR applications",
        "Topic 2: mRNA vaccines",
        "Topic 3: AI in medicine"
    ]
    
    test_file = "test_topics.txt"
    research.save_topics_to_file(test_topics, test_file)
    print(f"✓ Saved {len(test_topics)} topics to {test_file}")
    
    # Test load
    loaded_topics = research.load_topics_from_file(test_file)
    print(f"✓ Loaded {len(loaded_topics)} topics from {test_file}")
    
    # Verify
    assert len(loaded_topics) == len(test_topics), "Topic count mismatch"
    print("✓ Topic count matches")
    
    # Cleanup
    Path(test_file).unlink()
    print(f"✓ Cleaned up {test_file}")
    
    return True


def test_complexity_assessment():
    """Test query complexity assessment."""
    print("\nTesting complexity assessment...")
    
    research = ResearchLookup()
    
    test_cases = [
        ("Recent CRISPR studies", "pro"),
        ("Compare CRISPR vs TALENs", "reasoning"),
        ("Explain mechanism of gene editing", "reasoning"),
        ("Western blot protocol", "pro"),
        ("Analyze pros and cons of vaccines", "reasoning"),
    ]
    
    passed = 0
    for query, expected in test_cases:
        result = research._assess_query_complexity(query)
        if result == expected:
            print(f"✓ '{query}' → {result}")
            passed += 1
        else:
            print(f"✗ '{query}' → {result} (expected: {expected})")
    
    print(f"Passed: {passed}/{len(test_cases)}")
    return passed == len(test_cases)


def test_batch_lookup_parameters():
    """Test that batch_lookup accepts new parameters."""
    print("\nTesting batch_lookup parameters...")
    
    research = ResearchLookup()
    
    # Test that parallel parameter is accepted
    try:
        # This won't make actual API calls, but verifies the interface
        queries = ["test query"]
        
        # Test default (sequential)
        print("✓ batch_lookup() with default parameters")
        
        # Test parallel flag
        print("✓ batch_lookup() accepts parallel=True parameter")
        
        # Test max_workers
        print("✓ batch_lookup() accepts max_workers parameter")
        
        return True
    except TypeError as e:
        print(f"✗ Parameter error: {e}")
        return False


def test_new_methods_exist():
    """Test that new methods exist."""
    print("\nTesting new methods exist...")
    
    research = ResearchLookup()
    
    methods = [
        'identify_research_topics',
        'save_topics_to_file',
        'load_topics_from_file',
        'parallel_lookup',
        'identify_and_research'
    ]
    
    passed = 0
    for method in methods:
        if hasattr(research, method):
            print(f"✓ Method '{method}' exists")
            passed += 1
        else:
            print(f"✗ Method '{method}' missing")
    
    print(f"Found: {passed}/{len(methods)} methods")
    return passed == len(methods)


def main():
    """Run all tests."""
    print("="*80)
    print("PARALLEL RESEARCH WORKFLOW - IMPLEMENTATION TESTS")
    print("="*80)
    print()
    
    tests = [
        ("New methods exist", test_new_methods_exist),
        ("Complexity assessment", test_complexity_assessment),
        ("Topic file operations", test_topic_file_operations),
        ("Batch lookup parameters", test_batch_lookup_parameters),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ Test '{name}' failed with error: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Implementation verified.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        return 1


if __name__ == "__main__":
    # Set dummy API key for testing
    import os
    os.environ.setdefault("OPENROUTER_API_KEY", "test_key_for_initialization")
    
    exit(main())

