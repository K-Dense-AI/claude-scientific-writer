#!/usr/bin/env python3
"""
Research Information Lookup Tool
Uses Perplexity's Sonar Pro or Sonar Reasoning Pro models through OpenRouter.
Automatically selects the appropriate model based on query complexity.
Supports parallel research query execution for improved performance.
"""

import os
import json
import requests
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


class ResearchLookup:
    """Research information lookup using Perplexity Sonar models via OpenRouter."""

    # Complexity indicators for determining which model to use
    REASONING_KEYWORDS = [
        'compare', 'contrast', 'analyze', 'analysis', 'synthesis', 'meta-analysis',
        'systematic review', 'evaluate', 'critique', 'trade-off', 'tradeoff',
        'relationship', 'versus', 'vs', 'vs.', 'compared to',
        'mechanism', 'why', 'how does', 'how do', 'explain', 'theoretical framework',
        'implications', 'debate', 'controversy', 'conflicting', 'paradox',
        'reconcile', 'integrate', 'multifaceted', 'complex interaction',
        'causal relationship', 'underlying mechanism', 'interpret', 'reasoning',
        'pros and cons', 'advantages and disadvantages', 'critical analysis',
        'differences between', 'similarities', 'trade offs'
    ]

    def __init__(self, force_model: Optional[str] = None):
        """
        Initialize the research lookup tool.
        
        Args:
            force_model: Optional model override ('pro' or 'reasoning'). 
                        If None, automatically selects based on query complexity.
        """
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")

        self.base_url = "https://openrouter.ai/api/v1"
        self.model_pro = "perplexity/sonar-pro"  # Fast, efficient lookup
        self.model_reasoning = "perplexity/sonar-reasoning-pro"  # Deep analysis
        self.force_model = force_model
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://scientific-writer.local",  # Replace with your domain
            "X-Title": "Scientific Writer Research Tool"
        }

    def _assess_query_complexity(self, query: str) -> str:
        """
        Assess query complexity to determine which model to use.
        
        Returns:
            'reasoning' for complex analytical queries, 'pro' for straightforward lookups
        """
        query_lower = query.lower()
        
        # Count reasoning keywords
        reasoning_count = sum(1 for keyword in self.REASONING_KEYWORDS if keyword in query_lower)
        
        # Count questions (multiple questions suggest complexity)
        question_count = query.count('?')
        
        # Check for multiple clauses (complexity indicators)
        clause_indicators = [' and ', ' or ', ' but ', ' however ', ' whereas ', ' although ']
        clause_count = sum(1 for indicator in clause_indicators if indicator in query_lower)
        
        # Complexity score
        complexity_score = (
            reasoning_count * 3 +      # Reasoning keywords heavily weighted
            question_count * 2 +        # Multiple questions indicate complexity
            clause_count * 1.5 +        # Multiple clauses suggest nuance
            (1 if len(query) > 150 else 0)  # Long queries often more complex
        )
        
        # Threshold for using reasoning model (lowered to 3 to catch single reasoning keywords)
        return 'reasoning' if complexity_score >= 3 else 'pro'
    
    def _select_model(self, query: str) -> str:
        """Select the appropriate model based on query complexity or force override."""
        if self.force_model:
            return self.model_reasoning if self.force_model == 'reasoning' else self.model_pro
        
        complexity_level = self._assess_query_complexity(query)
        return self.model_reasoning if complexity_level == 'reasoning' else self.model_pro

    def _make_request(self, messages: List[Dict[str, str]], model: str, **kwargs) -> Dict[str, Any]:
        """Make a request to the OpenRouter API."""
        data = {
            "model": model,
            "messages": messages,
            "max_tokens": 4000,
            "temperature": 0.1,  # Low temperature for factual research
            "provider": {
                "order": ["Perplexity"],
                "allow_fallbacks": False
            },
            **kwargs
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=data,
                timeout=90  # Increased timeout for reasoning model
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")

    def _format_research_prompt(self, query: str) -> str:
        """Format the query for optimal research results."""
        return f"""You are an expert research assistant. Please provide comprehensive, accurate research information for the following query: "{query}"

IMPORTANT INSTRUCTIONS:
1. Focus on ACADEMIC and SCIENTIFIC sources (peer-reviewed papers, reputable journals, institutional research)
2. Include RECENT information (prioritize 2020-2024 publications)
3. Provide COMPLETE citations with authors, title, journal/conference, year, and DOI when available
4. Structure your response with clear sections and proper attribution
5. Be comprehensive but concise - aim for 800-1200 words
6. Include key findings, methodologies, and implications when relevant
7. Note any controversies, limitations, or conflicting evidence

RESPONSE FORMAT:
- Start with a brief summary (2-3 sentences)
- Present key findings and studies in organized sections
- End with future directions or research gaps if applicable
- Include 5-8 high-quality citations at the end

Remember: This is for academic research purposes. Prioritize accuracy, completeness, and proper attribution."""

    def lookup(self, query: str) -> Dict[str, Any]:
        """Perform a research lookup for the given query."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Select the appropriate model based on query complexity
        selected_model = self._select_model(query)
        model_type = "reasoning" if "reasoning" in selected_model else "standard"
        
        print(f"[Research] Using {selected_model} (detected complexity: {model_type})")

        # Format the research prompt
        research_prompt = self._format_research_prompt(query)

        # Prepare messages for the API with system message for academic mode
        messages = [
            {
                "role": "system", 
                "content": "You are an academic research assistant. Focus exclusively on scholarly sources: peer-reviewed journals, academic papers, research institutions, and reputable scientific publications. Prioritize recent academic literature (2020-2024) and provide complete citations with DOIs. Use academic/scholarly search mode."
            },
            {"role": "user", "content": research_prompt}
        ]

        try:
            # Make the API request with selected model
            response = self._make_request(messages, model=selected_model)

            # Extract the response content
            if "choices" in response and len(response["choices"]) > 0:
                choice = response["choices"][0]
                if "message" in choice and "content" in choice["message"]:
                    content = choice["message"]["content"]

                    # Extract citations if present (basic regex extraction)
                    citations = self._extract_citations(content)

                    return {
                        "success": True,
                        "query": query,
                        "response": content,
                        "citations": citations,
                        "timestamp": timestamp,
                        "model": selected_model,
                        "model_type": model_type,
                        "usage": response.get("usage", {})
                    }
                else:
                    raise Exception("Invalid response format from API")
            else:
                raise Exception("No response choices received from API")

        except Exception as e:
            return {
                "success": False,
                "query": query,
                "error": str(e),
                "timestamp": timestamp,
                "model": selected_model,
                "model_type": model_type
            }

    def _extract_citations(self, text: str) -> List[Dict[str, str]]:
        """Extract potential citations from the response text."""
        # This is a simple citation extractor - in practice, you might want
        # to use a more sophisticated approach or rely on the model's structured output

        citations = []

        # Look for common citation patterns
        import re

        # Pattern for author et al. year
        author_pattern = r'([A-Z][a-z]+(?:\s+[A-Z]\.)*(?:\s+et\s+al\.)?)\s*\((\d{4})\)'
        matches = re.findall(author_pattern, text)

        for author, year in matches:
            citations.append({
                "authors": author,
                "year": year,
                "type": "extracted"
            })

        # Look for DOI patterns
        doi_pattern = r'doi:\s*([^\s\)\]]+)'
        doi_matches = re.findall(doi_pattern, text, re.IGNORECASE)

        for doi in doi_matches:
            citations.append({
                "doi": doi.strip(),
                "type": "doi"
            })

        return citations

    def identify_research_topics(self, text: str, output_file: Optional[str] = None) -> List[str]:
        """
        Identify research topics/questions from a text that need to be looked up.
        
        Args:
            text: Input text to analyze for research topics
            output_file: Optional path to save identified topics
            
        Returns:
            List of identified research topics/questions
        """
        print("[Research] Identifying research topics...")
        
        # Use the API to identify research topics
        messages = [
            {
                "role": "system",
                "content": "You are a research assistant. Extract and list all specific research topics, questions, or areas that would benefit from literature lookup. Each topic should be a clear, focused research question."
            },
            {
                "role": "user",
                "content": f"""Analyze the following text and identify all research topics, questions, or areas that would benefit from academic literature lookup.

Format your response as a numbered list, with each item being a specific, focused research question or topic.

Text to analyze:
{text}

Provide ONLY the numbered list of research topics, one per line, without any additional explanation."""
            }
        ]
        
        try:
            # Use the pro model for this task (fast and efficient)
            response = self._make_request(messages, model=self.model_pro)
            
            if "choices" in response and len(response["choices"]) > 0:
                content = response["choices"][0]["message"]["content"]
                
                # Parse the numbered list into individual topics
                topics = []
                for line in content.strip().split('\n'):
                    line = line.strip()
                    if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                        # Remove numbering/bullets
                        topic = line.lstrip('0123456789.-•) ').strip()
                        if topic:
                            topics.append(topic)
                
                print(f"[Research] Identified {len(topics)} research topics")
                
                # Save to file if requested
                if output_file:
                    self.save_topics_to_file(topics, output_file)
                    
                return topics
            else:
                raise Exception("Failed to identify research topics")
                
        except Exception as e:
            print(f"[Research] Error identifying topics: {str(e)}")
            return []
    
    def save_topics_to_file(self, topics: List[str], filepath: str) -> None:
        """
        Save research topics to a text file.
        
        Args:
            topics: List of research topics
            filepath: Path to output file
        """
        output_path = Path(filepath)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# Research Topics Identified\n")
            f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Total topics: {len(topics)}\n\n")
            
            for i, topic in enumerate(topics, 1):
                f.write(f"{i}. {topic}\n")
        
        print(f"[Research] Saved {len(topics)} topics to {filepath}")
    
    def load_topics_from_file(self, filepath: str) -> List[str]:
        """
        Load research topics from a text file.
        
        Args:
            filepath: Path to input file
            
        Returns:
            List of research topics
        """
        topics = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith('#'):
                    # Remove numbering if present
                    topic = line.lstrip('0123456789.-•) ').strip()
                    if topic:
                        topics.append(topic)
        
        print(f"[Research] Loaded {len(topics)} topics from {filepath}")
        return topics
    
    def parallel_lookup(self, queries: List[str], max_workers: int = 5) -> List[Dict[str, Any]]:
        """
        Perform multiple research lookups in parallel using ThreadPoolExecutor.
        
        Args:
            queries: List of research queries
            max_workers: Maximum number of parallel workers (default: 5)
            
        Returns:
            List of results in the same order as input queries
        """
        print(f"[Research] Starting parallel lookup for {len(queries)} queries with {max_workers} workers...")
        
        results = [None] * len(queries)  # Pre-allocate results list
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all queries
            future_to_index = {
                executor.submit(self.lookup, query): i 
                for i, query in enumerate(queries)
            }
            
            # Process results as they complete
            completed = 0
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    result = future.result()
                    results[index] = result
                    completed += 1
                    
                    query_preview = queries[index][:50]
                    status = "✓" if result["success"] else "✗"
                    print(f"[Research] {status} Completed {completed}/{len(queries)}: {query_preview}...")
                    
                except Exception as e:
                    print(f"[Research] ✗ Error in query {index + 1}: {str(e)}")
                    results[index] = {
                        "success": False,
                        "query": queries[index],
                        "error": str(e),
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
        
        print(f"[Research] Parallel lookup complete. {sum(1 for r in results if r and r['success'])}/{len(queries)} successful")
        return results

    def batch_lookup(self, queries: List[str], delay: float = 1.0, parallel: bool = False, max_workers: int = 5) -> List[Dict[str, Any]]:
        """
        Perform multiple research lookups with optional delay between requests.
        
        Args:
            queries: List of research queries
            delay: Delay between sequential requests (ignored if parallel=True)
            parallel: If True, run queries in parallel (default: False for backward compatibility)
            max_workers: Maximum parallel workers when parallel=True (default: 5)
            
        Returns:
            List of results
        """
        if parallel:
            return self.parallel_lookup(queries, max_workers=max_workers)
        
        # Sequential execution (original behavior)
        results = []

        for i, query in enumerate(queries):
            if i > 0 and delay > 0:
                time.sleep(delay)  # Rate limiting

            result = self.lookup(query)
            results.append(result)

            # Print progress
            print(f"[Research] Completed query {i+1}/{len(queries)}: {query[:50]}...")

        return results

    def identify_and_research(
        self, 
        text: str, 
        topics_file: Optional[str] = None,
        parallel: bool = True,
        max_workers: int = 5,
        output_file: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Complete workflow: identify research topics and conduct parallel research.
        
        Args:
            text: Input text to analyze for research topics
            topics_file: Optional path to save identified topics
            parallel: Whether to run queries in parallel (default: True)
            max_workers: Maximum parallel workers (default: 5)
            output_file: Optional path to save results JSON
            
        Returns:
            Dictionary containing topics and results
        """
        print("[Research] Starting complete research workflow...")
        
        # Step 1: Identify research topics
        topics = self.identify_research_topics(text, output_file=topics_file)
        
        if not topics:
            return {
                "success": False,
                "error": "No research topics identified",
                "topics": [],
                "results": []
            }
        
        # Step 2: Conduct research
        print(f"\n[Research] Conducting research on {len(topics)} topics...")
        results = self.batch_lookup(topics, parallel=parallel, max_workers=max_workers)
        
        # Step 3: Save results if requested
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            output_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_topics": len(topics),
                "successful_queries": sum(1 for r in results if r["success"]),
                "topics": topics,
                "results": results
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            print(f"[Research] Complete results saved to {output_file}")
        
        return {
            "success": True,
            "topics": topics,
            "results": results,
            "successful_queries": sum(1 for r in results if r["success"]),
            "total_queries": len(results)
        }

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about available models from OpenRouter."""
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}


def main():
    """Command-line interface for testing the research lookup tool."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Research Information Lookup Tool with Parallel Execution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single query
  python research_lookup.py "Recent advances in CRISPR"
  
  # Identify research topics from text and save to file
  python research_lookup.py --identify input.txt --topics-file topics.txt
  
  # Run parallel research from saved topics
  python research_lookup.py --topics-file topics.txt --parallel --max-workers 10
  
  # Batch queries with parallel execution
  python research_lookup.py --batch "CRISPR" "mRNA vaccines" "AI in medicine" --parallel
        """
    )
    parser.add_argument("query", nargs="?", help="Research query to look up")
    parser.add_argument("--model-info", action="store_true", help="Show available models")
    parser.add_argument("--batch", nargs="+", help="Run multiple queries")
    parser.add_argument("--force-model", choices=['pro', 'reasoning'], 
                       help="Force use of specific model (pro=fast lookup, reasoning=deep analysis)")
    parser.add_argument("--parallel", action="store_true", 
                       help="Run batch queries in parallel (much faster)")
    parser.add_argument("--max-workers", type=int, default=5,
                       help="Maximum parallel workers (default: 5)")
    parser.add_argument("--identify", type=str, metavar="FILE",
                       help="Identify research topics from input text file")
    parser.add_argument("--topics-file", type=str, metavar="FILE",
                       help="Save identified topics to or load topics from this file")
    parser.add_argument("--output", type=str, metavar="FILE",
                       help="Save research results to JSON file")

    args = parser.parse_args()

    # Check for API key
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Error: OPENROUTER_API_KEY environment variable not set")
        print("Please set it in your .env file or export it:")
        print("  export OPENROUTER_API_KEY='your_openrouter_api_key'")
        return 1

    try:
        research = ResearchLookup(force_model=args.force_model)

        if args.model_info:
            print("Available models from OpenRouter:")
            models = research.get_model_info()
            if "data" in models:
                for model in models["data"]:
                    if "perplexity" in model["id"].lower():
                        print(f"  - {model['id']}: {model.get('name', 'N/A')}")
            return 0

        # Handle topic identification
        if args.identify:
            if not os.path.exists(args.identify):
                print(f"Error: Input file not found: {args.identify}")
                return 1
            
            with open(args.identify, 'r', encoding='utf-8') as f:
                text = f.read()
            
            topics = research.identify_research_topics(text, output_file=args.topics_file)
            
            if not topics:
                print("No research topics identified.")
                return 1
            
            print(f"\nIdentified {len(topics)} research topics:")
            for i, topic in enumerate(topics, 1):
                print(f"  {i}. {topic}")
            
            # If no topics file specified, don't continue to research
            if not args.topics_file:
                return 0
            
            # Continue to research the identified topics
            queries = topics
            
        # Load topics from file if specified and not identifying
        elif args.topics_file and os.path.exists(args.topics_file):
            queries = research.load_topics_from_file(args.topics_file)
            if not queries:
                print(f"No topics found in {args.topics_file}")
                return 1
                
        # Handle batch queries
        elif args.batch:
            queries = args.batch
            
        # Handle single query
        elif args.query:
            queries = [args.query]
            
        else:
            parser.print_help()
            return 1

        # Execute research queries
        if len(queries) > 1:
            print(f"\n{'='*80}")
            print(f"Researching {len(queries)} queries...")
            if args.parallel:
                print(f"Mode: PARALLEL with {args.max_workers} workers")
            else:
                print("Mode: SEQUENTIAL")
            print(f"{'='*80}\n")
            
            results = research.batch_lookup(
                queries, 
                parallel=args.parallel, 
                max_workers=args.max_workers
            )
        else:
            print(f"Researching: {queries[0]}")
            results = [research.lookup(queries[0])]

        # Display results
        print(f"\n{'='*80}")
        print("RESULTS")
        print(f"{'='*80}\n")
        
        for i, result in enumerate(results):
            if result["success"]:
                print(f"\n{'='*80}")
                print(f"Query {i+1}: {result['query']}")
                print(f"Timestamp: {result['timestamp']}")
                print(f"Model: {result['model']} ({result.get('model_type', 'unknown')})")
                print(f"{'='*80}")
                print(result["response"])

                if result["citations"]:
                    print(f"\nExtracted Citations ({len(result['citations'])}):")
                    for j, citation in enumerate(result["citations"]):
                        print(f"  {j+1}. {citation}")

                if result["usage"]:
                    print(f"\nUsage: {result['usage']}")
            else:
                print(f"\n{'='*80}")
                print(f"Query {i+1} FAILED: {result['query']}")
                print(f"Error: {result['error']}")
                print(f"{'='*80}")

        # Save results to file if requested
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n[Research] Results saved to {args.output}")

        # Summary
        successful = sum(1 for r in results if r["success"])
        print(f"\n{'='*80}")
        print(f"SUMMARY: {successful}/{len(results)} queries completed successfully")
        print(f"{'='*80}")

        return 0

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
