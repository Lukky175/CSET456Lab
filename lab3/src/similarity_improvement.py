from pathlib import Path
import json
import numpy as np
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"

TOP_50_FILE = OUTPUT_DIR / "top_50_tokens.csv"
EMBEDDING_MATRIX_FILE = OUTPUT_DIR / "random_embedding_matrix.npy"

IMPROVED_EMBEDDING_FILE = (
    OUTPUT_DIR / "improved_embedding_matrix.npy"
)

IMPROVED_SIMILARITY_FILE = (
    OUTPUT_DIR / "improved_similarity_results.csv"
)

IMPROVEMENT_STATISTICS_FILE = (
    OUTPUT_DIR / "similarity_improvement_statistics.json"
)

# How strongly related embeddings are moved toward each other.
LEARNING_RATE = 0.05

# Minimum shared-character ratio required before modifying
# the embeddings.
MIN_CHARACTER_OVERLAP = 0.40


# ============================================================
# UTILITY
# ============================================================

def print_section(title):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def cosine_similarity(vector_a, vector_b):

    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(
        np.dot(vector_a, vector_b)
        / (norm_a * norm_b)
    )


# ============================================================
# CHARACTER OVERLAP
# ============================================================

def character_overlap(token_a, token_b):
    """
    Calculate a simple character-set overlap.

    Example:

    token_a = "connect"
    token_b = "connected"

    The shared character set is compared against the smaller
    token's character set.
    """

    chars_a = set(str(token_a).lower())
    chars_b = set(str(token_b).lower())

    if not chars_a or not chars_b:
        return 0.0

    common = chars_a.intersection(chars_b)

    denominator = min(
        len(chars_a),
        len(chars_b)
    )

    return len(common) / denominator


# ============================================================
# NAIVE IMPROVEMENT ALGORITHM
# ============================================================

def improve_embeddings(tokens, embeddings):

    print_section("TASK 5 - NAIVE EMBEDDING IMPROVEMENT")

    print("Naive algorithm:")
    print()
    print("1. Compare every pair of top-50 tokens.")
    print("2. Calculate character overlap.")
    print(
        "3. If overlap >= "
        f"{MIN_CHARACTER_OVERLAP}, treat them as related."
    )
    print(
        "4. Move their embeddings slightly toward each other."
    )
    print(
        "5. Repeat the similarity experiment."
    )

    improved = embeddings.copy()

    related_pairs = []

    for i in range(len(tokens)):

        for j in range(i + 1, len(tokens)):

            overlap = character_overlap(
                tokens[i],
                tokens[j]
            )

            if overlap >= MIN_CHARACTER_OVERLAP:

                vector_i = improved[i].copy()
                vector_j = improved[j].copy()

                # Move each vector slightly toward the other.
                improved[i] = (
                    (1 - LEARNING_RATE) * vector_i
                    + LEARNING_RATE * vector_j
                )

                improved[j] = (
                    (1 - LEARNING_RATE) * vector_j
                    + LEARNING_RATE * vector_i
                )

                related_pairs.append(
                    {
                        "token_1": tokens[i],
                        "token_2": tokens[j],
                        "character_overlap": overlap
                    }
                )

    print()
    print(
        f"Related token pairs found : "
        f"{len(related_pairs)}"
    )

    np.save(
        IMPROVED_EMBEDDING_FILE,
        improved
    )

    print(
        f"[OK] Improved embedding matrix saved to:"
    )
    print( IMPROVED_EMBEDDING_FILE )

    return improved, related_pairs


# ============================================================
# REPEAT SIMILARITY EXPERIMENT
# ============================================================

