import re


def normalize_title(title):
    if not title:
        return ""

    title = title.lower()

    title = re.sub(r"[^a-z0-9\s]", "", title)

    title = re.sub(r"\s+", " ", title)

    return title.strip()


def normalize_doi(doi):
    if not doi:
        return ""

    doi = str(doi).lower().strip()

    doi = doi.replace("https://doi.org/", "")
    doi = doi.replace("http://doi.org/", "")

    return doi


def normalize_url(url):
    if not url:
        return ""

    return str(url).lower().strip().rstrip("/")


def get_record_key(record):
    """
    Create a stable key for identifying duplicate records.
    """

    doi = normalize_doi(record.get("doi"))

    if doi:
        return f"doi:{doi}"

    url = normalize_url(record.get("url"))

    if url:
        return f"url:{url}"

    title = normalize_title(record.get("title"))

    if title:
        return f"title:{title}"

    return None


def deduplicate_records(records):

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