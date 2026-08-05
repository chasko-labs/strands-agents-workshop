# module 03 — skills + steering

pluggable domain knowledge (AgentSkills) + deterministic and LLM guardrails.

## what you learn

- `AgentSkills(skills=["./skills"])` — loads SKILL.md recipe files
- `SteeringHandler` — deterministic pre-tool-call enforcement
- `LLMSteeringHandler` — secondary LLM evaluates output quality
- `LedgerProvider` — tracks tool call history for workflow validation
- `Proceed` / `Guide` return types control agent behavior

## skills

| skill           | purpose                                             |
| --------------- | --------------------------------------------------- |
| dynasty-debate  | step-by-step player/topic comparison workflow       |
| game-breakdown  | structured game analysis recipe                     |
| dynasty-context | background narrative (trade, CB crisis, win streak) |

## steering handlers

- `FactCheckHandler` — blocks get_season_stats until lookup_player confirms the player exists
- `DussaultToneHandler` — LLM evaluates response against the Dussault standard

## run

```bash
cd samples/03-skills-steering
python chat.py
```

## try

- "Compare Corey Dillon and Deion Branch — who was more important?"
- "Break down the AFC Championship game for me."
