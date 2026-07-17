---
name: zo-cyrus-operate
description: >-
  Operate the Cyrus agent running as a service on this Zo server: health checks,
  logs, restarts, adding repos, fixing webhook/auth failures. Use when: Cyrus is
  down, not picking up Linear issues, erroring, needs a new repo added, or a
  scheduled watchdog check runs.
compatibility: Created for Zo Computer
metadata:
  author: stationed
  category: Operations
  display-name: "Zo: Cyrus Operator"
  emoji: "🔧"
  version: "1.0"
allowed-tools: read_file create_or_rewrite_file run_command list_services diagnose_service update_service send_slack_message
---

# Zo — Cyrus Operator

Cyrus runs on this server as a Zo Service named `cyrus` (port 3456). Config lives in `~/.cyrus/` (`.env`, `config.json`, `repos/`, `worktrees/`, logs). Full deployment runbook: `docs/CYRUS-ON-ZO.md` in cyrus-ops.

## Quick health check

```bash
curl -s localhost:3456/status          # expect {"status":"idle"} or active
tail -50 ~/.cyrus/cyrus.log            # recent activity / errors
```

Plus `list_services` → `cyrus` should be running. Use `diagnose_service` if not.

## Diagnostics by symptom

| Symptom | Cause / fix |
|---|---|
| Service down | `diagnose_service`, then restart via `update_service` (or `list_services` → restart). Check `~/.cyrus/cyrus.err.log`. |
| Runs but never receives issues | Linear auto-disabled the OAuth app webhook after delivery failures. A human must re-enable: linear.app → Settings → API → applications → Cyrus → Webhooks toggle. Post the exact instruction to Slack. |
| `401 OAuth access token has expired` in issue comments | `CLAUDE_CODE_OAUTH_TOKEN` in `~/.cyrus/.env` expired/revoked. A human must run `claude setup-token` and update the value; then restart the service. |
| Asks "which repository?" on every issue | No catch-all repo in `config.json` — exactly one repo should have no routing rules. |
| Issue routed to wrong repo | Routing is cached per issue at first touch. Fix routing in `config.json` (hot-reloaded), then use a fresh issue. |
| No PRs created | GitHub auth broken in service context: `gh auth status` as the service user. |
| Webhook endpoint 401 on unsigned POST | Expected — signature validation working. |

## Adding a repository

1. `cyrus self-add-repo <git-url>` (clones under `~/.cyrus/repos/`).
2. Edit the new `repositories[]` entry in `~/.cyrus/config.json`: set `baseBranch`, routing (`teamKeys` / `projectKeys` / `routingLabels`), and the `appendInstruction` for Devin delegation (copy from an existing entry). Keep exactly one catch-all repo.
3. Config hot-reloads — verify with a test issue.

## Rules of engagement

- Never edit `linearWorkspaces` tokens in `config.json` — they're injected by `cyrus self-auth-linear`.
- Never print secret values from `~/.cyrus/.env` to Slack or logs.
- One restart attempt max before reporting; don't restart-loop.
- After any fix, confirm health (`/status` + log tail) and report what was wrong, what was done, and current state.