def repeat_similarity_experiment(
    tokens,
    original_embeddings,
    improved_embeddings
):

    print_section("TASK 6 - REPEATING SIMILARITY EXPERIMENT")

    results = []

    for i in range(len(tokens)):

        for j in range(i + 1, len(tokens)):

            original_similarity = cosine_similarity(
                original_embeddings[i],
                original_embeddings[j]
            )

            improved_similarity = cosine_similarity(
                improved_embeddings[i],
                improved_embeddings[j]
            )

            results.append(
                {
                    "token_1": tokens[i],
                    "token_2": tokens[j],
                    "original_similarity": original_similarity,
                    "improved_similarity": improved_similarity,
                    "change": (
                        improved_similarity
                        - original_similarity
                    )
                }
            )

    results_df = pd.DataFrame(results)

    results_df.to_csv(
        IMPROVED_SIMILARITY_FILE,
        index=False
    )

    print(
        f"Total token pairs analyzed : "
        f"{len(results_df)}"
    )

    print()
    print("Largest similarity improvements:")
    print("-" * 70)

    top_improvements = (
        results_df
        .sort_values(
            "change",
            ascending=False
        )
        .head(10)
    )

    for _, row in top_improvements.iterrows():

        print(
            f"{row['token_1']:20}"
            f" <-> "
            f"{row['token_2']:20}"
            f" | "
            f"{row['original_similarity']:.4f}"
            f" -> "
            f"{row['improved_similarity']:.4f}"
        )

    return results_df


# ============================================================
# SAVE OBSERVATIONS / STATISTICS
# ============================================================

def save_improvement_statistics(
    related_pairs,
    results_df
):

    print_section("SAVING TASK 5/6 RESULTS")

    average_before = (
        results_df["original_similarity"].mean()
    )

    average_after = (
        results_df["improved_similarity"].mean()
    )

    average_change = (
        results_df["change"].mean()
    )

    statistics = {
        "algorithm": {
            "type": "naive character-overlap embedding adjustment",
            "learning_rate": LEARNING_RATE,
            "minimum_character_overlap": MIN_CHARACTER_OVERLAP
        },
        "related_pairs_detected": len(related_pairs),
        "total_pairs_analyzed": len(results_df),
        "average_similarity_before": float(
            average_before
        ),
        "average_similarity_after": float(
            average_after
        ),
        "average_similarity_change": float(
            average_change
        )
    }

    with open(
        IMPROVEMENT_STATISTICS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            statistics,
            file,
            indent=4
        )

    print(
        f"Average similarity BEFORE : "
        f"{average_before:.6f}"
    )

    print(
        f"Average similarity AFTER  : "
        f"{average_after:.6f}"
    )

    print(
        f"Average change            : "
        f"{average_change:.6f}"
    )

    print()
    print(
        f"[OK] Statistics saved to:"
    )
    print(
        IMPROVEMENT_STATISTICS_FILE
    )


# ============================================================
# MAIN TASK FUNCTION
# ============================================================

def run_similarity_improvement():

    print_section(
        "TASK 5 & 6 - SIMILARITY IMPROVEMENT EXPERIMENT"
    )

    if not TOP_50_FILE.exists():

        raise FileNotFoundError(
            "top_50_tokens.csv not found. "
            "Run Task 2 first."
        )

    if not EMBEDDING_MATRIX_FILE.exists():

        raise FileNotFoundError(
            "random_embedding_matrix.npy not found. "
            "Run Task 2 first."
        )

    top_50 = pd.read_csv(
        TOP_50_FILE
    )

    tokens = (
        top_50["token"]
        .astype(str)
        .tolist()
    )

    original_embeddings = np.load(
        EMBEDDING_MATRIX_FILE
    )

    print(
        f"Tokens loaded       : {len(tokens)}"
    )

    print(
        f"Embedding dimensions: "
        f"{original_embeddings.shape}"
    )

    improved_embeddings, related_pairs = (
        improve_embeddings(
            tokens,
            original_embeddings
        )
    )

    results_df = repeat_similarity_experiment(
        tokens,
        original_embeddings,
        improved_embeddings
    )

    save_improvement_statistics(
        related_pairs,
        results_df
    )

    print()
    print("[✓] TASKS 5 AND 6 COMPLETED")

    return results_df


if __name__ == "__main__":
    run_similarity_improvement()