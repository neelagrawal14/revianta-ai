from data_pipeline.normalizers.paper_normalizer import normalize_paper


def normalize_record(
    title=None,
    authors=None,
    abstract=None,
    year=None,
    doi=None,
    url=None,
    source=None,
    record_type="research",
):
    """
    Convert a collected record into the common Revianta data format.
    """

    record = normalize_paper(
        title=title,
        authors=authors,
        abstract=abstract,
        year=year,
        doi=doi,
        url=url,
        source=source,
    )

    record["record_type"] = record_type

    return record


def normalize_records(records, source=None, record_type="research"):

    normalized_records = []

    for record in records:

        if not record:
            continue

        normalized_record = normalize_record(
            title=record.get("title"),
            authors=record.get("authors"),
            abstract=record.get("abstract"),
            year=record.get("year"),
            doi=record.get("doi"),
            url=record.get("url"),
            source=source or record.get("source"),
            record_type=record.get(
                "record_type",
                record_type
            ),
        )

        normalized_records.append(normalized_record)

    return normalized_records