import os

import requests
from dotenv import load_dotenv

from data_pipeline.normalizers.paper_normalizer import normalize_paper


load_dotenv()

PATENTS_VIEW_URL = "https://search.patentsview.org/api/v1/patent/"


def search_patents(query: str, limit: int = 10):
    """
    Search patents through the PatentsView Search API.

    Requires PATENTSVIEW_API_KEY in the environment.
    Returns an empty list when the API is unavailable.
    """

    api_key = os.getenv("PATENTSVIEW_API_KEY")

    if not api_key:
        print(
            "Patent collector: PATENTSVIEW_API_KEY is not configured. "
            "Skipping patent collection."
        )
        return []

    body = {
        "q": {
            "_text_any": {
                "patent_title": query
            }
        },
        "f": [
            "patent_id",
            "patent_title",
            "patent_date",
        ],
        "o": {
            "size": limit
        },
    }

    headers = {
        "X-Api-Key": api_key,
        "accept": "application/json",
    }

    try:
        response = requests.post(
            PATENTS_VIEW_URL,
            headers=headers,
            json=body,
            timeout=30,
        )
        response.raise_for_status()

    except requests.RequestException as exc:
        print(
            "Patent collector: PatentsView API is unavailable. "
            f"Skipping patent collection. Error: {exc}"
        )
        return []

    data = response.json()

    patents = []

    for patent in data.get("patents", []):
        patent_id = patent.get("patent_id")

        patent_url = None
        if patent_id:
            patent_url = (
                f"https://patents.google.com/patent/{patent_id}"
            )

        patent_date = patent.get("patent_date")

        year = None
        if patent_date:
            try:
                year = int(patent_date[:4])
            except (TypeError, ValueError):
                year = None

        normalized_patent = normalize_paper(
            title=patent.get("patent_title"),
            authors=[],
            abstract="",
            year=year,
            doi=None,
            url=patent_url,
            source="patents",
        )

        normalized_patent["record_type"] = "patent"
        normalized_patent["patent_id"] = patent_id

        patents.append(normalized_patent)

    return patents


if __name__ == "__main__":
    patents = search_patents("artificial intelligence", 5)

    print(f"Found {len(patents)} patents")

    for patent in patents:
        print("\n-------------------------")
        print("Title:", patent["title"])
        print("Patent ID:", patent.get("patent_id"))
        print("Year:", patent["year"])
        print("URL:", patent["url"])
        print("Source:", patent["source"])
