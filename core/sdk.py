from __future__ import annotations

import os
from typing import Optional

from agents import set_default_openai_client
from openai import AsyncOpenAI


def configure_openai_client(timeout_seconds: float = 180.0) -> AsyncOpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY is not set. Export it before running this project."
        )
    client = AsyncOpenAI(api_key=api_key, timeout=timeout_seconds)
    set_default_openai_client(client)
    return client
