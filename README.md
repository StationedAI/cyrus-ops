# cyrus-ops

Infra-as-code and runbook for the self-hosted [Cyrus](https://github.com/cyrusagents/cyrus) agent running on the Mac mini (`atomics-mini`, Tailscale).

Cyrus connects Linear to Claude Code: assign a Linear issue to Cyrus (or @mention it) and it implements/triages in an isolated git worktree, opens PRs, and streams progress back to the Linear issue.

## Layout

| Path | Purpose |
|---|---|
| `config/config.template.json` | `~/.cyrus/config.json` template (secrets stripped — OAuth tokens are injected by `cyrus self-auth-linear`) |
| `config/env.template` | `~/.cyrus/.env` template (names only, values from your secret store) |
| `launchd/com.cyrus.agent.plist` | launchd service definition (KeepAlive, logs to `~/.cyrus/*.log`) |
| `bin/devin` | `devin` CLI — thin wrapper over the Devin API for delegation (install to `/opt/homebrew/bin/devin`) |
| `skills/delegating-to-devin/SKILL.md` | Claude skill so Cyrus can delegate planning/complex work to Devin (install to `~/.claude/skills/`) |
| `docs/RUNBOOK.md` | Operations: deploy, add a repo, troubleshoot, known failure modes |
| `docs/OBSERVABILITY.md` | Logs, OpenTelemetry tracing, and behavior control |

## Architecture

```text
Sentry ──alert rule──▶ Linear (StationedAI)
                          │  assign / @cyrus
                          ▼  webhook (Tailscale Funnel)
                Mac mini: Cyrus EdgeWorker (launchd)
                          │  git worktree per issue
                          ▼
                Claude Code (subscription OAuth token)
                   │ simple: fix → PR → Devin Review
                   └ complex: `devin` CLI → Devin session (plan/review/handoff)
```

## Multi-repo

Each entry in `config.json`'s `repositories[]` is independent: its own clone, base branch, GitHub URL, and routing (team keys / project keys / labels; a repo without `routingLabels` acts as catch-all). Per-repo behavior comes from that repo's own `AGENTS.md` / `CLAUDE.md`. See `docs/RUNBOOK.md#adding-a-repository`.
