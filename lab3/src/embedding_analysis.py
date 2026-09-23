from pathlib import Path
import json
import numpy as np
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

EMBEDDING_DIMENSION = 128
TOP_K_TOKENS = 50
TOP_SIMILAR_PAIRS = 10
TOP_LEAST_SIMILAR_PAIRS = 10


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"

SUBWORD_FREQUENCY_FILE = OUTPUT_DIR / "subword_token_frequency.csv"

EMBEDDING_MATRIX_FILE = OUTPUT_DIR / "random_embedding_matrix.npy"

TOP_50_FILE = OUTPUT_DIR / "top_50_tokens.csv"
MOST_SIMILAR_FILE = OUTPUT_DIR / "top_10_most_similar.csv"
LEAST_SIMILAR_FILE = OUTPUT_DIR / "top_10_least_similar.csv"

EMBEDDING_STATISTICS_FILE = OUTPUT_DIR / "embedding_statistics.json"


# ============================================================
# UTILITY
# ============================================================

def print_section(title):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


# ============================================================
# LOAD TOKEN FREQUENCIES
# ============================================================

def load_token_frequencies():
    print_section("TASK 2 - LOADING SUBWORD TOKEN FREQUENCIES")

    if not SUBWORD_FREQUENCY_FILE.exists():
        raise FileNotFoundError(
            f"Subword frequency file not found:\n"
            f"{SUBWORD_FREQUENCY_FILE}\n\n"
            f"Run the subword tokenizer before running embedding analysis."
        )

    df = pd.read_csv(SUBWORD_FREQUENCY_FILE)

    print(f"Frequency file : {SUBWORD_FREQUENCY_FILE}")
    print(f"Total tokens   : {len(df)}")

    required_columns = {"token", "frequency"}

    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"Frequency CSV must contain columns: {required_columns}"
        )

    df = df.sort_values("frequency", ascending=False).reset_index(drop=True)

    print("[OK] Token frequency data loaded.")

    return df


# ============================================================
# TOP 50 TOKENS
# ============================================================

def get_top_50_tokens(df):
    print_section("FINDING TOP 50 MOST FREQUENT TOKENS")

    top_50 = df.head(TOP_K_TOKENS).copy()

    top_50.to_csv(TOP_50_FILE, index=False)

    print(f"Vocabulary size : {len(df)}")
    print(f"Selecting       : {len(top_50)} tokens")
    print(f"Saved to        : {TOP_50_FILE}")

    print()
    print("Top 10 tokens:")
    print("-" * 50)

    for _, row in top_50.head(10).iterrows():
        print(f"{str(row['token']):25} {int(row['frequency'])}")

    return top_50


# ============================================================
# RANDOM EMBEDDING MATRIX
# ============================================================

def create_random_embeddings(top_50):
    print_section("INITIALIZING RANDOM EMBEDDING MATRIX")

    tokens = top_50["token"].astype(str).tolist()

    print(f"Number of tokens : {len(tokens)}")
    print(f"Embedding size   : {EMBEDDING_DIMENSION}")

    print(
        f"\nCreating matrix of shape "
        f"({len(tokens)}, {EMBEDDING_DIMENSION})"
    )

    # Fixed seed makes the experiment reproducible.
    np.random.seed(42)

    embedding_matrix = np.random.normal(
        loc=0.0,
        scale=0.1,
        size=(len(tokens), EMBEDDING_DIMENSION)
    )

    np.save(EMBEDDING_MATRIX_FILE, embedding_matrix)

    print("[OK] Random embedding matrix created.")
    print(f"Shape            : {embedding_matrix.shape}")
    print(f"Saved to         : {EMBEDDING_MATRIX_FILE}")

    return tokens, embedding_matrix


# ============================================================
# COSINE SIMILARITY
# ============================================================

