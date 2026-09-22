from prepare_datasets import prepare_datasets
from clean_and_merge import clean_and_merge
from analyze_datasets import analyze_datasets


def main():

    print("\n")
    print("=" * 70)
    print("          AB-1 LAB-2")
    print("  MULTI-REPOSITORY DATASET PREPARATION")
    print("=" * 70)

    try:

        # -------------------------------------------------
        # Step 1
        # -------------------------------------------------

        print("\n[1/3] Preparing datasets...")

        prepare_datasets()

        print("\n[✓] Dataset preparation completed.")

        # -------------------------------------------------
        # Step 2
        # -------------------------------------------------

        print("\n[2/3] Cleaning and merging datasets...")

        clean_and_merge()

        print("\n[✓] Cleaning and merging completed.")

        # -------------------------------------------------
        # Step 3
        # -------------------------------------------------

        print("\n[3/3] Generating statistics...")

        analyze_datasets()

        print("\n[✓] Dataset analysis completed.")

        # -------------------------------------------------
        # Completion
        # -------------------------------------------------

        print("\n")
        print("=" * 70)
        print("              LAB-2 COMPLETED")
        print("=" * 70)

        print("\nGenerated files are available in:")
        print("output/")

    except FileNotFoundError as error:

        print("\n[ERROR] Required file not found.")
        print(error)

    except ValueError as error:

        print("\n[ERROR] Invalid dataset structure.")
        print(error)

    except Exception as error:

        print("\n[ERROR] Unexpected error occurred.")
        print(error)


if __name__ == "__main__":
    main()