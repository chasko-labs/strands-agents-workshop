# shared — datasets + model provider

common code used across all workshop modules.

## patriots_data.py

all 2004 new england patriots datasets. tools query this directly — no
external APIs or databases needed.

| dataset          | records                                                           |
| ---------------- | ----------------------------------------------------------------- |
| ROSTER           | 97 players (name, position, university, pro_bowl, all_pro)        |
| COACHES          | 12 staff (name, role)                                             |
| GAMES            | 19 games (16 regular + 3 playoff, with scores and key performers) |
| PLAYER_STATS     | 9 key contributors (full stat lines)                              |
| PODCAST_EPISODES | 16 episodes (4 dynasty series + 12 pats from the past)            |
| SEASON_RECORDS   | 25 fields (records, achievements, notable facts)                  |

## model_provider.py

helper to swap between inference backends:

```bash
# local (default) — no AWS creds needed
export MODEL_PROVIDER=ollama

# aws bedrock nova pro
export MODEL_PROVIDER=nova
```

usage in any module:

```python
import sys; sys.path.insert(0, "../shared")
from model_provider import get_model

agent = Agent(model=get_model(), tools=[...], system_prompt=SYSTEM_PROMPT)
```

## valkey_client.py

optional persistence layer for cross-module memory, research caching, analytics,
and leaderboard tracking. graceful fallback — returns None when unavailable, so
every module works without it.

```bash
# start valkey (optional)
docker run -d --name workshop-valkey -p 6379:6379 valkey/valkey:8
export VALKEY_URL=redis://localhost:6379
```

usage in any module:

```python
import sys; sys.path.insert(0, "../shared")
from valkey_client import get_valkey, workshop_user_id

vk = get_valkey()  # None if no VALKEY_URL or server unreachable
if vk:
    vk.set(f"user:{workshop_user_id()}:last_query", query)
```
