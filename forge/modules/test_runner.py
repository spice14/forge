import subprocess
from pathlib import Path
from typing import Dict

def save_test_file(fn_meta: Dict, test_code: str, tests_dir: Path) -> None:
    tests_dir.mkdir(parents=True, exist_ok=True)
    stem = Path(fn_meta["filepath"]).stem
    outfile = tests_dir / f"test_{stem}.py"
    with outfile.open("a", encoding="utf-8") as f:
        f.write(test_code.strip() + "\n\n")


def run_tests(repo_root: Path, tests_dir: Path) -> None:
    cov_target = repo_root
    cmd = [
        "pytest",
        "--cov-report", "term-missing",
        f"--cov={cov_target}",
        str(tests_dir),
    ]
    print("[+] Running tests (with coverage)…")
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        print("[!] coverage.py not installed – falling back to plain pytest")
        subprocess.run(["pytest", str(tests_dir)], check=True)
