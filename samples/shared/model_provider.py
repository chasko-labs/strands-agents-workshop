"""Model provider helper for the workshop.

Provides validated access to two model backends:

  ollama (default, local, free)
    - Runs locally via ollama serve
    - Uses qwen3:8b by default (override with MODEL_ID env var)
    - Connectivity check verifies the server is reachable and the model is pulled
    - No AWS credentials required

  nova / bedrock (AWS, per-token)
    - Amazon Bedrock Nova Pro (us.amazon.nova-pro-v1:0) by default
    - Requires valid AWS credentials and Bedrock model access in us-west-2
    - Override region with AWS_REGION env var

Usage in any workshop module:

    import sys; sys.path.insert(0, "../shared")
    from model_provider import get_model

    agent = Agent(model=get_model(), tools=[...], system_prompt=SYSTEM_PROMPT)

Environment variable MODEL_PROVIDER controls which backend:
    - "ollama"  (default) — local Ollama with qwen3:8b
    - "nova"    — Amazon Bedrock Nova Pro
    - "bedrock" — same as nova

Override the model ID:
    MODEL_ID=llama3.2 MODEL_PROVIDER=ollama python chat.py
"""

import os
import urllib.request
import urllib.error
import json


def get_model(provider: str | None = None, model_id: str | None = None):
    """Get the configured model provider with connectivity validation.

    Args:
        provider: "ollama" or "nova". Falls back to MODEL_PROVIDER env var, then "ollama".
        model_id: Override the model ID. Falls back to MODEL_ID env var.

    Returns:
        A strands model instance ready for use with Agent().

    Raises:
        ConnectionError: If ollama server is unreachable or model not pulled.
        ImportError: If required packages are missing.
        ValueError: If provider is unrecognized.
    """
    provider = provider or os.environ.get("MODEL_PROVIDER", "ollama")
    model_id = model_id or os.environ.get("MODEL_ID")

    if provider == "ollama":
        return _create_ollama_model(model_id)

    elif provider in ("nova", "bedrock"):
        return _create_bedrock_model(model_id)

    else:
        raise ValueError(
            f"Unknown MODEL_PROVIDER: {provider!r}. Use 'ollama', 'nova', or 'bedrock'."
        )


def _create_ollama_model(model_id: str | None):
    """Create an OllamaModel with connectivity validation."""
    try:
        from strands.models.ollama import OllamaModel
    except ImportError:
        raise ImportError(
            "Ollama support requires: pip install strands-agents"
        )

    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    mid = model_id or "qwen3:8b"

    # connectivity check — verify ollama server is reachable
    tags_url = f"{host}/api/tags"
    try:
        req = urllib.request.Request(tags_url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        raise ConnectionError(
            f"Cannot reach Ollama at {host}\n"
            f"  Error: {e.reason}\n\n"
            f"  Is Ollama running? Start it with:\n"
            f"    ollama serve\n\n"
            f"  Install Ollama if needed:\n"
            f"    curl -fsSL https://ollama.com/install.sh | sh"
        ) from e
    except Exception as e:
        raise ConnectionError(
            f"Unexpected error connecting to Ollama at {host}: {e}\n\n"
            f"  Verify Ollama is running: ollama serve"
        ) from e

    # verify the requested model is available
    available_models = [m.get("name", "") for m in data.get("models", [])]
    # ollama tags include the :latest suffix — check with and without
    model_found = any(
        mid == name or mid == name.split(":")[0] or f"{mid}:latest" == name
        for name in available_models
    )
    if not model_found:
        available_str = ", ".join(available_models[:10]) if available_models else "(none)"
        raise ConnectionError(
            f"Model not found: {mid!r}\n\n"
            f"  Available models: {available_str}\n\n"
            f"  Pull the model with:\n"
            f"    ollama pull {mid}"
        )

    return OllamaModel(host=host, model_id=mid)


def _create_bedrock_model(model_id: str | None):
    """Create a BedrockModel with import validation."""
    try:
        from strands.models import BedrockModel
    except ImportError:
        raise ImportError(
            "Bedrock support requires the AWS SDK:\n"
            "  pip install strands-agents boto3"
        )

    # verify boto3/botocore are importable (BedrockModel needs them at runtime)
    try:
        import boto3  # noqa: F401
        import botocore  # noqa: F401
    except ImportError:
        raise ImportError(
            "Amazon Bedrock requires the AWS SDK:\n"
            "  pip install boto3 botocore\n\n"
            "  Also ensure valid AWS credentials are configured:\n"
            "    aws configure\n"
            "  or set AWS_PROFILE to a profile with Bedrock access."
        )

    mid = model_id or "us.amazon.nova-pro-v1:0"
    region = os.environ.get("AWS_REGION", "us-west-2")

    return BedrockModel(model_id=mid, region_name=region)
