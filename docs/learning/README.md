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

## Drills, challenges and answer sheets
Each challenge comes in three parts:
1. **Concepts practised:** short cards with the idea in simple words, the industry term, related words you'll hear, and links to learn more.
2. **A practice drill** (`challenges/day-NNN/drill-<x>.md`): the same ideas on a small, different problem, 5–15 minutes, in a git-ignored `practice/` folder. Do it first; the real challenge then feels familiar.
3. **The challenge** itself, with its guide.

**Answer sheets** exist for both the drill and the challenge, but they're on a separate `answers` branch, never in your working folder, so you can't see them by accident. When you've tried (or been stuck for 15 minutes), read one on purpose:
```bash
lab answer drill-b        # the drill's answer, for the current day
lab answer b              # the challenge's answer
lab answer a 001          # a specific day
```
It asks "have you tried?" first, and notes in your session log that you opened it, which counts as a hint in the review, not a failure.

## Feedback and pace
Two sources tell the mentor how a day really went. The mentor uses them to size the next day.

**0. The timer (no effort).** `lab start` and `lab stop` (or `lab finish`) record your sessions in `challenges/day-NNN/sessions.log`. That's your real time, without tracking anything.

**1. Your manual input (wins when the two disagree).** At the end of each session, copy `challenges/FEEDBACK-template.md` to `challenges/day-NNN/FEEDBACK.md` and fill it in: a rough time (a range or "at least" is fine), difficulty, clarity, hints, where you got stuck, and what was wrong in the instructions. Two minutes is enough. If you're short on time, write one PR comment starting with `feedback:` instead.

**2. Metrics from your PRs.** In each review the mentor runs `python3 scripts/pace_report.py --pr <N> --day day-NNN` on the day's PRs. It measures:
- active minutes, from commit timestamps grouped into sessions (gaps over 45 minutes start a new session, and each session adds 15 minutes for the work before its first commit)
- minutes and commits per challenge, from the paths each commit touches
- TDD signals: test-only commits (red steps), and code commits without test changes
- friction signals: your edits to challenge files (usually a fix to the instructions), lint and type fix commits, and messages without the `day-NNN:` prefix

Commits can't see reading, thinking or setup time, so they undercount. Day 001 is the example: the commits show about 100 minutes for A, and you reported at least 2.5 hours.

**3. Calibration.** The mentor keeps `.lab/pace.json`, one entry per day with the estimate, your reported minutes, the measured minutes and the ratio between them (**pace factor** = actual ÷ estimated, using your time when you gave it; for "at least N" use N, for a range use its middle). For the next day:
- the plan uses the **average pace factor of the last 3 days**: a step estimated at 10 minutes for an expert is planned as 10 × factor
- the day's total, at your pace, stays at or under **60 minutes**. When that doesn't fit 3 challenges, the day has fewer: one guided challenge, plus a small one if it fits. B and C wait their turn. They're carried over, not dropped.
- a difficulty of 4–5 or a clarity of 1–2 on a challenge keeps that track's next challenge at the same size and level, with more examples
- every instruction error you found is fixed in the guide format, and listed in the review
- the factor is expected to fall over the weeks. When it reaches about 1.2, the day returns to 3 challenges.

## Going faster
Day 001's A took at least 2.5 hours against a 50-minute guided estimate. Most first-day time goes to things that aren't the lesson. Each fix below targets one of them, and the pace report shows whether it worked.

| Time sink | Fix | Metric that shows it |
|---|---|---|
| Typing long commands, and typos in them | `scripts/lab` (on your PATH as `lab` in the dev container): `lab test a`, `lab watch a`, `lab check a`, `lab save "…"` | fewer friction commits |
| Waiting for and re-running tests | `lab watch a` (or `b`) re-runs the tests on every save; keep it open in a second terminal | median minutes between commits |
| Lint and type errors at the end | the dev container formats and fixes on save, and shows type errors as you type | lint or type fix commits |
| Setup and boilerplate (workspace files, config, installs) | at levels 1–2 the mentor provides it, as a setup script or committed config; your time goes to the tests and the logic | minutes in commits that touch only config |
| Being stuck without knowing it | the timer (`lab start` / `lab stop`) and a rule: open a hint after **10 minutes** stuck, ask the AI tutor after **20** | time per step vs the guide's estimate |
| Reading too much | each guide starts with a 5-line **fast path**; read the full step only when the fast path isn't enough | |
| Git and PR wrangling | one loop: `lab start NNN` → work → `lab save` at each red and green → `lab finish`. When the mentor updates your day, `lab pull` | PRs and force pushes per day |
| Polishing | green is enough: make it pass, commit, then improve only if a refactor step asks | |

**Ask the AI tutor** (Claude Code or Codex, inside the dev container):
- "I'm on step N of guide-a. Explain the idea with a different example, don't give me the code."
- "Here's my error: … What does it mean, and where should I look?"
- "Review my change for step N against the guide. Point to problems, don't fix them."

**Metrics to watch over the weeks** (from `scripts/pace_report.py` and the timer): the pace factor going down toward about 1.2, the median minutes between commits going down, fewer friction signals, and fewer hints opened per challenge.

## When you're stuck
- Open hints one at a time.
- Ask Claude or Codex to explain a step without giving the code ("explain step 4, don't give me the code"). `AGENTS.md` tells them to coach, not solve.
- It's fine for a day to take two sessions. Unfinished work carries over to the next day.
