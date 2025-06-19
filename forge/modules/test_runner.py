import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# forge/modules/test_runner.py
import os
import subprocess

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
        return {"success": False, "output": "No tests directory found."}

    command = ["pytest", tests_path, "-v"]
    if with_coverage:
        command = ["coverage", "run", "--source", repo_path, "-m", "pytest", tests_path]

    try:
        result = subprocess.run(command, cwd=repo_path, capture_output=True, text=True)
        output = result.stdout + "\n" + result.stderr

        coverage_report = None
        if with_coverage:
            subprocess.run(["coverage", "html"], cwd=repo_path)
            coverage_report = os.path.join(repo_path, "htmlcov", "index.html")

        return {
            "success": result.returncode == 0,
            "output": output,
            "coverage_report": coverage_report
        }

    except Exception as e:
        return {"success": False, "output": str(e), "coverage_report": None}
 
