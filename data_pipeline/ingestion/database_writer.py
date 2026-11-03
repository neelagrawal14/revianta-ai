"""
Revianta AI - PostgreSQL Database Writer

Writes normalized external research records into PostgreSQL.

Supported:
    - papers
    - GitHub repositories
    - datasets
    - patents
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

import psycopg
from psycopg.types.json import Json


class DatabaseWriter:

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        database: str = "revianta_ai",
        user: str = "postgres",
        password: str | None = None,
    ):

        self.host = host
        self.port = port
        self.database = database
        self.user = user

        self.password = (
            password
            or os.getenv("POSTGRES_PASSWORD")
        )

        if not self.password:
            raise ValueError(
                "PostgreSQL password not provided. "
                "Set POSTGRES_PASSWORD or pass password."
            )

    # =========================================================
    # CONNECTION
    # =========================================================

    def connect(self):

        return psycopg.connect(
            host=self.host,
            port=self.port,
            dbname=self.database,
            user=self.user,
            password=self.password,
        )

    # =========================================================
    # PAPER
    # =========================================================

    def upsert_paper(
        self,
        conn,
        record: Dict[str, Any],
    ):

        metadata = record.get(
            "metadata",
            {},
        )

        with conn.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO papers (
                    record_id,
                    source,
                    external_id,
                    title,
                    abstract,
                    authors,
                    publication_year,
                    publication_date,
                    doi,
                    url,
                    source_name,
                    citation_count,
                    paper_type,
                    open_access,
                    keywords
                )
                VALUES (
                    %(record_id)s,
                    %(source)s,
                    %(external_id)s,
                    %(title)s,
                    %(abstract)s,
                    %(authors)s,
                    %(publication_year)s,
                    %(publication_date)s,
                    %(doi)s,
                    %(url)s,
                    %(source_name)s,
                    %(citation_count)s,
                    %(paper_type)s,
                    %(open_access)s,
                    %(keywords)s
                )
                ON CONFLICT (record_id)
                DO UPDATE SET
                    title = EXCLUDED.title,
                    abstract = EXCLUDED.abstract,
                    authors = EXCLUDED.authors,
                    publication_year = EXCLUDED.publication_year,
                    publication_date = EXCLUDED.publication_date,
                    doi = EXCLUDED.doi,
                    url = EXCLUDED.url,
                    source_name = EXCLUDED.source_name,
                    citation_count = EXCLUDED.citation_count,
                    paper_type = EXCLUDED.paper_type,
                    open_access = EXCLUDED.open_access,
                    keywords = EXCLUDED.keywords,
                    updated_at = CURRENT_TIMESTAMP
                """,
                {
                    "record_id": record["record_id"],
                    "source": record["source"],
                    "external_id": record["external_id"],
                    "title": record["title"],
                    "abstract": record["description"],
                    "authors": Json(
                        metadata.get(
                            "authors",
                            [],
                        )
                    ),
                    "publication_year": metadata.get(
                        "publication_year"
                    ),
                    "publication_date": metadata.get(
                        "publication_date"
                    ),
                    "doi": metadata.get("doi"),
                    "url": record["url"],
                    "source_name": metadata.get(
                        "source_name"
                    ),
                    "citation_count": metadata.get(
                        "citation_count",
                        0,
                    ),
                    "paper_type": metadata.get(
                        "type"
                    ),
                    "open_access": metadata.get(
                        "open_access"
                    ),
                    "keywords": Json(
                        metadata.get(
                            "keywords",
                            [],
                        )
                    ),
                },
            )

    # =========================================================
    # GITHUB
    # =========================================================

    def upsert_github(
        self,
        conn,
        record: Dict[str, Any],
    ):

        metadata = record.get(
            "metadata",
            {},
        )

        with conn.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO github_repositories (
                    record_id,
                    source,
                    external_id,
                    name,
                    full_name,
                    description,
                    owner,
                    url,
                    stars,
                    forks,
                    watchers,
                    open_issues,
                    language,
                    topics,
                    license,
                    created_at_external,
                    updated_at_external,
                    pushed_at,
                    default_branch,
                    is_fork,
                    archived,
                    has_issues,
                    has_wiki
                )
                VALUES (
                    %(record_id)s,
                    %(source)s,
                    %(external_id)s,
                    %(name)s,
                    %(full_name)s,
                    %(description)s,
                    %(owner)s,
                    %(url)s,
                    %(stars)s,
                    %(forks)s,
                    %(watchers)s,
                    %(open_issues)s,
                    %(language)s,
                    %(topics)s,
                    %(license)s,
                    %(created_at_external)s,
                    %(updated_at_external)s,
                    %(pushed_at)s,
                    %(default_branch)s,
                    %(is_fork)s,
                    %(archived)s,
                    %(has_issues)s,
                    %(has_wiki)s
                )
                ON CONFLICT (record_id)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    full_name = EXCLUDED.full_name,
                    description = EXCLUDED.description,
                    owner = EXCLUDED.owner,
                    url = EXCLUDED.url,
                    stars = EXCLUDED.stars,
                    forks = EXCLUDED.forks,
                    watchers = EXCLUDED.watchers,
                    open_issues = EXCLUDED.open_issues,
                    language = EXCLUDED.language,
                    topics = EXCLUDED.topics,
                    license = EXCLUDED.license,
                    created_at_external = EXCLUDED.created_at_external,
                    updated_at_external = EXCLUDED.updated_at_external,
                    pushed_at = EXCLUDED.pushed_at,
                    default_branch = EXCLUDED.default_branch,
                    is_fork = EXCLUDED.is_fork,
                    archived = EXCLUDED.archived,
                    has_issues = EXCLUDED.has_issues,
                    has_wiki = EXCLUDED.has_wiki,
                    updated_at = CURRENT_TIMESTAMP
                """,
                {
                    "record_id": record["record_id"],
                    "source": "github",
                    "external_id": record["external_id"],
                    "name": record["title"],
                    "full_name": metadata.get(
                        "full_name"
                    ),
                    "description": record["description"],
                    "owner": metadata.get(
                        "owner"
                    ),
                    "url": record["url"],
                    "stars": metadata.get(
                        "stars",
                        0,
                    ),
                    "forks": metadata.get(
                        "forks",
                        0,
                    ),
                    "watchers": metadata.get(
                        "watchers",
                        0,
                    ),
                    "open_issues": metadata.get(
                        "open_issues",
                        0,
                    ),
                    "language": metadata.get(
                        "language"
                    ),
                    "topics": Json(
                        metadata.get(
                            "topics",
                            [],
                        )
                    ),
                    "license": metadata.get(
                        "license"
                    ),
                    "created_at_external": metadata.get(
                        "created_at"
                    ),
                    "updated_at_external": metadata.get(
                        "updated_at"
                    ),
                    "pushed_at": metadata.get(
                        "pushed_at"
                    ),
                    "default_branch": metadata.get(
                        "default_branch"
                    ),
                    "is_fork": metadata.get(
                        "is_fork",
                        False,
                    ),
                    "archived": metadata.get(
                        "archived",
                        False,
                    ),
                    "has_issues": metadata.get(
                        "has_issues",
                        True,
                    ),
                    "has_wiki": metadata.get(
                        "has_wiki",
                        True,
                    ),
                },
            )

    # =========================================================
    # DATASET
    # =========================================================

    def upsert_dataset(
        self,
        conn,
        record: Dict[str, Any],
    ):

        metadata = record.get(
            "metadata",
            {},
        )

        with conn.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO datasets (
                    record_id,
                    source,
                    external_id,
                    name,
                    description,
                    url,
                    owner,
                    license,
                    tags,
                    downloads,
                    votes,
                    usability,
                    created_at_external,
                    updated_at_external
                )
                VALUES (
                    %(record_id)s,
                    %(source)s,
                    %(external_id)s,
                    %(name)s,
                    %(description)s,
                    %(url)s,
                    %(owner)s,
                    %(license)s,
                    %(tags)s,
                    %(downloads)s,
                    %(votes)s,
                    %(usability)s,
                    %(created_at_external)s,
                    %(updated_at_external)s
                )
                ON CONFLICT (record_id)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    description = EXCLUDED.description,
                    url = EXCLUDED.url,
                    owner = EXCLUDED.owner,
                    license = EXCLUDED.license,
                    tags = EXCLUDED.tags,
                    downloads = EXCLUDED.downloads,
                    votes = EXCLUDED.votes,
                    usability = EXCLUDED.usability,
                    created_at_external = EXCLUDED.created_at_external,
                    updated_at_external = EXCLUDED.updated_at_external,
                    updated_at = CURRENT_TIMESTAMP
                """,
                {
                    "record_id": record["record_id"],
                    "source": record["source"],
                    "external_id": record["external_id"],
                    "name": record["title"],
                    "description": record["description"],
                    "url": record["url"],
                    "owner": metadata.get(
                        "owner"
                    ),
                    "license": metadata.get(
                        "license"
                    ),
                    "tags": Json(
                        metadata.get(
                            "tags",
                            [],
                        )
                    ),
                    "downloads": metadata.get(
                        "downloads",
                        0,
                    ),
                    "votes": metadata.get(
                        "votes",
                        0,
                    ),
                    "usability": metadata.get(
                        "usability"
                    ),
                    "created_at_external": metadata.get(
                        "created_at"
                    ),
                    "updated_at_external": metadata.get(
                        "updated_at"
                    ),
                },
            )

    # =========================================================
    # PATENT
    # =========================================================

    def upsert_patent(
        self,
        conn,
        record: Dict[str, Any],
    ):

        metadata = record.get(
            "metadata",
            {},
        )

        with conn.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO patents (
                    record_id,
                    source,
                    external_id,
                    publication_number,
                    title,
                    abstract,
                    summary,
                    inventors,
                    assignee,
                    filing_date,
                    publication_date,
                    grant_year,
                    priority_date,
                    country,
                    kind,
                    url,
                    patent_type,
                    citation_count
                )
                VALUES (
                    %(record_id)s,
                    %(source)s,
                    %(external_id)s,
                    %(publication_number)s,
                    %(title)s,
                    %(abstract)s,
                    %(summary)s,
                    %(inventors)s,
                    %(assignee)s,
                    %(filing_date)s,
                    %(publication_date)s,
                    %(grant_year)s,
                    %(priority_date)s,
                    %(country)s,
                    %(kind)s,
                    %(url)s,
                    %(patent_type)s,
                    %(citation_count)s
                )
                ON CONFLICT (record_id)
                DO UPDATE SET
                    title = EXCLUDED.title,
                    abstract = EXCLUDED.abstract,
                    summary = EXCLUDED.summary,
                    inventors = EXCLUDED.inventors,
                    assignee = EXCLUDED.assignee,
                    filing_date = EXCLUDED.filing_date,
                    publication_date = EXCLUDED.publication_date,
                    grant_year = EXCLUDED.grant_year,
                    priority_date = EXCLUDED.priority_date,
                    country = EXCLUDED.country,
                    kind = EXCLUDED.kind,
                    url = EXCLUDED.url,
                    patent_type = EXCLUDED.patent_type,
                    citation_count = EXCLUDED.citation_count,
                    updated_at = CURRENT_TIMESTAMP
                """,
                {
                    "record_id": record["record_id"],
                    "source": record["source"],
                    "external_id": record["external_id"],
                    "publication_number": metadata.get(
                        "publication_number"
                    ),
                    "title": record["title"],
                    "abstract": record["description"],
                    "summary": metadata.get(
                        "summary"
                    ),
                    "inventors": Json(
                        metadata.get(
                            "inventors",
                            [],
                        )
                    ),
                    "assignee": metadata.get(
                        "assignee"
                    ),
                    "filing_date": metadata.get(
                        "filing_date"
                    ),
                    "publication_date": metadata.get(
                        "publication_date"
                    ),
                    "grant_year": metadata.get(
                        "grant_year"
                    ),
                    "priority_date": metadata.get(
                        "priority_date"
                    ),
                    "country": metadata.get(
                        "country"
                    ),
                    "kind": metadata.get(
                        "kind"
                    ),
                    "url": record["url"],
                    "patent_type": metadata.get(
                        "type"
                    ),
                    "citation_count": metadata.get(
                        "citation_count",
                        0,
                    ),
                },
            )

    # =========================================================
    # WRITE ALL RECORDS
    # =========================================================

    def write_records(
        self,
        records: List[Dict[str, Any]],
    ) -> Dict[str, int]:

        counts = {
            "paper": 0,
            "github": 0,
            "dataset": 0,
            "patent": 0,
        }

        with self.connect() as conn:

            for record in records:

                source_type = record[
                    "source_type"
                ]

                if source_type == "paper":

                    self.upsert_paper(
                        conn,
                        record,
                    )

                    counts["paper"] += 1

                elif source_type == "github":

                    self.upsert_github(
                        conn,
                        record,
                    )

                    counts["github"] += 1

                elif source_type == "dataset":

                    self.upsert_dataset(
                        conn,
                        record,
                    )

                    counts["dataset"] += 1

                elif source_type == "patent":

                    self.upsert_patent(
                        conn,
                        record,
                    )

                    counts["patent"] += 1

                else:

                    print(
                        f"[WARNING] Unsupported "
                        f"source type: {source_type}"
                    )

            conn.commit()

        return counts