"""Steering handlers for Module 3: Skills + Steering.

Two handlers:
1. FactCheckHandler (deterministic) — enforces lookup-before-claim workflow
2. DussaultToneHandler (LLM-based) — ensures output meets the Dussault standard
"""

import re

from strands.vended_plugins.steering import (
    SteeringHandler, LLMSteeringHandler,
    Proceed, Guide, ToolSteeringAction,
    LedgerProvider,
)


class FactCheckHandler(SteeringHandler):
    """Deterministic handler: enforce lookup-before-claim workflow.

    Rules:
    1. Must look up a player (lookup_player or get_season_stats) before
       the agent can make claims about them in its response.
    2. Must get_game_result before making claims about a specific game.

    This mirrors NGS human-in-the-loop: the broadcast director (steering)
    ensures the system doesn't output unchecked inference.
    """

    name = "fact-check"

    def __init__(self):
        super().__init__(context_providers=[LedgerProvider()])

    async def steer_before_tool(self, *, agent, tool_use, **kwargs) -> ToolSteeringAction:
        """For now, just log. The real enforcement happens on get_season_stats."""
        if tool_use.get("name") != "get_season_stats":
            return Proceed(reason="Not a stats query")

        print("[FACT-CHECK] \U0001f50d Stats query attempted — checking if player was looked up first...")

        ledger = self.steering_context.data.get("ledger", {})
        tool_calls = ledger.get("tool_calls", [])

        # Check if lookup_player was called for this player first
        player_name = tool_use.get("input", {}).get("player_name", "").lower()
        player_verified = any(
            c["tool_name"] == "lookup_player" and c["status"] == "success"
            and player_name in str(c.get("result", "")).lower()
            for c in tool_calls
        )

        if not player_verified:
            print(f"[FACT-CHECK] \u26a0\ufe0f  Guided: look up '{player_name}' first")
            return Guide(
                reason=f"Look up the player with lookup_player before pulling their stats. "
                f"This ensures you're referencing a verified 2004 roster member."
            )

        print("[FACT-CHECK] \u2705 Player verified — proceeding with stats lookup")
        return Proceed(reason="Player previously verified via lookup")


class DussaultToneHandler(LLMSteeringHandler):
    """LLM-based handler: evaluate output against the Dussault standard.

    Uses a secondary LLM call to check if the agent's response meets
    the quality bar — evidence-first, narrative-aware, specific citations.
    """

    name = "dussault-tone"

    def __init__(self):
        super().__init__(
            system_prompt="""You are evaluating a sports analyst's responses against
the Mike Dussault standard (patriots.com). Check for:

- Does the response cite specific data (stats, scores, game weeks)?
- Does it connect facts to narrative (why, not just what)?
- Does it avoid vague superlatives ("great", "amazing", "arguably")?
- Does it name what's unknown rather than hedging?
- Does it describe players in terms of team function?

If the response uses vague language without specific citations, or makes
claims without data backing, provide specific guidance on what to fix.
If it meets the standard, proceed."""
        )

    async def steer_after_model(self, **kwargs):
        print("[TONE] \U0001f50d Evaluating against Dussault standard...")
        result = await super().steer_after_model(**kwargs)
        action_type = type(result).__name__
        if action_type == "Proceed":
            print("[TONE] \u2705 Response meets the Dussault standard")
        else:
            reason = getattr(result, 'reason', '')
            print(f"[TONE] \u26a0\ufe0f  Guided: {reason[:80]}")
        return result


# Convenience instance for use in plugins list
tone_handler = DussaultToneHandler()
