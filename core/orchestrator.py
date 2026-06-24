from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
from typing import Sequence

from agents import trace

from agents.contradiction_agent import make_contradiction_agent, run_contradiction_analysis
from agents.critic_agent import make_critic_agent, run_critique
from agents.ingestion_agent import make_ingestion_agent, run_ingestion
from agents.memo_agent import make_memo_agent, run_memo
from agents.recommendation_agent import make_recommendation_agent, run_recommendation_analysis
from agents.theme_agent import make_theme_agent, run_theme_analysis
from core.config import AppConfig, load_config
from core.io_utils import ensure_dir, read_json, write_json, write_text
from core.prompts import load_prompt
from core.sdk import configure_openai_client


async def run_pipeline(config: AppConfig, max_signals: int | None = None, print_final_memo: bool = False) -> Path:
    configure_openai_client()
    ensure_dir(config.output_dir)

    raw_signals = read_json(config.data_path)
    if max_signals is not None:
        raw_signals = raw_signals[:max_signals]
    prior_week_summary = read_json(config.prior_week_path)

    ingestion_agent = make_ingestion_agent(config.model, load_prompt(config, "ingestion"))
    theme_agent = make_theme_agent(config.model, load_prompt(config, "theme"))
    contradiction_agent = make_contradiction_agent(config.model, load_prompt(config, "contradiction"))
    recommendation_agent = make_recommendation_agent(config.model, load_prompt(config, "recommendation"))
    critic_agent = make_critic_agent(config.model, load_prompt(config, "critic"))
    memo_agent = make_memo_agent(config.model, load_prompt(config, "memo"))

    with trace("Remix Weekly Decision Mix", metadata={"company": config.company_name, "week_ending": config.week_ending}):
        normalized_signals = await run_ingestion(ingestion_agent, raw_signals, max_turns=config.max_turns)
        write_json(config.output_dir / "normalized_signals.json", [item.model_dump() for item in normalized_signals])

        themes = await run_theme_analysis(theme_agent, normalized_signals, prior_week_summary, max_turns=config.max_turns)
        write_json(config.output_dir / "themes.json", [item.model_dump() for item in themes])

        contradictions = await run_contradiction_analysis(
            contradiction_agent,
            normalized_signals,
            themes,
            max_turns=config.max_turns,
        )
        write_json(config.output_dir / "contradictions.json", [item.model_dump() for item in contradictions])

        recommendations = await run_recommendation_analysis(
            recommendation_agent,
            normalized_signals,
            themes,
            contradictions,
            max_turns=config.max_turns,
        )
        write_json(config.output_dir / "recommendations.json", [item.model_dump() for item in recommendations])

        critique = await run_critique(
            critic_agent,
            themes,
            contradictions,
            recommendations,
            max_turns=config.max_turns,
        )
        write_json(config.output_dir / "critique.json", critique.model_dump())

        memo = await run_memo(
            memo_agent,
            company=config.company_name,
            week_ending=config.week_ending,
            themes=themes,
            contradictions=contradictions,
            recommendations=recommendations,
            critique=critique,
            max_turns=config.max_turns,
        )
        memo_path = config.output_dir / "weekly_decision_mix.md"
        write_text(memo_path, memo)

    if print_final_memo:
        print("\n" + memo)

    return memo_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Remix Intelligence Studio multi-agent MVP.")
    parser.add_argument("--max-signals", type=int, default=None, help="Optionally limit the number of synthetic records.")
    parser.add_argument("--output-dir", type=str, default=None, help="Override the output directory.")
    parser.add_argument("--print-final-memo", action="store_true", help="Print the final memo to stdout.")
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = load_config()
    if args.output_dir:
        config = AppConfig(
            model=config.model,
            company_name=config.company_name,
            week_ending=config.week_ending,
            data_path=config.data_path,
            prior_week_path=config.prior_week_path,
            prompts_dir=config.prompts_dir,
            output_dir=Path(args.output_dir),
            max_turns=config.max_turns,
        )
    memo_path = asyncio.run(
        run_pipeline(
            config,
            max_signals=args.max_signals,
            print_final_memo=args.print_final_memo,
        )
    )
    print(f"\nRun complete. Final memo written to: {memo_path}")
