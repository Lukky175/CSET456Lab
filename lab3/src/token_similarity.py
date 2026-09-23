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
    """Print a formatted section heading."""

    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


def print_subsection(title):
    """Print a smaller formatted heading."""

    print()
    print("-" * 78)
    print(title)
    print("-" * 78)


# ============================================================
# COSINE SIMILARITY
# ============================================================

def cosine_similarity(vector_a, vector_b):
    """
    Calculate cosine similarity between two vectors.

    Formula:

                A · B
    cosine = -----------
              ||A|| ||B||

    Range:
        -1  -> completely opposite directions
         0  -> orthogonal
         1  -> same direction
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
    """
    Load the top-50 token list and random embedding matrix
    generated during Task 2.
    """

    print_section("TASK 3 & 4 - LOADING TOKEN AND EMBEDDING DATA")

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

    print()
    print("[1/3] Loading top-50 tokens...")

    top_50 = pd.read_csv(TOP_50_FILE)

    print(
        f"      Tokens loaded : {len(top_50)}"
    )

    print()
    print("[2/3] Loading random embedding matrix...")

    embedding_matrix = np.load(
        EMBEDDING_MATRIX_FILE
    )

    print(
        f"      Matrix shape  : {embedding_matrix.shape}"
    )

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
            "Number of tokens does not match "
            "embedding matrix rows.\n"
            f"Tokens            : {len(tokens)}\n"
            f"Embedding rows    : {embedding_matrix.shape[0]}"
        )

    print()
    print("[3/3] Token and embedding data validated.")

    print()
    print("[✓] Task 3/4 input data ready.")

    return tokens, embedding_matrix, top_50


# ============================================================
# DISPLAY TOP 50 TOKENS
# ============================================================

def display_top_50_tokens(top_50):
    """
    Display the complete top-50 token list.

    The user can use the displayed numbers to select tokens.
    """

    print_section("TOP 50 MOST FREQUENT SUBWORD TOKENS")

    print()
    print(
        f"{'No.':<6}"
        f"{'Token':<30}"
        f"{'Frequency':>12}"
    )

    print("-" * 52)

    for index, row in top_50.iterrows():

        token = str(row["token"])

        frequency = int(row["frequency"])

        # Replace newlines so the terminal remains readable.
        token = (
            token
            .replace("\n", "\\n")
            .replace("\r", "\\r")
        )

        print(
            f"{index + 1:<6}"
            f"{token:<30}"
            f"{frequency:>12,}"
        )

    print()


# ============================================================
# GET INTEGER INPUT
# ============================================================

def get_integer_input(
    prompt,
    minimum,
    maximum
):
    """
    Safely read an integer from the user.

    Keeps asking until the user provides a valid number.
    """

    while True:

        try:

            value = int(
                input(prompt).strip()
            )

            if minimum <= value <= maximum:

                return value

            print(
                f"[!] Please enter a number between "
                f"{minimum} and {maximum}."
            )

        except ValueError:

            print(
                "[!] Invalid input. "
                "Please enter a number."
            )


# ============================================================
# SELECT FIVE TOKENS
# ============================================================

def select_five_tokens(
    tokens,
    top_50
):
    """
    Allow the user to select five tokens from the top 50.

    The user selects by number rather than typing the token
    manually, which prevents spelling mistakes.
    """

    print_section("TASK 3 - SELECT FIVE TOKENS")

    print(
        "You must select exactly five tokens from the top 50."
    )

    print()
    print(
        "IMPORTANT FOR THE LAB:"
    )

    print(
        "At least two of your selected tokens should be "
        "different from the tokens selected by the student "
        "sitting next to you."
    )

    print()
    print(
        "You can coordinate with your neighboring student "
        "before making the selection."
    )

    print()

    selected_indices = []

    while len(selected_indices) < NUMBER_OF_SELECTED_TOKENS:

        remaining = (
            NUMBER_OF_SELECTED_TOKENS
            - len(selected_indices)
        )

        print()
        print(
            f"Tokens still to select: {remaining}"
        )

        choice = get_integer_input(
            "Enter token number: ",
            1,
            len(tokens)
        )

        index = choice - 1

        if index in selected_indices:

            print(
                "[!] You already selected this token. "
                "Choose another."
            )

            continue

        selected_indices.append(index)

        token = tokens[index]

        print(
            f"[✓] Selected: #{choice} -> {token}"
        )

    selected_tokens = [
        tokens[index]
        for index in selected_indices
    ]

    print_subsection(
        "YOUR FIVE SELECTED TOKENS"
    )

    for number, token in enumerate(
        selected_tokens,
        start=1
    ):

        print(
            f"{number}. {token}"
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
    Ask the user to select the token they personally consider
    most related to the selected token.

    This represents the human-understanding part of Task 3.
    """

    print()
    print("=" * 78)

    print(
        f"TOKEN: {selected_token}"
    )

    print("=" * 78)

    print()
    print(
        "Choose the token that YOU consider most related "
        "to this token."
    )

    print()
    print(
        "This is your human/semantic judgement."
    )

    print(
        "The random embedding similarity is NOT used to "
        "make this decision."
    )

    print()

    candidates = []

    for index, token in enumerate(tokens):

        if token == selected_token:
            continue

        candidates.append(
            (
                index,
                token,
                int(top_50.iloc[index]["frequency"])
            )
        )

    print(
        f"{'No.':<6}"
        f"{'Token':<30}"
        f"{'Frequency':>12}"
    )

    print("-" * 52)

    for index, token, frequency in candidates:

        clean_token = (
            str(token)
            .replace("\n", "\\n")
            .replace("\r", "\\r")
        )

        print(
            f"{index + 1:<6}"
            f"{clean_token:<30}"
            f"{frequency:>12,}"
        )

    print()

    while True:

        choice = get_integer_input(
            f"Choose the token you consider related to "
            f"'{selected_token}': ",
            1,
            len(tokens)
        )

        chosen_token = tokens[choice - 1]

        if chosen_token == selected_token:

            print(
                "[!] You cannot select the same token."
            )

            continue

        print()
        print(
            f"[✓] Pair selected:"
        )

        print(
            f"    {selected_token}  <->  {chosen_token}"
        )

        return chosen_token


