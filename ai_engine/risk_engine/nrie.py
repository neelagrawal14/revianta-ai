"""
NRIE - NOVA Risk Intelligence Engine

Stage 1 orchestrator.

Flow:
Project Features
        ↓
Risk Calculator
        ↓
7 Risk Scores
        ↓
Overall Risk
        ↓
Project Health
        ↓
Explanation Generator
        ↓
Complete NRIE Report
"""

from typing import Dict

from .risk_calculator import RiskCalculator
from .explanations import RiskExplanationGenerator


class NRIE:

    def __init__(self):
        self.risk_calculator = RiskCalculator()
        self.explanation_generator = RiskExplanationGenerator()

    def analyze(
        self,
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
    ) -> Dict:
        """
        Run the complete NRIE Stage 1 analysis.
        """

        # -------------------------------------------------
        # STEP 1: Calculate the seven risk dimensions
        # -------------------------------------------------

        calculation = self.risk_calculator.analyze(
            technology_count=technology_count,
            dataset_count=dataset_count,
            research_dependency_count=research_dependency_count,
            novelty_score=novelty_score,
            research_gap_score=research_gap_score,
            highest_similarity=highest_similarity,
            deployment_required=deployment_required,
            hardware_required=hardware_required,
            real_time_required=real_time_required,
            data_quality=data_quality,
            market_uncertainty=market_uncertainty,
        )

        risk_scores = calculation["risk_scores"]

        # -------------------------------------------------
        # STEP 2: Generate explanations
        # -------------------------------------------------

        explanations = self.explanation_generator.generate_all_explanations(
            risk_scores=risk_scores,
            technology_count=technology_count,
            dataset_count=dataset_count,
            research_dependency_count=research_dependency_count,
            novelty_score=novelty_score,
            research_gap_score=research_gap_score,
            highest_similarity=highest_similarity,
            deployment_required=deployment_required,
            hardware_required=hardware_required,
            real_time_required=real_time_required,
            data_quality=data_quality,
            market_uncertainty=market_uncertainty,
        )

        # -------------------------------------------------
        # STEP 3: Combine everything into one NRIE report
        # -------------------------------------------------

        return {
            "engine": "NRIE",
            "stage": "Stage 1 - Rule Based",

            "risk_scores": risk_scores,

            "overall_risk": calculation["overall_risk"],

            "health_score": calculation["health_score"],

            "explanations": explanations,
        }


def print_report(report: Dict) -> None:
    """Pretty-print a complete NRIE report."""

    print("\n")
    print("=" * 65)
    print("             NRIE PROJECT RISK REPORT")
    print("=" * 65)

    print(f"\nEngine: {report['engine']}")
    print(f"Stage:  {report['stage']}")

    print("\n" + "-" * 65)
    print("RISK SUMMARY")
    print("-" * 65)

    for dimension, score in report["risk_scores"].items():

        explanation = report["explanations"][dimension]

        print(
            f"{dimension.title():18}"
            f"{score:6.2f}/100"
            f"   {explanation['level']}"
        )

    print("\n" + "-" * 65)
    print("OVERALL PROJECT ASSESSMENT")
    print("-" * 65)

    print(
        f"Overall Risk:     "
        f"{report['overall_risk']:.2f}/100"
    )

    print(
        f"Project Health:   "
        f"{report['health_score']:.2f}/100"
    )

    print("\n" + "-" * 65)
    print("DETAILED EXPLANATIONS")
    print("-" * 65)

    for dimension, explanation in report["explanations"].items():

        print(f"\n{dimension.upper()} RISK")

        print(
            f"Score: {explanation['score']:.2f}/100"
        )

        print(
            f"Level: {explanation['level']}"
        )

        print(
            f"Reason: {explanation['reason']}"
        )

        print(
            f"Recommendation: "
            f"{explanation['recommendation']}"
        )

    print("\n" + "=" * 65)
    print("                 END OF NRIE REPORT")
    print("=" * 65)


if __name__ == "__main__":

    nrie = NRIE()

    report = nrie.analyze(

        # Project complexity
        technology_count=7,
        dataset_count=2,
        research_dependency_count=4,

        # Research intelligence
        novelty_score=11.85,
        research_gap_score=23.67,
        highest_similarity=0.7629,

        # System requirements
        deployment_required=True,
        hardware_required=True,
        real_time_required=False,

        # Data / business assumptions
        data_quality=0.6,
        market_uncertainty=0.5,
    )

    print_report(report)