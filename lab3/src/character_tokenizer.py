from pathlib import Path
from collections import Counter
import json
import pandas as pd


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "input" / "combined_dataset.csv"

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STATS_FILE = OUTPUT_DIR / "character_tokenizer_statistics.json"
VOCAB_FILE = OUTPUT_DIR / "character_vocabulary.json"


# ============================================================
# CONFIGURATION
# ============================================================

# Embedding dimension required for Task 1 analysis.
EMBEDDING_DIMENSION = 128


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():
    """Load the combined Lab-2 dataset."""

    print("\n" + "=" * 70)
    print("TASK 1A — CHARACTER TOKENIZER")
    print("=" * 70)

    print("\n[1/5] Loading combined dataset...")
    print(f"      Input: {INPUT_FILE}")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Combined dataset not found:\n{INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    print("[✓] Dataset loaded successfully")
    print(f"    Rows    : {len(df)}")
    print(f"    Columns : {len(df.columns)}")

    return df


# ============================================================
# EXTRACT SOURCE CODE
# ============================================================

def extract_source_code(df):
    """
    Extract source-code text.

    The Lab-2 combined dataset is expected to contain a
    source_code column. If it does not exist, the function
    falls back to file_path so the tokenizer can still run.
    """

    print("\n[2/5] Extracting source-code data...")

    if "source_code" in df.columns:
        texts = df["source_code"].fillna("").astype(str)

        print("    Using column: source_code")

    elif "code" in df.columns:
        texts = df["code"].fillna("").astype(str)

        print("    Using column: code")

    else:
        print(
            "    WARNING: source_code column not found."
        )
        print(
            "    Falling back to file_path."
        )

        texts = df["file_path"].fillna("").astype(str)

    texts = texts.tolist()

    non_empty = sum(1 for text in texts if text.strip())

    print(f"[✓] Source-code records prepared")
    print(f"    Total records : {len(texts)}")
    print(f"    Non-empty     : {non_empty}")

    return texts


# ============================================================
# BUILD CHARACTER VOCABULARY
# ============================================================

def build_character_vocabulary(texts):
    """Build a character vocabulary from the dataset."""

    print("\n[3/5] Building character vocabulary...")

    counter = Counter()

    for text in texts:
        counter.update(text)

    # Sort characters by frequency.
    # Most frequent characters appear first.
    vocabulary = {
        token: index
        for index, (token, _) in enumerate(
            counter.most_common(),
            start=1
        )
    }

    print("[✓] Character vocabulary created")
    print(f"    Vocabulary size : {len(vocabulary)}")

    return vocabulary, counter


# ============================================================
# TOKENIZE
# ============================================================

def tokenize_texts(texts, vocabulary):
    """Convert characters into integer token IDs."""

    print("\n[4/5] Tokenizing source code...")

    token_sequences = []

    unknown_token_id = 0

    for text in texts:

        sequence = [
            vocabulary.get(character, unknown_token_id)
            for character in text
        ]

        token_sequences.append(sequence)

    sequence_lengths = [
        len(sequence)
        for sequence in token_sequences
    ]

    non_empty_lengths = [
        length
        for length in sequence_lengths
        if length > 0
    ]

    if non_empty_lengths:
        average_sequence_length = (
            sum(non_empty_lengths)
            / len(non_empty_lengths)
        )
    else:
        average_sequence_length = 0

    total_tokens = sum(sequence_lengths)

    print("[✓] Tokenization complete")
    print(f"    Total tokens           : {total_tokens}")
    print(
        f"    Average sequence len  : "
        f"{average_sequence_length:.2f}"
    )

    return (
        token_sequences,
        sequence_lengths,
        average_sequence_length
    )


# ============================================================
# CALCULATE EMBEDDING MATRIX
# ============================================================

def calculate_embedding_statistics(vocabulary_size):
    """
    Calculate the size of a hypothetical embedding matrix.

    Embedding matrix:
        vocabulary_size × embedding_dimension
    """

    matrix_rows = vocabulary_size
    matrix_columns = EMBEDDING_DIMENSION

    total_parameters = (
        matrix_rows * matrix_columns
    )

    matrix_size = (
        f"{matrix_rows} x {matrix_columns}"
    )

    return {
        "embedding_dimension": matrix_columns,
        "embedding_matrix_rows": matrix_rows,
        "embedding_matrix_columns": matrix_columns,
        "embedding_matrix_shape": matrix_size,
        "embedding_parameters": total_parameters
    }


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(
    vocabulary,
    counter,
    sequence_lengths,
    average_sequence_length
):
    """Save vocabulary and statistics."""

    vocabulary_size = len(vocabulary)

    embedding_stats = calculate_embedding_statistics(
        vocabulary_size
    )

    statistics = {
        "tokenizer": "character",
        "dataset": "combined_dataset.csv",
        "vocabulary_size": vocabulary_size,
        "total_sequences": len(sequence_lengths),
        "total_tokens": sum(sequence_lengths),
        "average_sequence_length": round(
            average_sequence_length,
            4
        ),
        "min_sequence_length": (
            min(sequence_lengths)
            if sequence_lengths
            else 0
        ),
        "max_sequence_length": (
            max(sequence_lengths)
            if sequence_lengths
            else 0
        ),
        "embedding": embedding_stats
    }

    # Save statistics
    with open(
        STATS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            statistics,
            file,
            indent=4,
            ensure_ascii=False
        )

    # Save vocabulary
    vocabulary_output = {
        "token_to_id": vocabulary,
        "token_frequency": dict(counter)
    }

    with open(
        VOCAB_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            vocabulary_output,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n[✓] Character tokenizer results saved")
    print(f"    Statistics : {STATS_FILE}")
    print(f"    Vocabulary : {VOCAB_FILE}")

    return statistics


# ============================================================
# MAIN FUNCTION
# ============================================================

def run_character_tokenizer():
    """Run the complete character-tokenization pipeline."""

    df = load_dataset()

    texts = extract_source_code(df)

    vocabulary, counter = build_character_vocabulary(
        texts
    )

    (
        token_sequences,
        sequence_lengths,
        average_sequence_length
    ) = tokenize_texts(
        texts,
        vocabulary
    )

    statistics = save_results(
        vocabulary,
        counter,
        sequence_lengths,
        average_sequence_length
    )

    print("\n" + "-" * 70)
    print("CHARACTER TOKENIZER SUMMARY")
    print("-" * 70)

    print(
        f"Vocabulary Size        : "
        f"{statistics['vocabulary_size']}"
    )

    print(
        f"Average Sequence Length: "
        f"{statistics['average_sequence_length']}"
    )

    print(
        f"Embedding Dimension    : "
        f"{EMBEDDING_DIMENSION}"
    )

    print(
        f"Embedding Matrix       : "
        f"{statistics['embedding']['embedding_matrix_shape']}"
    )

    print(
        f"Embedding Parameters   : "
        f"{statistics['embedding']['embedding_parameters']}"
    )

    print("\n[✓] Character tokenizer completed successfully.")

    return statistics


if __name__ == "__main__":
    run_character_tokenizer()