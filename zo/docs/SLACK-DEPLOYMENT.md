# Runbook — Zo as a Slack Teammate

Deploy Zo into the team's Slack workspace so anyone can DM it or mention it in channels. Slack is a native Zo channel — no webhook server or bot code to build (this is the big simplification vs the Dexter approach in stationed.dev, which needed its own `/api/slack/events` endpoint, HMAC verification, dedup, and LLM fallback).

## Prerequisites

- Cyrus running on the Zo (see `CYRUS-ON-ZO.md`) — Zo orchestrates it, so deploy it first.
- Persona, Bio (placeholders filled!), Rules, Skills, and Automations installed from `../install/` and `../Skills/`.

## Steps

### 1. Connect Slack

In Zo: **Settings → Channels → Slack** → add the Zo app to the team workspace (a workspace admin approves the install). Zo then responds to DMs and @mentions; mentions auto-thread.

### 2. Pin the orchestrator persona

Slack keeps its own active persona per channel. In a Slack DM with Zo:

```
/persona Zo — Team Orchestrator
```

Repeat in each channel where Zo is mentioned (or set it once and verify with `/info`). Also pick the model for the channel with `/model` if the default isn't right.

### 3. Invite Zo where the work happens

Invite Zo to the team's working channels (engineering, ops, the orchestration-updates channel named in the Bio). Zo only speaks when mentioned, DM'd, or when an automation posts.

### 4. Verify the golden paths

Run each of these in Slack and confirm behavior:

| Test | Expect |
|---|---|
| DM: "what can you do?" | Orchestrator persona voice, offers decompose/route/status/context |
| Mention with a multi-part request | `zo-decompose` breakdown with routed items + "Delegate now?" |
| "go" after a breakdown | `zo-orchestrate` runs: Linear issue(s) created for Cyrus, `devin new` for Devin items, delegation log updated |
| "status" | Table from the delegation log + live checks |
| "here's some context: <decision>" | One-line ack + note appended under `/home/workspace/zo/context/` |
| "is cyrus healthy?" | `zo-cyrus-operate` quick check with real service status |

### 5. Universal commands (teach the team)

`/new` (fresh conversation), `/conversations`, `/info`, `/model [name]`, `/persona [name]`, `/help`.

## Notes

- **One Zo, shared identity:** every teammate talks to the same Zo instance — that's what makes it context-aware across the team. Guarded actions (external comms, destructive ops) are approval-gated by the Rules regardless of who asks; the Approver is defined in the Bio.
- **Threading:** each Slack thread is its own conversation; cross-thread continuity comes from the context store and the delegation log, which is why the append-only logging rules matter.
- **Automations post proactively** (morning sweep, watchdog alerts) into the channel named in the Bio — if the channel changes, update the Bio.
