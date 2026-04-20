#!/usr/bin/env python3
"""
Research Information Lookup Tool

Routes research queries to the best backend:
  - parallel-cli search: Primary backend for all queries (fast, cost-effective)
  - Parallel Chat API (core model): Deep research requiring multi-source synthesis

Environment variables:
  PARALLEL_API_KEY    - Required for Parallel Chat API (deep research backend)
"""

import os
import sys
import json
import re
import subprocess
import time
import requests
from datetime import datetime
from typing import Any, Dict, List, Optional


ACADEMIC_DOMAINS = (
    "scholar.google.com,arxiv.org,pubmed.ncbi.nlm.nih.gov,semanticscholar.org,"
    "biorxiv.org,medrxiv.org,ncbi.nlm.nih.gov,nature.com,science.org,ieee.org,"
    "acm.org,springer.com,wiley.com,cell.com,pnas.org,nih.gov"
)

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

DEEP_RESEARCH_KEYWORDS = [
    "deep research", "exhaustive", "comprehensive review",
    "multi-source", "thorough analysis",
]

PARALLEL_SYSTEM_PROMPT = (
    "You are a deep research analyst. Provide a comprehensive, well-cited "
    "research report on the user's topic. Include:\n"
    "- Key findings with specific data, statistics, and quantitative evidence\n"
    "- Detailed analysis organized by themes\n"
    "- Multiple authoritative sources cited inline\n"
    "- Methodologies and implications where relevant\n"
    "- Future outlook and research gaps\n"
    "Use markdown formatting with clear section headers. "
    "Prioritize authoritative and recent sources."
)

CHAT_BASE_URL = "https://api.parallel.ai"


