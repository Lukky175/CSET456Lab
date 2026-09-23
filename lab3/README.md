# CSET456 --- Special Topics in DevOps

## Lab 3 --- Software Repository Tokenization and Embedding Analysis

------------------------------------------------------------------------

## 1. Lab Overview

Lab 3 takes the software-engineering data prepared in **Lab 2** and
explores how source-code/repository data can be represented for machine
learning.

The lab implements three tokenization strategies:

1.  Character-level tokenization
2.  Word-level tokenization
3.  Subword-level tokenization using **BPE (Byte Pair Encoding)**

The representations are compared using:

-   Vocabulary size
-   Average sequence length
-   Embedding dimension
-   Embedding matrix size
-   Embedding parameter count

The BPE/subword representation is then used for:

-   Random embedding initialization
-   Top-50 token analysis
-   Cosine similarity analysis
-   Human-selected token relationships
-   Naive similarity improvement
-   Before/after comparison

The overall flow is:


Lab 2 dataset
     ↓
Tokenization
     ↓
Numerical representation
     ↓
Embedding analysis
     ↓
Similarity analysis
     ↓
Naive improvement
     ↓
Before/after comparison


------------------------------------------------------------------------

# 2. Relationship with Previous Labs


LAB 1
Repository Acquisition / Mining
        │
        ▼
Repository Data
        │
        ▼
LAB 2
Data Preparation + Integration
        │
        ▼
combined_dataset.csv
        │
        ▼
LAB 3
Tokenization + Embedding Analysis
        │
        ▼
ML-ready representations


  -----------------------------------------------------------------------
  Lab                     Main Focus              Role in Pipeline
  ----------------------- ----------------------- -----------------------
  Lab 1                   Repository acquisition  Data acquisition
                          and mining              

  Lab 2                   Data cleaning,          Data preparation
                          preparation and         
                          integration             

  Lab 3                   Tokenization and        ML preprocessing and
                          embedding experiments   representation
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 3. How Lab 3 Relates to MLOps

Lab 1 corresponds mainly to **data acquisition and repository mining**.

Lab 2 corresponds to **data preparation and integration**.

Lab 3 moves toward **ML preprocessing and representation learning**.

Tokenization converts raw software data into discrete units. Embeddings
then convert those units into numerical vectors that can be consumed by
downstream machine-learning models.

Therefore:


Data Acquisition
      ↓
Data Preparation
      ↓
Tokenization
      ↓
Numerical Representation
      ↓
Embedding Analysis
      ↓
Similarity Analysis
      ↓
Downstream ML Model


This makes Lab 3 an important preprocessing stage in an ML/MLOps
pipeline.

------------------------------------------------------------------------

# 4. Input Dataset

The main input is:


lab3/data/input/combined_dataset.csv


The current dataset contains fields such as:


repository
file_path
language
extension
loc
size_bytes
change_count
history_present


### Source-code extraction

The tokenizer modules first look for a:


source_code


column.

If it is unavailable, they fall back to:


file_path


The current run therefore reports:


WARNING: source_code column not found.
Falling back to file_path.


> **Important:** the current experiment is therefore operating on
> file-path text rather than the actual contents of source files. This
> should be mentioned when interpreting the results. For a true
> source-code tokenization experiment, the dataset should contain the
> actual source code in a `source_code` field.

------------------------------------------------------------------------

# 5. Project Architecture


                         ┌───────────────────────┐
                         │       LAB 2           │
                         │ Data Preparation      │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │ combined_dataset.csv  │
                         └───────────┬───────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
                    ▼                ▼                ▼
          ┌────────────────┐ ┌───────────────┐ ┌─────────────────┐
          │ Character      │ │ Word          │ │ Subword / BPE   │
          │ Tokenizer      │ │ Tokenizer     │ │ Tokenizer       │
          └───────┬────────┘ └───────┬───────┘ └────────┬────────┘
                  │                  │                  │
                  ▼                  ▼                  ▼
             Vocabulary         Vocabulary         BPE Vocabulary
             Statistics         Statistics         + Statistics
                                                         │
                                                         ▼
                                              ┌────────────────────┐
                                              │ Embedding Analysis │
                                              └─────────┬──────────┘
                                                        │
                                                        ▼
                                              ┌────────────────────┐
                                              │ Random Embeddings  │
                                              │ Top 50 Tokens      │
                                              │ Cosine Similarity  │
                                              └─────────┬──────────┘
                                                        │
                                                        ▼
                                              ┌────────────────────┐
                                              │ Tasks 3 & 4        │
                                              │ Human Selection    │
                                              │ Pair Similarity    │
                                              └─────────┬──────────┘
                                                        │
                                                        ▼
                                              ┌────────────────────┐
                                              │ Tasks 5 & 6        │
                                              │ Naive Improvement  │
                                              │ Before / After     │
                                              └────────────────────┘


