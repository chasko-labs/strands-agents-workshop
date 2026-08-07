# module 04 — session managers

session managers give the agent memory that survives restarts. this module persists
conversation history to disk so Dussault remembers your prior research across sessions.
same pattern as NGS storing 10+ years of historical data in S3 — your agent builds
cumulative context over time instead of starting cold every run.

## prerequisites

- python venv activated (`source ../../.venv/bin/activate`)
- `pip install -r ../../requirements.txt`
- module 01 completed (you understand tools and the agent loop)
- ollama running with qwen3:8b pulled

## run

```bash
cd samples/04-session-managers
python chat.py                          # ollama (default)
MODEL_PROVIDER=nova python chat.py      # AWS Bedrock
```

## what you'll see

```
# first run:
You: Tell me about Tom Brady's 2004 stats
Dussault: Brady threw for 3,692 yards...

# second run (same session):
Restored 4 message(s) from previous session
You: What were we just talking about?
Dussault: We were discussing Brady's 2004 campaign...
```

## what you learn

- `FileSessionManager(session_id, storage_dir)` persists conversation to disk
- `SlidingWindowConversationManager(window_size=20)` caps context length
- session restore on restart (same session_id = same conversation)
- combining persistence with window management prevents unbounded growth

## troubleshooting

| error                                                   | fix                                                      |
| ------------------------------------------------------- | -------------------------------------------------------- |
| `ModuleNotFoundError: No module named 'strands'`        | `pip install -r ../../requirements.txt`                  |
| `ModuleNotFoundError: No module named 'dussault_tools'` | `cd` to this directory first, or ensure module 01 exists |
| `ConnectionRefusedError` (ollama)                       | run `ollama serve` in another terminal                   |
| `NoCredentialsError` (bedrock)                          | set `export MODEL_PROVIDER=ollama` to skip AWS           |
