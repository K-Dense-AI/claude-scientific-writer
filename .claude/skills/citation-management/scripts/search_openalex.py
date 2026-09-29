#!/usr/bin/env python3
"""
OpenAlex Search Tool
Search OpenAlex and export results as JSON or BibTeX.

OpenAlex indexes ~250 million scholarly works across every discipline, needs no
API key, and has a documented REST API rather than a scraped HTML surface. It
is the third leg of this skill's coverage: PubMed is authoritative for
biomedicine, Google Scholar is broad but fragile and rate-limited, and OpenAlex
is broad, stable, and machine-readable.

Setting OPENALEX_EMAIL (or passing --email) joins OpenAlex's "polite pool",
which is faster and more reliably available. The address is sent to
api.openalex.org only, as a query parameter, exactly as OpenAlex documents.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Dict, List, Optional

import requests

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    citation_key,
    format_pages,
    protect_title,
    render_entry,
)

API_URL = 'https://api.openalex.org/works'

# OpenAlex work types -> BibTeX entry types.
TYPE_MAP = {
    'article': 'article',
    'journal-article': 'article',
    'review': 'article',
    'book': 'book',
    'book-chapter': 'incollection',
    'monograph': 'book',
    'proceedings-article': 'inproceedings',
    'proceedings': 'inproceedings',
    'dissertation': 'phdthesis',
    'report': 'techreport',
    'preprint': 'misc',
    'posted-content': 'misc',
    'dataset': 'misc',
}


class OpenAlexSearcher:
    """Search OpenAlex via its public REST API."""

    def __init__(self, email: Optional[str] = None):
        self.email = email or os.getenv('OPENALEX_EMAIL', '')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'OpenAlexSearcher/1.0 (Citation Management Tool)'
        })

    def search(self, query: str, max_results: int = 50,
               year_start: Optional[int] = None, year_end: Optional[int] = None,
               work_type: Optional[str] = None,
               sort_by: str = 'relevance') -> List[Dict]:
        """
        Search OpenAlex and return normalised metadata records.

        Args:
            query: Free-text search query
            max_results: Maximum number of works to return
            year_start: Earliest publication year, inclusive
            year_end: Latest publication year, inclusive
            work_type: OpenAlex work type filter (e.g. 'article', 'review')
            sort_by: 'relevance' or 'citations'

        Returns:
            List of metadata dictionaries
        """
        filters = []
        if year_start:
            filters.append(f'from_publication_date:{year_start}-01-01')
        if year_end:
            filters.append(f'to_publication_date:{year_end}-12-31')
        if work_type:
            filters.append(f'type:{work_type}')

        params = {
            'search': query,
            'per-page': str(min(200, max_results)),
            'cursor': '*',
        }
        if filters:
            params['filter'] = ','.join(filters)
        if sort_by == 'citations':
            params['sort'] = 'cited_by_count:desc'
        if self.email:
            params['mailto'] = self.email

        print(f'Searching OpenAlex: {query}', file=sys.stderr)

        results: List[Dict] = []
        reported_total = False

        while len(results) < max_results:
            try:
                response = self.session.get(API_URL, params=params, timeout=30)
                response.raise_for_status()
                payload = response.json()
            except requests.exceptions.RequestException as e:
                print(f'Error searching OpenAlex: {e}', file=sys.stderr)
                break
            except ValueError as e:
                print(f'Error: OpenAlex returned invalid JSON: {e}', file=sys.stderr)
                break

            if not reported_total:
                total = payload.get('meta', {}).get('count', 0)
                print(f'Found {total} results, retrieving up to {max_results}', file=sys.stderr)
                reported_total = True

            works = payload.get('results', [])
            if not works:
                break

            for work in works:
                results.append(self._normalise(work))
                if len(results) >= max_results:
                    break

            next_cursor = payload.get('meta', {}).get('next_cursor')
            if not next_cursor or len(results) >= max_results:
                break
            params['cursor'] = next_cursor

            # OpenAlex asks for courteous pacing even in the polite pool.
            time.sleep(0.1)

        print(f'Retrieved {len(results)} results', file=sys.stderr)
        return results

    def _normalise(self, work: Dict) -> Dict:
        """Flatten one OpenAlex work into this skill's metadata shape."""
        authors = [
            authorship.get('author', {}).get('display_name', '')
            for authorship in work.get('authorships', [])
        ]
        authors = [name for name in authors if name]

        location = work.get('primary_location') or {}
        source = location.get('source') or {}
        biblio = work.get('biblio') or {}

        first_page = biblio.get('first_page') or ''
        last_page = biblio.get('last_page') or ''
        if first_page and last_page and first_page != last_page:
            pages = f'{first_page}-{last_page}'
        else:
            pages = first_page or ''

        doi = work.get('doi') or ''
        if doi.startswith('https://doi.org/'):
            doi = doi[len('https://doi.org/'):]

        return {
            'openalex_id': work.get('id', ''),
            'doi': doi,
            'title': work.get('title') or work.get('display_name') or '',
            'authors': ' and '.join(authors),
            'journal': source.get('display_name', '') or '',
            'publisher': source.get('host_organization_name', '') or '',
            'year': str(work.get('publication_year') or ''),
            'volume': biblio.get('volume') or '',
            'issue': biblio.get('issue') or '',
            'pages': pages,
            'type': work.get('type') or '',
            'citations': work.get('cited_by_count', 0),
            'is_open_access': (work.get('open_access') or {}).get('is_oa', False),
            'abstract': self._abstract(work.get('abstract_inverted_index')),
        }

    @staticmethod
    def _abstract(inverted_index: Optional[Dict]) -> str:
        """Rebuild the abstract from OpenAlex's inverted index."""
        if not inverted_index:
            return ''
        positions = []
        for word, indices in inverted_index.items():
            for index in indices:
                positions.append((index, word))
        positions.sort()
        return ' '.join(word for _, word in positions)

    def metadata_to_bibtex(self, metadata: Dict) -> str:
        """Convert a normalised record to a BibTeX entry."""
        entry_type = TYPE_MAP.get(metadata.get('type', ''), 'misc')

        key = citation_key(
            metadata.get('authors', ''),
            metadata.get('year', ''),
            metadata.get('title', ''),
        )

        fields = {
            'author': metadata.get('authors', ''),
            'title': protect_title(metadata.get('title', '')),
            'year': metadata.get('year', ''),
            'volume': metadata.get('volume', ''),
            'number': metadata.get('issue', ''),
            'pages': format_pages(metadata.get('pages')),
            'doi': metadata.get('doi', ''),
        }

        venue = metadata.get('journal', '')
        if entry_type in ('inproceedings', 'incollection'):
            fields['booktitle'] = venue
        elif entry_type != 'misc':
            fields['journal'] = venue

        if entry_type in ('book', 'incollection', 'inproceedings'):
            fields['publisher'] = metadata.get('publisher', '')
        elif entry_type == 'techreport':
            fields['institution'] = metadata.get('publisher', '')

        if entry_type == 'misc':
            if venue:
                fields['howpublished'] = venue
            fields['note'] = 'Preprint'

        if not fields['doi'] and metadata.get('openalex_id'):
            fields['url'] = metadata['openalex_id']

        return render_entry(entry_type, key, fields)


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description='Search OpenAlex (no API key required)',
        epilog='Example: python search_openalex.py "CRISPR gene editing" --limit 50 --format bibtex'
    )

    parser.add_argument('query', help='Search query')
    parser.add_argument('--limit', type=int, default=50,
                        help='Maximum number of results (default: 50)')
    parser.add_argument('--year-start', type=int, help='Earliest publication year')
    parser.add_argument('--year-end', type=int, help='Latest publication year')
    parser.add_argument('--type', dest='work_type',
                        help='OpenAlex work type filter (e.g. article, review, preprint)')
    parser.add_argument('--sort-by', choices=['relevance', 'citations'], default='relevance',
                        help='Sort order (default: relevance)')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('--format', choices=['json', 'bibtex'], default='json',
                        help='Output format (default: json)')
    parser.add_argument('--email',
                        help='Contact email for the OpenAlex polite pool (or set OPENALEX_EMAIL)')

    args = parser.parse_args()

    searcher = OpenAlexSearcher(email=args.email)
    results = searcher.search(
        args.query,
        max_results=args.limit,
        year_start=args.year_start,
        year_end=args.year_end,
        work_type=args.work_type,
        sort_by=args.sort_by,
    )

    if not results:
        print('No results found', file=sys.stderr)
        sys.exit(1)

    if args.format == 'json':
        output = json.dumps({
            'query': args.query,
            'count': len(results),
            'results': results,
        }, indent=2)
    else:
        output = '\n\n'.join(searcher.metadata_to_bibtex(r) for r in results) + '\n'

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f'Wrote {len(results)} results to {args.output}', file=sys.stderr)
    else:
        print(output)


if __name__ == '__main__':
    main()
