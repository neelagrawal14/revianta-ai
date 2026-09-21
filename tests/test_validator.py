from data_pipeline.validators.record_validator import (
    is_valid_url,
    is_valid_doi,
    is_valid_year,
    is_valid_authors,
    validate_record,
    validate_records,
)


def test_valid_url():
    assert is_valid_url("https://example.com/paper")
    assert is_valid_url("http://example.com")


def test_invalid_url():
    assert not is_valid_url("example.com")


def test_valid_doi():
    assert is_valid_doi("10.1234/example")


def test_invalid_doi():
    assert not is_valid_doi("not-a-doi")


def test_valid_year():
    assert is_valid_year(2025)
    assert is_valid_year(None)


def test_invalid_year():
    assert not is_valid_year(1800)
    assert not is_valid_year("not-a-year")


def test_valid_authors():
    assert is_valid_authors(["Alice", "Bob"])
    assert is_valid_authors([])


def test_invalid_authors():
    assert not is_valid_authors("Alice")
    assert not is_valid_authors(["Alice", ""])


def test_validate_valid_record():
    record = {
        "title": "Test Paper",
        "authors": ["Alice"],
        "abstract": "Test abstract",
        "year": 2025,
        "doi": "10.1234/test",
        "url": "https://example.com/test",
        "source": "openalex",
        "record_type": "paper",
    }

    is_valid, errors = validate_record(record)

    assert is_valid is True
    assert errors == []


def test_validate_invalid_record():
    record = {
        "title": "",
        "authors": "Alice",
        "year": 1800,
        "source": "unknown",
        "record_type": "invalid",
        "url": "not-a-url",
        "doi": "not-a-doi",
    }

    is_valid, errors = validate_record(record)

    assert is_valid is False
    assert "missing title" in errors
    assert "invalid source" in errors
    assert "invalid record_type" in errors
    assert "invalid authors" in errors
    assert "invalid year" in errors
    assert "invalid URL" in errors
    assert "invalid DOI" in errors


def test_validate_records():
    valid_record = {
        "title": "Valid Paper",
        "authors": ["Alice"],
        "year": 2025,
        "source": "openalex",
        "record_type": "paper",
    }

    invalid_record = {
        "title": "",
        "source": "unknown",
        "record_type": "paper",
    }

    valid_records, invalid_records = validate_records(
        [valid_record, invalid_record]
    )

    assert len(valid_records) == 1
    assert len(invalid_records) == 1
