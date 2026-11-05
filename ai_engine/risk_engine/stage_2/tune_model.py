"""
============================================================
REVIANTA AI - STAGE 2
XGBOOST MODEL TUNING
============================================================

Purpose:
    Compare controlled XGBoost configurations and identify
    the strongest Stage 2 NRIE candidate.

IMPORTANT:
    TEST DATA IS NOT USED HERE.

Used:
    TRAIN + VALIDATION

Not used:
    TEST

Primary selection metric:
    Macro F1

Secondary metrics:
    Macro Recall
    Abandoned Recall
    Accuracy
    Log Loss

The final test set will be evaluated only after tuning.
============================================================
"""

from pathlib import Path
import json
import time

import numpy as np
import pandas as pd

from scipy.sparse import load_npz

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
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

X_TRAIN_FILE = (
    FEATURE_DIR
    / "X_train.npz"
)

Y_TRAIN_FILE = (
    FEATURE_DIR
    / "y_train.csv"
)

X_VAL_FILE = (
    FEATURE_DIR
    / "X_validation.npz"
)

Y_VAL_FILE = (
    FEATURE_DIR
    / "y_validation.csv"
)

RESULTS_FILE = (
    MODEL_DIR
    / "tuning_results.csv"
)

REPORT_FILE = (
    MODEL_DIR
    / "tuning_report.txt"
)

