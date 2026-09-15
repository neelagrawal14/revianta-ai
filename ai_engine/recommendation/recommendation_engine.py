from typing import Dict, List, Any


class RecommendationEngine:
    """
    Stage 1 recommendation engine for Revianta AI.

    Generates explainable research recommendations using:
    - extracted technologies
    - keywords
    - similarity results
    - novelty analysis
    - research-gap analysis

    Stage 1 is rule/score based.
    Future versions can use learned recommendations.
    """

    def __init__(self):
        self.recommendation_rules = {
            "high_novelty": 75,
            "moderate_novelty": 50,
            "low_novelty": 25,
            "high_similarity": 0.70,
            "moderate_similarity": 0.40,
        }

    def recommend_technologies(
        self,
        technologies: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Generate recommendations based on detected technologies.
        """

        if not technologies:
            return []

        recommendations = []

        for technology in technologies:
            recommendations.append({
                "technology": technology,
                "reason": f"{technology} is relevant to the detected project technologies.",
                "priority": "high"
            })

        return recommendations

    def recommend_research_direction(
        self,
        novelty_score: float,
        gap_score: float,
        gap_type: str
    ) -> List[Dict[str, Any]]:
        """
        Recommend possible research directions using
        novelty and research-gap scores.
        """

        recommendations = []

        if novelty_score >= self.recommendation_rules["high_novelty"]:
            recommendations.append({
                "direction": "Explore the novel research area further.",
                "reason": "The project shows a high novelty score.",
                "priority": "high"
            })

        elif novelty_score >= self.recommendation_rules["moderate_novelty"]:
            recommendations.append({
                "direction": "Investigate existing approaches before defining the final contribution.",
                "reason": "The project has moderate novelty.",
                "priority": "medium"
            })

        else:
            recommendations.append({
                "direction": "Identify a stronger research contribution or differentiating approach.",
                "reason": "The current novelty score is relatively low.",
                "priority": "high"
            })

        if gap_score >= 60:
            recommendations.append({
                "direction": "Investigate the identified research gap in depth.",
                "reason": "The analysis indicates a potentially significant research gap.",
                "priority": "high"
            })

        elif gap_score >= 30:
            recommendations.append({
                "direction": "Study partially explored areas for an opportunity to extend existing work.",
                "reason": "The research area appears partially explored.",
                "priority": "medium"
            })

        else:
            recommendations.append({
                "direction": "Look for a more specific or unexplored research problem.",
                "reason": "The current research area appears relatively well explored.",
                "priority": "medium"
            })

        return recommendations

    def recommend_based_on_similarity(
        self,
        similarity_scores: List[float]
    ) -> List[Dict[str, Any]]:
        """
        Generate recommendations based on semantic similarity
        with existing research/projects.
        """

        if not similarity_scores:
            return [{
                "direction": "Expand the research search space.",
                "reason": "No comparable research items were provided.",
                "priority": "high"
            }]

        highest_similarity = max(similarity_scores)

        recommendations = []

        if highest_similarity >= self.recommendation_rules["high_similarity"]:
            recommendations.append({
                "direction": "Review highly similar existing research and identify differentiation.",
                "reason": "Strong semantic similarity was detected.",
                "priority": "high"
            })

        elif highest_similarity >= self.recommendation_rules["moderate_similarity"]:
            recommendations.append({
                "direction": "Compare the project with moderately related research.",
                "reason": "Moderate semantic similarity was detected.",
                "priority": "medium"
            })

        else:
            recommendations.append({
                "direction": "Explore broader research literature and related technologies.",
                "reason": "Few strongly related research items were detected.",
                "priority": "high"
            })

        return recommendations

    def generate_recommendations(
        self,
        technologies: List[str],
        similarity_scores: List[float],
        novelty_score: float,
        gap_score: float,
        gap_type: str
    ) -> Dict[str, Any]:
        """
        Main recommendation pipeline.
        """

        technology_recommendations = self.recommend_technologies(
            technologies
        )

        research_recommendations = self.recommend_research_direction(
            novelty_score,
            gap_score,
            gap_type
        )

        similarity_recommendations = self.recommend_based_on_similarity(
            similarity_scores
        )

        all_recommendations = (
            technology_recommendations
            + research_recommendations
            + similarity_recommendations
        )

        return {
            "technology_recommendations": technology_recommendations,
            "research_recommendations": research_recommendations,
            "similarity_recommendations": similarity_recommendations,
            "recommendations": all_recommendations
        }


if __name__ == "__main__":

    engine = RecommendationEngine()

    technologies = [
        "Satellite Image Analysis",
        "Computer Vision",
        "Geospatial Data",
        "Deep Learning",
        "Optical Imagery",
        "SAR",
        "Artificial Intelligence"
    ]

    similarity_scores = [
        0.7629,
        0.65,
        0.51,
        0.43,
        0.28
    ]

    novelty_score = 11.85
    gap_score = 23.67
    gap_type = "Partially explored area"

    result = engine.generate_recommendations(
        technologies=technologies,
        similarity_scores=similarity_scores,
        novelty_score=novelty_score,
        gap_score=gap_score,
        gap_type=gap_type
    )

    print("\n========== RECOMMENDATION ENGINE ==========\n")

    for category, recommendations in result.items():

        if category == "recommendations":
            continue

        print(f"\n{category.upper()}")

        for recommendation in recommendations:
            print(
                f"- {recommendation.get('direction', recommendation.get('technology'))}"
            )
            print(f"  Priority: {recommendation['priority']}")
            print(f"  Reason: {recommendation['reason']}")