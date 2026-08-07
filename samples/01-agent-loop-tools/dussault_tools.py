"""Dussault's tools — 2004 New England Patriots data extraction.
Each tool returns one structured dimension. Same pattern as NGS feature extraction.
"""

import sys
sys.path.insert(0, "../shared")

from strands import tool
from patriots_data import ROSTER, COACHES, GAMES, PLAYER_STATS, SEASON_RECORDS


@tool
def lookup_player(player_name: str) -> str:
    """Look up a player from the 2004 New England Patriots roster.

    Args:
        player_name: Full or partial name of the player (e.g. "Tom Brady", "Dillon")
    """
    matches = [p for p in ROSTER if player_name.lower() in p["name"].lower()]
    if not matches:
        return f"No player found matching '{player_name}' on the 2004 Patriots roster."
    results = []
    for p in matches:
        line = f"{p['name']} — {p['position']}, {p['university']}"
        if p['pro_bowl']:
            line += " (Pro Bowl)"
        if p['all_pro']:
            line += f" ({p['all_pro']} All-Pro)"
        results.append(line)
    return "\n".join(results)


@tool
def get_roster_by_position(position: str) -> str:
    """Get all players at a given position from the 2004 Patriots roster.

    Args:
        position: Position abbreviation (QB, RB, WR, TE, T, G, C, DE, NT, ILB, OLB, CB, SS, FS, K, P, LS)
    """
    matches = [p for p in ROSTER if position.upper() in p["position"].upper()]
    if not matches:
        return f"No players found at position '{position}'. Try: QB, RB, WR, TE, DE, NT, ILB, OLB, CB, SS, FS, K, P"
    lines = [f"{p['name']} — {p['position']}, {p['university']}" for p in matches]
    return f"{len(matches)} players at {position.upper()}:\n" + "\n".join(lines)


@tool
def get_game_result(week: int) -> str:
    """Get the result of a specific 2004 regular season game by week number.
    Use week 18 for Divisional, 19 for AFC Championship, 20 for Super Bowl.

    Args:
        week: Week number (1-17 regular season) or keyword lookup
    """
    # Map special weeks
    week_map = {18: "Divisional", 19: "AFC Championship", 20: "Super Bowl XXXIX"}
    search_week = week_map.get(week, week)

    game = next((g for g in GAMES if g["week"] == search_week or g["week"] == week), None)
    if not game:
        return f"No game found for week {week}. Regular season: 1-17 (bye week 3). Playoffs: 18=Divisional, 19=AFC Championship, 20=Super Bowl."

    location = "HOME" if game["home"] else "AWAY"
    result = f"Week {game['week']} ({game['date']}): Patriots {game['score_ne']}, {game['opponent']} {game['score_opp']} [{game['result']}] ({location})\n"
    result += f"Key performers: {'; '.join(game['key_performers'])}"
    return result


@tool
def get_season_stats(player_name: str) -> str:
    """Get detailed 2004 season statistics for a key contributor.
    Available for: Brady, Dillon, Branch, Givens, Seymour, Harrison, Vinatieri, Bruschi, McGinest.

    Args:
        player_name: Full or partial player name
    """
    # Find matching player in stats
    match = None
    for name in PLAYER_STATS:
        if player_name.lower() in name.lower():
            match = name
            break

    if not match:
        available = ", ".join(PLAYER_STATS.keys())
        return f"No detailed stats available for '{player_name}'. Available: {available}"

    stats = PLAYER_STATS[match]
    lines = [f"{match} — 2004 Season Statistics:"]
    for key, value in stats.items():
        if key == "notable_plays":
            lines.append(f"  Notable plays:")
            for play in value:
                lines.append(f"    - {play}")
        elif key == "note":
            lines.append(f"  Context: {value}")
        else:
            lines.append(f"  {key}: {value}")
    return "\n".join(lines)


@tool
def get_coaching_staff() -> str:
    """Get the full 2004 New England Patriots coaching staff."""
    lines = ["2004 New England Patriots Coaching Staff:"]
    for coach in COACHES:
        lines.append(f"  {coach['name']} — {coach['role']}")
    return "\n".join(lines)


@tool
def get_hoodie_data(query: str) -> str:
    """Look up Bill Belichick's hoodie/attire choices from the 2004 season.
    Based on Mike Dussault's famous Hoodie Database.

    Args:
        query: What to look up — "week 8", "super bowl", "record", "trivia", or "summary"
    """
    from patriots_data import HOODIE_DATABASE

    query_lower = query.lower()

    # Summary
    if "summary" in query_lower or "overview" in query_lower:
        return HOODIE_DATABASE["season_summary"]

    # Record/stats
    if "record" in query_lower or "stats" in query_lower or "analysis" in query_lower:
        return (
            f"Grey hoodie record in 2004: {HOODIE_DATABASE['grey_hoodie_record_2004']}\n"
            f"Statistical analysis: {HOODIE_DATABASE['statistical_analysis']}"
        )

    # Trivia
    if "trivia" in query_lower or "fun fact" in query_lower:
        return "Hoodie trivia:\n" + "\n".join(f"- {t}" for t in HOODIE_DATABASE["trivia"])

    # Specific game lookup
    for game in HOODIE_DATABASE["games"]:
        week_str = str(game["week"]).lower()
        opponent = game["opponent"].lower()
        if week_str in query_lower or opponent in query_lower:
            return (
                f"Week {game['week']} vs {game['opponent']}: "
                f"{game['attire']}, sleeves {game['sleeves']} — {game['result']}"
            )

    # Default: full season summary + all games
    lines = [HOODIE_DATABASE["season_summary"], "", "Game-by-game:"]
    for game in HOODIE_DATABASE["games"]:
        lines.append(f"  Week {game['week']} vs {game['opponent']}: {game['attire']}, {game['sleeves']} — {game['result']}")
    return "\n".join(lines)
