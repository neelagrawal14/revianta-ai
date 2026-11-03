"""
Test Revianta external ingestion layer.
"""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:

    sys.path.insert(
        0,
        str(PROJECT_ROOT)
    )


from data_pipeline.ingestion.external_ingestion import (
    ExternalIngestion,
)


def main():

    print("=" * 60)
    print("     REVIANTA EXTERNAL INGESTION TEST")
    print("=" * 60)

    ingestion = ExternalIngestion()

    query = "AI powered satellite image analysis"

    records = ingestion.collect(
        query=query,
        max_results_per_source=5,
    )

    # ---------------------------------------------------------
    # BASIC VALIDATION
    # ---------------------------------------------------------

    assert isinstance(
        records,
        list,
    )

    assert len(records) > 0

    required_fields = [
        "record_id",
        "source",
        "source_type",
        "external_id",
        "title",
        "description",
        "url",
        "metadata",
    ]

    for record in records:

        for field in required_fields:

            assert field in record, (
                f"Missing field: {field}"
            )

    # ---------------------------------------------------------
    # SOURCE TYPES
    # ---------------------------------------------------------

    source_types = set(
        record["source_type"]
        for record in records
    )

    print(
        "\nSource types detected:"
    )

    for source_type in sorted(
        source_types
    ):

        count = sum(
            1
            for record in records
            if record["source_type"]
            == source_type
        )

        print(
            f"   {source_type:10}: {count}"
        )

    # ---------------------------------------------------------
    # SAMPLE RECORDS
    # ---------------------------------------------------------

    print(
        "\nSample normalized records:"
    )

    for number, record in enumerate(
        records[:5],
        start=1,
    ):

        print(
            f"\n#{number}"
        )

        print(
            f"Source      : "
            f"{record['source']}"
        )

        print(
            f"Type        : "
            f"{record['source_type']}"
        )

        print(
            f"Title       : "
            f"{record['title']}"
        )

        print(
            f"Record ID   : "
            f"{record['record_id'][:16]}..."
        )

    # ---------------------------------------------------------
    # DUPLICATE CHECK
    # ---------------------------------------------------------

    record_ids = [
        record["record_id"]
        for record in records
    ]

    assert len(record_ids) == len(
        set(record_ids)
    )

    print(
        "\nDuplicate check: PASSED"
    )

    print("\n" + "=" * 60)
    print("     EXTERNAL INGESTION TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":

    main()