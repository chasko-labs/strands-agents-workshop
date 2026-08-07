# module 01 — agent loop + tools

the core strands agent pattern: give an LLM typed Python functions it can call, then let
it decide when to use them. this module builds Dussault with five tools that query the 2004
patriots roster, game log, and player stats. you will see the full agent loop in action —
prompt in, tool calls out, observations back, final response to the user.

## prerequisites

- python venv activated (`source ../../.venv/bin/activate`)
- `pip install -r ../../requirements.txt`
- ollama running with qwen3:8b pulled (`ollama serve` + `ollama pull qwen3:8b`)

## run

```bash
cd samples/01-agent-loop-tools
python chat.py                          # ollama (default)
MODEL_PROVIDER=nova python chat.py      # AWS Bedrock
```

## what you'll see

```
You: Who were the Pro Bowlers on the 2004 team?
Dussault: Based on the 2004 roster data, the Patriots had 4 Pro Bowl
selections: Tom Brady (QB), Richard Seymour (DL), Ty Law (CB), and
Adam Vinatieri (K)...
```

## what you learn

- `@tool` decorator turns a Python function into an agent-callable tool
- `Agent()` wires model + tools + system_prompt into a reasoning loop
- multi-turn conversation via `agent.messages` (context persists across turns)
- each tool extracts one data dimension — the NGS feature extraction pattern

## troubleshooting

| error                                            | fix                                            |
| ------------------------------------------------ | ---------------------------------------------- |
| `ModuleNotFoundError: No module named 'strands'` | `pip install -r ../../requirements.txt`        |
| `ConnectionRefusedError` (ollama)                | run `ollama serve` in another terminal         |
| `NoCredentialsError` (bedrock)                   | set `export MODEL_PROVIDER=ollama` to skip AWS |
