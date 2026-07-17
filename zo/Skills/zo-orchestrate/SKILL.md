---
name: zo-orchestrate
description: >-
  Delegate approved work items to Cyrus (via Linear), Devin (via the devin CLI),
  or humans (via Slack), and track them in the delegation log. Use when: the user
  approves a decomposition, says "delegate this", "send to cyrus", "have devin
  plan/test this", or asks for status of delegated work.
compatibility: Created for Zo Computer
metadata:
  author: stationed
  category: Orchestration
  display-name: "Zo: Orchestrator"
  emoji: "🎼"
  version: "1.0"
allowed-tools: read_file create_or_rewrite_file run_command use_linear send_slack_message
---

# Zo — Orchestrator

Execute the routing decided by `zo-decompose` (or delegate a single ad-hoc item). Every delegation is logged.

## Delegation mechanisms

### → Cyrus (scoped code)

Cyrus runs on this server and is driven entirely by Linear (the team workspace named in the Bio). Delegate by creating a Linear issue and assigning it to Cyrus:

1. Check repo routing in `~/.cyrus/config.json` — pick the team/labels that route to the right repo (see `docs/RUNBOOK.md#adding-a-repository` in cyrus-ops). If a repo isn't managed yet, flag it instead of delegating.
2. Create the issue with: outcome-oriented title; description containing acceptance criteria, relevant context/links, and constraints. For architectural work add the `plan-with-devin` label (Cyrus will run competitive planning with Devin). For changes needing verification add `devin-test`.
3. Assign to the Cyrus agent (or @mention `@cyrus` in a comment).
4. Cyrus streams progress into the issue and opens a PR against the repo's baseBranch.

### → Devin (planning / complex / testing)

Use the `devin` CLI (installed per cyrus-ops `bin/devin`, auth via `DEVIN_API_KEY`):

```bash
devin new "<full context: task, repo, constraints, deliverable>" --title "<short title>"
devin wait <session_id> 2700   # optional — or check later
devin messages <session_id>
```

Prompts must be self-contained (Devin has no access to this conversation). Include: repo name, base branch, the full ask, acceptance criteria, and "If your GitHub integration cannot access the repo, use a provisioned GitHub credential with HTTPS token auth."

### → Humans (decisions)

Post in Slack to the right person using the decision format:
`[Decision needed]` + `[Options]` (2–4, with trade-offs) + `[Recommendation]` + `[Why]`.
Do not proceed on the item until they answer.

## Tracking

Append every delegation to `/home/workspace/zo/delegations.md`:

```
| date | item | owner | link | status |
| 2026-07-17 | Fix auth redirect loop | cyrus | linear.app/<workspace>/issue/ABC-123 | open |
```

On "status" requests: read the log, then live-check each open item (Linear issue state via `use_linear`, `devin status <id>` for sessions). Update the log, report `item | owner | status | link | next action`, flag anything stalled >24h.

## Failure handling

- Cyrus doesn't pick up an issue → run `zo-cyrus-operate` diagnostics.
- Devin session blocked with a question → answer via `devin send <id> "<answer>"` if you know it; otherwise surface the question in Slack to the requester.
- An item bounces twice → escalate to the Approver (see Bio) with the history, don't retry silently.
