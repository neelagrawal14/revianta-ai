"""
Revianta Similarity Engine

Provides semantic similarity comparison between project text
and existing research/project text using shared embeddings.
"""

from typing import List

import numpy as np
from ..embeddings.embedding_service import EmbeddingService


class SimilarityEngine:
    """
    Semantic similarity engine.

    Uses a shared EmbeddingService instance so the embedding
    model is loaded only once by the Revianta pipeline.
    """

    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service

    # =========================================================
    # COSINE SIMILARITY
    # =========================================================

    def cosine_similarity(
        self,
        embedding_a: List[float],
        embedding_b: List[float],
    ) -> float:

        if not embedding_a or not embedding_b:
            raise ValueError(
                "Embeddings cannot be empty."
            )

        vector_a = np.array(
            embedding_a,
            dtype=float,
        )

        vector_b = np.array(
            embedding_b,
            dtype=float,
        )

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

        similarity = (
            np.dot(vector_a, vector_b)
            / (norm_a * norm_b)
        )

        return float(similarity)

    # =========================================================
    # COMPARE EMBEDDINGS
    # =========================================================

    def compare_embeddings(
        self,
        embedding_a: List[float],
        embedding_b: List[float],
    ) -> float:
        """
        Compare two already-generated embeddings.

        This avoids recalculating embeddings when they already
        exist.
        """

        return self.cosine_similarity(
            embedding_a,
            embedding_b,
        )

    # =========================================================
    # COMPARE TEXTS
    # =========================================================

    def compare_texts(
        self,
        text_a: str,
        text_b: str,
    ) -> float:
        """
        Generate embeddings for two texts and compare them.

        Useful for standalone similarity tests.
        """

        if not text_a or not text_a.strip():
            raise ValueError(
                "Text A cannot be empty."
            )

        if not text_b or not text_b.strip():
            raise ValueError(
                "Text B cannot be empty."
            )

        embedding_a = (
            self.embedding_service.generate_embedding(
                text_a
            )
        )

        embedding_b = (
            self.embedding_service.generate_embedding(
                text_b
            )
        )

        return self.compare_embeddings(
            embedding_a,
            embedding_b,
        )