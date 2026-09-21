import re


def normalize_title(title):
    if not title:
        return ""

    title = str(title).lower()

    title = re.sub(r"[^a-z0-9\s]", "", title)

    title = re.sub(r"\s+", " ", title)

    return title.strip()


def normalize_doi(doi):
    if not doi:
        return ""

    doi = str(doi).lower().strip()

    doi = doi.replace("https://doi.org/", "")
    doi = doi.replace("http://doi.org/", "")
    doi = doi.replace("doi:", "")

    return doi.strip()


def normalize_url(url):
    if not url:
        return ""

    return str(url).lower().strip().rstrip("/")


def get_record_key(record):
    """
    Create a stable key for identifying duplicate records.

    DOI is the strongest identifier.
    Otherwise use normalized title + year when available.
    Otherwise use normalized title.
    """

    doi = normalize_doi(record.get("doi"))

    if doi:
        return f"doi:{doi}"

    title = normalize_title(record.get("title"))
    year = record.get("year")

    if title and year:
        return f"title_year:{title}:{year}"

    if title:
        return f"title:{title}"

    url = normalize_url(record.get("url"))

    if url:
        return f"url:{url}"

    return None


def deduplicate_records(records):
    """
    Remove duplicate research records.

    Duplicate priority:
    1. DOI
    2. Normalized title + year
    3. Normalized title
    4. URL
    """

    if not records:
        return []

    unique_records = []
    seen_keys = set()

    for record in records:

        if not record:
            continue

        key = get_record_key(record)

        if key is None:
            unique_records.append(record)
            continue

        if key in seen_keys:
            continue

        seen_keys.add(key)

        unique_records.append(record)

    return unique_records