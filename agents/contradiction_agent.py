from __future__ import annotations

import json
from typing import List

from core.models import Contradiction, SignalEvent, Theme
from core.parsing import parse_model
from agents.common import build_agent, run_text_agent


def make_contradiction_agent(model: str, instructions: str):
    return build_agent("Contradiction Agent", instructions, model)


async def run_contradiction_analysis(agent, signals: List[SignalEvent], themes: List[Theme], *, max_turns: int = 8) -> List[Contradiction]:
    prompt = f"""
You are given normalized signal events and extracted themes.
Return a JSON array of 2 to 4 contradictions.

Signals:
{json.dumps([item.model_dump() for item in signals], indent=2)}

Themes:
{json.dumps([item.model_dump() for item in themes], indent=2)}
""".strip()
    text = await run_text_agent(agent, prompt, max_turns=max_turns)
    return parse_model(text, list[Contradiction])
