```
  +-[ strands agents workshop ]----------------------------------------------+
  |  hands-on . tools . hooks . steering . deploy . multi-agent . evals      |
  |  2004 new england patriots dynasty — bedrock nova inference backbone     |
  +--------------------------------------------------------------------------+
```

a strands-agents workshop themed around the 2004 world champion new england patriots.
seven modules build a "dynasty analyst" agent piece by piece — the same architectural
patterns AWS Next Gen Stats uses (feature extraction → inference → human-guided output)
applied to the greatest team ever assembled.

the gold standard for agent output quality is Mike Dussault's work at patriots.com —
evidence-first, narrative-aware, specific about what's known and honest about what isn't.

original workshop structure by [Morgan Willis](https://github.com/morganwillisAWS) at
[aws-samples/sample-strands-agents-hands-on-workshop](https://github.com/aws-samples/sample-strands-agents-hands-on-workshop).
all credit to morgan for the curriculum architecture. we diverged the use case and
patched model config for accounts enforcing `DenyThirdPartyBedrockInvoke`.

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

## modules

```
samples/
  01-agent-loop-tools/    -- dynasty analyst with roster/game/stat lookup tools
  02-hooks/               -- analytics tracking hook, repeat-query detector
  03-skills-steering/     -- dynasty debate skill + fact-check guardrail
  04-session-managers/    -- persistent dynasty research sessions
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
| 05     | deploy             | package the dynasty analyst as a serverless agentcore endpoint                                 |
| 06     | multi-agent        | orchestrator delegates podcast questions to a specialist with episode search tools             |
| 07     | evals              | output eval (is the response accurate?) + trajectory eval (did it follow lookup-before-claim?) |

---

## running

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install strands-agents strands-agents-tools

export AWS_PROFILE=<your-bedrock-enabled-profile>
export MODEL_PROVIDER=nova

cd samples/01-agent-loop-tools
python chat.py
```

for local-only (no aws creds needed):

```bash
export MODEL_PROVIDER=ollama
# ensure ollama is running with qwen3:8b pulled
python chat.py
```

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

## nfl/aws next gen stats parallel

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

## attribution

- morgan willis wrote the original workshop curriculum
- mike dussault's work at patriots.com is the quality standard for agent output
- bryan chasko diverged the use case and authored the 2004 patriots datasets
- AWS/NFL Next Gen Stats partnership informs the architectural framing

original repo: https://github.com/aws-samples/sample-strands-agents-hands-on-workshop
license: MIT-0 (inherited from the original)
