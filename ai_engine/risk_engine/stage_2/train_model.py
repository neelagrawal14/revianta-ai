"""
============================================================
REVIANTA AI - STAGE 2
XGBOOST MODEL TRAINING
============================================================

Input:
    data/stage2/features/X_train.npz
    data/stage2/features/X_validation.npz
    data/stage2/features/y_train.csv
    data/stage2/features/y_validation.csv

Target:
    0 = Fully
    1 = Partially
    2 = Abandoned

Model:
    XGBoost multiclass classifier

Important:
    TEST data is NOT used during training.
============================================================
"""

from pathlib import Path
import json

import numpy as np
import pandas as pd

from scipy.sparse import load_npz

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

X_TRAIN_FILE = FEATURE_DIR / "X_train.npz"
X_VAL_FILE = FEATURE_DIR / "X_validation.npz"

Y_TRAIN_FILE = FEATURE_DIR / "y_train.csv"
Y_VAL_FILE = FEATURE_DIR / "y_validation.csv"

FEATURE_NAMES_FILE = (
    FEATURE_DIR
    / "feature_names.csv"
)

MODEL_FILE = (
    MODEL_DIR
    / "nrie_stage2_xgboost.json"
)

METADATA_FILE = (
    MODEL_DIR
    / "training_metadata.json"
)

IMPORTANCE_FILE = (
    MODEL_DIR
    / "feature_importance.csv"
)


# ============================================================
# CONFIGURATION
# ============================================================

RANDOM_STATE = 42


