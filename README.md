```
  +-[ strands agents workshop ]----------------------------------------------+
  |  hands-on . tools . hooks . steering . deploy . multi-agent . evals      |
  |  2004 new england patriots dynasty — bedrock nova inference backbone     |
  +--------------------------------------------------------------------------+
```

a hands-on workshop that builds "Dussault" — an AI agent named after the patriots.com
writer — piece by piece across seven modules. themed around the 2004 world champion
new england patriots. runs locally with ollama (free) or on AWS Bedrock Nova Pro.

original workshop structure by [Morgan Willis](https://github.com/morganwillisAWS) at
[aws-samples/sample-strands-agents-hands-on-workshop](https://github.com/aws-samples/sample-strands-agents-hands-on-workshop).
we diverged the use case and patched model config for accounts enforcing
`DenyThirdPartyBedrockInvoke`.

---

## what is strands-agents?

[strands-agents](https://github.com/strands-agents/sdk-python) is an open-source Python SDK
for building AI agents that can call tools, follow recipes, persist memory, and deploy
serverlessly. it connects to any LLM backend — this workshop uses Amazon Nova Pro (via
Bedrock) or Ollama (local, free). seven modules teach the SDK's core concepts by building
one agent piece by piece.

---

## quickstart (5 minutes, no AWS needed)

```bash
# 1. clone
git clone https://github.com/chasko-labs/strands-agents-workshop.git
cd strands-agents-workshop

# 2. python environment
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. install ollama (skip if you have AWS Bedrock access)
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &                    # start the server
ollama pull qwen3:8b              # download the model (~5GB)

# 4. run module 01
cd samples/01-agent-loop-tools
python chat.py

# 5. try a question
# You: Who were the Pro Bowlers on the 2004 team?
# Dussault: Based on the roster data, the 2004 Patriots had 4 Pro Bowl selections...
```

for AWS Bedrock instead of ollama:

```bash
export MODEL_PROVIDER=nova
export AWS_PROFILE=your-bedrock-profile    # must have Nova Pro access in us-west-2
python chat.py
```

---

## modules

```
samples/
  01-agent-loop-tools/    -- Dussault with roster/game/stat lookup tools
  02-hooks/               -- analytics tracking hook, repeat-query detector
  03-skills-steering/     -- dynasty debate skill + fact-check guardrail
  04-session-managers/    -- persistent research sessions
  05-deploy/              -- agentcore serverless deployment
  06-multi-agent/         -- orchestrator + podcast research specialist
  07-evals/              -- output quality + trajectory evaluation
  shared/                 -- model_provider.py, patriots_data.py (datasets)
```

| module | concept            | scenario                                                                                       |
| ------ | ------------------ | ---------------------------------------------------------------------------------------------- |
| 01     | agent loop + tools | `lookup_player`, `get_game_result`, `get_season_stats` — query the 2004 roster and season      |
| 02     | hooks              | track query patterns, detect repeat lookups, enforce cite-your-source                          |
| 03     | skills + steering  | dynasty-debate workflow skill + fact-check handler (blocks claims without prior lookup)        |
| 04     | session managers   | persistent research sessions — agent remembers your prior analysis across restarts             |
| 05     | deploy             | package Dussault as a serverless agentcore endpoint                                            |
| 06     | multi-agent        | orchestrator delegates podcast questions to a specialist with episode search tools             |
| 07     | evals              | output eval (is the response accurate?) + trajectory eval (did it follow lookup-before-claim?) |

---

## glossary

| term            | what it means in this workshop                                                                   |
| --------------- | ------------------------------------------------------------------------------------------------ |
| agent           | a program that receives a question, reasons about it, calls tools, and produces an answer        |
| tool            | a Python function the agent can call during reasoning (`@tool` decorator)                        |
| hook            | code that runs automatically at specific moments in the agent's lifecycle (observe, gate, track) |
| skill           | a recipe file (SKILL.md) the agent follows for specific situations — like a playbook             |
| steering        | guardrails that check the agent's work before it reaches the user                                |
| session manager | persistence layer — agent remembers prior conversations across restarts                          |
| AgentCore       | AWS service that hosts your agent as a serverless endpoint (module 05)                           |
| eval            | automated quality scoring — LLM-as-judge rates agent output against a rubric                     |
| multi-agent     | pattern where one agent delegates subtasks to specialist agents                                  |
| model provider  | the LLM backend — ollama (local, free) or Bedrock Nova Pro (AWS, per-token)                      |

---

## prerequisites

### model access (pick one)

| option           | what you need                                                                            | cost               |
| ---------------- | ---------------------------------------------------------------------------------------- | ------------------ |
| **ollama local** | ollama running, `ollama pull qwen3:8b`                                                   | free, no AWS creds |
| **aws bedrock**  | account with Nova Pro model access (us-west-2), `DenyThirdPartyBedrockInvoke` compatible | per-token          |

### ollama setup (recommended for first-time users)

```bash
# install ollama
curl -fsSL https://ollama.com/install.sh | sh

# start the server (runs in background)
ollama serve &

# pull the model used by this workshop
ollama pull qwen3:8b

# verify it works
ollama run qwen3:8b "say hello" --verbose
# should print a greeting and model stats
```

ollama runs entirely on your machine. no API keys, no cloud account, no billing.
requires ~5GB disk for the model and ~6GB RAM during inference.

### python

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# module 07 additionally:
pip install strands-agents-evals nest_asyncio
```

---

## running

ollama (local, free — no AWS needed):

```bash
export MODEL_PROVIDER=ollama
# ensure ollama is running with qwen3:8b pulled
cd samples/01-agent-loop-tools
python chat.py
```

for AWS Bedrock Nova Pro:

```bash
export AWS_PROFILE=<your-bedrock-enabled-profile>
export MODEL_PROVIDER=nova
cd samples/01-agent-loop-tools
python chat.py
```

both providers work identically for all seven modules. ollama is slower but free.
bedrock is faster with better tool-calling accuracy.

---

## the dussault standard

our agent's output aspires to the quality bar set by Mike Dussault (patriots.com writer,
host/producer of the "2004 - Yes, it's a Dynasty" podcast series). what that means:

- lead with findings, not process
- cite specific data — game weeks, scores, stat lines — never vague superlatives
- connect facts to narrative — why something happened matters as much as what happened
- name what's unknown rather than hedge with "arguably" or "potentially"
- players described in terms of team function, not isolated glory
- confident declaratives mixed with open questions that name the specific unknown

the eval rubric in module 07 scores agent responses against these patterns.

---

## datasets

all data lives in `samples/shared/patriots_data.py` — mock tools query this directly.
no external APIs or databases required to run the workshop.

| dataset        | records                                                                                             | source                                 |
| -------------- | --------------------------------------------------------------------------------------------------- | -------------------------------------- |
| 2004 roster    | 94 players (name, position, university, pro bowl, all-pro)                                          | pro-football-reference / existing repo |
| coaching staff | 12 coaches (name, role)                                                                             | patriots.com                           |
| game log       | 19 games (16 regular + 3 playoff, with scores and key performers)                                   | pro-football-reference                 |
| player stats   | 9 key contributors (Brady, Dillon, Branch, Givens, Seymour, Harrison, Vinatieri, Bruschi, McGinest) | pro-football-reference                 |
| podcast index  | 17 episodes (4 dynasty series + 13 pats from the past with 2004 players)                            | patriots.com RSS                       |
| season records | win streak, point differential, team achievements                                                   | multiple verified sources              |

---

## nfl/aws next gen stats parallel (architectural context)

this workshop teaches the same architectural pattern that powers NFL Next Gen Stats:

| NGS pattern                                | strands agent equivalent                  | module |
| ------------------------------------------ | ----------------------------------------- | ------ |
| 11 features extracted per play             | tools extract structured data dimensions  | 01     |
| CloudWatch monitors every inference        | hooks observe every tool call             | 02     |
| trained models carry domain knowledge      | AgentSkills carry procedural recipes      | 03     |
| S3 stores 10+ years of historical data     | session managers persist analysis history | 04     |
| Lambda + API Gateway (event-driven)        | agentcore serverless deployment           | 05     |
| lean orchestrator delegates to specialists | agent-as-tool multi-agent pattern         | 06     |
| 90% directional approval from experts      | LLM-as-judge output + trajectory eval     | 07     |

---

## kiro crew (optional)

[kiro](https://kiro.dev) is an AI development environment. the `.kiro/` directory in this
repo configures a persistent workspace where the agent remembers corrections across sessions,
shares context across terminals, and can run tasks overnight. kiro is the tooling you use
to work through the workshop — not the workshop content itself.

the workshop runs identically in a plain terminal. kiro crew enhances the experience for
multi-session work:

```bash
git clone https://github.com/kirodotdev/KiroCrew.git
cd KiroCrew && make build && source .venv/bin/activate
kirocrew setup && kirocrew doctor && kirocrew gateway
# then work through modules in kiro-cli or the crew dashboard
```

see [.kiro/](.kiro/) for the crew configuration used to build this workshop.

---

## attribution

- morgan willis wrote the original workshop curriculum
- mike dussault's work at patriots.com is the quality standard for agent output
- bryan chasko diverged the use case and authored the 2004 patriots datasets
- AWS/NFL Next Gen Stats partnership informs the architectural framing

original repo: https://github.com/aws-samples/sample-strands-agents-hands-on-workshop
license: MIT-0 (inherited from the original)
