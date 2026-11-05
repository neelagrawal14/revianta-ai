"""
============================================================
REVIANTA AI - STAGE 2
DATASET V1 PREPARATION
============================================================

Purpose:
1. Load original project dataset
2. Remove completely empty columns
3. Detect the real target column
4. Remove missing/invalid target rows
5. Remove identity columns
6. Remove target leakage columns
7. Clean numeric columns
8. Clean categorical/text columns
9. Encode target
10. Validate dataset
11. Save Dataset V1

IMPORTANT:
- No synthetic data
- No oversampling
- No duplication
- No class balancing here
- Balancing happens AFTER train/validation/test split
- Training will later be balanced to 725/class
============================================================
"""

from pathlib import Path

import pandas as pd
import numpy as np


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[3]

RAW_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "original_project_dataset.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "stage2"
)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "dataset_v1.csv"
)

REPORT_FILE = (
    OUTPUT_DIR
    / "dataset_v1_report.txt"
)


# ============================================================
# REAL CSV COLUMN NAMES
# ============================================================

TARGET_COLUMN = "Did you complete the project?"


# ============================================================
# IDENTITY COLUMNS
# ============================================================

IDENTITY_COLUMNS = [
    "Timestamp",
    "Name",
    "Email",
]


# ============================================================
# DATA LEAKAGE COLUMNS
# ============================================================

# These columns contain information that is known only
# after / because of the project outcome.

LEAKAGE_COLUMNS = [
    "Actual time taken (in months)",
    "Did you publish a paper?",
    "Did you file a patent?",
    "If not fully completed — main reason?",
]


# ============================================================
# NUMERIC COLUMNS
# ============================================================

NUMERIC_COLUMNS = [
    "Team size",
    "Planned timeline (in months)",
    "Rate the technical difficulty at the start",
]


# ============================================================
# TARGET MAPPING
# ============================================================

TARGET_MAPPING = {
    "Fully": 0,
    "Partially": 1,
    "Abandoned": 2,
}


# ============================================================
# COLUMN NORMALIZATION
# ============================================================

def normalize_column_names(df):
    """
    Normalize whitespace/BOM in column names without
    changing the actual wording.
    """

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace("\ufeff", "", regex=False)
        .str.replace(r"\s+", " ", regex=True)
    )

    return df


# ============================================================
# FIND TARGET COLUMN
# ============================================================

def find_target_column(df):
    """
    Find the target column using case-insensitive matching.
    """

    target_normalized = (
        TARGET_COLUMN
        .strip()
        .lower()
    )

    for column in df.columns:

        if column.strip().lower() == target_normalized:

            return column

    raise ValueError(
        "\nTarget column not found.\n\n"
        f"Expected:\n"
        f"  {TARGET_COLUMN}\n\n"
        "Available columns:\n"
        +
        "\n".join(
            f"  - {column}"
            for column in df.columns
        )
    )


# ============================================================
# CLEAN TEXT COLUMN
# ============================================================

