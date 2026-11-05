from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = PROJECT_ROOT / "data" / "raw"
INPUT_FILE = DATA_DIR / "original_project_dataset.csv"

REPORT_DIR = PROJECT_ROOT / "data" / "diagnostics"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# IMPORTANT COLUMNS
# ============================================================

TARGET_COLUMN = "Did you complete the project?"

POTENTIAL_LEAKAGE_COLUMNS = [
    "Actual time taken (in months)",
    "Did you publish a paper?",
    "Did you file a patent?",
    "If not fully completed — main reason?",
]

IDENTITY_COLUMNS = [
    "Name",
    "Email",
    "Timestamp",
]

EMPTY_COLUMN_PREFIX = "Unnamed:"


# ============================================================
# HELPERS
# ============================================================

def normalize_column_name(column):
    """Normalize column names for comparison."""
    return (
        str(column)
        .replace("\ufeff", "")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\xa0", " ")
        .strip()
    )


def print_section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def save_text_report(lines):
    report_file = REPORT_DIR / "diagnostic_report.txt"

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return report_file


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"\nDataset not found:\n{INPUT_FILE}\n\n"
            "Place your original CSV inside data/raw/ "
            "and rename it to original_project_dataset.csv"
        )

    print(f"Loading dataset:")
    print(INPUT_FILE)

    df = pd.read_csv(INPUT_FILE)

    # Normalize column names
    df.columns = [normalize_column_name(c) for c in df.columns]

    return df


# ============================================================
# BASIC INFORMATION
# ============================================================

def analyze_basic_info(df, report):

    print_section("1. BASIC DATASET INFORMATION")

    rows, columns = df.shape

    print(f"Rows    : {rows}")
    print(f"Columns : {columns}")

    report.append("BASIC DATASET INFORMATION")
    report.append(f"Rows: {rows}")
    report.append(f"Columns: {columns}")
    report.append("")


# ============================================================
# COLUMN INFORMATION
# ============================================================

def analyze_columns(df, report):

    print_section("2. COLUMNS")

    report.append("COLUMNS")

    for i, column in enumerate(df.columns, start=1):

        dtype = str(df[column].dtype)
        unique = df[column].nunique(dropna=True)
        missing = df[column].isna().sum()

        print(
            f"{i:02d}. {column} "
            f"| dtype={dtype} "
            f"| unique={unique} "
            f"| missing={missing}"
        )

        report.append(
            f"{i:02d}. {column} | dtype={dtype} "
            f"| unique={unique} | missing={missing}"
        )

    report.append("")


# ============================================================
# MISSING VALUES
# ============================================================

def analyze_missing_values(df, report):

    print_section("3. MISSING VALUES")

    missing = df.isna().sum()

    missing = missing[missing > 0].sort_values(ascending=False)

    report.append("MISSING VALUES")

    if missing.empty:

        print("No missing values.")

        report.append("No missing values.")

    else:

        for column, count in missing.items():

            percentage = (count / len(df)) * 100

            print(
                f"{column}: {count} "
                f"({percentage:.2f}%)"
            )

            report.append(
                f"{column}: {count} ({percentage:.2f}%)"
            )

    report.append("")


# ============================================================
# DUPLICATES
# ============================================================

def analyze_duplicates(df, report):

    print_section("4. DUPLICATES")

    exact_duplicates = df.duplicated().sum()

    print(f"Exact duplicate rows: {exact_duplicates}")

    report.append("DUPLICATES")
    report.append(
        f"Exact duplicate rows: {exact_duplicates}"
    )
    report.append("")


# ============================================================
# EMPTY COLUMNS
# ============================================================

def analyze_empty_columns(df, report):

    print_section("5. EMPTY / USELESS COLUMNS")

    report.append("EMPTY COLUMNS")

    empty_columns = []

    for column in df.columns:

        if df[column].isna().all():

            empty_columns.append(column)

    if empty_columns:

        for column in empty_columns:

            print(f"EMPTY: {column}")
            report.append(f"EMPTY: {column}")

    else:

        print("No completely empty columns.")
        report.append("None")

    report.append("")


# ============================================================
# TARGET ANALYSIS
# ============================================================

def analyze_target(df, report):

    print_section("6. TARGET ANALYSIS")

    report.append("TARGET ANALYSIS")

    if TARGET_COLUMN not in df.columns:

        print(
            f"ERROR: Target column not found: "
            f"{TARGET_COLUMN}"
        )

        report.append(
            f"ERROR: Target column not found: "
            f"{TARGET_COLUMN}"
        )

        return

    target = df[TARGET_COLUMN]

    print(f"Target column: {TARGET_COLUMN}")
    print(f"Missing target: {target.isna().sum()}")

    report.append(f"Target: {TARGET_COLUMN}")
    report.append(
        f"Missing target: {target.isna().sum()}"
    )

    print("\nTarget distribution:")

    counts = target.value_counts(dropna=False)

    for value, count in counts.items():

        percentage = (count / len(df)) * 100

        print(
            f"  {value}: {count} "
            f"({percentage:.2f}%)"
        )

        report.append(
            f"  {value}: {count} ({percentage:.2f}%)"
        )

    report.append("")


# ============================================================
# CATEGORICAL VALUE ANALYSIS
# ============================================================

def analyze_categorical_columns(df, report):

    print_section("7. CATEGORICAL VALUE ANALYSIS")

    report.append("CATEGORICAL VALUE ANALYSIS")

    for column in df.columns:

        if df[column].dtype == "object":

            print("\n" + "-" * 60)
            print(column)

            report.append("-" * 60)
            report.append(column)

            values = df[column].value_counts(
                dropna=False
            )

            for value, count in values.head(30).items():

                percentage = (count / len(df)) * 100

                value_text = str(value)

                print(
                    f"  {value_text}: "
                    f"{count} ({percentage:.2f}%)"
                )

                report.append(
                    f"  {value_text}: "
                    f"{count} ({percentage:.2f}%)"
                )

    report.append("")


