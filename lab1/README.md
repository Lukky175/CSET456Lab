# AB-1 --- Mining and Profiling a Software Repository

A Python-based software repository mining and profiling tool developed
for **AB-1: Mining and Profiling a Software Repository**.

The project treats a software repository as a source of **structured and
unstructured software-engineering data**. It programmatically accesses a
public GitHub repository, analyzes its current file structure and source
code, mines its Git history, and produces reusable datasets and reports.

------------------------------------------------------------------------

## 1. What Is This Project?

Software repositories contain much more information than source code
alone. They include source files, documentation, configuration, tests,
build files, directory structures, commit history, contributors,
file-change patterns, and development activity.

This project automates the extraction of useful information from two
dimensions:

### Current Repository State

The current checkout is analyzed to determine:

-   Repository name
-   Total number of files
-   Number of source-code files
-   Number of directories
-   Programming languages
-   Total physical lines of code (LOC)
-   Average LOC per source file
-   Largest source files
-   File-type distribution
-   File-level metrics such as LOC and file size

### Repository Development History

Git history is mined to determine:

-   Total number of commits
-   Number of contributors
-   Most active contributor
-   Commits per month
-   Frequently changed files
-   Average file changes per month
-   Average lines added per commit
-   Average lines deleted per commit

The results are exported as **CSV datasets, JSON statistics, and a
Markdown report**.

------------------------------------------------------------------------

## 2. Quick Start

If you are opening this repository for the first time, follow these
steps.

### Step 1 --- Open the Project

Open the project in VS Code or another IDE.

``` text
CSET456Lab/
└── lab1/
```

### Step 2 --- Open a Terminal

Navigate to the Lab 1 directory:

``` bash
cd D:\CSET456Lab\lab1
```

Use your actual project path if it differs.

### Step 3 --- Verify Python

``` bash
python --version
```

Python 3.x is required.

### Step 4 --- Verify Git

``` bash
git --version
```

Git is required because the application clones repositories and mines
their history.

### Step 5 --- Run the Application

From the `lab1` directory:

``` bash
python -u "src\mine_repository.py"
```

### Step 6 --- Enter a GitHub Repository URL

The application prompts:

``` text
Enter GitHub repository URL:
```

Enter a public GitHub repository URL.

Example:

``` text
https://github.com/scikit-learn/scikit-learn
```

### Step 7 --- Wait for the Analysis

The application performs four stages:

``` text
Repository Setup
       ↓
File Metrics
       ↓
Git History Mining
       ↓
Report Generation
```

### Step 8 --- View the Results

Results are generated under:

``` text
lab1/output/<repository-name>/
```

Expected files:

``` text
file_metrics.csv
git_history_metrics.csv
repository_statistics.json
summary.md
```

------------------------------------------------------------------------

## 3. Runtime Input

The application requires one input:

``` text
GitHub repository URL
```

Example:

``` text
https://github.com/scikit-learn/scikit-learn
```

The application then:

1.  Validates the URL.
2.  Extracts the repository name.
3.  Determines the local repository path.
4.  Checks whether the repository already exists.
5.  Clones it if necessary.
6.  Analyzes the current repository.
7.  Mines Git history.
8.  Generates datasets and reports.

The current implementation accepts GitHub repository URLs.

------------------------------------------------------------------------

## 4. Problem Statement

### AB-1: Mining and Profiling a Software Repository

The lab demonstrates how a software repository can be treated as a
source of software-engineering data.

The project addresses the following objectives:

-   Understand a repository as a source of structured and unstructured
    software-engineering data.
-   Clone/access an open-source GitHub repository programmatically.
-   Traverse repository files and identify source-code files.
-   Extract repository-level and file-level metrics.
-   Use Git history to extract development information.
-   Produce machine-readable datasets for subsequent labs.
-   Understand the difference between source-code analysis and
    repository mining.

------------------------------------------------------------------------

## 5. Lab Tasks and Implementation

### Task 1 --- Repository Inventory

