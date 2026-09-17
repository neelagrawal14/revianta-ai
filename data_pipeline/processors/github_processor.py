from data_pipeline.cleaners.data_cleaner import clean_paper
from data_pipeline.normalizers.normalizer import normalize_record


def process_github_repository(repository):
    """
    Clean and normalize a single GitHub repository record.
    """
    if not repository:
        return None

    cleaned_repository = clean_paper(repository)

    if not cleaned_repository:
        return None

    processed_repository = normalize_record(
        title=cleaned_repository.get("title"),
        authors=cleaned_repository.get("authors"),
        abstract=cleaned_repository.get("abstract"),
        year=cleaned_repository.get("year"),
        doi=cleaned_repository.get("doi"),
        url=cleaned_repository.get("url"),
        source=cleaned_repository.get("source"),
        record_type="github",
    )

    return processed_repository


def process_github_repositories(repositories):
    processed_repositories = []

    for repository in repositories:
        processed_repository = process_github_repository(repository)

        if processed_repository:
            processed_repositories.append(processed_repository)

    return processed_repositories