------------------------------------------------------------------------

# 6. Complete Lab Pipeline


              Lab 2
                │  
                ▼
        combined_dataset.csv
                │
                ▼
┌───────────────────────────────┐
│ Task 1: Tokenization          │
│                               │
│ Character tokenizer           │
│ Word tokenizer                │
│ BPE subword tokenizer         │
│                               │
│ Analyze:                      │
│ • Vocabulary size             │
│ • Average sequence length     │
│ • Embedding matrix size       │
└───────────────┬───────────────┘
                │
                ▼
          BPE Tokenizer
                │
                ▼
┌───────────────────────────────┐
│ Task 2: Embedding Analysis    │
│                               │
│ • Top 50 frequent tokens      │
│ • Random embedding matrix     │
│ • Cosine similarity           │
│ • Top 10 similar pairs        │
│ • Top 10 least similar pairs  │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│ Task 3: Human Selection       │
│                               │
│ • Select 5 tokens             │
│ • Select a related token      │
│   for each                     │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│ Task 4: Pair Similarity       │
│                               │
│ Calculate cosine similarity   │
│ for the 5 selected pairs      │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│ Task 5: Naive Improvement     │
│                               │
│ • Character overlap           │
│ • Identify related tokens     │
│ • Move embeddings closer      │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│ Task 6: Re-experiment         │
│                               │
│ • Recalculate similarities    │
│ • Compare before vs after     │
└───────────────────────────────┘


------------------------------------------------------------------------

# 7. Folder Structure


lab3/
│
├── data/
│   └── input/
│       └── combined_dataset.csv
│
├── src/
│   ├── character_tokenizer.py
│   ├── word_tokenizer.py
│   ├── subword_tokenizer.py
│   ├── embedding_analysis.py
│   ├── token_similarity.py
│   ├── similarity_improvement.py
│   └── main.py
│
├── output/
│   ├── character_tokenizer_statistics.json
│   ├── character_vocabulary.json
│   ├── word_tokenizer_statistics.json
│   ├── word_vocabulary.json
│   ├── subword_tokenizer_statistics.json
│   ├── subword_vocabulary.json
│   ├── subword_token_frequency.csv
│   ├── bpe_tokenizer.json
│   ├── top_50_tokens.csv
│   ├── random_embedding_matrix.npy
│   ├── embedding_statistics.json
│   ├── top_10_most_similar.csv
│   ├── top_10_least_similar.csv
│   ├── task3_selected_tokens.csv
│   ├── task4_pair_similarity.csv
│   ├── improved_embedding_matrix.npy
│   ├── improved_similarity_results.csv
│   └── similarity_improvement_statistics.json
│
├── requirements.txt
└── README.md

------------------------------------------------------------------------

# 8. Task 1 --- Tokenization

## 8.1 Character-Level Tokenization

File:

character_tokenizer.py

The character tokenizer treats individual characters as tokens.

Conceptually:


test.py
  ↓
t e s t . p y


It calculates:

-   Vocabulary size
-   Total tokens
-   Average sequence length
-   Embedding dimension
-   Embedding matrix size
-   Embedding parameters

Character tokenization normally gives a small vocabulary but longer
sequences.

------------------------------------------------------------------------

## 8.2 Word-Level Tokenization

File:


word_tokenizer.py


The word tokenizer splits text into word-like units and builds a
vocabulary.

It calculates:


Vocabulary Size
Average Sequence Length
Embedding Dimension
Embedding Matrix Size
Embedding Parameters


