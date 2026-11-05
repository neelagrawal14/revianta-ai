"""
============================================================
REVIANTA AI - STAGE 2
FEATURE ENGINEERING
============================================================

INPUT:
    data/stage2/train.csv
    data/stage2/validation.csv
    data/stage2/test.csv

TARGET:
    project_outcome

OUTPUT:
    data/stage2/features/
        X_train.npz
        X_validation.npz
        X_test.npz

        y_train.csv
        y_validation.csv
        y_test.csv

        feature_names.csv
        feature_engineering_report.txt

IMPORTANT:
    Feature transformers are FIT ONLY on TRAIN.
    Validation and TEST are transformed using the
    TRAIN-fitted transformers.

This prevents data leakage.
============================================================
"""

from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd

from scipy.sparse import csr_matrix, hstack, save_npz

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[3]

DATA_DIR = BASE_DIR / "data" / "stage2"

TRAIN_FILE = DATA_DIR / "train.csv"
VALIDATION_FILE = DATA_DIR / "validation.csv"
TEST_FILE = DATA_DIR / "test.csv"

OUTPUT_DIR = DATA_DIR / "features"

X_TRAIN_FILE = OUTPUT_DIR / "X_train.npz"
X_VAL_FILE = OUTPUT_DIR / "X_validation.npz"
X_TEST_FILE = OUTPUT_DIR / "X_test.npz"

Y_TRAIN_FILE = OUTPUT_DIR / "y_train.csv"
Y_VAL_FILE = OUTPUT_DIR / "y_validation.csv"
Y_TEST_FILE = OUTPUT_DIR / "y_test.csv"

FEATURE_NAMES_FILE = OUTPUT_DIR / "feature_names.csv"

REPORT_FILE = OUTPUT_DIR / "feature_engineering_report.txt"

ARTIFACT_FILE = OUTPUT_DIR / "feature_transformers.joblib"


# ============================================================
# CONFIGURATION
# ============================================================

TARGET = "project_outcome"

TEXT_COLUMNS = [
    "project_title",
    "technologies_used"
]

CATEGORICAL_COLUMNS = [
    "dataset_availability",
    "hardware_required",
    "similar_project_awareness",
    "research_availability"
]

NUMERIC_COLUMNS = [
    "team_size",
    "planned_timeline_months",
    "technical_difficulty"
]


CLASS_NAMES = {
    0: "Fully",
    1: "Partially",
    2: "Abandoned"
}


RANDOM_STATE = 42


# ============================================================
# HELPER
# ============================================================

def clean_text(series):

    return (
        series
        .fillna("")
        .astype(str)
        .str.strip()
    )


# ============================================================
# LOAD DATA
# ============================================================

def load_dataset(path, name):

    if not path.exists():

        raise FileNotFoundError(
            f"\n{name} dataset not found:\n{path}"
        )

    df = pd.read_csv(path)

    print(
        f"{name:<12}: "
        f"{len(df)} rows, "
        f"{len(df.columns)} columns"
    )

    return df


# ============================================================
# CHECK COLUMNS
# ============================================================

def validate_columns(df, name):

    required = (
        TEXT_COLUMNS
        + CATEGORICAL_COLUMNS
        + NUMERIC_COLUMNS
        + [TARGET]
    )

    missing = [
        column
        for column in required
        if column not in df.columns
    ]

    if missing:

        raise ValueError(
            f"\n{name} is missing columns:\n"
            + "\n".join(
                f"  - {column}"
                for column in missing
            )
        )


# ============================================================
# PREPARE DATA
# ============================================================

