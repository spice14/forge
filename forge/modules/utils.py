from pathlib import Path

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

def load_prompt(name: str) -> str:
    """
    Load a prompt template from the prompts/ directory.
    
    Args:
        name: filename (e.g. "base_prompt.txt")
    
    Returns:
        The prompt template as a string.
    """
    path = PROMPTS_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    
    return path.read_text(encoding="utf-8")
 
