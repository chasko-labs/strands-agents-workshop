# project context — strands-agents-workshop

## what this repo is

a hands-on workshop teaching strands-agents SDK patterns through the 2004 new england
patriots dynasty season. seven modules build a "dynasty analyst" agent piece by piece —
tools, hooks, skills, sessions, deploy, multi-agent, evals. the gold standard for
agent output quality is Mike Dussault's work at patriots.com.

## stack

- python 3.12+
- strands-agents, strands-agents-tools, strands-agents-evals (PyPI)
- amazon bedrock nova pro (us.amazon.nova-pro-v1:0) via strands BedrockModel
- ollama (qwen3:8b) for local-only execution
- bedrock agentcore (module 05 deploy)

## repo structure

```
samples/
  shared/         — model_provider.py, patriots_data.py (all datasets)
  01-agent-loop-tools/  — core agent loop + @tool decorator
  02-hooks/             — HookProvider lifecycle hooks
  03-skills-steering/   — AgentSkills + SteeringHandler
  04-session-managers/  — FileSessionManager persistence
  05-deploy/            — BedrockAgentCoreApp serverless
  06-multi-agent/       — agent-as-tool delegation
  07-evals/             — OutputEvaluator + TrajectoryEvaluator
docs/             — implementation plan, architecture notes
.kiro/            — crew configuration for building the workshop
```

## conventions

- all mock data lives in `samples/shared/patriots_data.py` — tools query it directly
- no external APIs or databases required to run any module
- each module has a `chat.py` (terminal REPL) and a notebook (step-by-step cells)
- `MODEL_PROVIDER` env var controls ollama vs nova — both work for every module
- the dussault standard governs agent output quality (see docs/implementation-plan.md)

## crew workflow

the kiro crew builds this workshop content. the workflow:

1. research (ghost-kerouac-research-analyst) gathers and verifies 2004 data
2. sdk lookup (ghost-hcom-api-delegate) confirms current strands-agents patterns
3. authoring (ghost-hcom-python-coder) writes module code
4. style check (ghost-scribe-style-enforcer) validates output quality
5. git ops (ghost-orin-ci-cd) commits and pushes

## attribution

- original curriculum: Morgan Willis (aws-samples)
- quality standard: Mike Dussault (patriots.com)
- datasets + divergence: Bryan Chasko
- architectural framing: AWS/NFL Next Gen Stats partnership
