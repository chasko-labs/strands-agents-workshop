# module 04 — session managers

persistent memory across sessions.

## what you learn

- `FileSessionManager(session_id, storage_dir)` — persist to disk
- `SlidingWindowConversationManager(window_size=20)` — cap context
- session restore on restart (same session_id = same conversation)
- mirrors NGS S3 pattern: 10+ years of historical data persisted

## run

```bash
cd samples/04-session-managers
python chat.py
python chat.py --session-id brady-deep-dive
```

quit, then restart with the same session-id — it remembers.

## try

1. "Tell me about Tom Brady's 2004 stats"
2. quit
3. restart: "What were we just talking about?"
