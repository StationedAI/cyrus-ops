# Zo starter automations

> **Bootstrap:** Create each automation (Automations tab, or `tool create_automation`).
> Each runs as another instance of Zo with the same persona, rules, and tools.

## zo-morning-orchestration

- **RRULE:** `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;BYHOUR=8;BYMINUTE=30` (team timezone — see Bio)
- **Delivery:** none (posts to Slack itself)
- **Instruction:**
  Run the morning orchestration sweep. 1) Read /home/workspace/zo/delegations.md and check live status of every open item: Linear issue states for Cyrus items, `devin status <id>` for Devin sessions. 2) Check Cyrus service health (zo-cyrus-operate skill quick check). 3) Update statuses in the delegation log. 4) Post to the team Slack channel ONLY what needs attention: stalled items (>24h no movement), failed sessions, blocks needing a human, Cyrus health problems. If nothing needs attention, post nothing.

## zo-delegation-log-hygiene

- **RRULE:** `FREQ=WEEKLY;BYDAY=FR;BYHOUR=16;BYMINUTE=0` (team timezone — see Bio)
- **Delivery:** none
- **Instruction:**
  Weekly hygiene pass. Archive completed entries from /home/workspace/zo/delegations.md into /home/workspace/zo/archive/delegations-YYYY-WW.md. Compact /home/workspace/zo/context/ index: rebuild /home/workspace/zo/context/INDEX.md listing every note with a one-line summary. Do not delete or rewrite any context note.

## zo-cyrus-watchdog

- **RRULE:** `FREQ=HOURLY;BYMINUTE=15`
- **Delivery:** none
- **Instruction:**
  Silent health check on the Cyrus service: service running, `curl -s localhost:3456/status` responds, no new ERROR lines in ~/.cyrus/cyrus.log since last check (keep a cursor file at /home/workspace/zo/.cyrus-log-cursor). If unhealthy: attempt one restart via the zo-cyrus-operate skill, then re-check. If still unhealthy OR the Linear webhook appears disabled (repeated delivery failures in the log), post an alert to the team Slack channel with the exact symptom and log excerpt. If healthy, do nothing.
