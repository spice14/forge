from pathlib import Path
import subprocess

def iter_py_files(repo_root: Path):
    """
    Yield all Python source files recursively within the repo root.
    """
    return repo_root.rglob("*.py")


def extract_code_segment(file_path: Path, start_line: int, end_line: int) -> str:
    """
    Extract lines from a file between start_line and end_line (inclusive).
    """
    lines = Path(file_path).read_text(encoding="utf-8").splitlines()
    return "\n".join(lines[start_line - 1:end_line])

def clone_repo(repo_url: str, destination: Path) -> Path:
    """
    Clone a git repo to the given destination. Returns the root path of the cloned repo.
    """
    try:
        subprocess.run(["git", "clone", repo_url], cwd=destination, check=True)
        repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
        return destination / repo_name
    except Exception as e:
        print(f"[!] Git clone failed: {e}")
        return None
