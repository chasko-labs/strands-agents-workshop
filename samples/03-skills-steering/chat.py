"""Module 3: Skills + Steering — Dussault with workflow skills and guardrails.

AgentSkills loads SKILL.md recipe files. SteeringHandler enforces
fact-check workflow. LLMSteeringHandler evaluates tone.

    cd samples/03-skills-steering
    python chat.py
"""

import sys
sys.path.insert(0, "../shared")
sys.path.insert(0, "../01-agent-loop-tools")

from strands import Agent, AgentSkills
from model_provider import get_model
try:
    from dussault_tools import lookup_player, get_roster_by_position, get_game_result, get_season_stats, get_coaching_staff
except ImportError:
    print("ERROR: Module 01 tools not found.")
    print("       Ensure samples/01-agent-loop-tools/dussault_tools.py exists.")
    print("       Run from this directory: cd samples/NN-[name]")
    sys.exit(1)
try:
    from steering_handlers import FactCheckHandler, tone_handler
except ImportError:
    print("ERROR: steering_handlers.py not found.")
    print("       Ensure samples/03-skills-steering/steering_handlers.py exists.")
    sys.exit(1)

SYSTEM_PROMPT = """You are Dussault, a 2004 New England Patriots dynasty analyst. Your approach is deeply researched, evidence-first, narrative-aware.

- Look up the data before making claims. Never guess stats
- Connect facts to story — why something happened matters as much as what
- If a question is ambiguous, ask for clarity
- If the data isn't in your tools, say so clearly rather than fabricating
- Be specific: cite game weeks, scores, stat lines
- When comparing players or topics, activate the dynasty-debate skill
- When analyzing a game, activate the game-breakdown skill"""


def main():
    agent = Agent(
        model=get_model(),
        tools=[lookup_player, get_roster_by_position, get_game_result, get_season_stats, get_coaching_staff],
        plugins=[
            AgentSkills(skills=["./skills"]),
            FactCheckHandler(),
            tone_handler,
        ],
        system_prompt=SYSTEM_PROMPT,
    )

    print("Dussault (skills + steering) — type 'quit' to exit.")
    print('Try: "Compare Corey Dillon and Deion Branch — who was more important?"\n')

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
