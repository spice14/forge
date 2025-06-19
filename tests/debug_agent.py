import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from forge.modules.agent import generate_tests_with_agents

# Simulate output from scan_codebase()
code_data = [
    {
        "file": "example_module.py",
        "functions": ["is_even"]
    }
]

# Create a dummy file
with open("example_module.py", "w") as f:
    f.write("def is_even(n):\n    return n % 2 == 0\n")

generated = generate_tests_with_agents(code_data)
print("Generated Test Output:")
for test in generated:
    print(test["test_code"])
