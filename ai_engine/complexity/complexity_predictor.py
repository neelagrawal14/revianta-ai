from typing import Dict, Any


class ComplexityPredictor:
    """
    Stage 1 complexity predictor for Revianta AI.

    Calculates project implementation complexity using
    explainable project characteristics.

    Future versions can replace this rule-based approach
    with a trained ML model using historical project outcomes.
    """

    def __init__(self):
        self.weights = {
            "technology_count": 3,
            "dataset_count": 4,
            "research_dependency_count": 2,
            "deployment_requirement": 15,
            "hardware_requirement": 15,
            "real_time_requirement": 15
        }

    def calculate_score(
        self,
        technology_count: int,
        dataset_count: int,
        research_dependency_count: int,
        deployment_required: bool = False,
        hardware_required: bool = False,
        real_time_required: bool = False
    ) -> float:
        """
        Calculate a complexity score from 0 to 100.
        """

        score = 0.0

        # Technology complexity
        score += min(
            technology_count * self.weights["technology_count"],
            30
        )

        # Dataset complexity
        score += min(
            dataset_count * self.weights["dataset_count"],
            20
        )

        # Research dependency complexity
        score += min(
            research_dependency_count *
            self.weights["research_dependency_count"],
            10
        )

        # Additional implementation requirements
        if deployment_required:
            score += self.weights["deployment_requirement"]

        if hardware_required:
            score += self.weights["hardware_requirement"]

        if real_time_required:
            score += self.weights["real_time_requirement"]

        return min(score, 100.0)

    def classify_complexity(
        self,
        score: float
    ) -> str:
        """
        Convert complexity score into a human-readable level.
        """

        if score >= 75:
            return "Very High"

        if score >= 50:
            return "High"

        if score >= 25:
            return "Moderate"

        return "Low"

    def generate_explanation(
        self,
        score: float,
        technology_count: int,
        dataset_count: int,
        research_dependency_count: int,
        deployment_required: bool,
        hardware_required: bool,
        real_time_required: bool
    ) -> str:
        """
        Generate an explainable complexity assessment.
        """

        factors = []

        if technology_count >= 5:
            factors.append(
                f"{technology_count} technologies increase integration complexity"
            )

        if dataset_count >= 3:
            factors.append(
                f"{dataset_count} datasets increase data-processing complexity"
            )

        if research_dependency_count >= 3:
            factors.append(
                f"{research_dependency_count} research dependencies increase implementation uncertainty"
            )

        if deployment_required:
            factors.append(
                "deployment requirements add implementation complexity"
            )

        if hardware_required:
            factors.append(
                "hardware requirements add system complexity"
            )

        if real_time_required:
            factors.append(
                "real-time processing requirements add performance complexity"
            )

        if not factors:
            factors.append(
                "the project has relatively limited implementation requirements"
            )

        return "; ".join(factors) + "."

    def analyze(
        self,
        project_name: str,
        technology_count: int,
        dataset_count: int,
        research_dependency_count: int,
        deployment_required: bool = False,
        hardware_required: bool = False,
        real_time_required: bool = False
    ) -> Dict[str, Any]:
        """
        Perform complete project complexity analysis.
        """

        score = self.calculate_score(
            technology_count=technology_count,
            dataset_count=dataset_count,
            research_dependency_count=research_dependency_count,
            deployment_required=deployment_required,
            hardware_required=hardware_required,
            real_time_required=real_time_required
        )

        level = self.classify_complexity(score)

        explanation = self.generate_explanation(
            score=score,
            technology_count=technology_count,
            dataset_count=dataset_count,
            research_dependency_count=research_dependency_count,
            deployment_required=deployment_required,
            hardware_required=hardware_required,
            real_time_required=real_time_required
        )

        return {
            "project_name": project_name,
            "complexity_score": score,
            "complexity_level": level,
            "technology_count": technology_count,
            "dataset_count": dataset_count,
            "research_dependency_count": research_dependency_count,
            "deployment_required": deployment_required,
            "hardware_required": hardware_required,
            "real_time_required": real_time_required,
            "explanation": explanation
        }


if __name__ == "__main__":

    predictor = ComplexityPredictor()

    result = predictor.analyze(
        project_name="AI-Powered Satellite Image Analysis",

        technology_count=7,

        dataset_count=2,

        research_dependency_count=4,

        deployment_required=True,

        hardware_required=True,

        real_time_required=False
    )

    print("\n========== COMPLEXITY PREDICTION ==========\n")

    print(f"Project: {result['project_name']}")

    print(
        f"Complexity Score: "
        f"{result['complexity_score']:.2f}/100"
    )

    print(
        f"Complexity Level: "
        f"{result['complexity_level']}"
    )

    print("\nComplexity Factors:")

    print(
        f"- Technologies: "
        f"{result['technology_count']}"
    )

    print(
        f"- Datasets: "
        f"{result['dataset_count']}"
    )

    print(
        f"- Research Dependencies: "
        f"{result['research_dependency_count']}"
    )

    print(
        f"- Deployment Required: "
        f"{result['deployment_required']}"
    )

    print(
        f"- Hardware Required: "
        f"{result['hardware_required']}"
    )

    print(
        f"- Real-Time Required: "
        f"{result['real_time_required']}"
    )

    print("\nExplanation:")
    print(result["explanation"])