Compared with character tokenization, word tokenization normally
produces a larger vocabulary and shorter sequences.

------------------------------------------------------------------------

## 8.3 Subword-Level Tokenization

File:


subword_tokenizer.py


The subword tokenizer uses **BPE (Byte Pair Encoding)**.

It:

1.  Loads the dataset.
2.  Extracts the text.
3.  Trains a BPE tokenizer.
4.  Tokenizes the records.
5.  Calculates vocabulary and sequence statistics.
6.  Saves token frequencies.
7.  Saves the trained tokenizer.

------------------------------------------------------------------------

# 9. What is BPE?

**Byte Pair Encoding (BPE)** is a subword tokenization method.

It starts with small units and repeatedly merges frequently occurring
pairs.

Conceptually:


Characters
    ↓
Count frequent pairs
    ↓
Merge frequent pairs
    ↓
Larger subword units
    ↓
BPE vocabulary


This allows the tokenizer to represent common terms as larger units
while still representing uncommon terms using smaller pieces.

For software data, subwords can be useful for:

-   Identifiers
-   File names
-   Library names
-   Abbreviations
-   Code fragments
-   Rare terms

------------------------------------------------------------------------

# 10. Tokenization Statistics

For each tokenizer:

### Vocabulary Size


Number of unique tokens


### Average Sequence Length


Average number of tokens per record


### Embedding Matrix

If:


V = vocabulary size
D = embedding dimension


then:


Embedding Matrix = V × D


### Embedding Parameters


Embedding Parameters = V × D


This experiment uses:


Embedding Dimension = 128


------------------------------------------------------------------------

# 11. Task 2 --- Random Embedding Analysis

File:


embedding_analysis.py


The pipeline is:


BPE token frequencies
        ↓
Top 50 tokens
        ↓
Random 50 × 128 embedding matrix
        ↓
Pairwise cosine similarity
        ↓
Top 10 most similar
Top 10 least similar


The top-50 tokens are saved to:


output/top_50_tokens.csv


------------------------------------------------------------------------

# 12. Random Embeddings

The experiment creates:


Number of tokens = 50
Embedding dimension = 128


Therefore:


Embedding matrix = 50 × 128


The random matrix uses:


Random seed = 42


This makes the experiment reproducible.

Saved as:


random_embedding_matrix.npy


> The vectors are random. Their initial cosine similarities should
> therefore not be interpreted as learned semantic relationships.

------------------------------------------------------------------------

# 13. Cosine Similarity

Cosine similarity measures the angle between two vectors.


                 A · B
cosine(A,B) = -----------
               ||A|| ||B||


Interpretation:


-1  → opposite direction
 0  → orthogonal
+1  → same direction


For 50 tokens:


50 × 49 / 2 = 1225


pairwise comparisons are possible.

The experiment analyzes all 1225 pairs.

------------------------------------------------------------------------

# 14. Task 2 Output Files


top_50_tokens.csv
random_embedding_matrix.npy
embedding_statistics.json
top_10_most_similar.csv
top_10_least_similar.csv


------------------------------------------------------------------------

# 15. Task 3 --- Human Token Relationship Selection

File:


token_similarity.py


Task 3 is interactive.

The complete top-50 token table is shown before selection:


No.   Token                         Frequency
------------------------------------------------
1     _                               6,355
2     /                               5,356
3     py                              2,957
...
50    fixtures                           56


The user selects exactly five tokens by number.

Example:


Tokens still to select: 5
Enter token number: 2
[✓] Selected: #2 -> /


Selecting by number prevents spelling mistakes and makes the experiment
easier to use.

Duplicate selections are rejected.

------------------------------------------------------------------------

# 16. Selecting Related Tokens

For every selected token, the top-50 candidate list is displayed again.

The user chooses the token they consider most related.

For example:


TOKEN: tests

Choose the token that YOU consider most related to this token.

No.   Token                         Frequency
------------------------------------------------
...
40    app                                71
...


The user enters the candidate number.

This is explicitly the **human/semantic judgement** part of Task 3.

The random embedding similarity is not used to decide the relationship.

The selected pairs are saved to:


task3_selected_tokens.csv


