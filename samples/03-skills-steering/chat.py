"""Module 3: Skills + Steering — dynasty analyst with workflow skills and guardrails.

Demonstrates:
- AgentSkills plugin loading SKILL.md recipe files
- SteeringHandler (deterministic fact-check workflow)
- LLMSteeringHandler (Dussault tone evaluation)

From the repo root:
    cd samples/03-skills-steering
    python chat.py
"""

import sys
sys.path.insert(0, "../shared")
sys.path.insert(0, "../01-agent-loop-tools")

from strands import Agent, AgentSkills
from strands.models import BedrockModel
from dynasty_tools import lookup_player, get_roster_by_position, get_game_result, get_season_stats, get_coaching_staff
from steering_handlers import FactCheckHandler, tone_handler

SYSTEM_PROMPT = """You are a 2004 New England Patriots dynasty analyst. Your approach mirrors
the best of patriots.com's coverage — evidence-first, narrative-aware.

When answering:
- Always look up the data before making claims. Never guess stats.
- Connect facts to story — why something happened matters as much as what happened.
- If a question is ambiguous, ask for clarity.
- If the data isn't in your tools, say so clearly rather than fabricating.
- Be specific: cite game weeks, scores, stat lines.
- When comparing players or topics, activate the dynasty-debate skill.
- When analyzing a game, activate the game-breakdown skill."""


def main():
    agent = Agent(
        model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region_name="us-west-2"),
        tools=[lookup_player, get_roster_by_position, get_game_result, get_season_stats, get_coaching_staff],
        plugins=[
            AgentSkills(skills=["./skills"]),
            FactCheckHandler(),
            tone_handler,
        ],
        system_prompt=SYSTEM_PROMPT,
    )

    print("2004 Patriots Dynasty Analyst (skills + steering) — type 'quit' to exit.")
    print('Try: "Compare Corey Dillon and Deion Branch — who was more important?"')
    print('Or:  "Break down the AFC Championship game for me."\n')

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_input.lower() in {"quit", "exit", "q"}:
            print("Goodbye!")
            break
        if not user_input:
            continue

        print("\nAnalyst: ", end="")
        agent(user_input)
        print()


if __name__ == "__main__":
    main()
