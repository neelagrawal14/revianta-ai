from typing import List, Dict


class ResearchGapDetector:
    """
    Stage 1 Research Gap Detector for Revianta AI.

    Identifies potential research gaps by comparing
    the proposed project with existing research.

    This is an explainable baseline. It does not claim
    to prove that a research gap exists.
    """

    def __init__(
        self,
        low_similarity_threshold: float = 0.40,
        high_similarity_threshold: float = 0.70
    ):
        self.low_similarity_threshold = low_similarity_threshold
        self.high_similarity_threshold = high_similarity_threshold

    def classify_research(
        self,
        similarity_score: float
    ) -> str:
        """
        Classify how closely an existing research item
        relates to the proposed project.
        """

        if similarity_score >= self.high_similarity_threshold:
            return "Highly Related"

        if similarity_score >= self.low_similarity_threshold:
            return "Moderately Related"

        return "Weakly Related"

    def calculate_gap_score(
        self,
        similarity_scores: List[float]
    ) -> float:
        """
        Estimate potential research-gap strength.

        Lower average similarity indicates that the proposed
        project is less represented by the provided research.

        Returns a score from 0 to 100.
        """

        if not similarity_scores:
            return 100.0

        valid_scores = [
            max(-1.0, min(1.0, score))
            for score in similarity_scores
        ]

        # Convert cosine similarity [-1, 1]
        # into normalized similarity [0, 1].
        normalized_scores = [
            (score + 1) / 2
            for score in valid_scores
        ]

        average_similarity = sum(
            normalized_scores
        ) / len(normalized_scores)

        gap_score = (1 - average_similarity) * 100

        return float(gap_score)

    def identify_gap_type(
        self,
        similarity_scores: List[float]
    ) -> str:
        """
        Provide an interpretable description of the
        potential research-gap situation.
        """

        if not similarity_scores:
            return "Insufficient comparison data"

        highest_similarity = max(similarity_scores)
        average_similarity = sum(similarity_scores) / len(
            similarity_scores
        )

        if highest_similarity < self.low_similarity_threshold:
            return "Potentially unexplored area"

        if average_similarity < self.low_similarity_threshold:
            return "Potential research gap"

        if average_similarity < self.high_similarity_threshold:
            return "Partially explored area"

        return "Well explored area"

    def analyze(
        self,
        similarity_scores: List[float]
    ) -> Dict:
        """
        Perform complete research-gap analysis.
        """

        if not similarity_scores:
            return {
                "gap_score": 100.0,
                "gap_type": "Insufficient comparison data",
                "highest_similarity": None,
                "average_similarity": None,
                "research_classification": []
            }

        classifications = []

        for index, score in enumerate(
            similarity_scores,
            start=1
        ):
            classifications.append({
                "research_id": index,
                "similarity": round(score, 4),
                "classification": self.classify_research(score)
            })

        gap_score = self.calculate_gap_score(
            similarity_scores
        )

        gap_type = self.identify_gap_type(
            similarity_scores
        )

        return {
            "gap_score": round(gap_score, 2),
            "gap_type": gap_type,
            "highest_similarity": round(
                max(similarity_scores),
                4
            ),
            "average_similarity": round(
                sum(similarity_scores)
                / len(similarity_scores),
                4
            ),
            "research_classification": classifications
        }


if __name__ == "__main__":

    print("\n========== REVIANTA AI RESEARCH GAP DETECTOR ==========\n")

    detector = ResearchGapDetector()

    # Similarity between the proposed project
    # and existing research.
    similarity_scores = [
        0.7629,
        0.6500,
        0.5100,
        0.4300,
        0.2800
    ]

    print("Existing Research Similarity:")

    for index, score in enumerate(
        similarity_scores,
        start=1
    ):
        classification = detector.classify_research(score)

        print(
            f"Research {index}: "
            f"{score:.4f} "
            f"({score * 100:.2f}%) "
            f"→ {classification}"
        )

    result = detector.analyze(
        similarity_scores
    )

    print("\nHighest Similarity:")
    print(
        f"{result['highest_similarity']:.4f}"
    )

    print("\nAverage Similarity:")
    print(
        f"{result['average_similarity']:.4f}"
    )

    print("\nPotential Gap Score:")
    print(
        f"{result['gap_score']:.2f}/100"
    )

    print("\nGap Assessment:")
    print(
        result["gap_type"]
    )

    print("\n=======================================================\n")