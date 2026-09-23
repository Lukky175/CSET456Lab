from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "output"

TOP_50_FILE = OUTPUT_DIR / "top_50_tokens.csv"
EMBEDDING_MATRIX_FILE = OUTPUT_DIR / "random_embedding_matrix.npy"

TASK3_OUTPUT = OUTPUT_DIR / "task3_selected_tokens.csv"
TASK4_OUTPUT = OUTPUT_DIR / "task4_pair_similarity.csv"


# ============================================================
# CONFIGURATION
# ============================================================

NUMBER_OF_SELECTED_TOKENS = 5


# ============================================================
# TERMINAL UI
# ============================================================

def print_section(title):

    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


def print_subsection(title):

    print()
    print("-" * 78)
    print(title)
    print("-" * 78)


# ============================================================
# COSINE SIMILARITY
# ============================================================

def cosine_similarity(vector_a, vector_b):
    """
    Calculate cosine similarity between two embedding vectors.

    Formula:

                    A · B
    cosine = -------------------
              ||A|| * ||B||

    Range:

        -1 -> opposite directions
         0 -> unrelated/orthogonal directions
         1 -> same direction
    """

    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(
        np.dot(vector_a, vector_b)
        / (norm_a * norm_b)
    )


# ============================================================
# LOAD DATA
# ============================================================

def load_embedding_data():

    print_section(
        "TASK 3 & 4 — LOADING TOKEN AND EMBEDDING DATA"
    )

    if not TOP_50_FILE.exists():

        raise FileNotFoundError(
            f"\nTop-50 token file not found:\n"
            f"{TOP_50_FILE}\n\n"
            f"Run Task 2 first."
        )

    if not EMBEDDING_MATRIX_FILE.exists():

        raise FileNotFoundError(
            f"\nRandom embedding matrix not found:\n"
            f"{EMBEDDING_MATRIX_FILE}\n\n"
            f"Run Task 2 first."
        )

    # --------------------------------------------------------
    # Load top 50
    # --------------------------------------------------------

    print("\n[1/3] Loading top-50 token data...")

    top_50 = pd.read_csv(
        TOP_50_FILE
    )

    print(
        f"      Tokens loaded : {len(top_50)}"
    )

    # --------------------------------------------------------
    # Load embeddings
    # --------------------------------------------------------

    print("\n[2/3] Loading random embedding matrix...")

    embedding_matrix = np.load(
        EMBEDDING_MATRIX_FILE
    )

    print(
        f"      Matrix shape  : {embedding_matrix.shape}"
    )

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    if "token" not in top_50.columns:

        raise ValueError(
            "top_50_tokens.csv must contain a 'token' column."
        )

    tokens = (
        top_50["token"]
        .astype(str)
        .tolist()
    )

    if len(tokens) != embedding_matrix.shape[0]:

        raise ValueError(
            "\nNumber of tokens does not match "
            "embedding matrix rows.\n"
            f"Tokens         : {len(tokens)}\n"
            f"Embedding rows : {embedding_matrix.shape[0]}"
        )

    print("\n[3/3] Token and embedding data validated.")

    print(
        "\n[✓] Task 3/4 input data ready."
    )

    return (
        tokens,
        embedding_matrix,
        top_50
    )


# ============================================================
# CLEAN TOKEN FOR TERMINAL
# ============================================================

def clean_token(token):

    return (
        str(token)
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )


# ============================================================
# DISPLAY TOKEN TABLE
# ============================================================

def display_token_table(
    top_50,
    exclude_indices=None
):
    """
    Display the token choices in a compact table.

    exclude_indices:
        Token indices that should not be displayed.

    Example:
        If token #2 is selected, #2 will not appear as a
        possible related token.
    """

    if exclude_indices is None:

        exclude_indices = set()

    else:

        exclude_indices = set(
            exclude_indices
        )

    print()

    print(
        f"{'No.':<6}"
        f"{'Token':<28}"
        f"{'Frequency':>12}"
    )

    print("-" * 50)

    for index, row in top_50.iterrows():

        token_number = index + 1

        if token_number in exclude_indices:
            continue

        token = clean_token(
            row["token"]
        )

        frequency = int(
            row["frequency"]
        )

        print(
            f"{token_number:<6}"
            f"{token:<28}"
            f"{frequency:>12,}"
        )

    print("-" * 50)


