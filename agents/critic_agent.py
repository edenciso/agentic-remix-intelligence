from __future__ import annotations

import json
from typing import List

from core.models import Contradiction, Critique, Recommendation, Theme
from core.parsing import parse_model
from agents.common import build_agent, run_text_agent


def make_critic_agent(model: str, instructions: str):
    return build_agent("Critic Agent", instructions, model)


async def run_critique(agent, themes: List[Theme], contradictions: List[Contradiction], recommendations: List[Recommendation], *, max_turns: int = 8) -> Critique:
    prompt = f"""
You are reviewing outputs from the strategy interpretation system.
Return a single JSON object with strengths, caveats, weak_points, and confidence_adjustments.

Themes:
{json.dumps([item.model_dump() for item in themes], indent=2)}

Contradictions:
{json.dumps([item.model_dump() for item in contradictions], indent=2)}

Recommendations:
{json.dumps([item.model_dump() for item in recommendations], indent=2)}
""".strip()
    text = await run_text_agent(agent, prompt, max_turns=max_turns)
    return parse_model(text, Critique)
