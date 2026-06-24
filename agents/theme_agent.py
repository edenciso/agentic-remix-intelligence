from __future__ import annotations

import json
from typing import List

from core.models import SignalEvent, Theme
from core.parsing import parse_model
from agents.common import build_agent, run_text_agent


def make_theme_agent(model: str, instructions: str):
    return build_agent("Theme Agent", instructions, model)


async def run_theme_analysis(agent, signals: List[SignalEvent], prior_week_summary: dict, *, max_turns: int = 8) -> List[Theme]:
    payload = [item.model_dump() for item in signals]
    prompt = f"""
You are given normalized signal events from one week and a lightweight prior week summary.
Return a JSON array of 3 to 5 themes.

Current week signals:
{json.dumps(payload, indent=2)}

Prior week summary:
{json.dumps(prior_week_summary, indent=2)}
""".strip()
    text = await run_text_agent(agent, prompt, max_turns=max_turns)
    return parse_model(text, list[Theme])
