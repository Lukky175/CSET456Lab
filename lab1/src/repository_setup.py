from pathlib import Path
from urllib.parse import urlparse
import subprocess


# =========================================================
# Paths
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = BASE_DIR / "data" / "repo"


# =========================================================
# Repository Name
# =========================================================

def get_repository_name(url):

    url = url.strip()

    parsed = urlparse(url)

    if parsed.netloc.lower() not in {
        "github.com",
        "www.github.com"
    }:
        raise ValueError(
            "Please enter a valid GitHub repository URL."
        )

    parts = parsed.path.strip("/").split("/")

    if len(parts) < 2:
        raise ValueError(
            "Invalid GitHub repository URL."
        )

    name = parts[-1]

    if name.endswith(".git"):
        name = name[:-4]

    return name


# =========================================================
# Clone Repository
# =========================================================

def clone_repository(url, path):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    print("\nRepository not found locally.")
    print("Cloning repository...")
    print("-" * 70)

    result = subprocess.run(
        [
            "git",
            "clone",
            "--filter=blob:none",
            "--no-tags",
            url,
            str(path)
        ],
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace"
    )

    if result.returncode != 0:

        raise RuntimeError(
            "Repository cloning failed:\n"
            + result.stderr
        )

    print("Repository cloned successfully.")


# =========================================================
# Setup Repository
# =========================================================

def setup_repository(url):

    print("\n" + "=" * 70)
    print("REPOSITORY SETUP")
    print("=" * 70)

    name = get_repository_name(url)

    repository_path = (
        REPO_ROOT / name
    )

    print(
        f"\nRepository URL : {url}"
    )

    print(
        f"Repository Name: {name}"
    )

    print(
        f"Local Path     : {repository_path}"
    )

    # -----------------------------------------------------
    # Existing repository
    # -----------------------------------------------------

    if repository_path.exists():

        if (repository_path / ".git").exists():

            print(
                "\nRepository already exists locally."
            )

            print(
                "Using existing repository."
            )

            return {
                "repository_name": name,
                "repository_path": repository_path,
                "cloned": False
            }

        raise RuntimeError(
            f"{repository_path} exists but is "
            "not a Git repository."
        )

    # -----------------------------------------------------
    # Clone
    # -----------------------------------------------------

    clone_repository(
        url,
        repository_path
    )

    return {
        "repository_name": name,
        "repository_path": repository_path,
        "cloned": True
    }