# ============================================================
# TASK 3
# ============================================================

def perform_task_3(
    tokens,
    top_50
):
    """
    Execute Task 3.

    1. Select five tokens.
    2. For every token, select one token that the user
       considers related.
    """

    print_section(
        "TASK 3 - HUMAN TOKEN RELATIONSHIP SELECTION"
    )

    selected_tokens = select_five_tokens(
        tokens,
        top_50
    )

    print()
    print(
        "Now choose the token that you believe is most "
        "related to each selected token."
    )

    print()
    print(
        "The choices will be used in Task 4 to calculate "
        "cosine similarity."
    )

    pairs = []

    for selected_token in selected_tokens:

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

    result_df = pd.DataFrame(pairs)

    result_df.to_csv(
        TASK3_OUTPUT,
        index=False
    )

    print()
    print("=" * 78)
    print("TASK 3 COMPLETE")
    print("=" * 78)

    print()
    print(
        f"Selected token pairs : {len(result_df)}"
    )

    print(
        f"Saved to              : {TASK3_OUTPUT}"
    )

    print()

    for _, row in result_df.iterrows():

        print(
            f"  {row['token_a']:<25}"
            f" <-> "
            f"{row['token_b']}"
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
    """
    Calculate cosine similarity for the five manually
    selected token pairs.
    """

    print_section(
        "TASK 4 - CALCULATING PAIR SIMILARITY"
    )

    if pairs_df is None or pairs_df.empty:

        raise ValueError(
            "No token pairs were selected for Task 4."
        )

    results = []

    print()
    print(
        "Calculating cosine similarity for each selected pair..."
    )

    print()

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

        print(
            f"{token_a:<25}"
            f" <-> "
            f"{token_b:<25}"
            f" : {similarity:.6f}"
        )

    result_df = pd.DataFrame(
        results
    )

    result_df.to_csv(
        TASK4_OUTPUT,
        index=False
    )

    print()
    print(
        "[✓] Task 4 similarity calculation completed."
    )

    print(
        f"Saved to: {TASK4_OUTPUT}"
    )

    return result_df


# ============================================================
# MAIN TASK FUNCTION
# ============================================================

def run_token_similarity():
    """
    Run Tasks 3 and 4 interactively.
    """

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

    print()
    print("=" * 78)
    print("TASKS 3 AND 4 COMPLETED")
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