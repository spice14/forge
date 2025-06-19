import sys
import os
import subprocess
import shutil

# Ensure import path includes project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def find_source_dir(repo_path):
    """
    Heuristically finds the main source directory inside a repo.
    """
    common_candidates = ['src', 'source', 'my_pkg', 'app']
    for candidate in common_candidates:
        candidate_path = os.path.join(repo_path, candidate)
        if os.path.isdir(candidate_path):
            return candidate
    return '.'  # fallback to root

def run_tests(repo_path: str, with_coverage: bool = True) -> dict:
    """
    Runs tests using pytest (with or without coverage) inside the given repo.

    Args:
        repo_path (str): Root of the cloned repo
        with_coverage (bool): Whether to measure test coverage

    Returns:
        dict: Contains success flag, test output, and optional coverage report path
    """
    tests_path = os.path.join(repo_path, 'tests')
    if not os.path.exists(tests_path):
        return {"success": False, "output": "[!] No tests directory found.", "coverage_report": None}

    # Try to find the correct source directory
    source_dir = find_source_dir(repo_path)

    # Check if 'coverage' is available
    use_coverage = with_coverage and shutil.which("coverage") is not None

    if use_coverage:
        command = [
            "pytest",
            "--cov-report", "term-missing",
            f"--cov={source_dir}",
            "tests"
        ]
    else:
        if with_coverage:
            print("[!] 'coverage' not found — falling back to plain pytest.")
            print("    Tip: Install it with 'pip install coverage' and add to PATH.\n")
        command = ["pytest", "tests", "-v"]

    try:
        result = subprocess.run(
            command,
            cwd=repo_path,
            capture_output=True,
            text=True,
            shell=True  # ensures it works on Windows with PATH resolution
        )

        output = result.stdout + "\n" + result.stderr

        coverage_report = None
        if use_coverage:
            subprocess.run(["coverage", "html"], cwd=repo_path)
            coverage_report = os.path.join(repo_path, "htmlcov", "index.html")

        return {
            "success": result.returncode == 0,
            "output": output,
            "coverage_report": coverage_report
        }

    except FileNotFoundError as e:
        return {
            "success": False,
            "output": f"[!] '{e.filename}' not found — is it installed and on your PATH?\n\n"
                      f"Fix:\n  - Try running the command manually: {' '.join(command)}\n"
                      f"  - Or add it to your PATH.",
            "coverage_report": None
        }

    except Exception as e:
        return {
            "success": False,
            "output": f"[!] Unexpected error while running tests:\n{str(e)}",
            "coverage_report": None
        }
