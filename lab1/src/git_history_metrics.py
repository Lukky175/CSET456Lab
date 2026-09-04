from pathlib import Path
from collections import Counter
from datetime import datetime
import csv
import subprocess


# =========================================================
# Configuration
# =========================================================

HISTORY_WINDOW = 400


# =========================================================
# Helper
# =========================================================

def run_git_command(
    repository_path,
    arguments
):

    command = [
        "git",
        "-C",
        str(repository_path)
    ] + arguments

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    if result.returncode != 0:

        raise RuntimeError(
            "Git command failed:\n"
            + result.stderr
        )

    return result.stdout


# =========================================================
# Git History Metrics
# =========================================================

def generate_git_history_metrics(
    repository_path,
    output_path
):

    repository_path = Path(repository_path)
    output_path = Path(output_path)

    print("\n" + "=" * 70)
    print("GIT HISTORY METRICS")
    print("=" * 70)

    print(
        f"\nRepository: {repository_path}"
    )

    print(
        "Using all commits for metadata and "
        f"latest {HISTORY_WINDOW} commits for file changes."
    )

    # =====================================================
    # 1. ALL COMMITS
    #
    # Only commit hash, author and date are requested.
    # No file/diff information is loaded.
    # =====================================================

    print(
        "\n[1/2] Scanning all commit metadata..."
    )

    print("-" * 70)

    start_time = datetime.now()

    output = run_git_command(
        repository_path,
        [
            "log",
            "--all",
            "--format=%H%x09%an%x09%aI"
        ]
    )

    total_commits = 0

    contributors = Counter()
    commits_per_month = Counter()

    for line in output.splitlines():

        if not line.strip():
            continue

        parts = line.split(
            "\t",
            2
        )

        if len(parts) != 3:
            continue

        commit_hash, author, date = parts

        total_commits += 1

        if not author:
            author = "Unknown"

        contributors[author] += 1

        try:

            month = datetime.fromisoformat(
                date
            ).strftime("%Y-%m")

            commits_per_month[month] += 1

        except ValueError:

            pass

        if total_commits % 5000 == 0:

            elapsed = (
                datetime.now() - start_time
            )

            print(
                f"[PROGRESS] "
                f"{total_commits:,} commits "
                f"| elapsed: {elapsed}"
            )

    all_commits_time = (
        datetime.now() - start_time
    )

    print(
        f"[✓] {total_commits:,} commits scanned "
        f"in {all_commits_time}"
    )

    # =====================================================
    # 2. LATEST HISTORY_WINDOW COMMITS
    #
    # The most recent HISTORY_WINDOW commits are analyzed
    # for file-level change metrics.
    #
    # Git produces:
    #   additions
    #   deletions
    #   changed file
    #
    # No full patches are generated.
    # =====================================================

    print(
        f"\n[2/2] Analyzing latest "
        f"{HISTORY_WINDOW} commits..."
    )

    print("-" * 70)

    start_time = datetime.now()

    recent_output = run_git_command(
        repository_path,
        [
            "log",
            f"-{HISTORY_WINDOW}",
            "--numstat",
            "--format=COMMIT%x09%H%x09%aI"
        ]
    )

    file_change_counter = Counter()

    total_added_lines = 0
    total_deleted_lines = 0

    total_files_changed = 0
    analyzed_commits = 0

    current_commit_files = 0

    # -----------------------------------------------------
    # Parse Git output
    # -----------------------------------------------------

    for line in recent_output.splitlines():

        if not line.strip():
            continue

        # -------------------------------------------------
        # New commit
        # -------------------------------------------------

        if line.startswith("COMMIT\t"):

            if analyzed_commits > 0:

                total_files_changed += (
                    current_commit_files
                )

            parts = line.split(
                "\t",
                2
            )

            analyzed_commits += 1

            current_commit_files = 0

            if (
                analyzed_commits % 25 == 0
                or analyzed_commits == HISTORY_WINDOW
            ):

                elapsed = (
                    datetime.now() - start_time
                )

                print(
                    f"[PROGRESS] "
                    f"{analyzed_commits}/"
                    f"{HISTORY_WINDOW} commits "
                    f"| elapsed: {elapsed}"
                )

            continue

        # -------------------------------------------------
        # numstat line
        #
        # Example:
        #
        # 20  5  sklearn/example.py
        #
        # Binary:
        #
        # -  -  image.png
        # -------------------------------------------------

        parts = line.split(
            "\t",
            2
        )

        if len(parts) != 3:
            continue

        additions, deletions, file_path = parts

        current_commit_files += 1

        file_path = file_path.strip()

        if not file_path:
            continue

        file_change_counter[file_path] += 1

        # -------------------------------------------------
        # Additions
        # -------------------------------------------------

        if additions.isdigit():

            total_added_lines += int(
                additions
            )

        # -------------------------------------------------
        # Deletions
        # -------------------------------------------------

        if deletions.isdigit():

            total_deleted_lines += int(
                deletions
            )

    # Add the final commit
    if analyzed_commits > 0:

        total_files_changed += (
            current_commit_files
        )

    recent_time = (
        datetime.now() - start_time
    )

    print(
        f"[✓] {analyzed_commits} recent commits analyzed "
        f"in {recent_time}"
    )

    # =====================================================
    # Calculations
    # =====================================================

    # -----------------------------------------------------
    # Most active contributor
    # -----------------------------------------------------

    if contributors:

        most_active_name, most_active_count = (
            contributors.most_common(1)[0]
        )

    else:

        most_active_name = None
        most_active_count = 0

    # -----------------------------------------------------
    # Average files changed per month
    #
    # The latest HISTORY_WINDOW commits are grouped by
    # calendar month using their author dates.
    #
    # Formula:
    #
    # total file changes in the selected commit window
    # ------------------------------------------------
    # number of distinct calendar months represented
    #
    # IMPORTANT:
    # This is NOT the average number of unique files.
    # It is the average number of file-change events per
    # calendar month within the selected commit window.
    # -----------------------------------------------------

    recent_months = set()

    recent_date_output = run_git_command(
        repository_path,
        [
            "log",
            f"-{HISTORY_WINDOW}",
            "--format=%aI"
        ]
    )

    for line in recent_date_output.splitlines():

        if not line.strip():
            continue

        try:

            month = datetime.fromisoformat(
                line.strip()
            ).strftime("%Y-%m")

            recent_months.add(month)

        except ValueError:

            continue

    if recent_months:

        average_files_changed_per_month = (
            total_files_changed
            / len(recent_months)
        )

    else:

        average_files_changed_per_month = 0

    # -----------------------------------------------------
    # Average additions/deletions
    # -----------------------------------------------------

    if analyzed_commits:

        average_added_lines = (
            total_added_lines
            / analyzed_commits
        )

        average_deleted_lines = (
            total_deleted_lines
            / analyzed_commits
        )

    else:

        average_added_lines = 0
        average_deleted_lines = 0

    # =====================================================
    # Top frequently changed files
    # =====================================================

    top_changed_files = []

    for file_path, count in (
        file_change_counter.most_common(10)
    ):

        top_changed_files.append(
            {
                "file_path": file_path,
                "change_count": count
            }
        )

    # =====================================================
    # Contributor data
    # =====================================================

    contributor_data = []

    for author, count in (
        contributors.most_common()
    ):

        contributor_data.append(
            {
                "author": author,
                "commit_count": count
            }
        )

    # =====================================================
    # Commits per month
    # =====================================================

    commits_per_month_data = dict(
        sorted(
            commits_per_month.items()
        )
    )

    # =====================================================
    # Git History CSV
    #
    # This is an additional dataset.
    # The main required CSV remains file_metrics.csv.
    # =====================================================

    csv_path = (
        output_path /
        "git_history_metrics.csv"
    )

    with open(
        csv_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "file_path",
                "change_count"
            ]
        )

        for file_path, count in (
            file_change_counter.most_common()
        ):

            writer.writerow(
                [
                    file_path,
                    count
                ]
            )

    # =====================================================
    # Terminal Summary
    # =====================================================

    print("\n" + "=" * 70)
    print("GIT HISTORY SUMMARY")
    print("=" * 70)

    print(
        f"\nTotal Commits                 : "
        f"{total_commits:,}"
    )

    print(
        f"Number of Contributors       : "
        f"{len(contributors):,}"
    )

    print(
        f"Most Active Contributor      : "
        f"{most_active_name} "
        f"({most_active_count:,} commits)"
    )

    print(
        f"File Change Analysis Window  : "
        f"Latest {analyzed_commits:,} commits"
    )

    print(
        f"Average Files Changed/Month  : "
        f"{average_files_changed_per_month:,.2f} "
        f"(Last {analyzed_commits:,} commits)"
    )

    print(
        f"Average Added Lines/Commit   : "
        f"{average_added_lines:,.2f}"
    )

    print(
        f"Average Deleted Lines/Commit : "
        f"{average_deleted_lines:,.2f}"
    )

    # -----------------------------------------------------
    # Top changed files
    # -----------------------------------------------------

    print(
        "\nTop 10 Most Frequently Changed Files"
    )

    print("-" * 70)

    for rank, record in enumerate(
        top_changed_files,
        start=1
    ):

        print(
            f"{rank:2}. "
            f"{record['change_count']:5} changes  "
            f"{record['file_path']}"
        )

    # -----------------------------------------------------
    # Completion
    # -----------------------------------------------------

    total_time = (
        all_commits_time
        + recent_time
    )

    print(
        f"\nGit history analysis completed "
        f"in {total_time}"
    )

    print(
        f"CSV created: {csv_path}"
    )

    print("=" * 70)

    # =====================================================
    # Return statistics
    # =====================================================

    return {

        "total_commits":
            total_commits,

        "number_of_contributors":
            len(contributors),

        "most_active_contributor": {

            "name":
                most_active_name,

            "commit_count":
                most_active_count
        },

        "contributors":
            contributor_data,

        "top_frequently_changed_files":
            top_changed_files,

        "commits_per_month":
            commits_per_month_data,

        "file_change_metrics_scope":
            f"latest_{analyzed_commits}_commits",

        "file_change_analysis_window":
            analyzed_commits,

        "average_files_changed_per_month":
            round(
                average_files_changed_per_month,
                2
            ),

        "total_lines_added":
            total_added_lines,

        "total_lines_deleted":
            total_deleted_lines,

        "average_added_lines_per_commit":
            round(
                average_added_lines,
                2
            ),

        "average_deleted_lines_per_commit":
            round(
                average_deleted_lines,
                2
            ),

        "git_history_csv":
            str(csv_path)
    }

