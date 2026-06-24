from __future__ import annotations

from typing import Any

from agents import Agent, ModelSettings, Runner


async def run_text_agent(agent: Agent, input_text: str, *, max_turns: int = 8) -> str:
    result = await Runner.run(agent, input=input_text, max_turns=max_turns)
    final_output = result.final_output
    if isinstance(final_output, str):
        return final_output
    return str(final_output)


def build_agent(name: str, instructions: str, model: str) -> Agent:
    return Agent(
        name=name,
        instructions=instructions,
        model=model,
        model_settings=ModelSettings(temperature=0.2),
    )
