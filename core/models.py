from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, conint, confloat


SourceType = Literal[
    "customer_call",
    "support_ticket",
    "product_feedback",
    "sales_note",
    "internal_note",
]

SentimentType = Literal["positive", "mixed", "negative", "neutral"]
PriorityType = Literal["high", "medium", "low"]
ChangeType = Literal["up", "flat", "down", "unknown"]


class SignalEvent(BaseModel):
    id: str
    source_type: SourceType
    date: str
    team: str
    account_name: Optional[str] = None
    account_segment: str
    region: Optional[str] = None
    topic_tags: List[str]
    summary: str
    sentiment: SentimentType
    urgency: conint(ge=1, le=5)
    evidence_strength: conint(ge=1, le=5)
    quoted_claims: Optional[List[str]] = None
    metrics: Optional[Dict[str, Any]] = None
    owner: Optional[str] = None


class Theme(BaseModel):
    theme: str
    supporting_signal_ids: List[str]
    source_diversity: List[str]
    source_diversity_score: confloat(ge=0, le=1)
    signal_count: conint(ge=1)
    strength: confloat(ge=0, le=1)
    change_vs_prior_week: ChangeType
    explanation: str


class Contradiction(BaseModel):
    contradiction: str
    evidence_for_conflict: List[str]
    severity: confloat(ge=0, le=1)
    teams_involved: List[str]
    explanation: str


class Recommendation(BaseModel):
    recommendation: str
    rationale: str
    confidence: confloat(ge=0, le=1)
    supporting_signal_ids: List[str]
    priority: PriorityType


class Critique(BaseModel):
    strengths: List[str]
    caveats: List[str]
    weak_points: List[str]
    confidence_adjustments: Dict[str, confloat(ge=0, le=1)] = Field(default_factory=dict)


class WeeklyDecisionMix(BaseModel):
    company: str
    week_ending: str
    top_themes: List[str]
    what_changed: List[str]
    contradictions: List[str]
    recommended_actions: List[str]
    confidence_and_caveats: List[str]
    evidence_trail: List[str]