# ============================================================
# INTEGER INPUT
# ============================================================

def get_integer_input(
    prompt,
    minimum,
    maximum
):
    """
    Safely obtain an integer from the user.
    """

    while True:

        user_input = input(
            prompt
        ).strip()

        try:

            value = int(
                user_input
            )

        except ValueError:

            print(
                "[!] Invalid input. "
                "Enter a number."
            )

            continue

        if value < minimum or value > maximum:

            print(
                f"[!] Enter a number between "
                f"{minimum} and {maximum}."
            )

            continue

        return value


# ============================================================
# SELECT FIVE TOKENS
# ============================================================

def select_five_tokens(
    tokens,
    top_50
):

    print_section(
        "TASK 3 — SELECT FIVE TOKENS"
    )

    print(
        "Select exactly FIVE tokens from the TOP 50."
    )

    print(
        "Use the token numbers shown in the table."
    )

    print()

    print(
        "LAB REQUIREMENT:"
    )

    print(
        "At least TWO selected tokens should be different"
    )

    print(
        "from the tokens selected by the student next to you."
    )

    print_subsection(
        "TOP 50 TOKENS — USE THESE NUMBERS"
    )

    display_token_table(
        top_50
    )

    selected_indices = []

    # --------------------------------------------------------
    # Selection loop
    # --------------------------------------------------------

    while len(selected_indices) < NUMBER_OF_SELECTED_TOKENS:

        remaining = (
            NUMBER_OF_SELECTED_TOKENS
            - len(selected_indices)
        )

        print()

        print(
            f"Tokens remaining to select: {remaining}"
        )

        choice = get_integer_input(
            "Enter token number: ",
            1,
            len(tokens)
        )

        index = choice - 1

        # Duplicate check
        if index in selected_indices:

            print(
                "[!] You already selected this token."
            )

            continue

        selected_indices.append(
            index
        )

        print(
            f"[✓] Selected #{choice} -> "
            f"{clean_token(tokens[index])}"
        )

    selected_tokens = [
        tokens[index]
        for index in selected_indices
    ]

    # --------------------------------------------------------
    # Display final selection
    # --------------------------------------------------------

    print_subsection(
        "YOUR FIVE SELECTED TOKENS"
    )

    for number, token in enumerate(
        selected_tokens,
        start=1
    ):

        print(
            f"{number}. "
            f"{clean_token(token)}"
        )

    return selected_tokens


# ============================================================
# SELECT RELATED TOKEN
# ============================================================

def select_related_token(
    selected_token,
    tokens,
    top_50
):
    """
    Ask the student to choose the token they personally
    consider most related to the selected token.

    This is the human judgement component of Task 3.
    """

    print()
    print("=" * 78)

    print(
        f"TOKEN: {clean_token(selected_token)}"
    )

    print("=" * 78)

    print()

    print(
        "Choose the token YOU consider most related."
    )

    print(
        "This is your human/semantic judgement."
    )

    print(
        "Do NOT use the random embedding similarity "
        "to make this decision."
    )

    # Find selected token number
    selected_index = tokens.index(
        selected_token
    )

    selected_number = (
        selected_index + 1
    )

    print_subsection(
        "AVAILABLE TOKENS"
    )

    display_token_table(
        top_50,
        exclude_indices={
            selected_number
        }
    )

    print()

    while True:

        choice = get_integer_input(
            "Enter related token number: ",
            1,
            len(tokens)
        )

        chosen_token = tokens[
            choice - 1
        ]

        # Prevent same-token selection
        if chosen_token == selected_token:

            print(
                "[!] You cannot select the same token."
            )

            continue

        print()

        print(
            "[✓] Relationship selected:"
        )

        print(
            f"    "
            f"{clean_token(selected_token)}"
            f"  <->  "
            f"{clean_token(chosen_token)}"
        )

        return chosen_token


# ============================================================
# TASK 3
# ============================================================

