#!/usr/bin/env python3
"""
Research Information Lookup Tool

Routes research queries to the best backend:
  - Parallel Deep Research (pro-fast): Default for all general research queries
  - Perplexity sonar-pro-search (via OpenRouter): Academic-specific paper searches

Environment variables:
  PARALLEL_API_KEY    - Required for Parallel Deep Research (primary backend)
  OPENROUTER_API_KEY  - Required for Perplexity academic searches (fallback)
"""

import os
import sys
import json
import re
import time
import requests
from datetime import datetime
from typing import Any, Dict, List, Optional


class ResearchLookup:
    """Research information lookup with intelligent backend routing.

    Routes queries to Parallel Deep Research (default) or Perplexity
    sonar-pro-search (academic paper searches only).
    """

    # Keywords that indicate an academic-specific query (routes to Perplexity)
    ACADEMIC_KEYWORDS = [
        "find papers", "find paper", "find articles", "find article",
        "cite ", "citation", "citations for",
        "doi ", "doi:", "pubmed", "pmid",
        "journal article", "peer-reviewed",
        "systematic review", "meta-analysis",
        "literature search", "literature on",
        "academic papers", "academic paper",
        "research papers on", "research paper on",
        "published studies", "published study",
        "scholarly", "scholar",
        "arxiv", "preprint",
        "foundational papers", "seminal papers", "landmark papers",
        "highly cited", "most cited",
    ]

    def __init__(self, force_backend: Optional[str] = None):
        """Initialize the research lookup tool.

        Args:
            force_backend: Force a specific backend ('parallel' or 'perplexity').
                          If None, backend is auto-selected based on query content.
        """
        self.force_backend = force_backend

        # Validate that at least one backend is available
        self.parallel_available = bool(os.getenv("PARALLEL_API_KEY"))
        self.perplexity_available = bool(os.getenv("OPENROUTER_API_KEY"))

        if not self.parallel_available and not self.perplexity_available:
            raise ValueError(
                "No API keys found. Set at least one of:\n"
                "  PARALLEL_API_KEY (for Parallel Deep Research - primary)\n"
                "  OPENROUTER_API_KEY (for Perplexity academic search - fallback)"
            )

    def _select_backend(self, query: str) -> str:
        """Select the best backend for a query.

        Returns 'parallel' or 'perplexity' based on query content and
        available API keys.
        """
        if self.force_backend:
            if self.force_backend == "perplexity" and self.perplexity_available:
                return "perplexity"
            if self.force_backend == "parallel" and self.parallel_available:
                return "parallel"
            # Fall through if forced backend isn't available

        # Check if query is academic-specific
        query_lower = query.lower()
        is_academic = any(kw in query_lower for kw in self.ACADEMIC_KEYWORDS)

        if is_academic and self.perplexity_available:
            return "perplexity"

        if self.parallel_available:
            return "parallel"

        # Fallback: use whatever is available
        if self.perplexity_available:
            return "perplexity"

        raise ValueError("No backend available. Check API keys.")

    # ------------------------------------------------------------------
    # Parallel Deep Research backend (delegates to parallel-web skill)
    # ------------------------------------------------------------------

    def _get_parallel_researcher(self):
        """Lazy-load and cache the ParallelDeepResearch instance."""
        if not hasattr(self, "_parallel_researcher"):
            # Import from the parallel-web skill's script
            parallel_web_locations = [
                os.path.join(os.path.dirname(__file__), "..", "..", "parallel-web", "scripts"),
                os.path.join(os.path.dirname(__file__), "..", "parallel-web", "scripts"),
            ]
            for loc in parallel_web_locations:
                abs_loc = os.path.abspath(loc)
                if os.path.isdir(abs_loc) and abs_loc not in sys.path:
                    sys.path.insert(0, abs_loc)

            try:
                from parallel_web import ParallelDeepResearch
                self._parallel_researcher = ParallelDeepResearch()
            except ImportError:
                # Fallback: construct directly if import path fails
                self._parallel_researcher = self._build_parallel_researcher_fallback()
        return self._parallel_researcher

    def _build_parallel_researcher_fallback(self):
        """Fallback Parallel researcher when parallel_web module is not importable."""
        try:
            from parallel import Parallel
        except ImportError:
            raise ImportError(
                "The 'parallel-web' package is required for Parallel backend.\n"
                "Install it with: pip install parallel-web"
            )
        # Return a simple wrapper using the SDK directly
        class _FallbackResearcher:
            def __init__(self):
                self.client = Parallel(api_key=os.getenv("PARALLEL_API_KEY"))
            def research(self, query, processor="pro-fast", timeout=3600, description=None):
                from parallel.types import TaskSpecParam
                text_schema = {"type": "text"}
                if description:
                    text_schema["description"] = description
                task_run = self.client.task_run.create(
                    input=query, processor=processor,
                    task_spec=TaskSpecParam(output_schema=text_schema),
                )
                run_result = self.client.task_run.result(task_run.run_id, api_timeout=timeout)
                output_text = ""
                citations = []
                if hasattr(run_result, "output"):
                    output = run_result.output
                    if hasattr(output, "content"):
                        output_text = output.content if isinstance(output.content, str) else json.dumps(output.content, indent=2)
                    elif isinstance(output, str):
                        output_text = output
                    if hasattr(output, "basis") and output.basis:
                        for basis_item in output.basis:
                            if hasattr(basis_item, "citations") and basis_item.citations:
                                for cit in basis_item.citations:
                                    citations.append({
                                        "type": "source",
                                        "url": getattr(cit, "url", ""),
                                        "title": getattr(cit, "title", ""),
                                        "excerpts": getattr(cit, "excerpts", []),
                                    })
                return {
                    "success": True, "query": query, "response": output_text,
                    "output": output_text, "citations": citations,
                    "sources": citations, "citation_count": len(citations),
                    "run_id": task_run.run_id, "processor": processor,
                    "backend": "parallel", "model": f"parallel/{processor}",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
        return _FallbackResearcher()

    def _parallel_lookup(self, query: str) -> Dict[str, Any]:
        """Run research via Parallel Deep Research (pro-fast, text mode).

        Delegates to the ParallelDeepResearch class from the parallel-web skill.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        processor = "pro-fast"

        try:
            researcher = self._get_parallel_researcher()

            description = (
                "Provide a comprehensive, well-cited research report. "
                "Include key findings, methodologies, statistics, and implications. "
                "Prioritize authoritative and recent sources. "
                "Structure the report with clear sections."
            )

            result = researcher.research(
                query=query,
                processor=processor,
                description=description,
            )

            if not result.get("success"):
                return {
                    "success": False,
                    "query": query,
                    "error": result.get("error", "Unknown error from Parallel"),
                    "timestamp": timestamp,
                    "backend": "parallel",
                    "model": f"parallel/{processor}",
                }

            # Normalize the response and extract additional text citations
            response_text = result.get("response", result.get("output", ""))
            api_citations = result.get("sources", result.get("citations", []))
            text_citations = self._extract_citations_from_text(response_text)

            return {
                "success": True,
                "query": query,
                "response": response_text,
                "citations": api_citations + text_citations,
                "sources": api_citations,
                "timestamp": timestamp,
                "backend": "parallel",
                "model": result.get("model", f"parallel/{processor}"),
                "run_id": result.get("run_id"),
            }

        except Exception as e:
            return {
                "success": False,
                "query": query,
                "error": str(e),
                "timestamp": timestamp,
                "backend": "parallel",
                "model": f"parallel/{processor}",
            }

    # ------------------------------------------------------------------
    # Perplexity academic search backend
    # ------------------------------------------------------------------

    def _perplexity_lookup(self, query: str) -> Dict[str, Any]:
        """Run academic search via Perplexity sonar-pro-search through OpenRouter."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        api_key = os.getenv("OPENROUTER_API_KEY")
        model = "perplexity/sonar-pro-search"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://scientific-writer.local",
            "X-Title": "Scientific Writer Research Tool",
        }

        research_prompt = self._format_academic_prompt(query)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an academic research assistant specializing in finding "
                    "HIGH-IMPACT, INFLUENTIAL research.\n\n"
                    "QUALITY PRIORITIZATION (CRITICAL):\n"
                    "- ALWAYS prefer highly-cited papers over obscure publications\n"
                    "- ALWAYS prioritize Tier-1 venues: Nature, Science, Cell, NEJM, Lancet, JAMA, PNAS\n"
                    "- ALWAYS prefer papers from established researchers\n"
                    "- Include citation counts when known (e.g., 'cited 500+ times')\n"
                    "- Quality matters more than quantity\n\n"
                    "VENUE HIERARCHY:\n"
                    "1. Nature/Science/Cell family, NEJM, Lancet, JAMA (highest)\n"
                    "2. High-impact specialized journals (IF>10), top conferences (NeurIPS, ICML, ICLR)\n"
                    "3. Respected field-specific journals (IF 5-10)\n"
                    "4. Other peer-reviewed sources (only if no better option)\n\n"
                    "Focus exclusively on scholarly sources. Prioritize recent literature (2020-2026) "
                    "and provide complete citations with DOIs."
                ),
            },
            {"role": "user", "content": research_prompt},
        ]

        data = {
            "model": model,
            "messages": messages,
            "max_tokens": 8000,
            "temperature": 0.1,
            "search_mode": "academic",
            "search_context_size": "high",
        }

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=90,
            )
            response.raise_for_status()
            resp_json = response.json()

            if "choices" in resp_json and len(resp_json["choices"]) > 0:
                choice = resp_json["choices"][0]
                if "message" in choice and "content" in choice["message"]:
                    content = choice["message"]["content"]

                    api_citations = self._extract_api_citations(resp_json, choice)
                    text_citations = self._extract_citations_from_text(content)
                    citations = api_citations + text_citations

                    return {
                        "success": True,
                        "query": query,
                        "response": content,
                        "citations": citations,
                        "sources": api_citations,
                        "timestamp": timestamp,
                        "backend": "perplexity",
                        "model": model,
                        "usage": resp_json.get("usage", {}),
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
                "backend": "perplexity",
                "model": model,
            }

    # ------------------------------------------------------------------
    # Shared utilities
    # ------------------------------------------------------------------

    def _format_academic_prompt(self, query: str) -> str:
        """Format a query for academic research results via Perplexity."""
        return f"""You are an expert research assistant. Please provide comprehensive, accurate research information for the following query: "{query}"

IMPORTANT INSTRUCTIONS:
1. Focus on ACADEMIC and SCIENTIFIC sources (peer-reviewed papers, reputable journals, institutional research)
2. Include RECENT information (prioritize 2020-2026 publications)
3. Provide COMPLETE citations with authors, title, journal/conference, year, and DOI when available
4. Structure your response with clear sections and proper attribution
5. Be comprehensive but concise - aim for 800-1200 words
6. Include key findings, methodologies, and implications when relevant
7. Note any controversies, limitations, or conflicting evidence

PAPER QUALITY PRIORITIZATION (CRITICAL):
8. ALWAYS prioritize HIGHLY-CITED papers over obscure publications
9. ALWAYS prioritize papers from TOP-TIER VENUES (Nature, Science, Cell, NEJM, Lancet, JAMA, PNAS)
10. PREFER papers from ESTABLISHED, REPUTABLE AUTHORS
11. For EACH citation include when available: citation count, venue tier, author credentials
12. PRIORITIZE papers that DIRECTLY address the research question

RESPONSE FORMAT:
- Start with a brief summary (2-3 sentences)
- Present key findings and studies in organized sections
- Rank papers by impact: most influential/cited first
- End with future directions or research gaps if applicable
- Include 5-8 high-quality citations

Remember: Quality over quantity. Prioritize influential, highly-cited papers from prestigious venues."""

    def _extract_api_citations(self, response: Dict[str, Any], choice: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract citations from Perplexity API response fields."""
        citations = []

        # Perplexity returns citations in search_results field
        search_results = (
            response.get("search_results")
            or choice.get("search_results")
            or choice.get("message", {}).get("search_results")
            or []
        )

        for result in search_results:
            citation = {
                "type": "source",
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "date": result.get("date", ""),
            }
            if result.get("snippet"):
                citation["snippet"] = result["snippet"]
            citations.append(citation)

        # Legacy citations field (backward compatibility)
        legacy_citations = (
            response.get("citations")
            or choice.get("citations")
            or choice.get("message", {}).get("citations")
            or []
        )

        for url in legacy_citations:
            if isinstance(url, str):
                citations.append({"type": "source", "url": url, "title": "", "date": ""})
            elif isinstance(url, dict):
                citations.append({
                    "type": "source",
                    "url": url.get("url", ""),
                    "title": url.get("title", ""),
                    "date": url.get("date", ""),
                })

        return citations

    def _extract_citations_from_text(self, text: str) -> List[Dict[str, str]]:
        """Extract DOIs and academic URLs from response text as fallback."""
        citations = []

        # DOI patterns
        doi_pattern = r'(?:doi[:\s]*|https?://(?:dx\.)?doi\.org/)(10\.[0-9]{4,}/[^\s\)\]\,\[\<\>]+)'
        doi_matches = re.findall(doi_pattern, text, re.IGNORECASE)
        seen_dois = set()

        for doi in doi_matches:
            doi_clean = doi.strip().rstrip(".,;:)]")
            if doi_clean and doi_clean not in seen_dois:
                seen_dois.add(doi_clean)
                citations.append({
                    "type": "doi",
                    "doi": doi_clean,
                    "url": f"https://doi.org/{doi_clean}",
                })

        # Academic URLs
        url_pattern = (
            r'https?://[^\s\)\]\,\<\>\"\']+(?:arxiv\.org|pubmed|ncbi\.nlm\.nih\.gov|'
            r'nature\.com|science\.org|wiley\.com|springer\.com|ieee\.org|acm\.org)'
            r'[^\s\)\]\,\<\>\"\']*'
        )
        url_matches = re.findall(url_pattern, text, re.IGNORECASE)
        seen_urls = set()

        for url in url_matches:
            url_clean = url.rstrip(".")
            if url_clean not in seen_urls:
                seen_urls.add(url_clean)
                citations.append({"type": "url", "url": url_clean})

        return citations

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def lookup(self, query: str) -> Dict[str, Any]:
        """Perform a research lookup, routing to the best backend.

        Parallel Deep Research is used by default. Perplexity sonar-pro-search
        is used only for academic-specific queries (paper searches, DOI lookups).
        """
        backend = self._select_backend(query)
        print(f"[Research] Backend: {backend} | Query: {query[:80]}...", file=sys.stderr)

        if backend == "parallel":
            return self._parallel_lookup(query)
        else:
            return self._perplexity_lookup(query)

    def batch_lookup(self, queries: List[str], delay: float = 1.0) -> List[Dict[str, Any]]:
        """Perform multiple research lookups with delay between requests."""
        results = []
        for i, query in enumerate(queries):
            if i > 0 and delay > 0:
                time.sleep(delay)
            result = self.lookup(query)
            results.append(result)
            print(f"[Research] Completed query {i+1}/{len(queries)}: {query[:50]}...", file=sys.stderr)
        return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    """Command-line interface for the research lookup tool."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Research Information Lookup Tool (Parallel + Perplexity)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # General research (uses Parallel Deep Research)
  python research_lookup.py "latest advances in quantum computing 2025"

  # Academic paper search (auto-routes to Perplexity)
  python research_lookup.py "find papers on CRISPR gene editing clinical trials"

  # Force a specific backend
  python research_lookup.py "topic" --force-backend parallel
  python research_lookup.py "topic" --force-backend perplexity

  # Save output to file
  python research_lookup.py "topic" -o results.txt

  # JSON output
  python research_lookup.py "topic" --json -o results.json
        """,
    )
    parser.add_argument("query", nargs="?", help="Research query to look up")
    parser.add_argument("--batch", nargs="+", help="Run multiple queries")
    parser.add_argument(
        "--force-backend",
        choices=["parallel", "perplexity"],
        help="Force a specific backend (default: auto-select)",
    )
    parser.add_argument("-o", "--output", help="Write output to file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    output_file = None
    if args.output:
        output_file = open(args.output, "w", encoding="utf-8")

    def write_output(text):
        if output_file:
            output_file.write(text + "\n")
        else:
            print(text)

    # Check for at least one API key
    has_parallel = bool(os.getenv("PARALLEL_API_KEY"))
    has_perplexity = bool(os.getenv("OPENROUTER_API_KEY"))
    if not has_parallel and not has_perplexity:
        print("Error: No API keys found. Set at least one:", file=sys.stderr)
        print("  export PARALLEL_API_KEY='...'    (primary - Parallel Deep Research)", file=sys.stderr)
        print("  export OPENROUTER_API_KEY='...'   (fallback - Perplexity academic)", file=sys.stderr)
        if output_file:
            output_file.close()
        return 1

    if not args.query and not args.batch:
        parser.print_help()
        if output_file:
            output_file.close()
        return 1

    try:
        research = ResearchLookup(force_backend=args.force_backend)

        if args.batch:
            print(f"Running batch research for {len(args.batch)} queries...", file=sys.stderr)
            results = research.batch_lookup(args.batch)
        else:
            print(f"Researching: {args.query}", file=sys.stderr)
            results = [research.lookup(args.query)]

        if args.json:
            write_output(json.dumps(results, indent=2, ensure_ascii=False, default=str))
            if output_file:
                output_file.close()
            return 0

        for i, result in enumerate(results):
            if result["success"]:
                write_output(f"\n{'='*80}")
                write_output(f"Query {i+1}: {result['query']}")
                write_output(f"Timestamp: {result['timestamp']}")
                write_output(f"Backend: {result.get('backend', 'unknown')} | Model: {result.get('model', 'unknown')}")
                if result.get("run_id"):
                    write_output(f"Run ID: {result['run_id']}")
                write_output(f"{'='*80}")
                write_output(result["response"])

                sources = result.get("sources", [])
                if sources:
                    write_output(f"\nSources ({len(sources)}):")
                    for j, source in enumerate(sources):
                        title = source.get("title", "Untitled")
                        url = source.get("url", "")
                        date = source.get("date", "")
                        date_str = f" ({date})" if date else ""
                        write_output(f"  [{j+1}] {title}{date_str}")
                        if url:
                            write_output(f"      {url}")

                citations = result.get("citations", [])
                text_citations = [c for c in citations if c.get("type") in ("doi", "url")]
                if text_citations:
                    write_output(f"\nAdditional References ({len(text_citations)}):")
                    for j, citation in enumerate(text_citations):
                        if citation.get("type") == "doi":
                            write_output(f"  [{j+1}] DOI: {citation.get('doi', '')} - {citation.get('url', '')}")
                        elif citation.get("type") == "url":
                            write_output(f"  [{j+1}] {citation.get('url', '')}")

                if result.get("usage"):
                    write_output(f"\nUsage: {result['usage']}")
            else:
                write_output(f"\nError in query {i+1}: {result['error']}")

        if output_file:
            output_file.close()
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if output_file:
            output_file.close()
        return 1


if __name__ == "__main__":
    sys.exit(main())
