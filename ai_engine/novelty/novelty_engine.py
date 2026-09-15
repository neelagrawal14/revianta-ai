from typing import List, Dict


class NoveltyEngine:
    """
    Stage 1 Novelty Engine for Revianta AI.

    Determines novelty based on semantic similarity
    with existing research.

    Higher similarity → Lower novelty
    Lower similarity  → Higher novelty
    """

    def calculate_novelty_score(
        self,
        similarity_scores: List[float]
    ) -> float:
        """
        Calculate novelty from a list of cosine similarity scores.

        The highest similarity is used as the strongest indication
        that existing research is close to the proposed project.

        Novelty = 1 - highest similarity

        Returns a score from 0 to 100.
        """

        if not similarity_scores:
            return 100.0

        highest_similarity = max(similarity_scores)

        # Clamp cosine similarity to valid range
        highest_similarity = max(
            -1.0,
            min(1.0, highest_similarity)
        )

        # Convert cosine similarity [-1, 1]
        # into a novelty score [0, 100].
        #
        # similarity = 1   → novelty = 0
        # similarity = 0   → novelty = 50
        # similarity = -1  → novelty = 100
        novelty_score = ((1 - highest_similarity) / 2) * 100

        return float(novelty_score)

    def get_novelty_level(
        self,
        novelty_score: float
    ) -> str:
        """
        Convert novelty score into an interpretable category.
        """

        if novelty_score >= 75:
            return "Highly Novel"

        if novelty_score >= 50:
            return "Moderately Novel"

        if novelty_score >= 25:
            return "Low Novelty"

        return "Very Low Novelty"

    def analyze(
        self,
        similarity_scores: List[float]
    ) -> Dict:
        """
        Perform complete novelty analysis.
        """

        if not similarity_scores:
            return {
                "novelty_score": 100.0,
                "highest_similarity": None,
                "novelty_level": "Highly Novel"
            }

        highest_similarity = max(similarity_scores)

        novelty_score = self.calculate_novelty_score(
            similarity_scores
        )

        novelty_level = self.get_novelty_level(
            novelty_score
        )

        return {
            "novelty_score": round(novelty_score, 2),
            "highest_similarity": round(
                highest_similarity,
                4
            ),
            "novelty_level": novelty_level
        }


if __name__ == "__main__":

    print("\n========== REVIANTA AI NOVELTY ENGINE ==========\n")

    engine = NoveltyEngine()

    # Similarity scores between a new project
    # and existing research.
    similarity_scores = [
        0.7629,
        0.6500,
        0.5100,
        0.4300,
        0.2800
    ]

    print("Existing Research Similarity Scores:")

    for index, score in enumerate(
        similarity_scores,
        start=1
    ):
        print(
            f"Research {index}: "
            f"{score:.4f} "
            f"({score * 100:.2f}%)"
        )

    result = engine.analyze(
        similarity_scores
    )

    print("\nHighest Similarity:")
    print(
        f"{result['highest_similarity']:.4f}"
    )

    print("\nNovelty Score:")
    print(
        f"{result['novelty_score']:.2f}/100"
    )

    print("\nNovelty Level:")
    print(
        result["novelty_level"]
    )

    print("\n===============================================\n")