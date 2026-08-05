# module 05 — deploy

serverless deployment via bedrock agentcore.

## what you learn

- `BedrockAgentCoreApp()` + `@app.entrypoint` pattern
- event-driven invocation (request in, response out)
- lazy agent initialization (singleton pattern)
- mirrors NGS Lambda + API Gateway: fires on request, scales to zero

## architecture

```
HTTP request → AgentCore → invoke(payload) → Agent → response
```

## deploy

```bash
cd samples/05-deploy
pip install -r requirements.txt
agentcore deploy
```

## local test

```bash
python -c "from main import invoke; print(invoke({'prompt': 'Who was Super Bowl MVP?'}, None))"
```