def cosine_similarity_matrix(matrix):
    """
    Calculate pairwise cosine similarity.

    similarity(A, B) =
        A . B
        -------
        |A||B|
    """

    norms = np.linalg.norm(matrix, axis=1, keepdims=True)

    # Prevent division by zero.
    norms[norms == 0] = 1e-12

    normalized = matrix / norms

    return np.dot(normalized, normalized.T)


# ============================================================
# SIMILARITY ANALYSIS
# ============================================================

def analyze_similarity(tokens, embedding_matrix):
    print_section("CALCULATING EMBEDDING SIMILARITY")

    print("Calculating pairwise cosine similarity...")
    print(
        f"Comparisons possible: "
        f"{len(tokens) * (len(tokens) - 1) // 2}"
    )

    similarity_matrix = cosine_similarity_matrix(embedding_matrix)

    print("[OK] Similarity matrix generated.")
    print(f"Matrix shape: {similarity_matrix.shape}")

    pairs = []

    for i in range(len(tokens)):
        for j in range(i + 1, len(tokens)):

            pairs.append({
                "token_1": tokens[i],
                "token_2": tokens[j],
                "similarity": float(similarity_matrix[i, j])
            })

    similarity_df = pd.DataFrame(pairs)

    most_similar = (
        similarity_df
        .sort_values("similarity", ascending=False)
        .head(TOP_SIMILAR_PAIRS)
        .reset_index(drop=True)
    )

    least_similar = (
        similarity_df
        .sort_values("similarity", ascending=True)
        .head(TOP_LEAST_SIMILAR_PAIRS)
        .reset_index(drop=True)
    )

    most_similar.to_csv(MOST_SIMILAR_FILE, index=False)
    least_similar.to_csv(LEAST_SIMILAR_FILE, index=False)

    print()
    print("Top 10 MOST similar token pairs:")
    print("-" * 70)

    for _, row in most_similar.iterrows():
        print(
            f"{str(row['token_1']):20} "
            f"<-> "
            f"{str(row['token_2']):20} "
            f"{row['similarity']:.6f}"
        )

    print()
    print("Top 10 LEAST similar token pairs:")
    print("-" * 70)

    for _, row in least_similar.iterrows():
        print(
            f"{str(row['token_1']):20} "
            f"<-> "
            f"{str(row['token_2']):20} "
            f"{row['similarity']:.6f}"
        )

    return similarity_matrix, most_similar, least_similar


# ============================================================
# SAVE STATISTICS
# ============================================================

def save_embedding_statistics(
    tokens,
    embedding_matrix,
    most_similar,
    least_similar
):
    print_section("SAVING EMBEDDING ANALYSIS")

    statistics = {
        "embedding_dimension": EMBEDDING_DIMENSION,
        "number_of_tokens": len(tokens),
        "embedding_matrix_shape": list(embedding_matrix.shape),
        "random_seed": 42,
        "similarity_metric": "cosine_similarity",
        "top_similar_pairs": most_similar.to_dict(orient="records"),
        "top_least_similar_pairs": least_similar.to_dict(orient="records")
    }

    with open(
        EMBEDDING_STATISTICS_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(statistics, file, indent=4)

    print(f"[OK] Statistics saved to:")
    print(EMBEDDING_STATISTICS_FILE)


# ============================================================
# MAIN TASK FUNCTION
# ============================================================

def run_embedding_analysis():

    df = load_token_frequencies()

    top_50 = get_top_50_tokens(df)

    tokens, embedding_matrix = create_random_embeddings(top_50)

    similarity_matrix, most_similar, least_similar = (
        analyze_similarity(tokens, embedding_matrix)
    )

    save_embedding_statistics(
        tokens,
        embedding_matrix,
        most_similar,
        least_similar
    )

    print()
    print("[✓] TASK 2 COMPLETED")

    return {
        "tokens": tokens,
        "embedding_matrix": embedding_matrix,
        "similarity_matrix": similarity_matrix,
        "most_similar": most_similar,
        "least_similar": least_similar
    }


if __name__ == "__main__":
    run_embedding_analysis()