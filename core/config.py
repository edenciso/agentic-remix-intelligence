from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class AppConfig:
    model: str = "gpt-5.4"
    company_name: str = "RelayForge"
    week_ending: str = "2026-03-06"
    data_path: Path = Path("data/synthetic_week_01.json")
    prior_week_path: Path = Path("data/prior_week_summary.json")
    prompts_dir: Path = Path("prompts")
    output_dir: Path = Path("outputs")
    max_turns: int = 8


def load_config() -> AppConfig:
    load_dotenv()
    model = os.getenv("OPENAI_MODEL", "gpt-5.4")
    return AppConfig(model=model)
