"""Module 5: Deploy — serverless Dussault via Bedrock AgentCore.

Packages the agent as an event-driven serverless endpoint. Same pattern
as NGS Lambda + API Gateway: fires on request, scales to zero.

Deploy with: agentcore deploy
"""

import sys
import json
import logging

sys.path.insert(0, "../shared")
sys.path.insert(0, "../01-agent-loop-tools")

from strands import Agent
from strands.agent.conversation_manager import SlidingWindowConversationManager
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from model_provider import get_model
from dussault_tools import lookup_player, get_roster_by_position, get_game_result, get_season_stats, get_coaching_staff
from steering_handlers import FactCheckHandler, tone_handler

logger = logging.getLogger(__name__)

app = BedrockAgentCoreApp()

SYSTEM_PROMPT = """You are Dussault, a 2004 New England Patriots dynasty analyst API.
You receive questions about the 2004 season and return evidence-based answers.

- Look up the data before making claims
- Be specific: cite game weeks, scores, stat lines
- Connect facts to narrative
- If the data isn't in your tools, say so clearly"""

_agent = None


def get_agent():
    global _agent
    if _agent is None:
        _agent = Agent(
            model=get_model(),
            tools=[lookup_player, get_roster_by_position, get_game_result, get_season_stats, get_coaching_staff],
            plugins=[FactCheckHandler(), tone_handler],
            system_prompt=SYSTEM_PROMPT,
            conversation_manager=SlidingWindowConversationManager(window_size=20),
        )
    return _agent


@app.entrypoint
def invoke(payload, context):
    raw_prompt = payload.get("prompt")
    try:
        parsed = json.loads(raw_prompt)
        prompt = parsed.get("prompt", raw_prompt)
    except (TypeError, json.JSONDecodeError):
        prompt = raw_prompt

    if not prompt:
        raise ValueError("Missing required field: prompt")

    agent = get_agent()
    response = agent(prompt)
    return str(response).strip()


if __name__ == "__main__":
    app.run()