The application determines:

  -----------------------------------------------------------------------
  Metric                              Description
  ----------------------------------- -----------------------------------
  Repository Name                     Repository name extracted from the
                                      GitHub URL

  Number of Files                     Total files in the current
                                      repository snapshot

  Source-Code Files                   Files identified using supported
                                      source-code extensions

  Programming Languages               Languages inferred from source-file
                                      extensions

  Number of Directories               Directories excluding `.git`

  Total LOC                           Total physical lines across
                                      identified source files

  Average LOC per Source File         Average physical LOC across
                                      identified source files

  Largest Source Files                Top 10 source files by physical LOC

  File-Type Distribution              Distribution of file extensions
                                      across repository files
  -----------------------------------------------------------------------

### Task 2 --- File-Level Dataset

A CSV record is generated for every identified source-code file.

Schema:

``` text
file_path,language,extension,loc,size_bytes
```

Example:

``` text
src/main/User.java,Java,.java,184,6212
src/main/Login.java,Java,.java,237,8192
src/utils/Parser.java,Java,.java,421,15421
```

Output:

``` text
file_metrics.csv
```

### Task 3 --- Git History Mining

The application extracts:

-   Total commits
-   Contributors
-   Most active contributor
-   Frequently changed files
-   Commits per month
-   Average file changes per month
-   Average lines added per commit
-   Average lines deleted per commit

------------------------------------------------------------------------

## 6. Source-Code Analysis vs Repository Mining

This distinction is a central concept of the lab.

### Source-Code Analysis

Source-code analysis focuses on the current contents and characteristics
of source files.

This project performs basic analysis through:

-   Source-file identification
-   Programming-language classification
-   Physical LOC measurement
-   File-size measurement
-   Largest-file identification
-   File-type distribution

It answers:

> **What is currently in the repository?**

### Repository Mining

Repository mining focuses on historical software-engineering information
stored in Git.

This project mines:

-   Commits
-   Contributors
-   Commit dates
-   File changes
-   Lines added
-   Lines deleted
-   Frequently modified files
-   Development activity over time

It answers:

> **How has the repository evolved?**

``` text
             SOFTWARE REPOSITORY
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
   Current Snapshot          Git History
          │                       │
          ▼                       ▼
 Source-Code Analysis       Repository Mining
          │                       │
          ▼                       ▼
 "What is here?"          "How did it evolve?"
```

------------------------------------------------------------------------

## 7. System Architecture

The project uses a modular pipeline in which each Python module has a
specific responsibility.

``` text
                    GitHub Repository URL
                              │
                              ▼
                    ┌───────────────────┐
                    │ Repository Setup  │
                    │ repository_setup  │
                    │       .py         │
                    └─────────┬─────────┘
                              │
                              ▼
                    Local Git Repository
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
        ┌──────────────────┐     ┌────────────────────┐
        │  File Analysis   │     │   Git History      │
        │ file_metrics.py  │     │ git_history_       │
        │                  │     │ metrics.py         │
        └────────┬─────────┘     └─────────┬──────────┘
                 │                         │
                 ▼                         ▼
          file_metrics.csv       git_history_metrics.csv
                 │                         │
                 └────────────┬────────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Report Generator  │
                    │ report_generator  │
                    │       .py         │
                    └─────────┬─────────┘
                              │
                              ▼
              ┌──────────────────────────────┐
              │ repository_statistics.json   │
              │ summary.md                   │
              └──────────────────────────────┘
```

------------------------------------------------------------------------

## 8. End-to-End Execution Flow

