```
  +-[ strands agents workshop ]---------------------------------+
  |  hands-on . tools . hooks . steering . deploy . multi-agent |
  |  bedrock nova models as your inference backbone             |
  +-------------------------------------------------------------+
```

bryan chasko's walkthrough of the strands agents hands-on workshop — the guided
lab version that builds a customer service agent module by module.

original workshop by [Morgan Willis](https://github.com/morganwillisAWS) at
[aws-samples/sample-strands-agents-hands-on-workshop](https://github.com/aws-samples/sample-strands-agents-hands-on-workshop).
all credit to morgan for the curriculum structure and sample architecture.

---

## what changed here

every sample is patched to run on an AWS account enforcing `DenyThirdPartyBedrockInvoke`.
only `amazon.*` first-party models clear the guard — no claude, no third-party.

a `shared/model_provider.py` helper lets you switch between ollama (local, default)
and nova (bedrock) via environment variable:

```bash
MODEL_PROVIDER=nova python chat.py     # bedrock nova pro in us-west-2
MODEL_PROVIDER=ollama python chat.py   # local qwen3:8b via ollama
```

if your account allows third-party models, you don't need these patches — use morgan's original.

---

## modules

```
samples/
  01-agent-loop-tools/    -- multi-turn chat with customer service tools
  02-hooks/               -- pre/post tool hooks, approval gates
  03-skills-steering/     -- AgentSkills plugin + steering handlers
  04-session-managers/    -- file + s3 persistence across sessions
  05-deploy/              -- agentcore runtime deployment
  06-multi-agent/         -- orchestrator delegates to tech support specialist
  07-evals/               -- evaluation suite (trajectory + output)
  shared/                 -- model_provider.py (ollama/nova/bedrock switch)
```

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

## attribution

morgan willis wrote the workshop. i walked through it, patched the model config for my
account's security posture, and published this diverged copy so anyone running a
deny-third-party guard can use the samples without modification.

original repo: https://github.com/aws-samples/sample-strands-agents-hands-on-workshop
license: MIT-0 (inherited from the original)
