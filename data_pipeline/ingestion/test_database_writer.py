from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data_pipeline.ingestion.database_writer import DatabaseWriter
from data_pipeline.ingestion.external_ingestion import ExternalIngestion


def main():

    print("=" * 60)
    print("       REVIANTA DATABASE INGESTION TEST")
    print("=" * 60)

    query = "AI powered satellite image analysis"

    print("\nCollecting external records...")

    ingestion = ExternalIngestion()

    records = ingestion.collect(
        query=query,
        max_results_per_source=5,
    )

    print(
        f"\nRecords ready for database: {len(records)}"
    )

    print("\nConnecting to PostgreSQL...")

    writer = DatabaseWriter()

    counts = writer.write_records(
        records
    )

    print("\nDatabase write summary:")

    for source_type, count in counts.items():

        print(
            f"   {source_type:10}: {count}"
        )

    print("\n" + "=" * 60)
    print("       DATABASE INGESTION PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()