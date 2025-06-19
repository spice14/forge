import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from forge.modules.test_runner import run_tests

repo_path = "."  # Assuming tests/ exists here

results = run_tests(repo_path)
print("Test Runner Output:")
print(results['output'])
print("Coverage Report:", results.get("coverage_report"))
