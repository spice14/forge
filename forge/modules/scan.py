# forge/modules/scan.py
import os
import ast

def scan_codebase(repo_path: str) -> list:
    """
    Scans a Python codebase and collects function definitions.

    Args:
        repo_path (str): Path to the cloned repo.

    Returns:
        list of dicts: [{ "file": <path>, "functions": [<func_name>, ...] }]
    """
    results = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py") and "test" not in file.lower():
                full_path = os.path.join(root, file)
                with open(full_path, "r", encoding="utf-8") as f:
                    try:
                        tree = ast.parse(f.read(), filename=full_path)
                        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                        if functions:
                            results.append({"file": full_path, "functions": functions})
                    except Exception as e:
                        print(f"[!] Failed to parse {full_path}: {e}")
    return results
 