def prepare_dataframe(df):

    df = df.copy()

    # --------------------------------------------------------
    # Target
    # --------------------------------------------------------

    df[TARGET] = pd.to_numeric(
        df[TARGET],
        errors="coerce"
    )

    if df[TARGET].isna().any():

        raise ValueError(
            "Missing or invalid target values found."
        )

    df[TARGET] = df[TARGET].astype(int)


    # --------------------------------------------------------
    # Text
    # --------------------------------------------------------

    for column in TEXT_COLUMNS:

        df[column] = clean_text(
            df[column]
        )


    # --------------------------------------------------------
    # Categorical
    # --------------------------------------------------------

    for column in CATEGORICAL_COLUMNS:

        df[column] = (
            df[column]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

        df.loc[
            df[column] == "",
            column
        ] = "Unknown"


    # --------------------------------------------------------
    # Numeric
    # --------------------------------------------------------

    for column in NUMERIC_COLUMNS:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


    return df


# ============================================================
# ADD TEXT FEATURES
# ============================================================

def build_combined_text(df):

    """
    Combines project title and technology information
    into one textual representation.

    Example:

    Project:
        AI based pothole detection

    Technologies:
        Python, YOLO, OpenCV

    Becomes:

        AI based pothole detection
        Python YOLO OpenCV
    """

    title = clean_text(
        df["project_title"]
    )

    technologies = clean_text(
        df["technologies_used"]
    )

    combined = (
        title
        + " "
        + technologies
    )

    return combined


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)

    print(
        "   REVIANTA AI - STAGE 2 FEATURE ENGINEERING"
    )

    print("=" * 70)


    # ========================================================
    # 1. LOAD DATA
    # ========================================================

    print("\nLoading datasets...")

    train = load_dataset(
        TRAIN_FILE,
        "TRAIN"
    )

    validation = load_dataset(
        VALIDATION_FILE,
        "VALIDATION"
    )

    test = load_dataset(
        TEST_FILE,
        "TEST"
    )


    # ========================================================
    # 2. VALIDATE
    # ========================================================

    print("\nValidating columns...")

    validate_columns(
        train,
        "TRAIN"
    )

    validate_columns(
        validation,
        "VALIDATION"
    )

    validate_columns(
        test,
        "TEST"
    )

    print(
        "Column validation passed."
    )


    # ========================================================
    # 3. PREPARE
    # ========================================================

    train = prepare_dataframe(
        train
    )

    validation = prepare_dataframe(
        validation
    )

    test = prepare_dataframe(
        test
    )


    # ========================================================
    # 4. TARGET
    # ========================================================

    y_train = train[TARGET].values
    y_validation = validation[TARGET].values
    y_test = test[TARGET].values


    # ========================================================
    # 5. BUILD TEXT
    # ========================================================

    print(
        "\nBuilding text representations..."
    )

    train_text = build_combined_text(
        train
    )

    validation_text = build_combined_text(
        validation
    )

    test_text = build_combined_text(
        test
    )


    # ========================================================
    # 6. TF-IDF
    # ========================================================

    print(
        "\nFitting TF-IDF on TRAIN only..."
    )

    tfidf = TfidfVectorizer(
        lowercase=True,
        strip_accents="unicode",
        ngram_range=(1, 2),
        min_df=2,
        max_features=1000,
        sublinear_tf=True
    )


    X_train_text = tfidf.fit_transform(
        train_text
    )


    X_validation_text = tfidf.transform(
        validation_text
    )


    X_test_text = tfidf.transform(
        test_text
    )


    print(
        f"TF-IDF features: "
        f"{X_train_text.shape[1]}"
    )


    # ========================================================
    # 7. CATEGORICAL FEATURES
    # ========================================================

    print(
        "\nFitting categorical encoder on TRAIN only..."
    )

    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=True
    )


    X_train_cat = encoder.fit_transform(
        train[CATEGORICAL_COLUMNS]
    )


    X_validation_cat = encoder.transform(
        validation[CATEGORICAL_COLUMNS]
    )


    X_test_cat = encoder.transform(
        test[CATEGORICAL_COLUMNS]
    )


    print(
        f"Categorical features: "
        f"{X_train_cat.shape[1]}"
    )


    # ========================================================
    # 8. NUMERIC FEATURES
    # ========================================================

    print(
        "\nFitting numeric scaler on TRAIN only..."
    )

    scaler = StandardScaler()


    X_train_num = scaler.fit_transform(
        train[NUMERIC_COLUMNS]
    )


    X_validation_num = scaler.transform(
        validation[NUMERIC_COLUMNS]
    )


    X_test_num = scaler.transform(
        test[NUMERIC_COLUMNS]
    )


    # Convert to sparse matrices

    X_train_num = csr_matrix(
        X_train_num
    )

    X_validation_num = csr_matrix(
        X_validation_num
    )

    X_test_num = csr_matrix(
        X_test_num
    )


    print(
        f"Numeric features: "
        f"{X_train_num.shape[1]}"
    )


    # ========================================================
    # 9. COMBINE FEATURES
    # ========================================================

    print(
        "\nCombining feature groups..."
    )


    X_train = hstack(
        [
            X_train_text,
            X_train_cat,
            X_train_num
        ],
        format="csr"
    )


    X_validation = hstack(
        [
            X_validation_text,
            X_validation_cat,
            X_validation_num
        ],
        format="csr"
    )


    X_test = hstack(
        [
            X_test_text,
            X_test_cat,
            X_test_num
        ],
        format="csr"
    )


    # ========================================================
    # 10. FEATURE COUNT
    # ========================================================

    feature_count = X_train.shape[1]

    print(
        f"\nTotal ML features: "
        f"{feature_count}"
    )


    # ========================================================
    # 11. FEATURE NAMES
    # ========================================================

    print(
        "\nGenerating feature names..."
    )


    text_feature_names = [
        f"text__{name}"
        for name in tfidf.get_feature_names_out()
    ]


    categorical_feature_names = [
        f"categorical__{name}"
        for name in encoder.get_feature_names_out(
            CATEGORICAL_COLUMNS
        )
    ]


    numeric_feature_names = [
        f"numeric__{name}"
        for name in NUMERIC_COLUMNS
    ]


    feature_names = (
        text_feature_names
        + categorical_feature_names
        + numeric_feature_names
    )


    if len(feature_names) != feature_count:

        raise ValueError(
            "\nFeature name count does not match "
            "feature matrix dimension.\n"
            f"Names: {len(feature_names)}\n"
            f"Matrix: {feature_count}"
        )


    # ========================================================
    # 12. CREATE OUTPUT DIRECTORY
    # ========================================================

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    # ========================================================
    # 13. SAVE FEATURE MATRICES
    # ========================================================

    print(
        "\nSaving feature matrices..."
    )


    save_npz(
        X_TRAIN_FILE,
        X_train
    )

    save_npz(
        X_VAL_FILE,
        X_validation
    )

    save_npz(
        X_TEST_FILE,
        X_test
    )


    # ========================================================
    # 14. SAVE TARGETS
    # ========================================================

    pd.DataFrame(
        {
            TARGET: y_train
        }
    ).to_csv(
        Y_TRAIN_FILE,
        index=False
    )


    pd.DataFrame(
        {
            TARGET: y_validation
        }
    ).to_csv(
        Y_VAL_FILE,
        index=False
    )


    pd.DataFrame(
        {
            TARGET: y_test
        }
    ).to_csv(
        Y_TEST_FILE,
        index=False
    )


    # ========================================================
    # 15. SAVE FEATURE NAMES
    # ========================================================

    pd.DataFrame(
        {
            "feature_index": range(
                len(feature_names)
            ),
            "feature_name": feature_names
        }
    ).to_csv(
        FEATURE_NAMES_FILE,
        index=False
    )


    # ========================================================
    # 16. SAVE TRANSFORMERS
    # ========================================================

    joblib.dump(
        {
            "tfidf": tfidf,
            "encoder": encoder,
            "scaler": scaler,
            "text_columns": TEXT_COLUMNS,
            "categorical_columns": CATEGORICAL_COLUMNS,
            "numeric_columns": NUMERIC_COLUMNS,
            "target": TARGET
        },
        ARTIFACT_FILE
    )


    # ========================================================
    # 17. VERIFY MATRIX SHAPES
    # ========================================================

    print(
        "\n"
        + "=" * 60
    )

    print(
        "FEATURE MATRIX VERIFICATION"
    )

    print(
        "=" * 60
    )


    print(
        f"X_train      : "
        f"{X_train.shape}"
    )

    print(
        f"X_validation : "
        f"{X_validation.shape}"
    )

    print(
        f"X_test       : "
        f"{X_test.shape}"
    )


    if (
        X_train.shape[1]
        != X_validation.shape[1]
        or
        X_train.shape[1]
        != X_test.shape[1]
    ):

        raise ValueError(
            "Feature dimensions do not match."
        )


    # ========================================================
    # 18. VERIFY TARGET DISTRIBUTIONS
    # ========================================================

    print(
        "\nTARGET DISTRIBUTIONS"
    )


    for name, values in [
        ("TRAIN", y_train),
        ("VALIDATION", y_validation),
        ("TEST", y_test)
    ]:

        counts = pd.Series(
            values
        ).value_counts().sort_index()

        print(
            f"\n{name}:"
        )

        for class_id in [0, 1, 2]:

            print(
                f"  {CLASS_NAMES[class_id]:10}: "
                f"{counts.get(class_id, 0)}"
            )


    # ========================================================
    # 19. CHECK NaN / INFINITE VALUES
    # ========================================================

    print(
        "\nChecking numerical matrix integrity..."
    )


    for name, matrix in [
        ("TRAIN", X_train),
        ("VALIDATION", X_validation),
        ("TEST", X_test)
    ]:

        data = matrix.data

        if not np.isfinite(data).all():

            raise ValueError(
                f"{name} contains NaN or infinite values."
            )


    print(
        "Matrix integrity passed."
    )


    # ========================================================
    # 20. REPORT
    # ========================================================

    report = []

    report.append(
        "REVIANTA AI - STAGE 2 FEATURE ENGINEERING REPORT"
    )

    report.append(
        "=" * 60
    )

    report.append(
        ""
    )

    report.append(
        "FEATURE GROUPS"
    )

    report.append(
        f"TF-IDF features: {len(text_feature_names)}"
    )

    report.append(
        f"Categorical features: "
        f"{len(categorical_feature_names)}"
    )

    report.append(
        f"Numeric features: "
        f"{len(numeric_feature_names)}"
    )

    report.append(
        f"Total features: {feature_count}"
    )

    report.append(
        ""
    )

    report.append(
        "DATASET SHAPES"
    )

    report.append(
        f"TRAIN: {X_train.shape}"
    )

    report.append(
        f"VALIDATION: {X_validation.shape}"
    )

    report.append(
        f"TEST: {X_test.shape}"
    )

    report.append(
        ""
    )

    report.append(
        "FEATURE ENGINEERING POLICY"
    )

    report.append(
        "TF-IDF fitted on TRAIN only."
    )

    report.append(
        "Categorical encoder fitted on TRAIN only."
    )

    report.append(
        "Numeric scaler fitted on TRAIN only."
    )

    report.append(
        "Validation transformed using TRAIN-fitted transformers."
    )

    report.append(
        "Test transformed using TRAIN-fitted transformers."
    )

    report.append(
        "Target project_outcome excluded from input features."
    )

    report.append(
        ""
    )

    report.append(
        "STATUS: FEATURE ENGINEERING PASSED"
    )


    REPORT_FILE.write_text(
        "\n".join(report),
        encoding="utf-8"
    )


    # ========================================================
    # 21. FINAL
    # ========================================================

    print(
        "\n"
        + "=" * 70
    )

    print(
        "       STAGE 2 FEATURE ENGINEERING PASSED"
    )

    print(
        "=" * 70
    )

    print(
        f"\nTotal features : {feature_count}"
    )

    print(
        f"TRAIN          : {X_train.shape}"
    )

    print(
        f"VALIDATION     : {X_validation.shape}"
    )

    print(
        f"TEST           : {X_test.shape}"
    )

    print(
        "\nSaved:"
    )

    print(
        f"  {X_TRAIN_FILE}"
    )

    print(
        f"  {X_VAL_FILE}"
    )

    print(
        f"  {X_TEST_FILE}"
    )

    print(
        f"  {Y_TRAIN_FILE}"
    )

    print(
        f"  {Y_VAL_FILE}"
    )

    print(
        f"  {Y_TEST_FILE}"
    )

    print(
        f"  {FEATURE_NAMES_FILE}"
    )

    print(
        f"  {ARTIFACT_FILE}"
    )

    print(
        f"  {REPORT_FILE}"
    )

    print(
        "\nSTATUS: READY FOR MODEL TRAINING"
    )

    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()