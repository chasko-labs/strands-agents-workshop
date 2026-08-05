# module 07 — evals

automated output quality + trajectory evaluation.

## what you learn

- `OutputEvaluator(rubric=...)` — LLM-as-judge scores responses
- `TrajectoryEvaluator` — validates tool-call ordering
- `Case` + `Experiment` — define test inputs and expected outputs
- `tools_use_extractor` — capture tool sequences from agent messages
- weak-vs-strong comparison proves the rubric discriminates
- mirrors NGS 90% directional approval from domain experts

## the dussault rubric

scores on: accuracy, specificity (numbers not superlatives), narrative
connection (why not just what), honesty about unknowns.

## run

```bash
cd samples/07-evals
pip install -r requirements.txt
python run_evals.py
```

output shows weak agent (no tools, guesses) vs strong agent (tools, verifies)
with the score gap proving the rubric catches fabrication.
