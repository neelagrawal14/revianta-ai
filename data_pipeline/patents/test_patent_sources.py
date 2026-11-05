"""
Test PatentBrief patent source.
"""

from pathlib import Path
import sys


# ---------------------------------------------------------
# Add project root to Python path
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )


from data_pipeline.patents.patent_sources import PatentSources


def main():

    print("=" * 50)
    print("       PATENTBRIEF SOURCE TEST")
    print("=" * 50)

    print("\nInitializing PatentBrief client...")

    client = PatentSources()

    # -----------------------------------------------------
    # Test 1: Load complete index
    # -----------------------------------------------------

    print("\n[1/3] Loading PatentBrief index...")

    all_patents = client.get_all_patents()

    print(
        f"Patent records available: "
        f"{len(all_patents)}"
    )

    assert len(all_patents) > 0, (
        "PatentBrief returned no patent records."
    )

    # -----------------------------------------------------
    # Test 2: Search
    # -----------------------------------------------------

    print("\n[2/3] Searching for AI patents...")

    results = client.search_patents(
        query="AI",
        max_results=10,
    )

    print(
        f"Search results: {len(results)}"
    )

    assert len(results) > 0, (
        "PatentBrief search returned no results."
    )

    for i, patent in enumerate(
        results,
        start=1,
    ):

        print(
            f"\n{i}. {patent['title']}"
        )

        print(
            f"   Patent: "
            f"{patent['publication_number']}"
        )

        print(
            f"   Assignee: "
            f"{patent['assignee']}"
        )

        print(
            f"   Year: "
            f"{patent['grant_year']}"
        )

        print(
            f"   Citations: "
            f"{patent['citation_count']}"
        )

        print(
            f"   URL: "
            f"{patent['url']}"
        )

    # -----------------------------------------------------
    # Test 3: Validate normalized structure
    # -----------------------------------------------------

    print(
        "\n[3/3] Validating normalized structure..."
    )

    required_fields = [
        "source",
        "external_id",
        "publication_number",
        "title",
        "abstract",
        "summary",
        "inventors",
        "assignee",
        "filing_date",
        "publication_date",
        "grant_year",
        "priority_date",
        "country",
        "kind",
        "url",
        "type",
        "citation_count",
    ]

    for patent in results:

        for field in required_fields:

            assert field in patent, (
                f"Missing field: {field}"
            )

    print(
        "Normalized structure: VALID"
    )

    print("\n" + "=" * 50)
    print("       PATENTBRIEF TEST PASSED")
    print("=" * 50)


if __name__ == "__main__":
    main()