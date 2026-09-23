from pathlib import Path
import csv
import json
from collections import Counter

import pandas as pd

from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import ByteLevel


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "input"
    / "combined_dataset.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "output"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

TOKENIZER_FILE = (
    OUTPUT_DIR
    / "bpe_tokenizer.json"
)

STATS_FILE = (
    OUTPUT_DIR
    / "subword_tokenizer_statistics.json"
)

VOCAB_FILE = (
    OUTPUT_DIR
    / "subword_vocabulary.json"
)

TOKEN_FREQUENCY_FILE = (
    OUTPUT_DIR
    / "subword_token_frequency.csv"
)


# ============================================================
# CONFIGURATION
# ============================================================

EMBEDDING_DIMENSION = 128

# Maximum vocabulary size requested for BPE.
BPE_VOCAB_SIZE = 10000

SPECIAL_TOKENS = [
    "[PAD]",
    "[UNK]",
    "[CLS]",
    "[SEP]",
    "[MASK]"
]


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():

    print("\n" + "=" * 70)
    print("TASK 1C — SUBWORD TOKENIZER (BPE)")
    print("=" * 70)

    print("\n[1/6] Loading combined dataset...")

    print(
        f"      Input: {INPUT_FILE}"
    )

    if not INPUT_FILE.exists():

        raise FileNotFoundError(
            f"Combined dataset not found:\n"
            f"{INPUT_FILE}"
        )

    df = pd.read_csv(
        INPUT_FILE
    )

    print(
        "[✓] Dataset loaded successfully"
    )

    print(
        f"    Rows    : {len(df)}"
    )

    print(
        f"    Columns : {len(df.columns)}"
    )

    print(
        f"    Available columns: "
        f"{', '.join(df.columns)}"
    )

    return df


# ============================================================
# EXTRACT TEXT DATA
# ============================================================

def extract_source_code(df):

    print(
        "\n[2/6] Extracting source-code data..."
    )

    if "source_code" in df.columns:

        texts = (
            df["source_code"]
            .fillna("")
            .astype(str)
            .tolist()
        )

        print(
            "    Using column: source_code"
        )

    elif "code" in df.columns:

        texts = (
            df["code"]
            .fillna("")
            .astype(str)
            .tolist()
        )

        print(
            "    Using column: code"
        )

    else:

        print(
            "    WARNING: source_code column "
            "not found."
        )

        print(
            "    Falling back to file_path."
        )

        if "file_path" not in df.columns:

            raise ValueError(
                "Neither 'source_code', 'code', "
                "nor 'file_path' exists in the dataset."
            )

        texts = (
            df["file_path"]
            .fillna("")
            .astype(str)
            .tolist()
        )

    # Remove completely empty documents.
    texts = [
        text
        for text in texts
        if text.strip()
    ]

    print(
        "[✓] Source-code records prepared"
    )

    print(
        f"    Documents : {len(texts)}"
    )

    return texts


# ============================================================
# TRAIN BPE TOKENIZER
# ============================================================

def train_bpe_tokenizer(texts):

    print(
        "\n[3/6] Training BPE tokenizer..."
    )

    print(
        f"    Target vocabulary size : "
        f"{BPE_VOCAB_SIZE}"
    )

    print(
        "    Algorithm              : "
        "Byte Pair Encoding (BPE)"
    )

    # Initialize an empty BPE model.
    tokenizer = Tokenizer(
        BPE(
            unk_token="[UNK]"
        )
    )

    # Byte-level pre-tokenization.
    # This is useful for source-code-like text because
    # it can represent unusual characters and whitespace.
    tokenizer.pre_tokenizer = ByteLevel(
        add_prefix_space=False
    )

    trainer = BpeTrainer(

        vocab_size=BPE_VOCAB_SIZE,

        special_tokens=SPECIAL_TOKENS,

        min_frequency=2
    )

    tokenizer.train_from_iterator(
        texts,
        trainer=trainer
    )

    actual_vocab_size = (
        tokenizer.get_vocab_size()
    )

    print(
        "[✓] BPE tokenizer trained"
    )

    print(
        f"    Actual vocabulary size : "
        f"{actual_vocab_size}"
    )

    return tokenizer


# ============================================================
# TOKENIZE DATASET
# ============================================================

def tokenize_texts(
    tokenizer,
    texts
):

    print(
        "\n[4/6] Tokenizing source code "
        "using BPE..."
    )

    sequence_lengths = []

    total_tokens = 0

    # Counter used for Task 2.
    token_counter = Counter()

    for index, text in enumerate(texts):

        encoding = tokenizer.encode(
            text
        )

        tokens = encoding.tokens

        length = len(tokens)

        sequence_lengths.append(
            length
        )

        total_tokens += length

        # Count every BPE token.
        token_counter.update(
            tokens
        )

        # Progress indicator every 100 documents.
        if (
            (index + 1) % 100 == 0
            or index == len(texts) - 1
        ):

            print(
                f"    Processed "
                f"{index + 1}/{len(texts)} "
                f"documents"
            )

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

    print(
        "[✓] BPE tokenization complete"
    )

    print(
        f"    Total tokens          : "
        f"{total_tokens}"
    )

    print(
        f"    Unique tokens observed: "
        f"{len(token_counter)}"
    )

    print(
        f"    Average sequence len : "
        f"{average_sequence_length:.2f}"
    )

    return (
        sequence_lengths,
        total_tokens,
        average_sequence_length,
        token_counter
    )


