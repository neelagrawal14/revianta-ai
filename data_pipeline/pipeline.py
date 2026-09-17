from data_pipeline.collectors.openalex import search_papers as search_openalex
from data_pipeline.collectors.semantic_scholar import search_papers as search_semantic_scholar
from data_pipeline.collectors.arxiv import search_papers as search_arxiv
from data_pipeline.collectors.github import search_repositories
from data_pipeline.collectors.kaggle import search_datasets as search_kaggle
from data_pipeline.collectors.huggingface import search_datasets as search_huggingface
from data_pipeline.collectors.patents import search_patents

from data_pipeline.cleaners.data_cleaner import clean_paper
from data_pipeline.normalizers.normalizer import normalize_record
from data_pipeline.deduplication.deduplicator import deduplicate_records

from data_pipeline.processors.paper_processor import process_papers
from data_pipeline.processors.github_processor import process_github_repositories
from data_pipeline.processors.dataset_processor import process_datasets
from data_pipeline.processors.patent_processor import process_patents


def collect_data(query, limit=5):
    """
    Collect records from all configured external sources.
    """

    records = []

    print("\nCollecting from OpenAlex...")
    records.extend(search_openalex(query, limit))

    print("\nCollecting from Semantic Scholar...")
    records.extend(search_semantic_scholar(query, limit))

    print("\nCollecting from arXiv...")
    records.extend(search_arxiv(query, limit))

    print("\nCollecting from GitHub...")
    records.extend(search_repositories(query, limit))

    print("\nCollecting from Kaggle...")
    records.extend(search_kaggle(query, limit))

    print("\nCollecting from Hugging Face...")
    records.extend(search_huggingface(query, limit))

    print("\nCollecting from patents...")
    records.extend(search_patents(query, limit))

    return records


def clean_records(records):
    """
    Clean collected records.
    """

    cleaned_records = []

    for record in records:
        cleaned_record = clean_paper(record)

        if cleaned_record:
            cleaned_records.append(cleaned_record)

    return cleaned_records


def normalize_records_for_pipeline(records):
    """
    Normalize all records into the common Revianta format.
    """

    normalized_records = []

    for record in records:
        normalized_record = normalize_record(
            title=record.get("title"),
            authors=record.get("authors"),
            abstract=record.get("abstract"),
            year=record.get("year"),
            doi=record.get("doi"),
            url=record.get("url"),
            source=record.get("source"),
            record_type=record.get(
                "record_type",
                "research",
            ),
        )

        normalized_records.append(normalized_record)

    return normalized_records


def process_records(records):
    """
    Process records according to their type.
    """

    papers = []
    github_repositories = []
    datasets = []
    patents = []

    for record in records:
        record_type = record.get("record_type")

        if record_type == "github":
            github_repositories.append(record)

        elif record_type == "dataset":
            datasets.append(record)

        elif record_type == "patent":
            patents.append(record)

        else:
            papers.append(record)

    processed_records = []

    processed_records.extend(process_papers(papers))
    processed_records.extend(
        process_github_repositories(github_repositories)
    )
    processed_records.extend(
        process_datasets(datasets)
    )
    processed_records.extend(
        process_patents(patents)
    )

    return processed_records


def run_pipeline(query, limit=5):
    """
    Run the complete Revianta data pipeline.
    """

    print("\n==============================")
    print("REVIANTA DATA PIPELINE")
    print("==============================")

    print(f"\nQuery: {query}")
    print(f"Limit per source: {limit}")

    # 1. Collect
    records = collect_data(query, limit)

    print(f"\nCollected records: {len(records)}")

    # 2. Clean
    cleaned_records = clean_records(records)

    print(f"Cleaned records: {len(cleaned_records)}")

    # 3. Normalize
    normalized_records = normalize_records_for_pipeline(
        cleaned_records
    )

    print(
        f"Normalized records: "
        f"{len(normalized_records)}"
    )

    # 4. Deduplicate
    unique_records = deduplicate_records(
        normalized_records
    )

    print(
        f"Unique records after deduplication: "
        f"{len(unique_records)}"
    )

    # 5. Process
    processed_records = process_records(
        unique_records
    )

    print(
        f"Processed records: "
        f"{len(processed_records)}"
    )

    print("\n==============================")
    print("PIPELINE COMPLETE")
    print("==============================")

    return processed_records


if __name__ == "__main__":
    results = run_pipeline(
        "artificial intelligence",
        2,
    )

    print("\nSample results:")

    for record in results[:5]:
        print("\n-------------------------")
        print("Title:", record.get("title"))
        print("Source:", record.get("source"))
        print("Type:", record.get("record_type"))
        print("URL:", record.get("url"))