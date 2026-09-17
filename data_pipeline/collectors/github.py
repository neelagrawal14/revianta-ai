from data_pipeline.normalizers.paper_normalizer import normalize_paper
import requests


GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"


def search_repositories(query: str, per_page: int = 10):

    params = {
        "q": query,
        "per_page": per_page,
    }

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ReviantaAI-DataPipeline/1.0",
    }

    response = requests.get(
        GITHUB_SEARCH_URL,
        params=params,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    repositories = []

    for repo in data.get("items", []):

        description = repo.get("description") or ""

        owner = repo.get("owner") or {}

        author = owner.get("login")

        authors = [author] if author else []

        normalized_repository = normalize_paper(
            title=repo.get("name"),
            authors=authors,
            abstract=description,
            year=None,
            doi=None,
            url=repo.get("html_url"),
            source="github",
        )

        repositories.append(normalized_repository)

    return repositories


if __name__ == "__main__":

    repositories = search_repositories(
        "artificial intelligence",
        5
    )

    print(f"Found {len(repositories)} repositories")

    for repository in repositories:

        print("\n-------------------------")
        print("Title:", repository["title"])
        print("Authors:", repository["authors"])
        print("Description:", repository["abstract"])
        print("URL:", repository["url"])
        print("Source:", repository["source"])