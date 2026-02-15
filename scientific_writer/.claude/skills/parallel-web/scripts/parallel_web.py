#!/usr/bin/env python3
"""
Parallel Web Systems API Client

Provides web search, URL content extraction, and deep research capabilities
using the Parallel Web Systems API (https://docs.parallel.ai).

Three main classes:
  - ParallelSearch:       Web search with LLM-optimized excerpts
  - ParallelExtract:      URL content extraction to clean markdown
  - ParallelDeepResearch: Deep research via Task API with citations

Environment variable required:
  PARALLEL_API_KEY - Your Parallel API key from https://platform.parallel.ai
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from typing import Any, Dict, List, Optional


def _get_client():
    """Create and return a Parallel client, handling import and key validation."""
    try:
        from parallel import Parallel
    except ImportError:
        raise ImportError(
            "The 'parallel-web' package is required. Install it with:\n"
            "  pip install parallel-web"
        )

    api_key = os.getenv("PARALLEL_API_KEY")
    if not api_key:
        raise ValueError(
            "PARALLEL_API_KEY environment variable not set.\n"
            "Get your key at https://platform.parallel.ai and set it:\n"
            "  export PARALLEL_API_KEY='your_key_here'"
        )
    return Parallel(api_key=api_key)


class ParallelSearch:
    """Web search using Parallel's Search API.

    Returns ranked, LLM-optimized excerpts from web sources based on
    natural language objectives or keyword queries.
    """

    def __init__(self):
        self.client = _get_client()

    def search(
        self,
        objective: str,
        search_queries: Optional[List[str]] = None,
        max_results: int = 10,
        max_chars_per_result: int = 10000,
        source_policy: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute a web search.

        Args:
            objective: Natural language description of the search goal.
            search_queries: Optional keyword queries to supplement the objective.
            max_results: Maximum number of results (1-20, default 10).
            max_chars_per_result: Max characters per excerpt (default 10000).
            source_policy: Optional source policy dict for domain filtering.

        Returns:
            Dict with 'results' list containing url, title, excerpts, etc.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        kwargs = {
            "objective": objective,
            "max_results": max_results,
            "excerpts": {"max_chars_per_result": max_chars_per_result},
        }
        if search_queries:
            kwargs["search_queries"] = search_queries
        if source_policy:
            kwargs["source_policy"] = source_policy

        try:
            response = self.client.beta.search(**kwargs)

            results = []
            if hasattr(response, "results") and response.results:
                for r in response.results:
                    result = {
                        "url": getattr(r, "url", ""),
                        "title": getattr(r, "title", ""),
                        "publish_date": getattr(r, "publish_date", None),
                        "excerpts": getattr(r, "excerpts", []),
                    }
                    results.append(result)

            return {
                "success": True,
                "objective": objective,
                "results": results,
                "result_count": len(results),
                "timestamp": timestamp,
                "search_id": getattr(response, "search_id", None),
            }

        except Exception as e:
            return {
                "success": False,
                "objective": objective,
                "error": str(e),
                "timestamp": timestamp,
            }


class ParallelExtract:
    """Extract clean content from URLs using Parallel's Extract API.

    Converts any public URL into clean, LLM-optimized markdown including
    JavaScript-heavy pages and PDFs.
    """

    def __init__(self):
        self.client = _get_client()

    def extract(
        self,
        urls: List[str],
        objective: Optional[str] = None,
        excerpts: bool = True,
        full_content: bool = False,
    ) -> Dict[str, Any]:
        """Extract content from one or more URLs.

        Args:
            urls: List of URLs to extract content from.
            objective: Optional objective to focus extraction.
            excerpts: Whether to return focused excerpts (default True).
            full_content: Whether to return full page content (default False).

        Returns:
            Dict with 'results' list containing url, title, excerpts/content.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        kwargs = {
            "urls": urls,
            "excerpts": excerpts,
            "full_content": full_content,
        }
        if objective:
            kwargs["objective"] = objective

        try:
            response = self.client.beta.extract(**kwargs)

            results = []
            if hasattr(response, "results") and response.results:
                for r in response.results:
                    result = {
                        "url": getattr(r, "url", ""),
                        "title": getattr(r, "title", ""),
                        "publish_date": getattr(r, "publish_date", None),
                        "excerpts": getattr(r, "excerpts", []),
                        "full_content": getattr(r, "full_content", None),
                    }
                    results.append(result)

            errors = []
            if hasattr(response, "errors") and response.errors:
                errors = [str(e) for e in response.errors]

            return {
                "success": True,
                "urls": urls,
                "results": results,
                "errors": errors,
                "timestamp": timestamp,
                "extract_id": getattr(response, "extract_id", None),
            }

        except Exception as e:
            return {
                "success": False,
                "urls": urls,
                "error": str(e),
                "timestamp": timestamp,
            }


