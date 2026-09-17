from data_pipeline.normalizers.paper_normalizer import normalize_paper
import requests
import time


SEMANTIC_SCHOLAR_URL = (
    "https://api.semanticscholar.org/graph/v1/paper/search"
)


def search_papers(query: str, limit: int = 10, retries: int = 3):

    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,abstract,year,externalIds,url",
    }

    headers = {
        "User-Agent": "ReviantaAI-DataPipeline/1.0"
    }

    for attempt in range(retries):

        response = requests.get(
            SEMANTIC_SCHOLAR_URL,
            params=params,
            headers=headers,
            timeout=30,
        )

        if response.status_code == 429:

            if attempt < retries - 1:
                wait_time = 10 * (attempt + 1)

                print(
                    f"Semantic Scholar rate limit reached. "
                    f"Waiting {wait_time} seconds..."
                )

                time.sleep(wait_time)
                continue

            print(
                "Semantic Scholar is currently rate-limiting requests. "
                "Skipping this request."
            )

            return []

        response.raise_for_status()

        data = response.json()
        break

    papers = []

    for paper in data.get("data", []):

        authors = []

        for author in paper.get("authors") or []:
            if author.get("name"):
                authors.append(author["name"])

        external_ids = paper.get("externalIds") or {}

        doi = external_ids.get("DOI")

        normalized_paper = normalize_paper(
            title=paper.get("title"),
            authors=authors,
            abstract=paper.get("abstract"),
            year=paper.get("year"),
            doi=doi,
            url=paper.get("url"),
            source="semantic_scholar",
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