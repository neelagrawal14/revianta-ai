"""
Test unified external search layer.
"""

from pathlib import Path
import sys


# ---------------------------------------------------------
# Add project root
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )


from data_pipeline.unified.external_search import ExternalSearch


def main():

    print("=" * 60)
    print("        REVIANTA UNIFIED EXTERNAL SEARCH TEST")
    print("=" * 60)

    print("\nInitializing external sources...")

    search = ExternalSearch()

    query = "AI powered satellite image analysis"

    print(f"\nSearch query: {query}")

    print("\nRunning search across all sources...")

    results = search.search_all(
        query=query,
        max_results_per_source=5,
    )

    # -----------------------------------------------------
    # Results
    # -----------------------------------------------------

    print("\n" + "-" * 60)

    total = 0

    for source, source_results in results.items():

        count = len(source_results)

        total += count

        print(
            f"{source.upper():12} : {count} results"
        )

        for item in source_results[:3]:

            title = (
                item.get("title")
                or item.get("name")
                or "Untitled"
            )

            print(
                f"   - {title}"
            )

    print("-" * 60)

    print(
        f"\nTOTAL RESULTS: {total}"
    )

    # -----------------------------------------------------
    # Validation
    # -----------------------------------------------------

    assert isinstance(results, dict)

    required_sources = [
        "papers",
        "github",
        "datasets",
        "patents",
    ]

    for source in required_sources:

        assert source in results

        assert isinstance(
            results[source],
            list,
        )

    print(
        "\nUnified result structure: VALID"
    )

    print("\n" + "=" * 60)
    print("       UNIFIED EXTERNAL SEARCH PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