``` text
START
  │
  ▼
Enter GitHub Repository URL
  │
  ▼
┌─────────────────────────────┐
│ 1. Repository Setup         │
├─────────────────────────────┤
│ Validate URL                │
│ Extract repository name     │
│ Determine local path        │
│ Check existing repository  │
│ Clone if required           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ 2. File Metrics             │
├─────────────────────────────┤
│ Traverse repository         │
│ Ignore .git                 │
│ Identify source files       │
│ Count files/directories     │
│ Detect languages            │
│ Calculate LOC               │
│ Calculate file sizes        │
│ Calculate file types        │
│ Find largest source files   │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ 3. Git History              │
├─────────────────────────────┤
│ Scan all commit metadata    │
│ Count commits               │
│ Count contributors          │
│ Calculate commits/month     │
│                             │
│ Analyze latest 400 commits  │
│ File changes                │
│ Additions                   │
│ Deletions                   │
│ Frequently changed files   │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ 4. Report Generation        │
├─────────────────────────────┤
│ Generate CSV datasets       │
│ Generate JSON statistics    │
│ Generate Markdown report    │
└──────────────┬──────────────┘
               │
               ▼
              END
```

------------------------------------------------------------------------

## 9. Project Directory Structure

``` text
CSET456Lab/
│
├── lab1/
│   │
│   ├── data/
│   │   └── repo/
│   │       └── <repository-name>/
│   │           └── cloned Git repository
│   │
│   ├── output/
│   │   └── <repository-name>/
│   │       ├── file_metrics.csv
│   │       ├── git_history_metrics.csv
│   │       ├── repository_statistics.json
│   │       └── summary.md
│   │
│   ├── src/
│   │   ├── mine_repository.py
│   │   ├── repository_setup.py
│   │   ├── file_metrics.py
│   │   ├── git_history_metrics.py
│   │   └── report_generator.py
│   │
│   ├── requirements.txt
│   └── README.md
│
└── lab2/
```

### Generated Directories

``` text
data/repo/
```

stores locally cloned repositories.

``` text
output/
```

stores generated analysis results.

Python may also create:

``` text
__pycache__/
```

This contains Python bytecode and is not part of the analysis.

------------------------------------------------------------------------

## 10. Module Responsibilities

### `src/mine_repository.py`

**Role:** Main entry point and workflow orchestrator.

**Responsibilities:**

-   Accept the repository URL.
-   Start repository setup.
-   Run file analysis.
-   Run Git-history analysis.
-   Generate reports.
-   Display progress and results.
-   Handle errors and cancellation.

Workflow:

``` text
mine_repository.py
        │
        ├── setup_repository()
        ├── generate_file_metrics()
        ├── generate_git_history_metrics()
        └── generate_reports()
```

The file coordinates the workflow but delegates detailed analysis to the
other modules.

### `src/repository_setup.py`

**Role:** Repository validation, local repository management, and
cloning.

**Responsibilities:**

-   Validate GitHub repository URLs.
-   Extract repository names.
-   Determine local paths.
-   Detect an existing clone.
-   Clone repositories when required.

Example:

``` text
https://github.com/scikit-learn/scikit-learn
                    ↓
              scikit-learn
                    ↓
lab1/data/repo/scikit-learn/
```

Repositories are cloned using:

``` text
--filter=blob:none
--no-tags
```

to reduce unnecessary download overhead.

### `src/file_metrics.py`

**Role:** Current repository snapshot analysis.

**Responsibilities:**

-   Traverse repository files.
-   Exclude `.git`.
-   Identify source files.
-   Count files and directories.
-   Detect programming languages.
-   Calculate physical LOC.
-   Calculate file sizes.
-   Determine file-type distribution.
-   Find the 10 largest source files.
-   Generate `file_metrics.csv`.

### Supported Languages

The current implementation recognizes source files using extension-based
classification for:

-   Python
-   Cython
-   C
-   C/C++
-   C++
-   Java
-   JavaScript
-   TypeScript
-   Rust
-   Go
-   Fortran

### Extension Mapping

  Extension   Language
  ----------- ------------
  `.py`       Python
  `.pyx`      Cython
  `.pxd`      Cython
  `.pxi`      Cython
  `.c`        C
  `.h`        C/C++
  `.cpp`      C++
  `.java`     Java
  `.js`       JavaScript
  `.ts`       TypeScript
  `.rs`       Rust
  `.go`       Go
  `.f90`      Fortran
  `.f`        Fortran

