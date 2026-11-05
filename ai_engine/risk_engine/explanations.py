"""
NRIE Stage 1 Explanations

Converts numerical risk scores into:
1. Risk level
2. Plain-English explanation
3. Recommendation

Stage 1 is rule-based and fully explainable.
"""


class RiskExplanationGenerator:

    @staticmethod
    def get_risk_level(score: float) -> str:
        """Convert a 0-100 risk score into a readable level."""

        if score >= 75:
            return "Very High"

        if score >= 50:
            return "High"

        if score >= 25:
            return "Moderate"

        return "Low"

    def explain_technical(
        self,
        score: float,
        technology_count: int,
        hardware_required: bool,
        real_time_required: bool,
    ) -> dict:

        reasons = []

        if technology_count > 5:
            reasons.append(
                f"{technology_count} technologies increase integration complexity"
            )

        if hardware_required:
            reasons.append(
                "hardware requirements add system complexity"
            )

        if real_time_required:
            reasons.append(
                "real-time processing increases technical difficulty"
            )

        if not reasons:
            reasons.append(
                "the project has relatively limited technical complexity"
            )

        return {
            "score": round(score, 2),
            "level": self.get_risk_level(score),
            "reason": "; ".join(reasons) + ".",
            "recommendation": (
                "Reduce unnecessary technologies and validate the "
                "most technically demanding components early."
            ),
        }

    def explain_dataset(
        self,
        score: float,
        dataset_count: int,
        data_quality: float,
    ) -> dict:

        if dataset_count == 0:
            reason = (
                "No dataset sources are currently identified, "
                "which creates a major data availability risk."
            )

            recommendation = (
                "Identify and validate at least one accessible "
                "dataset before implementation."
            )

        elif data_quality < 0.5:
            reason = (
                f"{dataset_count} dataset source(s) were identified, "
                "but estimated data quality is limited."
            )

            recommendation = (
                "Check annotation quality, size, balance, and access "
                "conditions before development."
            )

        else:
            reason = (
                f"{dataset_count} dataset source(s) are identified "
                "with acceptable estimated data quality."
            )

            recommendation = (
                "Validate dataset accessibility and suitability "
                "with a small sample before full implementation."
            )

        return {
            "score": round(score, 2),
            "level": self.get_risk_level(score),
            "reason": reason,
            "recommendation": recommendation,
        }

    def explain_implementation(
        self,
        score: float,
        technology_count: int,
        research_dependency_count: int,
        deployment_required: bool,
    ) -> dict:

        reasons = []

        if technology_count > 5:
            reasons.append(
                f"{technology_count} technologies need to be integrated"
            )

        if research_dependency_count > 2:
            reasons.append(
                f"{research_dependency_count} research dependencies "
                "increase implementation uncertainty"
            )

        if deployment_required:
            reasons.append(
                "deployment requirements add implementation complexity"
            )

        if not reasons:
            reasons.append(
                "the project has relatively manageable implementation requirements"
            )

        return {
            "score": round(score, 2),
            "level": self.get_risk_level(score),
            "reason": "; ".join(reasons) + ".",
            "recommendation": (
                "Simplify the technology stack, reduce unnecessary "
                "dependencies, and validate the core system before "
                "adding advanced components."
            ),
        }

    def explain_novelty(
        self,
        score: float,
        novelty_score: float,
        highest_similarity: float,
    ) -> dict:

        if score >= 75:
            reason = (
                f"The novelty score is only {novelty_score:.2f}/100 "
                f"and the strongest similarity is "
                f"{highest_similarity * 100:.2f}%, indicating "
                "substantial overlap with existing work."
            )

            recommendation = (
                "Identify a specific technical differentiator and "
                "clearly distinguish the project from the closest "
                "papers, repositories, and patents."
            )

        elif score >= 50:
            reason = (
                "The project shows noticeable similarity to existing "
                "research and may need stronger differentiation."
            )

            recommendation = (
                "Review the closest existing work and define a "
                "clearer contribution."
            )

        else:
            reason = (
                "The project shows comparatively lower overlap with "
                "the available similar research."
            )

            recommendation = (
                "Continue validating novelty against additional "
                "papers, repositories, and patents."
            )

        return {
            "score": round(score, 2),
            "level": self.get_risk_level(score),
            "reason": reason,
            "recommendation": recommendation,
        }

    def explain_research(
        self,
        score: float,
        research_gap_score: float,
        highest_similarity: float,
    ) -> dict:

        if score >= 75:
            reason = (
                f"The research gap score is {research_gap_score:.2f}/100 "
                f"while the strongest research similarity is "
                f"{highest_similarity * 100:.2f}%, suggesting the "
                "area is already substantially explored."
            )

            recommendation = (
                "Review the strongest related papers carefully and "
                "identify an unresolved research question or limitation."
            )

        elif score >= 50:
            reason = (
                "The project is located in an active research area "
                "with meaningful existing literature."
            )

            recommendation = (
                "Map the major existing approaches and identify "
                "a specific unresolved limitation."
            )

        else:
            reason = (
                "The available research evidence indicates relatively "
                "limited overlap with existing work."
            )

            recommendation = (
                "Expand the literature review to confirm whether "
                "the apparent research gap is genuine."
            )

        return {
            "score": round(score, 2),
            "level": self.get_risk_level(score),
            "reason": reason,
            "recommendation": recommendation,
        }

    def explain_deployment(
        self,
        score: float,
        deployment_required: bool,
        hardware_required: bool,
        real_time_required: bool,
    ) -> dict:

        reasons = []

        if deployment_required:
            reasons.append(
                "deployment is required"
            )

        if hardware_required:
            reasons.append(
                "hardware requirements increase system complexity"
            )

        if real_time_required:
            reasons.append(
                "real-time operation increases scalability and performance requirements"
            )

        if not reasons:
            reasons.append(
                "the project has limited deployment requirements"
            )

        return {
            "score": round(score, 2),
            "level": self.get_risk_level(score),
            "reason": "; ".join(reasons) + ".",
            "recommendation": (
                "Start with a simple deployment architecture and "
                "validate performance, scalability, and resource "
                "requirements before production deployment."
            ),
        }

    def explain_business(
        self,
        score: float,
        market_uncertainty: float,
    ) -> dict:

        if score >= 75:
            reason = (
                "High market uncertainty creates significant "
                "business and practical applicability risk."
            )

            recommendation = (
                "Validate the target users, competing solutions, "
                "development cost, and practical value early."
            )

        elif score >= 50:
            reason = (
                "There is moderate uncertainty regarding market "
                "applicability and competing solutions."
            )

            recommendation = (
                "Identify the target users and compare the project "
                "against existing alternatives."
            )

        else:
            reason = (
                "The estimated business uncertainty is relatively low."
            )

            recommendation = (
                "Continue validating practical applicability and "
                "potential differentiation."
            )

        return {
            "score": round(score, 2),
            "level": self.get_risk_level(score),
            "reason": reason,
            "recommendation": recommendation,
        }

    def generate_all_explanations(
        self,
        risk_scores: dict,
        technology_count: int,
        dataset_count: int,
        research_dependency_count: int,
        novelty_score: float,
        research_gap_score: float,
        highest_similarity: float,
        deployment_required: bool = False,
        hardware_required: bool = False,
        real_time_required: bool = False,
        data_quality: float = 0.5,
        market_uncertainty: float = 0.5,
    ) -> dict:

        return {

            "technical": self.explain_technical(
                risk_scores["technical"],
                technology_count,
                hardware_required,
                real_time_required,
            ),

            "dataset": self.explain_dataset(
                risk_scores["dataset"],
                dataset_count,
                data_quality,
            ),

            "implementation": self.explain_implementation(
                risk_scores["implementation"],
                technology_count,
                research_dependency_count,
                deployment_required,
            ),

            "novelty": self.explain_novelty(
                risk_scores["novelty"],
                novelty_score,
                highest_similarity,
            ),

            "research": self.explain_research(
                risk_scores["research"],
                research_gap_score,
                highest_similarity,
            ),

            "deployment": self.explain_deployment(
                risk_scores["deployment"],
                deployment_required,
                hardware_required,
                real_time_required,
            ),

            "business": self.explain_business(
                risk_scores["business"],
                market_uncertainty,
            ),
        }


if __name__ == "__main__":

    generator = RiskExplanationGenerator()

    scores = {
        "technical": 55,
        "dataset": 32,
        "implementation": 68,
        "novelty": 88.15,
        "research": 76.31,
        "deployment": 75,
        "business": 50,
    }

    explanations = generator.generate_all_explanations(
        risk_scores=scores,
        technology_count=7,
        dataset_count=2,
        research_dependency_count=4,
        novelty_score=11.85,
        research_gap_score=23.67,
        highest_similarity=0.7629,
        deployment_required=True,
        hardware_required=True,
        real_time_required=False,
        data_quality=0.6,
        market_uncertainty=0.5,
    )

    print("\n========== NRIE EXPLANATIONS ==========\n")

    for dimension, result in explanations.items():

        print(f"{dimension.upper()} RISK")
        print(f"Score: {result['score']}/100")
        print(f"Level: {result['level']}")
        print(f"Reason: {result['reason']}")
        print(f"Recommendation: {result['recommendation']}")
        print("-" * 60)