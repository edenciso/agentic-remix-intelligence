from __future__ import annotations

import json
from typing import List

from core.models import SignalEvent
from core.parsing import parse_model
from agents.common import build_agent, run_text_agent


def make_ingestion_agent(model: str, instructions: str):
    return build_agent("Ingestion Agent", instructions, model)


async def run_ingestion(agent, raw_signals: list[dict], *, max_turns: int = 8) -> List[SignalEvent]:
    prompt = f"""
Normalize the following weekly company artifacts into a JSON array of canonical signal events.

Return JSON only.

Raw input records:
{json.dumps(raw_signals, indent=2)}
""".strip()
    text = await run_text_agent(agent, prompt, max_turns=max_turns)
    return parse_model(text, list[SignalEvent])
