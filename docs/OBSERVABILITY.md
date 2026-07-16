# Observability & Behavior Control

## Layers

### 1. Linear activity threads (per issue)
Every Cyrus session streams its actions as a thread on the Linear issue — the first place to look for "what did it do and why".

### 2. Structured logs (host)
`~/.cyrus/cyrus.log` / `cyrus.err.log`: EdgeWorker events tagged with `{session, platform, issue}` — webhook receipt, routing decisions, Claude session lifecycle (`Session completed (subtype: success)`), errors. launchd rotates nothing; logrotate or periodic truncation recommended.

### 3. OpenTelemetry (Claude Code native)
Claude Code exports metrics + events via OTLP when enabled in `~/.cyrus/.env` (see `config/env.template`): token usage, cost per session, tool invocations, session duration, model used. Point `OTEL_EXPORTER_OTLP_ENDPOINT` at any OTLP collector (Grafana Cloud, Honeycomb, self-hosted). Every Cyrus-triggered Claude run is then traced without code changes.

## Behavior control

| Lever | What it controls |
|---|---|
| Repo `AGENTS.md` / `CLAUDE.md` | Conventions per codebase: base branch, PR rules, test commands, style. Cyrus's Claude reads the repo it's working in. |
| Label-based prompt modes | Linear labels select the system prompt: `scoper` (plan only), `debugger` (root-cause), `builder` (implement), `orchestrator` (decompose into sub-issues). |
| `~/.claude/settings.json` permissions | Allow/deny rules for tools and shell commands Claude may run on the mini. |
| Skills (`~/.claude/skills/`) | Reusable procedures, e.g. `delegating-to-devin` for escalating complex work to a Devin session. |
| `config.json` routing | Which repos exist, which issues route where, base branches. |
| Model selection | Opus with Sonnet fallback by default; configurable per repository. |
