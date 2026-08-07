# .kiro/settings/

MCP server configuration for the workshop crew.

## servers

| server   | purpose                                       | required?              |
| -------- | --------------------------------------------- | ---------------------- |
| context7 | live strands-agents SDK documentation         | yes                    |
| valkey   | workshop state (progress, cache, leaderboard) | no — graceful fallback |

## running locally

context7 runs via npx automatically. for valkey:

```bash
docker run -d --name workshop-valkey -p 6379:6379 valkey/valkey:8
```

if valkey isn't running, all workshop features still work — you just lose
cross-session persistence and leaderboard tracking.