class ResearchLookup:
    """Research information lookup with intelligent backend routing.

    Routes queries to parallel-cli search (default, fast) or the
    Parallel Chat API (deep research only).
    """

    def __init__(self, force_backend: Optional[str] = None):
        """Initialize the research lookup tool.

        Args:
            force_backend: Force a specific backend ('parallel-cli' or 'parallel-chat').
                          If None, backend is auto-selected based on query content.
        """
        self.force_backend = force_backend
        self.parallel_chat_available = bool(os.getenv("PARALLEL_API_KEY"))
        self.parallel_cli_available = self._check_parallel_cli()

        if not self.parallel_cli_available and not self.parallel_chat_available:
            raise ValueError(
                "No backend available. Set at least one of:\n"
                "  Install parallel-cli (primary backend)\n"
                "  PARALLEL_API_KEY (for deep research via Parallel Chat API)"
            )

    def _check_parallel_cli(self) -> bool:
        """Check if parallel-cli is installed and available."""
        try:
            result = subprocess.run(
                ["parallel-cli", "--version"],
                capture_output=True, text=True, timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def _select_backend(self, query: str) -> str:
        """Select the best backend for a query."""
        if self.force_backend:
            if self.force_backend == "parallel-chat" and self.parallel_chat_available:
                return "parallel-chat"
            if self.force_backend == "parallel-cli" and self.parallel_cli_available:
                return "parallel-cli"

        query_lower = query.lower()
        is_deep = any(kw in query_lower for kw in DEEP_RESEARCH_KEYWORDS)

        if is_deep and self.parallel_chat_available:
            return "parallel-chat"

        if self.parallel_cli_available:
            return "parallel-cli"

        if self.parallel_chat_available:
            return "parallel-chat"

        raise ValueError("No backend available. Check parallel-cli installation or PARALLEL_API_KEY.")

    # ------------------------------------------------------------------
    # parallel-cli search backend (primary)
    # ------------------------------------------------------------------

    def _parallel_cli_lookup(self, query: str) -> Dict[str, Any]:
        """Run research via parallel-cli search (primary backend)."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query_lower = query.lower()
        is_academic = any(kw in query_lower for kw in ACADEMIC_KEYWORDS)

        try:
            all_results = []

            if is_academic:
                # Two-search pattern for academic queries
                print("[Research] parallel-cli search (academic domains)...", file=sys.stderr)
                academic_result = self._run_parallel_cli_search(
                    query,
                    include_domains=ACADEMIC_DOMAINS,
                    max_results=10,
                )
                all_results.extend(academic_result)

            # General search (always run for non-academic; supplemental for academic)
            print("[Research] parallel-cli search (general)...", file=sys.stderr)
            general_result = self._run_parallel_cli_search(query, max_results=10)
            # Deduplicate by URL
            existing_urls = {r.get("url") for r in all_results}
            for r in general_result:
                if r.get("url") not in existing_urls:
                    all_results.append(r)
                    existing_urls.add(r.get("url"))

            response_text = self._format_cli_results(query, all_results)
            sources = [
                {"type": "source", "title": r.get("title", ""), "url": r.get("url", ""),
                 "date": r.get("date", ""), "snippet": r.get("snippet", "")}
                for r in all_results
            ]

            return {
                "success": True,
                "query": query,
                "response": response_text,
                "citations": sources,
                "sources": sources,
                "timestamp": timestamp,
                "backend": "parallel-cli",
                "model": "parallel-cli/search",
            }

        except Exception as e:
            return {
                "success": False,
                "query": query,
                "error": str(e),
                "timestamp": timestamp,
                "backend": "parallel-cli",
                "model": "parallel-cli/search",
            }

    def _run_parallel_cli_search(
        self,
        query: str,
        include_domains: Optional[str] = None,
        max_results: int = 10,
        after_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Execute a parallel-cli search and return parsed results."""
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            out_path = f.name

        cmd = [
            "parallel-cli", "search", query,
            "--json",
            "--max-results", str(max_results),
            "--excerpt-max-chars-total", "27000",
            "-o", out_path,
        ]
        if include_domains:
            cmd += ["--include-domains", include_domains]
        if after_date:
            cmd += ["--after-date", after_date]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        try:
            with open(out_path) as f:
                data = json.load(f)
            os.unlink(out_path)
            return data if isinstance(data, list) else data.get("results", [])
        except Exception:
            os.unlink(out_path)
            return []

    def _format_cli_results(self, query: str, results: List[Dict[str, Any]]) -> str:
        """Format parallel-cli results into a readable response."""
        if not results:
            return f"No results found for: {query}"

        lines = [f"## Research Results: {query}\n"]
        for i, r in enumerate(results, 1):
            title = r.get("title", "Untitled")
            url = r.get("url", "")
            snippet = r.get("snippet", "")
            date = r.get("date", "")
            date_str = f" ({date})" if date else ""
            lines.append(f"### [{i}] {title}{date_str}")
            if url:
                lines.append(f"**Source**: {url}")
            if snippet:
                lines.append(f"\n{snippet}\n")
            lines.append("")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Parallel Chat API backend (deep research only)
    # ------------------------------------------------------------------

    def _get_chat_client(self):
        """Lazy-load and cache the OpenAI client for Parallel Chat API."""
        if not hasattr(self, "_chat_client"):
            try:
                from openai import OpenAI
            except ImportError:
                raise ImportError(
                    "The 'openai' package is required for Parallel Chat API.\n"
                    "Install it with: pip install openai"
                )
            self._chat_client = OpenAI(
                api_key=os.getenv("PARALLEL_API_KEY"),
                base_url=CHAT_BASE_URL,
            )
        return self._chat_client

    def _parallel_chat_lookup(self, query: str) -> Dict[str, Any]:
        """Run deep research via the Parallel Chat API (core model)."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        model = "core"

        try:
            client = self._get_chat_client()
            print(f"[Research] Parallel Chat API (model={model}, deep research)...", file=sys.stderr)

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": PARALLEL_SYSTEM_PROMPT},
                    {"role": "user", "content": query},
                ],
                stream=False,
            )

            content = ""
            if response.choices and len(response.choices) > 0:
                content = response.choices[0].message.content or ""

            api_citations = self._extract_basis_citations(response)
            text_citations = self._extract_citations_from_text(content)

            return {
                "success": True,
                "query": query,
                "response": content,
                "citations": api_citations + text_citations,
                "sources": api_citations,
                "timestamp": timestamp,
                "backend": "parallel-chat",
                "model": f"parallel-chat/{model}",
            }

        except Exception as e:
            return {
                "success": False,
                "query": query,
                "error": str(e),
                "timestamp": timestamp,
                "backend": "parallel-chat",
                "model": f"parallel-chat/{model}",
            }

    def _extract_basis_citations(self, response) -> List[Dict[str, str]]:
        """Extract citation sources from the Chat API research basis."""
        citations = []
        basis = getattr(response, "basis", None)
        if not basis:
            return citations

        seen_urls = set()
        if isinstance(basis, list):
            for item in basis:
                cits = (
                    item.get("citations", []) if isinstance(item, dict)
                    else getattr(item, "citations", None) or []
                )
                for cit in cits:
                    url = cit.get("url", "") if isinstance(cit, dict) else getattr(cit, "url", "")
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        title = cit.get("title", "") if isinstance(cit, dict) else getattr(cit, "title", "")
                        excerpts = cit.get("excerpts", []) if isinstance(cit, dict) else getattr(cit, "excerpts", [])
                        citations.append({
                            "type": "source",
                            "url": url,
                            "title": title,
                            "excerpts": excerpts,
                        })
        return citations

    # ------------------------------------------------------------------
    # Shared utilities
    # ------------------------------------------------------------------

    def _extract_citations_from_text(self, text: str) -> List[Dict[str, str]]:
        """Extract DOIs and academic URLs from response text as fallback."""
        citations = []

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

        parallel-cli search is used by default (fast, cost-effective).
        Parallel Chat API is used only when deep/exhaustive research is requested.
        """
        backend = self._select_backend(query)
        print(f"[Research] Backend: {backend} | Query: {query[:80]}...", file=sys.stderr)

        if backend == "parallel-chat":
            return self._parallel_chat_lookup(query)
        else:
            return self._parallel_cli_lookup(query)

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
        description="Research Information Lookup Tool (parallel-cli search + Parallel Chat API)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # General research (uses parallel-cli search, fast)
  python research_lookup.py "latest advances in quantum computing 2025"

  # Academic paper search (uses parallel-cli with academic domains)
  python research_lookup.py "find papers on CRISPR gene editing clinical trials"

  # Deep research (uses Parallel Chat API - slow but comprehensive)
  python research_lookup.py "comprehensive review of mRNA vaccine mechanisms" --force-backend parallel-chat

  # Force a specific backend
  python research_lookup.py "topic" --force-backend parallel-cli
  python research_lookup.py "topic" --force-backend parallel-chat

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
        choices=["parallel-cli", "parallel-chat"],
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

    has_parallel_cli = True  # will be checked inside ResearchLookup
    has_parallel_chat = bool(os.getenv("PARALLEL_API_KEY"))

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
