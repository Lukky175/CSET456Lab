# AB-2 — Mining Multiple Software Repositories, Data Cleaning & Dataset Preparation

## 1. Project Overview

**AB-2** is the second stage of the software repository mining project for the CSET456 laboratory.

In **Lab-1**, five open-source GitHub repositories were mined individually. For each repository, two CSV datasets were generated:

- `file_metrics.csv` — current source-code/file-level information
- `git_history_metrics.csv` — historical file-change information

In **Lab-2**, these Lab-1 outputs are used as the raw input. The repositories are **not mined again**.

The objective is to combine, clean, validate and integrate the data from all five repositories and produce three analysis-ready datasets:

1. **Source-code dataset**
2. **Commit-history dataset**
3. **Combined dataset**

The final combined dataset connects **static source-code characteristics** such as LOC, language and file size with **historical development activity** represented by file change count.

---

## 2. Lab Problem Statement

### AB-2: Mining Multiple Software Repositories, Cleaning Data and Preparing a Dataset

The lab requires:

- Using all five repositories from Lab-1.
- Extracting source-code information separately.
- Extracting commit-history information separately.
- Identifying relevant and irrelevant attributes.
- Cleaning and validating the data.
- Combining the two datasets using meaningful common attributes.
- Generating statistics for all three datasets.
- Identifying software-engineering problems where the resulting datasets can be used.
- Documenting the complete process and providing required screenshots.

The key idea is:


Lab-1: Collect the data
        ↓
Lab-2: Clean, consolidate and integrate the data

---

# 3. What This Lab Does

The complete Lab-2 pipeline is:


                    LAB-1 OUTPUTS
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ▼                                 ▼
 file_metrics.csv                 git_history_metrics.csv
 from 5 repositories              from 5 repositories
        │                                 │
        └────────────────┬────────────────┘
                         ▼
                    data/input/
                         │
                         ▼
              prepare_datasets.py
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       Source-Code Dataset    Commit-History Dataset
              │                     │
              └──────────┬──────────┘
                         ▼
                clean_and_merge.py
                         │
                         ▼
                  Combined Dataset
                         │
                         ▼
                analyze_datasets.py
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
          Source       History     Combined
         Statistics   Statistics   Statistics
             │           │           │
             └───────────┼───────────┘
                         ▼
                      output/

---

# 4. Repositories Used

The same five repositories mined in Lab-1 are used:

| Repository | Lab-1 Data Used |
|---|---|
| Flask | `file_metrics.csv`, `git_history_metrics.csv` |
| Requests | `file_metrics.csv`, `git_history_metrics.csv` |
| Pytest | `file_metrics.csv`, `git_history_metrics.csv` |
| FastAPI | `file_metrics.csv`, `git_history_metrics.csv` |
| Scikit-learn | `file_metrics.csv`, `git_history_metrics.csv` |

There are therefore **10 input CSV files** in total.

---

# 5. Input Structure

The Lab-1 outputs are organized repository-wise:

data/
└── input/
    ├── flask/
    │   ├── file_metrics.csv
    │   └── git_history_metrics.csv
    │
    ├── requests/
    │   ├── file_metrics.csv
    │   └── git_history_metrics.csv
    │
    ├── pytest/
    │   ├── file_metrics.csv
    │   └── git_history_metrics.csv
    │
    ├── fastapi/
    │   ├── file_metrics.csv
    │   └── git_history_metrics.csv
    │
    └── scikit-learn/
        ├── file_metrics.csv
        └── git_history_metrics.csv

The `data/input/` directory is the **raw input layer** of Lab-2.

---

# 6. Architecture

                         LAB-1 DATA
                             │
             ┌───────────────┴───────────────┐
             │                               │
             ▼                               ▼
     Source-code CSVs                 Git-history CSVs
      from 5 repos                     from 5 repos
             │                               │
             └───────────────┬───────────────┘
                             ▼
                      data/input/
                             │
                             ▼
                  prepare_datasets.py
                             │
               ┌─────────────┴─────────────┐
               ▼                           ▼
       source_code_dataset.csv     commit_history_dataset.csv
               │                           │
               └─────────────┬─────────────┘
                             ▼
                    clean_and_merge.py
                             │
                             ▼
                    combined_dataset.csv
                             │
                             ▼
                    analyze_datasets.py
                             │
             ┌───────────────┼───────────────┐
             ▼               ▼               ▼
       Source Statistics History Statistics Combined Statistics
             │               │               │
             └───────────────┼───────────────┘
                             ▼
                          output/

