# Challenges

Each weekday gets its own folder, `challenges/day-NNN/`:

- `README.md`: today's 3 challenges, added by the day's pull request
- `REVIEW.md`: feedback on your work, added by the next day's pull request

Every challenge follows **spec → test → code → docs**, matching the shared skills in `.claude/skills/` and `.agents/skills/`.

## Scaffolding
Every challenge is written for the learner's current level on that track (`docs/learning/README.md`). At levels 1 and 2, the README's compact challenge is paired with a step-by-step guide, `challenges/day-NNN/guide-<a|b|c>.md`, in the format of `challenges/day-001/guide-a.md`:
- **Step N: <one idea> (≈N min):** why it matters, the idea in plain words, an example on a different problem, "Your turn", a **Check** (command and expected output), a **Commit**, and collapsed hints
- a glossary of new terms, and short official links to learn more
- at most two new concepts per challenge; the rest is practice of known concepts

The README line under each challenge title also says **Level: N** and **New concepts:** (at most two).

Each challenge also has:
- **Concepts practised:** concept cards in the README, pairing simple words with the industry terms used in job postings and interviews, with links to official docs for further learning (format in the skill `learning-instructor`)
- **a practice drill**, `drill-<a|b|c>.md`: a 5–15 minute warm-up with the same concepts that builds a small, real piece of the product (a helper, a type, a config file), which the challenge then reuses. Only when that isn't possible, a standalone drill in a git-ignored `practice/` folder
- **answer sheets** for the drill and the challenge, kept on the separate `answers` branch (`answers/day-NNN/`), so they can't be seen by accident. Read one on purpose with `lab answer <id>`.

Each day folder also has an empty `FEEDBACK.md` (from `challenges/FEEDBACK-template.md`) for the learner's own report: minutes, difficulty, clarity, hints, and what was wrong in the instructions. The mentor reads it first in the next review, together with `scripts/pace_report.py` (see "Feedback and pace" in `docs/learning/README.md`). A day has up to 3 challenges: fewer when the learner's pace says 3 won't fit in 60 minutes.

## Format of `README.md`

```markdown
# Day NNN — <theme>
Phase X · milestone · total time ≈ NN min

## A — Backend (≈15 min)
**Goal:** one sentence, the outcome
**Feature:** F-id and wave, from docs/product/lean-inception.md, plus the journey step it serves
**Serves:** which goal(s) in docs/GOALS.md and which job requirement
**Context:** how this builds on yesterday
**Industry standard:** the practice or standard followed, and why it's today's choice, with 2–3 primary sources linked
**Book reference:** <short title>, ch. N, "<chapter title>": the concept, in your own words (from docs/READING.md)
**Reference lab (when one applies):** a lab from docs/REFERENCES.md, and what to learn from it
**1. Spec (≈3 min):** review `openspec/changes/<id>/`, and refine one scenario or add the missing edge case
**2. Red:** the failing test(s) to write or finish, named after the scenarios
**3. Green → refactor:** what to implement, plus the pattern to apply and why
**4. Docs (≈2 min):** the diagram, contract, ADR or README to update
**UX principle (UI and alert work):** the Norman principle applied (signifier, feedback, mapping, constraint, conceptual model, error design)
**Done when:** test command(s) pass, and `openspec validate <id> --strict` passes
**Hints:** collapsed <details>, progressive
**Docs:** official links, current versions

## B — Full stack (≈15 min)
...
## C — Cloud, DevOps and AI agents (≈15 min)
...

## Exploratory session variant (once a week, replaces one of A, B or C, ≈15–20 min)
**Charter:** Explore <target> with <tour, data, tool or fault> to discover <risks or questions>
**Tour:** one of Whittaker's tours (see `docs/testing/exploratory/README.md`), and why it fits this week's changes
**Persona:** Maya, Sam or Dev
**Book reference:** EST, ch. N, "<chapter title>"
**Setup (≈2 min):** how to start the stack and which tools to have open
**Session (≈12 min):** a few starting ideas for varying inputs, state, data and environment; no expected results
**Debrief (≈4 min):** fill in the session sheet `docs/testing/exploratory/sessions/day-NNN.md` (PROOF, time split, bugs, new charters)
**Done when:** the session sheet is committed, and each bug has an issue and a failing `@regression` scenario (or a note on why not)

## Stretch (optional)

## Reading this week (Fridays; optional, about 2 × 25 min, outside the 60 min)
One or two focused sections for next week's milestones, plus a reflection prompt. Notes go in `docs/reading-notes/`.

## Interview drill (optional, ≈5 min, outside the 60 min)
One question tied to today's work. Answer it in `docs/interview/README.md`, citing today's code as evidence.
```

## Rules
- Challenges are researched before they're written: current industry standards, primary sources, and current stable, non-deprecated APIs and versions.
- Security is part of the definition of done (the `security-hardening` checklist).
- Every challenge has an automated "done when" check.
- TDD: commit at each green step (`day-NNN: <behaviour>`), so the review can see red → green → refactor.
- Reference solutions never appear in the day's challenge. They arrive the next day in `REVIEW.md`.
- After merge, archive the change: `openspec archive <id>`.
