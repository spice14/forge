import os
import subprocess

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL_NAME", "codellama:3b")

class LLMClient:
    def __init__(self, model=OLLAMA_MODEL):
        self.model = model

    def generate(self, prompt: str, temperature: float = 0.2) -> str:
        try:
            completed = subprocess.run(
                ["ollama", "run", self.model, prompt],
                text=True,
                capture_output=True,
                check=True,
                timeout=300,
            )
            return completed.stdout.strip()
        except Exception as e:
            raise RuntimeError(f"Ollama execution failed: {e}")

llm = LLMClient()