The application is intentionally split into multiple modules rather than putting the entire pipeline inside one large `main.py`.

---

# 7. Project Directory Structure

lab2/
│
├── data/
│   └── input/
│       ├── flask/
│       │   ├── file_metrics.csv
│       │   └── git_history_metrics.csv
│       │
│       ├── requests/
│       │   ├── file_metrics.csv
│       │   └── git_history_metrics.csv
│       │
│       ├── pytest/
│       │   ├── file_metrics.csv
│       │   └── git_history_metrics.csv
│       │
│       ├── fastapi/
│       │   ├── file_metrics.csv
│       │   └── git_history_metrics.csv
│       │
│       └── scikit-learn/
│           ├── file_metrics.csv
│           └── git_history_metrics.csv
│
├── src/
│   ├── prepare_datasets.py
│   ├── clean_and_merge.py
│   ├── analyze_datasets.py
│   └── main.py
│
├── output/
│   ├── source_code_dataset.csv
│   ├── commit_history_dataset.csv
│   ├── combined_dataset.csv
│   │
│   ├── source_code_statistics.json
│   ├── commit_history_statistics.json
│   ├── combined_dataset_statistics.json
│   │
│   └── screenshots/
│
├── requirements.txt
└── README.md

---

# 8. What Each File Does

## `prepare_datasets.py`

This is the **data consolidation stage**.

It:

1. Reads the five `file_metrics.csv` files.
2. Adds a `repository` column to preserve the source repository.
3. Combines them into one source-code dataset.
4. Reads the five `git_history_metrics.csv` files.
5. Adds the repository identity.
6. Combines them into one commit-history dataset.

Outputs:


output/source_code_dataset.csv
output/commit_history_dataset.csv


Conceptually:


Flask file_metrics.csv
Requests file_metrics.csv
Pytest file_metrics.csv
FastAPI file_metrics.csv
Scikit-learn file_metrics.csv
             │
             ▼
    source_code_dataset.csv


and:

Flask git_history_metrics.csv
Requests git_history_metrics.csv
Pytest git_history_metrics.csv
FastAPI git_history_metrics.csv
Scikit-learn git_history_metrics.csv
             │
             ▼
    commit_history_dataset.csv

---

## `clean_and_merge.py`

This is the **data cleaning and integration stage**.

It:

- Removes empty rows.
- Removes duplicate records.
- Normalizes repository names.
- Normalizes file paths.
- Validates numeric fields.
- Validates relevant categorical fields.
- Removes malformed records.
- Merges the two cleaned datasets.

The common key is:


repository + file_path


The merge uses a **left join**:


Current Source Files
        │
        │ LEFT JOIN
        ▼
Historical Change Information


The source-code dataset is the left/base dataset because the final dataset should retain current source files even when a corresponding history record is unavailable.

Output:


output/combined_dataset.csv

---

## `analyze_datasets.py`

This is the **analysis/statistics stage**.

It calculates statistics for:

1. Source-code dataset
2. Commit-history dataset
3. Combined dataset

Outputs:


output/source_code_statistics.json
output/commit_history_statistics.json
output/combined_dataset_statistics.json


The statistics provide a compact way to inspect the size, distribution and characteristics of each dataset.

---

## `main.py`

This is the **main orchestration file**.

It does not contain all the processing logic. Instead, it runs the modules in the correct order:


main.py
   │
   ├── prepare_datasets.py
   │
   ├── clean_and_merge.py
   │
   └── analyze_datasets.py


This keeps the application modular and prevents one large script from becoming difficult to maintain.

---

# 9. Why the `repository` Column is Required

The five repositories can contain files with the same relative path.

For example:


flask/src/main.py
requests/src/main.py


Both may have:


file_path = src/main.py


