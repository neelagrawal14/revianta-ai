from data_pipeline.cleaners.data_cleaner import clean_paper
from data_pipeline.normalizers.normalizer import normalize_record


def process_dataset(dataset):
    """
    Clean and normalize a single dataset record.
    """
    if not dataset:
        return None

    cleaned_dataset = clean_paper(dataset)

    if not cleaned_dataset:
        return None

    processed_dataset = normalize_record(
        title=cleaned_dataset.get("title"),
        authors=cleaned_dataset.get("authors"),
        abstract=cleaned_dataset.get("abstract"),
        year=cleaned_dataset.get("year"),
        doi=cleaned_dataset.get("doi"),
        url=cleaned_dataset.get("url"),
        source=cleaned_dataset.get("source"),
        record_type="dataset",
    )

    return processed_dataset


def process_datasets(datasets):
    processed_datasets = []

    for dataset in datasets:
        processed_dataset = process_dataset(dataset)

        if processed_dataset:
            processed_datasets.append(processed_dataset)

    return processed_datasets