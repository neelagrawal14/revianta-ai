"""
============================================================
REVIANTA AI - STAGE 2
ERROR ANALYSIS
============================================================

Analyzes mistakes made by the trained NRIE Stage 2 model.

Handles both:
    0 / 1 / 2
and:
    Fully / Partially / Abandoned

No model retraining is performed.
============================================================
"""

from pathlib import Path

import pandas as pd
import numpy as np


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[3]

DATA_DIR = BASE_DIR / "data" / "stage2"

MODEL_DIR = DATA_DIR / "models"

TEST_FILE = DATA_DIR / "test.csv"

PREDICTIONS_FILE = (
    MODEL_DIR / "test_predictions.csv"
)

ERROR_FILE = (
    MODEL_DIR / "error_analysis.csv"
)

SUMMARY_FILE = (
    MODEL_DIR / "error_analysis_report.txt"
)

CONFIDENCE_FILE = (
    MODEL_DIR / "uncertain_predictions.csv"
)


# ============================================================
# CLASS MAPPING
# ============================================================

CLASS_NAMES = {
    0: "Fully",
    1: "Partially",
    2: "Abandoned"
}

CLASS_TO_ID = {
    "Fully": 0,
    "Partially": 1,
    "Abandoned": 2
}


# ============================================================
# HELPERS
# ============================================================

def check_file(path):

    if not path.exists():

        raise FileNotFoundError(
            f"\nRequired file not found:\n{path}"
        )


