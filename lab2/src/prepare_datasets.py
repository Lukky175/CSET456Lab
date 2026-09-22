from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_DIR = BASE_DIR / "data" / "input"
OUTPUT_DIR = BASE_DIR / "output"


# Repositories required by Lab-2
REPOSITORIES = [
    "flask",
    "requests",
    "pytest",
    "fastapi",
    "scikit-learn",
]


# ---------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------

def clean_repository_name(name):
    """Return a normalized repository name."""
    return name.strip().lower()


def load_repository_data(repository):
    """
    Load the two Lab-1 CSV files for one repository.

    Returns:
        source_df
        history_df
    """

    repository_dir = INPUT_DIR / repository

    file_metrics_path = repository_dir / "file_metrics.csv"
    history_metrics_path = repository_dir / "git_history_metrics.csv"

    if not file_metrics_path.exists():
        raise FileNotFoundError(
            f"Missing file_metrics.csv for repository: {repository}"
        )

    if not history_metrics_path.exists():
        raise FileNotFoundError(
            f"Missing git_history_metrics.csv for repository: {repository}"
        )

    print(f"\nProcessing repository: {repository}")

    # -----------------------------
    # Source-code dataset
    # -----------------------------

    source_df = pd.read_csv(file_metrics_path)

    required_source_columns = [
        "file_path",
        "language",
        "extension",
        "loc",
        "size_bytes",
    ]

    missing_source = [
        column
        for column in required_source_columns
        if column not in source_df.columns
    ]

    if missing_source:
        raise ValueError(
            f"{repository}/file_metrics.csv is missing columns: "
            f"{missing_source}"
        )

    source_df = source_df[required_source_columns].copy()

    source_df.insert(
        0,
        "repository",
        clean_repository_name(repository)
    )

    # -----------------------------
    # Git-history dataset
    # -----------------------------

    history_df = pd.read_csv(history_metrics_path)

    required_history_columns = [
        "file_path",
        "change_count",
    ]

    missing_history = [
        column
        for column in required_history_columns
        if column not in history_df.columns
    ]

    if missing_history:
        raise ValueError(
            f"{repository}/git_history_metrics.csv is missing columns: "
            f"{missing_history}"
        )

    history_df = history_df[required_history_columns].copy()

    history_df.insert(
        0,
        "repository",
        clean_repository_name(repository)
    )

    print(f"  Source-code records : {len(source_df)}")
    print(f"  History records     : {len(history_df)}")

    return source_df, history_df


# ---------------------------------------------------------
# Main Preparation Function
# ---------------------------------------------------------

def prepare_datasets():
    """
    Read all five repositories and combine their respective
    Lab-1 datasets.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    source_datasets = []
    history_datasets = []

    print("=" * 70)
    print("LAB-2 DATASET PREPARATION")
    print("=" * 70)

    for repository in REPOSITORIES:

        source_df, history_df = load_repository_data(repository)

        source_datasets.append(source_df)
        history_datasets.append(history_df)

    # -----------------------------------------------------
    # Combine all source-code datasets
    # -----------------------------------------------------

    combined_source = pd.concat(
        source_datasets,
        ignore_index=True
    )

    # -----------------------------------------------------
    # Combine all history datasets
    # -----------------------------------------------------

    combined_history = pd.concat(
        history_datasets,
        ignore_index=True
    )

    # -----------------------------------------------------
    # Save
    # -----------------------------------------------------

    source_output = OUTPUT_DIR / "source_code_dataset.csv"
    history_output = OUTPUT_DIR / "commit_history_dataset.csv"

    combined_source.to_csv(
        source_output,
        index=False
    )

    combined_history.to_csv(
        history_output,
        index=False
    )

    print("\n" + "=" * 70)
    print("DATASET PREPARATION COMPLETED")
    print("=" * 70)

    print(f"\nSource-code dataset:")
    print(f"  Records : {len(combined_source)}")
    print(f"  Output  : {source_output}")

    print(f"\nCommit-history dataset:")
    print(f"  Records : {len(combined_history)}")
    print(f"  Output  : {history_output}")

    return combined_source, combined_history


if __name__ == "__main__":
    prepare_datasets()