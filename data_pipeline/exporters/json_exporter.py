import json
from pathlib import Path


def export_records_to_json(records, output_path):
    """
    Export processed records to a JSON file.
    """

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, ensure_ascii=False)

    return output_file


if __name__ == "__main__":
    sample_records = [
        {
            "title": "Example Research Paper",
            "authors": ["Alice"],
            "abstract": "Example abstract",
            "year": 2026,
            "doi": None,
            "url": "https://example.com",
            "source": "test",
            "record_type": "paper",
        }
    ]

    output = export_records_to_json(
        sample_records,
        "data_pipeline/output/test_records.json",
    )

    print(f"Exported records to: {output}")