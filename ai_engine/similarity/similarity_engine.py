from typing import List
import numpy as np

from embeddings.embedding_service import EmbeddingService


class SimilarityEngine:
    """
    Calculates semantic similarity between research texts
    using sentence embeddings and cosine similarity.
    """

    def __init__(self):
        self.embedding_service = EmbeddingService()

    def cosine_similarity(
        self,
        embedding_a: List[float],
        embedding_b: List[float]
    ) -> float:

        if not embedding_a or not embedding_b:
            raise ValueError("Embeddings cannot be empty.")

        vector_a = np.array(embedding_a, dtype=float)
        vector_b = np.array(embedding_b, dtype=float)

        if vector_a.shape != vector_b.shape:
            raise ValueError(
                "Embeddings must have the same dimensions."
            )

        norm_a = np.linalg.norm(vector_a)
        norm_b = np.linalg.norm(vector_b)

        if norm_a == 0 or norm_b == 0:
            raise ValueError(
                "Cannot calculate similarity for a zero vector."
            )

        similarity = np.dot(vector_a, vector_b) / (
            norm_a * norm_b
        )

        return float(similarity)

    def compare_texts(
        self,
        text_a: str,
        text_b: str
    ) -> float:
        """
        Generate embeddings for two texts and
        calculate their semantic similarity.
        """

        embedding_a = self.embedding_service.generate_embedding(
            text_a
        )

        embedding_b = self.embedding_service.generate_embedding(
            text_b
        )

        return self.cosine_similarity(
            embedding_a,
            embedding_b
        )


if __name__ == "__main__":

    print("\n========== REVIANTA AI SEMANTIC SIMILARITY ==========\n")

    engine = SimilarityEngine()

    project_a = """
    An AI-powered system for detecting urban development
    from satellite imagery using deep learning, computer vision,
    optical imagery and SAR data.
    """

    project_b = """
    A deep learning model that analyzes satellite images
    to identify changes in cities, buildings and infrastructure
    using optical and radar remote sensing data.
    """

    project_c = """
    A machine learning system for predicting crop diseases
    from agricultural leaf images.
    """

    project_d = """
    A web application for managing student attendance,
    assignments and academic records.
    """

    print("Project A:")
    print(project_a.strip())

    print("\nProject B:")
    print(project_b.strip())

    similarity_ab = engine.compare_texts(
        project_a,
        project_b
    )

    print("\nA ↔ B Similarity:")
    print(f"{similarity_ab:.4f}")
    print(f"{similarity_ab * 100:.2f}%")

    similarity_ac = engine.compare_texts(
        project_a,
        project_c
    )

    print("\nA ↔ C Similarity:")
    print(f"{similarity_ac:.4f}")
    print(f"{similarity_ac * 100:.2f}%")

    similarity_ad = engine.compare_texts(
        project_a,
        project_d
    )

    print("\nA ↔ D Similarity:")
    print(f"{similarity_ad:.4f}")
    print(f"{similarity_ad * 100:.2f}%")

    print("\n=====================================================\n")