Therefore, `file_path` alone cannot uniquely identify a file across all repositories.

Lab-2 adds:


repository


so a record can be uniquely identified using:


repository + file_path


For example:


flask + src/main.py
requests + src/main.py


This preserves repository identity throughout the consolidation and merge process.

---

# 10. Dataset 1 — Source-Code Dataset

The source-code dataset is created by combining the five Lab-1 `file_metrics.csv` files.

Typical fields are:

| Field | Meaning |
|---|---|
| `repository` | Repository from which the file originated |
| `file_path` | Repository-relative file path |
| `language` | Detected programming language |
| `extension` | File extension |
| `loc` | Physical lines in the source file |
| `size_bytes` | File size in bytes |

It represents the **current/static characteristics** of source files.

---

# 11. Dataset 2 — Commit-History Dataset

The commit-history dataset is created by combining the five Lab-1 `git_history_metrics.csv` files.

Typical fields are:

| Field | Meaning |
|---|---|
| `repository` | Repository from which the record originated |
| `file_path` | Repository-relative file path |
| `change_count` | Number of times the file appeared in the analyzed Git history |

It represents **historical development activity**.

---

# 12. Dataset 3 — Combined Dataset

The combined dataset connects the two datasets using:

repository + file_path


A resulting record can contain:


repository
file_path
language
extension
loc
size_bytes
change_count


This allows a file to be studied using both:

### Static characteristics

Language
Extension
LOC
File size

### Historical characteristics

Change count

The combined dataset therefore provides a common basis for studying relationships between source-code characteristics and development activity.

---

# 13. Data Cleaning

The lab specifically requires identifying relevant information and removing or handling information that is not useful.

The cleaning process checks for:

### Empty rows

Rows containing no meaningful information are removed.

### Duplicate records

Duplicate records are removed so that the same observation is not unintentionally counted multiple times.

### Repository names

Repository names are normalized to a consistent representation.

### File paths

File paths are normalized so matching records can be joined correctly.

### Numeric values

Values such as:


loc
size_bytes
change_count


are validated as numeric values.

### Invalid/malformed records

Rows that cannot be reliably interpreted are removed.

### Irrelevant information

Temporary, duplicated or unnecessary fields are excluded when they do not contribute to the required analysis.

---

# 14. Relevant vs. Irrelevant Information

The important principle is:

> Keep information that helps describe a source file or its historical activity; remove information that creates noise, duplication or ambiguity without supporting the required analysis.

### Relevant

- Repository
- File path
- Language
- Extension
- LOC
- File size
- Change count

### Potentially irrelevant

- Empty columns
- Temporary/index columns
- Duplicate records
- Repeated metadata
- Malformed records
- Fields that cannot be matched between datasets

The exact fields retained by the implementation are chosen to support the three required datasets and their integration.

---

# 15. Merge Strategy

The two datasets are related through:

repository + file_path

The relationship is:


                 repository
                      +
                  file_path
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
   Source-Code Data        History Data
          │                       │
          └───────────┬───────────┘
                      ▼
               Combined Data


A **left join** is used:

Source-Code Dataset
        │
        │ LEFT JOIN
        ▼
Commit-History Dataset

This means all current source-file records from the source-code dataset are retained.

If a current source file has no matching history record, it is not discarded merely because historical information is unavailable.

---

# 16. Execution Flow

                 LAB-1 OUTPUT
                      │
                      ▼
                  data/input/
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
   file_metrics.csv       git_history_metrics.csv
   from 5 repositories    from 5 repositories
          │                       │
          ▼                       ▼
  Add repository field    Add repository field
          │                       │
          ▼                       ▼
  Clean source data       Clean history data
          │                       │
          ▼                       ▼
source_code_dataset.csv  commit_history_dataset.csv
          │                       │
          └───────────┬───────────┘
                      │
             repository + file_path
                      │
                      ▼
             combined_dataset.csv
                      │
                      ▼
              Dataset Analysis
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       Source       Commit      Combined
      Statistics   Statistics  Statistics
          │           │           │
          ▼           ▼           ▼
         JSON        JSON        JSON

---

# 17. Detailed Runtime Flow

