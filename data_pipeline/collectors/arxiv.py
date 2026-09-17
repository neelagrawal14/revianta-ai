from data_pipeline.normalizers.paper_normalizer import normalize_paper
import requests
import xml.etree.ElementTree as ET


ARXIV_URL = "https://export.arxiv.org/api/query"

ATOM_NAMESPACE = {
    "atom": "http://www.w3.org/2005/Atom"
}


def search_papers(query: str, max_results: int = 10):

    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
    }

    response = requests.get(
        ARXIV_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    root = ET.fromstring(response.text)

    papers = []

    for entry in root.findall("atom:entry", ATOM_NAMESPACE):

        title_element = entry.find(
            "atom:title",
            ATOM_NAMESPACE
        )

        summary_element = entry.find(
            "atom:summary",
            ATOM_NAMESPACE
        )

        published_element = entry.find(
            "atom:published",
            ATOM_NAMESPACE
        )

        id_element = entry.find(
            "atom:id",
            ATOM_NAMESPACE
        )

        title = (
            title_element.text.strip()
            if title_element is not None and title_element.text
            else None
        )

        abstract = (
            summary_element.text.strip()
            if summary_element is not None and summary_element.text
            else ""
        )

        published = (
            published_element.text
            if published_element is not None
            else None
        )

        year = None

        if published:
            try:
                year = int(published[:4])
            except ValueError:
                year = None

        url = (
            id_element.text.strip()
            if id_element is not None and id_element.text
            else None
        )

        authors = []

        for author in entry.findall(
            "atom:author",
            ATOM_NAMESPACE
        ):
            name_element = author.find(
                "atom:name",
                ATOM_NAMESPACE
            )

            if name_element is not None and name_element.text:
                authors.append(name_element.text.strip())

        normalized_paper = normalize_paper(
            title=title,
            authors=authors,
            abstract=abstract,
            year=year,
            doi=None,
            url=url,
            source="arxiv",
        )

        papers.append(normalized_paper)

    return papers


if __name__ == "__main__":

    papers = search_papers(
        "artificial intelligence",
        5
    )

    print(f"Found {len(papers)} papers")

    for paper in papers:

        print("\n-------------------------")
        print("Title:", paper["title"])
        print("Authors:", paper["authors"])
        print("Year:", paper["year"])
        print("DOI:", paper["doi"])
        print("URL:", paper["url"])
        print("Source:", paper["source"])