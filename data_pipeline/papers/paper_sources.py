import requests
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional


class PaperSources:
    """
    Unified paper search client for:
    1. OpenAlex
    2. Semantic Scholar
    3. arXiv

    All sources return the same normalized paper structure.

    If one source fails, the other sources will still return
    their available results.
    """

    OPENALEX_URL = "https://api.openalex.org/works"

    SEMANTIC_SCHOLAR_URL = (
        "https://api.semanticscholar.org/graph/v1/paper/search"
    )

    ARXIV_URL = "https://export.arxiv.org/api/query"

    def __init__(
        self,
        mailto: Optional[str] = None,
        semantic_scholar_api_key: Optional[str] = None,
        timeout: int = 30
    ):
        self.mailto = mailto
        self.semantic_scholar_api_key = (
            semantic_scholar_api_key
        )
        self.timeout = timeout

    # ============================================================
    # COMMON HELPERS
    # ============================================================

    @staticmethod
    def _safe_text(
        value: Any
    ) -> Optional[str]:

        if value is None:
            return None

        value = str(value).strip()

        return value if value else None

    @staticmethod
    def _normalize_authors(
        authors: Any
    ) -> List[str]:

        result = []

        if not authors:
            return result

        for author in authors:

            if isinstance(author, str):
                name = author.strip()

            elif isinstance(author, dict):
                name = (
                    author.get("name")
                    or author.get("display_name")
                    or (
                        author.get("author") or {}
                    ).get("display_name")
                )

            else:
                name = None

            if name:
                result.append(name)

        return result

    # ============================================================
    # OPENALEX
    # ============================================================

    def search_openalex(
        self,
        query: str,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:

        if not query or not query.strip():
            raise ValueError(
                "OpenAlex query cannot be empty."
            )

        params = {
            "search": query.strip(),
            "per-page": min(
                max_results,
                100
            )
        }

        if self.mailto:
            params["mailto"] = self.mailto

        response = requests.get(
            self.OPENALEX_URL,
            params=params,
            timeout=self.timeout
        )

        response.raise_for_status()

        data = response.json()

        papers = []

        for work in data.get(
            "results",
            []
        ):

            papers.append(
                self._normalize_openalex(work)
            )

        return papers

    def _normalize_openalex(
        self,
        work: Dict[str, Any]
    ) -> Dict[str, Any]:

        primary_location = (
            work.get("primary_location")
            or {}
        )

        source = (
            primary_location.get("source")
            or {}
        )

        abstract = (
            self._extract_openalex_abstract(work)
        )

        authors = []

        for authorship in work.get(
            "authorships",
            []
        ):

            author = (
                authorship.get("author")
                or {}
            )

            name = author.get(
                "display_name"
            )

            if name:
                authors.append(name)

        keywords = []

        for item in work.get(
            "keywords",
            []
        ):

            name = item.get(
                "display_name"
            )

            if name:
                keywords.append(name)

        return {
            "source": "openalex",

            "external_id": work.get(
                "id"
            ),

            "title": self._safe_text(
                work.get("display_name")
                or work.get("title")
            ),

            "abstract": abstract,

            "authors": authors,

            "publication_year": work.get(
                "publication_year"
            ),

            "publication_date": work.get(
                "publication_date"
            ),

            "doi": work.get(
                "doi"
            ),

            "url": (
                primary_location.get(
                    "landing_page_url"
                )
                or work.get("id")
            ),

            "source_name": source.get(
                "display_name"
            ),

            "citation_count": work.get(
                "cited_by_count",
                0
            ),

            "type": work.get(
                "type"
            ),

            "open_access": (
                work.get(
                    "open_access"
                )
                or {}
            ).get(
                "is_oa",
                False
            ),

            "keywords": keywords,
        }

    @staticmethod
    def _extract_openalex_abstract(
        work: Dict[str, Any]
    ) -> Optional[str]:

        inverted_index = work.get(
            "abstract_inverted_index"
        )

        if not inverted_index:
            return None

        words = []

        for word, positions in (
            inverted_index.items()
        ):

            for position in positions:

                words.append(
                    (
                        position,
                        word
                    )
                )

        words.sort(
            key=lambda item: item[0]
        )

        return " ".join(
            word
            for _, word in words
        )

    # ============================================================
    # SEMANTIC SCHOLAR
    # ============================================================

    def search_semantic_scholar(
        self,
        query: str,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:

        if not query or not query.strip():
            raise ValueError(
                "Semantic Scholar query cannot be empty."
            )

        params = {
            "query": query.strip(),

            "limit": min(
                max_results,
                100
            ),

            "fields": (
                "paperId,title,abstract,authors,"
                "year,publicationDate,venue,"
                "citationCount,url,openAccessPdf,"
                "externalIds"
            )
        }

        headers = {}

        if self.semantic_scholar_api_key:

            headers["x-api-key"] = (
                self.semantic_scholar_api_key
            )

        response = requests.get(
            self.SEMANTIC_SCHOLAR_URL,
            params=params,
            headers=headers,
            timeout=self.timeout
        )

        # --------------------------------------------------------
        # Rate limit handling
        # --------------------------------------------------------

        if response.status_code == 429:

            retry_after = (
                response.headers.get(
                    "Retry-After"
                )
            )

            raise RuntimeError(
                "Semantic Scholar rate limit reached "
                "(HTTP 429). "
                f"Retry-After: "
                f"{retry_after or 'not provided'}. "
                "Please wait before trying again."
            )

        response.raise_for_status()

        data = response.json()

        papers = []

        for paper in data.get(
            "data",
            []
        ):

            papers.append(
                self._normalize_semantic_scholar(
                    paper
                )
            )

        return papers

    def _normalize_semantic_scholar(
        self,
        paper: Dict[str, Any]
    ) -> Dict[str, Any]:

        external_ids = (
            paper.get(
                "externalIds"
            )
            or {}
        )

        open_access_pdf = (
            paper.get(
                "openAccessPdf"
            )
            or {}
        )

        authors = []

        for author in paper.get(
            "authors",
            []
        ):

            name = author.get(
                "name"
            )

            if name:
                authors.append(name)

        doi = external_ids.get(
            "DOI"
        )

        if doi:
            doi = (
                f"https://doi.org/{doi}"
            )

        return {
            "source": "semantic_scholar",

            "external_id": paper.get(
                "paperId"
            ),

            "title": self._safe_text(
                paper.get("title")
            ),

            "abstract": self._safe_text(
                paper.get("abstract")
            ),

            "authors": authors,

            "publication_year": paper.get(
                "year"
            ),

            "publication_date": paper.get(
                "publicationDate"
            ),

            "doi": doi,

            "url": (
                open_access_pdf.get(
                    "url"
                )
                or paper.get("url")
            ),

            "source_name": paper.get(
                "venue"
            ),

            "citation_count": paper.get(
                "citationCount",
                0
            ),

            "type": None,

            "open_access": bool(
                open_access_pdf.get(
                    "url"
                )
            ),

            "keywords": [],
        }

    # ============================================================
    # ARXIV
    # ============================================================

    def search_arxiv(
        self,
        query: str,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:

        if not query or not query.strip():
            raise ValueError(
                "arXiv query cannot be empty."
            )

        params = {
            "search_query": (
                f'all:{query.strip().replace(" ", "+AND+")}'
            ),

            "start": 0,

            "max_results": min(
                max_results,
                100
            )
        }

        response = requests.get(
            self.ARXIV_URL,
            params=params,
            timeout=self.timeout
        )

        response.raise_for_status()

        root = ET.fromstring(
            response.text
        )

        namespace = {
            "atom":
            "http://www.w3.org/2005/Atom"
        }

        papers = []

        for entry in root.findall(
            "atom:entry",
            namespace
        ):

            papers.append(
                self._normalize_arxiv(
                    entry,
                    namespace
                )
            )

        return papers

    def _normalize_arxiv(
        self,
        entry: ET.Element,
        namespace: Dict[str, str]
    ) -> Dict[str, Any]:

        title_element = entry.find(
            "atom:title",
            namespace
        )

        summary_element = entry.find(
            "atom:summary",
            namespace
        )

        published_element = entry.find(
            "atom:published",
            namespace
        )

        id_element = entry.find(
            "atom:id",
            namespace
        )

        title = (
            title_element.text.strip()
            if (
                title_element is not None
                and title_element.text
            )
            else None
        )

        abstract = (
            summary_element.text.strip()
            if (
                summary_element is not None
                and summary_element.text
            )
            else None
        )

        published = (
            published_element.text.strip()
            if (
                published_element is not None
                and published_element.text
            )
            else None
        )

        external_id = (
            id_element.text.strip()
            if (
                id_element is not None
                and id_element.text
            )
            else None
        )

        authors = []

        for author in entry.findall(
            "atom:author",
            namespace
        ):

            name_element = author.find(
                "atom:name",
                namespace
            )

            if (
                name_element is not None
                and name_element.text
            ):

                authors.append(
                    name_element.text.strip()
                )

        categories = []

        for category in entry.findall(
            "atom:category",
            namespace
        ):

            term = category.attrib.get(
                "term"
            )

            if term:
                categories.append(term)

        return {
            "source": "arxiv",

            "external_id": external_id,

            "title": title,

            "abstract": abstract,

            "authors": authors,

            "publication_year": (
                int(published[:4])
                if (
                    published
                    and len(published) >= 4
                )
                else None
            ),

            "publication_date": (
                published[:10]
                if published
                else None
            ),

            "doi": None,

            "url": external_id,

            "source_name": "arXiv",

            "citation_count": 0,

            "type": "preprint",

            "open_access": True,

            "keywords": categories,
        }

    # ============================================================
    # SEARCH ALL PAPER SOURCES
    # ============================================================

    def search_all(
        self,
        query: str,
        max_results_per_source: int = 10
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search every paper source independently.

        If one source fails, the other sources continue working.

        Example:
            Semantic Scholar -> HTTP 429
            OpenAlex        -> still returns results
            arXiv           -> still returns results
        """

        results = {
            "openalex": [],
            "semantic_scholar": [],
            "arxiv": []
        }

        # --------------------------------------------------------
        # OpenAlex
        # --------------------------------------------------------

        try:

            results["openalex"] = (
                self.search_openalex(
                    query=query,
                    max_results=max_results_per_source
                )
            )

        except Exception as exc:

            print(
                f"[WARNING] OpenAlex search failed: {exc}"
            )

        # --------------------------------------------------------
        # Semantic Scholar
        # --------------------------------------------------------

        try:

            results["semantic_scholar"] = (
                self.search_semantic_scholar(
                    query=query,
                    max_results=max_results_per_source
                )
            )

        except Exception as exc:

            print(
                "[WARNING] Semantic Scholar "
                f"search failed: {exc}"
            )

        # --------------------------------------------------------
        # arXiv
        # --------------------------------------------------------

        try:

            results["arxiv"] = (
                self.search_arxiv(
                    query=query,
                    max_results=max_results_per_source
                )
            )

        except Exception as exc:

            print(
                f"[WARNING] arXiv search failed: {exc}"
            )

        return results

    # ============================================================
    # FLAT SEARCH
    # ============================================================

    def search_all_flat(
        self,
        query: str,
        max_results_per_source: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Return results from all working paper sources
        as one flat list.
        """

        results = self.search_all(
            query=query,
            max_results_per_source=max_results_per_source
        )

        papers = []

        for source_results in results.values():

            papers.extend(
                source_results
            )

        return papers