------------------------------------------------------------------------

# 17. Task 4 --- Pair Cosine Similarity

Task 4 calculates cosine similarity for the five manually selected
pairs.

Example:


tests                     <-> app
sklearn                   <-> selection
310                       <-> path


The results are saved to:


task4_pair_similarity.csv


This allows the human-selected relationships to be compared against the
random embedding space.

------------------------------------------------------------------------

# 18. Task 5 --- Naive Similarity Improvement

File:


similarity_improvement.py


Task 5 introduces a simple manually designed heuristic.

It is intentionally a basic experiment and **not a trained embedding
model**.

The algorithm:


1. Load random embeddings.
2. Compare every pair of top-50 tokens.
3. Calculate character overlap.
4. If overlap >= 0.40, mark the pair as related.
5. Move their embeddings slightly toward each other.
6. Save the improved embeddings.


Configuration:


Learning Rate            = 0.05
Minimum Character Overlap = 0.40


------------------------------------------------------------------------

# 19. Character Overlap

The algorithm compares the sets of unique characters in two tokens.

Conceptually:


Characters(token A) ∩ Characters(token B)


is compared against the smaller character set.

If:


overlap >= 0.40


the pair is considered related by the heuristic.

------------------------------------------------------------------------

# 20. Embedding Update

For a related pair:


new_A = (1 - learning_rate) × A
        + learning_rate × B

new_B = (1 - learning_rate) × B
        + learning_rate × A


With:


learning_rate = 0.05


each embedding moves slightly toward the other.

Conceptually:


Before:

A ●


                  ● B


After:

          ● A  B ●


The goal is to demonstrate how a rule-based modification can change the
geometry of an embedding space.

------------------------------------------------------------------------

# 21. Task 6 --- Repeating the Experiment

Task 6 calculates similarity again after the embedding update.

For each pair:


Original Similarity
        ↓
Improved Similarity
        ↓
Change


The change is:


Change =
Improved Similarity - Original Similarity


Results:


improved_similarity_results.csv


Statistics:


similarity_improvement_statistics.json


------------------------------------------------------------------------

# 22. BPE Tokenizer Artifact

The file:


bpe_tokenizer.json


is the saved trained BPE tokenizer.

The conceptual process is:


combined_dataset.csv
        ↓
Text corpus
        ↓
BPE training
        ↓
Vocabulary + merge information
        ↓
bpe_tokenizer.json


The file preserves the trained tokenizer configuration and vocabulary
information for reproducibility.

The current `embedding_analysis.py` uses the generated BPE
token-frequency CSV and top-50 vocabulary rather than directly loading
`bpe_tokenizer.json`. The JSON is still preserved as the trained BPE
artifact.

------------------------------------------------------------------------

# 23. Source Code Module Responsibilities

  -----------------------------------------------------------------------
  File                                Lab Responsibility
  ----------------------------------- -----------------------------------
  `character_tokenizer.py`            Character tokenizer +
                                      vocabulary/sequence/embedding
                                      statistics

  `word_tokenizer.py`                 Word tokenizer +
                                      vocabulary/sequence/embedding
                                      statistics

  `subword_tokenizer.py`              BPE tokenizer + statistics + saved
                                      tokenizer

  `embedding_analysis.py`             Task 2: random embeddings, top 50
                                      and similarity analysis

  `token_similarity.py`               Tasks 3--4: interactive selection
                                      and pair similarity

  `similarity_improvement.py`         Tasks 5--6: naive improvement and
                                      re-experiment

  `main.py`                           Runs the entire pipeline in order

  `requirements.txt`                  Python dependencies
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 24. Main.py Pipeline

`main.py` coordinates the complete experiment:


main.py
   │
   ├── Task 1
   │    ├── character_tokenizer.py
   │    ├── word_tokenizer.py
   │    └── subword_tokenizer.py
   │
   ├── Task 2
   │    └── embedding_analysis.py
   │
   ├── Tasks 3 & 4
   │    └── token_similarity.py
   │
   └── Tasks 5 & 6
        └── similarity_improvement.py


Later stages use artifacts generated by earlier stages.

------------------------------------------------------------------------

# 25. Running the Lab

