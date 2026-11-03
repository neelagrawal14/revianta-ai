"""
============================================================
REVIANTA AI - STAGE 2
MODEL EVALUATION
============================================================

Evaluates the trained XGBoost NRIE Stage 2 model.

IMPORTANT:
    TEST data is used only at this stage.
    The test set was NOT used during training.

Outputs:
    - Accuracy
    - Precision
    - Recall
    - F1-score
    - Classification report
    - Confusion matrix
    - Per-class metrics
    - Predicted probabilities
    - Test predictions
    - Evaluation report
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

X_VAL_FILE = (
    FEATURE_DIR
    / "X_validation.npz"
)

Y_VAL_FILE = (
    FEATURE_DIR
    / "y_validation.csv"
)

X_TEST_FILE = (
    FEATURE_DIR
    / "X_test.npz"
)

Y_TEST_FILE = (
    FEATURE_DIR
    / "y_test.csv"
)

MODEL_FILE = (
    MODEL_DIR
    / "nrie_stage2_xgboost.json"
)

PREDICTIONS_FILE = (
    MODEL_DIR
    / "test_predictions.csv"
)

CONFUSION_FILE = (
    MODEL_DIR
    / "confusion_matrix.csv"
)

REPORT_FILE = (
    MODEL_DIR
    / "evaluation_report.txt"
)

METRICS_FILE = (
    MODEL_DIR
    / "evaluation_metrics.json"
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
# HELPER
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
        "   REVIANTA AI - STAGE 2 MODEL EVALUATION"
    )

    print("=" * 70)


    # ========================================================
    # 1. CHECK FILES
    # ========================================================

    print(
        "\nChecking required files..."
    )

    required_files = [
        MODEL_FILE,
        X_VAL_FILE,
        Y_VAL_FILE,
        X_TEST_FILE,
        Y_TEST_FILE
    ]

    for file in required_files:

        check_file(file)

    print(
        "All required files found."
    )


    # ========================================================
    # 2. LOAD MODEL
    # ========================================================

    print(
        "\nLoading trained XGBoost model..."
    )

    model = XGBClassifier()

    model.load_model(
        MODEL_FILE
    )

    print(
        "Model loaded successfully."
    )


    # ========================================================
    # 3. LOAD VALIDATION DATA
    # ========================================================

    print(
        "\nLoading validation data..."
    )

    X_validation = load_npz(
        X_VAL_FILE
    )

    y_validation = pd.read_csv(
        Y_VAL_FILE
    )["project_outcome"].values


    print(
        f"Validation features : "
        f"{X_validation.shape}"
    )

    print(
        f"Validation targets  : "
        f"{y_validation.shape}"
    )


    # ========================================================
    # 4. LOAD TEST DATA
    # ========================================================

    print(
        "\nLoading TEST data..."
    )

    X_test = load_npz(
        X_TEST_FILE
    )

    y_test = pd.read_csv(
        Y_TEST_FILE
    )["project_outcome"].values


    print(
        f"Test features : "
        f"{X_test.shape}"
    )

    print(
        f"Test targets  : "
        f"{y_test.shape}"
    )


    # ========================================================
    # 5. CHECK DIMENSIONS
    # ========================================================

    if X_validation.shape[1] != X_test.shape[1]:

        raise ValueError(
            "Validation and test feature dimensions differ."
        )


    if X_test.shape[0] != len(y_test):

        raise ValueError(
            "Test feature/target row count mismatch."
        )


    # ========================================================
    # 6. VALIDATION PREDICTIONS
    # ========================================================

    print(
        "\n"
        + "=" * 60
    )

    print(
        "VALIDATION EVALUATION"
    )

    print(
        "=" * 60
    )


    validation_probabilities = (
        model.predict_proba(
            X_validation
        )
    )


    validation_predictions = (
        np.argmax(
            validation_probabilities,
            axis=1
        )
    )


    validation_accuracy = (
        accuracy_score(
            y_validation,
            validation_predictions
        )
    )


    validation_precision = (
        precision_score(
            y_validation,
            validation_predictions,
            average="macro",
            zero_division=0
        )
    )


    validation_recall = (
        recall_score(
            y_validation,
            validation_predictions,
            average="macro",
            zero_division=0
        )
    )


    validation_f1 = (
        f1_score(
            y_validation,
            validation_predictions,
            average="macro",
            zero_division=0
        )
    )


    validation_logloss = (
        log_loss(
            y_validation,
            validation_probabilities,
            labels=[0, 1, 2]
        )
    )


    print(
        f"Accuracy       : "
        f"{validation_accuracy:.4f}"
    )

    print(
        f"Macro Precision: "
        f"{validation_precision:.4f}"
    )

    print(
        f"Macro Recall   : "
        f"{validation_recall:.4f}"
    )

    print(
        f"Macro F1       : "
        f"{validation_f1:.4f}"
    )

    print(
        f"Log Loss       : "
        f"{validation_logloss:.4f}"
    )


    # ========================================================
    # 7. TEST PREDICTIONS
    # ========================================================

    print(
        "\n"
        + "=" * 60
    )

    print(
        "FINAL TEST EVALUATION"
    )

    print(
        "=" * 60
    )


    test_probabilities = (
        model.predict_proba(
            X_test
        )
    )


    test_predictions = (
        np.argmax(
            test_probabilities,
            axis=1
        )
    )


    # ========================================================
    # 8. TEST METRICS
    # ========================================================

    accuracy = accuracy_score(
        y_test,
        test_predictions
    )


    precision_macro = precision_score(
        y_test,
        test_predictions,
        average="macro",
        zero_division=0
    )


    recall_macro = recall_score(
        y_test,
        test_predictions,
        average="macro",
        zero_division=0
    )


    f1_macro = f1_score(
        y_test,
        test_predictions,
        average="macro",
        zero_division=0
    )


    precision_weighted = precision_score(
        y_test,
        test_predictions,
        average="weighted",
        zero_division=0
    )


    recall_weighted = recall_score(
        y_test,
        test_predictions,
        average="weighted",
        zero_division=0
    )


    f1_weighted = f1_score(
        y_test,
        test_predictions,
        average="weighted",
        zero_division=0
    )


    test_logloss = log_loss(
        y_test,
        test_probabilities,
        labels=[0, 1, 2]
    )


    # ========================================================
    # 9. PRINT OVERALL METRICS
    # ========================================================

    print(
        f"\nAccuracy           : "
        f"{accuracy:.4f}"
    )

    print(
        f"Macro Precision    : "
        f"{precision_macro:.4f}"
    )

    print(
        f"Macro Recall       : "
        f"{recall_macro:.4f}"
    )

    print(
        f"Macro F1           : "
        f"{f1_macro:.4f}"
    )

    print(
        f"Weighted Precision : "
        f"{precision_weighted:.4f}"
    )

    print(
        f"Weighted Recall    : "
        f"{recall_weighted:.4f}"
    )

    print(
        f"Weighted F1        : "
        f"{f1_weighted:.4f}"
    )

    print(
        f"Log Loss           : "
        f"{test_logloss:.4f}"
    )


    # ========================================================
    # 10. CLASSIFICATION REPORT
    # ========================================================

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


    report_dict = classification_report(
        y_test,
        test_predictions,
        labels=[0, 1, 2],
        target_names=[
            "Fully",
            "Partially",
            "Abandoned"
        ],
        output_dict=True,
        zero_division=0
    )


    report_text = classification_report(
        y_test,
        test_predictions,
        labels=[0, 1, 2],
        target_names=[
            "Fully",
            "Partially",
            "Abandoned"
        ],
        zero_division=0
    )


    print(
        report_text
    )


    # ========================================================
    # 11. CONFUSION MATRIX
    # ========================================================

    print(
        "=" * 60
    )

    print(
        "CONFUSION MATRIX"
    )

    print(
        "=" * 60
    )


    cm = confusion_matrix(
        y_test,
        test_predictions,
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


    print(
        cm_df.to_string()
    )


    # ========================================================
    # 12. PER-CLASS METRICS
    # ========================================================

    print(
        "\n"
        + "=" * 60
    )

    print(
        "PER-CLASS PERFORMANCE"
    )

    print(
        "=" * 60
    )


    for class_id in [0, 1, 2]:

        class_name = CLASS_NAMES[
            class_id
        ]

        metrics = report_dict[
            class_name
        ]

        print(
            f"\n{class_name}"
        )

        print(
            f"  Precision : "
            f"{metrics['precision']:.4f}"
        )

        print(
            f"  Recall    : "
            f"{metrics['recall']:.4f}"
        )

        print(
            f"  F1-score  : "
            f"{metrics['f1-score']:.4f}"
        )

        print(
            f"  Support   : "
            f"{int(metrics['support'])}"
        )


    # ========================================================
    # 13. ABANDONED CLASS FOCUS
    # ========================================================

    abandoned_metrics = report_dict[
        "Abandoned"
    ]


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
        f"Abandoned Precision : "
        f"{abandoned_metrics['precision']:.4f}"
    )

    print(
        f"Abandoned Recall    : "
        f"{abandoned_metrics['recall']:.4f}"
    )

    print(
        f"Abandoned F1        : "
        f"{abandoned_metrics['f1-score']:.4f}"
    )


    # ========================================================
    # 14. SAVE PREDICTIONS
    # ========================================================

    predictions_df = pd.DataFrame(
        {
            "actual_outcome": [
                CLASS_NAMES[int(x)]
                for x in y_test
            ],

            "predicted_outcome": [
                CLASS_NAMES[int(x)]
                for x in test_predictions
            ],

            "probability_fully":
                test_probabilities[:, 0],

            "probability_partially":
                test_probabilities[:, 1],

            "probability_abandoned":
                test_probabilities[:, 2]
        }
    )


    predictions_df.to_csv(
        PREDICTIONS_FILE,
        index=False
    )


    # ========================================================
    # 15. SAVE CONFUSION MATRIX
    # ========================================================

    cm_df.to_csv(
        CONFUSION_FILE
    )


    # ========================================================
    # 16. SAVE METRICS JSON
    # ========================================================

    metrics_json = {

        "validation": {

            "accuracy":
                float(validation_accuracy),

            "macro_precision":
                float(validation_precision),

            "macro_recall":
                float(validation_recall),

            "macro_f1":
                float(validation_f1),

            "log_loss":
                float(validation_logloss)
        },

        "test": {

            "accuracy":
                float(accuracy),

            "macro_precision":
                float(precision_macro),

            "macro_recall":
                float(recall_macro),

            "macro_f1":
                float(f1_macro),

            "weighted_precision":
                float(precision_weighted),

            "weighted_recall":
                float(recall_weighted),

            "weighted_f1":
                float(f1_weighted),

            "log_loss":
                float(test_logloss)
        },

        "abandoned": {

            "precision":
                float(abandoned_metrics["precision"]),

            "recall":
                float(abandoned_metrics["recall"]),

            "f1":
                float(abandoned_metrics["f1-score"])
        }
    }


    with open(
        METRICS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            metrics_json,
            f,
            indent=4
        )


    # ========================================================
    # 17. SAVE TEXT REPORT
    # ========================================================

    report_lines = []

    report_lines.append(
        "REVIANTA AI - STAGE 2 MODEL EVALUATION"
    )

    report_lines.append(
        "=" * 60
    )

    report_lines.append("")

    report_lines.append(
        "VALIDATION PERFORMANCE"
    )

    report_lines.append(
        f"Accuracy: {validation_accuracy:.6f}"
    )

    report_lines.append(
        f"Macro Precision: {validation_precision:.6f}"
    )

    report_lines.append(
        f"Macro Recall: {validation_recall:.6f}"
    )

    report_lines.append(
        f"Macro F1: {validation_f1:.6f}"
    )

    report_lines.append(
        f"Log Loss: {validation_logloss:.6f}"
    )

    report_lines.append("")

    report_lines.append(
        "FINAL TEST PERFORMANCE"
    )

    report_lines.append(
        f"Accuracy: {accuracy:.6f}"
    )

    report_lines.append(
        f"Macro Precision: {precision_macro:.6f}"
    )

    report_lines.append(
        f"Macro Recall: {recall_macro:.6f}"
    )

    report_lines.append(
        f"Macro F1: {f1_macro:.6f}"
    )

    report_lines.append(
        f"Weighted Precision: {precision_weighted:.6f}"
    )

    report_lines.append(
        f"Weighted Recall: {recall_weighted:.6f}"
    )

    report_lines.append(
        f"Weighted F1: {f1_weighted:.6f}"
    )

    report_lines.append(
        f"Log Loss: {test_logloss:.6f}"
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
        "ABANDONED PROJECT DETECTION"
    )

    report_lines.append(
        f"Precision: "
        f"{abandoned_metrics['precision']:.6f}"
    )

    report_lines.append(
        f"Recall: "
        f"{abandoned_metrics['recall']:.6f}"
    )

    report_lines.append(
        f"F1: "
        f"{abandoned_metrics['f1-score']:.6f}"
    )

    report_lines.append("")

    report_lines.append(
        "TEST DATA WAS NOT USED DURING TRAINING."
    )


    REPORT_FILE.write_text(
        "\n".join(report_lines),
        encoding="utf-8"
    )


    # ========================================================
    # 18. FINAL
    # ========================================================

    print(
        "\n"
        + "=" * 70
    )

    print(
        "       STAGE 2 MODEL EVALUATION COMPLETE"
    )

    print(
        "=" * 70
    )

    print(
        "\nSaved:"
    )

    print(
        f"  {PREDICTIONS_FILE}"
    )

    print(
        f"  {CONFUSION_FILE}"
    )

    print(
        f"  {METRICS_FILE}"
    )

    print(
        f"  {REPORT_FILE}"
    )

    print(
        "\nSTATUS: MODEL EVALUATION COMPLETE"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()