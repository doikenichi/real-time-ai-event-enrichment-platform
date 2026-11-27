# CLAUDE.md

This repository is a **progressive lab**. A real product, the real-time AI event enrichment platform, is built through daily coding challenges. Read `docs/GOALS.md`, `ROADMAP.md` and `.lab/state.json` before doing anything.

## For coding agents helping the learner
- The learner writes the core code. Explain, hint, review and pair with them, but don't solve a challenge unless explicitly asked to.
- Follow the conventions below. Use current stable APIs only; check versions before adding a dependency.

## Conventions
- **Python 3.13:** uv workspace; ruff (lint and format); mypy `--strict`; pytest with pytest-asyncio; Pydantic v2; async-first (asyncio, `TaskGroup`, timeouts with `asyncio.timeout`). No blocking I/O on the event loop.
- **TypeScript:** pnpm workspace; `strict: true`; ESM; eslint; vitest; zod at boundaries; async/await with `AbortSignal` for cancellation.
- **Architecture:** ports and adapters. Domain code never imports SDKs directly. Adapters for Kafka, AWS, LLMs and MCP live behind interfaces, with in-memory or fake adapters for tests.
- **LLM providers:** `RecordedProvider` (tests, CI, demo), `ClaudeAgentSdkProvider` and `CodexProvider` (local development with the learner's subscription login, personal use only), `OllamaProvider` (deployment). Never call the Anthropic API with subscription OAuth tokens, and never deploy subscription credentials. They are selected through `LLM_PROVIDER`.
- **Testing:** unit → contract → integration (Testcontainers, AWS Emulator, Floci) → e2e (Playwright). Agent tests: scripted LLM, record/replay, trajectories, evals with thresholds, red-team tests, budgets. Telemetry is tested with in-memory exporters.
- **Observability:** structured JSON logs, OpenTelemetry traces with context carried in Kafka headers, RED metrics, and GenAI semantic conventions for agent spans.
- **Security:** no secrets in git (gitleaks runs in pre-commit); `.env` is git-ignored and `.env.example` is committed.
- **Commits:** `day-NNN: <summary>` for learner work, `lab(day-NNN): <summary>` for mentor commits.
- **Decisions:** record significant decisions as ADRs in `docs/adr/` (template: `docs/adr/0000-template.md`).
- **Cost:** everything must be free for the learner to use. Prefer open source when it is the industry standard.

## Daily mentor protocol
This protocol is followed by the scheduled mentor run each weekday.

1. **Sync.** Fetch `main`. Read `.lab/state.json`, `ROADMAP.md`, `docs/GOALS.md` and the previous day's `challenges/day-NNN/README.md`. List the learner's commits since `last_reviewed_commit`. If an open `lab/day-*` PR has not been merged and there are no new learner commits, do not create a new day. Post a short reminder comment on that PR, then stop.
2. **Review the previous day.** For each challenge (A, B, C), decide whether it is *done*, *partial* or *not started*, based on the diff and on running the tests where possible. Write `challenges/day-<prev>/REVIEW.md` containing:
   - what went well, with specific references to files and lines
   - issues: correctness, async pitfalls, patterns, tests, security
   - a **reference solution** for anything partial or not started, plus an idiomatic alternative for done work where it teaches something
   - one "industry insight": how this is done in production, or how it would come up in a consulting or client conversation
3. **Plan today.** Choose the next 3 challenges. Unfinished work carries over first, folded into today's 3; never stack more than 3. Take the next unchecked milestones from the current phase, one each for track A (backend), B (full stack) and C (cloud, DevOps and AI agents). Each challenge must build on code that is already in the repo, take 10–20 minutes, and keep the total at or under 60 minutes.
4. **Verify currency.** Web-search the current stable versions and recommended APIs for every library or tool used today. Note the versions in the challenge.
5. **Write the challenge.** Create `challenges/day-NNN/README.md` in the format from `challenges/README.md`. Add failing tests or stubs where they help, so that "done when" is an automated check. Testing is part of every challenge. Never include solutions.
6. **Update state.** Update `.lab/state.json`: `current_day`, `next_day`, `phase`, `milestone`, `last_reviewed_commit`, and per-day status, `carry_over` and `skills_to_reinforce`. Tick finished milestones in `ROADMAP.md`. Move to the next phase only when the current phase's milestones are done.
7. **Deliver.** Commit on branch `lab/day-NNN`, push it, and open a PR titled `Day NNN — <theme>`. The PR body holds a summary of the review, today's 3 challenges with their time estimates, and any setup needed (accounts, tools). If a challenge needs a new account (CircleCI, Vercel, Aiven and so on), say so at the top.
