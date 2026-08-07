"""Module 7: Evals — automated output quality + trajectory evaluation.

Two evaluations:
1. Output eval (LLM-as-judge): accurate and well-formed?
2. Trajectory eval: did the agent follow lookup-before-claim?

Weak-vs-strong agent comparison proves the rubric discriminates.

    cd samples/07-evals
    pip install -r requirements.txt
    python run_evals.py
"""

import sys
sys.path.insert(0, "../shared")
sys.path.insert(0, "../01-agent-loop-tools")

import nest_asyncio
nest_asyncio.apply()

from strands import Agent
from model_provider import get_model
from strands_evals import Case, Experiment
from strands_evals.evaluators import OutputEvaluator, TrajectoryEvaluator
from strands_evals.extractors import tools_use_extractor
from dussault_tools import lookup_player, get_roster_by_position, get_game_result, get_season_stats, get_coaching_staff


# --- Dussault Output Rubric ---

DUSSAULT_RUBRIC = """
Evaluate the Dussault response against the quality standard:

1. Accuracy — Does it contain correct data from the 2004 season? Fabricated
   stats, wrong scores, or invented details must score 0.
2. Specificity — Does it cite specific numbers (stats, scores, game weeks)?
   Vague superlatives ("great season", "amazing player") without data score low.
3. Narrative connection — Does it explain WHY, not just WHAT? Facts connected
   to the team's story score higher than isolated stat dumps.
4. Honesty about unknowns — If the data isn't available, does it say so
   clearly rather than hedging or fabricating?

Score 1.0 if: accurate data + specific citations + narrative context + honest limits.
Score 0.5 if: partially correct or flat stat dump without narrative.
Score 0.0 if: fabricated data, vague claims, or wrong information.
"""


# --- System prompts for weak vs strong agents ---

WEAK_PROMPT = """You are a football analyst. Answer questions about the Patriots.
Do your best even without access to specific data."""

STRONG_PROMPT = """You are Dussault, a 2004 New England Patriots dynasty analyst.
Always look up the data before making claims. Never guess stats.
Be specific: cite game weeks, scores, stat lines.
Connect facts to narrative. Name what's unknown."""


# --- Output Eval Cases ---

output_cases = [
    Case[str, str](
        name="seymour-all-pro",
        input="Was Richard Seymour All-Pro in 2004?",
        expected_output="Yes, Richard Seymour was a 1st Team All-Pro in 2004. He had 5 sacks and 30 tackles as a dominant defensive end.",
    ),
    Case[str, str](
        name="super-bowl-score",
        input="What was the score of Super Bowl XXXIX?",
        expected_output="Patriots 24, Eagles 21. Deion Branch was MVP with 11 catches for 133 yards. Harrison sealed it with an INT with 9 seconds left.",
    ),
    Case[str, str](
        name="dillon-trade",
        input="How did Corey Dillon end up on the 2004 Patriots?",
        expected_output="Dillon was acquired in a trade from Cincinnati before the 2004 draft. He rushed for 1,635 yards (Patriots record) and 12 TDs.",
    ),
    Case[str, str](
        name="unknown-player",
        input="Tell me about Patrick Mahomes on the 2004 Patriots.",
        expected_output="Patrick Mahomes was not on the 2004 Patriots roster. He was born in 1995 and was drafted in 2017.",
    ),
]


# --- Trajectory Eval Cases ---

trajectory_cases = [
    Case[str, str](
        name="player-stat-workflow",
        input="Tell me about Tom Brady's 2004 season stats.",
        expected_output="Brady's 2004 stats looked up via tools.",
        expected_trajectory=["lookup_player", "get_season_stats"],
    ),
    Case[str, str](
        name="game-lookup",
        input="What happened in the AFC Championship?",
        expected_output="AFC Championship result looked up via tools.",
        expected_trajectory=["get_game_result"],
    ),
    Case[str, str](
        name="position-query",
        input="Who played quarterback for the 2004 Patriots?",
        expected_output="QB roster looked up via tools.",
        expected_trajectory=["get_roster_by_position"],
    ),
]


