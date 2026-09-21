from data_pipeline.cleaners.data_cleaner import (
    clean_text,
    clean_authors,
    clean_doi,
    clean_paper,
)


def test_clean_text():
    assert clean_text("  Hello    World  ") == "Hello World"


def test_clean_authors():
    authors = [" Alice ", "Bob", "Alice", ""]
    assert clean_authors(authors) == ["Alice", "Bob"]


def test_clean_doi():
    assert clean_doi("https://doi.org/10.1234/example") == "10.1234/example"


def test_clean_paper():
    paper = {
        "title": "  Test   Paper ",
        "authors": [" Alice ", "Alice"],
        "abstract": " Some   abstract ",
        "year": 2025,
        "doi": "https://doi.org/10.1234/test",
        "url": " https://example.com/test ",
        "source": "openalex",
    }

    cleaned = clean_paper(paper)

    assert cleaned["title"] == "Test Paper"
    assert cleaned["authors"] == ["Alice"]
    assert cleaned["abstract"] == "Some abstract"
    assert cleaned["doi"] == "10.1234/test"
    assert cleaned["url"] == "https://example.com/test"
