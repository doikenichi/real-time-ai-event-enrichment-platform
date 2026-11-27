# Challenges

Each weekday gets its own folder, `challenges/day-NNN/`:

- `README.md`: today's 3 challenges, added by the day's pull request
- `REVIEW.md`: feedback on your work, added by the next day's pull request

## Format of `README.md`

```markdown
# Day NNN — <theme>
Phase X · milestone · total time ≈ NN min

## A — Backend (≈15 min)
**Goal:** one sentence, the outcome
**Context:** how this builds on yesterday
**Tasks:** 2–4 concrete steps
**Done when:** the test command(s) that must pass
**Patterns and practices:** which pattern and why
**Hints:** collapsed <details>, progressive
**Docs:** official links, current versions

## B — Full stack (≈15 min)
...
## C — Cloud, DevOps and AI agents (≈15 min)
...

## Stretch (optional)
```

## Rules
- Challenges only use current stable, non-deprecated APIs. Versions are checked when the challenge is written.
- Every challenge has an automated "done when" check: a failing test, a command, or a CI job.
- Reference solutions never appear in the day's challenge. They arrive the next day in `REVIEW.md`.
- Commit messages: `day-NNN: <summary>` (for example, `day-004: idempotent producer with retry`).
