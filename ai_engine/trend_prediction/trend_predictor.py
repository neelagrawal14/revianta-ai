from typing import Dict, List, Any


class TrendPredictor:
    """
    Stage 1 trend predictor for Revianta AI.

    Analyzes historical research/activity counts and determines
    whether a research area is:

    - Growing
    - Stable
    - Declining

    Stage 1 is rule-based and explainable.

    Future versions can use real forecasting models once
    sufficient historical data is available.
    """

    def __init__(
        self,
        growth_threshold: float = 0.15,
        decline_threshold: float = -0.15
    ):
        self.growth_threshold = growth_threshold
        self.decline_threshold = decline_threshold

    def calculate_growth_rate(
        self,
        activity_counts: List[float]
    ) -> float:
        """
        Calculate overall growth rate from the first
        and last historical activity values.

        Example:
        [100, 120, 140]

        Growth rate = (140 - 100) / 100 = 0.40
        """

        if len(activity_counts) < 2:
            return 0.0

        first_value = activity_counts[0]
        last_value = activity_counts[-1]

        if first_value == 0:
            return 0.0

        return (last_value - first_value) / first_value

    def classify_trend(
        self,
        growth_rate: float
    ) -> str:
        """
        Classify the trend using predefined thresholds.
        """

        if growth_rate >= self.growth_threshold:
            return "Growing"

        if growth_rate <= self.decline_threshold:
            return "Declining"

        return "Stable"

    def calculate_average_growth(
        self,
        activity_counts: List[float]
    ) -> float:
        """
        Calculate average period-to-period growth.

        This gives additional context beyond the
        overall first-to-last growth rate.
        """

        if len(activity_counts) < 2:
            return 0.0

        growth_rates = []

        for previous, current in zip(
            activity_counts,
            activity_counts[1:]
        ):

            if previous == 0:
                continue

            growth = (current - previous) / previous
            growth_rates.append(growth)

        if not growth_rates:
            return 0.0

        return sum(growth_rates) / len(growth_rates)

    def generate_explanation(
        self,
        trend: str,
        growth_rate: float
    ) -> str:
        """
        Generate a human-readable explanation.
        """

        percentage = growth_rate * 100

        if trend == "Growing":
            return (
                f"Research activity increased by approximately "
                f"{percentage:.2f}% across the observed period."
            )

        if trend == "Declining":
            return (
                f"Research activity decreased by approximately "
                f"{abs(percentage):.2f}% across the observed period."
            )

        return (
            f"Research activity changed by approximately "
            f"{percentage:.2f}% across the observed period, "
            f"which is within the stable range."
        )

    def analyze(
        self,
        topic: str,
        years: List[int],
        activity_counts: List[float]
    ) -> Dict[str, Any]:
        """
        Perform complete trend analysis.
        """

        if len(years) != len(activity_counts):
            raise ValueError(
                "years and activity_counts must have the same length."
            )

        if len(activity_counts) < 2:
            return {
                "topic": topic,
                "trend": "Insufficient Data",
                "growth_rate": 0.0,
                "average_growth": 0.0,
                "years": years,
                "activity_counts": activity_counts,
                "explanation": (
                    "At least two historical observations "
                    "are required for trend analysis."
                )
            }

        growth_rate = self.calculate_growth_rate(
            activity_counts
        )

        average_growth = self.calculate_average_growth(
            activity_counts
        )

        trend = self.classify_trend(
            growth_rate
        )

        explanation = self.generate_explanation(
            trend,
            growth_rate
        )

        return {
            "topic": topic,
            "trend": trend,
            "growth_rate": growth_rate,
            "growth_percentage": growth_rate * 100,
            "average_growth": average_growth,
            "average_growth_percentage": average_growth * 100,
            "years": years,
            "activity_counts": activity_counts,
            "explanation": explanation
        }


if __name__ == "__main__":

    predictor = TrendPredictor()

    # Example historical research activity.
    #
    # In the real Revianta system these values will
    # eventually come from the research data pipeline.

    years = [
        2021,
        2022,
        2023,
        2024,
        2025
    ]

    activity_counts = [
        100,
        120,
        145,
        175,
        210
    ]

    result = predictor.analyze(
        topic="Satellite Image Analysis",
        years=years,
        activity_counts=activity_counts
    )

    print("\n========== TREND PREDICTION ==========\n")

    print(f"Topic: {result['topic']}")
    print(f"Trend: {result['trend']}")

    print(
        f"Overall Growth: "
        f"{result['growth_percentage']:.2f}%"
    )

    print(
        f"Average Period Growth: "
        f"{result['average_growth_percentage']:.2f}%"
    )

    print("\nHistorical Activity:")

    for year, count in zip(
        result["years"],
        result["activity_counts"]
    ):
        print(f"- {year}: {count}")

    print("\nExplanation:")
    print(result["explanation"])