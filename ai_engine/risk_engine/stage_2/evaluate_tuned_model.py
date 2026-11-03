"""
============================================================
REVIANTA AI - STAGE 2
TUNED MODEL FINAL EVALUATION
============================================================

Evaluates the selected tuned XGBoost candidate on the
UNTOUCHED TEST SET.

Model selection was performed using:
    TRAIN + VALIDATION

This script uses:
    TEST

Purpose:
    Compare the tuned model against the original baseline
    on completely unseen test data.

============================================================
"""

from pathlib import Path
import json

import numpy as np
import pandas as pd

from scipy.sparse import load_npz

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    log_loss
)

from xgboost import XGBClassifier


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[3]

FEATURE_DIR = (
    BASE_DIR
    / "data"
    / "stage2"
    / "features"
)

MODEL_DIR = (
    BASE_DIR
    / "data"
    / "stage2"
    / "models"
)

X_TEST_FILE = (
    FEATURE_DIR
    / "X_test.npz"
)

Y_TEST_FILE = (
    FEATURE_DIR
    / "y_test.csv"
)

TUNED_MODEL_FILE = (
    MODEL_DIR
    / "nrie_stage2_tuned_candidate.json"
)

BASELINE_PREDICTIONS_FILE = (
    MODEL_DIR
    / "test_predictions.csv"
)

OUTPUT_PREDICTIONS_FILE = (
    MODEL_DIR
    / "tuned_test_predictions.csv"
)

CONFUSION_FILE = (
    MODEL_DIR
    / "tuned_confusion_matrix.csv"
)

METRICS_FILE = (
    MODEL_DIR
    / "tuned_evaluation_metrics.json"
)

REPORT_FILE = (
    MODEL_DIR
    / "tuned_evaluation_report.txt"
)

COMPARISON_FILE = (
    MODEL_DIR
    / "baseline_vs_tuned_test.csv"
)


# ============================================================
# CLASS NAMES
# ============================================================

CLASS_NAMES = {
    0: "Fully",
    1: "Partially",
    2: "Abandoned"
}


# ============================================================
# HELPERS
# ============================================================

