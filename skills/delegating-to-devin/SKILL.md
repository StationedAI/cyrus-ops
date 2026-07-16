---
name: delegating-to-devin
description: Delegate planning, review, or complex implementation work to Devin (Cognition's cloud software agent) via the `devin` CLI. Use when an issue is complex, ambiguous, architectural, or labeled `plan`/`devin` — get Devin to produce an implementation plan or review, then act on it. Also use to hand off entire complex tickets.
---

# Delegating to Devin

Devin is a cloud software agent with its own VM and access to the HGDWAPP/hgdw-lms repo. A `devin` CLI is installed at /opt/homebrew/bin/devin (auth is preconfigured via ~/.cyrus/.env).

## When to delegate
- Issue labeled `plan` or `devin`, or the requester asks for Devin.
- The task is complex/architectural: multi-system changes, unclear root cause, large refactors, DB migrations with prod impact.
- You want an independent plan or review before/after implementing.

Do NOT delegate small mechanical fixes — implement those yourself.

## How
1. Create a session with full context (issue identifier, title, description, relevant comments, your findings):
   ```bash
   devin new "Plan only, do not write code: <task>. Repo: HGDWAPP/hgdw-lms (base branch staging). Context: <details>. Deliver a step-by-step implementation plan with file paths." --title "Plan: <issue-id>"
   ```
   This prints a session_id and URL.
2. Wait for it to finish or block (polls every 30s):
   ```bash
   devin wait <session_id> 2700
   ```
3. Read the result:
   ```bash
   devin messages <session_id>
   devin status <session_id>
   ```
4. Post the plan/result back to the Linear issue (your Linear tools), including the Devin session URL. If you were asked to implement, follow the plan yourself and open the PR.
5. If Devin asks a question (status blocked with a question), answer it with `devin send <session_id> "<answer>"` if you know the answer; otherwise surface the question in the Linear issue.

## Full handoff (Devin implements)
For tickets explicitly meant for Devin end-to-end, create the session with the full ticket and instruction to open a PR against `staging` following AGENTS.md, then just link the session URL in Linear — no need to wait.
