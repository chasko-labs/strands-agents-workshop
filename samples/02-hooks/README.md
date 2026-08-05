# module 02 — hooks

lifecycle hooks for observability and guardrails.

## what you learn

- `HookProvider` class with `register_hooks()`
- `BeforeInvocationEvent` — fires at start of each agent turn
- `BeforeToolCallEvent` — fires before every tool execution
- `event.cancel_tool` — block a tool call with a message
- cross-turn state tracking (queried players persist across turns)

## the hook: DynastyAnalyticsHook

- tracks which players and games have been queried this session
- blocks repeat lookups ("already looked up Brady — use cached info")
- logs analysis depth per turn (tool call count)
- mirrors NGS CloudWatch pattern: observe every inference call

## run

```bash
cd samples/02-hooks
python chat.py
```

## try

ask about the same player twice to see the repeat-query blocker fire.
