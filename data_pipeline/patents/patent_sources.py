"""
PatentBrief patent source.

PatentBrief provides free public JSON endpoints with no API key.
The public corpus is a curated collection of explained US patents.

Docs:
https://patentbrief.org/api-page
https://patentbrief.org/developers
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import requests


class PatentSources:
    """Client for the public PatentBrief dataset."""

    BASE_URL = "https://patentbrief.org"

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Revianta-AI/1.0",
                "Accept": "application/json",
            }
        )

        self._index_cache: Optional[List[Dict[str, Any]]] = None

    # ---------------------------------------------------------
    # Load complete PatentBrief index
    # ---------------------------------------------------------

    def _load_index(self) -> List[Dict[str, Any]]:
        """Download and cache the complete PatentBrief index."""

        if self._index_cache is not None:
            return self._index_cache

        url = f"{self.BASE_URL}/patents.json"

        response = self.session.get(
            url,
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()

        if isinstance(data, dict):
            records = data.get("records", [])
        elif isinstance(data, list):
            records = data
        else:
            raise RuntimeError(
                "Unexpected PatentBrief response format."
            )

        if not isinstance(records, list):
            raise RuntimeError(
                "PatentBrief records field is not a list."
            )

        self._index_cache = records

        return records

    # ---------------------------------------------------------
    # Normalize patent record
    # ---------------------------------------------------------

    def _normalize(self, patent: Dict[str, Any]) -> Dict[str, Any]:
        """Convert PatentBrief data into Revianta's common schema."""

        patent_number = patent.get("patent_number", "")

        country = patent.get("country", "US")

        title = patent.get("title", "")

        assignee = patent.get(
            "assignee",
            patent.get("holder", ""),
        )

        grant_year = patent.get("grant_year")

        citation_count = patent.get(
            "times_cited",
            0,
        )

        url = patent.get("url", "")

        return {
            "source": "patentbrief",
            "external_id": patent_number,
            "publication_number": patent_number,
            "title": title,
            "abstract": "",
            "summary": "",
            "inventors": [],
            "assignee": assignee,
            "filing_date": None,
            "publication_date": None,
            "grant_year": grant_year,
            "priority_date": None,
            "country": country,
            "kind": None,
            "url": url,
            "type": "patent",
            "citation_count": citation_count,
        }

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def search_patents(
        self,
        query: str,
        max_results: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Search the PatentBrief public corpus locally.

        Searches:
        - patent title
        - assignee / holder
        - patent number

        Results are ranked by simple textual relevance.
        """

        if not query or not query.strip():
            return []

        query = query.strip().lower()

        query_terms = [
            term
            for term in query.split()
            if term
        ]

        records = self._load_index()

        scored_results = []

        for patent in records:

            title = str(
                patent.get("title", "")
            ).lower()

            assignee = str(
                patent.get(
                    "assignee",
                    patent.get("holder", ""),
                )
            ).lower()

            patent_number = str(
                patent.get(
                    "patent_number",
                    "",
                )
            ).lower()

            searchable_text = (
                f"{title} "
                f"{assignee} "
                f"{patent_number}"
            )

            score = 0

            # Exact phrase match
            if query in title:
                score += 10

            if query in assignee:
                score += 5

            # Individual term matches
            for term in query_terms:

                if term in title:
                    score += 3

                if term in assignee:
                    score += 1

                if term in patent_number:
                    score += 1

            if score > 0:
                normalized = self._normalize(patent)

                scored_results.append(
                    (
                        score,
                        normalized,
                    )
                )

        scored_results.sort(
            key=lambda item: (
                -item[0],
                item[1]["title"],
            )
        )

        return [
            result
            for _, result in scored_results[:max_results]
        ]

    # ---------------------------------------------------------
    # Get individual patent
    # ---------------------------------------------------------

    def get_patent(
        self,
        country: str,
        patent_number: str,
        slug: str,
    ) -> Dict[str, Any]:
        """
        Retrieve detailed information for one PatentBrief patent.

        Example:
        country = "us"
        patent_number = "4405829"
        slug = "rsa-encryption"
        """

        url = (
            f"{self.BASE_URL}"
            f"/patent/{country.lower()}"
            f"/{patent_number}"
            f"/{slug}"
            f"/json"
        )

        response = self.session.get(
            url,
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()

        if not isinstance(data, dict):
            raise RuntimeError(
                "Unexpected PatentBrief patent response."
            )

        return data

    # ---------------------------------------------------------
    # Search and return raw records
    # ---------------------------------------------------------

    def search_raw(
        self,
        query: str,
        max_results: int = 10,
    ) -> List[Dict[str, Any]]:
        """Return raw PatentBrief records matching the query."""

        if not query or not query.strip():
            return []

        query = query.strip().lower()

        records = self._load_index()

        results = []

        for patent in records:

            title = str(
                patent.get("title", "")
            ).lower()

            assignee = str(
                patent.get(
                    "assignee",
                    patent.get("holder", ""),
                )
            ).lower()

            if query in title or query in assignee:
                results.append(patent)

            if len(results) >= max_results:
                break

        return results

    # ---------------------------------------------------------
    # Get complete dataset
    # ---------------------------------------------------------

    def get_all_patents(self) -> List[Dict[str, Any]]:
        """Return all normalized PatentBrief records."""

        records = self._load_index()

        return [
            self._normalize(record)
            for record in records
        ]

    # ---------------------------------------------------------
    # Flat search
    # ---------------------------------------------------------

    def search_flat(
        self,
        query: str,
        max_results: int = 10,
    ) -> List[Dict[str, Any]]:
        """Alias used by Revianta data-pipeline conventions."""

        return self.search_patents(
            query=query,
            max_results=max_results,
        )