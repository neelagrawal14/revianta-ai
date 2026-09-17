from data_pipeline.cleaners.data_cleaner import clean_paper
from data_pipeline.normalizers.normalizer import normalize_record


def process_patent(patent):
    """
    Clean and normalize a single patent record.
    """
    if not patent:
        return None

    cleaned_patent = clean_paper(patent)

    if not cleaned_patent:
        return None

    processed_patent = normalize_record(
        title=cleaned_patent.get("title"),
        authors=cleaned_patent.get("authors"),
        abstract=cleaned_patent.get("abstract"),
        year=cleaned_patent.get("year"),
        doi=cleaned_patent.get("doi"),
        url=cleaned_patent.get("url"),
        source=cleaned_patent.get("source"),
        record_type="patent",
    )

    return processed_patent


def process_patents(patents):
    processed_patents = []

    for patent in patents:
        processed_patent = process_patent(patent)

        if processed_patent:
            processed_patents.append(processed_patent)

    return processed_patents