def run_output_evals():
    """Part 1: Output evaluation — weak vs strong agent."""
    print("=" * 60)
    print("PART 1: OUTPUT EVALUATION (Dussault Standard)")
    print("=" * 60)

    output_evaluator = OutputEvaluator(rubric=DUSSAULT_RUBRIC, include_inputs=True)

    # Weak agent — no tools, will guess/fabricate
    print("\n\u274c Weak agent (no tools) — expect LOW scores:")

    def weak_task(case: Case) -> str:
        agent = Agent(
            model=get_model(),
            system_prompt=WEAK_PROMPT,
            callback_handler=None,
        )
        return str(agent(case.input))

    weak_experiment = Experiment[str, str](
        cases=output_cases, evaluators=[output_evaluator]
    )
    weak_report = weak_experiment.run_evaluations(weak_task)
    weak_report.run_display(include_actual_output=True)

    # Strong agent — has tools, will look up real data
    print("\n\u2705 Strong agent (with tools) — expect HIGH scores:")

    def strong_task(case: Case) -> str:
        agent = Agent(
            model=get_model(),
            tools=[lookup_player, get_roster_by_position, get_game_result, get_season_stats, get_coaching_staff],
            system_prompt=STRONG_PROMPT,
            callback_handler=None,
        )
        return str(agent(case.input))

    strong_experiment = Experiment[str, str](
        cases=output_cases, evaluators=[output_evaluator]
    )
    strong_report = strong_experiment.run_evaluations(strong_task)
    strong_report.run_display(include_actual_output=True)

    print(f"\n\U0001f4ca Weak: {weak_report.overall_score:.2f} vs Strong: {strong_report.overall_score:.2f}")
    print("The gap proves the rubric discriminates real knowledge from fabrication.")


def run_trajectory_evals():
    """Part 2: Trajectory evaluation — did it follow the right workflow?"""
    print("\n" + "=" * 60)
    print("PART 2: TRAJECTORY EVALUATION (Lookup-Before-Claim)")
    print("=" * 60)

    trajectory_evaluator = TrajectoryEvaluator(
        rubric="""
        Evaluate whether the agent used the expected tools in the correct order.
        Use the scoring tools provided to verify trajectory matches:
        - The expected tools should appear in order (extra tools between are OK).
        - Score 1.0 if the expected sequence is followed.
        - Score 0.5 if tools are called but in wrong order or incomplete.
        - Score 0.0 if expected tools are missing entirely.
        """,
        include_inputs=True,
    )

    # Build a sample agent to extract tool descriptions for the evaluator
    sample_agent = Agent(
        tools=[lookup_player, get_roster_by_position, get_game_result, get_season_stats, get_coaching_staff]
    )
    tool_descriptions = tools_use_extractor.extract_tools_description(sample_agent, is_short=True)
    trajectory_evaluator.update_trajectory_description(tool_descriptions)

    def trajectory_task(case: Case) -> dict:
        agent = Agent(
            model=get_model(),
            tools=[lookup_player, get_roster_by_position, get_game_result, get_season_stats, get_coaching_staff],
            system_prompt=STRONG_PROMPT,
            callback_handler=None,
        )
        response = agent(case.input)
        trajectory = tools_use_extractor.extract_agent_tools_used_from_messages(agent.messages)
        return {"output": str(response), "trajectory": trajectory}

    print("\n\u2705 Steered agent — expect correct tool sequences:")
    trajectory_experiment = Experiment[str, str](
        cases=trajectory_cases, evaluators=[trajectory_evaluator]
    )
    report = trajectory_experiment.run_evaluations(trajectory_task)
    report.run_display(include_actual_output=True)
    print(f"\n\U0001f4ca Trajectory score: {report.overall_score:.2f}")


if __name__ == "__main__":
    run_output_evals()
    run_trajectory_evals()
    print("\n" + "=" * 60)
    print("EVALUATION COMPLETE")
    print("The Dussault standard catches fabrication. The trajectory eval catches missing guardrails.")
    print("=" * 60)
