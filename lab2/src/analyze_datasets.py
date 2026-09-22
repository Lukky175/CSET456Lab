from pathlib import Path
import json
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
# JSON Utility
# ---------------------------------------------------------

def save_json(data, path):
    """Save dictionary as formatted JSON."""

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


# ---------------------------------------------------------
# Source-Code Statistics
# ---------------------------------------------------------

def source_code_statistics(df):

    statistics = {
        "dataset": "source_code_dataset",
        "total_records": int(len(df)),
        "repositories": int(df["repository"].nunique()),
        "source_files": int(df["file_path"].nunique()),
        "languages": (
            df["language"]
            .value_counts()
            .to_dict()
        ),
        "extensions": (
            df["extension"]
            .value_counts()
            .to_dict()
        ),
        "total_loc": int(df["loc"].sum()),
        "average_loc": round(
            float(df["loc"].mean()),
            2
        ),
        "maximum_loc": int(
            df["loc"].max()
        ),
        "minimum_loc": int(
            df["loc"].min()
        ),
        "total_size_bytes": int(
            df["size_bytes"].sum()
        ),
        "average_size_bytes": round(
            float(df["size_bytes"].mean()),
            2
        ),
        "records_per_repository": (
            df["repository"]
            .value_counts()
            .to_dict()
        ),
    }

    return statistics


# ---------------------------------------------------------
# Commit-History Statistics
# ---------------------------------------------------------

def commit_history_statistics(df):

    statistics = {
        "dataset": "commit_history_dataset",
        "total_records": int(len(df)),
        "repositories": int(df["repository"].nunique()),
        "unique_files": int(
            df["file_path"].nunique()
        ),
        "total_change_events": int(
            df["change_count"].sum()
        ),
        "average_change_count": round(
            float(df["change_count"].mean()),
            2
        ),
        "maximum_change_count": int(
            df["change_count"].max()
        ),
        "minimum_change_count": int(
            df["change_count"].min()
        ),
        "records_per_repository": (
            df["repository"]
            .value_counts()
            .to_dict()
        ),
        "changes_per_repository": (
            df.groupby("repository")["change_count"]
            .sum()
            .astype(int)
            .to_dict()
        ),
    }

    return statistics


# ---------------------------------------------------------
# Combined Dataset Statistics
# ---------------------------------------------------------

def combined_statistics(df):

    frequently_changed = (
        df.sort_values(
            "change_count",
            ascending=False
        )
        [
            [
                "repository",
                "file_path",
                "change_count",
            ]
        ]
        .head(10)
        .to_dict(orient="records")
    )

    largest_files = (
        df.sort_values(
            "loc",
            ascending=False
        )
        [
            [
                "repository",
                "file_path",
                "loc",
            ]
        ]
        .head(10)
        .to_dict(orient="records")
    )

    statistics = {
        "dataset": "combined_dataset",
        "total_records": int(len(df)),
        "repositories": int(
            df["repository"].nunique()
        ),
        "total_loc": int(
            df["loc"].sum()
        ),
        "average_loc": round(
            float(df["loc"].mean()),
            2
        ),
        "total_size_bytes": int(
            df["size_bytes"].sum()
        ),
        "average_size_bytes": round(
            float(df["size_bytes"].mean()),
            2
        ),
        "total_change_count": int(
            df["change_count"].sum()
        ),
        "average_change_count": round(
            float(df["change_count"].mean()),
            2
        ),
        "files_with_history": int(
            df["history_present"].sum()
        ),
        "files_without_history": int(
            (~df["history_present"]).sum()
        ),
        "languages": (
            df["language"]
            .value_counts()
            .to_dict()
        ),
        "records_per_repository": (
            df["repository"]
            .value_counts()
            .to_dict()
        ),
        "top_frequently_changed_files": frequently_changed,
        "largest_files_by_loc": largest_files,
    }

    return statistics


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def analyze_datasets():

    print("=" * 70)
    print("LAB-2 DATASET ANALYSIS")
    print("=" * 70)

    # -----------------------------------------------------
    # Load datasets
    # -----------------------------------------------------

    source_df = pd.read_csv(
        SOURCE_DATASET
    )

    history_df = pd.read_csv(
        HISTORY_DATASET
    )

    combined_df = pd.read_csv(
        COMBINED_DATASET
    )

    # -----------------------------------------------------
    # Generate statistics
    # -----------------------------------------------------

    source_stats = source_code_statistics(
        source_df
    )

    history_stats = commit_history_statistics(
        history_df
    )

    combined_stats = combined_statistics(
        combined_df
    )

    # -----------------------------------------------------
    # Output paths
    # -----------------------------------------------------

    source_output = (
        OUTPUT_DIR /
        "source_code_statistics.json"
    )

    history_output = (
        OUTPUT_DIR /
        "commit_history_statistics.json"
    )

    combined_output = (
        OUTPUT_DIR /
        "combined_dataset_statistics.json"
    )

    # -----------------------------------------------------
    # Save JSON
    # -----------------------------------------------------

    save_json(
        source_stats,
        source_output
    )

    save_json(
        history_stats,
        history_output
    )

    save_json(
        combined_stats,
        combined_output
    )

    # -----------------------------------------------------
    # Display summary
    # -----------------------------------------------------

    print("\nStatistics generated successfully.")

    print("\nSource-Code Dataset")
    print(
        f"  Records      : {source_stats['total_records']}"
    )
    print(
        f"  Repositories  : {source_stats['repositories']}"
    )
    print(
        f"  Total LOC     : {source_stats['total_loc']}"
    )

    print("\nCommit-History Dataset")
    print(
        f"  Records       : {history_stats['total_records']}"
    )
    print(
        f"  Repositories  : {history_stats['repositories']}"
    )
    print(
        f"  Change Events : {history_stats['total_change_events']}"
    )

    print("\nCombined Dataset")
    print(
        f"  Records       : {combined_stats['total_records']}"
    )
    print(
        f"  Repositories  : {combined_stats['repositories']}"
    )
    print(
        f"  Total LOC     : {combined_stats['total_loc']}"
    )
    print(
        f"  Total Changes : {combined_stats['total_change_count']}"
    )

    print("\nOutput files:")
    print(f"  {source_output}")
    print(f"  {history_output}")
    print(f"  {combined_output}")


if __name__ == "__main__":
    analyze_datasets()