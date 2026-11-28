# Learning path: from guided steps to compact instructions

The learner started this lab new to Python, TypeScript and TDD. Challenges start fully guided and become more independent as skills grow, so that the compact instructions of Day 001 become easy to follow.

## Scaffolding levels
Each track (A backend, B full stack, C cloud/DevOps/agents) has its own level in `.lab/state.json` → `learner.levels`.

| Level | Name | What a challenge gives | Example |
|---|---|---|---|
| **1** | Guided | a step-by-step guide: one new idea per step, an example on a *different* problem, "your turn", a command with the expected output, a commit, hints one at a time, a glossary | `challenges/day-001/guide-a.md` |
| **2** | Supported | numbered steps, each with a goal, a check and hints; examples only for ideas met for the first time | |
| **3** | Hinted | the goal, failing tests, the pattern to use, and collapsed hints | |
| **4** | Independent | the goal, the spec and the "done when" check; you design the tests | the compact part of Day 001's README |

**Moving up:** a track goes up one level after two challenges in a row reviewed as *done* with few or no hints. **Moving down:** after a challenge reviewed as *partial* or *not started* because the instructions were unclear, the track drops one level and the concept is practised again.

## Concept ladder
Each new concept is introduced once with a worked example, then practised until it's routine. The mentor updates this table in every review. A challenge introduces at most **two** new concepts.

| Concept | Track | Introduced | Practised | Status |
|---|---|---|---|---|
| Red → green → refactor | A, B | day 001 | 0 | new |
| Reading a failing test and its error | A, B | day 001 | 0 | new |
| Python functions and type hints | A | day 001 | 0 | new |
| FastAPI routes and the app factory | A | day 001 | 0 | new |
| async / await | A | day 001 | 0 | new |
| Dependency injection (passing collaborators in) | A | day 001 | 0 | new |
| Concurrency with `asyncio.gather` | A | day 001 | 0 | new |
| Timeouts with `asyncio.timeout` | A | day 001 | 0 | new |
| HTTP status codes and problem details | A | day 001 | 0 | new |
| ruff and mypy | A | day 001 | 0 | new |
| TypeScript types, union types, `Record` | B | day 001 | 0 | new |
| React components and props | B | day 001 | 0 | new |
| Testing Library queries by role | B | day 001 | 0 | new |
| GitHub rulesets and repo security settings | C | day 001 | 0 | new |

Statuses: **new** (seen once) → **practising** → **routine** (used without hints twice). Day 001 introduced more concepts than the limit, because it bootstraps everything; the next days repeat these before adding new ones.

## Feedback and pace
Two sources tell the mentor how a day really went. The mentor uses them to size the next day.

**1. Your manual input (wins when the two disagree).** At the end of each session, copy `challenges/FEEDBACK-template.md` to `challenges/day-NNN/FEEDBACK.md` and fill it in: minutes, difficulty, clarity, hints, where you got stuck, and what was wrong in the instructions. Two minutes is enough. If you're short on time, write one PR comment starting with `feedback:` instead.

**2. Metrics from your PRs.** In each review the mentor runs `python3 scripts/pace_report.py --pr <N> --day day-NNN` on the day's PRs. It measures:
- active minutes, from commit timestamps grouped into sessions (gaps over 45 minutes start a new session, and each session adds 15 minutes for the work before its first commit)
- minutes and commits per challenge, from the paths each commit touches
- TDD signals: test-only commits (red steps), and code commits without test changes
- friction signals: your edits to challenge files (usually a fix to the instructions), lint and type fix commits, and messages without the `day-NNN:` prefix

Commits can't see reading, thinking or setup time, so they undercount. Day 001 is the example: the commits show about 100 minutes for A, and you reported "way more than an hour".

**3. Calibration.** The mentor keeps `.lab/pace.json`, one entry per day with the estimate, your reported minutes, the measured minutes and the ratio between them (**pace factor** = actual ÷ estimated, using your minutes when you gave them). For the next day:
- the plan uses the **average pace factor of the last 3 days**: a step estimated at 10 minutes for an expert is planned as 10 × factor
- the day's total, at your pace, stays at or under **60 minutes**. When that doesn't fit 3 challenges, the day has fewer: one guided challenge, plus a small one if it fits. B and C wait their turn. They're carried over, not dropped.
- a difficulty of 4–5 or a clarity of 1–2 on a challenge keeps that track's next challenge at the same size and level, with more examples
- every instruction error you found is fixed in the guide format, and listed in the review
- the factor is expected to fall over the weeks. When it reaches about 1.2, the day returns to 3 challenges.

## When you're stuck
- Open hints one at a time.
- Ask Claude or Codex to explain a step without giving the code ("explain step 4, don't give me the code"). `AGENTS.md` tells them to coach, not solve.
- It's fine for a day to take two sessions. Unfinished work carries over to the next day.
