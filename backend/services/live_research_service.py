
import os
import httpx

TIMEOUT = 20.0


async def search_crossref(client, query: str, limit: int):
    response = await client.get(
        "https://api.crossref.org/works",
        params={
            "query": query,
            "rows": limit,
            "select": (
                "DOI,title,author,published,created,"
                "is-referenced-by-count,URL,abstract,publisher"
            ),
        },
    )
    response.raise_for_status()

    items = response.json().get("message", {}).get("items", [])
    results = []

    for paper in items:
        titles = paper.get("title") or []
        dates = (
            paper.get("published", {}).get("date-parts")
            or paper.get("created", {}).get("date-parts")
            or [[]]
        )
        year = dates[0][0] if dates and dates[0] else None

        results.append({
            "id": paper.get("DOI") or paper.get("URL"),
            "title": titles[0] if titles else "Untitled paper",
            "authors": [
                " ".join(filter(None, [a.get("given"), a.get("family")]))
                for a in paper.get("author", [])
            ],
            "year": year,
            "citationCount": paper.get("is-referenced-by-count", 0),
            "abstract": paper.get("abstract") or "No abstract available.",
            "source": paper.get("publisher") or "Crossref",
            "url": paper.get("URL"),
        })

    return results


async def search_live(source: str, query: str, limit: int = 10):
    """Search external providers; return live results, never mock records."""
    source = source.strip().lower()
    query = query.strip()
    limit = max(1, min(int(limit), 25))

    if not query:
        raise ValueError("Search query is required.")

    async with httpx.AsyncClient(
        timeout=TIMEOUT,
        follow_redirects=True,
        headers={"User-Agent": "ReviantaAI/1.0"},
    ) as client:

        if source == "papers":
            headers = {}
            key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
            if key:
                headers["x-api-key"] = key

            try:
                response = await client.get(
                    "https://api.semanticscholar.org/graph/v1/paper/search",
                    params={
                        "query": query,
                        "limit": limit,
                        "fields": (
                            "title,authors,year,citationCount,"
                            "abstract,venue,url"
                        ),
                    },
                    headers=headers,
                )
                response.raise_for_status()

                records = response.json().get("data", [])
                return [{
                    "id": p.get("paperId"),
                    "title": p.get("title") or "Untitled paper",
                    "authors": [
                        a.get("name", "") for a in p.get("authors", [])
                    ],
                    "year": p.get("year"),
                    "citationCount": p.get("citationCount") or 0,
                    "abstract": p.get("abstract") or "No abstract available.",
                    "source": p.get("venue") or "Semantic Scholar",
                    "url": p.get("url"),
                } for p in records]

            except httpx.HTTPStatusError as exc:
                if exc.response.status_code not in (429, 500, 502, 503, 504):
                    raise
                print("Semantic Scholar unavailable; trying Crossref.")
                return await search_crossref(client, query, limit)

        if source == "github":
            headers = {"Accept": "application/vnd.github+json"}
            token = os.getenv("GITHUB_TOKEN")
            if token:
                headers["Authorization"] = f"Bearer {token}"

            response = await client.get(
                "https://api.github.com/search/repositories",
                params={
                    "q": query,
                    "sort": "stars",
                    "per_page": limit,
                },
                headers=headers,
            )
            response.raise_for_status()

            return [{
                "id": repo["id"],
                "name": repo["full_name"],
                "description": repo.get("description") or "No description provided.",
                "stars": repo.get("stargazers_count", 0),
                "language": repo.get("language") or "Unknown",
                "topics": repo.get("topics") or [],
                "url": repo["html_url"],
            } for repo in response.json().get("items", [])]

        if source == "datasets":
            response = await client.get(
                "https://huggingface.co/api/datasets",
                params={
                    "search": query,
                    "limit": limit,
                    "sort": "downloads",
                    "direction": "-1",
                },
            )
            response.raise_for_status()

            return [{
                "id": dataset.get("id"),
                "name": dataset.get("id"),
                "description": dataset.get("description") or "Dataset hosted on Hugging Face.",
                "downloads": dataset.get("downloads", 0),
                "likes": dataset.get("likes", 0),
                "url": "https://huggingface.co/datasets/" + dataset["id"],
                "source": "Hugging Face",
            } for dataset in response.json()]

        if source == "patents":
            # Use live Google Patents search links without fabricating records.
            # Structured patent results can be added when a verified provider
            # and valid credentials are configured.
            from urllib.parse import quote_plus

            return [{
                "id": f"google-patents-search-{query}",
                "title": f"Search patents for: {query}",
                "abstract": "Open Google Patents to view matching patent records.",
                "publicationDate": None,
                "url": (
                    "https://patents.google.com/xhr/query?url="
                    + quote_plus("q=" + query)
                ),
                "source": "Google Patents",
                "searchUrl": (
                    "https://patents.google.com/?q="
                    + quote_plus(query)
                ),
            }]

    raise ValueError("Unsupported source. Use papers, github, datasets, or patents.")
