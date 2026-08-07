# Rules for AI Assistants

**This file is a ROUTER.** Project identity + pointers to docs you must read.

## What this is

A strands-agents workshop teaching AI agent patterns through the 2004 New England
Patriots dynasty. Seven modules build "Dussault" — named after the patriots.com writer
whose work sets the quality bar.

- **Runtime:** strands-agents SDK (Python, PyPI)
- **Model:** Amazon Nova Pro or Ollama (qwen3:8b local)
- **Deploy:** Bedrock AgentCore (module 05)
- **Crew:** Kiro crew orchestrates the build (Belichick + coaching staff)
- **Data home:** `samples/shared/patriots_data.py`

## Read before you touch

| If touching…        | Read first                                                              |
| ------------------- | ----------------------------------------------------------------------- |
| datasets            | `samples/shared/patriots_data.py` + `samples/shared/README.md`          |
| tools               | `samples/01-agent-loop-tools/dussault_tools.py`                         |
| hooks               | `samples/02-hooks/chat.py`                                              |
| skills / steering   | `samples/03-skills-steering/skills/` + `steering_handlers.py`           |
| session persistence | `samples/04-session-managers/chat.py`                                   |
| serverless deploy   | `samples/05-deploy/main.py`                                             |
| multi-agent         | `samples/06-multi-agent/chat.py`                                        |
| evals               | `samples/07-evals/run_evals.py`                                         |
| project context     | `.kiro/steering/project-context.md` + `.kiro/steering/project-scope.md` |

## Crew roster (who builds this workshop)

| agent                             | persona                    | role                                 | when active          |
| --------------------------------- | -------------------------- | ------------------------------------ | -------------------- |
| poltergeist-belichick-core-anchor | Belichick (HC)             | orchestrates, delegates, never codes | session coordination |
| ghost-weis-offense-author         | Charlie Weis (OC)          | writes module code                   | implementation       |
| ghost-crennel-defense-validator   | Romeo Crennel (DC)         | quality gate, style check            | before commit        |
| ghost-pioli-personnel-research    | Scott Pioli (VP Personnel) | data research, SDK docs              | before authoring     |
| ghost-mangini-ops-ci              | Eric Mangini (DB Coach)    | git ops, commits                     | every commit         |
| ghost-mcdaniels-qb-tools          | Josh McDaniels (QB Coach)  | tool authoring                       | tool changes         |

## Kiro concepts demonstrated by this crew

| concept             | where to look                        | what it teaches                                   |
| ------------------- | ------------------------------------ | ------------------------------------------------- |
| custom agents       | `.kiro/agents/*.json`                | agent config schema (name, model, tools, hooks)   |
| persona trifecta    | `.kiro/agents/belichick/`            | SOUL.md + SKILL.md + DUTIES.md pattern            |
| enforcement hooks   | `.kiro/hooks/belichick-code-gate.sh` | preToolUse hooks that block actions               |
| MCP servers         | `.kiro/settings/mcp.json`            | wiring external tools (context7, valkey)          |
| steering docs       | `.kiro/steering/`                    | project context + scope as loaded resources       |
| subagent delegation | belichick's use_subagent tool        | flat delegation model (orchestrator → specialist) |
| includeMcpJson      | agent JSON `includeMcpJson: true`    | global vs agent-specific server config            |

## Quality standard

Agent output aspires to the Dussault standard:

- lead with findings, not process
- cite specific data (game weeks, scores, stat lines)
- connect facts to narrative
- name what's unknown rather than hedge
- players described in terms of team function

## Model

`MODEL_PROVIDER=nova` (Amazon Nova Pro) or `MODEL_PROVIDER=ollama` (local qwen3:8b).
See `samples/shared/model_provider.py` for the swap helper.

## Git

- `main` is the default branch
- commit format: `<type>: <summary>` (feat, fix, docs, chore)
- one logical change per commit
