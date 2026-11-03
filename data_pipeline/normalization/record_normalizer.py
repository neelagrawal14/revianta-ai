"""
Revianta AI - External Record Normalizer

Converts records from:
    - Papers
    - GitHub
    - Datasets
    - Patents

into one common Revianta record structure.

This module does NOT store data in the database.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, List


class RecordNormalizer:
    """
    Normalize heterogeneous external-source records
    into a common Revianta format.
    """

    # =========================================================
    # TEXT UTILITIES
    # =========================================================

    @staticmethod
    def clean_text(value: Any) -> str:

        if value is None:
            return ""

        text = str(value)

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    @staticmethod
    def normalize_title(title: Any) -> str:

        title = RecordNormalizer.clean_text(title)

        title = title.lower()

        title = re.sub(
            r"[^a-z0-9\s]",
            "",
            title
        )

        title = re.sub(
            r"\s+",
            " ",
            title
        )

        return title.strip()

    # =========================================================
    # ID GENERATION
    # =========================================================

    @staticmethod
    def generate_record_id(
        source: str,
        external_id: str,
        title: str = "",
    ) -> str:

        base = "|".join(
            [
                RecordNormalizer.clean_text(source),
                RecordNormalizer.clean_text(external_id),
                RecordNormalizer.normalize_title(title),
            ]
        )

        return hashlib.sha256(
            base.encode("utf-8")
        ).hexdigest()

    # =========================================================
    # COMMON RECORD
    # =========================================================

    @staticmethod
    def build_record(
        source: str,
        source_type: str,
        external_id: str,
        title: str = "",
        description: str = "",
        url: str = "",
        metadata: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:

        title = RecordNormalizer.clean_text(title)

        external_id = RecordNormalizer.clean_text(
            external_id
        )

        record_id = RecordNormalizer.generate_record_id(
            source=source,
            external_id=external_id,
            title=title,
        )

        return {
            "record_id": record_id,
            "source": RecordNormalizer.clean_text(source),
            "source_type": RecordNormalizer.clean_text(
                source_type
            ),
            "external_id": external_id,
            "title": title,
            "description": RecordNormalizer.clean_text(
                description
            ),
            "url": RecordNormalizer.clean_text(url),
            "metadata": metadata or {},
        }

    # =========================================================
    # PAPER
    # =========================================================

    def normalize_paper(
        self,
        paper: Dict[str, Any],
    ) -> Dict[str, Any]:

        return self.build_record(
            source=paper.get("source", ""),
            source_type="paper",
            external_id=paper.get("external_id", ""),
            title=paper.get("title", ""),
            description=paper.get("abstract", ""),
            url=paper.get("url", ""),
            metadata={
                "authors": paper.get("authors", []),
                "publication_year": paper.get(
                    "publication_year"
                ),
                "publication_date": paper.get(
                    "publication_date"
                ),
                "doi": paper.get("doi"),
                "source_name": paper.get(
                    "source_name"
                ),
                "citation_count": paper.get(
                    "citation_count",
                    0,
                ),
                "type": paper.get("type"),
                "open_access": paper.get(
                    "open_access"
                ),
                "keywords": paper.get(
                    "keywords",
                    [],
                ),
            },
        )

    # =========================================================
    # GITHUB
    # =========================================================

    def normalize_github(
        self,
        repository: Dict[str, Any],
    ) -> Dict[str, Any]:

        return self.build_record(
            source="github",
            source_type="github",
            external_id=repository.get(
                "external_id",
                repository.get(
                    "full_name",
                    "",
                ),
            ),
            title=repository.get(
                "name",
                "",
            ),
            description=repository.get(
                "description",
                "",
            ),
            url=repository.get(
                "url",
                "",
            ),
            metadata={
                "full_name": repository.get(
                    "full_name"
                ),
                "owner": repository.get(
                    "owner"
                ),
                "stars": repository.get(
                    "stars",
                    0,
                ),
                "forks": repository.get(
                    "forks",
                    0,
                ),
                "watchers": repository.get(
                    "watchers",
                    0,
                ),
                "open_issues": repository.get(
                    "open_issues",
                    0,
                ),
                "language": repository.get(
                    "language"
                ),
                "topics": repository.get(
                    "topics",
                    [],
                ),
                "license": repository.get(
                    "license"
                ),
                "created_at": repository.get(
                    "created_at"
                ),
                "updated_at": repository.get(
                    "updated_at"
                ),
                "pushed_at": repository.get(
                    "pushed_at"
                ),
                "default_branch": repository.get(
                    "default_branch"
                ),
                "is_fork": repository.get(
                    "is_fork"
                ),
                "archived": repository.get(
                    "archived"
                ),
                "has_issues": repository.get(
                    "has_issues"
                ),
                "has_wiki": repository.get(
                    "has_wiki"
                ),
            },
        )

    # =========================================================
    # DATASET
    # =========================================================

    def normalize_dataset(
        self,
        dataset: Dict[str, Any],
    ) -> Dict[str, Any]:

        return self.build_record(
            source=dataset.get(
                "source",
                "",
            ),
            source_type="dataset",
            external_id=dataset.get(
                "external_id",
                "",
            ),
            title=dataset.get(
                "name",
                dataset.get(
                    "title",
                    "",
                ),
            ),
            description=dataset.get(
                "description",
                "",
            ),
            url=dataset.get(
                "url",
                "",
            ),
            metadata={
                "owner": dataset.get(
                    "owner"
                ),
                "license": dataset.get(
                    "license"
                ),
                "tags": dataset.get(
                    "tags",
                    [],
                ),
                "downloads": dataset.get(
                    "downloads",
                    0,
                ),
                "votes": dataset.get(
                    "votes",
                    0,
                ),
                "usability": dataset.get(
                    "usability"
                ),
                "created_at": dataset.get(
                    "created_at"
                ),
                "updated_at": dataset.get(
                    "updated_at"
                ),
            },
        )

    # =========================================================
    # PATENT
    # =========================================================

    def normalize_patent(
        self,
        patent: Dict[str, Any],
    ) -> Dict[str, Any]:

        return self.build_record(
            source=patent.get(
                "source",
                "",
            ),
            source_type="patent",
            external_id=patent.get(
                "external_id",
                patent.get(
                    "publication_number",
                    "",
                ),
            ),
            title=patent.get(
                "title",
                "",
            ),
            description=(
                patent.get(
                    "abstract"
                )
                or patent.get(
                    "summary"
                )
                or ""
            ),
            url=patent.get(
                "url",
                "",
            ),
            metadata={
                "publication_number": patent.get(
                    "publication_number"
                ),
                "inventors": patent.get(
                    "inventors",
                    [],
                ),
                "assignee": patent.get(
                    "assignee"
                ),
                "filing_date": patent.get(
                    "filing_date"
                ),
                "publication_date": patent.get(
                    "publication_date"
                ),
                "grant_year": patent.get(
                    "grant_year"
                ),
                "priority_date": patent.get(
                    "priority_date"
                ),
                "country": patent.get(
                    "country"
                ),
                "kind": patent.get(
                    "kind"
                ),
                "type": patent.get(
                    "type"
                ),
                "citation_count": patent.get(
                    "citation_count",
                    0,
                ),
            },
        )

    # =========================================================
    # NORMALIZE ONE RECORD
    # =========================================================

    def normalize(
        self,
        record: Dict[str, Any],
        source_type: str,
    ) -> Dict[str, Any]:

        source_type = source_type.lower().strip()

        if source_type == "paper":
            return self.normalize_paper(record)

        if source_type == "github":
            return self.normalize_github(record)

        if source_type == "dataset":
            return self.normalize_dataset(record)

        if source_type == "patent":
            return self.normalize_patent(record)

        raise ValueError(
            f"Unsupported source type: {source_type}"
        )

    # =========================================================
    # NORMALIZE ALL
    # =========================================================

    def normalize_all(
        self,
        results: Dict[str, List[Dict[str, Any]]],
    ) -> List[Dict[str, Any]]:

        normalized = []

        mapping = {
            "papers": "paper",
            "github": "github",
            "datasets": "dataset",
            "patents": "patent",
        }

        for category, records in results.items():

            source_type = mapping.get(category)

            if source_type is None:
                continue

            for record in records:

                try:

                    normalized_record = self.normalize(
                        record,
                        source_type,
                    )

                    normalized.append(
                        normalized_record
                    )

                except Exception as exc:

                    print(
                        f"[WARNING] Failed to normalize "
                        f"{category} record: {exc}"
                    )

        return normalized

    # =========================================================
    # DEDUPLICATION
    # =========================================================

    @staticmethod
    def deduplicate(
        records: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:

        unique_records = []

        seen_ids = set()

        seen_titles = set()

        for record in records:

            record_id = record.get(
                "record_id"
            )

            normalized_title = (
                RecordNormalizer.normalize_title(
                    record.get(
                        "title",
                        "",
                    )
                )
            )

            # Primary duplicate check
            if record_id and record_id in seen_ids:
                continue

            # Secondary duplicate check
            if (
                normalized_title
                and normalized_title in seen_titles
            ):
                continue

            if record_id:
                seen_ids.add(record_id)

            if normalized_title:
                seen_titles.add(
                    normalized_title
                )

            unique_records.append(
                record
            )

        return unique_records