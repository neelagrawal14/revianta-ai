from typing import List
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Embedding service for Revianta AI.

    Converts research text into numerical vectors
    that can later be used for similarity, novelty,
    research-gap detection, and recommendations.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2"
    ):
        self.model_name = model_name

        print(f"Loading embedding model: {model_name}")

        self.model = SentenceTransformer(model_name)

        print("Embedding model loaded successfully.")

    def generate_embedding(self, text: str) -> List[float]:
        """
        Convert a single text into an embedding vector.
        """

        if not text or not text.strip():
            return []

        embedding = self.model.encode(
            text,
            convert_to_numpy=True
        )

        return embedding.tolist()

    def generate_embeddings(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        """
        Convert multiple texts into embedding vectors.
        """

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True
        )

        return embeddings.tolist()

    def get_embedding_dimension(self) -> int:
        """
        Return the size of the embedding vector.
        """

        return self.model.get_sentence_embedding_dimension()


if __name__ == "__main__":

    print("\n========== REVIANTA AI EMBEDDING TEST ==========\n")

    service = EmbeddingService()

    project_description = """
    An AI-powered satellite image analysis system that detects
    urban development and changes using optical and SAR imagery.
    The system uses deep learning, computer vision and geospatial
    data to identify buildings, roads and other infrastructure.
    """

    embedding = service.generate_embedding(project_description)

    print("\nEmbedding Dimension:")
    print(len(embedding))

    print("\nFirst 10 Embedding Values:")

    for index, value in enumerate(embedding[:10], start=1):
        print(f"{index}. {value:.6f}")

    print("\nModel Embedding Dimension:")
    print(service.get_embedding_dimension())

    print("\n===============================================\n")