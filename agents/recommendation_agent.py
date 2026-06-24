from __future__ import annotations

import json
from typing import List

from core.models import Contradiction, Recommendation, SignalEvent, Theme
from core.parsing import parse_model
from agents.common import build_agent, run_text_agent


def make_recommendation_agent(model: str, instructions: str):
    return build_agent("Recommendation Agent", instructions, model)


async def run_recommendation_analysis(agent, signals: List[SignalEvent], themes: List[Theme], contradictions: List[Contradiction], *, max_turns: int = 8) -> List[Recommendation]:
    prompt = f"""
You are given normalized signal events, themes, and contradictions.
Return a JSON array of 3 to 5 recommendations.

Signals:
{json.dumps([item.model_dump() for item in signals], indent=2)}

Themes:
{json.dumps([item.model_dump() for item in themes], indent=2)}

Contradictions:
{json.dumps([item.model_dump() for item in contradictions], indent=2)}
""".strip()
    text = await run_text_agent(agent, prompt, max_turns=max_turns)
    return parse_model(text, list[Recommendation])
