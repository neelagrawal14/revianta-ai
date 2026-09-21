from data_pipeline.normalizers.paper_normalizer import normalize_paper
import requests


OPENALEX_URL = "https://api.openalex.org/works"


def reconstruct_abstract(inverted_index):
    if not inverted_index:
        return ""

    words = []

    for word, positions in inverted_index.items():
        for position in positions:
            words.append((position, word))

    words.sort(key=lambda x: x[0])

    return " ".join(word for _, word in words)


def search_papers(query: str, per_page: int = 10):
    params = {
        "search": query,
        "per-page": per_page,
    }

    response = requests.get(
        OPENALEX_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    papers = []

    for paper in data.get("results", []):

        authors = []

        for authorship in paper.get("authorships", []):
            author = authorship.get("author", {})

            if author.get("display_name"):
                authors.append(author["display_name"])

        normalized_paper = normalize_paper(
            title=paper.get("title"),
            authors=authors,
            abstract=reconstruct_abstract(
                paper.get("abstract_inverted_index")
            ),
            year=paper.get("publication_year"),
            doi=paper.get("doi"),
            url=paper.get("id"),
            source="openalex",
        )

        papers.append(normalized_paper)

    return papers


if __name__ == "__main__":

    papers = search_papers("artificial intelligence", 5)

    print(f"Found {len(papers)} papers")

    for paper in papers:
        print("\n-------------------------")
        print("Title:", paper["title"])
        print("Authors:", paper["authors"])
        print("Year:", paper["year"])
        print("DOI:", paper["doi"])
        print("URL:", paper["url"])
        print("Source:", paper["source"])