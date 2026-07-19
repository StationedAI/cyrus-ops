# AGENT-CONTEXT.md

Agent-facing context for **cyrus-ops** — infrastructure-as-code and runbooks
for the Cyrus agents running on the Zo server. Read the README and
`docs/RUNBOOK.md` for operating procedures; `zo/` mirrors the Zo-side
persona/skills/install docs.

The repo map below is regenerated weekly by
`.github/workflows/agent-repo-docs.yml` — do not edit it by hand.

## Repo map (generated — do not edit by hand)

**./**
- .deploy-check
- .gitignore
- README.md — § Layout; § Architecture; § Multi-repo
**bin/**
- cyrus-autoassign — def gql
- cyrus-ops-deploy — fn note
- cyrus-repo-sync
- cyrus-watchdog — fn ts; fn note; fn alert
- devin
**docs/**
- AGENT-CONTEXT.md — § Repo map (generated — do not edit by hand)
- OBSERVABILITY.md — § Layers; § Behavior control
- RUNBOOK.md — § Deploy from scratch; § Adding a repository; § Troubleshooting; § Service management
**skills/delegating-to-devin/**
- SKILL.md — § When to delegate; § Testing with Devin (mandatory for non-trivial PRs); § How; § Full handoff (Devin implements)
