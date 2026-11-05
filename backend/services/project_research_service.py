"""
Revianta AI - Project Research Service

Connects a Revianta project with external research
records already stored in PostgreSQL.

Flow:

Project
   ↓
PostgreSQL
   ↓
Papers / GitHub / Datasets / Patents
   ↓
Relevance matching
   ↓
Project research context
"""

from __future__ import annotations

import re
from typing import Any, Dict, List

import psycopg


class ProjectResearchService:
    """
    Service for creating projects and finding
    relevant external research records.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        database: str = "revianta_ai",
        user: str = "postgres",
        password: str | None = None,
    ):

        self.connection_config = {
            "host": host,
            "port": port,
            "dbname": database,
            "user": user,
            "password": password,
        }

        if not password:
            raise ValueError(
                "PostgreSQL password is required."
            )

    # =========================================================
    # DATABASE CONNECTION
    # =========================================================

    def connect(self):

        return psycopg.connect(
            **self.connection_config
        )

    # =========================================================
    # TEXT NORMALIZATION
    # =========================================================

    @staticmethod
    def tokenize(text: str) -> set[str]:

        if not text:
            return set()

        text = text.lower()

        words = re.findall(
            r"[a-z0-9]+",
            text,
        )

        stop_words = {
            "the",
            "and",
            "for",
            "with",
            "using",
            "use",
            "based",
            "system",
            "analysis",
            "project",
            "ai",
        }

        return {
            word
            for word in words
            if len(word) > 2
            and word not in stop_words
        }

    # =========================================================
    # SIMPLE RELEVANCE SCORE
    # =========================================================

    def calculate_relevance(
        self,
        query: str,
        title: str,
        description: str = "",
    ) -> float:

        query_tokens = self.tokenize(query)

        record_tokens = self.tokenize(
            f"{title} {description}"
        )

        if not query_tokens or not record_tokens:
            return 0.0

        overlap = (
            query_tokens
            & record_tokens
        )

        score = (
            len(overlap)
            / len(query_tokens)
        )

        return round(
            min(score, 1.0),
            5,
        )

    # =========================================================
    # CREATE PROJECT
    # =========================================================

    def create_project(
        self,
        name: str,
        title: str,
        description: str = "",
        created_by: str = "system",
    ) -> int:

        with self.connect() as conn:

            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO projects (
                        name,
                        title,
                        description,
                        created_by
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    RETURNING id
                    """,
                    (
                        name,
                        title,
                        description,
                        created_by,
                    ),
                )

                project_id = cursor.fetchone()[0]

            conn.commit()

        return project_id

    # =========================================================
    # GET PROJECT
    # =========================================================

    def get_project(
        self,
        project_id: int,
    ) -> Dict[str, Any] | None:

        with self.connect() as conn:

            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        id,
                        name,
                        title,
                        description,
                        status,
                        created_by,
                        created_at,
                        updated_at
                    FROM projects
                    WHERE id = %s
                    """,
                    (project_id,),
                )

                row = cursor.fetchone()

                if row is None:
                    return None

                columns = [
                    "id",
                    "name",
                    "title",
                    "description",
                    "status",
                    "created_by",
                    "created_at",
                    "updated_at",
                ]

                return dict(
                    zip(columns, row)
                )

    # =========================================================
    # SEARCH PAPERS
    # =========================================================

    def search_papers(
        self,
        query: str,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:

        with self.connect() as conn:

            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        id,
                        record_id,
                        source,
                        external_id,
                        title,
                        abstract,
                        publication_year,
                        doi,
                        url,
                        citation_count
                    FROM papers
                    ORDER BY citation_count DESC NULLS LAST
                    LIMIT %s
                    """,
                    (limit,),
                )

                rows = cursor.fetchall()

        results = []

        for row in rows:

            title = row[4] or ""
            abstract = row[5] or ""

            relevance = (
                self.calculate_relevance(
                    query,
                    title,
                    abstract,
                )
            )

            results.append(
                {
                    "id": row[0],
                    "record_id": row[1],
                    "source": row[2],
                    "external_id": row[3],
                    "title": title,
                    "abstract": abstract,
                    "publication_year": row[6],
                    "doi": row[7],
                    "url": row[8],
                    "citation_count": row[9],
                    "relevance_score": relevance,
                }
            )

        results.sort(
            key=lambda item: (
                item["relevance_score"],
                item["citation_count"] or 0,
            ),
            reverse=True,
        )

        return results

    # =========================================================
    # SEARCH GITHUB
    # =========================================================

    def search_github(
        self,
        query: str,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:

        with self.connect() as conn:

            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        id,
                        record_id,
                        external_id,
                        name,
                        full_name,
                        description,
                        owner,
                        url,
                        stars,
                        forks,
                        language
                    FROM github_repositories
                    ORDER BY stars DESC NULLS LAST
                    LIMIT %s
                    """,
                    (limit,),
                )

                rows = cursor.fetchall()

        results = []

        for row in rows:

            title = row[3] or ""
            description = row[5] or ""

            relevance = (
                self.calculate_relevance(
                    query,
                    title,
                    description,
                )
            )

            results.append(
                {
                    "id": row[0],
                    "record_id": row[1],
                    "external_id": row[2],
                    "name": title,
                    "full_name": row[4],
                    "description": description,
                    "owner": row[6],
                    "url": row[7],
                    "stars": row[8],
                    "forks": row[9],
                    "language": row[10],
                    "relevance_score": relevance,
                }
            )

        results.sort(
            key=lambda item: (
                item["relevance_score"],
                item["stars"] or 0,
            ),
            reverse=True,
        )

        return results

    # =========================================================
    # SEARCH DATASETS
    # =========================================================

    def search_datasets(
        self,
        query: str,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:

        with self.connect() as conn:

            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        id,
                        record_id,
                        source,
                        external_id,
                        name,
                        description,
                        url,
                        owner,
                        license,
                        downloads
                    FROM datasets
                    ORDER BY downloads DESC NULLS LAST
                    LIMIT %s
                    """,
                    (limit,),
                )

                rows = cursor.fetchall()

        results = []

        for row in rows:

            name = row[4] or ""
            description = row[5] or ""

            relevance = (
                self.calculate_relevance(
                    query,
                    name,
                    description,
                )
            )

            results.append(
                {
                    "id": row[0],
                    "record_id": row[1],
                    "source": row[2],
                    "external_id": row[3],
                    "name": name,
                    "description": description,
                    "url": row[6],
                    "owner": row[7],
                    "license": row[8],
                    "downloads": row[9],
                    "relevance_score": relevance,
                }
            )

        results.sort(
            key=lambda item: (
                item["relevance_score"],
                item["downloads"] or 0,
            ),
            reverse=True,
        )

        return results

    # =========================================================
    # SEARCH PATENTS
    # =========================================================

    def search_patents(
        self,
        query: str,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:

        with self.connect() as conn:

            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        id,
                        record_id,
                        source,
                        external_id,
                        publication_number,
                        title,
                        abstract,
                        summary,
                        assignee,
                        publication_date,
                        url
                    FROM patents
                    ORDER BY publication_date DESC NULLS LAST
                    LIMIT %s
                    """,
                    (limit,),
                )

                rows = cursor.fetchall()

        results = []

        for row in rows:

            title = row[5] or ""
            abstract = row[6] or ""
            summary = row[7] or ""

            description = (
                f"{abstract} {summary}"
            )

            relevance = (
                self.calculate_relevance(
                    query,
                    title,
                    description,
                )
            )

            results.append(
                {
                    "id": row[0],
                    "record_id": row[1],
                    "source": row[2],
                    "external_id": row[3],
                    "publication_number": row[4],
                    "title": title,
                    "abstract": abstract,
                    "summary": summary,
                    "assignee": row[8],
                    "publication_date": row[9],
                    "url": row[10],
                    "relevance_score": relevance,
                }
            )

        results.sort(
            key=lambda item:
                item["relevance_score"],
            reverse=True,
        )

        return results

    # =========================================================
    # FIND RESEARCH
    # =========================================================

    def find_research(
        self,
        query: str,
        limit: int = 10,
    ) -> Dict[str, List[Dict[str, Any]]]:

        return {
            "papers": self.search_papers(
                query,
                limit,
            ),
            "github": self.search_github(
                query,
                limit,
            ),
            "datasets": self.search_datasets(
                query,
                limit,
            ),
            "patents": self.search_patents(
                query,
                limit,
            ),
        }

    # =========================================================
    # ATTACH PAPER
    # =========================================================

    def attach_paper(
        self,
        project_id: int,
        paper_id: int,
        relevance_score: float,
    ):

        with self.connect() as conn:

            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO project_papers (
                        project_id,
                        paper_id,
                        relevance_score
                    )
                    VALUES (
                        %s,
                        %s,
                        %s
                    )
                    ON CONFLICT (
                        project_id,
                        paper_id
                    )
                    DO UPDATE SET
                        relevance_score =
                            EXCLUDED.relevance_score
                    """,
                    (
                        project_id,
                        paper_id,
                        relevance_score,
                    ),
                )

            conn.commit()

    # =========================================================
    # ATTACH GITHUB
    # =========================================================

    def attach_github(
        self,
        project_id: int,
        github_id: int,
        relevance_score: float,
    ):

        with self.connect() as conn:

            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO project_github (
                        project_id,
                        github_id,
                        relevance_score
                    )
                    VALUES (
                        %s,
                        %s,
                        %s
                    )
                    ON CONFLICT (
                        project_id,
                        github_id
                    )
                    DO UPDATE SET
                        relevance_score =
                            EXCLUDED.relevance_score
                    """,
                    (
                        project_id,
                        github_id,
                        relevance_score,
                    ),
                )

            conn.commit()

    # =========================================================
    # ATTACH DATASET
    # =========================================================

    def attach_dataset(
        self,
        project_id: int,
        dataset_id: int,
        relevance_score: float,
    ):

        with self.connect() as conn:

            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO project_datasets (
                        project_id,
                        dataset_id,
                        relevance_score
                    )
                    VALUES (
                        %s,
                        %s,
                        %s
                    )
                    ON CONFLICT (
                        project_id,
                        dataset_id
                    )
                    DO UPDATE SET
                        relevance_score =
                            EXCLUDED.relevance_score
                    """,
                    (
                        project_id,
                        dataset_id,
                        relevance_score,
                    ),
                )

            conn.commit()

    # =========================================================
    # ATTACH PATENT
    # =========================================================

    def attach_patent(
        self,
        project_id: int,
        patent_id: int,
        relevance_score: float,
    ):

        with self.connect() as conn:

            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO project_patents (
                        project_id,
                        patent_id,
                        relevance_score
                    )
                    VALUES (
                        %s,
                        %s,
                        %s
                    )
                    ON CONFLICT (
                        project_id,
                        patent_id
                    )
                    DO UPDATE SET
                        relevance_score =
                            EXCLUDED.relevance_score
                    """,
                    (
                        project_id,
                        patent_id,
                        relevance_score,
                    ),
                )

            conn.commit()

    # =========================================================
    # BUILD PROJECT RESEARCH CONTEXT
    # =========================================================

    def build_project_context(
        self,
        project_id: int,
        query: str,
        minimum_relevance: float = 0.20,
        limit: int = 10,
    ) -> Dict[str, Any]:

        research = self.find_research(
            query=query,
            limit=limit,
        )

        selected = {
            "papers": [],
            "github": [],
            "datasets": [],
            "patents": [],
        }

        for paper in research["papers"]:

            if (
                paper["relevance_score"]
                >= minimum_relevance
            ):

                self.attach_paper(
                    project_id,
                    paper["id"],
                    paper["relevance_score"],
                )

                selected["papers"].append(
                    paper
                )

        for repository in research["github"]:

            if (
                repository["relevance_score"]
                >= minimum_relevance
            ):

                self.attach_github(
                    project_id,
                    repository["id"],
                    repository["relevance_score"],
                )

                selected["github"].append(
                    repository
                )

        for dataset in research["datasets"]:

            if (
                dataset["relevance_score"]
                >= minimum_relevance
            ):

                self.attach_dataset(
                    project_id,
                    dataset["id"],
                    dataset["relevance_score"],
                )

                selected["datasets"].append(
                    dataset
                )

        for patent in research["patents"]:

            if (
                patent["relevance_score"]
                >= minimum_relevance
            ):

                self.attach_patent(
                    project_id,
                    patent["id"],
                    patent["relevance_score"],
                )

                selected["patents"].append(
                    patent
                )

        return {
            "project_id": project_id,
            "query": query,
            "minimum_relevance": minimum_relevance,
            "results": selected,
            "counts": {
                key: len(value)
                for key, value
                in selected.items()
            },
        }