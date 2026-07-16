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

## Plan-with-Devin workflow (labeled issues): competitive planning
Two independent plans are produced, then the strongest wins. Devin reads the repo on its own machine (it has repo access + provisioned credentials) — do not feed it your findings; independence is the point.
1. Kick off the Devin planning session FIRST (so it runs while you work), with the full ticket verbatim:
   ```bash
   devin new "Plan only, do not write code or open PRs. Investigate the HGDWAPP/hgdw-lms repo yourself first: find what already exists that is relevant (tables, flows, migrations, prior PRs) — do not assume greenfield. Ticket <issue-id>: <full title + description + relevant comments>. Deliver: repo findings, then a step-by-step implementation plan with file paths, migration steps, and test strategy." --title "Plan: <issue-id>"
   ```
2. While Devin works, write YOUR OWN plan from your own repo investigation. Do not look at Devin's output before yours is done.
3. `devin wait <session_id> 2700`, then `devin messages <session_id>` to get Devin's plan.
4. **Assess both plans** against the repo reality: correctness of assumptions, coverage of edge cases/migrations/RLS, test strategy, risk. Pick the stronger one as the base and fold in anything the other caught that it missed.
5. **Post to the Linear issue**: the canonical (merged) plan, a short assessment of the two plans (what each got right/missed), and the Devin session URL.
6. Implement against the canonical plan and open the PR. If during implementation the repo contradicts the plan, note the discrepancy in a comment and ask Devin (`devin send`) or flag it for the requester rather than silently diverging.

## Testing with Devin (mandatory for non-trivial PRs)
Devin is the designated tester: its VM has the full environment and all credentials provisioned. After you open a PR for any non-trivial change (and always when the issue has a `devin-test` label or asks for verification), create a Devin testing session:
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
