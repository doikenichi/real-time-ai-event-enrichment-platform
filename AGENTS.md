# AGENTS.md

These instructions are shared by Claude Code (through `CLAUDE.md` → `@AGENTS.md`), Codex and other agents.

This repository is a **progressive lab**. A real product, the real-time AI event enrichment platform, is built through daily coding challenges. Read `docs/GOALS.md`, `ROADMAP.md` and `.lab/state.json` before doing anything.

## Workflow: spec → test → code → docs
Every change, by the learner or an agent, follows this order. Each step has a shared skill (installed in `.claude/skills/` and `.agents/skills/` from [spec-driven-tdd-agent-skills](https://github.com/doikenichi/spec-driven-tdd-agent-skills)):

1. **Spec:** an OpenSpec change in `openspec/changes/<id>/` with Given/When/Then scenarios → skill `spec-driven-change`
2. **Test (red):** failing tests named after the scenarios → skill `tdd-red-green-refactor`
3. **Code (green → refactor):** the simplest passing code, then refactor with the tests green
4. **Docs:** update the UML/C4 diagrams, OpenAPI/AsyncAPI contracts, arc42 sections and ADRs in the same change → skills `uml-and-c4-diagrams`, `api-and-event-contracts`, `architecture-docs`

Agent work also uses `agent-testing`, telemetry work uses `observability-instrumentation`, every change is checked against `security-hardening`, NFR work (performance, resilience, accessibility) uses `performance-and-nfr-testing`, event flows across services use `distributed-event-testing`, and reviews use `code-review-mentor`.

## For coding agents helping the learner
- The learner writes the core code. Explain, hint, review and pair with them, but don't solve a challenge unless explicitly asked to. In TDD, offer the next failing test or a hint rather than the green step.
- Use current stable APIs only; check versions before adding a dependency.

## Conventions
- **Python 3.13:** uv workspace; ruff (lint and format); mypy `--strict`; pytest with pytest-asyncio; Pydantic v2; async-first (asyncio, `TaskGroup`, timeouts with `asyncio.timeout`). No blocking I/O on the event loop.
- **TypeScript:** pnpm workspace; `strict: true`; ESM; eslint; vitest; zod at boundaries; async/await with `AbortSignal` for cancellation.
- **Architecture:** ports and adapters. Domain code never imports SDKs directly. Adapters for Kafka, AWS, LLMs and MCP live behind interfaces, with in-memory or fake adapters for tests.
- **LLM providers:** `RecordedProvider` (tests, CI, demo), `ClaudeAgentSdkProvider` and `CodexProvider` (local development with the learner's subscription login, personal use only), `OllamaProvider` (deployment). Never call the Anthropic API with subscription OAuth tokens, and never deploy subscription credentials. They are selected through `LLM_PROVIDER`.
- **Testing:** unit → contract → integration (Testcontainers, AWS Emulator, Floci) → e2e (Playwright). Agent tests: scripted LLM, record/replay, trajectories, evals with thresholds, red-team tests, budgets. Telemetry is tested with in-memory exporters.
- **Distributed testing:** every producer or consumer change includes failure-mode tests (duplicate, delayed, missing, out-of-order and poison events, retries, rebalance). Eventual consistency is asserted by polling with SLO timeouts, never sleeps. Validate downstream state, and propagate correlation ids and trace context through Kafka headers.
- **Non-functional testing:** NFRs are spec scenarios with numbers. k6 scripts in `tests/perf/` with thresholds and baselines; Locust for LLM paths; Toxiproxy and Chaos Mesh for resilience; Lighthouse CI and axe-core for the web. Heavy load runs only against local or disposable environments, never against free-tier hosts.
- **Observability:** structured JSON logs, OpenTelemetry traces with context carried in Kafka headers, RED metrics, and GenAI semantic conventions for agent spans.
- **Documentation:** arc42 in `docs/architecture/`; UML and C4 diagrams as Mermaid; contracts in `docs/contracts/` (OpenAPI 3.1, AsyncAPI 3); ADRs (MADR) in `docs/adr/`; runbooks in `docs/runbooks/`; living specs in `openspec/specs/`.
- **Security:** secure by default (skill `security-hardening`): no secrets in git (gitleaks runs in pre-commit, push protection is on); `.env` is git-ignored and `.env.example` is committed; validate every input; pin dependencies; keep the scans green (CodeQL, Semgrep, Trivy, Checkov); follow the OWASP Top 10 for web, API and LLM applications.
- **Commits:** `day-NNN: <summary>` for learner work, `lab(day-NNN): <summary>` for mentor commits. Commit at each green TDD step.
- **Skills:** never edit `.claude/skills/` or `.agents/skills/` directly. Change them in the skills repo, then re-run the update command in `.lab/skills.json`.
- **Cost:** everything must be free for the learner to use. Prefer open source when it is the industry standard.

## Daily mentor protocol
This protocol is followed by the scheduled mentor run each weekday.

1. **Sync.** Fetch `main`. Read `.lab/state.json`, `ROADMAP.md`, `docs/GOALS.md` and the previous day's `challenges/day-NNN/README.md`. List the learner's commits since `last_reviewed_commit`. If an open `lab/day-*` PR has not been merged and there are no new learner commits, do not create a new day. Post a short reminder comment on that PR, then stop.
2. **Review the previous day** using the `code-review-mentor` skill. For each challenge (A, B, C), decide whether it is *done*, *partial* or *not started*, based on the diff and on running the tests where possible. Check the spec scenarios are covered by tests, look for evidence of TDD, and check docs and diagrams were updated. Write `challenges/day-<prev>/REVIEW.md` containing:
   - what went well, with specific references to files and lines
   - issues: correctness, async pitfalls, patterns, tests, docs, security (the `security-hardening` checklist)
   - a **reference solution** for anything partial or not started, plus an idiomatic alternative for done work where it teaches something
   - one "industry insight": how this is done in production, or how it would come up in a consulting or client conversation
3. **Plan today.** Choose the next 3 challenges. Unfinished work carries over first, folded into today's 3; never stack more than 3. Take the next unchecked milestones from the current phase, one each for track A (backend), B (full stack) and C (cloud, DevOps and AI agents). Each challenge must build on code that is already in the repo, take 10–20 minutes, and keep the total at or under 60 minutes.
4. **Goals check, then deep research.** Keep `docs/GOALS.md` in mind for every decision; each challenge must serve at least one goal and move toward the target job. Before writing anything, research each planned challenge in depth:
   - Use several web searches per challenge (extended mode where available), and read the primary sources: official docs and changelogs, standards bodies (OWASP, NIST, CNCF, OpenSSF, IETF and W3C, OpenTelemetry), the Thoughtworks Technology Radar, engineering blogs from leading companies, and current job postings, including the Foci role.
   - Confirm the current stable versions and recommended APIs, and check for deprecations and newer alternatives that have become the standard.
   - Compare at least two approaches, and pick the one industry uses today; record trade-offs in an ADR when it's significant.
   - If research shows the roadmap is outdated or missing an industry practice, update `ROADMAP.md` in the same PR and explain why in the PR body.
   - Record the sources in the challenge's "Industry standard" section.
5. **Write the challenge.** Create `challenges/day-NNN/README.md` in the format from `challenges/README.md`. For each challenge, draft the **OpenSpec change** (`openspec/changes/<id>/` with proposal, spec delta with scenarios, and tasks) using `spec-driven-change`, leaving the learner a small refinement to make. Add failing test stubs named after the scenarios where they help, so that "done when" is an automated check. Name the doc or diagram to update. Never include solutions.
6. **Update state.** Update `.lab/state.json`: `current_day`, `next_day`, `phase`, `milestone`, `last_reviewed_commit`, and per-day status, `carry_over` and `skills_to_reinforce`. Tick finished milestones in `ROADMAP.md`. Move to the next phase only when the current phase's milestones are done. If the skills repo `main` has moved past the commit in `.lab/skills.json`, re-sync the skills (copy them into both folders and update the commit).
7. **Interview drill.** Add one interview question tied to today's work (prefer distributed-systems testing, security, performance and AI agents) to the challenge README as an optional 5-minute drill outside the 60 minutes. Append it to the question bank in `docs/interview/README.md`, and fill in the "Evidence from this platform" table when a challenge implements a technique. In `REVIEW.md`, give feedback on any answer the learner wrote.
8. **Deliver.** Commit on branch `lab/day-NNN`, push it, and open a PR titled `Day NNN — <theme>`. The PR body holds a summary of the review, today's 3 challenges with their time estimates, and any setup needed (accounts, tools). If a challenge needs a new account (CircleCI, Vercel, Aiven and so on), say so at the top.