class ParallelDeepResearch:
    """Deep research using Parallel's Task API.

    Transforms natural language research queries into comprehensive
    intelligence reports with citations, reasoning, and confidence levels.

    Processor guide:
      - pro-fast     (default): 30s-5min, exploratory web research, fast
      - pro          : 2-10min, exploratory web research, freshest data
      - ultra-fast   : 1-10min, advanced multi-source deep research, fast
      - ultra        : 5-25min, advanced multi-source deep research
      - core-fast    : 15s-100s, cross-referenced moderately complex outputs
      - base-fast    : 15s-50s, reliable standard enrichments
    """

    # Default timeout for polling (1 hour)
    DEFAULT_TIMEOUT = 3600

    def __init__(self):
        self.client = _get_client()

    def research(
        self,
        query: str,
        processor: str = "pro-fast",
        timeout: int = DEFAULT_TIMEOUT,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Run deep research and return a markdown text report.

        Args:
            query: The research question or topic (max 15,000 chars).
            processor: Task API processor to use (default 'pro-fast').
            timeout: Max seconds to wait for results (default 3600).
            description: Optional description to guide report output.

        Returns:
            Dict with 'output' (markdown text), 'citations', and metadata.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            from parallel.types import TaskSpecParam

            task_spec_kwargs = {}
            text_schema = {"type": "text"}
            if description:
                text_schema["description"] = description
            task_spec_kwargs["output_schema"] = text_schema

            task_run = self.client.task_run.create(
                input=query,
                processor=processor,
                task_spec=TaskSpecParam(**task_spec_kwargs),
            )

            run_id = task_run.run_id
            print(f"[Parallel] Deep research started: {run_id} (processor: {processor})", file=sys.stderr)

            run_result = self.client.task_run.result(run_id, api_timeout=timeout)

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
                                citation = {
                                    "type": "source",
                                    "url": getattr(cit, "url", ""),
                                    "title": getattr(cit, "title", ""),
                                    "excerpts": getattr(cit, "excerpts", []),
                                }
                                citations.append(citation)

            return {
                "success": True,
                "query": query,
                "response": output_text,
                "output": output_text,  # alias for backward compat
                "citations": citations,
                "sources": citations,   # alias matching research_lookup format
                "citation_count": len(citations),
                "run_id": run_id,
                "processor": processor,
                "backend": "parallel",
                "model": f"parallel/{processor}",
                "timestamp": timestamp,
            }

        except Exception as e:
            return {
                "success": False,
                "query": query,
                "error": str(e),
                "processor": processor,
                "timestamp": timestamp,
            }

    def research_structured(
        self,
        query: str,
        processor: str = "pro-fast",
        output_schema: Optional[Dict[str, Any]] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> Dict[str, Any]:
        """Run deep research and return structured JSON output.

        Uses auto-schema mode by default, which lets the processor determine
        the best output structure. You can also provide a custom JSON schema.

        Args:
            query: The research question or topic (max 15,000 chars).
            processor: Task API processor to use (default 'pro-fast').
            output_schema: Optional JSON schema dict for structured output.
            timeout: Max seconds to wait for results (default 3600).

        Returns:
            Dict with 'content' (structured data), 'basis' (citations), metadata.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            create_kwargs = {
                "input": query,
                "processor": processor,
            }

            if output_schema:
                from parallel.types import TaskSpecParam
                create_kwargs["task_spec"] = TaskSpecParam(
                    output_schema={"type": "json", "json_schema": output_schema}
                )
            # else: auto-schema mode (default for pro/ultra processors)

            task_run = self.client.task_run.create(**create_kwargs)
            run_id = task_run.run_id
            print(f"[Parallel] Structured research started: {run_id} (processor: {processor})", file=sys.stderr)

            run_result = self.client.task_run.result(run_id, api_timeout=timeout)

            content = None
            basis = []

            if hasattr(run_result, "output"):
                output = run_result.output
                if hasattr(output, "content"):
                    content = output.content
                if hasattr(output, "basis") and output.basis:
                    for b in output.basis:
                        basis_entry = {
                            "field": getattr(b, "field", ""),
                            "reasoning": getattr(b, "reasoning", ""),
                            "confidence": getattr(b, "confidence", ""),
                            "citations": [],
                        }
                        if hasattr(b, "citations") and b.citations:
                            for cit in b.citations:
                                basis_entry["citations"].append({
                                    "type": "source",
                                    "url": getattr(cit, "url", ""),
                                    "title": getattr(cit, "title", ""),
                                    "excerpts": getattr(cit, "excerpts", []),
                                })
                        basis.append(basis_entry)

            return {
                "success": True,
                "query": query,
                "content": content,
                "basis": basis,
                "run_id": run_id,
                "processor": processor,
                "timestamp": timestamp,
            }

        except Exception as e:
            return {
                "success": False,
                "query": query,
                "error": str(e),
                "processor": processor,
                "timestamp": timestamp,
            }


# ---------------------------------------------------------------------------
# CLI Interface
# ---------------------------------------------------------------------------

def _print_search_results(result: Dict[str, Any], output_file=None):
    """Pretty-print search results."""
    def write(text):
        if output_file:
            output_file.write(text + "\n")
        else:
            print(text)

    if not result["success"]:
        write(f"Error: {result.get('error', 'Unknown error')}")
        return

    write(f"\n{'='*80}")
    write(f"Search: {result['objective']}")
    write(f"Results: {result['result_count']} | Time: {result['timestamp']}")
    write(f"{'='*80}")

    for i, r in enumerate(result["results"]):
        write(f"\n[{i+1}] {r['title']}")
        write(f"    URL: {r['url']}")
        if r.get("publish_date"):
            write(f"    Date: {r['publish_date']}")
        if r.get("excerpts"):
            excerpt = r["excerpts"][0] if isinstance(r["excerpts"], list) else str(r["excerpts"])
            if len(excerpt) > 300:
                excerpt = excerpt[:300] + "..."
            write(f"    Excerpt: {excerpt}")


def _print_extract_results(result: Dict[str, Any], output_file=None):
    """Pretty-print extract results."""
    def write(text):
        if output_file:
            output_file.write(text + "\n")
        else:
            print(text)

    if not result["success"]:
        write(f"Error: {result.get('error', 'Unknown error')}")
        return

    write(f"\n{'='*80}")
    write(f"Extracted from: {', '.join(result['urls'])}")
    write(f"Time: {result['timestamp']}")
    write(f"{'='*80}")

    for i, r in enumerate(result["results"]):
        write(f"\n--- [{i+1}] {r['title']} ---")
        write(f"URL: {r['url']}")
        if r.get("full_content"):
            write(f"\n{r['full_content']}")
        elif r.get("excerpts"):
            for j, excerpt in enumerate(r["excerpts"]):
                write(f"\nExcerpt {j+1}:")
                write(excerpt[:2000] if len(excerpt) > 2000 else excerpt)

    if result.get("errors"):
        write(f"\nErrors: {result['errors']}")


def _print_research_results(result: Dict[str, Any], output_file=None):
    """Pretty-print deep research results."""
    def write(text):
        if output_file:
            output_file.write(text + "\n")
        else:
            print(text)

    if not result["success"]:
        write(f"Error: {result.get('error', 'Unknown error')}")
        return

    write(f"\n{'='*80}")
    write(f"Research: {result['query'][:100]}...")
    write(f"Processor: {result['processor']} | Run: {result.get('run_id', 'N/A')}")
    write(f"Citations: {result.get('citation_count', 0)} | Time: {result['timestamp']}")
    write(f"{'='*80}\n")

    write(result.get("response", result.get("output", "No output received.")))

    citations = result.get("citations", [])
    if citations:
        write(f"\n\n{'='*40} SOURCES {'='*40}")
        seen_urls = set()
        for i, cit in enumerate(citations):
            url = cit.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                title = cit.get("title", "Untitled")
                write(f"  [{len(seen_urls)}] {title}")
                write(f"      {url}")


def main():
    parser = argparse.ArgumentParser(
        description="Parallel Web Systems API Client - Search, Extract, and Deep Research",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python parallel_web.py search "latest advances in quantum computing"
  python parallel_web.py search "climate policy 2025" --queries "Paris agreement updates" "carbon tax"
  python parallel_web.py extract "https://example.com" --objective "key findings"
  python parallel_web.py research "comprehensive analysis of EV battery market"
  python parallel_web.py research "compare mRNA vs protein subunit vaccines" --processor ultra-fast
  python parallel_web.py research "AI regulation landscape 2025" -o report.md
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="API command")

    # --- search subcommand ---
    search_parser = subparsers.add_parser("search", help="Web search with LLM-optimized excerpts")
    search_parser.add_argument("objective", help="Natural language search objective")
    search_parser.add_argument("--queries", nargs="+", help="Additional search keyword queries")
    search_parser.add_argument("--max-results", type=int, default=10, help="Max results (1-20, default 10)")
    search_parser.add_argument("-o", "--output", help="Write output to file")
    search_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # --- extract subcommand ---
    extract_parser = subparsers.add_parser("extract", help="Extract content from URLs")
    extract_parser.add_argument("urls", nargs="+", help="One or more URLs to extract")
    extract_parser.add_argument("--objective", help="Objective to focus extraction")
    extract_parser.add_argument("--full-content", action="store_true", help="Return full page content")
    extract_parser.add_argument("-o", "--output", help="Write output to file")
    extract_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # --- research subcommand ---
    research_parser = subparsers.add_parser("research", help="Deep research via Task API")
    research_parser.add_argument("query", help="Research question or topic")
    research_parser.add_argument("--processor", default="pro-fast",
                                  choices=["lite-fast", "base-fast", "core-fast", "pro-fast",
                                           "ultra-fast", "lite", "base", "core", "pro", "ultra",
                                           "ultra2x", "ultra2x-fast", "ultra4x", "ultra4x-fast"],
                                  help="Processor to use (default: pro-fast)")
    research_parser.add_argument("--structured", action="store_true", help="Return structured JSON (auto-schema)")
    research_parser.add_argument("--timeout", type=int, default=3600, help="Max wait time in seconds (default 3600)")
    research_parser.add_argument("-o", "--output", help="Write output to file")
    research_parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    output_file = None
    if hasattr(args, "output") and args.output:
        output_file = open(args.output, "w", encoding="utf-8")

    try:
        if args.command == "search":
            searcher = ParallelSearch()
            result = searcher.search(
                objective=args.objective,
                search_queries=args.queries,
                max_results=args.max_results,
            )
            if args.json:
                text = json.dumps(result, indent=2, ensure_ascii=False, default=str)
                (output_file or sys.stdout).write(text + "\n")
            else:
                _print_search_results(result, output_file)

        elif args.command == "extract":
            extractor = ParallelExtract()
            result = extractor.extract(
                urls=args.urls,
                objective=args.objective,
                full_content=args.full_content,
            )
            if args.json:
                text = json.dumps(result, indent=2, ensure_ascii=False, default=str)
                (output_file or sys.stdout).write(text + "\n")
            else:
                _print_extract_results(result, output_file)

        elif args.command == "research":
            researcher = ParallelDeepResearch()
            if args.structured:
                result = researcher.research_structured(
                    query=args.query,
                    processor=args.processor,
                    timeout=args.timeout,
                )
            else:
                result = researcher.research(
                    query=args.query,
                    processor=args.processor,
                    timeout=args.timeout,
                )
            if args.json:
                text = json.dumps(result, indent=2, ensure_ascii=False, default=str)
                (output_file or sys.stdout).write(text + "\n")
            else:
                _print_research_results(result, output_file)

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    finally:
        if output_file:
            output_file.close()


if __name__ == "__main__":
    sys.exit(main())
