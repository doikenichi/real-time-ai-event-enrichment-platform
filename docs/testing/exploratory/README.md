# Exploratory testing

Exploratory testing here follows James Whittaker's *Exploratory Software Testing* (EST, see `docs/READING.md`) and session-based test management: a **charter**, a **time box**, a **tour**, a **persona**, and a **debrief**. It complements the BDD regression suite: exploration finds the surprises, and every bug it finds becomes a `@regression` scenario. Skill: `exploratory-testing`.

## Cadence
Once a week, one of the day's three challenges is a 15–20 minute session on what changed that week. Session sheets go in `sessions/day-NNN.md`.

## Tours for this product
Pick the tour that fits the week's change. Full table in the `exploratory-testing` skill.

| When the change is… | Try |
| --- | --- |
| a new endpoint or form | Couch Potato (defaults, empty input), Antisocial (invalid and malformed input), Intellectual (the hardest inputs) |
| a new event flow, producer or consumer | FedEx (follow one event by correlation id to every output), Obsessive-Compulsive (duplicates, replays), Saboteur (stop Kafka or the database) |
| a new dashboard view or alert | Supermodel (surface, wording, Norman's checklist), Landmark (hop between features), Supporting Actor (empty states, filters) |
| a new background job or TTL | After-Hours (what runs unattended), All-Nighter (long-running sessions and streams) |
| a bug fix or refactor | Bad-Neighborhood (around the fix), Prior Version (compare with the last release) |
| docs or a runbook | Guidebook (follow it exactly) |
| a new agent behaviour | Intellectual and Antisocial (tricky and hostile prompts in events), Collector's (every output type) |

## Session sheet template (`sessions/day-NNN.md`)
```markdown
# Session: <short title> (day NNN, YYYY-MM-DD)
**Charter:** Explore <target> with <resources> to discover <information>
**Tour:** <name> · **Persona:** <Maya | Sam | Dev> · **Time box:** NN min
**Build / commit:** <sha> · **Environment:** <compose, browser, tools>

## Notes (as you go)
- HH:MM tried … → saw …
- Question: …

## Bugs
| # | Summary | Severity | Issue | Regression scenario |
|---|---|---|---|---|

## Debrief (PROOF)
- **Past:** what happened
- **Results:** what was found
- **Obstacles:** what got in the way
- **Outlook:** what's left; new charters
- **Feelings:** confidence in this area (1–5) and why
- **Time split:** design and execution NN% · bug investigation NN% · setup NN%
```

## Rules
- Use only synthetic data, your own premises, or public sample footage (ADR-0007).
- Never explore against free-tier production hosts with load or fault tools; use the local or disposable stack.
- AI agents may suggest charters and variations; you run the session and judge the results.
