def normalize_paper(
    title=None,
    authors=None,
    abstract=None,
    year=None,
    doi=None,
    url=None,
    source=None,
):
    return {
        "title": title,
        "authors": authors or [],
        "abstract": abstract or "",
        "year": year,
        "doi": doi,
        "url": url,
        "source": source,
    }