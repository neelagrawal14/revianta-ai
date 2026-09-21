from data_pipeline.normalizers.normalizer import (
    normalize_record,
    normalize_records,
)


def test_normalize_record():
    record = normalize_record(
        title="Test Paper",
        authors=["Alice"],
        abstract="Test abstract",
        year=2025,
        doi="10.1234/test",
        url="https://example.com",
        source="openalex",
        record_type="paper",
    )

    assert record["title"] == "Test Paper"
    assert record["authors"] == ["Alice"]
    assert record["abstract"] == "Test abstract"
    assert record["year"] == 2025
    assert record["doi"] == "10.1234/test"
    assert record["url"] == "https://example.com"
    assert record["source"] == "openalex"
    assert record["record_type"] == "paper"


def test_normalize_records():
    records = [
        {
            "title": "Paper One",
            "authors": ["Alice"],
            "abstract": "Abstract one",
            "year": 2024,
            "doi": "10.1234/one",
            "url": "https://example.com/one",
            "source": "openalex",
        },
        {
            "title": "Paper Two",
            "authors": ["Bob"],
            "abstract": "Abstract two",
            "year": 2025,
            "doi": "10.1234/two",
            "url": "https://example.com/two",
            "source": "arxiv",
        },
    ]

    normalized = normalize_records(records)

    assert len(normalized) == 2
    assert normalized[0]["title"] == "Paper One"
    assert normalized[1]["title"] == "Paper Two"
    assert normalized[0]["record_type"] == "research"
    assert normalized[1]["record_type"] == "research"
