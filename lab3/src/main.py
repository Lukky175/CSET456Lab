from pathlib import Path
import sys
import time


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "output"


# ============================================================
# IMPORT PROJECT MODULES
# ============================================================

from character_tokenizer import (
    run_character_tokenizer
)

from word_tokenizer import (
    run_word_tokenizer
)

from subword_tokenizer import (
    run_subword_tokenizer
)

from embedding_analysis import (
    run_embedding_analysis
)

from token_similarity import (
    run_token_similarity
)

from similarity_improvement import (
    run_similarity_improvement
)


# ============================================================
# TERMINAL UI
# ============================================================

def print_banner():

    print()

    print("=" * 78)

    print(
        " " * 20
        + "SPECIAL TOPICS IN DEVOPS"
    )

    print(
        " " * 29
        + "LAB - 3"
    )

    print()

    print(
        " " * 12
        + "SOFTWARE REPOSITORY TOKENIZATION"
    )

    print("=" * 78)

    print()

    print(
        "Dataset : combined_dataset.csv"
    )

    print(
        "Pipeline: "
        "Tokenization -> Embeddings -> "
        "Similarity -> Improvement"
    )

    print()


def print_stage(
    number,
    title
):

    print()
    print()

    print("#" * 78)

    print(
        f"# TASK {number}: {title}"
    )

    print("#" * 78)

    print()


def print_success(
    message
):

    print()

    print("-" * 78)

    print(
        f"[✓] {message}"
    )

    print("-" * 78)


def print_error(
    message
):

    print()

    print("-" * 78)

    print(
        f"[ERROR] {message}"
    )

    print("-" * 78)


# ============================================================
# OUTPUT DIRECTORY
# ============================================================

def print_output_directory():

    print()

    print("=" * 78)

    print(
        "GENERATED OUTPUT FILES"
    )

    print("=" * 78)

    print()

    if not OUTPUT_DIR.exists():

        print(
            "Output directory does not exist."
        )

        return

    files = sorted(
        OUTPUT_DIR.iterdir()
    )

    if not files:

        print(
            "No output files generated."
        )

        return

    for file in files:

        if file.is_file():

            size = file.stat().st_size

            print(
                f"{file.name:45}"
                f"{size:>12,} bytes"
            )

    print()


# ============================================================
# SAFE TASK EXECUTION
# ============================================================

def run_task(
    task_number,
    task_name,
    function
):

    print_stage(
        task_number,
        task_name
    )

    start_time = time.time()

    try:

        result = function()

        elapsed = (
            time.time()
            - start_time
        )

        print()

        print_success(
            f"Task {task_number} completed "
            f"in {elapsed:.2f} seconds."
        )

        return True, result

    except FileNotFoundError as error:

        elapsed = (
            time.time()
            - start_time
        )

        print_error(
            f"Task {task_number} could not "
            f"find a required file."
        )

        print()

        print(
            str(error)
        )

        print()

        print(
            f"Task {task_number} stopped after "
            f"{elapsed:.2f} seconds."
        )

        return False, None

    except ValueError as error:

        elapsed = (
            time.time()
            - start_time
        )

        print_error(
            f"Task {task_number} encountered "
            f"invalid data."
        )

        print()

        print(
            str(error)
        )

        print()

        print(
            f"Task {task_number} stopped after "
            f"{elapsed:.2f} seconds."
        )

        return False, None

    except Exception as error:

        elapsed = (
            time.time()
            - start_time
        )

        print_error(
            f"Task {task_number} failed."
        )

        print()

        print(
            f"Error type : "
            f"{type(error).__name__}"
        )

        print(
            f"Error      : "
            f"{error}"
        )

        print()

        print(
            f"Task {task_number} stopped after "
            f"{elapsed:.2f} seconds."
        )

        return False, None


# ============================================================
# TASK 1
# ============================================================

