"""
Revianta AI - External Data Ingestion

Flow:

ExternalSearch
      ↓
Normalization
      ↓
Deduplication
      ↓
Clean records

This version does NOT write to PostgreSQL yet.
"""

from __future__ import annotations

from typing import Any, Dict, List

from data_pipeline.unified.external_search import (
    ExternalSearch,
)

from data_pipeline.normalization.record_normalizer import (
    RecordNormalizer,
)


class ExternalIngestion:
    """
    Coordinates external search, normalization,
    and deduplication.
    """

    def __init__(self):

        self.external_search = ExternalSearch()

        self.normalizer = RecordNormalizer()

    # =========================================================
    # SEARCH + NORMALIZE
    # =========================================================

    def collect(
        self,
        query: str,
        max_results_per_source: int = 5,
    ) -> List[Dict[str, Any]]:

        print("\n" + "=" * 60)
        print("       REVIANTA EXTERNAL DATA INGESTION")
        print("=" * 60)

        print(
            f"\nQuery: {query}"
        )

        # -----------------------------------------------------
        # SEARCH
        # -----------------------------------------------------

        print(
            "\n[1/3] Searching external sources..."
        )

        results = self.external_search.search_all(
            query=query,
            max_results_per_source=max_results_per_source,
        )

        for source, records in results.items():

            print(
                f"   {source.upper():12}: "
                f"{len(records)} records"
            )

        # -----------------------------------------------------
        # NORMALIZATION
        # -----------------------------------------------------

        print(
            "\n[2/3] Normalizing records..."
        )

        normalized = (
            self.normalizer.normalize_all(
                results
            )
        )

        print(
            f"   Normalized records: "
            f"{len(normalized)}"
        )

        # -----------------------------------------------------
        # DEDUPLICATION
        # -----------------------------------------------------

        print(
            "\n[3/3] Removing duplicates..."
        )

        unique_records = (
            self.normalizer.deduplicate(
                normalized
            )
        )

        duplicates_removed = (
            len(normalized)
            - len(unique_records)
        )

        print(
            f"   Duplicates removed: "
            f"{duplicates_removed}"
        )

        print(
            f"   Final records: "
            f"{len(unique_records)}"
        )

        print("\n" + "=" * 60)
        print("       EXTERNAL INGESTION COMPLETE")
        print("=" * 60)

        return unique_records