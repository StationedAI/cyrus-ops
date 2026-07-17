# Runbook — Cyrus on Zo

Deploy Cyrus directly on the Zo Computer server (Linux), replacing the Mac mini deployment. The Zo server is always-on with a persistent filesystem, and Zo itself becomes Cyrus's operator (see `../Skills/zo-cyrus-operate/`).

What changes vs the Mac mini (`../../docs/RUNBOOK.md`):

| Mac mini | Zo |
|---|---|
| launchd plist (`launchd/com.cyrus.agent.plist`) | **Zo Service** (managed, auto-restart, service doctor) |
| Tailscale Funnel public URL | **Zo Service public HTTP proxy URL** (`*.zocomputer.io`) |
| macOS keychain gotcha for Claude auth | Same fix applies: long-lived `CLAUDE_CODE_OAUTH_TOKEN` (services don't get interactive auth) |
| Human SSHes in to operate | Zo operates it conversationally (logs, restarts, config) |

## Phase 1 — Install (in a Zo chat or SSH)

```bash
# Node 20+ ships on Zo; install the agents
npm install -g cyrus-ai @anthropic-ai/claude-code

# GitHub auth for PR creation (PAT with repo scope on all managed repos)
gh auth login
git config --global user.name  "Cyrus Agent"
git config --global user.email "<CYRUS_GIT_EMAIL>"

# Config skeleton (must exist before Linear auth)
mkdir -p ~/.cyrus
echo '{"repositories":[]}' > ~/.cyrus/config.json
```

## Phase 2 — Claude auth

Mint a long-lived token interactively once (a service process can't complete interactive OAuth):

```bash
claude setup-token   # copy the token
```

Goes into `~/.cyrus/.env` as `CLAUDE_CODE_OAUTH_TOKEN` (or set `ANTHROPIC_API_KEY` instead).

## Phase 3 — Create the Zo Service (gets you the public URL)

Ask Zo (or use `tool create_service`):

> Create a service named `cyrus`: entrypoint `cyrus`, working directory `~`, port `3456`, public HTTP access.

Note the service's **public HTTP proxy URL** (`https://<something>.zocomputer.io`) — this replaces the Tailscale Funnel URL and is your `CYRUS_BASE_URL`. The service will crash-loop until `.env` exists; that's fine, finish config then restart.

## Phase 4 — Linear OAuth application

In Linear (workspace admin): Settings → API → OAuth Applications → Create new:

- Name: `Cyrus`; Callback URL: `https://<service-url>/callback`
- Client credentials ON; Webhooks ON, URL `https://<service-url>/linear-webhook`
- App events: **Agent session events**, Inbox notifications, Permission changes

Copy Client ID, Client Secret, Webhook signing secret.

## Phase 5 — Configure

`~/.cyrus/.env` (template: `../../config/env.template`; Linux path notes below):

```bash
LINEAR_DIRECT_WEBHOOKS=true
CYRUS_BASE_URL=https://<service-url>          # the Zo service public URL
CYRUS_SERVER_PORT=3456
LINEAR_CLIENT_ID=...
LINEAR_CLIENT_SECRET=...
LINEAR_WEBHOOK_SECRET=...
CLAUDE_CODE_OAUTH_TOKEN=...                   # from Phase 2
DEVIN_API_KEY=...                             # for the devin delegation CLI
```

Then authorize and add repos:

```bash
cyrus self-auth-linear      # approve in browser
cyrus self-add-repo https://github.com/<org>/<repo>.git
```

Edit `~/.cyrus/config.json` per repo: `baseBranch`, routing (`teamKeys`/`projectKeys`/`routingLabels` — keep exactly one catch-all), and `appendInstruction` (copy the Devin-delegation instruction from `../../config/config.template.json`, fixing paths from `/Users/...` to `/root` or `/home/<user>` and the devin CLI path to `/usr/local/bin/devin`). Config hot-reloads.

## Phase 6 — Devin CLI + skill

```bash
install -m 755 bin/devin /usr/local/bin/devin
mkdir -p ~/.claude/skills && cp -r skills/delegating-to-devin ~/.claude/skills/
```

## Phase 7 — Start and verify

Restart the `cyrus` Zo Service, then:

- [ ] `curl -s localhost:3456/status` → `{"status":"idle"}`
- [ ] `curl https://<service-url>` reaches the server (any response ≠ timeout)
- [ ] `cyrus check-tokens` reports valid Linear tokens
- [ ] Delegate a test Linear issue → worktree appears under `~/.cyrus/worktrees/`, activities stream into the issue
- [ ] Session ends with a PR against the repo's `baseBranch`
- [ ] Restart the service → sessions still authenticate (long-lived token survives)

## Ongoing operation

Zo operates Cyrus itself via the `zo-cyrus-operate` skill, and the `zo-cyrus-watchdog` automation (see `../install/automations.md`) health-checks hourly. Known failure modes and fixes are in that skill; they're the same gotchas as the Mac mini (webhook auto-disabled by Linear, expired Claude token, missing catch-all repo).

## Migrating from the Mac mini

1. Deploy on Zo per this runbook, using the **same Linear OAuth app** — just update its callback + webhook URLs to the Zo service URL.
2. Stop the Mac mini service: `launchctl unload ~/Library/LaunchAgents/com.cyrus.agent.plist` (and the watchdog/reposync/opsdeploy plists).
3. Verify a fresh test issue routes to the Zo deployment.
4. Keep the mini's `~/.cyrus/` as backup for a week, then decommission.
