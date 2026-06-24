# Agentic Remix Intelligence Studio

This is a runnable starter prototype for an **Agentic Remix Intelligence Studio**, an AI-native multi-agent system that turns a week of cross-functional company signals into a concise **Weekly Executive Memo** to support strategic leadership decisions.

It uses:
- the **OpenAI Agents SDK** for orchestration
- the **Responses API** through the OpenAI Python SDK
- **GPT-5.4** as the reasoning model
- a fully populated **synthetic dataset** for a fictional company called RelayForge

The prototype is intentionally narrow:
- one use case: **Weekly Executive Signal Mix**
- one week of input signals
- one output memo for leadership

## What it does

The pipeline ingests synthetic records across:
- customer calls
- support tickets
- product feedback
- sales notes
- internal notes

It then runs six agents:
1. Ingestion Agent
2. Theme Agent
3. Contradiction Agent
4. Recommendation Agent
5. Critic Agent
6. Memo Agent

And produces:
- `outputs/normalized_signals.json`
- `outputs/themes.json`
- `outputs/contradictions.json`
- `outputs/recommendations.json`
- `outputs/critique.json`
- `outputs/weekly_decision_mix.md`

## Prerequisites

- Python 3.10+
- An OpenAI API key exported as `OPENAI_API_KEY`

The OpenAI quickstart shows the Python SDK using `client.responses.create(...)`, and its example uses `gpt-5.4` as the model. The Agents SDK docs position the SDK as the orchestration layer on top of model calls and tools. citeturn1view1turn1view0

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configure

```bash
cp .env.example .env
export OPENAI_API_KEY="your_api_key_here"
```

If you want OpenAI tracing in the console, leave tracing enabled. If you want to disable it, export:

```bash
export OPENAI_AGENTS_DISABLE_TRACING=1
```

## Run

```bash
python run.py
```

## Optional flags

```bash
python run.py --max-signals 20
python run.py --output-dir outputs
python run.py --print-final-memo
```

## Files

```text
remix_agents_starter_repo/
├── agents/
├── core/
├── data/
├── outputs/
├── prompts/
├── .env.example
├── README.md
├── requirements.txt
└── run.py
```

## Notes on architecture

This repo uses a **Python-controlled sequential pipeline** with specialist Agents SDK agents at each stage. That keeps the workflow deterministic enough for a one-week prototype while still exercising agent specialization and model-based reasoning.

OpenAI’s agents materials describe both centralized “agent-as-tool” and orchestrated multi-agent workflows as valid patterns, and the SDK supports tools, traces, and multi-step runs. citeturn3view0turn0search0turn2search4

## Suggested next experiments

- swap synthetic data for redacted real artifacts
- add a source diversity score to theme outputs
- add a lightweight evaluator over recommendation quality
- add a small web UI or notebook viewer
