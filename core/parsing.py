from __future__ import annotations

import json
import re
from typing import Any, Type, TypeVar

from pydantic import BaseModel, TypeAdapter

T = TypeVar("T")


JSON_BLOCK_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)


def extract_json_str(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("{") or stripped.startswith("["):
        return stripped
    match = JSON_BLOCK_RE.search(stripped)
    if match:
        return match.group(1).strip()
    first_brace = stripped.find("{")
    first_bracket = stripped.find("[")
    candidates = [i for i in [first_brace, first_bracket] if i != -1]
    if candidates:
        return stripped[min(candidates):].strip()
    raise ValueError("No JSON payload found in agent output.")


def parse_model(text: str, model_type: Type[T]) -> T:
    payload = json.loads(extract_json_str(text))
    if isinstance(model_type, type) and issubclass(model_type, BaseModel):
        return model_type.model_validate(payload)
    adapter = TypeAdapter(model_type)
    return adapter.validate_python(payload)