def check_file(path):

    if not path.exists():

        raise FileNotFoundError(
            f"\nRequired file not found:\n{path}"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)

    print(
        "   REVIANTA AI - TUNED MODEL FINAL EVALUATION"
    )

    print("=" * 70)


    # ========================================================
    # 1. CHECK FILES
    # ========================================================

    print(
        "\nChecking required files..."
    )

    required_files = [
        X_TEST_FILE,
        Y_TEST_FILE,
        TUNED_MODEL_FILE,
        BASELINE_PREDICTIONS_FILE
    ]

    for file in required_files:

        check_file(file)

    print(
        "All required files found."
    )


    # ========================================================
    # 2. LOAD TEST DATA
    # ========================================================

    print(
        "\nLoading untouched TEST data..."
    )

    X_test = load_npz(
        X_TEST_FILE
    )

    y_test = pd.read_csv(
        Y_TEST_FILE
    )["project_outcome"].values


    print(
        f"Test features : {X_test.shape}"
    )

    print(
        f"Test targets  : {y_test.shape}"
    )


    # ========================================================
    # 3. LOAD TUNED MODEL
    # ========================================================

    print(
        "\nLoading tuned candidate..."
    )

    tuned_model = XGBClassifier()

    tuned_model.load_model(
        TUNED_MODEL_FILE
    )

    print(
        "Tuned model loaded successfully."
    )


    # ========================================================
    # 4. PREDICT
    # ========================================================

    print(
        "\nRunning final test prediction..."
    )

    probabilities = tuned_model.predict_proba(
        X_test
    )


    predictions = np.argmax(
        probabilities,
        axis=1
    )


    # ========================================================
    # 5. OVERALL METRICS
    # ========================================================

    accuracy = accuracy_score(
        y_test,
        predictions
    )


    macro_precision = precision_score(
        y_test,
        predictions,
        average="macro",
        zero_division=0
    )


    macro_recall = recall_score(
        y_test,
        predictions,
        average="macro",
        zero_division=0
    )


    macro_f1 = f1_score(
        y_test,
        predictions,
        average="macro",
        zero_division=0
    )


    weighted_precision = precision_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )


    weighted_recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )


    weighted_f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )


    test_logloss = log_loss(
        y_test,
        probabilities,
        labels=[0, 1, 2]
    )


    # ========================================================
    # 6. CLASSIFICATION REPORT
    # ========================================================

    report_text = classification_report(
        y_test,
        predictions,
        labels=[0, 1, 2],
        target_names=[
            "Fully",
            "Partially",
            "Abandoned"
        ],
        zero_division=0
    )


    report_dict = classification_report(
        y_test,
        predictions,
        labels=[0, 1, 2],
        target_names=[
            "Fully",
            "Partially",
            "Abandoned"
        ],
        output_dict=True,
        zero_division=0
    )


    # ========================================================
    # 7. CONFUSION MATRIX
    # ========================================================

    cm = confusion_matrix(
        y_test,
        predictions,
        labels=[0, 1, 2]
    )


    cm_df = pd.DataFrame(
        cm,
        index=[
            "Actual_Fully",
            "Actual_Partially",
            "Actual_Abandoned"
        ],
        columns=[
            "Predicted_Fully",
            "Predicted_Partially",
            "Predicted_Abandoned"
        ]
    )


    # ========================================================
    # 8. ABANDONED METRICS
    # ========================================================

    abandoned_precision = (
        report_dict[
            "Abandoned"
        ]["precision"]
    )

    abandoned_recall = (
        report_dict[
            "Abandoned"
        ]["recall"]
    )

    abandoned_f1 = (
        report_dict[
            "Abandoned"
        ]["f1-score"]
    )


    # ========================================================
    # 9. PRINT RESULTS
    # ========================================================

    print(
        "\n"
        + "=" * 60
    )

    print(
        "FINAL TEST RESULTS - TUNED MODEL"
    )

    print(
        "=" * 60
    )


    print(
        f"\nAccuracy           : "
        f"{accuracy:.4f}"
    )

    print(
        f"Macro Precision    : "
        f"{macro_precision:.4f}"
    )

    print(
        f"Macro Recall       : "
        f"{macro_recall:.4f}"
    )

    print(
        f"Macro F1           : "
        f"{macro_f1:.4f}"
    )

    print(
        f"Weighted Precision : "
        f"{weighted_precision:.4f}"
    )

    print(
        f"Weighted Recall    : "
        f"{weighted_recall:.4f}"
    )

    print(
        f"Weighted F1        : "
        f"{weighted_f1:.4f}"
    )

    print(
        f"Log Loss           : "
        f"{test_logloss:.4f}"
    )


    print(
        "\n"
        + "=" * 60
    )

    print(
        "CLASSIFICATION REPORT"
    )

    print(
        "=" * 60
    )

    print(
        report_text
    )


    print(
        "=" * 60
    )

    print(
        "CONFUSION MATRIX"
    )

    print(
        "=" * 60
    )

    print(
        cm_df.to_string()
    )


    print(
        "\n"
        + "=" * 60
    )

    print(
        "ABANDONED PROJECT DETECTION"
    )

    print(
        "=" * 60
    )

    print(
        f"Precision : "
        f"{abandoned_precision:.4f}"
    )

    print(
        f"Recall    : "
        f"{abandoned_recall:.4f}"
    )

    print(
        f"F1        : "
        f"{abandoned_f1:.4f}"
    )


    # ========================================================
    # 10. LOAD BASELINE PREDICTIONS
    # ========================================================

    print(
        "\nLoading baseline test predictions..."
    )

    baseline_df = pd.read_csv(
        BASELINE_PREDICTIONS_FILE
    )


    if len(baseline_df) != len(y_test):

        raise ValueError(
            "Baseline predictions do not match test size."
        )


    # ========================================================
    # 11. BASELINE VS TUNED
    # ========================================================

    baseline_predictions = []

    for value in baseline_df[
        "predicted_outcome"
    ]:

        if value == "Fully":

            baseline_predictions.append(0)

        elif value == "Partially":

            baseline_predictions.append(1)

        elif value == "Abandoned":

            baseline_predictions.append(2)

        else:

            baseline_predictions.append(
                int(value)
            )


    baseline_predictions = np.array(
        baseline_predictions
    )


    baseline_accuracy = accuracy_score(
        y_test,
        baseline_predictions
    )


    baseline_macro_precision = precision_score(
        y_test,
        baseline_predictions,
        average="macro",
        zero_division=0
    )


    baseline_macro_recall = recall_score(
        y_test,
        baseline_predictions,
        average="macro",
        zero_division=0
    )


    baseline_macro_f1 = f1_score(
        y_test,
        baseline_predictions,
        average="macro",
        zero_division=0
    )


    baseline_abandoned_recall = recall_score(
        y_test,
        baseline_predictions,
        labels=[2],
        average=None,
        zero_division=0
    )[0]


    tuned_abandoned_recall = recall_score(
        y_test,
        predictions,
        labels=[2],
        average=None,
        zero_division=0
    )[0]


    comparison_df = pd.DataFrame(
        [
            {
                "model": "Baseline",
                "accuracy": baseline_accuracy,
                "macro_precision":
                    baseline_macro_precision,
                "macro_recall":
                    baseline_macro_recall,
                "macro_f1":
                    baseline_macro_f1,
                "abandoned_recall":
                    baseline_abandoned_recall
            },
            {
                "model": "Tuned_Depth_5",
                "accuracy": accuracy,
                "macro_precision":
                    macro_precision,
                "macro_recall":
                    macro_recall,
                "macro_f1":
                    macro_f1,
                "abandoned_recall":
                    tuned_abandoned_recall
            }
        ]
    )


    print(
        "\n"
        + "=" * 60
    )

    print(
        "BASELINE VS TUNED - TEST SET"
    )

    print(
        "=" * 60
    )


    print(
        comparison_df
        .round(4)
        .to_string(index=False)
    )


    # ========================================================
    # 12. SAVE PREDICTIONS
    # ========================================================

    predictions_df = pd.DataFrame(
        {
            "actual_outcome": [
                CLASS_NAMES[int(x)]
                for x in y_test
            ],

            "predicted_outcome": [
                CLASS_NAMES[int(x)]
                for x in predictions
            ],

            "probability_fully":
                probabilities[:, 0],

            "probability_partially":
                probabilities[:, 1],

            "probability_abandoned":
                probabilities[:, 2]
        }
    )


    predictions_df.to_csv(
        OUTPUT_PREDICTIONS_FILE,
        index=False
    )


    # ========================================================
    # 13. SAVE CONFUSION MATRIX
    # ========================================================

    cm_df.to_csv(
        CONFUSION_FILE
    )


    # ========================================================
    # 14. SAVE COMPARISON
    # ========================================================

    comparison_df.to_csv(
        COMPARISON_FILE,
        index=False
    )


    # ========================================================
    # 15. SAVE METRICS JSON
    # ========================================================

    metrics = {

        "model":
            "Tuned XGBoost - depth_5",

        "test_size":
            int(len(y_test)),

        "accuracy":
            float(accuracy),

        "macro_precision":
            float(macro_precision),

        "macro_recall":
            float(macro_recall),

        "macro_f1":
            float(macro_f1),

        "weighted_precision":
            float(weighted_precision),

        "weighted_recall":
            float(weighted_recall),

        "weighted_f1":
            float(weighted_f1),

        "log_loss":
            float(test_logloss),

        "abandoned_precision":
            float(abandoned_precision),

        "abandoned_recall":
            float(abandoned_recall),

        "abandoned_f1":
            float(abandoned_f1),

        "baseline_test_accuracy":
            float(baseline_accuracy),

        "baseline_test_macro_f1":
            float(baseline_macro_f1),

        "baseline_test_abandoned_recall":
            float(baseline_abandoned_recall),

        "test_data_used_after_model_selection":
            True
    }


    with open(
        METRICS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            metrics,
            f,
            indent=4
        )


    # ========================================================
    # 16. SAVE REPORT
    # ========================================================

    report_lines = []

    report_lines.append(
        "REVIANTA AI - STAGE 2"
    )

    report_lines.append(
        "TUNED MODEL FINAL TEST EVALUATION"
    )

    report_lines.append(
        "=" * 60
    )

    report_lines.append("")

    report_lines.append(
        "MODEL: Tuned XGBoost - depth_5"
    )

    report_lines.append(
        "MODEL SELECTION: TRAIN + VALIDATION"
    )

    report_lines.append(
        "FINAL EVALUATION: TEST"
    )

    report_lines.append("")

    report_lines.append(
        "TEST PERFORMANCE"
    )

    report_lines.append(
        f"Accuracy: {accuracy:.6f}"
    )

    report_lines.append(
        f"Macro Precision: "
        f"{macro_precision:.6f}"
    )

    report_lines.append(
        f"Macro Recall: "
        f"{macro_recall:.6f}"
    )

    report_lines.append(
        f"Macro F1: "
        f"{macro_f1:.6f}"
    )

    report_lines.append(
        f"Weighted F1: "
        f"{weighted_f1:.6f}"
    )

    report_lines.append(
        f"Log Loss: "
        f"{test_logloss:.6f}"
    )

    report_lines.append("")

    report_lines.append(
        "ABANDONED DETECTION"
    )

    report_lines.append(
        f"Precision: "
        f"{abandoned_precision:.6f}"
    )

    report_lines.append(
        f"Recall: "
        f"{abandoned_recall:.6f}"
    )

    report_lines.append(
        f"F1: "
        f"{abandoned_f1:.6f}"
    )

    report_lines.append("")

    report_lines.append(
        "CLASSIFICATION REPORT"
    )

    report_lines.append(
        report_text
    )

    report_lines.append("")

    report_lines.append(
        "CONFUSION MATRIX"
    )

    report_lines.append(
        cm_df.to_string()
    )

    report_lines.append("")

    report_lines.append(
        "BASELINE VS TUNED"
    )

    report_lines.append(
        comparison_df
        .round(6)
        .to_string(index=False)
    )


    REPORT_FILE.write_text(
        "\n".join(report_lines),
        encoding="utf-8"
    )


    # ========================================================
    # 17. FINAL
    # ========================================================

    print(
        "\n"
        + "=" * 70
    )

    print(
        "      TUNED MODEL TEST EVALUATION COMPLETE"
    )

    print(
        "=" * 70
    )

    print(
        "\nSaved:"
    )

    print(
        f"  {OUTPUT_PREDICTIONS_FILE}"
    )

    print(
        f"  {CONFUSION_FILE}"
    )

    print(
        f"  {COMPARISON_FILE}"
    )

    print(
        f"  {METRICS_FILE}"
    )

    print(
        f"  {REPORT_FILE}"
    )

    print(
        "\nSTATUS: FINAL TEST EVALUATION COMPLETE"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()