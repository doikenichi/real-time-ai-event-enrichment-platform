# Challenges

Each weekday gets its own folder, `challenges/day-NNN/`:

- `README.md`: today's 3 challenges, added by the day's pull request
- `REVIEW.md`: feedback on your work, added by the next day's pull request

Every challenge follows **spec → test → code → docs**, matching the shared skills in `.claude/skills/` and `.agents/skills/`.

## Format of `README.md`

```markdown
# Day NNN — <theme>
Phase X · milestone · total time ≈ NN min

## A — Backend (≈15 min)
**Goal:** one sentence, the outcome
**Serves:** which goal(s) in docs/GOALS.md and which job requirement
**Context:** how this builds on yesterday
**Industry standard:** the practice or standard followed, and why it's today's choice, with 2–3 primary sources linked
**1. Spec (≈3 min):** review `openspec/changes/<id>/`, and refine one scenario or add the missing edge case
**2. Red:** the failing test(s) to write or finish, named after the scenarios
**3. Green → refactor:** what to implement, plus the pattern to apply and why
**4. Docs (≈2 min):** the diagram, contract, ADR or README to update
**Done when:** test command(s) pass, and `openspec validate <id> --strict` passes
**Hints:** collapsed <details>, progressive
**Docs:** official links, current versions

## B — Full stack (≈15 min)
...
## C — Cloud, DevOps and AI agents (≈15 min)
...

## Stretch (optional)
```

## Rules
- Challenges are researched before they're written: current industry standards, primary sources, and current stable, non-deprecated APIs and versions.
- Security is part of the definition of done (the `security-hardening` checklist).
- Every challenge has an automated "done when" check.
- TDD: commit at each green step (`day-NNN: <behaviour>`), so the review can see red → green → refactor.
- Reference solutions never appear in the day's challenge. They arrive the next day in `REVIEW.md`.
- After merge, archive the change: `openspec archive <id>`.
