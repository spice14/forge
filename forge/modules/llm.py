"""
forge.modules.llm
-----------------
Tiny wrapper around Ollama’s HTTP API (or CLI fallback) so the rest of the
project can simply call `llm.generate(prompt)`.
"""

import json
import os
import subprocess
import textwrap
from typing import Optional

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "codellama:3b")

class LLMClient:
    """Very small helper for talking to Ollama."""
    def __init__(self, model: str = MODEL_NAME, base_url: str = OLLAMA_BASE_URL):
        self.model = model
        self.base_url = base_url.rstrip("/")

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def generate(self, prompt: str, temperature: float = 0.2,
                 max_tokens: Optional[int] = None) -> str:
        """
        Send `prompt` to Ollama and return raw text response.

        • Uses subprocess call to `ollama run` for portability;               │
        • Falls back to HTTP POST if `ollama` binary not found.               │
        """

        try:
            completed = subprocess.run(
                ["ollama", "run", self.model, prompt],
                text=True,
                capture_output=True,
                check=True,
                timeout=300,
            )
            return completed.stdout.strip()
        except FileNotFoundError:
            # Fallback to HTTP API
            import requests
            payload = {
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature,
            }
            if max_tokens is not None:
                payload["num_predict"] = max_tokens
            resp = requests.post(f"{self.base_url}/api/generate",
                                 json=payload, timeout=300)
            resp.raise_for_status()
            return resp.json()["response"].strip()

# Single, reusable instance
llm = LLMClient()
