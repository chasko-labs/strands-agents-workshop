# module 01 — agent loop + tools

the core strands agent loop: prompt → tool call → observe → respond.

## what you learn

- `@tool` decorator for defining typed tool functions
- `Agent()` with model, tools, and system_prompt
- multi-turn conversation (agent.messages persists context)
- each tool extracts one data dimension (NGS feature extraction pattern)

## tools

| tool                               | returns                                     |
| ---------------------------------- | ------------------------------------------- |
| `lookup_player(player_name)`       | roster entry (position, university, honors) |
| `get_roster_by_position(position)` | all players at that position                |
| `get_game_result(week)`            | score, opponent, key performers             |
| `get_season_stats(player_name)`    | full stat line for key contributors         |
| `get_coaching_staff()`             | all 12 coaches + roles                      |

## run

```bash
cd samples/01-agent-loop-tools
pip install -r requirements.txt
python chat.py
```

## try

- "Who were the Pro Bowlers on the 2004 team?"
- "What happened in the AFC Championship game?"
- "Tell me about Corey Dillon's stats"