### LOC Definition

LOC means **physical lines of file content**.

The implementation reads files in binary mode and counts line records.

Therefore:

``` text
LOC = physical lines
```

It is not a logical-statement count and does not remove comments or
blank lines.

### `src/git_history_metrics.py`

**Role:** Git history mining and development analysis.

The module uses two scopes.

#### Complete Repository History

Used for:

-   Total commits
-   Contributors
-   Most active contributor
-   Commits per month

#### Latest 400 Commits

Used for:

-   File-change frequency
-   Lines added
-   Lines deleted

Git `--numstat` is used instead of generating full patches.

### `src/report_generator.py`

**Role:** Converts collected metrics into final reports.

**Responsibilities:**

-   Combine repository and Git-history statistics.
-   Generate `repository_statistics.json`.
-   Generate `summary.md`.
-   Organize results under the repository-specific output directory.

------------------------------------------------------------------------

## 11. Git History Analysis

The Git-history analysis intentionally separates complete-history
metadata from recent file-change analysis.

``` text
All available commits
        │
        ├── Total commits
        ├── Contributors
        ├── Most active contributor
        └── Commits per month
                 +
Latest 400 commits
        │
        ├── File changes
        ├── Additions
        ├── Deletions
        └── Frequently changed files
```

### Why the Latest 400 Commits?

Analyzing complete diffs for a large repository can be expensive. The
latest 400 commits provide a useful recent-development sample while
keeping file-change analysis practical.

Full repository history is still used for lightweight commit metadata.

------------------------------------------------------------------------

## 12. Git Metrics

### Total Commits

Number of commits found in the available repository history.

### Number of Contributors

Number of distinct Git author names found in the history.

### Most Active Contributor

Contributor with the highest number of commits.

### Commits Per Month

Commit dates are grouped using:

``` text
YYYY-MM
```

Example:

``` text
2026-01 → 35 commits
2026-02 → 42 commits
2026-03 → 51 commits
```

### Average File Changes Per Month

For the latest 400 commits:

``` text
Total file-change events
────────────────────────
Number of calendar months represented
```

This is the average number of **file-change events per calendar month**,
not the number of unique files.

If a file appears in five different commits, it contributes five
file-change events.

### Average Lines Added Per Commit

``` text
Total lines added
─────────────────
Number of analyzed commits
```

### Average Lines Deleted Per Commit

``` text
Total lines deleted
───────────────────
Number of analyzed commits
```

------------------------------------------------------------------------

## 13. Generated Datasets

### `file_metrics.csv`

Contains one row per identified source-code file.

  Column         Description
  -------------- --------------------------------------
  `file_path`    Repository-relative source-file path
  `language`     Detected programming language
  `extension`    File extension
  `loc`          Physical lines in the file
  `size_bytes`   File size in bytes

Example:

``` csv
file_path,language,extension,loc,size_bytes
src/example.py,Python,.py,250,8420
src/utils.py,Python,.py,180,6120
```

### `git_history_metrics.csv`

Contains file-change frequency information from the latest 400 commits.

  -----------------------------------------------------------------------
  Column                              Description
  ----------------------------------- -----------------------------------
  `file_path`                         Repository-relative file path

  `change_count`                      Number of times the file appeared
                                      in analyzed commit changes
  -----------------------------------------------------------------------

Example:

``` csv
file_path,change_count
src/example.py,12
src/utils.py,9
```

These datasets are designed to be reusable in later software-engineering
analysis.

------------------------------------------------------------------------

## 14. Generated Reports

### `repository_statistics.json`

Combined machine-readable repository statistics.

High-level structure:

``` json
{
  "repository": {},
  "git_history": {}
}
```

The `repository` section contains metrics such as:

-   Repository name
-   File counts
-   Directory count
-   Source-file count
-   Total and average LOC
-   Programming languages
-   File types
-   Largest source files
-   Dataset path