def task_1_tokenization():

    """
    Execute all three tokenizer experiments.

    Character
    Word
    Subword/BPE
    """

    print(
        "Starting three tokenizer experiments..."
    )

    print()

    # --------------------------------------------------------
    # Character tokenizer
    # --------------------------------------------------------

    print(
        "[1/3] Character-level tokenizer"
    )

    character_result = (
        run_character_tokenizer()
    )

    print_success(
        "Character-level tokenizer completed."
    )

    # --------------------------------------------------------
    # Word tokenizer
    # --------------------------------------------------------

    print()

    print(
        "[2/3] Word-level tokenizer"
    )

    word_result = (
        run_word_tokenizer()
    )

    print_success(
        "Word-level tokenizer completed."
    )

    # --------------------------------------------------------
    # Subword tokenizer
    # --------------------------------------------------------

    print()

    print(
        "[3/3] Subword-level BPE tokenizer"
    )

    subword_result = (
        run_subword_tokenizer()
    )

    print_success(
        "Subword/BPE tokenizer completed."
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print()

    print(
        "=" * 78
    )

    print(
        "TOKENIZATION SUMMARY"
    )

    print(
        "=" * 78
    )

    print()

    print(
        "Character tokenizer : completed"
    )

    print(
        "Word tokenizer      : completed"
    )

    print(
        "Subword/BPE tokenizer: completed"
    )

    return {
        "character": character_result,
        "word": word_result,
        "subword": subword_result
    }


# ============================================================
# TASK 2
# ============================================================

def task_2_embeddings():

    """
    Run the random embedding experiment.

    Includes:

    - Top 50 token identification
    - Random embedding initialization
    - Embedding matrix generation
    - Cosine similarity
    - Top 10 most similar pairs
    - Top 10 least similar pairs
    """

    print(
        "Using the subword/BPE tokenizer "
        "for embedding analysis."
    )

    print()

    print(
        "Embedding dimension : 128"
    )

    print(
        "Top frequent tokens : 50"
    )

    print(
        "Similarity metric   : Cosine similarity"
    )

    print()

    result = (
        run_embedding_analysis()
    )

    return result


# ============================================================
# TASK 3 + TASK 4
# ============================================================

def task_3_and_4_similarity():

    """
    Execute Tasks 3 and 4.

    Task 3:
        Interactively select five tokens from the
        top 50 and manually choose a related token
        for each.

    Task 4:
        Calculate cosine similarity between each
        selected pair.
    """

    print(
        "Tasks 3 and 4 now use interactive selection."
    )

    print()

    print(
        "You will:"
    )

    print(
        "  1. See the top 50 tokens."
    )

    print(
        "  2. Select five tokens by number."
    )

    print(
        "  3. Choose one related token for each."
    )

    print(
        "  4. Calculate cosine similarity."
    )

    print()

    print(
        "Remember:"
    )

    print(
        "At least two selected tokens should be "
        "different from your neighboring student's choices."
    )

    print()

    result = (
        run_token_similarity()
    )

    return result


# ============================================================
# TASK 5 + TASK 6
# ============================================================

def task_5_and_6_improvement():

    """
    Execute Tasks 5 and 6.

    Task 5:
        Apply the naive similarity improvement algorithm.

    Task 6:
        Repeat the similarity experiment and compare
        the original and improved embeddings.
    """

    print(
        "Starting naive similarity improvement experiment."
    )

    print()

    print(
        "Method:"
    )

    print(
        "Character/token relationship rule"
        " -> identify related tokens"
        " -> move embeddings closer"
    )

    print()

    result = (
        run_similarity_improvement()
    )

    return result


# ============================================================
# MAIN PIPELINE
# ============================================================

def main():

    overall_start = time.time()

    print_banner()

    # --------------------------------------------------------
    # Prepare output directory
    # --------------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print(
        f"Output directory: {OUTPUT_DIR}"
    )

    print()

    # ========================================================
    # TASK 1
    # ========================================================

    task_1_success, task_1_result = (
        run_task(
            1,
            "CHARACTER, WORD AND SUBWORD TOKENIZATION",
            task_1_tokenization
        )
    )

    if not task_1_success:

        print_error(
            "Pipeline stopped because Task 1 failed."
        )

        return 1

    # ========================================================
    # TASK 2
    # ========================================================

    task_2_success, task_2_result = (
        run_task(
            2,
            "RANDOM EMBEDDING AND TOKEN SIMILARITY ANALYSIS",
            task_2_embeddings
        )
    )

    if not task_2_success:

        print_error(
            "Pipeline stopped because Task 2 failed."
        )

        return 1

    # ========================================================
    # TASK 3 + TASK 4
    # ========================================================

    task_3_success, task_3_result = (
        run_task(
            "3 & 4",
            "INTERACTIVE TOKEN SELECTION AND SIMILARITY",
            task_3_and_4_similarity
        )
    )

    if not task_3_success:

        print_error(
            "Pipeline stopped because Tasks 3 and 4 failed."
        )

        return 1

    # ========================================================
    # TASK 5 + TASK 6
    # ========================================================

    task_5_success, task_5_result = (
        run_task(
            "5 & 6",
            "NAIVE SIMILARITY IMPROVEMENT AND RE-EXPERIMENT",
            task_5_and_6_improvement
        )
    )

    if not task_5_success:

        print_error(
            "Pipeline stopped because Tasks 5 and 6 failed."
        )

        return 1

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    total_time = (
        time.time()
        - overall_start
    )

    print()

    print()

    print(
        "=" * 78
    )

    print(
        " " * 27
        + "LAB-3 COMPLETE"
    )

    print(
        "=" * 78
    )

    print()

    print(
        f"Total execution time : "
        f"{total_time:.2f} seconds"
    )

    print()

    print(
        "Completed stages:"
    )

    print(
        "  [✓] Character-level tokenization"
    )

    print(
        "  [✓] Word-level tokenization"
    )

    print(
        "  [✓] Subword/BPE tokenization"
    )

    print(
        "  [✓] Random embedding matrix"
    )

    print(
        "  [✓] Top 50 token analysis"
    )

    print(
        "  [✓] Top 10 most similar embeddings"
    )

    print(
        "  [✓] Top 10 least similar embeddings"
    )

    print(
        "  [✓] Five-token manual experiment"
    )

    print(
        "  [✓] Pair cosine similarity"
    )

    print(
        "  [✓] Naive similarity improvement"
    )

    print(
        "  [✓] Before/after experiment"
    )

    # --------------------------------------------------------
    # OUTPUT FILES
    # --------------------------------------------------------

    print_output_directory()

    print()

    print(
        "=" * 78
    )

    print(
        "NEXT STEP"
    )

    print(
        "=" * 78
    )

    print()

    print(
        "Review the generated files in:"
    )

    print(
        f"    {OUTPUT_DIR}"
    )

    print()

    print(
        "Important Task 3/4 outputs:"
    )

    print(
        "    task3_selected_tokens.csv"
    )

    print(
        "    task4_pair_similarity.csv"
    )

    print()

    print(
        "Use these files and the terminal output "
        "when documenting your observations in README.md."
    )

    print()

    return 0


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:

        exit_code = main()

        sys.exit(exit_code)

    except KeyboardInterrupt:

        print()
        print()

        print(
            "=" * 78
        )

        print(
            "PROGRAM INTERRUPTED"
        )

        print(
            "=" * 78
        )

        print()

        print(
            "Execution stopped by the user."
        )

        print()

        sys.exit(130)

    except Exception as error:

        print()
        print()

        print(
            "=" * 78
        )

        print(
            "UNEXPECTED PIPELINE ERROR"
        )

        print(
            "=" * 78
        )

        print()

        print(
            f"Error type : "
            f"{type(error).__name__}"
        )

        print(
            f"Error      : "
            f"{error}"
        )

        print()

        sys.exit(1)