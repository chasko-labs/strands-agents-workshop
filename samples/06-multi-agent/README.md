# module 06 — multi-agent

the agent-as-tool pattern: wrap a specialist agent inside a `@tool` function so the
orchestrator can delegate subtasks. this module adds a podcast research specialist that
the main Dussault agent calls when questions involve episode content. same pattern as NGS:
lean orchestrator routes to domain specialists, synthesizes their results.

## prerequisites

- python venv activated (`source ../../.venv/bin/activate`)
- `pip install -r ../../requirements.txt`
- module 01 completed (you understand tools and the agent loop)
- ollama running with qwen3:8b pulled

## run

```bash
cd samples/06-multi-agent
python chat.py                          # ollama (default)
MODEL_PROVIDER=nova python chat.py      # AWS Bedrock
```

## what you'll see

```
You: What did the podcasts say about the Dillon trade?
[DELEGATION] orchestrator → podcast_research_specialist
[DELEGATION] specialist searching episodes for: Dillon trade
[DELEGATION] specialist returning 2 relevant episodes
Dussault: According to the dynasty podcast series, the Dillon
acquisition from Cincinnati was discussed in episode 3...
```

## what you learn

- wrapping an `Agent()` inside a `@tool` function (agent-as-tool pattern)
- `callback_handler=None` suppresses streaming for inner agents
- orchestrator decides WHEN to delegate based on query type
- specialist carries its own tools and system prompt (isolated context)
- direct queries (roster, stats) stay with the orchestrator — no unnecessary delegation

## troubleshooting

| error                                                   | fix                                                      |
| ------------------------------------------------------- | -------------------------------------------------------- |
| `ModuleNotFoundError: No module named 'strands'`        | `pip install -r ../../requirements.txt`                  |
| `ModuleNotFoundError: No module named 'dussault_tools'` | `cd` to this directory first, or ensure module 01 exists |
| `ConnectionRefusedError` (ollama)                       | run `ollama serve` in another terminal                   |
| `NoCredentialsError` (bedrock)                          | set `export MODEL_PROVIDER=ollama` to skip AWS           |
