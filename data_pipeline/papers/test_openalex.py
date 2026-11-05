from .openalex_client import OpenAlexClient
from .paper_normalizer import PaperNormalizer


def main():

    print("=" * 60)
    print("          REVIANTA OPENALEX PAPER TEST")
    print("=" * 60)

    query = "AI pothole detection"

    print(f"\nQuery: {query}")
    print("\nConnecting to OpenAlex...")

    client = OpenAlexClient()

    papers = client.search_works(
        query=query,
        max_results=10
    )

    print(f"Papers retrieved: {len(papers)}")

    if not papers:
        print("ERROR: No papers returned.")
        return

    normalized = PaperNormalizer.normalize_many(papers)

    print(f"Normalized papers: {len(normalized)}")

    print("\n" + "-" * 60)

    for index, paper in enumerate(normalized[:5], start=1):

        print(f"\nPaper {index}")
        print(f"Title       : {paper['title']}")
        print(f"Year        : {paper['publication_year']}")
        print(f"Authors     : {', '.join(paper['authors'][:3])}")
        print(f"Citations   : {paper['citation_count']}")
        print(f"Open Access : {paper['open_access']}")
        print(f"DOI         : {paper['doi']}")
        print(f"URL         : {paper['url']}")

    print("\n" + "=" * 60)
    print("OPENALEX PAPER TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()