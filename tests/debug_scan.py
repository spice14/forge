import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from forge.modules.scan import scan_codebase

# Replace with actual path printed from debug_repo.py
repo_path = "E:/Temp/algorithms"  # or wherever it was cloned

scanned = scan_codebase(repo_path)
print("Scanned Output:")
for item in scanned:
    print(f"- {item['file']}")
    for func in item['functions']:
        print(f"   • {func}")
