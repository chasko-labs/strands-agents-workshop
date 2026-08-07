# module 03 — skills + steering

skills give the agent procedural recipes to follow; steering handlers enforce quality
gates on its output. this module adds a dynasty-debate skill (step-by-step comparison
workflow) and two guardrails: a fact-check handler that blocks claims without a prior
lookup, and a tone handler that scores responses against the Dussault standard.

## prerequisites

- python venv activated (`source ../../.venv/bin/activate`)
- `pip install -r ../../requirements.txt`
- module 01 completed (you understand tools and the agent loop)
- ollama running with qwen3:8b pulled

## run

```bash
cd samples/03-skills-steering
python chat.py                          # ollama (default)
MODEL_PROVIDER=nova python chat.py      # AWS Bedrock
```

## what you'll see

```
You: Compare Corey Dillon and Deion Branch
[FACT-CHECK] blocking get_season_stats — must lookup_player first
Dussault: Let me verify both players are on the roster first...
[TONE] score=8/10 — specific stats cited, narrative connection present
Dussault: Dillon rushed for 1,635 yards...
```

## what you learn

- `AgentSkills(skills=["./skills"])` loads SKILL.md recipe files as agent knowledge
- `SteeringHandler` enforces deterministic pre-tool-call rules
- `LLMSteeringHandler` uses a secondary LLM to evaluate output quality
- `LedgerProvider` tracks tool call history for workflow validation
- `Proceed` / `Guide` return types control whether the agent continues or corrects

## troubleshooting

| error                                                   | fix                                                      |
| ------------------------------------------------------- | -------------------------------------------------------- |
| `ModuleNotFoundError: No module named 'strands'`        | `pip install -r ../../requirements.txt`                  |
| `ModuleNotFoundError: No module named 'dussault_tools'` | `cd` to this directory first, or ensure module 01 exists |
| `ConnectionRefusedError` (ollama)                       | run `ollama serve` in another terminal                   |
| `NoCredentialsError` (bedrock)                          | set `export MODEL_PROVIDER=ollama` to skip AWS           |
