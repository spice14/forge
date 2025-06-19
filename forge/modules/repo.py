import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# forge/modules/repo.py
import os
import git

def clone_repo(repo_url: str, target_dir: str) -> str:
    """
    Clones a Git repository into a local target directory.

    Args:
        repo_url (str): URL of the Git repository.
        target_dir (str): Temporary or specified directory to clone into.

    Returns:
        str: Path to the cloned repo root.
    """
    repo_name = repo_url.strip().split("/")[-1].replace(".git", "")
    repo_path = os.path.join(target_dir, repo_name)
    git.Repo.clone_from(repo_url, repo_path)
    return repo_path

from pathlib import Path

def extract_code_segment(file_path: Path, start_line: int, end_line: int) -> str:
    """
    Extract lines from a Python file between start_line and end_line (inclusive).
    Lines are 1-indexed to match AST lineno behavior.
    """
    lines = Path(file_path).read_text(encoding="utf-8").splitlines()
    segment = lines[start_line - 1 : end_line]
    return "\n".join(segment)