def perform_task_3(
    tokens,
    top_50
):

    print_section(
        "TASK 3 — HUMAN TOKEN RELATIONSHIP SELECTION"
    )

    # --------------------------------------------------------
    # Select five tokens
    # --------------------------------------------------------

    selected_tokens = select_five_tokens(
        tokens,
        top_50
    )

    print()

    print(
        "You have selected five tokens."
    )

    print(
        "Now choose ONE related token for each."
    )

    print(
        "These choices will be compared using cosine "
        "similarity in Task 4."
    )

    pairs = []

    # --------------------------------------------------------
    # Select relationship for each token
    # --------------------------------------------------------

    for number, selected_token in enumerate(
        selected_tokens,
        start=1
    ):

        print()

        print(
            f"[{number}/5] Selecting related token for:"
        )

        print(
            f"      {clean_token(selected_token)}"
        )

        related_token = select_related_token(
            selected_token,
            tokens,
            top_50
        )

        pairs.append(
            {
                "token_a": selected_token,
                "token_b": related_token
            }
        )

    result_df = pd.DataFrame(
        pairs
    )

    result_df.to_csv(
        TASK3_OUTPUT,
        index=False
    )

    # --------------------------------------------------------
    # Final Task 3 summary
    # --------------------------------------------------------

    print()
    print_section(
        "TASK 3 COMPLETE — SELECTED TOKEN PAIRS"
    )

    for number, row in enumerate(
        result_df.itertuples(index=False),
        start=1
    ):

        print(
            f"{number}. "
            f"{clean_token(row.token_a)}"
            f"  <->  "
            f"{clean_token(row.token_b)}"
        )

    print()

    print(
        f"Saved to: {TASK3_OUTPUT}"
    )

    return result_df


# ============================================================
# TASK 4
# ============================================================

def perform_task_4(
    pairs_df,
    tokens,
    embedding_matrix
):

    print_section(
        "TASK 4 — CHECKING TOKEN SIMILARITY"
    )

    if pairs_df is None or pairs_df.empty:

        raise ValueError(
            "No token pairs were selected."
        )

    print(
        "Calculating cosine similarity between "
        "your selected pairs..."
    )

    print()

    results = []

    for _, row in pairs_df.iterrows():

        token_a = str(
            row["token_a"]
        )

        token_b = str(
            row["token_b"]
        )

        index_a = tokens.index(
            token_a
        )

        index_b = tokens.index(
            token_b
        )

        similarity = cosine_similarity(
            embedding_matrix[index_a],
            embedding_matrix[index_b]
        )

        results.append(
            {
                "token_a": token_a,
                "token_b": token_b,
                "cosine_similarity": similarity
            }
        )

    result_df = pd.DataFrame(
        results
    )

    # --------------------------------------------------------
    # Display results
    # --------------------------------------------------------

    print(
        f"{'Token A':<25}"
        f"{'Token B':<25}"
        f"{'Cosine Similarity':>20}"
    )

    print("-" * 72)

    for _, row in result_df.iterrows():

        print(
            f"{clean_token(row['token_a']):<25}"
            f"{clean_token(row['token_b']):<25}"
            f"{row['cosine_similarity']:>20.6f}"
        )

    result_df.to_csv(
        TASK4_OUTPUT,
        index=False
    )

    print()

    print(
        "[✓] Task 4 completed."
    )

    print(
        f"Saved to: {TASK4_OUTPUT}"
    )

    return result_df


# ============================================================
# MAIN TASK FUNCTION
# ============================================================

def run_token_similarity():

    # --------------------------------------------------------
    # Load Task 2 outputs
    # --------------------------------------------------------

    tokens, embedding_matrix, top_50 = (
        load_embedding_data()
    )

    # --------------------------------------------------------
    # TASK 3
    # --------------------------------------------------------

    task3_results = perform_task_3(
        tokens,
        top_50
    )

    # --------------------------------------------------------
    # TASK 4
    # --------------------------------------------------------

    task4_results = perform_task_4(
        task3_results,
        tokens,
        embedding_matrix
    )

    # --------------------------------------------------------
    # Final status
    # --------------------------------------------------------

    print()
    print("=" * 78)
    print("TASKS 3 & 4 COMPLETED")
    print("=" * 78)

    return {
        "selected_pairs": task3_results,
        "similarity_results": task4_results
    }


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run_token_similarity()