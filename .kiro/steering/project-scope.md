# project scope — strands-agents-workshop

## in scope

- 7 workshop modules teaching strands-agents SDK patterns
- 2004 new england patriots dynasty as the sole use case
- datasets in `samples/shared/patriots_data.py`
- each module: chat.py (REPL) + notebook (cells) + README.md
- model provider: nova pro (bedrock) or ollama (local)
- eval rubric based on mike dussault's writing standards

## out of scope

- production agent deployment beyond module 05 demo
- real-time data ingestion (all data is mock/historical)
- non-2004 patriots seasons
- payment or subscription features
- user authentication

## quality bar

agent output aspires to the dussault standard:

- lead with findings, not process
- cite specific data (game weeks, scores, stat lines)
- connect facts to narrative
- name what's unknown rather than hedge
- players described in terms of team function
