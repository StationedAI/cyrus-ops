---
name: delegating-to-devin
description: Delegate planning, review, or complex implementation work to Devin (Cognition's cloud software agent) via the `devin` CLI. Use when an issue is complex, ambiguous, architectural, or labeled `plan`/`devin` — get Devin to produce an implementation plan or review, then act on it. Also use to hand off entire complex tickets.
---

# Delegating to Devin

Devin is a cloud software agent with its own VM and access to the HGDWAPP/hgdw-lms repo. A `devin` CLI is installed at /opt/homebrew/bin/devin (auth is preconfigured via ~/.cyrus/.env).

## When to delegate
- **MANDATORY**: the issue has a `plan-with-devin` or `devin` label, or the requester asks for Devin. On these issues you MUST delegate planning to Devin — even if you believe you could plan it yourself. This is a hard rule, not a judgment call.
- Otherwise at your discretion: the task is complex/architectural (multi-system changes, unclear root cause, large refactors, DB migrations with prod impact), or you want an independent plan or review.

Do NOT delegate small mechanical fixes — implement those yourself.

## Plan-with-Devin workflow (labeled issues)
Devin owns repo investigation AND planning. Do NOT do your own repo recon first — delegate immediately and let Devin read the codebase on its own machine (it has repo access).
1. Create the Devin session with the full ticket verbatim:
   ```bash
   devin new "Plan only, do not write code or open PRs. Investigate the HGDWAPP/hgdw-lms repo yourself first: find what already exists that is relevant (tables, flows, migrations, prior PRs) — do not assume greenfield. Ticket <issue-id>: <full title + description + relevant comments>. Deliver: repo findings, then a step-by-step implementation plan with file paths, migration steps, and test strategy." --title "Plan: <issue-id>"
   ```
2. `devin wait <session_id> 2700`, then `devin messages <session_id>` to get the plan.
3. **Post Devin's full plan as a comment on the Linear issue** (include the Devin session URL), clearly marked as "Plan from Devin".
4. Implement against that plan and open the PR. If during implementation the repo contradicts the plan, note the discrepancy in a comment and ask Devin (`devin send`) or flag it for the requester rather than silently diverging.

## Testing with Devin
Devin is excellent at end-to-end testing. After you open a PR for a non-trivial change (or when the issue asks for verification), you may create a Devin session to test it:
```bash
devin new "Test PR <url> on HGDWAPP/hgdw-lms: check out the branch, run the test suite, and exercise the changed behavior end-to-end with real assertions (no stub checks, no visual-only verification). Report the derived contract, failure modes covered, and pasted actual test output; list anything unverified and why. Do not push changes." --title "Test: <issue-id>"
```
Link the testing session URL in the Linear issue and in the PR description.

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
