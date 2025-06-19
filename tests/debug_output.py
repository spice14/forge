import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from forge.modules.output import write_output

repo_path = "."  # current dir

dummy_results = [
    {
        "file": "example_module.py",
        "function": "is_even",
        "test_code": "def test_is_even():\n    assert is_even(2) is True"
    }
]

write_output(dummy_results, repo_path)