From the project root:


cd D:\CSET456Lab


Install dependencies:


pip install -r "D:\CSET456Lab\lab3\src\requirements.txt"


Run the complete pipeline:


python -u "D:\CSET456Lab\lab3\src\main.py"


The execution order is:


Task 1
  ↓
Task 2
  ↓
Task 3
  ↓
Task 4
  ↓
Task 5
  ↓
Task 6


Tasks 3 and 4 require interactive input.

------------------------------------------------------------------------

# 26. Generated Output Files

## Tokenization


character_tokenizer_statistics.json
character_vocabulary.json

word_tokenizer_statistics.json
word_vocabulary.json

subword_tokenizer_statistics.json
subword_vocabulary.json
subword_token_frequency.csv
bpe_tokenizer.json


## Embedding Analysis


top_50_tokens.csv
random_embedding_matrix.npy
embedding_statistics.json
top_10_most_similar.csv
top_10_least_similar.csv


## Tasks 3 and 4


task3_selected_tokens.csv
task4_pair_similarity.csv


## Tasks 5 and 6


improved_embedding_matrix.npy
improved_similarity_results.csv
similarity_improvement_statistics.json


------------------------------------------------------------------------

# 27. Current Experimental Results

The current execution used:


Dataset records       : 2670
Embedding dimension   : 128
Top tokens analyzed   : 50
Pairwise comparisons  : 1225


## Character tokenizer


Vocabulary size          : 42
Average sequence length : 42.9322
Embedding matrix        : 42 × 128
Embedding parameters    : 5,376


## Word tokenizer


Vocabulary size          : 1,943
Average sequence length : 7.6719
Embedding matrix        : 1,943 × 128
Embedding parameters    : 248,704


## BPE tokenizer


Target vocabulary size  : 10,000
Actual vocabulary size  : 1,755
Unique observed tokens  : 1,208
Average sequence length : 13.1337
Embedding matrix        : 1,755 × 128
Embedding parameters    : 224,640


These results are specific to the current dataset and configuration.

------------------------------------------------------------------------

# 28. Current Top BPE Tokens

The current experiment produced:


_          6355
/          5356
py         2957
.          2336
test       1720
tests      1011
tutorial    938
sklearn     768
src         603
/_          508


These are frequency statistics, not semantic similarity scores.

------------------------------------------------------------------------

# 29. Current Task 3 Selections

The current interactive experiment selected:


/          <-> _
.          <-> py
tests      <-> app
sklearn    <-> selection
310        <-> path


Saved in:


task3_selected_tokens.csv


------------------------------------------------------------------------

# 30. Current Task 4 Results

The current random-embedding similarities were:


/          <-> _            :  0.029607
.          <-> py           : -0.004125
tests      <-> app          :  0.047734
sklearn    <-> selection    : -0.027402
310        <-> path         : -0.077537


Because the embeddings are random, these numbers do not represent
learned semantic similarity.

------------------------------------------------------------------------

# 31. Current Task 5/6 Results

The current naive improvement experiment detected:


Related token pairs : 453
Total pairs analyzed: 1225


Average similarity:


Before : -0.001855
After  :  0.115754
Change :  0.117609


The increase is an expected effect of the update rule because related
pairs are explicitly moved closer together.

It should not be interpreted by itself as proof that the resulting
embedding space is semantically better.

------------------------------------------------------------------------

# 32. Important Observations

### Character Tokenization

The character tokenizer produced the smallest vocabulary:


42


but the longest average sequence:


42.9322


This demonstrates the vocabulary-size versus sequence-length trade-off.

### Word Tokenization

Word tokenization produced:


Vocabulary = 1,943
Average sequence length = 7.6719


The vocabulary is larger while sequences are substantially shorter.

### BPE Tokenization

BPE produced:


Vocabulary = 1,755
Average sequence length = 13.1337


For this dataset, BPE sits between character and word tokenization in
average sequence length.

BPE also provides subword units that can represent portions of
identifiers and other uncommon terms.

------------------------------------------------------------------------

# 33. Important Dataset Limitation

The current dataset does not contain a `source_code` column.

Therefore the tokenizer prints:


