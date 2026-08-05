"""Module 2: Hooks — dynasty analyst with analytics tracking.

Demonstrates HookProvider lifecycle hooks:
- BeforeInvocationEvent: reset tracking at start of each turn
- BeforeToolCallEvent: track queries, detect repeats, enforce cite-your-source

From the repo root:
    cd samples/02-hooks
    python chat.py
"""

import sys
sys.path.insert(0, "../shared")

from strands import Agent
from strands.models import BedrockModel
from strands.hooks import HookProvider, HookRegistry, BeforeInvocationEvent, BeforeToolCallEvent

# Import tools from module 01
sys.path.insert(0, "../01-agent-loop-tools")
from dynasty_tools import lookup_player, get_roster_by_position, get_game_result, get_season_stats, get_coaching_staff


class DynastyAnalyticsHook(HookProvider):
    """Tracks analysis patterns and blocks repeat lookups.
    
    Like NGS CloudWatch monitoring every inference — this hook observes
    every tool call, tracks what's been queried, and prevents redundant lookups.
    """

    def __init__(self):
        self.queried_players: set = set()
        self.queried_games: set = set()
        self.tool_count: int = 0

    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(BeforeInvocationEvent, self.reset_turn)
        registry.add_callback(BeforeToolCallEvent, self.track_and_gate)

    def reset_turn(self, event: BeforeInvocationEvent) -> None:
        """Reset per-turn counters. Keeps cross-turn memory of queried players."""
        self.tool_count = 0
        print(f"[ANALYTICS] \U0001f4ca Session state: {len(self.queried_players)} players queried, {len(self.queried_games)} games reviewed")

    def track_and_gate(self, event: BeforeToolCallEvent) -> None:
        """Track queries and block repeat lookups."""
        name = event.tool_use["name"]
        args = event.tool_use.get("input", {})
        self.tool_count += 1

        print(f"[ANALYTICS] \U0001f50d Tool call #{self.tool_count}: {name}({args})")

        # Track and gate player lookups
        if name == "lookup_player":
            player = args.get("player_name", "").lower()
            if player in self.queried_players:
                event.cancel_tool = (
                    f"Already looked up '{player}' this session. "
                    "Use the information from the previous lookup instead of repeating it."
                )
                print(f"[ANALYTICS] \U0001f6ab BLOCKED: repeat lookup for '{player}'")
                return
            self.queried_players.add(player)

        # Track game queries
        if name == "get_game_result":
            week = args.get("week", "")
            if week in self.queried_games:
                event.cancel_tool = (
                    f"Already reviewed week {week} this session. "
                    "Reference the earlier result instead of re-querying."
                )
                print(f"[ANALYTICS] \U0001f6ab BLOCKED: repeat game lookup for week {week}")
                return
            self.queried_games.add(week)

        # Depth warning
        if self.tool_count > 5:
            print(f"[ANALYTICS] \u26a0\ufe0f  High analysis depth: {self.tool_count} tools this turn")


SYSTEM_PROMPT = """You are a 2004 New England Patriots dynasty analyst. Your approach mirrors
the best of patriots.com's coverage — evidence-first, narrative-aware.

When answering:
- Always look up the data before making claims. Never guess stats.
- Connect facts to story — why something happened matters as much as what happened.
- Be specific: cite game weeks, scores, stat lines.
- Describe players in terms of their role on the team."""


def main():
    agent = Agent(
        model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region_name="us-west-2"),
        tools=[lookup_player, get_roster_by_position, get_game_result, get_season_stats, get_coaching_staff],
        hooks=[DynastyAnalyticsHook()],
        system_prompt=SYSTEM_PROMPT,
    )

    print("2004 Patriots Dynasty Analyst (with analytics hooks) — type 'quit' to exit.")
    print("Try asking about the same player twice to see the repeat-query blocker.")
    print('Or:  "Compare Brady and Dillon\'s seasons" to see analysis depth tracking.\n')

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
