from typing import Any, Dict, List, Optional


class PaperNormalizer:
    """
    Converts raw OpenAlex records into the internal
    Revianta paper representation.
    """

    @staticmethod
    def _extract_abstract(work: Dict[str, Any]) -> Optional[str]:
        """
        OpenAlex stores abstracts as an inverted index.
        Convert it back into readable text.
        """

        inverted_index = work.get("abstract_inverted_index")

        if not inverted_index:
            return None

        words = []

        for word, positions in inverted_index.items():
            for position in positions:
                words.append((position, word))

        words.sort(key=lambda x: x[0])

        return " ".join(word for _, word in words)

    @staticmethod
    def _extract_authors(work: Dict[str, Any]) -> List[str]:
        authors = []

        for authorship in work.get("authorships", []):
            author = authorship.get("author", {})

            display_name = author.get("display_name")

            if display_name:
                authors.append(display_name)

        return authors

    @staticmethod
    def normalize(work: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert one OpenAlex work into a Revianta paper object.
        """

        primary_location = work.get("primary_location") or {}
        source = primary_location.get("source") or {}

        return {
            "external_id": work.get("id"),
            "source": "openalex",

            "title": work.get("display_name")
            or work.get("title"),

            "abstract": PaperNormalizer._extract_abstract(work),

            "authors": PaperNormalizer._extract_authors(work),

            "publication_year": work.get("publication_year"),

            "publication_date": work.get("publication_date"),

            "doi": work.get("doi"),

            "url": (
                primary_location.get("landing_page_url")
                or work.get("id")
            ),

            "source_name": source.get("display_name"),

            "citation_count": work.get("cited_by_count", 0),

            "type": work.get("type"),

            "open_access": (
                (work.get("open_access") or {})
                .get("is_oa", False)
            ),

            "keywords": [
                item.get("display_name")
                for item in work.get("keywords", [])
                if item.get("display_name")
            ],
        }

    @classmethod
    def normalize_many(
        cls,
        works: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        return [cls.normalize(work) for work in works]