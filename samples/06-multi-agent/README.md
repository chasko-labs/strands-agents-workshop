# module 06 — multi-agent

orchestrator + specialist delegation (agent-as-tool pattern).

## what you learn

- wrapping an `Agent()` inside a `@tool` function
- `callback_handler=None` — suppress streaming for inner agents
- orchestrator decides WHEN to delegate based on query type
- specialist has its own tools and system prompt (isolated context)
- mirrors NGS pattern: lean orchestrator delegates to specialists

## architecture

```
user → orchestrator (roster/game tools)
                   ↓ (podcast questions)
         podcast_research_specialist (search_podcast_episodes, get_episode_details)
                   ↓
         result returned to orchestrator → synthesized answer to user
```

## run

```bash
cd samples/06-multi-agent
python chat.py
```

## try

- "What did the podcasts say about how the Dillon trade came together?"
- "Is there an episode where Harrison talks about 2004 vs 2007?"
- "Look up Tom Brady's stats" (handled directly, no delegation)
