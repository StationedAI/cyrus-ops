# Runbook

Host: Mac mini `atomics-mini` (Tailscale IP 100.106.238.16, DNS `atomics-mini.tail230a40.ts.net`), user `atomicgtmlab`.

## Deploy from scratch

1. `npm install -g cyrus-ai` and install Claude Code (`/opt/homebrew/bin/claude`).
2. Create `~/.cyrus/config.json` with `{"repositories":[]}` (must exist before auth) — then merge in `config/config.template.json`.
3. Copy `config/env.template` → `~/.cyrus/.env` and fill values from the secret store.
   - `CLAUDE_CODE_OAUTH_TOKEN`: run `claude setup-token` interactively (valid ~1 year). Required because launchd services cannot read the macOS keychain — without it Cyrus fails with `401 OAuth access token has expired`.
4. Linear OAuth app (workspace settings → API → applications): callback `https://atomics-mini.tail230a40.ts.net/callback`, webhook `https://atomics-mini.tail230a40.ts.net/linear-webhook`, client credentials + webhooks ON, events: Agent session events, Inbox notifications, Permission changes.
5. `cyrus self-auth-linear` (approve the OAuth link), then `cyrus self-add-repo` per repository.
6. Expose the webhook: `tailscale funnel 3456` (Funnel must be enabled on the tailnet).
7. Install `launchd/com.cyrus.agent.plist` → `~/Library/LaunchAgents/` and `launchctl load` it.
8. Install `bin/devin` → `/opt/homebrew/bin/devin` and `skills/delegating-to-devin/` → `~/.claude/skills/`.
9. GitHub: authenticate git with a PAT that can push branches + open PRs on all managed repos.

## Adding a repository

1. Clone it under `~/.cyrus/repos/<name>` (or run `cyrus self-add-repo`).
2. Add an entry to `repositories[]` in `~/.cyrus/config.json`:
   - `baseBranch`: the branch PRs should target for that repo.
   - Routing: `teamKeys` (Linear team key, e.g. `["STA"]`), `projectKeys`, or `routingLabels`. Priority: description repo tag > labels > project > team > catch-all. A repo with no routing rules is the catch-all — keep exactly one.
3. Per-repo behavior (conventions, branch naming, test commands) lives in that repo's `AGENTS.md` / `CLAUDE.md` — Cyrus's Claude follows the instructions of the repo it works in.
4. `launchctl kickstart -k gui/$(id -u)/com.cyrus.agent` to restart.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| Linear says webhook disabled | Repeated delivery failures (mini offline / funnel down). Re-enable: Linear → settings → API → applications → Cyrus → Webhooks toggle. |
| `401 OAuth access token has expired` in Linear comments | Claude keychain auth unavailable to launchd. Refresh `CLAUDE_CODE_OAUTH_TOKEN` via `claude setup-token`, restart service. |
| Cyrus asks "which repository?" on every issue | No catch-all repo — remove `routingLabels` from the default repo or add routing for the issue's team. |
| Webhook endpoint 401 on unsigned POST | Expected — signature validation working. |
| Nothing happens on assignment | Check `tailscale funnel status`, `curl https://atomics-mini.tail230a40.ts.net/status`, and `tail -f ~/.cyrus/cyrus.log`. |

## Service management

```bash
launchctl list | grep cyrus                 # running?
launchctl kickstart -k gui/$(id -u)/com.cyrus.agent   # restart
tail -f ~/.cyrus/cyrus.log ~/.cyrus/cyrus.err.log
curl -s https://atomics-mini.tail230a40.ts.net/status  # {"status":"idle"}
```
