import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""
forge.cli
---------
Entry point: python -m forge.cli <repo-url>
"""

import sys
import tempfile
from pathlib import Path
from forge.modules.agent import generate_tests
from forge.modules.repo import clone_repo
from forge.modules.test_runner import run_tests


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m forge.cli <git-repo-url>")
        sys.exit(1)

    repo_url = sys.argv[1]

    print("[+] ForgeTest CLI started.")
    print(f"[+] Cloning repo: {repo_url}")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        repo_path = clone_repo(repo_url, tmpdir_path)

        if not repo_path:
            print("[!] Failed to clone repository.")
            sys.exit(1)

        print(f"[+] Repo cloned to: {repo_path}")

        tests_dir = repo_path / "tests"
        generate_tests(repo_path, tests_dir)
        run_tests(repo_path, tests_dir)


if __name__ == "__main__":
    main()