Run:

python src/main.py


### Step 1 — Read Lab-1 data

The program reads the five repository directories inside:


data/input/


### Step 2 — Consolidate source-code data

All five `file_metrics.csv` files are combined.

The repository name is added to each record.

Output:


source_code_dataset.csv


### Step 3 — Consolidate commit-history data

All five `git_history_metrics.csv` files are combined.

The repository name is added to each record.

Output:


commit_history_dataset.csv


### Step 4 — Clean the datasets

The consolidated datasets are validated and normalized.

### Step 5 — Merge

The datasets are joined using:


repository + file_path


Output:


combined_dataset.csv


### Step 6 — Generate statistics

Statistics are calculated for all three datasets.

Outputs:


source_code_statistics.json
commit_history_statistics.json
combined_dataset_statistics.json

---

# 18. How to Run

## Prerequisites

Install:

- Python 3.x
- pip

No GitHub repository needs to be cloned during Lab-2 execution.

---

## Step 1 — Navigate to Lab-2

cd lab2

---

## Step 2 — Install Dependencies

pip install -r requirements.txt

---

## Step 3 — Verify Input

Make sure the following directories exist:

data/input/flask/
data/input/requests/
data/input/pytest/
data/input/fastapi/
data/input/scikit-learn/

Each directory must contain:

file_metrics.csv
git_history_metrics.csv

---

## Step 4 — Run

python src/main.py

The complete pipeline runs automatically.

---

# 19. Runtime Input

Unlike Lab-1, Lab-2 does **not ask the user for a GitHub URL**.

Lab-1 required:

GitHub URL
      ↓
Repository Clone
      ↓
Repository Mining


Lab-2 uses:


Lab-1 CSV Outputs
      ↓
data/input/
      ↓
Dataset Preparation


Therefore, the input to Lab-2 is the repository-wise CSV data already generated in Lab-1.

---

# 20. Output Structure

After successful execution:


output/
│
├── source_code_dataset.csv
├── commit_history_dataset.csv
├── combined_dataset.csv
│
├── source_code_statistics.json
├── commit_history_statistics.json
├── combined_dataset_statistics.json
│
└── screenshots/

---

# 21. Statistics

## Source-Code Statistics

The source-code statistics summarize characteristics such as:

- Number of records
- Number of repositories
- Number of languages
- Number of extensions
- Total LOC
- Average LOC
- Total file size
- Average file size
- Repository distribution
- Language distribution

---

## Commit-History Statistics

The commit-history statistics summarize:

- Number of records
- Number of repositories
- Total change events
- Average change count
- Minimum/maximum change count
- Frequently changed files
- Repository-level activity

---

## Combined Dataset Statistics

The combined statistics summarize:

- Number of records
- Number of repositories
- Language distribution
- LOC statistics
- File-size statistics
- Change-count statistics
- Repository distribution

---

# 22. Why the Combined Dataset is Useful

The individual datasets answer different questions.

### Source-code dataset


"What does the file look like?"


It provides:


LOC
Language
Extension
Size


### Commit-history dataset


"How active has this file been?"


It provides:


Change count


### Combined dataset


"How do the characteristics of a file relate to its historical activity?"


For example, it enables investigation of whether larger or more complex-looking files tend to have higher historical activity.

The dataset itself does not claim that such relationships exist; it provides the data needed to investigate them.

---

# 23. Potential Software-Engineering Applications

The resulting datasets can be used for:

## Code Hotspot Analysis

Files with both high size/LOC and high change activity can be investigated as potential maintenance hotspots.

## Code Churn Analysis

Change counts can be used to study which files receive frequent modifications.

## Maintenance Planning

Frequently modified files can be examined further for refactoring or maintenance needs.

## Repository Comparison

The five repositories can be compared using common attributes such as:


Average LOC
Average file size
Language distribution
Historical activity


## Historical Activity Analysis

The combined data can be used to investigate relationships between static source characteristics and historical development activity.

## Future Predictive Analysis

The combined dataset can serve as a foundation for future machine-learning or statistical studies involving:

- Change-prone files
- Maintenance hotspots
- Refactoring candidates
- Potential defect-prone areas

