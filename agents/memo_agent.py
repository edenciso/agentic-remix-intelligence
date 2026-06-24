from __future__ import annotations

import json
from typing import List

from core.models import Contradiction, Critique, Recommendation, Theme
from agents.common import build_agent, run_text_agent


def make_memo_agent(model: str, instructions: str):
    return build_agent("Memo Agent", instructions, model)


async def run_memo(agent, *, company: str, week_ending: str, themes: List[Theme], contradictions: List[Contradiction], recommendations: List[Recommendation], critique: Critique, max_turns: int = 8) -> str:
    prompt = f"""
Create a concise markdown Weekly Decision Mix memo for leadership.

Company: {company}
Week ending: {week_ending}

Themes:
{json.dumps([item.model_dump() for item in themes], indent=2)}

Contradictions:
{json.dumps([item.model_dump() for item in contradictions], indent=2)}

Recommendations:
{json.dumps([item.model_dump() for item in recommendations], indent=2)}

Critique:
{json.dumps(critique.model_dump(), indent=2)}
""".strip()
    return await run_text_agent(agent, prompt, max_turns=max_turns)