# ============================================================
# SAVE TOKEN FREQUENCY
# ============================================================

def save_token_frequency(
    token_counter
):

    print(
        "\n[5/6] Saving BPE token frequencies..."
    )

    # Sort tokens by frequency in descending order.
    sorted_tokens = (
        token_counter
        .most_common()
    )

    with open(
        TOKEN_FREQUENCY_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(
            file
        )

        writer.writerow(
            [
                "token",
                "frequency"
            ]
        )

        for token, frequency in sorted_tokens:

            writer.writerow(
                [
                    token,
                    frequency
                ]
            )

    print(
        "[✓] Token frequency dataset saved"
    )

    print(
        f"    File: {TOKEN_FREQUENCY_FILE}"
    )

    print(
        f"    Unique tokens: "
        f"{len(sorted_tokens)}"
    )

    # Show the first few tokens in terminal
    # so the user can visually verify the output.
    print(
        "\n    Top 10 most frequent BPE tokens:"
    )

    for rank, (
        token,
        frequency
    ) in enumerate(
        sorted_tokens[:10],
        start=1
    ):

        print(
            f"      {rank:2d}. "
            f"{repr(token):20s} "
            f"{frequency}"
        )

    return sorted_tokens


# ============================================================
# EMBEDDING STATISTICS
# ============================================================

def calculate_embedding_statistics(
    vocabulary_size
):

    rows = vocabulary_size

    columns = EMBEDDING_DIMENSION

    parameters = (
        rows * columns
    )

    return {

        "embedding_dimension":
            columns,

        "embedding_matrix_rows":
            rows,

        "embedding_matrix_columns":
            columns,

        "embedding_matrix_shape":
            f"{rows} x {columns}",

        "embedding_parameters":
            parameters
    }


# ============================================================
# SAVE TOKENIZER
# ============================================================

def save_tokenizer(
    tokenizer
):

    print(
        "\n[6/6] Saving trained BPE tokenizer..."
    )

    tokenizer.save(
        str(TOKENIZER_FILE)
    )

    print(
        "[✓] BPE tokenizer saved"
    )

    print(
        f"    File: {TOKENIZER_FILE}"
    )


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(
    tokenizer,
    sequence_lengths,
    total_tokens,
    average_sequence_length,
    token_counter
):

    vocabulary_size = (
        tokenizer.get_vocab_size()
    )

    embedding_stats = (
        calculate_embedding_statistics(
            vocabulary_size
        )
    )

    statistics = {

        "tokenizer":
            "subword",

        "algorithm":
            "BPE",

        "dataset":
            "combined_dataset.csv",

        "target_vocabulary_size":
            BPE_VOCAB_SIZE,

        "vocabulary_size":
            vocabulary_size,

        "total_sequences":
            len(sequence_lengths),

        "total_tokens":
            total_tokens,

        "unique_tokens_observed":
            len(token_counter),

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
            embedding_stats,

        "token_frequency_file":
            TOKEN_FREQUENCY_FILE.name
    }

    # --------------------------------------------------------
    # Save statistics
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Save vocabulary
    # --------------------------------------------------------

    vocabulary = (
        tokenizer.get_vocab()
    )

    with open(
        VOCAB_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            vocabulary,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        "\n[✓] Subword tokenizer results saved"
    )

    print(
        f"    Statistics : {STATS_FILE}"
    )

    print(
        f"    Vocabulary : {VOCAB_FILE}"
    )

    print(
        f"    Frequencies : "
        f"{TOKEN_FREQUENCY_FILE}"
    )

    return statistics


# ============================================================
# MAIN PIPELINE
# ============================================================

def run_subword_tokenizer():

    df = load_dataset()

    texts = extract_source_code(
        df
    )

    tokenizer = train_bpe_tokenizer(
        texts
    )

    (
        sequence_lengths,
        total_tokens,
        average_sequence_length,
        token_counter
    ) = tokenize_texts(
        tokenizer,
        texts
    )

    # Save token frequencies before
    # moving to the final output stage.
    save_token_frequency(
        token_counter
    )

    save_tokenizer(
        tokenizer
    )

    statistics = save_results(
        tokenizer,
        sequence_lengths,
        total_tokens,
        average_sequence_length,
        token_counter
    )

    print(
        "\n" + "-" * 70
    )

    print(
        "SUBWORD TOKENIZER SUMMARY"
    )

    print(
        "-" * 70
    )

    print(
        f"Algorithm              : BPE"
    )

    print(
        f"Vocabulary Size        : "
        f"{statistics['vocabulary_size']}"
    )

    print(
        f"Unique Observed Tokens : "
        f"{statistics['unique_tokens_observed']}"
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

    print(
        f"Token Frequency CSV     : "
        f"{TOKEN_FREQUENCY_FILE.name}"
    )

    print(
        "\n[✓] Subword tokenizer "
        "completed successfully."
    )

    return statistics


# ============================================================
# SCRIPT ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run_subword_tokenizer()