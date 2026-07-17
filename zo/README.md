# Zo — Team Orchestrator

Zo is the team's context-aware Slack buddy: a [Zo Computer](https://docs.zocomputer.com) instance deployed as a teammate in the team's Slack workspace. Anyone on the team can talk to it to provide context, ask questions, or trigger workflows. Its main persona is an **orchestrator** — it doesn't do the work itself; it decomposes requests and routes them to the right worker (Cyrus, Devin, or a human).

Cyrus runs **directly on the Zo server** (a real always-on Linux box), replacing the Mac mini deployment. Zo therefore has first-hand operational context on Cyrus: it can read its logs, check its status, and manage its config.

## Architecture

```text
Slack (team workspace)
  │  DM @Zo or mention in channel — anyone on the team
  ▼
Zo Computer (persistent Linux server)
  ├─ Persona: "Zo — Team Orchestrator" (zo/install/persona.md)
  ├─ Skills: zo-decompose (specialty), zo-orchestrate, zo-cyrus-operate
  ├─ Bio + Rules: team/system context (zo/install/bio.md, rules.md)
  │
  ├─ Cyrus (Zo Service, port 3456) ◀── Linear webhooks (Zo service public URL)
  │     └─ Claude Code → git worktrees → PRs → Devin Review
  │
  └─ Delegation targets
        ├─ Cyrus  — via Linear (create/assign issue; webhook hits the local service)
        ├─ Devin  — via Devin API (bin/devin CLI, installed on Zo)
        └─ Humans — via Slack (@mention with a clear brief)
```

## Layout

| Path | Purpose |
|---|---|
| `install/persona.md` | Zo's main persona — orchestrator identity, division of labor, voice |
| `install/bio.md` | Additive Bio block — team context, systems, delegation targets |
| `install/rules.md` | Always-on + conditional rules (decompose-first, guardrails, approvals) |
| `install/automations.md` | Starter scheduled automations |
| `Skills/zo-decompose/` | **Specialty skill** — decompose any request into routed work items |
| `Skills/zo-orchestrate/` | Route decomposed work to Cyrus / Devin / humans and track it |
| `Skills/zo-cyrus-operate/` | Operate the Cyrus service running on this Zo (status, logs, config) |
| `docs/CYRUS-ON-ZO.md` | Runbook: deploy Cyrus directly on the Zo server |
| `docs/SLACK-DEPLOYMENT.md` | Runbook: deploy Zo as a Slack teammate |

## Bootstrap order

1. `docs/CYRUS-ON-ZO.md` — get Cyrus running as a Zo Service and receiving Linear webhooks.
2. Install persona, bio, rules, automations from `install/` (paste into Zo settings or ask Zo to install them — each file has bootstrap instructions at the top).
3. Copy `Skills/` to `/home/workspace/Skills/` on the Zo.
4. `docs/SLACK-DEPLOYMENT.md` — connect Zo to Slack, pin the orchestrator persona to the workspace channels.

## Team-agnostic by design

All team-specific values (Approver, teammates, Linear workspace, Slack channel, timezone) live in ONE place: the Bio block (`install/bio.md`). Personas, rules, and skills are role-based — nothing about a specific person or workspace is hardcoded — so any team can adopt this system by filling in the Bio placeholders.

## Relationship to Dexter (stationed.dev)

Zo borrows Dexter's proven patterns — decompose-first thinking, explicit division of labor, channel-context awareness, discuss-vs-decide modes, signal-over-noise reporting — but differs in one fundamental way: **Dexter is read-only in Slack; Zo can execute.** Zo runs on its own server with real tools, so its guardrails are rule-based (see `install/rules.md`): destructive/external actions need explicit human approval, everything else it can do.
