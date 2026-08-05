# implementation plan — 2004 patriots dynasty agent workshop

---

## overview

seven modules build a "dynasty analyst" agent using strands-agents SDK. each module
layers one capability on the same 2004 patriots use case. the agent's output quality
targets mike dussault's approach at patriots.com: evidence-first, narrative-aware,
specific about what's known, honest about what isn't.

---

## shared datasets (samples/shared/patriots_data.py)

all mock data lives in a single python file. tools query it directly — no external
APIs, no databases, no network calls required.

### dataset 1: roster (94 players)

```python
ROSTER = [
    {"name": "Tom Brady", "position": "QB", "pro_bowl": True, "all_pro": False, "university": "University of Michigan"},
    {"name": "Corey Dillon", "position": "RB", "pro_bowl": True, "all_pro": False, "university": "University of Washington"},
    # ... 94 total
]
```

source: existing CSV at BryanChasko/pythonExamplesWithNewEnglandPatriots

### dataset 2: coaching staff (12)

```python
COACHES = [
    {"name": "Bill Belichick", "role": "Head Coach"},
    {"name": "Charlie Weis", "role": "Offensive Coordinator"},
    {"name": "Romeo Crennel", "role": "Defensive Coordinator"},
    # ... 12 total
]
```

### dataset 3: game log (19 games)

```python
GAMES = [
    {"week": 1, "date": "2004-09-09", "opponent": "Indianapolis Colts", "home": True, "score_ne": 27, "score_opp": 24, "result": "W", "key_performers": ["Brady 335 yds, 3 TD", "Bruschi INT"]},
    # 16 regular season + 3 playoff
]
```

verified by kerouac research (high confidence). includes:

- 14-2 regular season
- divisional: Patriots 20, Colts 3
- AFC championship: Patriots 41, Steelers 27
- super bowl XXXIX: Patriots 24, Eagles 21

### dataset 4: player stats (9 key contributors)

```python
PLAYER_STATS = {
    "Tom Brady": {"games": 16, "comp": 288, "att": 474, "yards": 3692, "td": 28, "int": 14, "rating": 92.6},
    "Corey Dillon": {"games": 15, "carries": 345, "rush_yards": 1635, "rush_td": 12, "ypc": 4.7},
    "Deion Branch": {"games": 9, "rec": 35, "rec_yards": 454, "rec_td": 4, "playoff_rec": 11, "playoff_yards": 133, "super_bowl_mvp": True},
    "David Givens": {"games": 16, "rec": 56, "rec_yards": 874, "rec_td": 3},
    "Richard Seymour": {"games": 15, "tackles": 30, "sacks": 5.0, "pro_bowl": True, "all_pro": "1st Team"},
    "Rodney Harrison": {"games": 16, "all_pro": "2nd Team", "playoff_int": 3, "super_bowl_int": 1},
    "Adam Vinatieri": {"games": 16, "fg_made": 31, "fg_pct": 93.9, "points": 141, "all_pro": "1st Team"},
    "Tedy Bruschi": {"games": 16, "tackles": 76, "all_pro": "2nd Team", "super_bowl_int": 1},
    "Willie McGinest": {"games": 16, "sacks": 9.5, "team_leader": True},
}
```

### dataset 5: podcast index (17 episodes)

```python
PODCAST_EPISODES = [
    # dynasty series (Mike Dussault, host/producer)
    {"series": "2004 Dynasty", "episode": "I", "title": "Reloaded", "duration_min": 42, "date": "2025-02-17",
     "description": "Corey Dillon trade, Vince Wilfork draft, offseason reloading",
     "keywords": ["Dillon", "Wilfork", "trade", "draft", "offseason"]},
    # ... 4 dynasty episodes + 13 pats from the past episodes featuring 2004 players
]
```

### dataset 6: season records

```python
SEASON_RECORDS = {
    "regular_season": "14-2",
    "playoff": "3-0",
    "overall": "17-2",
    "points_scored": 437,
    "points_allowed": 260,
    "point_differential": 177,
    "win_streak": 21,
    "win_streak_note": "NFL record for consecutive regular season + playoff wins (carried from 2003)",
    "super_bowl": "XXXIX",
    "super_bowl_opponent": "Philadelphia Eagles",
    "super_bowl_score": "24-21",
    "super_bowl_mvp": "Deion Branch",
    "pro_bowlers": ["Tom Brady", "Corey Dillon", "Richard Seymour", "Adam Vinatieri", "Tedy Bruschi", "Larry Izzo"],
}
```

---

## module 01 — agent loop + tools

**concept:** core agent loop, tool-calling pattern

**tools:**

- `lookup_player(player_name: str)` → roster info
- `get_roster_by_position(position: str)` → all players at position
- `get_game_result(week: int)` → game details + key performers
- `get_season_stats(player_name: str)` → full stat line
- `get_coaching_staff()` → all coaches + roles

