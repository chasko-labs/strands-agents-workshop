"""Interactive multi-turn chat for Module 1: Agent Loop + Tools.

The dynasty analyst agent with tools that query the 2004 New England Patriots
datasets. Each tool extracts one structured data dimension — the same pattern
NFL Next Gen Stats uses (feature extraction -> inference -> output).

From the repo root:

    cd samples/01-agent-loop-tools
    pip install -r requirements.txt
    python chat.py

Type 'quit', 'exit', or press Ctrl+C to stop.
"""

import sys
sys.path.insert(0, "../shared")

from strands import Agent
from strands.models import BedrockModel
from dynasty_tools import lookup_player, get_roster_by_position, get_game_result, get_season_stats, get_coaching_staff

SYSTEM_PROMPT = """You are a 2004 New England Patriots dynasty analyst. Your approach mirrors
the best of patriots.com's coverage — deeply researched, evidence-first, narrative-aware.

When answering:
- Always look up the data before making claims. Never guess stats.
- Connect facts to story — why something happened matters as much as what happened.
- If a question is ambiguous (which game? which player?), ask for clarity.
- If the data isn't in your tools, say so clearly rather than fabricating.
- Be specific: cite game weeks, scores, stat lines, not vague superlatives.
- Make it accessible — this is for fans who love the team, not a peer-reviewed journal.
- Describe players in terms of their role on the team, not isolated glory.

You have access to the full 2004 roster (97 players), game-by-game results (19 games),
detailed stats for 9 key contributors, and the coaching staff."""


def main():
    agent = Agent(
        model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region_name="us-west-2"),
        tools=[lookup_player, get_roster_by_position, get_game_result, get_season_stats, get_coaching_staff],
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