The `git_history` section contains:

-   Total commits
-   Contributors
-   Most active contributor
-   Contributor information
-   Frequently changed files
-   Commits per month
-   Analysis window
-   Average file changes per month
-   Additions
-   Deletions
-   Average additions per commit
-   Average deletions per commit
-   Dataset path

### `summary.md`

Human-readable Markdown report containing:

-   Repository inventory
-   Programming-language distribution
-   File-type distribution
-   Largest source files
-   Git-history statistics
-   Frequently changed files
-   Commits per month
-   Generated datasets

------------------------------------------------------------------------

## 15. Output Flow

``` text
                         Repository
                              │
               ┌──────────────┴──────────────┐
               │                             │
               ▼                             ▼
        Current Snapshot                Git History
               │                             │
               ▼                             ▼
      file_metrics.csv             git_history_metrics.csv
               │                             │
               └──────────────┬──────────────┘
                              │
                              ▼
                  repository_statistics.json
                              │
                              ▼
                          summary.md
```

------------------------------------------------------------------------

## 16. Example Execution

A typical run looks like:

``` text
======================================================================
          SOFTWARE REPOSITORY MINING - LAB 1
======================================================================

Enter GitHub repository URL: https://github.com/scikit-learn/scikit-learn

[1/4] Repository setup

Repository URL : https://github.com/scikit-learn/scikit-learn
Repository Name: scikit-learn
Local Path     : .../lab1/data/repo/scikit-learn

Repository already exists locally.
Using existing repository.

[✓] Repository setup completed

[2/4] File metrics

Repository Name       : scikit-learn
Total Files           : ...
Source-Code Files     : ...
Directories           : ...
Total LOC             : ...
Average LOC/File      : ...

[✓] File metrics completed

[3/4] Git history

Using all commits for metadata and latest 400 commits for file changes.

[1/2] Scanning all commit metadata...
[✓] ... commits scanned

[2/2] Analyzing latest 400 commits...
[✓] 400 recent commits analyzed

Total Commits                 : ...
Number of Contributors        : ...
Most Active Contributor       : ...
Average Files Changed/Month   : ...
Average Added Lines/Commit    : ...
Average Deleted Lines/Commit  : ...

[✓] Git history completed

[4/4] Generating reports
[✓] Reports generated

======================================================================
LAB-1 COMPLETED
======================================================================
```

------------------------------------------------------------------------

## 17. Re-running the Application

If the requested repository has already been cloned, the application can
reuse the existing local repository.

Example:

``` text
Repository already exists locally.
Using existing repository.
```

This prevents unnecessary repeated cloning.

If the local clone needs to reflect newer upstream changes, update it
before running the analysis again.

------------------------------------------------------------------------

## 18. Requirements

The project requires:

-   Python 3.x
-   Git
-   Internet access when cloning a repository
-   A public GitHub repository URL

The implementation primarily uses Python's standard library:

``` text
pathlib
collections
datetime
csv
json
subprocess
urllib.parse
```

If additional dependencies are introduced, they should be added to:

``` text
requirements.txt
```

------------------------------------------------------------------------

## 19. Performance Considerations

The implementation avoids unnecessarily expensive operations.

### File Analysis

Only the current repository snapshot is traversed.

### Complete History

Only lightweight commit metadata is requested.

### Recent History

Only the latest 400 commits are analyzed for file-level changes.

Git `--numstat` provides:

``` text
additions
deletions
file path
```

without generating full patches.

This is significantly more efficient than processing complete diffs for
every commit.

------------------------------------------------------------------------

## 20. Design Decisions

### Modular Architecture

Each major responsibility is isolated in its own module, making the
system easier to understand, test, and extend.

### No Full Git Patches

The history analysis uses metadata and `--numstat` instead of complete
patches.

### 400-Commit File-Change Window

A fixed recent window provides useful development information without
making large-repository analysis unnecessarily expensive.

### Extension-Based Language Detection

Language classification is deterministic and lightweight because it is
based on file extensions.

