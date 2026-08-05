"""Module 4: Session Managers — persistent dynasty research sessions.

The agent remembers your prior analysis across restarts. Quit, run again
with the same --session-id, and it recalls your previous questions.

From the repo root:
    cd samples/04-session-managers
    python chat.py
    python chat.py --session-id brady-deep-dive
"""

import sys
import argparse
sys.path.insert(0, "../shared")
sys.path.insert(0, "../01-agent-loop-tools")

from strands import Agent, AgentSkills
from strands.models import BedrockModel
from strands.agent.conversation_manager import SlidingWindowConversationManager
from strands.session.file_session_manager import FileSessionManager
from dynasty_tools import lookup_player, get_roster_by_position, get_game_result, get_season_stats, get_coaching_staff

SYSTEM_PROMPT = """You are a 2004 New England Patriots dynasty analyst with persistent memory.

If there are previous messages in the conversation history, use that context
to continue the analysis without asking the user to repeat information.

When answering:
- Always look up the data before making claims. Never guess stats.
- Connect facts to story.
- Reference prior conversation context when relevant ("as we discussed earlier...").
- Be specific: cite game weeks, scores, stat lines."""


def main():
    parser = argparse.ArgumentParser(description="Persistent dynasty research session.")
    parser.add_argument(
        "--session-id",
        default="dynasty-research-001",
        help="Session id to persist/resume (default: dynasty-research-001)",
    )
    args = parser.parse_args()

    session_manager = FileSessionManager(
        session_id=args.session_id,
        storage_dir="./sessions",
    )

    agent = Agent(
        model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region_name="us-west-2"),
        tools=[lookup_player, get_roster_by_position, get_game_result, get_season_stats, get_coaching_staff],
        plugins=[AgentSkills(skills=["./skills"])],
        system_prompt=SYSTEM_PROMPT,
        conversation_manager=SlidingWindowConversationManager(window_size=20),
        session_manager=session_manager,
    )

    restored = len(agent.messages)
    print(f"Dynasty Research Session ({args.session_id}) — type 'quit' to exit.")
    if restored:
        print(f"Restored {restored} message(s) from previous session.")
    print('Try: "Tell me about Tom Brady\'s 2004 stats"')
    print("Then quit and restart — it remembers your prior analysis.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSession saved. Goodbye!")
            break

        if user_input.lower() in {"quit", "exit", "q"}:
            print("Session saved. Goodbye!")
            break
        if not user_input:
            continue

        print("\nAnalyst: ", end="")
        agent(user_input)
        print()


if __name__ == "__main__":
    main()
