from data_pipeline.cleaners.data_cleaner import clean_paper
from data_pipeline.normalizers.normalizer import normalize_record


def process_paper(paper):
    """
    Clean and normalize a single research paper.
    """

    if not paper:
        return None

    cleaned_paper = clean_paper(paper)

    if not cleaned_paper:
        return None

    processed_paper = normalize_record(
        title=cleaned_paper.get("title"),
        authors=cleaned_paper.get("authors"),
        abstract=cleaned_paper.get("abstract"),
        year=cleaned_paper.get("year"),
        doi=cleaned_paper.get("doi"),
        url=cleaned_paper.get("url"),
        source=cleaned_paper.get("source"),
        record_type="paper",
    )

    return processed_paper


def process_papers(papers):

    processed_papers = []

    for paper in papers:

        processed_paper = process_paper(paper)

        if processed_paper:
            processed_papers.append(processed_paper)

    return processed_papers