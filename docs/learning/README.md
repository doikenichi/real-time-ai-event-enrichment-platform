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

## When you're stuck
- Open hints one at a time.
- Ask Claude or Codex to explain a step without giving the code ("explain step 4, don't give me the code"). `AGENTS.md` tells them to coach, not solve.
- It's fine for a day to take two sessions. Unfinished work carries over to the next day.
