from data_pipeline.normalizers.paper_normalizer import normalize_paper


def search_patents(query: str, limit: int = 10):
    """
    Patent collection endpoint will be integrated here.

    The external patent API endpoint currently needs verification,
    so this function returns an empty list instead of crashing.
    """

    print(
        "Patent collector: external API endpoint needs verification."
    )

    return []


if __name__ == "__main__":

    patents = search_patents(
        "artificial intelligence",
        5
    )

    print(f"Found {len(patents)} patents")

    for patent in patents:

        print("\n-------------------------")
        print("Title:", patent["title"])
        print("Inventors:", patent["authors"])
        print("Year:", patent["year"])
        print("Abstract:", patent["abstract"])
        print("URL:", patent["url"])
        print("Source:", patent["source"])