# ============================================================
# NUMERIC ANALYSIS
# ============================================================

def analyze_numeric_columns(df, report):

    print_section("8. NUMERIC COLUMN ANALYSIS")

    report.append("NUMERIC COLUMN ANALYSIS")

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns

    for column in numeric_columns:

        series = df[column].dropna()

        if series.empty:
            continue

        print("\n" + "-" * 60)
        print(column)

        print(f"  Min    : {series.min()}")
        print(f"  Max    : {series.max()}")
        print(f"  Mean   : {series.mean():.3f}")
        print(f"  Median : {series.median():.3f}")

        report.append("-" * 60)
        report.append(column)
        report.append(f"Min: {series.min()}")
        report.append(f"Max: {series.max()}")
        report.append(f"Mean: {series.mean():.3f}")
        report.append(f"Median: {series.median():.3f}")

    report.append("")


# ============================================================
# POSSIBLE OUTLIERS
# ============================================================

def analyze_outliers(df, report):

    print_section("9. POSSIBLE NUMERIC OUTLIERS")

    report.append("POSSIBLE NUMERIC OUTLIERS")

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns

    for column in numeric_columns:

        series = df[column].dropna()

        if len(series) < 10:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = series[
            (series < lower) |
            (series > upper)
        ]

        if len(outliers) > 0:

            print(
                f"{column}: "
                f"{len(outliers)} possible outliers"
            )

            print(
                f"  Normal range approximately: "
                f"{lower:.2f} to {upper:.2f}"
            )

            report.append(
                f"{column}: {len(outliers)} possible outliers"
            )

            report.append(
                f"  Approx range: "
                f"{lower:.2f} to {upper:.2f}"
            )

    report.append("")


# ============================================================
# LEAKAGE ANALYSIS
# ============================================================

def analyze_leakage(df, report):

    print_section("10. POSSIBLE DATA LEAKAGE")

    report.append("POSSIBLE DATA LEAKAGE")

    for column in POTENTIAL_LEAKAGE_COLUMNS:

        if column in df.columns:

            print(f"POST-OUTCOME / POSSIBLE LEAKAGE: {column}")

            report.append(
                f"POST-OUTCOME / POSSIBLE LEAKAGE: {column}"
            )

    report.append("")


# ============================================================
# IDENTITY ANALYSIS
# ============================================================

def analyze_identity_columns(df, report):

    print_section("11. IDENTITY / PERSONAL COLUMNS")

    report.append("IDENTITY / PERSONAL COLUMNS")

    for column in IDENTITY_COLUMNS:

        if column in df.columns:

            print(f"EXCLUDE FROM ML: {column}")

            report.append(
                f"EXCLUDE FROM ML: {column}"
            )

    report.append("")


# ============================================================
# TEXT COLUMN ANALYSIS
# ============================================================

def analyze_text_columns(df, report):

    print_section("12. TEXT / NLP CANDIDATES")

    report.append("TEXT / NLP CANDIDATES")

    for column in df.columns:

        if df[column].dtype == "object":

            avg_length = (
                df[column]
                .dropna()
                .astype(str)
                .str.len()
                .mean()
            )

            if avg_length > 20:

                print(
                    f"NLP candidate: {column} "
                    f"(average length: {avg_length:.1f})"
                )

                report.append(
                    f"NLP candidate: {column} "
                    f"(average length: {avg_length:.1f})"
                )

    report.append("")


# ============================================================
# SAVE CLEAN COLUMN SUMMARY
# ============================================================

def save_column_summary(df):

    rows = []

    for column in df.columns:

        rows.append({
            "column": column,
            "dtype": str(df[column].dtype),
            "rows": len(df),
            "missing": int(df[column].isna().sum()),
            "missing_percentage":
                round(
                    df[column].isna().mean() * 100,
                    2
                ),
            "unique_values":
                int(df[column].nunique(dropna=True)),
            "completely_empty":
                bool(df[column].isna().all()),
        })

    summary = pd.DataFrame(rows)

    output = REPORT_DIR / "column_summary.csv"

    summary.to_csv(
        output,
        index=False
    )

    return output


# ============================================================
# MAIN
# ============================================================

def main():

    report = []

    print("\n")
    print("=" * 70)
    print("        REVIANTA AI — STAGE 2 DATA DIAGNOSTIC")
    print("=" * 70)

    df = load_data()

    print(f"\nLoaded successfully: {len(df)} records")

    analyze_basic_info(df, report)

    analyze_columns(df, report)

    analyze_missing_values(df, report)

    analyze_duplicates(df, report)

    analyze_empty_columns(df, report)

    analyze_target(df, report)

    analyze_categorical_columns(df, report)

    analyze_numeric_columns(df, report)

    analyze_outliers(df, report)

    analyze_leakage(df, report)

    analyze_identity_columns(df, report)

    analyze_text_columns(df, report)

    summary_file = save_column_summary(df)

    report_file = save_text_report(report)

    print_section("DIAGNOSTIC COMPLETE")

    print(f"Column summary:")
    print(summary_file)

    print(f"\nFull diagnostic report:")
    print(report_file)

    print("\nNo model was trained.")
    print("No records were modified.")
    print("Original dataset remains untouched.")

    print("\nSTATUS: DIAGNOSTIC PASSED")


if __name__ == "__main__":
    main()