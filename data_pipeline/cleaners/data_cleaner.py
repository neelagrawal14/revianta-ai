import re


def clean_text(value):
    if value is None:
        return ""

    value = str(value)

    value = re.sub(r"\s+", " ", value)

    return value.strip()


def clean_title(title):
    return clean_text(title)


def clean_abstract(abstract):
    return clean_text(abstract)


def clean_authors(authors):
    if not authors:
        return []

    cleaned_authors = []

    for author in authors:

        author = clean_text(author)

        if author and author not in cleaned_authors:
            cleaned_authors.append(author)

    return cleaned_authors


def clean_url(url):
    return clean_text(url)


def clean_doi(doi):
    doi = clean_text(doi)

    if not doi:
        return None

    doi = doi.replace("https://doi.org/", "")
    doi = doi.replace("http://doi.org/", "")

    return doi.strip()


def clean_paper(paper):

    if not paper:
        return None

    cleaned_paper = paper.copy()

    cleaned_paper["title"] = clean_title(
        paper.get("title")
    )

    cleaned_paper["abstract"] = clean_abstract(
        paper.get("abstract")
    )

    cleaned_paper["authors"] = clean_authors(
        paper.get("authors")
    )

    cleaned_paper["url"] = clean_url(
        paper.get("url")
    )

    cleaned_paper["doi"] = clean_doi(
        paper.get("doi")
    )

    return cleaned_paper