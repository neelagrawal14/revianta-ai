from data_pipeline.deduplication.deduplicator import (
    normalize_title,
    normalize_doi,
    get_record_key,
    deduplicate_records,
)


def test_normalize_title():
    assert normalize_title("  Deep Learning: An Introduction! ") == "deep learning an introduction"


def test_normalize_doi():
    assert normalize_doi("https://doi.org/10.1234/ABC") == "10.1234/abc"


def test_get_record_key_with_doi():
    record = {
        "title": "Test Paper",
        "doi": "10.1234/test",
        "year": 2025,
    }

    assert get_record_key(record) == "doi:10.1234/test"


def test_get_record_key_with_title_and_year():
    record = {
        "title": "Test Paper",
        "year": 2025,
    }

    assert get_record_key(record) == "title_year:test paper:2025"


def test_deduplicate_records():
    records = [
        {
            "title": "Test Paper",
            "year": 2025,
            "source": "openalex",
        },
        {
            "title": " Test   Paper ",
            "year": 2025,
            "source": "arxiv",
        },
        {
            "title": "Test Paper",
            "year": 2024,
            "source": "openalex",
        },
    ]

    unique_records = deduplicate_records(records)

    assert len(unique_records) == 2
    assert unique_records[0]["source"] == "openalex"
    assert unique_records[1]["year"] == 2024
