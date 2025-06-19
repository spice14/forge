import typer
import tempfile

from forge.modules.repo import clone_repo
from forge.modules.scan import scan_codebase
from forge.modules.agent import generate_tests_with_agents
from forge.modules.output import write_output
from forge.modules.test_runner import run_tests
from forge.modules.refiner import refine_test

app = typer.Typer()

def main(
    repo_url: str = typer.Argument(..., help="Git repo URL"),
    refine: bool = typer.Option(False, "--refine", help="Enable test refinement using LLM feedback")
):
    print("[+] ForgeTest CLI started.")
    print(f"[+] Cloning repo: {repo_url}")

    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = clone_repo(repo_url, tmpdir)
        print(f"[+] Repo cloned to: {repo_path}")

        print("[+] Scanning codebase...")
        scanned = scan_codebase(repo_path)
        if not scanned:
            print("[!] No functions found.")
            raise typer.Exit()

        print("[+] Generating tests...")
        generated = generate_tests_with_agents(scanned)
        write_output(generated, repo_path)

        print("[+] Running tests...")
        results = run_tests(repo_path)
        print(results['output'])

        if refine and not results['success']:
            print("[!] Tests failed. Refining...")
            refined_tests = []
            for item in generated:
                src_code = open(item['file'], 'r', encoding='utf-8').read()
                refined = refine_test(item['function'], item['test_code'], results['output'], src_code)
                refined_tests.append({
                    "file": item['file'],
                    "function": item['function'],
                    "test_code": refined
                })

            print("[+] Writing refined tests...")
            write_output(refined_tests, repo_path)

            print("[+] Re-running refined tests...")
            refined_results = run_tests(repo_path)
            print(refined_results['output'])

            if refined_results['success']:
                print("[+] All refined tests passed.")
            else:
                print("[!] Refined tests still failed.")
        elif not refine:
            print("[i] Refine disabled. Use --refine to try fixing failed tests.")

        if results.get("coverage_report"):
            print(f"[i] Coverage report: {results['coverage_report']}")

# ✅ Register the command properly
app.command()(main)

if __name__ == "__main__":
    print("[+] Entry point reached")
    app()
