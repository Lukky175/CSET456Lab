from pathlib import Path
from collections import Counter
import json
import re

import pandas as pd


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "input" / "combined_dataset.csv"

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STATS_FILE = OUTPUT_DIR / "word_tokenizer_statistics.json"
VOCAB_FILE = OUTPUT_DIR / "word_vocabulary.json"


# ============================================================
# CONFIGURATION
# ============================================================

EMBEDDING_DIMENSION = 128


# ============================================================
# WORD TOKENIZER
# ============================================================

def tokenize_code(text):
    """
    Tokenize source code into word-level tokens.

    The pattern preserves:
    - identifiers
    - numbers
    - common operators
    - punctuation
    - symbols

    Examples:

    def calculate_sum(a, b):

    becomes approximately:

    def
    calculate_sum
    (
    a
    ,
    b
    )
    :
    """

    pattern = r"""
        [A-Za-z_][A-Za-z0-9_]*
        |
        \d+(?:\.\d+)?
        |
        ==|!=|<=|>=|->|=>|::|&&|\|\|
        |
        [^\s]
    """

    return re.findall(
        pattern,
        text,
        flags=re.VERBOSE
    )


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():

    print("\n" + "=" * 70)
    print("TASK 1B — WORD TOKENIZER")
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

    print("\n[2/5] Extracting source-code data...")

    if "source_code" in df.columns:

        texts = (
            df["source_code"]
            .fillna("")
            .astype(str)
            .tolist()
        )

        print("    Using column: source_code")

    elif "code" in df.columns:

        texts = (
            df["code"]
            .fillna("")
            .astype(str)
            .tolist()
        )

        print("    Using column: code")

    else:

        print(
            "    WARNING: source_code column not found."
        )

        print(
            "    Falling back to file_path."
        )

        texts = (
            df["file_path"]
            .fillna("")
            .astype(str)
            .tolist()
        )

    non_empty = sum(
        1
        for text in texts
        if text.strip()
    )

    print("[✓] Source-code records prepared")
    print(f"    Total records : {len(texts)}")
    print(f"    Non-empty     : {non_empty}")

    return texts


# ============================================================
# BUILD VOCABULARY
# ============================================================

def build_word_vocabulary(texts):

    print("\n[3/5] Building word vocabulary...")

    counter = Counter()

    tokenized_documents = []

    for text in texts:

        tokens = tokenize_code(text)

        tokenized_documents.append(tokens)

        counter.update(tokens)

    vocabulary = {
        token: index
        for index, (token, _) in enumerate(
            counter.most_common(),
            start=1
        )
    }

    print("[✓] Word vocabulary created")
    print(
        f"    Vocabulary size : "
        f"{len(vocabulary)}"
    )

    return (
        vocabulary,
        counter,
        tokenized_documents
    )


# ============================================================
# CALCULATE SEQUENCE STATISTICS
# ============================================================

def calculate_sequence_statistics(
    tokenized_documents
):

    print("\n[4/5] Calculating sequence statistics...")

    sequence_lengths = [
        len(tokens)
        for tokens in tokenized_documents
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

    print("[✓] Sequence statistics calculated")

    print(
        f"    Total tokens          : "
        f"{total_tokens}"
    )

    print(
        f"    Average sequence len : "
        f"{average_sequence_length:.2f}"
    )

    return (
        sequence_lengths,
        average_sequence_length
    )


# ============================================================
# EMBEDDING STATISTICS
# ============================================================

def calculate_embedding_statistics(
    vocabulary_size
):

    rows = vocabulary_size
    columns = EMBEDDING_DIMENSION

    parameters = rows * columns

    return {
        "embedding_dimension": columns,
        "embedding_matrix_rows": rows,
        "embedding_matrix_columns": columns,
        "embedding_matrix_shape": (
            f"{rows} x {columns}"
        ),
        "embedding_parameters": parameters
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

    vocabulary_size = len(vocabulary)

    embedding_stats = (
        calculate_embedding_statistics(
            vocabulary_size
        )
    )

    statistics = {

        "tokenizer": "word",

        "dataset": (
            "combined_dataset.csv"
        ),

        "vocabulary_size":
            vocabulary_size,

        "total_sequences":
            len(sequence_lengths),

        "total_tokens":
            sum(sequence_lengths),

        "average_sequence_length":
            round(
                average_sequence_length,
                4
            ),

        "min_sequence_length":
            (
                min(sequence_lengths)
                if sequence_lengths
                else 0
            ),

        "max_sequence_length":
            (
                max(sequence_lengths)
                if sequence_lengths
                else 0
            ),

        "embedding":
            embedding_stats
    }

    with open(
        STATS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            statistics,
            file,
            indent=4
        )

    vocabulary_output = {

        "token_to_id":
            vocabulary,

        "token_frequency":
            dict(counter)
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

    print("\n[✓] Word tokenizer results saved")

    print(
        f"    Statistics : {STATS_FILE}"
    )

    print(
        f"    Vocabulary : {VOCAB_FILE}"
    )

    return statistics


# ============================================================
# MAIN PIPELINE
# ============================================================

def run_word_tokenizer():

    df = load_dataset()

    texts = extract_source_code(df)

    (
        vocabulary,
        counter,
        tokenized_documents
    ) = build_word_vocabulary(
        texts
    )

    (
        sequence_lengths,
        average_sequence_length
    ) = calculate_sequence_statistics(
        tokenized_documents
    )

    statistics = save_results(
        vocabulary,
        counter,
        sequence_lengths,
        average_sequence_length
    )

    print("\n" + "-" * 70)
    print("WORD TOKENIZER SUMMARY")
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

    print("\n[✓] Word tokenizer completed successfully.")

    return statistics


if __name__ == "__main__":
    run_word_tokenizer()