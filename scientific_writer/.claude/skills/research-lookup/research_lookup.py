#!/usr/bin/env python3
"""
Research Information Lookup Tool
Uses Perplexity's Sonar Pro or Sonar Reasoning Pro models through OpenRouter.
Automatically selects the appropriate model based on query complexity.
"""

import os
import json
import requests
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import quote


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

    def batch_lookup(self, queries: List[str], delay: float = 1.0) -> List[Dict[str, Any]]:
        """Perform multiple research lookups with optional delay between requests."""
        results = []

        for i, query in enumerate(queries):
            if i > 0 and delay > 0:
                time.sleep(delay)  # Rate limiting

            result = self.lookup(query)
            results.append(result)

            # Print progress
            print(f"[Research] Completed query {i+1}/{len(queries)}: {query[:50]}...")

        return results

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

    parser = argparse.ArgumentParser(description="Research Information Lookup Tool")
    parser.add_argument("query", nargs="?", help="Research query to look up")
    parser.add_argument("--model-info", action="store_true", help="Show available models")
    parser.add_argument("--batch", nargs="+", help="Run multiple queries")
    parser.add_argument("--force-model", choices=['pro', 'reasoning'], 
                       help="Force use of specific model (pro=fast lookup, reasoning=deep analysis)")

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

        if not args.query and not args.batch:
            parser.print_help()
            return 1

        if args.batch:
            print(f"Running batch research for {len(args.batch)} queries...")
            results = research.batch_lookup(args.batch)
        else:
            print(f"Researching: {args.query}")
            results = [research.lookup(args.query)]

        # Display results
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
                print(f"\nError in query {i+1}: {result['error']}")

        return 0

    except Exception as e:
        print(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
