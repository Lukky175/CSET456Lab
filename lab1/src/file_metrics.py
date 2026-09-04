from pathlib import Path
from collections import Counter
import csv


# =========================================================
# Supported Source Languages
# =========================================================

SOURCE_EXTENSIONS = {

    ".py": "Python",
    ".pyx": "Cython",
    ".pxd": "Cython",
    ".pxi": "Cython",

    ".c": "C",
    ".h": "C/C++",
    ".cpp": "C++",
    ".hpp": "C++",

    ".java": "Java",
    ".js": "JavaScript",
    ".ts": "TypeScript",

    ".rs": "Rust",
    ".go": "Go",

    ".f90": "Fortran",
    ".f": "Fortran"
}


# =========================================================
# Count Lines
# =========================================================

def count_lines(path):

    try:

        with open(
            path,
            "rb"
        ) as file:

            return sum(
                1 for _ in file
            )

    except (
        OSError,
        PermissionError
    ):

        return 0


# =========================================================
# Generate File Metrics
# =========================================================

def generate_file_metrics(
    repository_path,
    output_path
):

    repository_path = Path(repository_path)
    output_path = Path(output_path)

    output_path.mkdir(
        parents=True,
        exist_ok=True
    )

    print("\n" + "=" * 70)
    print("FILE-LEVEL REPOSITORY METRICS")
    print("=" * 70)

    # -----------------------------------------------------
    # Find files
    # -----------------------------------------------------

    files = []
    source_files = []
    directories = []

    for path in repository_path.rglob("*"):

        if ".git" in path.parts:
            continue

        if path.is_dir():

            directories.append(path)

        elif path.is_file():

            files.append(path)

            if path.suffix.lower() in SOURCE_EXTENSIONS:

                source_files.append(path)

    # -----------------------------------------------------
    # File types
    # -----------------------------------------------------

    file_types = Counter()

    for path in files:

        extension = (
            path.suffix.lower()
            if path.suffix
            else "[no extension]"
        )

        file_types[extension] += 1

    # -----------------------------------------------------
    # Programming languages
    # -----------------------------------------------------

    languages = Counter()

    for path in source_files:

        extension = path.suffix.lower()

        languages[
            SOURCE_EXTENSIONS[extension]
        ] += 1

    # -----------------------------------------------------
    # File-level records
    # -----------------------------------------------------

    records = []

    for path in source_files:

        extension = path.suffix.lower()

        relative_path = path.relative_to(
            repository_path
        )

        record = {

            "file_path":
                str(relative_path).replace("\\", "/"),

            "language":
                SOURCE_EXTENSIONS[extension],

            "extension":
                extension,

            "loc":
                count_lines(path),

            "size_bytes":
                path.stat().st_size
        }

        records.append(record)

    # -----------------------------------------------------
    # Repository statistics
    # -----------------------------------------------------

    total_loc = sum(
        record["loc"]
        for record in records
    )

    average_loc = (

        total_loc / len(source_files)

        if source_files

        else 0
    )

    # -----------------------------------------------------
    # Largest source files
    # -----------------------------------------------------

    largest_files = sorted(
        records,
        key=lambda item: item["loc"],
        reverse=True
    )[:10]

    # =====================================================
    # CSV
    # =====================================================

    csv_path = (
        output_path /
        "file_metrics.csv"
    )

    with open(
        csv_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "file_path",
                "language",
                "extension",
                "loc",
                "size_bytes"
            ]
        )

        writer.writeheader()

        writer.writerows(records)

    # =====================================================
    # Terminal Output
    # =====================================================

    print(
        f"\nRepository Name       : "
        f"{repository_path.name}"
    )

    print(
        f"Total Files           : "
        f"{len(files):,}"
    )

    print(
        f"Source-Code Files     : "
        f"{len(source_files):,}"
    )

    print(
        f"Directories           : "
        f"{len(directories):,}"
    )

    print(
        f"Total LOC             : "
        f"{total_loc:,}"
    )

    print(
        f"Average LOC/File      : "
        f"{average_loc:,.2f}"
    )

    # -----------------------------------------------------
    # Languages
    # -----------------------------------------------------

    print("\nProgramming Languages")
    print("-" * 40)

    for language, count in (
        languages.most_common()
    ):

        print(
            f"{language:15} : {count}"
        )

    # -----------------------------------------------------
    # File types
    # -----------------------------------------------------

    print("\nFile-Type Distribution")
    print("-" * 40)

    for extension, count in (
        file_types.most_common()
    ):

        print(
            f"{extension:15} : {count}"
        )

    # -----------------------------------------------------
    # Largest files
    # -----------------------------------------------------

    print("\nLargest Source Files")
    print("-" * 60)

    for record in largest_files:

        print(
            f"{record['loc']:7,} LOC  "
            f"{record['file_path']}"
        )

    # -----------------------------------------------------
    # CSV
    # -----------------------------------------------------

    print("\nFile-Level Dataset")
    print("-" * 60)

    print(
        f"CSV created : {csv_path}"
    )

    print(
        f"Records     : {len(records):,}"
    )

    return {

        "repository_name":
            repository_path.name,

        "total_files":
            len(files),

        "source_code_files":
            len(source_files),

        "directories":
            len(directories),

        "total_loc":
            total_loc,

        "average_loc_per_source_file":
            round(
                average_loc,
                2
            ),

        "programming_languages":
            dict(
                languages.most_common()
            ),

        "file_type_distribution":
            dict(
                file_types.most_common()
            ),

        "largest_source_files":
            largest_files,

        "file_metrics_csv":
            str(csv_path)
    }

