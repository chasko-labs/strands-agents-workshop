# Rules for AI Assistants

**This file is a ROUTER.** It carries the project identity and points to docs
you MUST read before touching a subsystem.

## What this is

A strands-agents workshop teaching AI agent patterns through the 2004 New England
Patriots dynasty season. Seven modules build a "dynasty analyst" agent piece by
piece. The gold standard for agent output quality is Mike Dussault's work at
patriots.com.

- **Runtime:** strands-agents SDK (Python, PyPI)
- **Model:** Amazon Nova Pro (us.amazon.nova-pro-v1:0) or Ollama (qwen3:8b local)
- **Deploy:** Bedrock AgentCore (module 05)
- **Crew:** Kiro Crew orchestrates the build workflow (research → author → validate → commit)
- **Data home:** `samples/shared/patriots_data.py` (all datasets, no external deps)

## Read before you touch

| If you are touching…                      | Read first                                                                  |
| ----------------------------------------- | --------------------------------------------------------------------------- |
| datasets (roster, games, stats, podcasts) | `samples/shared/patriots_data.py` + `samples/shared/README.md`              |
| any module's tools                        | `samples/01-agent-loop-tools/dynasty_tools.py` (canonical tool definitions) |
| hooks (lifecycle, analytics)              | `samples/02-hooks/chat.py`                                                  |
| skills or steering handlers               | `samples/03-skills-steering/skills/` + `steering_handlers.py`               |
| session persistence                       | `samples/04-session-managers/chat.py`                                       |
| serverless deploy                         | `samples/05-deploy/main.py`                                                 |
| multi-agent delegation                    | `samples/06-multi-agent/chat.py`                                            |
| eval rubrics or test cases                | `samples/07-evals/run_evals.py`                                             |
| project scope, conventions, quality bar   | `.kiro/steering/project-context.md` + `.kiro/steering/project-scope.md`     |
| implementation plan, dataset schemas      | `docs/implementation-plan.md`                                               |
| NGS architectural parallel                | `README.md`                                                                 |

## Crew roster (who builds this workshop)

| agent                          | role                                             | when active           |
| ------------------------------ | ------------------------------------------------ | --------------------- |
| poltergeist-harald-core-anchor | orchestration, planning, dataset curation        | session coordination  |
| ghost-kerouac-research-analyst | 2004 patriots data research, podcast RSS parsing | data gathering        |
| ghost-hcom-api-delegate        | strands-agents SDK doc lookup via context7       | before authoring code |
| ghost-hcom-python-coder        | module authoring (tools, hooks, skills, evals)   | implementation        |
| ghost-orin-ci-cd               | git ops, commits, branch management              | every commit          |
| ghost-scribe-style-enforcer    | dussault standard enforcement on output          | quality gate          |

## Quality standard

Agent output aspires to the Dussault standard (docs/implementation-plan.md):

- lead with findings, not process
- cite specific data (game weeks, scores, stat lines)
- connect facts to narrative (why, not just what)
- name what's unknown rather than hedge
- players described in terms of team function

## Long-term intent

This workshop is built via kiro-cli crew sessions today. The long-term direction
is multi-surface interaction: kiro-cli, Kiro Crew (desktop/web/TUI), langchain,
deepagents/dcode. The `.kiro/` config provides the chassis that carries across
all surfaces — steering files, skills, and agents persist regardless of which
tool drives the session.

## Model

All work uses Amazon Nova Pro (`us.amazon.nova-pro-v1:0`), consistent with
accounts enforcing `DenyThirdPartyBedrockInvoke`. Local dev: ollama with qwen3:8b.
See `samples/shared/model_provider.py` for the swap helper.

## Git

- `main` is the default branch
- changes land through commits (ghost-orin-ci-cd)
- commit format: `<type>: <summary>` (feat, fix, docs, chore)
- one logical change per commit
