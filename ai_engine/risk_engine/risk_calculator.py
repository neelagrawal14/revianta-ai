"""
NRIE Stage 1 Risk Calculator

Calculates the seven NRIE risk dimensions using
observable project-level features.

All risk scores:
    0   = very low risk
    100 = very high risk
"""

from typing import Dict

from .risk_weights import RISK_WEIGHTS


class RiskCalculator:

    def __init__(self):
        self.weights = RISK_WEIGHTS

    @staticmethod
    def _clamp(value: float, minimum: float = 0, maximum: float = 100) -> float:
        """Keep a score between 0 and 100."""
        return max(minimum, min(value, maximum))

    def calculate_technical_risk(
        self,
        technology_count: int,
        hardware_required: bool = False,
        real_time_required: bool = False,
    ) -> float:
        """
        Technical risk increases with:
        - number of technologies
        - hardware requirements
        - real-time requirements
        """

        risk = technology_count * 5

        if hardware_required:
            risk += 20

        if real_time_required:
            risk += 20

        return self._clamp(risk)

    def calculate_dataset_risk(
        self,
        dataset_count: int,
        data_quality: float = 0.5,
    ) -> float:
        """
        Dataset risk considers:
        - number of datasets
        - estimated data quality

        data_quality:
            0.0 = poor
            1.0 = excellent
        """

        risk = dataset_count * 8

        quality_penalty = (1 - data_quality) * 40

        risk += quality_penalty

        return self._clamp(risk)

    def calculate_implementation_risk(
        self,
        technology_count: int,
        research_dependency_count: int,
        deployment_required: bool = False,
    ) -> float:
        """
        Implementation risk increases with:
        - technology integration
        - research dependencies
        - deployment requirements
        """

        risk = technology_count * 4
        risk += research_dependency_count * 5

        if deployment_required:
            risk += 20

        return self._clamp(risk)

    def calculate_novelty_risk(
        self,
        novelty_score: float,
    ) -> float:
        """
        Low novelty means higher risk.

        novelty_score:
            0   = not novel
            100 = highly novel
        """

        return self._clamp(100 - novelty_score)

    def calculate_research_risk(
        self,
        research_gap_score: float,
        highest_similarity: float,
    ) -> float:
        """
        Research risk considers:
        - research gap score
        - similarity to existing research

        Higher gap score reduces research risk.
        Higher similarity increases risk of overlap.
        """

        gap_component = 100 - research_gap_score
        similarity_component = max(0, highest_similarity) * 100

        risk = (
            gap_component * 0.6
            + similarity_component * 0.4
        )

        return self._clamp(risk)

    def calculate_deployment_risk(
        self,
        deployment_required: bool,
        hardware_required: bool = False,
        real_time_required: bool = False,
    ) -> float:
        """Calculate deployment-related risk."""

        risk = 0

        if deployment_required:
            risk += 50

        if hardware_required:
            risk += 25

        if real_time_required:
            risk += 25

        return self._clamp(risk)

    def calculate_business_risk(
        self,
        market_uncertainty: float = 0.5,
    ) -> float:
        """
        Business risk based on estimated market uncertainty.

        market_uncertainty:
            0.0 = low uncertainty
            1.0 = high uncertainty
        """

        return self._clamp(market_uncertainty * 100)

    def calculate_overall_risk(
        self,
        risk_scores: Dict[str, float],
    ) -> float:
        """
        Calculate weighted overall risk.
        """

        weighted_risk = 0

        for dimension, weight in self.weights.items():
            score = risk_scores.get(dimension, 0)
            weighted_risk += score * weight

        return round(self._clamp(weighted_risk), 2)

    def calculate_health_score(
        self,
        overall_risk: float,
    ) -> float:
        """
        Overall Project Health Score.

        Higher risk -> lower health.
        """

        return round(
            self._clamp(100 - overall_risk),
            2
        )

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

        risk_scores = {
            "technical": self.calculate_technical_risk(
                technology_count,
                hardware_required,
                real_time_required,
            ),

            "dataset": self.calculate_dataset_risk(
                dataset_count,
                data_quality,
            ),

            "implementation": self.calculate_implementation_risk(
                technology_count,
                research_dependency_count,
                deployment_required,
            ),

            "novelty": self.calculate_novelty_risk(
                novelty_score,
            ),

            "research": self.calculate_research_risk(
                research_gap_score,
                highest_similarity,
            ),

            "deployment": self.calculate_deployment_risk(
                deployment_required,
                hardware_required,
                real_time_required,
            ),

            "business": self.calculate_business_risk(
                market_uncertainty,
            ),
        }

        overall_risk = self.calculate_overall_risk(
            risk_scores
        )

        health_score = self.calculate_health_score(
            overall_risk
        )

        return {
            "risk_scores": risk_scores,
            "overall_risk": overall_risk,
            "health_score": health_score,
        }


if __name__ == "__main__":

    calculator = RiskCalculator()

    result = calculator.analyze(
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

    print("\n========== NRIE RISK CALCULATOR ==========\n")

    print("RISK SCORES")

    for dimension, score in result["risk_scores"].items():
        print(
            f"- {dimension.title():15} "
            f"{score:.2f}/100"
        )

    print("\nOVERALL RISK")
    print(f"- {result['overall_risk']:.2f}/100")

    print("\nPROJECT HEALTH")
    print(f"- {result['health_score']:.2f}/100")