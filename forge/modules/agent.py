import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""
forge.modules.agent
-------------------
High-level orchestration: scan repo, call LLM for test generation,
write tests to disk.
"""

from pathlib import Path
from forge.modules.utils import load_prompt
from forge.modules.repo import extract_code_segment, iter_py_files
from forge.modules.scan import get_function_spans
from forge.modules.test_runner import save_test_file
from forge.modules.llm import llm


def generate_tests(repo_root: Path, tests_dir: Path) -> None:
    print("[+] Scanning codebase…")
    py_files = list(iter_py_files(repo_root))

    base_prompt = load_prompt("base_prompt.txt")

    for file_path in py_files:
        for fn_meta in get_function_spans(file_path):
            code_block = extract_code_segment(
                file_path, fn_meta["start_line"], fn_meta["end_line"]
            )
            prompt = base_prompt.replace("{code}", code_block)

            print(f"[LLM] Generating test for {fn_meta['qualified_name']} "
                  f"in {file_path.relative_to(repo_root)}")

            raw = llm.generate(prompt)
            cleaned = _clean_llm_output(raw)

            try:
                compile(cleaned, "<generated test>", "exec")
            except SyntaxError as e:
                print(f"[!] Invalid Python generated for "
                      f"{fn_meta['qualified_name']}: {e}")
                continue

            save_test_file(fn_meta, cleaned, tests_dir)

    print(f"[✓] Generated tests saved to: {tests_dir}")


def _clean_llm_output(text: str) -> str:
    for fence in ("```python", "```py", "```"):
        text = text.replace(fence, "")
    return text.strip() + "\n"
