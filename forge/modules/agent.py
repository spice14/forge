import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ollama import Client

client = Client(host='http://localhost:11434')

def generate_tests_with_agents(code_data: list) -> list:
    """
    Generates unit tests for scanned functions using Ollama LLM.

    Args:
        code_data (list): Output of scan_codebase - list of dicts with 'file' and 'functions'

    Returns:
        list: Each item is a dict: { 'file': <source_file>, 'function': <name>, 'test_code': <str> }
    """
    results = []
    call_counter = 1

    for item in code_data:
        filepath = item['file']
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                full_code = f.read()
        except Exception as e:
            print(f"[!] Could not read file {filepath}: {e}")
            continue

        for func in item['functions']:
            print(f"[LLM] Generating test #{call_counter} for function '{func}' in file '{filepath}'")

            prompt = (
                f"Write a detailed pytest unit test for the following Python function:\n\n"
                f"Filename: {filepath}\n"
                f"Function: {func}\n\n"
                f"Code:\n```python\n{full_code}\n```"
            )

            try:
                response = client.chat(
                    model='codellama:7b',
                    messages=[{"role": "user", "content": prompt}]
                )
                test_code = response['message']['content']
                results.append({
                    "file": filepath,
                    "function": func,
                    "test_code": test_code.strip()
                })

                print(f"[LLM] ✅ Test #{call_counter} generated successfully.")
            except Exception as e:
                print(f"[!] Failed to generate test for {func} in {filepath}: {e}")

            call_counter += 1

    return results
