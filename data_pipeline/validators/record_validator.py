import re


def is_valid_url(url):
    if not url:
        return True

    url_pattern = re.compile(
        r"^https?://[^\s]+$",
        re.IGNORECASE,
    )

    return bool(url_pattern.match(str(url).strip()))


def is_valid_doi(doi):
    if not doi:
        return True

    doi_pattern = re.compile(
        r"^10\.\d{4,9}/\S+$",
        re.IGNORECASE,
    )

    return bool(doi_pattern.match(str(doi).strip()))


def is_valid_year(year):
    if year is None or year == "":
        return True

    try:
        year = int(year)
    except (TypeError, ValueError):
        return False

    return 1900 <= year <= 2100


def validate_record(record):
    """
    Validate a single research record.

    Returns:
        (True, []) when valid
        (False, [errors]) when invalid
    """

    errors = []

    if not record:
        return False, ["record is empty"]

    if not record.get("title"):
        errors.append("missing title")

    if not record.get("source"):
        errors.append("missing source")

    if not record.get("record_type"):
        errors.append("missing record_type")

    if not is_valid_year(record.get("year")):
        errors.append("invalid year")

    if not is_valid_url(record.get("url")):
        errors.append("invalid URL")

    if not is_valid_doi(record.get("doi")):
        errors.append("invalid DOI")

    return len(errors) == 0, errors


def validate_records(records):
    """
    Validate multiple research records.

    Returns:
        valid_records, invalid_records
    """

    valid_records = []
    invalid_records = []

    for record in records:
        is_valid, errors = validate_record(record)

        if is_valid:
            valid_records.append(record)
        else:
            invalid_records.append(
                {
                    "record": record,
                    "errors": errors,
                }
            )

    return valid_records, invalid_records