### Current Snapshot for File Metrics

File metrics describe the repository as it exists in the current
checkout.

### Machine-Readable Outputs

CSV and JSON make the generated information reusable by later labs,
scripts, visualizations, and machine-learning workflows.

------------------------------------------------------------------------

## 21. Limitations and Metric Interpretation

### LOC

LOC represents physical lines and does not remove:

-   Comments
-   Blank lines
-   Generated code
-   Formatting-only lines

### Language Detection

Languages are identified from file extensions rather than source-code
parsing.

### Contributor Count

Contributors are identified by Git author names. Different names for the
same person may therefore be counted separately.

### File-Change Frequency

A file appearing in multiple commits contributes once per appearance.

Therefore:

``` text
change_count ≠ number of unique files changed
```

### Current Repository State

File inventory metrics describe the current checkout.

### Git History Scope

Commit-level metadata uses the complete available history, while
file-level change metrics use the latest 400 commits.

------------------------------------------------------------------------

## 22. Error Handling

The application handles common problems such as:

-   Empty repository URL
-   Invalid GitHub URL
-   Invalid repository path
-   Git command failure
-   Repository cloning failure
-   File-access errors
-   Permission errors
-   User cancellation with `Ctrl+C`

Errors are reported through the terminal instead of being left as
unhandled application crashes.

------------------------------------------------------------------------

## 23. Lab Deliverables

The project produces the required artifacts:

  -----------------------------------------------------------------------
  File                                Purpose
  ----------------------------------- -----------------------------------
  `file_metrics.csv`                  File-level source-code dataset

  `git_history_metrics.csv`           Git file-change dataset

  `repository_statistics.json`        Combined machine-readable
                                      repository statistics

  `summary.md`                        Human-readable analysis report

  `README.md`                         Complete project documentation
  -----------------------------------------------------------------------

Expected output:

``` text
output/<repository-name>/
├── file_metrics.csv
├── git_history_metrics.csv
├── repository_statistics.json
└── summary.md
```

------------------------------------------------------------------------

## 24. Future Extensions

The modular architecture allows additional repository-mining
capabilities to be added later, including:

-   Commit activity by contributor
-   Code churn
-   Developer contribution distribution
-   Commit-size distribution
-   File age
-   File ownership
-   Hotspot detection
-   Bug-fix commit identification
-   Repository activity visualization
-   Contributor collaboration networks
-   Historical LOC trends
-   Cyclomatic complexity
-   Code duplication
-   Commit-message analysis
-   Branch analysis

These can be implemented in subsequent labs using the datasets produced
by this project.

------------------------------------------------------------------------

## 25. Quick Reference

### Run

``` bash
cd D:\CSET456Lab\lab1
python -u "src\mine_repository.py"
```

### Input

``` text
GitHub repository URL
```

### Current Repository Analysis

-   Files
-   Directories
-   Source files
-   Languages
-   LOC
-   File sizes
-   File types
-   Largest source files

### Git Analysis

-   All available commits for metadata
-   Contributors
-   Most active contributor
-   Commits per month
-   Latest 400 commits for file changes
-   Additions
-   Deletions
-   Frequently changed files

### Output

``` text
output/<repository-name>/
├── file_metrics.csv
├── git_history_metrics.csv
├── repository_statistics.json
└── summary.md
```

------------------------------------------------------------------------

## 26. Conclusion

This project implements a complete basic **software repository mining
and profiling pipeline**:

``` text
GitHub Repository
       ↓
Repository Acquisition
       ↓
Repository Inventory
       ↓
File-Level Analysis
       ↓
Git History Mining
       ↓
Machine-Readable Datasets
       ↓
Repository Statistics
       ↓
Human-Readable Report
```

The project demonstrates how a software repository can be treated as a
structured source of software-engineering information rather than simply
a collection of source-code files.

The generated datasets and reports provide a foundation for deeper
repository analysis, visualization, and software-engineering research in
subsequent labs.
