import re
from typing import List

def clean_text(text: str) -> str:
    """Remove extra whitespace and special chars."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def truncate(text: str, max_len: int = 200) -> str:
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."

def chunk_list(lst: list, chunk_size: int) -> List[list]:
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i+chunk_size]
