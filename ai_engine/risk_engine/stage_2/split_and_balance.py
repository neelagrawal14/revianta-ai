from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split


# ============================================================
# REVIANTA AI - STAGE 2
# STRATIFIED SPLIT + TRAINING BALANCING
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[3]

INPUT_FILE = BASE_DIR / "data" / "stage2" / "dataset_v1.csv"
OUTPUT_DIR = BASE_DIR / "data" / "stage2"

TRAIN_FILE = OUTPUT_DIR / "train.csv"
VAL_FILE = OUTPUT_DIR / "validation.csv"
TEST_FILE = OUTPUT_DIR / "test.csv"
REPORT_FILE = OUTPUT_DIR / "split_report.txt"

TARGET = "project_outcome"

RANDOM_STATE = 42

TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15


CLASS_NAMES = {
    0: "Fully",
    1: "Partially",
    2: "Abandoned"
}


# ============================================================
# DISPLAY DISTRIBUTION
# ============================================================

def show_distribution(df, name):

    print(f"\n{name} distribution:")

    counts = (
        df[TARGET]
        .value_counts()
        .sort_index()
    )

    for class_id in [0, 1, 2]:

        count = counts.get(class_id, 0)

        print(
            f"  {class_id} - "
            f"{CLASS_NAMES[class_id]:10} "
            f"{count}"
        )

    return counts


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print(
        "   REVIANTA AI - STAGE 2 "
        "STRATIFIED SPLIT + TRAIN BALANCING"
    )
    print("=" * 70)


    # ========================================================
    # 1. LOAD DATA
    # ========================================================

    print("\nLoading Dataset V1...")

    if not INPUT_FILE.exists():

        raise FileNotFoundError(
            f"\nDataset not found:\n{INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    print(
        f"Dataset V1 records : {len(df)}"
    )

    print(
        f"Dataset V1 columns : {len(df.columns)}"
    )


    # ========================================================
    # 2. CHECK TARGET
    # ========================================================

    if TARGET not in df.columns:

        raise ValueError(
            f"\nTarget column '{TARGET}' not found.\n\n"
            "Available columns:\n"
            + "\n".join(
                f"  - {c}"
                for c in df.columns
            )
        )


    # ========================================================
    # 3. CLEAN TARGET
    # ========================================================

    df = df.dropna(
        subset=[TARGET]
    ).copy()

    df[TARGET] = pd.to_numeric(
        df[TARGET],
        errors="coerce"
    )

    df = df.dropna(
        subset=[TARGET]
    ).copy()

    df[TARGET] = df[TARGET].astype(int)


    # ========================================================
    # 4. CHECK CLASSES
    # ========================================================

    expected_classes = {0, 1, 2}

    actual_classes = set(
        df[TARGET].unique()
    )

    if actual_classes != expected_classes:

        raise ValueError(
            "\nUnexpected target classes.\n"
            f"Expected: {expected_classes}\n"
            f"Found: {actual_classes}"
        )


    # ========================================================
    # 5. DATASET V1 DISTRIBUTION
    # ========================================================

    print("\n" + "=" * 60)
    print("DATASET V1 DISTRIBUTION")
    print("=" * 60)

    original_counts = show_distribution(
        df,
        "Dataset V1"
    )


    # ========================================================
    # 6. REMOVE ML-IDENTICAL DUPLICATES
    #
    # These are duplicates AFTER identity/leakage columns
    # were removed during Dataset V1 preparation.
    #
    # Keep the first occurrence.
    # ========================================================

    duplicate_count = df.duplicated().sum()

    print(
        f"\nML-identical duplicate rows found : "
        f"{duplicate_count}"
    )

    if duplicate_count > 0:

        df = (
            df
            .drop_duplicates()
            .reset_index(drop=True)
        )

        print(
            f"Removed duplicate rows            : "
            f"{duplicate_count}"
        )

        print(
            f"Records remaining                  : "
            f"{len(df)}"
        )


    # ========================================================
    # 7. STRATIFIED TRAIN / TEMP SPLIT
    # ========================================================

    print("\n" + "=" * 60)
    print("STRATIFIED SPLIT")
    print("=" * 60)

    train, temp = train_test_split(
        df,
        test_size=(1 - TRAIN_RATIO),
        random_state=RANDOM_STATE,
        stratify=df[TARGET]
    )


    # ========================================================
    # 8. TEMP -> VALIDATION / TEST
    # ========================================================

    # temp is 30% of dataset.
    #
    # We divide temp equally:
    #
    # validation = 15%
    # test       = 15%

    validation, test = train_test_split(
        temp,
        test_size=0.50,
        random_state=RANDOM_STATE,
        stratify=temp[TARGET]
    )


    # ========================================================
    # 9. SHOW RAW TRAIN DISTRIBUTION
    # ========================================================

    print("\nRAW TRAIN BEFORE BALANCING")

    train_counts_before = show_distribution(
        train,
        "TRAIN"
    )


    # ========================================================
    # 10. BALANCE TRAIN ONLY
    #
    # We use undersampling.
    #
    # Smallest class determines training size.
    # ========================================================

    minimum_class_count = min(
        train_counts_before.get(0, 0),
        train_counts_before.get(1, 0),
        train_counts_before.get(2, 0)
    )

    print(
        f"\nSmallest TRAIN class : "
        f"{minimum_class_count}"
    )

    print(
        "\nBalancing TRAIN using "
        "random undersampling..."
    )


    balanced_parts = []

    for class_id in [0, 1, 2]:

        class_data = train[
            train[TARGET] == class_id
        ].copy()

        balanced_class = (
            class_data
            .sample(
                n=minimum_class_count,
                random_state=RANDOM_STATE
            )
        )

        balanced_parts.append(
            balanced_class
        )


    train_balanced = (
        pd.concat(
            balanced_parts,
            ignore_index=True
        )
        .sample(
            frac=1.0,
            random_state=RANDOM_STATE
        )
        .reset_index(drop=True)
    )


    # ========================================================
    # 11. FINAL TRAIN DISTRIBUTION
    # ========================================================

    print("\n" + "=" * 60)
    print("FINAL BALANCED TRAIN DISTRIBUTION")
    print("=" * 60)

    train_counts = show_distribution(
        train_balanced,
        "TRAIN"
    )


    # ========================================================
    # 12. VALIDATION DISTRIBUTION
    # ========================================================

    print("\n" + "=" * 60)
    print("VALIDATION DISTRIBUTION")
    print("=" * 60)

    validation_counts = show_distribution(
        validation,
        "VALIDATION"
    )


    # ========================================================
    # 13. TEST DISTRIBUTION
    # ========================================================

    print("\n" + "=" * 60)
    print("TEST DISTRIBUTION")
    print("=" * 60)

    test_counts = show_distribution(
        test,
        "TEST"
    )


    # ========================================================
    # 14. VERIFY ALL CLASSES EXIST
    # ========================================================

    for dataset_name, dataset in [
        ("TRAIN", train_balanced),
        ("VALIDATION", validation),
        ("TEST", test)
    ]:

        classes = set(
            dataset[TARGET].unique()
        )

        if classes != {0, 1, 2}:

            raise ValueError(
                f"\n{dataset_name} does not contain "
                f"all three classes.\n"
                f"Found: {classes}"
            )


    # ========================================================
    # 15. VERIFY TRAIN BALANCE
    # ========================================================

    train_values = (
        train_balanced[TARGET]
        .value_counts()
    )

    if len(
        set(train_values.tolist())
    ) != 1:

        raise ValueError(
            "\nTRAIN is not balanced."
        )


    # ========================================================
    # 16. CHECK DUPLICATES
    # ========================================================

    print("\n" + "=" * 60)
    print("DATA INTEGRITY CHECK")
    print("=" * 60)

    train_dup = train_balanced.duplicated().sum()
    val_dup = validation.duplicated().sum()
    test_dup = test.duplicated().sum()

    print(
        f"TRAIN duplicates      : {train_dup}"
    )

    print(
        f"VALIDATION duplicates : {val_dup}"
    )

    print(
        f"TEST duplicates       : {test_dup}"
    )


    # ========================================================
    # 17. CROSS-SPLIT OVERLAP
    # ========================================================

    def row_keys(data):

        return set(
            map(
                tuple,
                data.astype(str).values
            )
        )


    train_keys = row_keys(
        train_balanced
    )

    val_keys = row_keys(
        validation
    )

    test_keys = row_keys(
        test
    )


    train_val_overlap = (
        train_keys & val_keys
    )

    train_test_overlap = (
        train_keys & test_keys
    )

    val_test_overlap = (
        val_keys & test_keys
    )


    print(
        f"TRAIN/VALIDATION overlap : "
        f"{len(train_val_overlap)}"
    )

    print(
        f"TRAIN/TEST overlap       : "
        f"{len(train_test_overlap)}"
    )

    print(
        f"VALIDATION/TEST overlap  : "
        f"{len(val_test_overlap)}"
    )


    if (
        train_val_overlap
        or train_test_overlap
        or val_test_overlap
    ):

        raise ValueError(
            "\nCross-split data leakage detected."
        )


    # ========================================================
    # 18. SAVE DATASETS
    # ========================================================

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    train_balanced.to_csv(
        TRAIN_FILE,
        index=False
    )

    validation.to_csv(
        VAL_FILE,
        index=False
    )

    test.to_csv(
        TEST_FILE,
        index=False
    )


    # ========================================================
    # 19. SAVE REPORT
    # ========================================================

    report = []

    report.append(
        "REVIANTA AI - STAGE 2 SPLIT REPORT"
    )

    report.append("=" * 60)

    report.append(
        f"Dataset V1 records: {len(df)}"
    )

    report.append(
        f"Target: {TARGET}"
    )

    report.append(
        f"Random state: {RANDOM_STATE}"
    )

    report.append("")

    report.append(
        "TRAIN"
    )

    for class_id in [0, 1, 2]:

        report.append(
            f"{CLASS_NAMES[class_id]}: "
            f"{train_counts.get(class_id, 0)}"
        )

    report.append(
        f"Total: {len(train_balanced)}"
    )

    report.append("")

    report.append(
        "VALIDATION"
    )

    for class_id in [0, 1, 2]:

        report.append(
            f"{CLASS_NAMES[class_id]}: "
            f"{validation_counts.get(class_id, 0)}"
        )

    report.append(
        f"Total: {len(validation)}"
    )

    report.append("")

    report.append(
        "TEST"
    )

    for class_id in [0, 1, 2]:

        report.append(
            f"{CLASS_NAMES[class_id]}: "
            f"{test_counts.get(class_id, 0)}"
        )

    report.append(
        f"Total: {len(test)}"
    )

    report.append("")

    report.append(
        "DATA INTEGRITY"
    )

    report.append(
        f"ML-identical duplicates removed: "
        f"{duplicate_count}"
    )

    report.append(
        "Training balanced using undersampling."
    )

    report.append(
        "Validation and test were not balanced."
    )

    report.append(
        "All three classes present in all splits."
    )

    report.append(
        "No cross-split overlap."
    )


    REPORT_FILE.write_text(
        "\n".join(report),
        encoding="utf-8"
    )


    # ========================================================
    # 20. FINAL SUCCESS
    # ========================================================

    print("\n" + "=" * 70)
    print(
        "              STAGE 2 SPLIT PASSED"
    )
    print("=" * 70)

    print(
        f"\nTRAIN       : {len(train_balanced)} records"
    )

    print(
        f"VALIDATION  : {len(validation)} records"
    )

    print(
        f"TEST        : {len(test)} records"
    )

    print(
        f"\nSaved:"
    )

    print(
        f"  {TRAIN_FILE}"
    )

    print(
        f"  {VAL_FILE}"
    )

    print(
        f"  {TEST_FILE}"
    )

    print(
        f"  {REPORT_FILE}"
    )

    print(
        "\nSTATUS: DATA SPLIT READY FOR FEATURE ENGINEERING"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()