CLASS_NAMES = {
    0: "Fully",
    1: "Partially",
    2: "Abandoned"
}


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)

    print(
        "   REVIANTA AI - STAGE 2 XGBOOST MODEL TRAINING"
    )

    print("=" * 70)


    # ========================================================
    # 1. CHECK FILES
    # ========================================================

    required_files = [
        X_TRAIN_FILE,
        X_VAL_FILE,
        Y_TRAIN_FILE,
        Y_VAL_FILE,
        FEATURE_NAMES_FILE
    ]

    for file in required_files:

        if not file.exists():

            raise FileNotFoundError(
                f"\nRequired file not found:\n{file}"
            )


    # ========================================================
    # 2. LOAD FEATURES
    # ========================================================

    print("\nLoading feature matrices...")

    X_train = load_npz(
        X_TRAIN_FILE
    )

    X_validation = load_npz(
        X_VAL_FILE
    )


    print(
        f"X_train      : {X_train.shape}"
    )

    print(
        f"X_validation : {X_validation.shape}"
    )


    # ========================================================
    # 3. LOAD TARGETS
    # ========================================================

    y_train = pd.read_csv(
        Y_TRAIN_FILE
    )["project_outcome"].values


    y_validation = pd.read_csv(
        Y_VAL_FILE
    )["project_outcome"].values


    print(
        f"y_train      : {y_train.shape}"
    )

    print(
        f"y_validation : {y_validation.shape}"
    )


    # ========================================================
    # 4. VERIFY DIMENSIONS
    # ========================================================

    if X_train.shape[0] != len(y_train):

        raise ValueError(
            "TRAIN feature/target row count mismatch."
        )


    if X_validation.shape[0] != len(y_validation):

        raise ValueError(
            "VALIDATION feature/target row count mismatch."
        )


    if X_train.shape[1] != X_validation.shape[1]:

        raise ValueError(
            "TRAIN and VALIDATION feature dimensions differ."
        )


    # ========================================================
    # 5. CHECK TARGET CLASSES
    # ========================================================

    print(
        "\nTarget distribution:"
    )

    for dataset_name, y in [
        ("TRAIN", y_train),
        ("VALIDATION", y_validation)
    ]:

        print(
            f"\n{dataset_name}:"
        )

        counts = (
            pd.Series(y)
            .value_counts()
            .sort_index()
        )

        for class_id in [0, 1, 2]:

            print(
                f"  {CLASS_NAMES[class_id]:10}: "
                f"{counts.get(class_id, 0)}"
            )


    # ========================================================
    # 6. CREATE MODEL DIRECTORY
    # ========================================================

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    # ========================================================
    # 7. CREATE XGBOOST MODEL
    # ========================================================

    print(
        "\nCreating XGBoost classifier..."
    )


    model = XGBClassifier(

        objective="multi:softprob",

        num_class=3,

        n_estimators=300,

        learning_rate=0.05,

        max_depth=6,

        min_child_weight=2,

        subsample=0.85,

        colsample_bytree=0.85,

        reg_alpha=0.1,

        reg_lambda=1.0,

        eval_metric="mlogloss",

        tree_method="hist",

        random_state=RANDOM_STATE,

        n_jobs=-1
    )


    # ========================================================
    # 8. TRAIN
    # ========================================================

    print(
        "\n"
        + "=" * 60
    )

    print(
        "TRAINING XGBOOST"
    )

    print(
        "=" * 60
    )


    model.fit(

        X_train,

        y_train,

        eval_set=[
            (
                X_train,
                y_train
            ),
            (
                X_validation,
                y_validation
            )
        ],

        verbose=True
    )


    # ========================================================
    # 9. SAVE MODEL
    # ========================================================

    print(
        "\nSaving model..."
    )


    model.save_model(
        MODEL_FILE
    )


    print(
        f"Model saved:"
    )

    print(
        MODEL_FILE
    )


    # ========================================================
    # 10. FEATURE IMPORTANCE
    # ========================================================

    print(
        "\nGenerating feature importance..."
    )


    feature_names = pd.read_csv(
        FEATURE_NAMES_FILE
    )["feature_name"].tolist()


    importance = model.feature_importances_


    if len(feature_names) != len(importance):

        raise ValueError(
            "Feature name count does not match "
            "model feature count."
        )


    importance_df = pd.DataFrame(
        {
            "feature_name": feature_names,
            "importance": importance
        }
    )


    importance_df = (
        importance_df
        .sort_values(
            "importance",
            ascending=False
        )
        .reset_index(drop=True)
    )


    importance_df[
        "importance_rank"
    ] = range(
        1,
        len(importance_df) + 1
    )


    importance_df.to_csv(
        IMPORTANCE_FILE,
        index=False
    )


    # ========================================================
    # 11. TOP FEATURES
    # ========================================================

    print(
        "\n"
        + "=" * 60
    )

    print(
        "TOP 20 FEATURES"
    )

    print(
        "=" * 60
    )


    top_features = (
        importance_df
        .head(20)
    )


    for _, row in top_features.iterrows():

        print(
            f"{int(row['importance_rank']):2}. "
            f"{row['feature_name']:<50} "
            f"{row['importance']:.6f}"
        )


    # ========================================================
    # 12. TRAINING METADATA
    # ========================================================

    metadata = {

        "model": "XGBClassifier",

        "objective": "multi:softprob",

        "num_classes": 3,

        "classes": CLASS_NAMES,

        "random_state": RANDOM_STATE,

        "n_estimators": 300,

        "learning_rate": 0.05,

        "max_depth": 6,

        "min_child_weight": 2,

        "subsample": 0.85,

        "colsample_bytree": 0.85,

        "reg_alpha": 0.1,

        "reg_lambda": 1.0,

        "tree_method": "hist",

        "train_rows": int(
            X_train.shape[0]
        ),

        "validation_rows": int(
            X_validation.shape[0]
        ),

        "feature_count": int(
            X_train.shape[1]
        ),

        "test_used_during_training": False
    }


    with open(
        METADATA_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4
        )


    # ========================================================
    # 13. FINAL
    # ========================================================

    print(
        "\n"
        + "=" * 70
    )

    print(
        "       STAGE 2 MODEL TRAINING PASSED"
    )

    print(
        "=" * 70
    )

    print(
        f"\nTraining records : "
        f"{X_train.shape[0]}"
    )

    print(
        f"Validation       : "
        f"{X_validation.shape[0]}"
    )

    print(
        f"Features         : "
        f"{X_train.shape[1]}"
    )

    print(
        "\nSaved:"
    )

    print(
        f"  {MODEL_FILE}"
    )

    print(
        f"  {METADATA_FILE}"
    )

    print(
        f"  {IMPORTANCE_FILE}"
    )

    print(
        "\nSTATUS: MODEL READY FOR EVALUATION"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()