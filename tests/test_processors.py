from data_pipeline.processors.paper_processor import process_paper
from data_pipeline.processors.github_processor import process_github_repository
from data_pipeline.processors.dataset_processor import process_dataset
from data_pipeline.processors.patent_processor import process_patent


def make_record(source, record_type=None):
    record = {
        "title": "  Test Record  ",
        "authors": [" Alice ", "Alice"],
        "abstract": " Test   abstract ",
        "year": 2025,
        "doi": "https://doi.org/10.1234/test",
        "url": "https://example.com/test",
        "source": source,
    }

    if record_type:
        record["record_type"] = record_type

    return record


def test_process_paper():
    result = process_paper(make_record("openalex"))

    assert result["title"] == "Test Record"
    assert result["authors"] == ["Alice"]
    assert result["abstract"] == "Test abstract"
    assert result["doi"] == "10.1234/test"
    assert result["record_type"] == "paper"
    assert result["source"] == "openalex"


def test_process_github_repository():
    result = process_github_repository(make_record("github"))

    assert result["title"] == "Test Record"
    assert result["authors"] == ["Alice"]
    assert result["record_type"] == "github"
    assert result["source"] == "github"


def test_process_dataset():
    result = process_dataset(make_record("kaggle"))

    assert result["title"] == "Test Record"
    assert result["authors"] == ["Alice"]
    assert result["record_type"] == "dataset"
    assert result["source"] == "kaggle"


def test_process_patent():
    result = process_patent(make_record("patents"))

    assert result["title"] == "Test Record"
    assert result["authors"] == ["Alice"]
    assert result["record_type"] == "patent"
    assert result["source"] == "patents"


def test_process_empty_record():
    assert process_paper(None) is None
    assert process_github_repository(None) is None
    assert process_dataset(None) is None
    assert process_patent(None) is None
