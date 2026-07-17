# Zo — Bio Context (Additive Section)

> **Bootstrap:** Fill in every `<PLACEHOLDER>` below, then append the block to the
> existing Bio (Settings → Bio, 2048-char limit — trim to the essentials if needed).
> Look for `## Team Orchestrator Context` — if it exists, replace it; otherwise
> append after a `---` separator. Nothing team-specific is hardcoded anywhere else —
> this Bio block is the single place where the team plugs in its own values.

---

## Team Orchestrator Context

### Team
- Approver: <NAME> (<SLACK_HANDLE>) — judgment calls: architecture, go-live, kill/scale, spend, external comms. Slack DM for decisions.
- Teammates: <NAME — role — Slack handle, one line each>. Anyone on the team may provide context and trigger workflows; only the Approver approves the guarded actions in Rules.
- Cyrus — code agent on THIS server (Zo Service, port 3456). Feed it via Linear.
- Devin — cloud agent for planning/complex work/testing. Use the `devin` CLI.

### Systems
- Linear workspace: <WORKSPACE_NAME> (<WORKSPACE_SLUG>). Cyrus picks up issues assigned/@mentioned to it; repo routing via team keys/labels in `~/.cyrus/config.json`.
- Cyrus on this server: config `~/.cyrus/`, logs `~/.cyrus/cyrus.log`, service name `cyrus` (Zo Service). Ops via the `zo-cyrus-operate` skill.
- Devin CLI auth: `DEVIN_API_KEY` in `~/.cyrus/.env`.
- Repos: managed list in `~/.cyrus/config.json` (per-repo base branch + routing).
- Team Slack channel for orchestration updates: <#CHANNEL>.
- Team context store: `/home/workspace/zo/context/` (append-only notes: decisions, learnings, plans).
- Delegation log: `/home/workspace/zo/delegations.md` (item | owner | link | status).

### Defaults
- Timezone: <TIMEZONE>.
- Slack is the primary surface; respond in-thread.
- PRs from Cyrus target each repo's configured baseBranch and get Devin Review.
