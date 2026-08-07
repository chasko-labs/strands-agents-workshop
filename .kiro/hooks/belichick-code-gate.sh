#!/usr/bin/env bash
# belichick-code-gate.sh — blocks orchestrator from writing source code
# Teaching point: this is how kiro hooks enforce delegation discipline
#
# Exit codes:
#   0 = allow the write
#   2 = block the write (kiro treats exit 2 as hard block)

TOOL_INPUT="${KIRO_TOOL_INPUT:-}"

# Block writes to module source code
if echo "$TOOL_INPUT" | grep -qE '(samples/|patriots_data\.py|dussault_tools\.py)'; then
	echo "[GATE] Blocked: orchestrator does not write source code. Delegate to ghost-weis-offense-author."
	exit 2
fi

# Allow writes to .kiro/, docs/, README
exit 0
