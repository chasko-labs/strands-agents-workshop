# agents — strands-agents-workshop

this workshop is primarily developed via kiro-cli crew sessions. the crew
builds datasets, writes module code, validates with evals, and deploys docs.

## active crew for this project

| agent                          | role in this repo                             |
| ------------------------------ | --------------------------------------------- |
| poltergeist-harald-core-anchor | orchestration, planning, dataset curation     |
| ghost-kerouac-research-analyst | 2004 patriots data research, podcast parsing  |
| ghost-hcom-api-delegate        | strands-agents SDK doc lookup via context7    |
| ghost-hcom-python-coder        | python module authoring, tool/hook/skill code |
| ghost-orin-ci-cd               | git ops, PR creation, branch management       |
| ghost-scribe-style-enforcer    | dussault standard enforcement on agent output |

## intent

the long-term direction is interacting with strands agents via multiple surfaces:
kiro-cli (current), langchain, deepagents/dcode. the `.kiro/` config here provides
the crew chassis that builds and maintains the workshop content. workshop participants
themselves use the strands-agents SDK directly — the crew builds what they consume.

## model

all work in this repo uses Amazon Nova Pro (`us.amazon.nova-pro-v1:0`) as the
inference backbone, consistent with accounts enforcing `DenyThirdPartyBedrockInvoke`.
local development uses ollama with qwen3:8b via the shared model_provider.py helper.
