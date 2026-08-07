# module 02 — hooks

lifecycle hooks let you observe, gate, and track everything the agent does — without
modifying the agent itself. this module adds a DynastyAnalyticsHook that logs query
patterns, counts tool calls per turn, and blocks repeat lookups. same pattern as NGS
CloudWatch monitoring every inference call in production.

## prerequisites

- python venv activated (`source ../../.venv/bin/activate`)
- `pip install -r ../../requirements.txt`
- module 01 completed (you understand the basic agent loop)
- ollama running with qwen3:8b pulled

## run

```bash
cd samples/02-hooks
python chat.py                          # ollama (default)
MODEL_PROVIDER=nova python chat.py      # AWS Bedrock
```

## what you'll see

```
You: Tell me about Tom Brady
[ANALYTICS] turn=1 tools_called=1 players_queried=['Tom Brady']
Dussault: Brady's 2004 season...

You: Tell me about Tom Brady again
[ANALYTICS] repeat query blocked: Tom Brady (already in session cache)
Dussault: I already looked up Brady this session...
```

## what you learn

- `HookProvider` class with `register_hooks()` for lifecycle integration
- `BeforeInvocationEvent` fires at the start of each agent turn
- `BeforeToolCallEvent` fires before every tool execution
- `event.cancel_tool` blocks a tool call and returns a message instead
- cross-turn state tracking (queried players persist across the session)

## troubleshooting

| error                                                   | fix                                                      |
| ------------------------------------------------------- | -------------------------------------------------------- |
| `ModuleNotFoundError: No module named 'strands'`        | `pip install -r ../../requirements.txt`                  |
| `ModuleNotFoundError: No module named 'dussault_tools'` | `cd` to this directory first, or ensure module 01 exists |
| `ConnectionRefusedError` (ollama)                       | run `ollama serve` in another terminal                   |
| `NoCredentialsError` (bedrock)                          | set `export MODEL_PROVIDER=ollama` to skip AWS           |
