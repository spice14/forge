import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from forge.modules.repo import clone_repo
import tempfile

repo_url = "https://github.com/keon/algorithms.git"

with tempfile.TemporaryDirectory() as tmpdir:
    path = clone_repo(repo_url, tmpdir)
    print(f"Repo cloned to: {path}")
