"""Model provider helper for the workshop.

Instead of using the default Bedrock Claude, this module provides
easy access to Ollama (local) and Amazon Nova (Bedrock).

Usage in any workshop module:

    import sys; sys.path.insert(0, "../shared")
    from model_provider import get_model

    agent = Agent(model=get_model(), tools=[...], system_prompt=SYSTEM_PROMPT)

Environment variable MODEL_PROVIDER controls which model to use:
    - "ollama"  (default) — local Ollama with qwen3:8b
    - "nova"    — Amazon Bedrock Nova Pro

You can also override the model ID:
    MODEL_ID=llama3.2 MODEL_PROVIDER=ollama python chat.py
"""

import os
from strands.models.ollama import OllamaModel
from strands.models import BedrockModel


def get_model(provider: str | None = None, model_id: str | None = None):
    """Get the configured model provider.

    Args:
        provider: "ollama" or "nova". Falls back to MODEL_PROVIDER env var, then "ollama".
        model_id: Override the model ID. Falls back to MODEL_ID env var.
    """
    provider = provider or os.environ.get("MODEL_PROVIDER", "ollama")
    model_id = model_id or os.environ.get("MODEL_ID")

    if provider == "ollama":
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        mid = model_id or "qwen3:8b"
        return OllamaModel(host=host, model_id=mid)

    elif provider == "nova":
        mid = model_id or "us.amazon.nova-pro-v1:0"
        return BedrockModel(model_id=mid, region_name=os.environ.get("AWS_REGION", "us-west-2"))

    elif provider == "bedrock":
        # fallback to default Bedrock (Claude) if you want
        mid = model_id or "us.amazon.nova-pro-v1:0"
        return BedrockModel(model_id=mid, region_name=os.environ.get("AWS_REGION", "us-west-2"))

    else:
        raise ValueError(f"Unknown MODEL_PROVIDER: {provider}. Use 'ollama', 'nova', or 'bedrock'.")
