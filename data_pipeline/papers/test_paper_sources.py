from paper_sources import PaperSources


def print_paper(paper, number):
    print(f"\n#{number}")
    print(f"Source      : {paper['source']}")
    print(f"Title       : {paper['title']}")
    print(f"Year       : {paper['publication_year']}")
    print(f"Authors     : {', '.join(paper['authors'][:3])}")
    print(f"Citations   : {paper['citation_count']}")
    print(f"Open Access : {paper['open_access']}")
    print(f"DOI        : {paper['doi']}")
    print(f"URL        : {paper['url']}")


def main():

    print("=" * 70)
    print("          REVIANTA PAPER SOURCES TEST")
    print("=" * 70)

    query = "AI powered satellite image analysis"

    print(f"\nQuery: {query}")

    client = PaperSources()

    # ============================================================
    # OPENALEX
    # ============================================================

    print("\n" + "-" * 70)
    print("1. OPENALEX")
    print("-" * 70)

    openalex_papers = client.search_openalex(
        query,
        max_results=5
    )

    print(f"Papers retrieved: {len(openalex_papers)}")

    for i, paper in enumerate(
        openalex_papers,
        start=1
    ):
        print_paper(paper, i)

    # ============================================================
    # SEMANTIC SCHOLAR
    # ============================================================

    print("\n" + "-" * 70)
    print("2. SEMANTIC SCHOLAR")
    print("-" * 70)

    semantic_papers = []

    try:
        semantic_papers = client.search_semantic_scholar(
            query,
            max_results=5
        )

        print(
            f"Papers retrieved: "
            f"{len(semantic_papers)}"
        )

        for i, paper in enumerate(
            semantic_papers,
            start=1
        ):
            print_paper(paper, i)

    except Exception as error:

        print(
            "WARNING: Semantic Scholar unavailable."
        )

        print(
            f"Reason: {error}"
        )

        print(
            "Continuing with arXiv..."
        )

    # ============================================================
    # ARXIV
    # ============================================================

    print("\n" + "-" * 70)
    print("3. ARXIV")
    print("-" * 70)

    arxiv_papers = client.search_arxiv(
        query,
        max_results=5
    )

    print(
        f"Papers retrieved: "
        f"{len(arxiv_papers)}"
    )

    for i, paper in enumerate(
        arxiv_papers,
        start=1
    ):
        print_paper(paper, i)

    # ============================================================
    # VALIDATION
    # ============================================================

    print("\n" + "=" * 70)
    print("VALIDATION")
    print("=" * 70)

    # OpenAlex MUST work
    if len(openalex_papers) == 0:
        raise AssertionError(
            "OpenAlex returned no papers."
        )

    # arXiv MUST work
    if len(arxiv_papers) == 0:
        raise AssertionError(
            "arXiv returned no papers."
        )

    # Semantic Scholar is optional for now
    if len(semantic_papers) > 0:
        print(
            "Semantic Scholar records "
            "retrieved and validated."
        )
    else:
        print(
            "Semantic Scholar skipped "
            "because the API is currently unavailable/rate-limited."
        )

    # ============================================================
    # NORMALIZED STRUCTURE VALIDATION
    # ============================================================

    required_fields = [
        "source",
        "external_id",
        "title",
        "abstract",
        "authors",
        "publication_year",
        "publication_date",
        "doi",
        "url",
        "source_name",
        "citation_count",
        "type",
        "open_access",
        "keywords",
    ]

    all_papers = (
        openalex_papers
        + semantic_papers
        + arxiv_papers
    )

    print("\nChecking normalized paper structure...")

    for paper in all_papers:

        for field in required_fields:

            if field not in paper:

                raise AssertionError(
                    f"Missing field '{field}' "
                    f"from {paper.get('source')} paper."
                )

    print(
        "All available paper records "
        "contain the required fields."
    )

    # ============================================================
    # SOURCE COUNTS
    # ============================================================

    print("\nSource counts:")

    print(
        f"OpenAlex         : "
        f"{len(openalex_papers)}"
    )

    print(
        f"Semantic Scholar : "
        f"{len(semantic_papers)}"
    )

    print(
        f"arXiv            : "
        f"{len(arxiv_papers)}"
    )

    print(
        f"Total             : "
        f"{len(all_papers)}"
    )

    # ============================================================
    # FINAL STATUS
    # ============================================================

    print("\n" + "=" * 70)
    print("        PAPER SOURCES TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()