"""Module 6: Multi-Agent — orchestrator + podcast research specialist.

Agent-as-tool pattern: Dussault handles roster/game queries directly,
delegates podcast research to a specialist with its own tools and prompt.

    cd samples/06-multi-agent
    python chat.py
"""

import sys
sys.path.insert(0, "../shared")
sys.path.insert(0, "../01-agent-loop-tools")

from strands import Agent, tool
from model_provider import get_model
from patriots_data import PODCAST_EPISODES
from dussault_tools import lookup_player, get_roster_by_position, get_game_result, get_season_stats, get_coaching_staff


# --- Podcast specialist tools ---

@tool
def search_podcast_episodes(query: str) -> str:
    """Search podcast episodes about the 2004 Patriots dynasty by keyword.

    Args:
        query: Search term (player name, topic, keyword)
    """
    query_lower = query.lower()
    matches = []
    for ep in PODCAST_EPISODES:
        searchable = f"{ep['title']} {ep['description']} {' '.join(ep.get('keywords', []))} {' '.join(ep.get('interviewees', []))}".lower()
        if query_lower in searchable:
            matches.append(ep)

    if not matches:
        return f"No podcast episodes found matching '{query}'. Try a player name or topic like 'trade', 'defense', 'Super Bowl'."

    results = []
    for ep in matches:
        interviewees = ", ".join(ep.get("interviewees", ["unknown"]))
        results.append(
            f"{ep['series']} Ep {ep['episode']}: \"{ep['title']}\" ({ep['duration_min']} min, {ep['date']})\n"
            f"  Guests: {interviewees}\n"
            f"  {ep['description'][:120]}..."
        )
    return f"{len(matches)} episode(s) found:\n\n" + "\n\n".join(results)


@tool
def get_episode_details(series: str, episode: str) -> str:
    """Get full details for a specific podcast episode.

    Args:
        series: Series name ("2004 Dynasty" or "Pats from the Past")
        episode: Episode number or identifier ("I", "II", "7", "48", etc.)
    """
    match = next(
        (ep for ep in PODCAST_EPISODES
         if ep["series"].lower() == series.lower() and str(ep["episode"]) == str(episode)),
        None
    )
    if not match:
        return f"Episode not found: {series} #{episode}. Available series: '2004 Dynasty' (I-IV), 'Pats from the Past' (7-54)."

    lines = [
        f"{match['series']} — Episode {match['episode']}: \"{match['title']}\"",
        f"Duration: {match['duration_min']} minutes",
        f"Published: {match['date']}",
        f"Interviewees: {', '.join(match.get('interviewees', ['not listed']))}",
        f"Description: {match['description']}",
        f"Keywords: {', '.join(match.get('keywords', []))}",
    ]
    return "\n".join(lines)


# --- Specialist agent wrapped as a tool ---

@tool
def podcast_research_specialist(query: str) -> str:
    """Delegate podcast research to the specialist agent.
    Use this when the user asks about interviews, podcast episodes, or
    what players/coaches said about the 2004 season.

    Args:
        query: The research question about podcast content
    """
    specialist = Agent(
        model=get_model(),
        tools=[search_podcast_episodes, get_episode_details],
        system_prompt="""You are a podcast research specialist for the 2004 Patriots dynasty.
You search episode archives to find relevant interviews and content.
Always cite the specific episode, guest, and air date.
If multiple episodes are relevant, rank them by relevance to the query.""",
        callback_handler=None,  # Silent — don't stream specialist output
    )
    print(f"\n[DELEGATION] \U0001f3a7 Podcast specialist activated for: {query[:60]}")
    response = specialist(query)
    print(f"[DELEGATION] \u2705 Specialist responded")
    return str(response)


# --- Orchestrator ---

SYSTEM_PROMPT = """You are Dussault, a 2004 New England Patriots dynasty analyst with access to
both data tools AND a podcast research specialist.

You handle:
- Roster lookups, game results, player stats, coaching staff (directly)
- Questions about what players or coaches said, podcast interviews,
  behind-the-scenes stories (delegate to podcast_research_specialist)

When a user asks about interviews, quotes, what someone said about the
season, or podcast content, delegate to the podcast_research_specialist
tool with a clear description of what to find.

After getting the specialist's response, synthesize it with your own
knowledge to give a complete answer."""


def main():
    orchestrator = Agent(
        model=get_model(),
        tools=[lookup_player, get_roster_by_position, get_game_result, get_season_stats,
               get_coaching_staff, podcast_research_specialist],
        system_prompt=SYSTEM_PROMPT,
    )

    print("Dussault (multi-agent) — type 'quit' to exit.")
    print("Delegates podcast research to a specialist.")
    print('Try: "What did the podcasts say about how the Dillon trade came together?"\n')

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
        orchestrator(user_input)
        print()


if __name__ == "__main__":
    main()
