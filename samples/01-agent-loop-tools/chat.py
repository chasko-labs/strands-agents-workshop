"""Module 1: Agent Loop + Tools — Dussault with roster/game/stat lookups.

Five tools extract structured data from the 2004 Patriots datasets.
Same pattern as NFL Next Gen Stats feature extraction.

    cd samples/01-agent-loop-tools
    python chat.py                          # uses ollama (default)
    MODEL_PROVIDER=nova python chat.py      # uses AWS Bedrock Nova Pro
"""

import sys

sys.path.insert(0, "../shared")

from dussault_tools import (
    get_coaching_staff,
    get_game_result,
    get_roster_by_position,
    get_season_stats,
    lookup_player,
)
from model_provider import get_model
from strands import Agent

SYSTEM_PROMPT = """You are Dussault, a 2004 New England Patriots dynasty analyst. Your approach is deeply researched, evidence-first, narrative-aware.

- Look up the data before making claims. Never guess stats
- Connect facts to story — why something happened matters as much as what
- If data isn't in tools, establish as an issue to be resolved rather than fabricating
- Be specific: cite game weeks, scores, stat lines, not vague superlatives
- Use inclusive & accessible language — this is for fans who love the team, not a peer-reviewed journal
- Describe players in terms of their role on the team, not isolated glory

Use access to the full 2004 roster (97 players), game-by-game results (19 games),
detailed stats for 9 key contributors, and the coaching staff."""


def main():
    agent = Agent(
        model=get_model(),
        tools=[
            lookup_player,
            get_roster_by_position,
            get_game_result,
            get_season_stats,
            get_coaching_staff,
        ],
        system_prompt=SYSTEM_PROMPT,
    )

    print("2004 Patriots Dynasty Analyst — type 'quit' to exit.")
    print('Try: "Who were the Pro Bowlers on the 2004 team?"')
    print('Or:  "What happened in the AFC Championship game?"\n')

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
