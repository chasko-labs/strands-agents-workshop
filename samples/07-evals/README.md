# module 07 — evals

automated quality scoring: an LLM-as-judge rates agent output against the Dussault rubric
while a trajectory evaluator confirms the agent followed correct tool-call ordering. this
module proves the evaluation framework discriminates between a strong agent (uses tools,
cites data) and a weak agent (guesses without lookups). same pattern as NGS achieving 90%
directional approval from domain experts.

## prerequisites

- python venv activated (`source ../../.venv/bin/activate`)
- `pip install -r ../../requirements.txt`
- `pip install strands-agents-evals nest_asyncio`
- module 01 completed (you understand tools and the agent loop)
- ollama running with qwen3:8b pulled

> **note:** evals run multiple agent invocations per test case. expect ~5-15 minutes
> total runtime depending on your hardware (ollama) or network latency (bedrock).

## run

```bash
cd samples/07-evals
python run_evals.py                     # ollama (default)
MODEL_PROVIDER=nova python run_evals.py # AWS Bedrock
```

## what you'll see

```
Running output evaluation...
case: pro_bowlers    strong=9.2  weak=3.1  gap=6.1
case: afc_champ     strong=8.8  weak=4.0  gap=4.8
case: dillon_trade  strong=9.0  weak=2.5  gap=6.5

Running trajectory evaluation...
case: lookup_before_claim  strong=PASS  weak=FAIL

Summary: rubric discriminates — strong agent scores 2.5x weak agent
```

## what you learn

- `OutputEvaluator(rubric=...)` scores responses via LLM-as-judge
- `TrajectoryEvaluator` validates tool-call ordering (lookup before claim)
- `Case` + `Experiment` define test inputs and expected behaviors
- `tools_use_extractor` captures tool sequences from agent messages
- weak-vs-strong comparison proves the rubric catches fabrication

## troubleshooting

| error                                                         | fix                                                        |
| ------------------------------------------------------------- | ---------------------------------------------------------- |
| `ModuleNotFoundError: No module named 'strands'`              | `pip install -r ../../requirements.txt`                    |
| `ModuleNotFoundError: No module named 'strands_agents_evals'` | `pip install strands-agents-evals nest_asyncio`            |
| `ModuleNotFoundError: No module named 'dussault_tools'`       | `cd` to this directory first, or ensure module 01 exists   |
| `ConnectionRefusedError` (ollama)                             | run `ollama serve` in another terminal                     |
| `NoCredentialsError` (bedrock)                                | set `export MODEL_PROVIDER=ollama` to skip AWS             |
| runs seem stuck / slow                                        | evals invoke the agent multiple times — 5-15 min is normal |
