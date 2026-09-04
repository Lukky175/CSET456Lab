from pathlib import Path

from repository_setup import setup_repository
from file_metrics import generate_file_metrics
from git_history_metrics import generate_git_history_metrics
from report_generator import generate_reports


# =========================================================
# Paths
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_ROOT = (
    BASE_DIR /
    "output"
)


# =========================================================
# Main Program
# =========================================================

def main():

    print("\n" + "=" * 70)

    print(
        "          SOFTWARE REPOSITORY MINING - LAB 1"
    )

    print("=" * 70)

    # =====================================================
    # Input
    # =====================================================

    repository_url = input(
        "\nEnter GitHub repository URL: "
    ).strip()

    if not repository_url:

        print(
            "\nERROR: Repository URL cannot be empty."
        )

        return

    try:

        # =================================================
        # 1. Repository Setup
        # =================================================

        print(
            "\n[1/4] Repository setup"
        )

        repository = setup_repository(
            repository_url
        )

        repository_name = (
            repository[
                "repository_name"
            ]
        )

        repository_path = (
            repository[
                "repository_path"
            ]
        )

        print(
            "[✓] Repository setup completed"
        )

        # =================================================
        # Output directory
        # =================================================

        output_path = (
            OUTPUT_ROOT /
            repository_name
        )

        output_path.mkdir(
            parents=True,
            exist_ok=True
        )

        # =================================================
        # 2. File Metrics
        # =================================================

        print(
            "\n[2/4] File metrics"
        )

        file_statistics = (
            generate_file_metrics(
                repository_path,
                output_path
            )
        )

        print(
            "[✓] File metrics completed"
        )

        # =================================================
        # 3. Git History
        # =================================================

        print(
            "\n[3/4] Git history"
        )

        git_statistics = (
            generate_git_history_metrics(
                repository_path,
                output_path
            )
        )

        print(
            "[✓] Git history completed"
        )

        # =================================================
        # 4. Reports
        # =================================================

        print(
            "\n[4/4] Generating reports"
        )

        reports = generate_reports(
            repository_name,
            output_path,
            file_statistics,
            git_statistics
        )

        print(
            "[✓] Reports generated"
        )

        # =================================================
        # Final Output
        # =================================================

        print("\n" + "=" * 70)
        print("LAB-1 COMPLETED")
        print("=" * 70)

        print(
            f"\nRepository : {repository_name}"
        )

        print(
            f"Output     : {output_path}"
        )

        print("\nGenerated Files")
        print("-" * 70)

        print(
            f"✓ file_metrics.csv"
        )

        print(
            f"✓ git_history_metrics.csv"
        )

        print(
            f"✓ repository_statistics.json"
        )

        print(
            f"✓ summary.md"
        )

        print("\n" + "=" * 70)

    except KeyboardInterrupt:

        print(
            "\n\nOperation cancelled by user."
        )

    except Exception as error:

        print("\n" + "=" * 70)
        print("ERROR")
        print("=" * 70)

        print(
            f"\n{error}"
        )


# =========================================================
# Run
# =========================================================

if __name__ == "__main__":

    main()

