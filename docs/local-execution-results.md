# Strands Agents Workshop — Local Execution Results

Executed 2026-07-31 on rocm-aibox using Ollama (qwen3:8b) as the model provider
instead of AWS Workshop Studio's pre-configured Bedrock Claude.

## Environment

- Python 3.12.3
- strands-agents 1.50.2
- strands-agents-evals 1.0.3
- strands-agents-tools 0.8.5
- Ollama 0.18.0 with qwen3:8b (8.2B params, Q4_K_M)
- Workshop repo: aws-samples/sample-strands-agents-hands-on-workshop

## Model Provider Configuration

Instead of the workshop's default Bedrock Claude, we use `samples/shared/model_provider.py`
which provides `get_model()` returning either OllamaModel or BedrockModel (Nova):

```python
import sys; sys.path.insert(0, "../shared")
from model_provider import get_model
from strands import Agent

agent = Agent(model=get_model(), tools=[...], system_prompt=SYSTEM_PROMPT)
```

Environment variables: `MODEL_PROVIDER` (ollama|nova|bedrock), `MODEL_ID`, `OLLAMA_HOST`

## Module Results

| Module | Status | Key Finding |
|--------|--------|-------------|
| 1 — Agent Loop + Tools | PASS | 2 cycles, 1375 tokens. Native tool calling works with qwen3:8b |
| 2 — Hooks | PASS | RateLimiterHook fires correctly. event.cancel_tool blocks execution |
| 3 — Skills + Steering | PASS | AgentSkills plugin loads SKILL.md files from ./skills/ subdirectories |
| 4 — Session Managers | PASS | FileSessionManager persists and restores messages across agent instances |
| 5 — Deploy | DOCUMENTED | AgentCore Runtime pattern captured (requires Bedrock auth, local-only) |
| 6 — Multi-Agent | PASS | agents-as-tools delegation works. Full orchestrator→specialist chain times out at 180s on this hardware |
| 7 — Evals | PASS | Case/Experiment/OutputEvaluator framework works. Expected output matching verified |

## Architecture Patterns Learned

### Agent Loop
```
User → LLM reasoning → Tool Selection → Tool Execution → back to LLM → Response
```
- Tools: `@tool` decorated functions with docstrings the model reads
- Loop control: `agent.messages` trace, `result.metrics` for cycles/tokens

### Hooks (deterministic code wrapping the loop)
```python
class RateLimiterHook(HookProvider):
    def register_hooks(self, registry: HookRegistry):
        registry.add_callback(BeforeToolCallEvent, self.check)
    def check(self, event: BeforeToolCallEvent):
        event.cancel_tool = "blocked"  # stops execution
```

### Skills (prompt-injected procedural knowledge)
```
./skills/refund-processing/SKILL.md → injected into system context
```

### Session Managers (state persistence)
```python
FileSessionManager(session_id="user-123", storage_dir="./sessions")
# Auto-saves after each invocation, auto-restores on agent construction
```

### Multi-Agent (agents-as-tools pattern)
```python
@tool
def specialist(issue: str) -> str:
    agent = Agent(model=model, tools=[...])
    return str(agent(issue))

orchestrator = Agent(tools=[specialist, ...])
```

### Deploy (AgentCore Runtime)
```python
from bedrock_agentcore.runtime import BedrockAgentCoreApp
app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload, context):
    return str(agent(payload.get("prompt")))

app.run()
```

### Evals (LLM-as-judge)
```python
from strands_evals import Case, Experiment
from strands_evals.evaluators import OutputEvaluator

cases = [Case(name="test", input="...", expected_output="...")]
evaluator = OutputEvaluator(rubric="Score 1 if correct, 0 if not.")
experiment = Experiment(cases=cases, evaluator=evaluator)
```

## Hardware Constraints

- qwen3:8b on RX 6700 XT (12GB VRAM) handles single-agent tool-calling workflows well
- Multi-agent chains (orchestrator → specialist → orchestrator) exceed 180s timeout
- Model warm-up required on first call (~20s cold start)
- For production multi-agent: use Nova Pro via Bedrock or a larger local model

## Blocked: Valkey + S3Vectors Storage

Both depend on AWS SSO token (valkey via SSM port-forward, s3vectors via SigV4).
Run `aws sso login --sso-session kiro-sso` to unblock.