BEST_CONFIG_FILE = (
    MODEL_DIR
    / "best_model_config.json"
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


def calculate_metrics(
    y_true,
    probabilities
):

    predictions = np.argmax(
        probabilities,
        axis=1
    )

    accuracy = accuracy_score(
        y_true,
        predictions
    )

    precision = precision_score(
        y_true,
        predictions,
        average="macro",
        zero_division=0
    )

    recall = recall_score(
        y_true,
        predictions,
        average="macro",
        zero_division=0
    )

    f1 = f1_score(
        y_true,
        predictions,
        average="macro",
        zero_division=0
    )

    weighted_f1 = f1_score(
        y_true,
        predictions,
        average="weighted",
        zero_division=0
    )

    abandoned_recall = recall_score(
        y_true,
        predictions,
        labels=[2],
        average=None,
        zero_division=0
    )[0]

    abandoned_precision = precision_score(
        y_true,
        predictions,
        labels=[2],
        average=None,
        zero_division=0
    )[0]

    abandoned_f1 = f1_score(
        y_true,
        predictions,
        labels=[2],
        average=None,
        zero_division=0
    )[0]

    loss = log_loss(
        y_true,
        probabilities,
        labels=[0, 1, 2]
    )

    return {
        "accuracy": accuracy,
        "macro_precision": precision,
        "macro_recall": recall,
        "macro_f1": f1,
        "weighted_f1": weighted_f1,
        "abandoned_precision": abandoned_precision,
        "abandoned_recall": abandoned_recall,
        "abandoned_f1": abandoned_f1,
        "log_loss": loss
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)

    print(
        "        REVIANTA AI - STAGE 2 MODEL TUNING"
    )

    print("=" * 70)


    # ========================================================
    # 1. CHECK FILES
    # ========================================================

    print(
        "\nChecking required files..."
    )

    required_files = [
        X_TRAIN_FILE,
        Y_TRAIN_FILE,
        X_VAL_FILE,
        Y_VAL_FILE
    ]

    for file in required_files:

        check_file(file)

    print(
        "All required files found."
    )


    # ========================================================
    # 2. LOAD TRAINING DATA
    # ========================================================

    print(
        "\nLoading training data..."
    )

    X_train = load_npz(
        X_TRAIN_FILE
    )

    y_train = pd.read_csv(
        Y_TRAIN_FILE
    )["project_outcome"].values


    print(
        f"X_train : {X_train.shape}"
    )

    print(
        f"y_train: {y_train.shape}"
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
        f"X_validation : {X_validation.shape}"
    )

    print(
        f"y_validation : {y_validation.shape}"
    )


    # ========================================================
    # 4. VALIDATE DATA
    # ========================================================

    if X_train.shape[0] != len(y_train):

        raise ValueError(
            "Training feature/target mismatch."
        )


    if X_validation.shape[0] != len(y_validation):

        raise ValueError(
            "Validation feature/target mismatch."
        )


    if X_train.shape[1] != X_validation.shape[1]:

        raise ValueError(
            "Training and validation feature dimensions differ."
        )


    # ========================================================
    # 5. SHOW CLASS DISTRIBUTION
    # ========================================================

    print(
        "\nTraining distribution:"
    )

    train_counts = pd.Series(
        y_train
    ).value_counts().sort_index()


    for class_id, count in train_counts.items():

        print(
            f"  {class_id} - "
            f"{CLASS_NAMES[int(class_id)]}: "
            f"{count}"
        )


    print(
        "\nValidation distribution:"
    )

    val_counts = pd.Series(
        y_validation
    ).value_counts().sort_index()


    for class_id, count in val_counts.items():

        print(
            f"  {class_id} - "
            f"{CLASS_NAMES[int(class_id)]}: "
            f"{count}"
        )


    # ========================================================
    # 6. CONFIGURATIONS
    # ========================================================

    configurations = [

        # ----------------------------------------------------
        # 1. CURRENT BASELINE
        # ----------------------------------------------------

        {
            "name": "baseline",

            "n_estimators": 300,
            "learning_rate": 0.05,
            "max_depth": 6,
            "min_child_weight": 2,

            "subsample": 0.85,
            "colsample_bytree": 0.85,

            "reg_alpha": 0.1,
            "reg_lambda": 1.0,

            "gamma": 0.0
        },


        # ----------------------------------------------------
        # 2. SHALLOW REGULARIZED
        # ----------------------------------------------------

        {
            "name": "shallow_regularized",

            "n_estimators": 400,
            "learning_rate": 0.04,
            "max_depth": 4,
            "min_child_weight": 3,

            "subsample": 0.85,
            "colsample_bytree": 0.80,

            "reg_alpha": 0.2,
            "reg_lambda": 2.0,

            "gamma": 0.05
        },


        # ----------------------------------------------------
        # 3. DEPTH 5
        # ----------------------------------------------------

        {
            "name": "depth_5",

            "n_estimators": 400,
            "learning_rate": 0.04,
            "max_depth": 5,
            "min_child_weight": 2,

            "subsample": 0.85,
            "colsample_bytree": 0.85,

            "reg_alpha": 0.1,
            "reg_lambda": 1.5,

            "gamma": 0.0
        },


        # ----------------------------------------------------
        # 4. STRONGER REGULARIZATION
        # ----------------------------------------------------

        {
            "name": "strong_regularization",

            "n_estimators": 400,
            "learning_rate": 0.04,
            "max_depth": 5,
            "min_child_weight": 4,

            "subsample": 0.80,
            "colsample_bytree": 0.75,

            "reg_alpha": 0.5,
            "reg_lambda": 3.0,

            "gamma": 0.10
        },


        # ----------------------------------------------------
        # 5. LOWER LEARNING RATE
        # ----------------------------------------------------

        {
            "name": "low_learning_rate",

            "n_estimators": 600,
            "learning_rate": 0.025,
            "max_depth": 5,
            "min_child_weight": 2,

            "subsample": 0.85,
            "colsample_bytree": 0.85,

            "reg_alpha": 0.1,
            "reg_lambda": 1.5,

            "gamma": 0.0
        },


        # ----------------------------------------------------
        # 6. BALANCED
        # ----------------------------------------------------

        {
            "name": "balanced",

            "n_estimators": 450,
            "learning_rate": 0.035,
            "max_depth": 5,
            "min_child_weight": 3,

            "subsample": 0.90,
            "colsample_bytree": 0.85,

            "reg_alpha": 0.2,
            "reg_lambda": 2.0,

            "gamma": 0.05
        }

    ]


    # ========================================================
    # 7. TRAIN MODELS
    # ========================================================

    results = []

    best_model = None
    best_config = None
    best_metrics = None

    best_score = -1


    print(
        "\n"
        + "=" * 70
    )

    print(
        "STARTING CONTROLLED MODEL TUNING"
    )

    print(
        "=" * 70
    )


    for index, config in enumerate(
        configurations,
        start=1
    ):

        name = config["name"]


        print(
            "\n"
            + "-" * 60
        )

        print(
            f"MODEL {index}/{len(configurations)}"
        )

        print(
            f"Configuration: {name}"
        )

        print(
            "-" * 60
        )


        start_time = time.time()


        model = XGBClassifier(

            objective="multi:softprob",

            num_class=3,

            n_estimators=config[
                "n_estimators"
            ],

            learning_rate=config[
                "learning_rate"
            ],

            max_depth=config[
                "max_depth"
            ],

            min_child_weight=config[
                "min_child_weight"
            ],

            subsample=config[
                "subsample"
            ],

            colsample_bytree=config[
                "colsample_bytree"
            ],

            reg_alpha=config[
                "reg_alpha"
            ],

            reg_lambda=config[
                "reg_lambda"
            ],

            gamma=config[
                "gamma"
            ],

            eval_metric="mlogloss",

            tree_method="hist",

            random_state=42,

            n_jobs=-1
        )


        print(
            "Training..."
        )


        model.fit(
            X_train,
            y_train,
            eval_set=[
                (
                    X_validation,
                    y_validation
                )
            ],
            verbose=False
        )


        elapsed = (
            time.time()
            - start_time
        )


        # ----------------------------------------------------
        # VALIDATION PREDICTIONS
        # ----------------------------------------------------

        probabilities = (
            model.predict_proba(
                X_validation
            )
        )


        metrics = calculate_metrics(
            y_validation,
            probabilities
        )


        # ----------------------------------------------------
        # PRINT RESULTS
        # ----------------------------------------------------

        print(
            f"\nAccuracy           : "
            f"{metrics['accuracy']:.4f}"
        )

        print(
            f"Macro Precision    : "
            f"{metrics['macro_precision']:.4f}"
        )

        print(
            f"Macro Recall       : "
            f"{metrics['macro_recall']:.4f}"
        )

        print(
            f"Macro F1           : "
            f"{metrics['macro_f1']:.4f}"
        )

        print(
            f"Weighted F1        : "
            f"{metrics['weighted_f1']:.4f}"
        )

        print(
            f"Abandoned Recall   : "
            f"{metrics['abandoned_recall']:.4f}"
        )

        print(
            f"Abandoned F1      : "
            f"{metrics['abandoned_f1']:.4f}"
        )

        print(
            f"Log Loss           : "
            f"{metrics['log_loss']:.4f}"
        )

        print(
            f"Training Time      : "
            f"{elapsed:.2f} seconds"
        )


        # ----------------------------------------------------
        # STORE RESULTS
        # ----------------------------------------------------

        result = {

            "configuration": name,

            "accuracy":
                metrics["accuracy"],

            "macro_precision":
                metrics["macro_precision"],

            "macro_recall":
                metrics["macro_recall"],

            "macro_f1":
                metrics["macro_f1"],

            "weighted_f1":
                metrics["weighted_f1"],

            "abandoned_precision":
                metrics["abandoned_precision"],

            "abandoned_recall":
                metrics["abandoned_recall"],

            "abandoned_f1":
                metrics["abandoned_f1"],

            "log_loss":
                metrics["log_loss"],

            "training_time_seconds":
                elapsed,

            **{
                key: value
                for key, value in config.items()
                if key != "name"
            }
        }


        results.append(
            result
        )


        # ----------------------------------------------------
        # BEST MODEL
        # ----------------------------------------------------

        current_score = (
            metrics["macro_f1"]
        )


        if current_score > best_score:

            best_score = (
                current_score
            )

            best_model = model

            best_config = config.copy()

            best_metrics = metrics.copy()


            print(
                "\n*** CURRENT BEST MODEL ***"
            )


    # ========================================================
    # 8. RESULTS TABLE
    # ========================================================

    results_df = pd.DataFrame(
        results
    )


    results_df = results_df.sort_values(
        by="macro_f1",
        ascending=False
    )


    print(
        "\n"
        + "=" * 70
    )

    print(
        "MODEL COMPARISON"
    )

    print(
        "=" * 70
    )


    display_columns = [
        "configuration",
        "accuracy",
        "macro_precision",
        "macro_recall",
        "macro_f1",
        "weighted_f1",
        "abandoned_recall",
        "abandoned_f1",
        "log_loss"
    ]


    print(
        results_df[
            display_columns
        ]
        .round(4)
        .to_string(index=False)
    )


    # ========================================================
    # 9. SAVE RESULTS
    # ========================================================

    results_df.to_csv(
        RESULTS_FILE,
        index=False
    )


    # ========================================================
    # 10. BEST MODEL INFORMATION
    # ========================================================

    print(
        "\n"
        + "=" * 70
    )

    print(
        "BEST CONFIGURATION"
    )

    print(
        "=" * 70
    )


    print(
        f"\nConfiguration:"
        f" {best_config['name']}"
    )


    print(
        f"Macro F1:"
        f" {best_metrics['macro_f1']:.4f}"
    )


    print(
        f"Accuracy:"
        f" {best_metrics['accuracy']:.4f}"
    )


    print(
        f"Macro Recall:"
        f" {best_metrics['macro_recall']:.4f}"
    )


    print(
        f"Abandoned Recall:"
        f" {best_metrics['abandoned_recall']:.4f}"
    )


    print(
        f"Abandoned F1:"
        f" {best_metrics['abandoned_f1']:.4f}"
    )


    print(
        f"Log Loss:"
        f" {best_metrics['log_loss']:.4f}"
    )


    # ========================================================
    # 11. SAVE BEST CONFIG
    # ========================================================

    best_config_output = {

        "selection_metric":
            "validation_macro_f1",

        "best_configuration":
            best_config,

        "validation_metrics":
            {
                key: float(value)
                for key, value
                in best_metrics.items()
            },

        "test_used":
            False,

        "note":
            "Best model selected using TRAIN and VALIDATION only. "
            "TEST data remains untouched."
    }


    with open(
        BEST_CONFIG_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            best_config_output,
            f,
            indent=4
        )


    # ========================================================
    # 12. SAVE BEST MODEL
    # ========================================================

    BEST_MODEL_FILE = (
        MODEL_DIR
        / "nrie_stage2_tuned_candidate.json"
    )


    best_model.save_model(
        BEST_MODEL_FILE
    )


    # ========================================================
    # 13. CREATE REPORT
    # ========================================================

    report = []

    report.append(
        "REVIANTA AI - STAGE 2 MODEL TUNING REPORT"
    )

    report.append(
        "=" * 60
    )

    report.append("")

    report.append(
        "DATA POLICY"
    )

    report.append(
        "TRAIN data used: YES"
    )

    report.append(
        "VALIDATION data used: YES"
    )

    report.append(
        "TEST data used: NO"
    )

    report.append("")

    report.append(
        "MODEL SELECTION"
    )

    report.append(
        "Primary metric: Validation Macro F1"
    )

    report.append(
        f"Best configuration: "
        f"{best_config['name']}"
    )

    report.append("")

    report.append(
        "BEST VALIDATION PERFORMANCE"
    )

    report.append(
        f"Accuracy: "
        f"{best_metrics['accuracy']:.6f}"
    )

    report.append(
        f"Macro Precision: "
        f"{best_metrics['macro_precision']:.6f}"
    )

    report.append(
        f"Macro Recall: "
        f"{best_metrics['macro_recall']:.6f}"
    )

    report.append(
        f"Macro F1: "
        f"{best_metrics['macro_f1']:.6f}"
    )

    report.append(
        f"Weighted F1: "
        f"{best_metrics['weighted_f1']:.6f}"
    )

    report.append(
        f"Abandoned Precision: "
        f"{best_metrics['abandoned_precision']:.6f}"
    )

    report.append(
        f"Abandoned Recall: "
        f"{best_metrics['abandoned_recall']:.6f}"
    )

    report.append(
        f"Abandoned F1: "
        f"{best_metrics['abandoned_f1']:.6f}"
    )

    report.append(
        f"Log Loss: "
        f"{best_metrics['log_loss']:.6f}"
    )

    report.append("")

    report.append(
        "MODEL COMPARISON"
    )

    report.append(
        results_df[
            display_columns
        ]
        .round(6)
        .to_string(index=False)
    )

    report.append("")

    report.append(
        "BEST MODEL SAVED TO:"
    )

    report.append(
        str(BEST_MODEL_FILE)
    )

    report.append("")

    report.append(
        "TEST DATA REMAINS UNTOUCHED."
    )


    REPORT_FILE.write_text(
        "\n".join(report),
        encoding="utf-8"
    )


    # ========================================================
    # 14. FINAL
    # ========================================================

    print(
        "\n"
        + "=" * 70
    )

    print(
        "          MODEL TUNING COMPLETE"
    )

    print(
        "=" * 70
    )


    print(
        "\nSaved:"
    )

    print(
        f"  {RESULTS_FILE}"
    )

    print(
        f"  {BEST_CONFIG_FILE}"
    )

    print(
        f"  {BEST_MODEL_FILE}"
    )

    print(
        f"  {REPORT_FILE}"
    )


    print(
        "\nSTATUS: TUNING COMPLETE"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()