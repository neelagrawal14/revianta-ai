"""
NRIE Stage 1 risk weights.

All weights are configurable so they can be tuned later
using real project outcome data.

Risk scores are expressed on a 0-100 scale.
"""

RISK_WEIGHTS = {
    "technical": 0.20,
    "dataset": 0.15,
    "implementation": 0.20,
    "novelty": 0.15,
    "research": 0.10,
    "deployment": 0.10,
    "business": 0.10,
}


def validate_weights(weights: dict[str, float]) -> None:
    """
    Validate that all seven NRIE dimensions exist
    and their weights sum to 1.0.
    """

    required_dimensions = {
        "technical",
        "dataset",
        "implementation",
        "novelty",
        "research",
        "deployment",
        "business",
    }

    missing = required_dimensions - weights.keys()

    if missing:
        raise ValueError(
            f"Missing NRIE risk dimensions: {sorted(missing)}"
        )

    if any(weight < 0 for weight in weights.values()):
        raise ValueError(
            "Risk weights cannot be negative."
        )

    total = sum(weights.values())

    if abs(total - 1.0) > 1e-6:
        raise ValueError(
            f"NRIE risk weights must sum to 1.0. "
            f"Current total: {total}"
        )


validate_weights(RISK_WEIGHTS)


if __name__ == "__main__":

    print("\n========== NRIE RISK WEIGHTS ==========\n")

    for dimension, weight in RISK_WEIGHTS.items():
        print(
            f"{dimension.title():15} "
            f"{weight:.0%}"
        )

    print(
        f"\nTotal: {sum(RISK_WEIGHTS.values()):.0%}"
    )

    print("\nWeight validation: PASSED")