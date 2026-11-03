import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data_pipeline.papers.openalex_client import OpenAlexClient
from data_pipeline.papers.paper_normalizer import PaperNormalizer

from ai_engine.embeddings.embedding_service import EmbeddingService
from ai_engine.similarity.similarity_engine import SimilarityEngine


def main():

    print("=" * 70)
    print("       REVIANTA REAL PAPER SIMILARITY TEST")
    print("=" * 70)

    # ---------------------------------------------------------
    # PROJECT IDEA
    # ---------------------------------------------------------

    project_text = """
    AI-powered pothole detection using smartphone camera images.
    The system uses computer vision and deep learning to detect
    road potholes and road damage in real time.
    """

    print("\nPROJECT:")
    print(project_text.strip())

    # ---------------------------------------------------------
    # 1. SEARCH OPENALEX
    # ---------------------------------------------------------

    print("\n[1/4] Searching OpenAlex...")

    client = OpenAlexClient()

    papers = client.search_works(
        query="AI pothole detection",
        max_results=10
    )

    print(f"Papers retrieved: {len(papers)}")

    if not papers:
        raise RuntimeError("OpenAlex returned no papers.")

    # ---------------------------------------------------------
    # 2. NORMALIZE
    # ---------------------------------------------------------

    print("\n[2/4] Normalizing papers...")

    normalized_papers = PaperNormalizer.normalize_many(papers)

    valid_papers = []

    for paper in normalized_papers:

        title = paper.get("title")
        abstract = paper.get("abstract")

        if not title:
            continue

        text_parts = [title]

        if abstract:
            text_parts.append(abstract)

        paper["search_text"] = " ".join(text_parts)

        valid_papers.append(paper)

    print(f"Valid papers: {len(valid_papers)}")

    # ---------------------------------------------------------
    # 3. EMBEDDINGS
    # ---------------------------------------------------------

    print("\n[3/4] Generating embeddings...")

    embedding_service = EmbeddingService()

    project_embedding = embedding_service.generate_embedding(
        project_text
    )

    print(
        "Project embedding dimension:",
        len(project_embedding)
    )

    # ---------------------------------------------------------
    # 4. SIMILARITY
    # ---------------------------------------------------------

    print("\n[4/4] Calculating similarity...")

    similarity_engine = SimilarityEngine(embedding_service)

    results = []

    for paper in valid_papers:

        paper_embedding = embedding_service.generate_embedding(
            paper["search_text"]
        )

        score = similarity_engine.compare_embeddings(
            project_embedding,
            paper_embedding
        )

        results.append({
            "title": paper["title"],
            "year": paper["publication_year"],
            "citations": paper["citation_count"],
            "doi": paper["doi"],
            "similarity": float(score)
        })

    # Highest similarity first
    results.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )

    # ---------------------------------------------------------
    # RESULTS
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("              REAL PAPER SIMILARITY RESULTS")
    print("=" * 70)

    for index, result in enumerate(results, start=1):

        print(f"\n#{index}")
        print(f"Title      : {result['title']}")
        print(f"Year       : {result['year']}")
        print(f"Citations  : {result['citations']}")
        print(f"Similarity : {result['similarity']:.4f}")
        print(f"DOI        : {result['doi']}")

    highest = results[0]["similarity"]

    print("\n" + "-" * 70)
    print(f"Highest similarity: {highest:.4f}")
    print("-" * 70)

    print("\nREAL PAPER SIMILARITY TEST PASSED")


if __name__ == "__main__":
    main()