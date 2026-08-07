"""Optional Valkey connection for workshop state.

Set VALKEY_URL (e.g. redis://localhost:6379) to enable cross-module memory,
research caching, analytics persistence, and leaderboard tracking.
Without it, everything works — you just lose persistence between sessions.

    docker run -d --name workshop-valkey -p 6379:6379 valkey/valkey:8
    export VALKEY_URL=redis://localhost:6379
"""

import os

_client = None


def get_valkey():
    """Returns a Valkey client or None if unavailable."""
    global _client
    if _client is not None:
        return _client
    url = os.environ.get("VALKEY_URL")
    if not url:
        return None
    try:
        import valkey
        _client = valkey.from_url(url, decode_responses=True)
        _client.ping()
        return _client
    except Exception:
        _client = None
        return None


def workshop_user_id() -> str:
    """Stable user identifier for leaderboard + progress tracking."""
    return os.environ.get("WORKSHOP_USER", os.environ.get("USER", "anonymous"))
