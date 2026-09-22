from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "output"

SOURCE_DATASET = OUTPUT_DIR / "source_code_dataset.csv"
HISTORY_DATASET = OUTPUT_DIR / "commit_history_dataset.csv"

COMBINED_DATASET = OUTPUT_DIR / "combined_dataset.csv"


# ---------------------------------------------------------
# Cleaning Functions
# ---------------------------------------------------------

def clean_source_dataset(df):
    """Clean source-code dataset."""

    # Normalize column names
    df.columns = [
        column.strip().lower()
        for column in df.columns
    ]

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Clean text columns
    for column in [
        "repository",
        "file_path",
        "language",
        "extension",
    ]:
        if column in df.columns:
            df[column] = (
                df[column]
                .fillna("")
                .astype(str)
                .str.strip()
            )

    # Normalize path separators
    df["file_path"] = (
        df["file_path"]
        .str.replace("\\", "/", regex=False)
    )

    # Convert numerical fields
    df["loc"] = pd.to_numeric(
        df["loc"],
        errors="coerce"
    )

    df["size_bytes"] = pd.to_numeric(
        df["size_bytes"],
        errors="coerce"
    )

    # Remove invalid records
    df = df[
        (df["repository"] != "") &
        (df["file_path"] != "") &
        (df["loc"].notna()) &
        (df["size_bytes"].notna())
    ]

    # LOC and file size cannot be negative
    df = df[
        (df["loc"] >= 0) &
        (df["size_bytes"] >= 0)
    ]

    # Convert numeric values to integers
    df["loc"] = df["loc"].astype(int)
    df["size_bytes"] = df["size_bytes"].astype(int)

    # Remove duplicate records
    df = df.drop_duplicates(
        subset=["repository", "file_path"],
        keep="first"
    )

    return df


def clean_history_dataset(df):
    """Clean commit-history dataset."""

    # Normalize column names
    df.columns = [
        column.strip().lower()
        for column in df.columns
    ]

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Clean text fields
    df["repository"] = (
        df["repository"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["file_path"] = (
        df["file_path"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.replace("\\", "/", regex=False)
    )

    # Convert change count
    df["change_count"] = pd.to_numeric(
        df["change_count"],
        errors="coerce"
    )

    # Remove invalid records
    df = df[
        (df["repository"] != "") &
        (df["file_path"] != "") &
        (df["change_count"].notna())
    ]

    # Change count cannot be negative
    df = df[
        df["change_count"] >= 0
    ]

    df["change_count"] = (
        df["change_count"]
        .astype(int)
    )

    # If duplicate repository/file combinations exist,
    # aggregate their change counts.
    df = (
        df.groupby(
            ["repository", "file_path"],
            as_index=False
        )["change_count"]
        .sum()
    )

    return df


# ---------------------------------------------------------
# Merge
# ---------------------------------------------------------

def merge_datasets(source_df, history_df):
    """
    Merge source-code and commit-history datasets.

    A LEFT JOIN is used because the source-code dataset
    represents the current repository snapshot.

    Files that have no recorded change in the analyzed
    history receive change_count = 0.
    """

    combined = pd.merge(
        source_df,
        history_df,
        on=["repository", "file_path"],
        how="left"
    )

    # Files with no history record were not present in the
    # analyzed history window.
    combined["change_count"] = (
        combined["change_count"]
        .fillna(0)
        .astype(int)
    )

    # Helpful derived indicator
    combined["history_present"] = (
        combined["change_count"] > 0
    )

    # Arrange columns logically
    combined = combined[
        [
            "repository",
            "file_path",
            "language",
            "extension",
            "loc",
            "size_bytes",
            "change_count",
            "history_present",
        ]
    ]

    return combined


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def clean_and_merge():

    print("=" * 70)
    print("LAB-2 CLEANING AND MERGING")
    print("=" * 70)

    if not SOURCE_DATASET.exists():
        raise FileNotFoundError(
            f"Missing: {SOURCE_DATASET}"
        )

    if not HISTORY_DATASET.exists():
        raise FileNotFoundError(
            f"Missing: {HISTORY_DATASET}"
        )

    # Load
    source_df = pd.read_csv(SOURCE_DATASET)
    history_df = pd.read_csv(HISTORY_DATASET)

    print("\nBefore cleaning:")
    print(f"Source records  : {len(source_df)}")
    print(f"History records : {len(history_df)}")

    # Clean
    source_df = clean_source_dataset(source_df)
    history_df = clean_history_dataset(history_df)

    print("\nAfter cleaning:")
    print(f"Source records  : {len(source_df)}")
    print(f"History records : {len(history_df)}")

    # Merge
    combined_df = merge_datasets(
        source_df,
        history_df
    )

    # Save
    combined_df.to_csv(
        COMBINED_DATASET,
        index=False
    )

    print("\n" + "=" * 70)
    print("MERGE COMPLETED")
    print("=" * 70)

    print(f"\nCombined records : {len(combined_df)}")
    print(f"Output           : {COMBINED_DATASET}")

    return combined_df


if __name__ == "__main__":
    clean_and_merge()