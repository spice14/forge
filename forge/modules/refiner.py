# forge/modules/refiner.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ollama import Client

client = Client(host='http://localhost:11434')

def refine_test(function_name: str, original_test: str, error_output: str, source_code: str) -> str:
    """
    Uses LLM to refine a broken test using feedback from test execution.

    Args:
        function_name (str): Name of the function being tested
        original_test (str): The original failing test code
        error_output (str): Pytest error output
        source_code (str): Full source code of the module

    Returns:
        str: Refined test code
    """
    prompt = (
        f"The following unit test for a Python function failed during execution.\n"
        f"Function name: {function_name}\n\n"
        f"Original test:\n```python\n{original_test}\n```\n\n"
        f"Error output:\n```\n{error_output}\n```\n\n"
        f"Here is the original source code:\n```python\n{source_code}\n```\n\n"
        f"Please revise the test code to fix the error(s) and ensure it passes."
    )

    try:
        response = client.chat(
            model='codellama:7b',
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content'].strip()
    except Exception as e:
        print(f"[!] Failed to refine test: {e}")
        return original_test
