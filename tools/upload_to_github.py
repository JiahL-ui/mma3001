"""Upload all project artefacts (source, tests, docs, notebook) to GitHub.

This consolidates and FIXES the notebook's final upload cells, which had a
real bug that would crash on execution:

    repo_local_path = f"/content/{mma3001}"
    clone_url = f"https://{GH_PAT}@github.com/{JiahL-ui}/{mma3001}.git"

`mma3001`, `GH_PAT`, and `JiahL-ui` were used as bare names inside an
f-string instead of quoted strings or the already-defined variables
(`REPOSITORY_NAME`, `GIT_TOKEN`, `GITHUB_USERNAME`), which raises
`NameError: name 'mma3001' is not defined` the moment it runs.

This script uses the correctly-named variables throughout and copies
files into the structured layout (src/, tests/, docs/, tools/) instead
of the previous ad-hoc `source/`, `test/` naming.

Intended to be run from Colab, where `google.colab.userdata` provides
the GitHub Personal Access Token (PAT). Configure a secret named
`GH_PAT` in Colab's Secrets panel before running.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

# --- Configuration — edit these for your own repo -------------------------
GITHUB_USERNAME = "your_github_username"      # <-- replace
REPOSITORY_NAME = "your_repo_name"            # <-- replace
NOTEBOOK_FILENAME = "Workshop_01_2026.ipynb"  # <-- replace with your actual notebook name

CONTENT_ROOT = Path("/content")
LOCAL_REPO_PATH = CONTENT_ROOT / REPOSITORY_NAME


def get_github_token() -> str:
    """Fetch the GitHub PAT from Colab Secrets (falls back to env var)."""
    try:
        from google.colab import userdata  # type: ignore

        token = userdata.get("GH_PAT")
        if token:
            return token
    except ImportError:
        pass

    token = os.environ.get("GH_PAT")
    if not token:
        raise RuntimeError(
            "GitHub token not found. Set a Colab secret named 'GH_PAT', "
            "or export GH_PAT as an environment variable."
        )
    return token


def run(cmd: str, cwd: Path | None = None) -> None:
    """Run a shell command, raising on failure instead of failing silently."""
    print(f"$ {cmd}")
    subprocess.run(cmd, shell=True, check=True, cwd=cwd)


def clone_repository(token: str) -> None:
    """Clone the target repository, replacing any existing local copy."""
    if LOCAL_REPO_PATH.exists():
        shutil.rmtree(LOCAL_REPO_PATH)

    clone_url = f"https://{token}@github.com/{GITHUB_USERNAME}/{REPOSITORY_NAME}.git"
    run(f"git clone {clone_url} {LOCAL_REPO_PATH}")
    print(f"Repository cloned to: {LOCAL_REPO_PATH}")


def copy_project_files(project_root: Path) -> None:
    """Copy src/, tests/, docs/, tools/, and the notebook into the repo.

    Args:
        project_root: Local directory containing the organised project
            (the structure produced alongside this script: src/, tests/,
            docs/, tools/, data/, examples/).
    """
    folders_to_sync = ["src", "tests", "docs", "tools", "data", "examples"]

    for folder in folders_to_sync:
        source = project_root / folder
        if not source.exists():
            continue
        destination = LOCAL_REPO_PATH / folder
        shutil.copytree(source, destination, dirs_exist_ok=True)
        print(f"Copied {source} -> {destination}")

    notebook_source = CONTENT_ROOT / NOTEBOOK_FILENAME
    if notebook_source.exists():
        shutil.copy2(notebook_source, LOCAL_REPO_PATH / NOTEBOOK_FILENAME)
        print(f"Copied notebook -> {LOCAL_REPO_PATH / NOTEBOOK_FILENAME}")
    else:
        print(f"Warning: notebook not found at {notebook_source}, skipping.")


def commit_and_push(commit_message: str = "Add organised project structure") -> None:
    """Stage, commit, and push all changes on the current branch."""
    status = subprocess.run(
        "git status --porcelain", shell=True, cwd=LOCAL_REPO_PATH,
        capture_output=True, text=True,
    ).stdout.strip()

    if not status:
        print("Nothing to commit — working tree is clean.")
        return

    run("git add .", cwd=LOCAL_REPO_PATH)
    run(f'git commit -m "{commit_message}"', cwd=LOCAL_REPO_PATH)
    run("git push origin main", cwd=LOCAL_REPO_PATH)
    print("Push complete.")


def main() -> None:
    token = get_github_token()
    clone_repository(token)
    copy_project_files(project_root=Path.cwd())
    commit_and_push()


if __name__ == "__main__":
    main()