These are possible applications; this lab does not claim that the dataset alone proves any of these outcomes.

---

# 24. Lab-1 vs Lab-2

| Lab-1 | Lab-2 |
|---|---|
| Mines repositories | Uses Lab-1 outputs |
| Works with repositories individually | Works across five repositories |
| Collects source/file metrics | Consolidates source metrics |
| Mines Git history | Consolidates history metrics |
| Produces repository-specific CSVs | Produces cross-repository datasets |
| Focuses on data collection | Focuses on cleaning and integration |
| Requires repository access | Uses existing CSV input |

Overall:


LAB-1
Repository Mining
      ↓
Raw Datasets
      ↓
LAB-2
Cleaning + Consolidation + Integration
      ↓
Analysis-Ready Dataset

---

# 25. Design Decisions

### Use Lab-1 outputs

The lab builds directly on Lab-1, so repositories are not mined again.

### Repository-wise input

Keeping each repository inside its own folder makes the data source clear and prevents manual confusion.

### Two consolidated datasets

Source-code and Git-history information are first consolidated separately because they represent different types of information.

### Repository identity

The `repository` field is added before combining records so their original source is never lost.

### Composite merge key

The merge uses:

repository + file_path


instead of `file_path` alone.

### Left join

The source-code dataset is the base so current source files remain represented even if no corresponding history record exists.

### Modular architecture

The pipeline is split into:


Preparation
    ↓
Cleaning + Merge
    ↓
Analysis


This makes the project easier to understand, debug and extend.

---

# 26. Lab Deliverables

The project produces:


✓ source_code_dataset.csv
✓ commit_history_dataset.csv
✓ combined_dataset.csv

✓ source_code_statistics.json
✓ commit_history_statistics.json
✓ combined_dataset_statistics.json

✓ screenshots/
✓ README.md


The screenshots directory can contain the required prompts, execution evidence and other relevant laboratory screenshots.

---

# 27. Final Architecture


                         ┌──────────────────────┐
                         │      LAB-1 DATA      │
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
            Flask                Requests               Pytest
              │                     │                     │
              └─────────────────────┼─────────────────────┘
                                    │
                         FastAPI + Scikit-learn
                                    │
                                    ▼
                             data/input/
                                    │
                                    ▼
                       ┌────────────────────────┐
                       │ prepare_datasets.py    │
                       └───────────┬────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
          Source-Code Dataset             Commit-History Dataset
                    │                             │
                    └──────────────┬──────────────┘
                                   ▼
                       ┌────────────────────────┐
                       │ clean_and_merge.py     │
                       └───────────┬────────────┘
                                   │
                                   ▼
                         Combined Dataset
                                   │
                                   ▼
                       ┌────────────────────────┐
                       │ analyze_datasets.py    │
                       └───────────┬────────────┘
                                   │
                  ┌────────────────┼────────────────┐
                  ▼                ▼                ▼
             Source Stats     History Stats    Combined Stats
                  │                │                │
                  └────────────────┼────────────────┘
                                   ▼
                                output/

---

# 28. Quick Start

cd lab2
pip install -r requirements.txt
python src/main.py

### Input

data/input/

### Main Outputs

output/
├── source_code_dataset.csv
├── commit_history_dataset.csv
├── combined_dataset.csv
├── source_code_statistics.json
├── commit_history_statistics.json
└── combined_dataset_statistics.json

---

# 29. Final Summary

Lab-2 extends the repository-mining work completed in Lab-1.

The overall process is:


Five Lab-1 Repositories
          ↓
Ten Lab-1 CSV Files
          ↓
Repository-wise Input Organization
          ↓
Consolidated Source-Code Dataset
          +
Consolidated Commit-History Dataset
          ↓
Cleaning & Validation
          ↓
Repository + File Path Join
          ↓
Combined Dataset
          ↓
Statistics
          ↓
Software-Engineering Analysis


The central outcome is a **cleaned and integrated multi-repository dataset** where current source-code characteristics can be studied together with historical development activity.

This dataset provides a reusable foundation for repository comparison, code hotspot analysis, maintenance studies, historical activity analysis and future software-engineering research.