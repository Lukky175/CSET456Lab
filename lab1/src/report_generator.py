from pathlib import Path
import json


# =========================================================
# Generate Final Reports
# =========================================================

def generate_reports(
    repository_name,
    output_path,
    file_statistics,
    git_statistics
):

    output_path = Path(output_path)

    output_path.mkdir(
        parents=True,
        exist_ok=True
    )

    # =====================================================
    # Combined JSON
    # =====================================================

    statistics = {

        "repository": file_statistics,

        "git_history": git_statistics
    }

    json_path = (
        output_path /
        "repository_statistics.json"
    )

    with open(
        json_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            statistics,
            file,
            indent=4
        )

    # =====================================================
    # Markdown Summary
    # =====================================================

    summary_path = (
        output_path /
        "summary.md"
    )

    with open(
        summary_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "# Software Repository Mining Report\n\n"
        )

        file.write(
            f"**Repository:** {repository_name}\n\n"
        )

        # =================================================
        # Repository Inventory
        # =================================================

        file.write(
            "## 1. Repository Inventory\n\n"
        )

        file.write(
            f"- Total files: "
            f"{file_statistics['total_files']:,}\n"
        )

        file.write(
            f"- Source-code files: "
            f"{file_statistics['source_code_files']:,}\n"
        )

        file.write(
            f"- Directories: "
            f"{file_statistics['directories']:,}\n"
        )

        file.write(
            f"- Total LOC: "
            f"{file_statistics['total_loc']:,}\n"
        )

        file.write(
            f"- Average LOC per source file: "
            f"{file_statistics['average_loc_per_source_file']:,.2f}\n\n"
        )

        # =================================================
        # Programming Languages
        # =================================================

        file.write(
            "### Programming Languages\n\n"
        )

        for language, count in (
            file_statistics[
                "programming_languages"
            ].items()
        ):

            file.write(
                f"- {language}: {count:,} files\n"
            )

        file.write("\n")

        # =================================================
        # File Types
        # =================================================

        file.write(
            "### File-Type Distribution\n\n"
        )

        file.write(
            "| Extension | Files |\n"
            "|---|---:|\n"
        )

        for extension, count in (
            file_statistics[
                "file_type_distribution"
            ].items()
        ):

            file.write(
                f"| `{extension}` | "
                f"{count:,} |\n"
            )

        file.write("\n")

        # =================================================
        # Largest Files
        # =================================================

        file.write(
            "### Largest Source Files\n\n"
        )

        file.write(
            "| File | LOC |\n"
            "|---|---:|\n"
        )

        for item in (
            file_statistics[
                "largest_source_files"
            ]
        ):

            file.write(
                f"| `{item['file_path']}` | "
                f"{item['loc']:,} |\n"
            )

        file.write("\n")

        # =================================================
        # Git History
        # =================================================

        file.write(
            "## 2. Git History\n\n"
        )

        file.write(
            f"- Total commits: "
            f"{git_statistics['total_commits']:,}\n"
        )

        file.write(
            f"- Number of contributors: "
            f"{git_statistics['number_of_contributors']:,}\n"
        )

        most_active = (
            git_statistics[
                "most_active_contributor"
            ]
        )

        file.write(
            f"- Most active contributor: "
            f"{most_active['name']} "
            f"({most_active['commit_count']:,} commits)\n"
        )

        file.write(
            f"- File-change analysis window: "
            f"Latest {git_statistics['file_change_analysis_window']:,} commits\n"
        )

        file.write(
            f"- Average files changed per month "
            f"(last {git_statistics['file_change_analysis_window']:,} commits): "
            f"{git_statistics['average_files_changed_per_month']:,.2f}\n"
        )

        file.write(
            f"- Average lines added per commit: "
            f"{git_statistics['average_added_lines_per_commit']:,.2f}\n"
        )

        file.write(
            f"- Average lines deleted per commit: "
            f"{git_statistics['average_deleted_lines_per_commit']:,.2f}\n\n"
        )

        # =================================================
        # Frequently Changed Files
        # =================================================

        file.write(
            "### Most Frequently Changed Files\n\n"
        )

        file.write(
            "| Rank | File | Changes |\n"
            "|---:|---|---:|\n"
        )

        for rank, item in enumerate(
            git_statistics[
                "top_frequently_changed_files"
            ],
            start=1
        ):

            file.write(
                f"| {rank} | "
                f"`{item['file_path']}` | "
                f"{item['change_count']:,} |\n"
            )

        file.write("\n")

        # =================================================
        # Commits Per Month
        # =================================================

        file.write(
            "### Commits Per Month\n\n"
        )

        file.write(
            "| Month | Commits |\n"
            "|---|---:|\n"
        )

        for month, count in (
            git_statistics[
                "commits_per_month"
            ].items()
        ):

            file.write(
                f"| {month} | "
                f"{count:,} |\n"
            )

        file.write("\n")

        # =================================================
        # Generated Datasets
        # =================================================

        file.write(
            "## 3. Generated Datasets\n\n"
        )

        file.write(
            "- `file_metrics.csv` — "
            "file-level dataset\n"
        )

        file.write(
            "- `git_history_metrics.csv` — "
            "file-change frequency dataset for the latest "
            f"{git_statistics['file_change_metrics_scope'].split('_')[-2]} "
            "commits\n"
        )

        file.write(
            "- `repository_statistics.json` — "
            "complete repository statistics\n"
        )

        file.write(
            "- `summary.md` — "
            "human-readable report\n"
        )

    return {

        "json_path":
            str(json_path),

        "summary_path":
            str(summary_path)
    }

