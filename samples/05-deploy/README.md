# module 05 — deploy

package Dussault as a serverless endpoint using Bedrock AgentCore. this module turns your
local agent into an event-driven service that fires on HTTP request and scales to zero when
idle. same pattern as NGS Lambda + API Gateway: request in, inference runs, response out,
no persistent compute.

## prerequisites

- python venv activated (`source ../../.venv/bin/activate`)
- `pip install -r ../../requirements.txt`
- modules 01 and 03 completed (agent loop + steering handlers)
- AWS credentials configured with Bedrock access (for deploy)

> **note:** AgentCore is an AWS-only service. without AWS creds you can still test
> `invoke()` locally but cannot deploy. set `MODEL_PROVIDER=ollama` to run the local
> test without any AWS dependency.

## run

```bash
cd samples/05-deploy

# local test (no deploy, no AWS needed):
python -c "from main import invoke; print(invoke({'prompt': 'Who was Super Bowl MVP?'}, None))"

# full deploy (requires AWS creds + agentcore CLI):
agentcore deploy
```

## what you'll see

```
# local invoke:
{'response': 'Deion Branch was named Super Bowl XXXIX MVP...'}

# after deploy:
Deploying agent to AgentCore...
Running on http://localhost:8080
```

> **cost note:** AgentCore runs on AWS infrastructure. remember to tear down with
> `agentcore destroy` when you are done to avoid ongoing charges.

## what you learn

- `BedrockAgentCoreApp()` + `@app.entrypoint` pattern for serverless agents
- event-driven invocation (request payload in, structured response out)
- lazy agent initialization via singleton pattern (cold start optimization)
- local `invoke()` testing before cloud deployment

## troubleshooting

| error                                                   | fix                                                                                  |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| `ModuleNotFoundError: No module named 'strands'`        | `pip install -r ../../requirements.txt`                                              |
| `ModuleNotFoundError: No module named 'dussault_tools'` | `cd` to this directory first, or ensure module 01 exists                             |
| `NoCredentialsError` (bedrock)                          | set `export MODEL_PROVIDER=ollama` for local test, or configure AWS creds for deploy |
| `agentcore: command not found`                          | `pip install strands-agents[agentcore]`                                              |
| charges after testing                                   | run `agentcore destroy` to tear down the deployment                                  |
