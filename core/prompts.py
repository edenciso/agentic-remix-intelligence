from __future__ import annotations

from pathlib import Path

from core.config import AppConfig
from core.io_utils import read_text


PROMPT_FILES = {
    "ingestion": "ingestion_system.txt",
    "theme": "theme_system.txt",
    "contradiction": "contradiction_system.txt",
    "recommendation": "recommendation_system.txt",
    "critic": "critic_system.txt",
    "memo": "memo_system.txt",
}


def load_prompt(config: AppConfig, name: str) -> str:
    filename = PROMPT_FILES[name]
    return read_text(config.prompts_dir / filename)