**system prompt:** dynasty analyst persona (dussault standard)

**NGS parallel:** tools as feature extractors — each returns one structured data dimension

---

## module 02 — hooks

**concept:** lifecycle hooks for observability and guardrails

**hooks:**

- `DynastyAnalyticsHook` — tracks which players/games queried per session, logs analysis depth
- repeat-query detector — cancels tool if same player looked up twice in one invocation
- source-citation logger — prints which data sources were accessed

**NGS parallel:** CloudWatch monitoring every inference call

---

## module 03 — skills + steering

**concept:** pluggable domain knowledge + deterministic/LLM guardrails

**skills (SKILL.md format):**

- `skills/player-comparison/` — step-by-step comparison workflow
- `skills/game-breakdown/` — structured game analysis recipe
- `skills/dynasty-context/` — background narrative knowledge

**steering handlers:**

- `FactCheckHandler(SteeringHandler)` — enforces lookup→claim ordering via LedgerProvider
- `DussaultToneHandler(LLMSteeringHandler)` — LLM-as-judge ensures output meets the standard

**NGS parallel:** trained models (skills) + human-in-the-loop (steering)

---

## module 04 — session managers

**concept:** persistent memory across sessions

**implementation:** FileSessionManager + SlidingWindowConversationManager(window_size=20)

**scenario:** persistent dynasty research — agent remembers prior analysis across restarts

**NGS parallel:** S3 storing 10+ years of historical data

---

## module 05 — deploy

**concept:** serverless deployment via bedrock agentcore

**implementation:** BedrockAgentCoreApp with @app.entrypoint

**NGS parallel:** Lambda + API Gateway (event-driven, scales to zero between games)

---

## module 06 — multi-agent

**concept:** orchestrator + specialist delegation (agent-as-tool pattern)

**orchestrator tools:** lookup_player, get_game_result, get_season_stats + podcast_research_specialist

**specialist agent:** has `search_podcast_episodes` and `get_episode_details` tools, searches
the 17-episode podcast dataset. callback_handler=None (silent execution).

**demo prompt:** "What did the podcasts say about how the Corey Dillon trade came together?"

**NGS parallel:** lean orchestrator delegates to specialist inference teams

---

## module 07 — evals

**concept:** automated output + trajectory evaluation

**output eval cases:**

- "Was Richard Seymour All-Pro in 2004?" → must say 1st Team All-Pro
- "What was the Super Bowl XXXIX score?" → must cite 24-21, Branch MVP, 11 catches 133 yards
- "Tell me about Patrick Mahomes on the 2004 Patriots." → must say not on roster

**trajectory eval cases:**

- refund→compare: must call lookup_player + get_season_stats before comparing
- game query: must call get_game_result

**dussault rubric (output evaluator):**

```
Score 1.0 if: leads with findings, cites specific data (numbers, weeks, scores),
connects facts to narrative context, names unknowns explicitly.
Score 0.5 if: correct data but presented as flat list without narrative.
Score 0.0 if: vague superlatives, fabricated stats, no specific citations.
```

**NGS parallel:** 90% directional approval from domain experts

---

## dussault style standard (eval rubric reference)

extracted from patriots.com articles (3 full-text articles analyzed):

- leads with verdict/result, unpacks chronologically
- specific stat citations embedded in prose naturally
- connects plays to game narrative (not isolated moments)
- confident declaratives mixed with named open questions
- describes players in terms of team function
- names the specific unknown (not "it's unclear" but "their availability will set the ceiling")
- uses historical references as proof ("previous losses came in 1986, 2005, 2013, 2015")
- no exclamation points in analysis
- no "arguably" without naming the argument
- active voice throughout

---

## data confidence notes

| dataset             | confidence  | flag                                                                  |
| ------------------- | ----------- | --------------------------------------------------------------------- |
| roster (94 players) | HIGH        | from existing verified CSV                                            |
| game log            | HIGH        | kerouac-verified from multiple sources                                |
| Brady stats         | HIGH        | 288/474, 3692, 28 TD, 14 INT, 92.6                                    |
| Dillon stats        | HIGH        | 345 carries, 1635 yds, 12 rush TD                                     |
| Branch stats        | HIGH        | 35 rec, 454 yds (reg season); 11/133 SB                               |
| Givens stats        | HIGH        | 56 rec, 874 yds, 3 TD                                                 |
| Seymour stats       | MEDIUM      | 5 sacks may undercount disruption                                     |
| Harrison stats      | MEDIUM      | 2nd Team All-Pro confirmed; exact regular season INT count unverified |
| Vinatieri stats     | HIGH        | 31 FG, 93.9%, 141 points                                              |
| Bruschi stats       | MEDIUM      | ~76 tackles per patriots.com                                          |
| McGinest stats      | MEDIUM-HIGH | 9.5 sacks (team leader)                                               |
| podcast episodes    | HIGH        | confirmed via Apple Podcasts + RSS                                    |