WARNING: source_code column not found.
Falling back to file_path.


The current statistics are consequently based on file-path strings.

For a true source-code tokenization experiment, the input dataset should
include actual source-code contents, for example:


source_code


This limitation should be explicitly mentioned in the lab
report/observations.

------------------------------------------------------------------------

# 34. Reproducibility

The experiment saves important artifacts at every stage.

### Random seed


42


### BPE tokenizer


bpe_tokenizer.json


### Token vocabularies


character_vocabulary.json
word_vocabulary.json
subword_vocabulary.json


### Random embeddings


random_embedding_matrix.npy


### Human selections


task3_selected_tokens.csv


### Similarity results


task4_pair_similarity.csv
improved_similarity_results.csv


This makes it possible to inspect the experiment after execution instead
of relying only on terminal output.

------------------------------------------------------------------------

# 35. Technologies Used


Python
Pandas
NumPy
BPE Tokenization
Cosine Similarity
CSV
JSON
NumPy .npy matrices


The project is organized into separate modules so that each stage has a
clear responsibility.

------------------------------------------------------------------------

# 36. Final Architecture Summary


┌──────────────────────────────────────────────────────────────┐
│                         LAB 2 DATA                           │
│                                                              │
│                    combined_dataset.csv                      │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                         TASK 1                               │
│                       TOKENIZATION                           │
│                                                              │
│   Character       Word              Subword / BPE            │
│      │              │                    │                   │
│      ▼              ▼                    ▼                   │
│  Vocabulary     Vocabulary          BPE Vocabulary           │
│  Statistics     Statistics          Statistics               │
└─────────────────────────────────────┬────────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────┐
│                         TASK 2                               │
│                   EMBEDDING ANALYSIS                         │
│                                                              │
│  BPE Frequencies → Top 50 → Random Embeddings → Similarity   │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                       TASKS 3 & 4                            │
│                                                              │
│  Human selects 5 tokens → Related tokens → Cosine Similarity│
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                       TASKS 5 & 6                            │
│                                                              │
│  Character-overlap heuristic                                │
│             ↓                                                │
│  Move related embeddings closer                              │
│             ↓                                                │
│  Recalculate similarities                                    │
│             ↓                                                │
│  Compare before vs after                                     │
└──────────────────────────────────────────────────────────────┘


------------------------------------------------------------------------

# 37. Conclusion

Lab 3 demonstrates the transition from prepared software-engineering
data to machine-learning-oriented representations.

The complete progression is:


Repository Data
      ↓
Prepared Dataset
      ↓
Character / Word / BPE Tokenization
      ↓
Vocabulary Analysis
      ↓
Numerical Embeddings
      ↓
Cosine Similarity
      ↓
Human Relationship Analysis
      ↓
Naive Embedding Improvement
      ↓
Before / After Comparison


The experiment shows that tokenization is an important design decision
because it affects:

-   Vocabulary size
-   Sequence length
-   Embedding matrix size
-   Number of embedding parameters

The BPE tokenizer provides the representation used for the later
experiments, while the embedding and similarity stages demonstrate how
token representations can be analyzed and modified.

The final similarity-improvement method is intentionally simple. It
demonstrates the idea of changing an embedding space using a
relationship heuristic, but it is **not a trained embedding model** and
should not be treated as a replacement for learned methods such as
Word2Vec, GloVe, transformer embeddings or other representation-learning
approaches.

Overall, Lab 3 forms the bridge between repository-data preparation and
the ML preprocessing/representation stages required before applying
machine-learning models to software-engineering data.

------------------------------------------------------------------------

## Lab 3 Pipeline at a Glance


Lab 1
  │
  ▼
Repository Mining
  │
  ▼
Lab 2
  │
  ▼
combined_dataset.csv
  │
  ▼
Lab 3
  │
  ├── Character Tokenization
  ├── Word Tokenization
  ├── BPE Tokenization
  │
  ├── Random Embeddings
  ├── Top 50 Token Analysis
  ├── Cosine Similarity
  │
  ├── Human Token Selection
  ├── Pair Similarity
  │
  ├── Naive Similarity Improvement
  └── Before/After Experiment


**End of Lab 3 documentation.**
