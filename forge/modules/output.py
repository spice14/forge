import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# forge/modules/output.py
import os

def write_output(test_results: list, repo_path: str) -> None:
    """
    Writes generated test code into a /tests/ directory inside the cloned repo.

    Args:
        test_results (list): Output from agent.py - list of dicts with 'file', 'function', 'test_code'
        repo_path (str): Path to the root of the cloned repo
    """
    tests_dir = os.path.join(repo_path, 'tests')
    os.makedirs(tests_dir, exist_ok=True)

    for result in test_results:
        src_file = os.path.basename(result['file']).replace('.py', '')
        test_filename = f"test_{src_file}.py"
        test_path = os.path.join(tests_dir, test_filename)

        # Append mode — allows multiple functions from the same file
        with open(test_path, 'a', encoding='utf-8') as f:
            f.write("\n\n")
            f.write(result['test_code'])
            f.write("\n")

    print(f"[✓] Generated test cases saved to: {tests_dir}")
 
