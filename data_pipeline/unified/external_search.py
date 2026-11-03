"""
Unified external-source search layer for Revianta AI.

This module connects the currently available external sources:

Papers:
    - OpenAlex
    - arXiv
    - Semantic Scholar

Code:
    - GitHub

Datasets:
    - Kaggle
    - Hugging Face

Patents:
    - PatentBrief

This layer only collects and combines external data.
It does NOT run AI analysis.

If one external source fails, the other sources continue
working independently.
"""

from __future__ import annotations

from typing import Any, Dict, List

from data_pipeline.papers.paper_sources import PaperSources
from data_pipeline.github.github_sources import GitHubSources
from data_pipeline.datasets.dataset_sources import DatasetSources
from data_pipeline.patents.patent_sources import PatentSources


class ExternalSearch:
    """
    Unified interface for all Revianta external data sources.
    """

    def __init__(self):

        self.paper_sources = PaperSources()

        self.github_sources = GitHubSources()

        self.dataset_sources = DatasetSources()

        self.patent_sources = PatentSources()

    # =========================================================
    # PAPERS
    # =========================================================

    def search_papers(
        self,
        query: str,
        max_results_per_source: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Search all available paper sources.

        Sources:
            - OpenAlex
            - arXiv
            - Semantic Scholar

        If Semantic Scholar is rate-limited, OpenAlex and
        arXiv results are still returned.
        """

        return self.paper_sources.search_all_flat(
            query=query,
            max_results_per_source=max_results_per_source,
        )

    # =========================================================
    # GITHUB
    # =========================================================

    def search_github(
        self,
        query: str,
        max_results: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Search GitHub repositories.
        """

        return self.github_sources.search_repositories(
            query=query,
            max_results=max_results,
        )

    # =========================================================
    # DATASETS
    # =========================================================

    def search_datasets(
        self,
        query: str,
        max_results_per_source: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Search all dataset sources.

        Sources:
            - Kaggle
            - Hugging Face
        """

        return self.dataset_sources.search_all_flat(
            query=query,
            max_results_per_source=max_results_per_source,
        )

    # =========================================================
    # PATENTS
    # =========================================================

    def search_patents(
        self,
        query: str,
        max_results: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Search PatentBrief.

        PatentBrief is currently used as the Revianta
        patent source.
        """

        return self.patent_sources.search_patents(
            query=query,
            max_results=max_results,
        )

    # =========================================================
    # ALL SOURCES
    # =========================================================

    def search_all(
        self,
        query: str,
        max_results_per_source: int = 5,
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search every external source independently.

        A failure in one source does not stop the remaining
        sources.

        Returns:

        {
            "papers": [...],
            "github": [...],
            "datasets": [...],
            "patents": [...]
        }
        """

        results = {
            "papers": [],
            "github": [],
            "datasets": [],
            "patents": [],
        }

        # -----------------------------------------------------
        # PAPERS
        # -----------------------------------------------------

        try:

            results["papers"] = self.search_papers(
                query=query,
                max_results_per_source=max_results_per_source,
            )

        except Exception as exc:

            print(
                f"[WARNING] Paper search failed: {exc}"
            )

        # -----------------------------------------------------
        # GITHUB
        # -----------------------------------------------------

        try:

            results["github"] = self.search_github(
                query=query,
                max_results=max_results_per_source,
            )

        except Exception as exc:

            print(
                f"[WARNING] GitHub search failed: {exc}"
            )

        # -----------------------------------------------------
        # DATASETS
        # -----------------------------------------------------

        try:

            results["datasets"] = self.search_datasets(
                query=query,
                max_results_per_source=max_results_per_source,
            )

        except Exception as exc:

            print(
                f"[WARNING] Dataset search failed: {exc}"
            )

        # -----------------------------------------------------
        # PATENTS
        # -----------------------------------------------------

        try:

            results["patents"] = self.search_patents(
                query=query,
                max_results=max_results_per_source,
            )

        except Exception as exc:

            print(
                f"[WARNING] Patent search failed: {exc}"
            )

        return results

    # =========================================================
    # FLAT ALL-SOURCE RESULTS
    # =========================================================

    def search_all_flat(
        self,
        query: str,
        max_results_per_source: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Search all external sources and return one flat list.

        Example:

            Papers
            GitHub
            Datasets
            Patents

        are combined into a single list.
        """

        results = self.search_all(
            query=query,
            max_results_per_source=max_results_per_source,
        )

        flat_results = []

        for source_results in results.values():

            flat_results.extend(
                source_results
            )

        return flat_results