def clean_text_column(series):
    """
    Clean text/categorical values.
    """

    series = (
        series
        .astype("string")
        .str.strip()
    )

    series = series.replace(
        {
            "": pd.NA,
            "nan": pd.NA,
            "NaN": pd.NA,
            "None": pd.NA,
            "none": pd.NA,
        }
    )

    return series.fillna("Unknown")


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("       REVIANTA AI - STAGE 2 DATASET PREPARATION")
    print("=" * 70)


    # ========================================================
    # 1. CHECK RAW DATASET
    # ========================================================

    if not RAW_FILE.exists():

        raise FileNotFoundError(
            "\nRaw dataset not found:\n"
            f"{RAW_FILE}\n\n"
            "Expected location:\n"
            "data/raw/original_project_dataset.csv"
        )


    # ========================================================
    # 2. LOAD DATASET
    # ========================================================

    print("\nLoading raw dataset...")

    df = pd.read_csv(
        RAW_FILE,
        low_memory=False
    )

    original_rows = len(df)
    original_columns = len(df.columns)

    print(
        f"Raw records : {original_rows}"
    )

    print(
        f"Raw columns : {original_columns}"
    )


    # ========================================================
    # 3. NORMALIZE COLUMN NAMES
    # ========================================================

    df = normalize_column_names(df)


    # ========================================================
    # 4. REMOVE COMPLETELY EMPTY COLUMNS
    # ========================================================

    empty_columns = [
        column
        for column in df.columns
        if df[column].isna().all()
    ]

    if empty_columns:

        df = df.drop(
            columns=empty_columns
        )

        print(
            f"Removed empty columns: "
            f"{len(empty_columns)}"
        )

        for column in empty_columns:

            print(
                f"  - {column}"
            )

    else:

        print(
            "Removed empty columns: 0"
        )


    # ========================================================
    # 5. FIND TARGET
    # ========================================================

    target_column = find_target_column(df)

    print(
        f"\nTarget column detected:"
    )

    print(
        f"  {target_column}"
    )


    # ========================================================
    # 6. CLEAN TARGET
    # ========================================================

    df[target_column] = (
        df[target_column]
        .astype("string")
        .str.strip()
    )


    # ========================================================
    # 7. SHOW RAW TARGET DISTRIBUTION
    # ========================================================

    print(
        "\nRaw target distribution:"
    )

    print(
        df[target_column]
        .value_counts(
            dropna=False
        )
        .to_string()
    )


    # ========================================================
    # 8. REMOVE MISSING TARGET
    # ========================================================

    missing_target = (
        df[target_column]
        .isna()
        .sum()
    )

    print(
        f"\nMissing target records: "
        f"{missing_target}"
    )

    if missing_target > 0:

        df = df.dropna(
            subset=[
                target_column
            ]
        )


    # ========================================================
    # 9. REMOVE INVALID TARGET VALUES
    # ========================================================

    valid_targets = set(
        TARGET_MAPPING.keys()
    )

    invalid_target_mask = (
        ~df[target_column].isin(
            valid_targets
        )
    )

    invalid_target_count = (
        invalid_target_mask.sum()
    )

    print(
        f"Invalid target records: "
        f"{invalid_target_count}"
    )

    if invalid_target_count > 0:

        print(
            "\nInvalid target values:"
        )

        print(
            df.loc[
                invalid_target_mask,
                target_column
            ]
            .value_counts()
            .to_string()
        )

        df = df.loc[
            ~invalid_target_mask
        ].copy()


    # ========================================================
    # 10. REMOVE IDENTITY COLUMNS
    # ========================================================

    identity_to_remove = [
        column
        for column in IDENTITY_COLUMNS
        if column in df.columns
    ]

    if identity_to_remove:

        df = df.drop(
            columns=identity_to_remove
        )

        print(
            "\nRemoved identity columns:"
        )

        for column in identity_to_remove:

            print(
                f"  - {column}"
            )

    else:

        print(
            "\nRemoved identity columns: 0"
        )


    # ========================================================
    # 11. REMOVE LEAKAGE COLUMNS
    # ========================================================

    leakage_to_remove = [
        column
        for column in LEAKAGE_COLUMNS
        if column in df.columns
    ]

    if leakage_to_remove:

        df = df.drop(
            columns=leakage_to_remove
        )

        print(
            "\nRemoved leakage columns:"
        )

        for column in leakage_to_remove:

            print(
                f"  - {column}"
            )

    else:

        print(
            "\nRemoved leakage columns: 0"
        )


    # ========================================================
    # 12. CLEAN NUMERIC COLUMNS
    # ========================================================

    print(
        "\nCleaning numeric columns..."
    )

    numeric_invalid_records = set()

    for column in NUMERIC_COLUMNS:

        if column not in df.columns:

            print(
                f"  WARNING: numeric column "
                f"not found: {column}"
            )

            continue


        # Convert to numeric
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


    # ========================================================
    # 13. TEAM SIZE CLEANING
    # ========================================================

    if "Team size" in df.columns:

        invalid_team = (
            (df["Team size"] < 1)
            |
            (df["Team size"] > 20)
        )

        invalid_count = (
            invalid_team.sum()
        )

        print(
            f"Invalid team-size values: "
            f"{invalid_count}"
        )

        df.loc[
            invalid_team,
            "Team size"
        ] = np.nan


    # ========================================================
    # 14. PLANNED TIMELINE CLEANING
    # ========================================================

    if "Planned timeline (in months)" in df.columns:

        invalid_timeline = (
            (
                df[
                    "Planned timeline (in months)"
                ] < 0.5
            )
            |
            (
                df[
                    "Planned timeline (in months)"
                ] > 60
            )
        )

        invalid_count = (
            invalid_timeline.sum()
        )

        print(
            f"Invalid timeline values: "
            f"{invalid_count}"
        )

        df.loc[
            invalid_timeline,
            "Planned timeline (in months)"
        ] = np.nan


    # ========================================================
    # 15. TECHNICAL DIFFICULTY CLEANING
    # ========================================================

    difficulty_column = (
        "Rate the technical difficulty at the start"
    )

    if difficulty_column in df.columns:

        invalid_difficulty = (
            (
                df[
                    difficulty_column
                ] < 1
            )
            |
            (
                df[
                    difficulty_column
                ] > 5
            )
        )

        invalid_count = (
            invalid_difficulty.sum()
        )

        print(
            f"Invalid difficulty values: "
            f"{invalid_count}"
        )

        df.loc[
            invalid_difficulty,
            difficulty_column
        ] = np.nan


    # ========================================================
    # 16. FILL NUMERIC MISSING VALUES
    # ========================================================

    print(
        "\nFilling numeric missing values..."
    )

    for column in NUMERIC_COLUMNS:

        if column not in df.columns:
            continue

        median_value = (
            df[column]
            .median()
        )

        df[column] = (
            df[column]
            .fillna(median_value)
        )


    # ========================================================
    # 17. FIND TEXT/CATEGORICAL COLUMNS
    # ========================================================

    text_columns = []

    for column in df.columns:

        if column == target_column:
            continue

        if (
            pd.api.types.is_string_dtype(
                df[column]
            )
            or
            pd.api.types.is_object_dtype(
                df[column]
            )
        ):

            text_columns.append(
                column
            )


    print(
        "\nText/categorical columns:"
    )

    for column in text_columns:

        print(
            f"  - {column}"
        )


    # ========================================================
    # 18. CLEAN TEXT/CATEGORICAL COLUMNS
    # ========================================================

    for column in text_columns:

        df[column] = clean_text_column(
            df[column]
        )


    # ========================================================
    # 19. ENCODE TARGET
    # ========================================================

    print(
        "\nEncoding target..."
    )

    df[target_column] = (
        df[target_column]
        .map(TARGET_MAPPING)
    )


    # ========================================================
    # 20. VALIDATE TARGET ENCODING
    # ========================================================

    if df[target_column].isna().any():

        raise ValueError(
            "\nTarget encoding produced "
            "missing values."
        )


    df[target_column] = (
        df[target_column]
        .astype(int)
    )


    # ========================================================
    # 21. REMOVE DUPLICATES
    # ========================================================

    duplicate_count = (
        df.duplicated().sum()
    )

    print(
        f"\nDuplicate rows: "
        f"{duplicate_count}"
    )

    if duplicate_count > 0:

        df = (
            df
            .drop_duplicates()
            .reset_index(drop=True)
        )

        print(
            f"Removed duplicate rows: "
            f"{duplicate_count}"
        )


    # ========================================================
    # 22. RESET INDEX
    # ========================================================

    df = (
        df
        .reset_index(drop=True)
    )


    # ========================================================
    # 23. FINAL VALIDATION
    # ========================================================

    print(
        "\nRunning final validation..."
    )


    # Dataset cannot be empty
    if df.empty:

        raise ValueError(
            "Dataset became empty."
        )


    # Target must exist
    if target_column not in df.columns:

        raise ValueError(
            "Target column missing "
            "after preprocessing."
        )


    # Target cannot contain NaN
    if df[target_column].isna().any():

        raise ValueError(
            "Target contains missing values."
        )


    # Target must contain only 0,1,2
    valid_encoded_targets = {
        0,
        1,
        2
    }

    actual_targets = set(
        df[target_column].unique()
    )

    if not actual_targets.issubset(
        valid_encoded_targets
    ):

        raise ValueError(
            "Invalid encoded target values: "
            f"{actual_targets}"
        )


    # Numeric columns cannot contain NaN
    for column in NUMERIC_COLUMNS:

        if column not in df.columns:
            continue

        if df[column].isna().any():

            raise ValueError(
                f"Missing values remain in "
                f"numeric column: {column}"
            )


    # ========================================================
    # 24. FINAL CLASS DISTRIBUTION
    # ========================================================

    class_names = {
        0: "Fully",
        1: "Partially",
        2: "Abandoned"
    }

    class_counts = (
        df[target_column]
        .value_counts()
        .sort_index()
    )


    # ========================================================
    # 25. CREATE OUTPUT DIRECTORY
    # ========================================================

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    # ========================================================
    # 26. SAVE DATASET V1
    # ========================================================

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )


    # ========================================================
    # 27. GENERATE REPORT
    # ========================================================

    final_rows = len(df)

    final_columns = len(df.columns)

    removed_records = (
        original_rows
        - final_rows
    )


    report_lines = []


    report_lines.append(
        "REVIANTA AI - STAGE 2 DATASET V1"
    )

    report_lines.append(
        "=" * 60
    )

    report_lines.append(
        f"Original records : {original_rows}"
    )

    report_lines.append(
        f"Final records    : {final_rows}"
    )

    report_lines.append(
        f"Removed records  : {removed_records}"
    )

    report_lines.append(
        f"Final columns    : {final_columns}"
    )

    report_lines.append("")


    report_lines.append(
        "Target distribution:"
    )


    for class_id in [
        0,
        1,
        2
    ]:

        count = class_counts.get(
            class_id,
            0
        )

        percentage = (
            count
            / final_rows
            * 100
        )

        report_lines.append(
            f"{class_id} - "
            f"{class_names[class_id]:10} "
            f"{count:5} "
            f"({percentage:.2f}%)"
        )


    report_lines.append("")


    report_lines.append(
        "Target mapping:"
    )

    report_lines.append(
        "Fully = 0"
    )

    report_lines.append(
        "Partially = 1"
    )

    report_lines.append(
        "Abandoned = 2"
    )


    report_lines.append("")


    report_lines.append(
        "Identity columns removed:"
    )

    for column in identity_to_remove:

        report_lines.append(
            f"- {column}"
        )


    if not identity_to_remove:

        report_lines.append(
            "- None"
        )


    report_lines.append("")


    report_lines.append(
        "Leakage columns removed:"
    )

    for column in leakage_to_remove:

        report_lines.append(
            f"- {column}"
        )


    if not leakage_to_remove:

        report_lines.append(
            "- None"
        )


    report_lines.append("")


    report_lines.append(
        "Empty columns removed:"
    )

    for column in empty_columns:

        report_lines.append(
            f"- {column}"
        )


    if not empty_columns:

        report_lines.append(
            "- None"
        )


    report_lines.append("")


    report_lines.append(
        "Dataset policy:"
    )

    report_lines.append(
        "- No synthetic data"
    )

    report_lines.append(
        "- No oversampling"
    )

    report_lines.append(
        "- No duplicated records"
    )

    report_lines.append(
        "- Dataset V1 remains naturally imbalanced"
    )

    report_lines.append(
        "- Train/validation/test split comes next"
    )

    report_lines.append(
        "- Only TRAIN will be balanced"
    )

    report_lines.append(
        "- Training target: 725 records per class"
    )


    REPORT_FILE.write_text(
        "\n".join(report_lines),
        encoding="utf-8"
    )


    # ========================================================
    # 28. FINAL CONSOLE OUTPUT
    # ========================================================

    print("\n")

    print("=" * 70)

    print(
        "                 FINAL DATASET V1"
    )

    print("=" * 70)


    print(
        f"\nOriginal records : "
        f"{original_rows}"
    )

    print(
        f"Final records    : "
        f"{final_rows}"
    )

    print(
        f"Removed records  : "
        f"{removed_records}"
    )

    print(
        f"Final columns    : "
        f"{final_columns}"
    )


    print(
        "\nTarget distribution:"
    )


    for class_id in [
        0,
        1,
        2
    ]:

        count = class_counts.get(
            class_id,
            0
        )

        percentage = (
            count
            / final_rows
            * 100
        )

        print(
            f"  {class_id} - "
            f"{class_names[class_id]:10} "
            f"{count:5} "
            f"({percentage:.2f}%)"
        )


    print(
        "\nValidation"
    )

    print(
        "-" * 50
    )

    print(
        "All validation checks passed."
    )


    print(
        "\nSaved Dataset V1:"
    )

    print(
        OUTPUT_FILE
    )


    print(
        "\nSaved report:"
    )

    print(
        REPORT_FILE
    )


    print(
        "\nSTATUS: DATASET V1 READY"
    )


    print(
        "\nNext Stage:"
    )

    print(
        "1. Stratified train/validation/test split"
    )

    print(
        "2. Balance TRAIN ONLY"
    )

    print(
        "3. Use exactly 725 real records per class"
    )

    print(
        "4. No synthetic data"
    )

    print(
        "5. No duplicated records"
    )


    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()