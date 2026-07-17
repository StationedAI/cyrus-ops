---
name: zo-decompose
description: >-
  Zo's specialty skill: decompose any request — a Slack message, meeting dump,
  voice note, or project idea — into discrete, routable work items with owners.
  Use when: user says "decompose this", "break this down", "process this",
  "here's what we discussed", pastes a raw dump, or makes any request that
  contains more than one piece of work.
compatibility: Created for Zo Computer
metadata:
  author: stationed
  category: Orchestration
  display-name: "Zo: Decomposer"
  emoji: "🧩"
  version: "1.0"
allowed-tools: read_file create_or_rewrite_file run_command send_slack_message
---

# Zo — Decomposer

Turn raw input into a routed work breakdown. This is analysis + proposal only — actual delegation happens via the `zo-orchestrate` skill after the user approves.

## Protocol

### Step 1: Absorb

Accept the input as-is (Slack message, meeting notes, voice dump, idea). Do not ask for clarification yet — extract what you can. Pull relevant context from `/home/workspace/zo/context/` and the recent Slack thread.

### Step 2: Decompose

Break the input into work items. For each item capture:

- **What** — one-sentence outcome (a deliverable, not an activity)
- **Type** — `code` / `plan` / `decision` / `context` / `ops`
- **Repo** — which repo it touches (if code), from `~/.cyrus/config.json` repositories
- **Needs** — inputs, credentials, or prior decisions required
- **Blocked by** — dependency on another item or a person
- **Size** — S (mechanical, clear) / M (scoped, some unknowns) / L (ambiguous or architectural)

Also extract non-work signals: **decisions made** (log to context), **learnings** (log to context), **open questions** (route to a human).

### Step 3: Route

Assign each item an owner using the routing table:

| Item profile | Owner | Mechanism |
|---|---|---|
| `code`, size S/M, clear repo + acceptance criteria | **Cyrus** | Linear issue (assign to Cyrus) |
| `code` size L, `plan`, unclear root cause, multi-system | **Devin** | `devin` CLI session |
| `decision` — architecture, go-live, kill/scale, spend | **The Approver** (see Bio) | Slack, `[Decision needed]` format |
| `context` / `ops` / summaries / drafts | **Zo** | do it directly |
| Sequential chains (A blocks B) | flag the chain | delegate A now, queue B |

Mark which items can run **in parallel** and which are **sequential**.

### Step 4: Propose

Post the breakdown before delegating anything:

```
Decomposed into N items:

PARALLEL — can start now:
1. [S/code → Cyrus] <what> (repo: <repo>)
2. [L/plan → Devin] <what>
3. [decision → Approver] <what>

SEQUENTIAL — queued:
4. [M/code → Cyrus] <what> — blocked by #2

CONTEXT LOGGED: <decisions/learnings captured>
OPEN QUESTIONS: <anything unroutable>

Delegate now? (all / pick numbers / edit first)
```

### Step 5: Hand off

On approval ("go", "all", "1 and 3"), invoke the `zo-orchestrate` skill with the approved items. Log decisions/learnings to `/home/workspace/zo/context/` as dated notes regardless of approval.