def normalize_label(value):

    """
    Converts:
        0 -> Fully
        1 -> Partially
        2 -> Abandoned

    and preserves text labels.
    """

    if pd.isna(value):
        return "Unknown"

    # Numeric values
    if isinstance(value, (int, np.integer)):

        return CLASS_NAMES.get(
            int(value),
            "Unknown"
        )

    if isinstance(value, (float, np.floating)):

        if value in [0.0, 1.0, 2.0]:

            return CLASS_NAMES.get(
                int(value),
                "Unknown"
            )

    # Text values
    text = str(value).strip()

    if text in CLASS_TO_ID:

        return text

    # Handle numeric strings
    if text in ["0", "1", "2"]:

        return CLASS_NAMES[
            int(text)
        ]

    return text


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)

    print(
        "       REVIANTA AI - STAGE 2 ERROR ANALYSIS"
    )

    print("=" * 70)


    # ========================================================
    # 1. CHECK FILES
    # ========================================================

    print(
        "\nChecking required files..."
    )

    check_file(TEST_FILE)
    check_file(PREDICTIONS_FILE)

    print(
        "All required files found."
    )


    # ========================================================
    # 2. LOAD TEST DATA
    # ========================================================

    print(
        "\nLoading original test records..."
    )

    test_df = pd.read_csv(
        TEST_FILE
    )

    print(
        f"Test records: {len(test_df)}"
    )


    # ========================================================
    # 3. LOAD PREDICTIONS
    # ========================================================

    print(
        "\nLoading model predictions..."
    )

    pred_df = pd.read_csv(
        PREDICTIONS_FILE
    )

    print(
        f"Prediction records: {len(pred_df)}"
    )


    # ========================================================
    # 4. VALIDATE ROW COUNTS
    # ========================================================

    if len(test_df) != len(pred_df):

        raise ValueError(
            "Test data and prediction row counts do not match."
        )


    # ========================================================
    # 5. BUILD ANALYSIS DATAFRAME
    # ========================================================

    print(
        "\nBuilding error analysis..."
    )

    analysis_df = test_df.copy()


    # ========================================================
    # 6. NORMALIZE ACTUAL LABELS
    # ========================================================

    analysis_df[
        "actual_outcome"
    ] = analysis_df[
        "project_outcome"
    ].apply(
        normalize_label
    )


    # ========================================================
    # 7. NORMALIZE PREDICTED LABELS
    # ========================================================

    analysis_df[
        "predicted_outcome"
    ] = pred_df[
        "predicted_outcome"
    ].apply(
        normalize_label
    )


    # ========================================================
    # 8. COPY PROBABILITIES
    # ========================================================

    probability_columns = [
        "probability_fully",
        "probability_partially",
        "probability_abandoned"
    ]


    for column in probability_columns:

        if column not in pred_df.columns:

            raise ValueError(
                f"Missing prediction column: {column}"
            )

        analysis_df[column] = (
            pred_df[column]
        )


    # ========================================================
    # 9. CORRECT / INCORRECT
    # ========================================================

    analysis_df[
        "correct_prediction"
    ] = (
        analysis_df[
            "actual_outcome"
        ]
        ==
        analysis_df[
            "predicted_outcome"
        ]
    )


    # ========================================================
    # 10. CONFIDENCE
    # ========================================================

    analysis_df[
        "prediction_confidence"
    ] = analysis_df[
        probability_columns
    ].max(
        axis=1
    )


    # ========================================================
    # 11. PREDICTION MARGIN
    # ========================================================

    sorted_probabilities = np.sort(
        analysis_df[
            probability_columns
        ].values,
        axis=1
    )


    analysis_df[
        "prediction_margin"
    ] = (
        sorted_probabilities[:, -1]
        -
        sorted_probabilities[:, -2]
    )


    # ========================================================
    # 12. ERROR TYPE
    # ========================================================

    def get_error_type(row):

        actual = row[
            "actual_outcome"
        ]

        predicted = row[
            "predicted_outcome"
        ]

        if actual == predicted:

            return "Correct"

        return (
            f"{actual} -> {predicted}"
        )


    analysis_df[
        "error_type"
    ] = analysis_df.apply(
        get_error_type,
        axis=1
    )


    # ========================================================
    # 13. OVERALL ANALYSIS
    # ========================================================

    total = len(
        analysis_df
    )

    correct = int(
        analysis_df[
            "correct_prediction"
        ].sum()
    )

    incorrect = (
        total - correct
    )


    print(
        "\n"
        + "=" * 60
    )

    print(
        "OVERALL PREDICTION ANALYSIS"
    )

    print(
        "=" * 60
    )

    print(
        f"Total predictions : {total}"
    )

    print(
        f"Correct           : {correct}"
    )

    print(
        f"Incorrect         : {incorrect}"
    )

    print(
        f"Accuracy          : "
        f"{correct / total:.4f}"
    )


    # ========================================================
    # 14. ERROR BREAKDOWN
    # ========================================================

    print(
        "\n"
        + "=" * 60
    )

    print(
        "ERROR BREAKDOWN"
    )

    print(
        "=" * 60
    )


    error_counts = (
        analysis_df[
            "error_type"
        ]
        .value_counts()
    )


    for error_type, count in error_counts.items():

        print(
            f"{error_type:<30} : {count}"
        )


    # ========================================================
    # 15. CLASS-WISE ANALYSIS
    # ========================================================

    print(
        "\n"
        + "=" * 60
    )

    print(
        "CLASS-WISE ERROR ANALYSIS"
    )

    print(
        "=" * 60
    )


    for class_name in [
        "Fully",
        "Partially",
        "Abandoned"
    ]:

        class_df = analysis_df[
            analysis_df[
                "actual_outcome"
            ]
            ==
            class_name
        ]


        class_total = len(
            class_df
        )


        class_correct = int(
            class_df[
                "correct_prediction"
            ].sum()
        )


        class_incorrect = (
            class_total
            - class_correct
        )


        print(
            f"\n{class_name}"
        )

        print(
            f"  Total     : {class_total}"
        )

        print(
            f"  Correct   : {class_correct}"
        )

        print(
            f"  Incorrect : {class_incorrect}"
        )


        if class_total > 0:

            print(
                f"  Recall    : "
                f"{class_correct / class_total:.4f}"
            )

        else:

            print(
                "  Recall    : N/A"
            )


        print(
            "  Predictions:"
        )


        class_predictions = (
            class_df[
                "predicted_outcome"
            ]
            .value_counts()
        )


        for prediction, count in (
            class_predictions.items()
        ):

            print(
                f"    -> {prediction}: {count}"
            )


    # ========================================================
    # 16. CONFIDENCE ANALYSIS
    # ========================================================

    print(
        "\n"
        + "=" * 60
    )

    print(
        "CONFIDENCE ANALYSIS"
    )

    print(
        "=" * 60
    )


    correct_df = analysis_df[
        analysis_df[
            "correct_prediction"
        ]
    ]


    incorrect_df = analysis_df[
        ~analysis_df[
            "correct_prediction"
        ]
    ]


    if len(correct_df) > 0:

        print(
            f"\nAverage confidence - Correct:"
            f" {correct_df['prediction_confidence'].mean():.4f}"
        )

        print(
            f"Average margin - Correct:"
            f" {correct_df['prediction_margin'].mean():.4f}"
        )


    if len(incorrect_df) > 0:

        print(
            f"Average confidence - Incorrect:"
            f" {incorrect_df['prediction_confidence'].mean():.4f}"
        )

        print(
            f"Average margin - Incorrect:"
            f" {incorrect_df['prediction_margin'].mean():.4f}"
        )


    # ========================================================
    # 17. UNCERTAIN PREDICTIONS
    # ========================================================

    print(
        "\n"
        + "=" * 60
    )

    print(
        "UNCERTAIN PREDICTIONS"
    )

    print(
        "=" * 60
    )


    LOW_CONFIDENCE = 0.50
    LOW_MARGIN = 0.15


    uncertain_df = analysis_df[
        (
            analysis_df[
                "prediction_confidence"
            ] < LOW_CONFIDENCE
        )
        |
        (
            analysis_df[
                "prediction_margin"
            ] < LOW_MARGIN
        )
    ].copy()


    print(
        f"\nUncertain predictions:"
        f" {len(uncertain_df)}"
    )

    print(
        f"Percentage:"
        f" {len(uncertain_df) / total * 100:.2f}%"
    )


    if len(uncertain_df) > 0:

        display_columns = [
            "project_title",
            "actual_outcome",
            "predicted_outcome",
            "probability_fully",
            "probability_partially",
            "probability_abandoned",
            "prediction_confidence",
            "prediction_margin",
            "error_type"
        ]


        available_columns = [
            column
            for column in display_columns
            if column in uncertain_df.columns
        ]


        print(
            "\nFirst 20 uncertain predictions:"
        )

        print(
            uncertain_df[
                available_columns
            ]
            .head(20)
            .to_string(index=False)
        )


    # ========================================================
    # 18. ABANDONED ANALYSIS
    # ========================================================

    print(
        "\n"
        + "=" * 60
    )

    print(
        "ABANDONED PROJECT ERROR ANALYSIS"
    )

    print(
        "=" * 60
    )


    abandoned_df = analysis_df[
        analysis_df[
            "actual_outcome"
        ]
        ==
        "Abandoned"
    ]


    abandoned_correct = int(
        (
            abandoned_df[
                "predicted_outcome"
            ]
            ==
            "Abandoned"
        ).sum()
    )


    abandoned_missed = abandoned_df[
        abandoned_df[
            "predicted_outcome"
        ]
        !=
        "Abandoned"
    ]


    print(
        f"Actual abandoned projects:"
        f" {len(abandoned_df)}"
    )

    print(
        f"Correctly detected:"
        f" {abandoned_correct}"
    )

    print(
        f"Missed abandoned projects:"
        f" {len(abandoned_missed)}"
    )


    # ========================================================
    # 19. FULLY ANALYSIS
    # ========================================================

    print(
        "\n"
        + "=" * 60
    )

    print(
        "FULLY COMPLETED PROJECT ERROR ANALYSIS"
    )

    print(
        "=" * 60
    )


    fully_df = analysis_df[
        analysis_df[
            "actual_outcome"
        ]
        ==
        "Fully"
    ]


    fully_correct = int(
        fully_df[
            "correct_prediction"
        ].sum()
    )


    fully_missed = fully_df[
        ~fully_df[
            "correct_prediction"
        ]
    ]


    print(
        f"Actual fully completed:"
        f" {len(fully_df)}"
    )

    print(
        f"Correctly detected:"
        f" {fully_correct}"
    )

    print(
        f"Misclassified:"
        f" {len(fully_missed)}"
    )


    # ========================================================
    # 20. PARTIALLY ANALYSIS
    # ========================================================

    print(
        "\n"
        + "=" * 60
    )

    print(
        "PARTIALLY COMPLETED PROJECT ERROR ANALYSIS"
    )

    print(
        "=" * 60
    )


    partially_df = analysis_df[
        analysis_df[
            "actual_outcome"
        ]
        ==
        "Partially"
    ]


    partially_correct = int(
        partially_df[
            "correct_prediction"
        ].sum()
    )


    partially_missed = partially_df[
        ~partially_df[
            "correct_prediction"
        ]
    ]


    print(
        f"Actual partially completed:"
        f" {len(partially_df)}"
    )

    print(
        f"Correctly detected:"
        f" {partially_correct}"
    )

    print(
        f"Misclassified:"
        f" {len(partially_missed)}"
    )


    # ========================================================
    # 21. SAVE ERROR ANALYSIS
    # ========================================================

    analysis_df.to_csv(
        ERROR_FILE,
        index=False
    )


    # ========================================================
    # 22. SAVE UNCERTAIN PREDICTIONS
    # ========================================================

    uncertain_df.to_csv(
        CONFIDENCE_FILE,
        index=False
    )


    # ========================================================
    # 23. SUMMARY REPORT
    # ========================================================

    report = []

    report.append(
        "REVIANTA AI - STAGE 2 ERROR ANALYSIS"
    )

    report.append(
        "=" * 60
    )

    report.append("")

    report.append(
        "OVERALL"
    )

    report.append(
        f"Total predictions: {total}"
    )

    report.append(
        f"Correct: {correct}"
    )

    report.append(
        f"Incorrect: {incorrect}"
    )

    report.append(
        f"Accuracy: {correct / total:.6f}"
    )

    report.append("")

    report.append(
        "ERROR BREAKDOWN"
    )

    for error_type, count in error_counts.items():

        report.append(
            f"{error_type}: {count}"
        )

    report.append("")

    report.append(
        "CONFIDENCE"
    )

    if len(correct_df) > 0:

        report.append(
            f"Correct average confidence: "
            f"{correct_df['prediction_confidence'].mean():.6f}"
        )

        report.append(
            f"Correct average margin: "
            f"{correct_df['prediction_margin'].mean():.6f}"
        )

    if len(incorrect_df) > 0:

        report.append(
            f"Incorrect average confidence: "
            f"{incorrect_df['prediction_confidence'].mean():.6f}"
        )

        report.append(
            f"Incorrect average margin: "
            f"{incorrect_df['prediction_margin'].mean():.6f}"
        )

    report.append("")

    report.append(
        "UNCERTAIN PREDICTIONS"
    )

    report.append(
        f"Count: {len(uncertain_df)}"
    )

    report.append(
        f"Percentage: "
        f"{len(uncertain_df) / total * 100:.2f}%"
    )

    report.append("")

    report.append(
        "ABANDONED PROJECTS"
    )

    report.append(
        f"Actual: {len(abandoned_df)}"
    )

    report.append(
        f"Correctly detected: {abandoned_correct}"
    )

    report.append(
        f"Missed: {len(abandoned_missed)}"
    )

    report.append("")

    report.append(
        "FULLY COMPLETED PROJECTS"
    )

    report.append(
        f"Actual: {len(fully_df)}"
    )

    report.append(
        f"Correctly detected: {fully_correct}"
    )

    report.append(
        f"Misclassified: {len(fully_missed)}"
    )

    report.append("")

    report.append(
        "PARTIALLY COMPLETED PROJECTS"
    )

    report.append(
        f"Actual: {len(partially_df)}"
    )

    report.append(
        f"Correctly detected: {partially_correct}"
    )

    report.append(
        f"Misclassified: {len(partially_missed)}"
    )


    SUMMARY_FILE.write_text(
        "\n".join(report),
        encoding="utf-8"
    )


    # ========================================================
    # 24. FINAL
    # ========================================================

    print(
        "\n"
        + "=" * 70
    )

    print(
        "          ERROR ANALYSIS COMPLETE"
    )

    print(
        "=" * 70
    )

    print(
        "\nSaved:"
    )

    print(
        f"  {ERROR_FILE}"
    )

    print(
        f"  {CONFIDENCE_FILE}"
    )

    print(
        f"  {SUMMARY_FILE}"
    )

    print(
        "\nSTATUS: ERROR ANALYSIS COMPLETE"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()