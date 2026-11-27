# Day 001 — Foundations: health probes, first component, protected main

Phase 0 · Foundations · total time ≈ 55 min

The first day lays three foundations at once: a test-first Python service, a test-first React component, and a protected repository. Each challenge follows **spec → test → code → docs**.

## Setup (≈5 min, once)
Prerequisites: the dev container (`.devcontainer/`, see `docs/how-to/develop-on-any-machine.md`), which provides Python 3.15 with [uv](https://docs.astral.sh/uv/), Node.js 26 LTS with nvm and pnpm, and the GitHub CLI (`gh auth login`). Without it: Python 3.15, uv, Node.js 26 LTS and pnpm on your host.

```bash
git switch -c work/day-001                     # from today on, work happens on a branch (see Challenge C)
npm install -g @fission-ai/openspec@latest     # OpenSpec 1.14+
openspec init --tools "claude,codex"           # creates openspec/ plus the agent integrations
mkdir -p openspec/changes
cp -r challenges/day-001/starter/openspec/changes/* openspec/changes/
openspec list                                  # shows the 3 drafted changes for today
```

Each challenge has a starter test. Copy it into place **after** scaffolding (A and B below), because `create-next-app` refuses non-empty folders.

---

## A — Backend: health probes for `ingest-api` (≈20 min)

1. **Goal:** a uv workspace with its first service, `ingest-api`, exposing liveness and readiness probes, built test-first.
2. **Serves:** goals 1 (async Python, patterns), 3 (spec-driven, TDD), 4 (testing). Job: production-grade services, containers and Kubernetes.
3. **Context:** the first code in the repo. Every later service reuses this probe pattern, and the Phase 5 Kubernetes deployment wires these endpoints into its probes.
4. **Industry standard:** separate `/livez` and `/readyz`. Kubernetes itself deprecated the combined `/healthz` endpoint, and the API server uses the more specific `livez` and `readyz` instead. **Liveness must not check dependencies**: if the database is down and liveness fails, every restarted pod fails too. Readiness checks dependencies, and failing it removes the pod from traffic without restarting it.

* [Kubernetes API health endpoints](https://kubernetes.io/docs/reference/using-api/health-checks/)
* [uv workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/)
* [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/) (FastAPI 0.16x; pin the version you install)

**Book reference:** DDIA (2nd ed.), ch. 2, on nonfunctional requirements. Reliability means tolerating faults rather than preventing every one. Separating liveness from readiness is a small fault-tolerance decision: a broken dependency removes the service from traffic instead of causing a restart storm.

**1. Spec (≈3 min):** read `openspec/changes/add-service-health-probes/`. Add the missing scenario: *a readiness check that hangs*. Decide the time budget (for example 1 s), and what the probe answers.

**2. Red (≈4 min):**

```bash
uv init --bare --name platform .                          # workspace root (no package code)
# add to the root pyproject.toml:  [tool.uv.workspace]  members = ["services/*"]
uv init --package --name ingest-api services/ingest-api   # src/ingest_api/
uv add --package ingest-api fastapi
uv add --package ingest-api --dev pytest pytest-asyncio httpx ruff mypy
cp -r challenges/day-001/starter/services/ingest-api/tests services/ingest-api/
uv run --package ingest-api pytest services/ingest-api -q   # RED: ImportError / failures
```

Then write the hung-check test (see the TODO in the test file). Commit: `day-001: failing tests for service health`.

**3. Green → refactor (≈10 min):** implement `ingest_api.app.create_app(readiness_checks)`.

* **App factory and dependency injection:** the checks are injected, not imported. This is the first **port**; real adapters (Kafka, DynamoDB) arrive later and tests keep using fakes.
* Run all checks **concurrently** (`asyncio.TaskGroup` or `asyncio.gather`) under **`asyncio.timeout`**. A hung dependency must never hang the probe.
* On failure, answer `503` with `application/problem+json` (RFC 9457) and no internal details. Probe endpoints need no auth, and do no heavy work.

Commit at each green step. Then make `uv run ruff check`, `uv run ruff format --check` and `uv run mypy --strict services/ingest-api/src` clean.

**4. Docs (≈3 min):** write `docs/adr/0005-monorepo-layout-and-tooling.md` (template: `0000-template.md`): uv workspace plus pnpm workspace, alternatives considered (separate repos, Poetry, Nx or Turborepo), and the consequences.

**Done when:**

```bash
uv run --package ingest-api pytest services/ingest-api -q    # 4 passed
openspec validate add-service-health-probes --strict
```

<details><summary>Hint 1: test client</summary>The tests use <code>httpx.ASGITransport(app=app)</code>, so no server is started. Your factory just has to return a FastAPI app.</details>
<details><summary>Hint 2: concurrency and timeouts</summary>Wrap the concurrent run in <code>async with asyncio.timeout(budget):</code>, and treat <code>TimeoutError</code> as "not ready".</details>
<details><summary>Hint 3: problem details</summary>Return a <code>JSONResponse</code> with <code>media_type="application/problem+json"</code> and the fields <code>type</code>, <code>title</code> and <code>status</code>.</details>

---

## B — Full stack: the dashboard's first component (≈20 min)

**Goal:** a Next.js dashboard in a pnpm workspace, with Vitest and Testing Library, and an accessible `ServiceStatus` component built test-first.
**Serves:** goals 1 (TypeScript), 3 (TDD), 4 (testing), 7 (accessibility). Job: full stack, front end plus back end.
**Context:** this component will show the `/readyz` result from Challenge A, then live events from the gateway in Phase 1.
**Industry standard:** Next.js 16 documents **Vitest with React Testing Library** for unit and component tests, and E2E tests (Playwright) for async Server Components, which Vitest can't render. Testing Library queries by **role and accessible name**, which tests what users and assistive technology experience; status must not rely on colour alone (WCAG 2.2, 1.4.1).

* [Next.js: setting up Vitest](https://nextjs.org/docs/app/guides/testing/vitest)
* [Testing Library: query priority (`ByRole` first)](https://testing-library.com/docs/queries/about/#priority)
* [WCAG 2.2: Use of Color (1.4.1)](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

**Book reference:** AIE, ch. 10, "AI Engineering Architecture and User Feedback". The dashboard is where operators will later give feedback on enrichments. Starting with a clear, accessible status component is the first step of that interface.

**1. Spec (≈3 min):** read `openspec/changes/add-dashboard-service-status/`, and add the scenario for an **"unknown"** state (before the first readiness result arrives).

**2. Red (≈6 min):**

```bash
printf 'packages:\n  - "web/*"\n' > pnpm-workspace.yaml
pnpm create next-app@latest web/dashboard --ts --app --eslint --use-pnpm --no-tailwind --no-src-dir --import-alias "@/*" --yes   # --yes accepts the defaults for any newer prompts
cd web/dashboard
pnpm add -D vitest @vitejs/plugin-react jsdom @testing-library/react @testing-library/dom vite-tsconfig-paths
cp -r ../../challenges/day-001/starter/web/dashboard/__tests__ .
```

Create `vitest.config.mts` as in the Next.js guide (`environment: 'jsdom'`), add `"test": "vitest"` to `package.json`, and run `pnpm test --run`. It's RED: the component doesn't exist yet. Add the test for the "unknown" scenario. Commit.

**3. Green → refactor (≈8 min):** create `components/service-status.tsx`.

* Type the state as a union, `"ready" | "unavailable" | "unknown"`, mapped to labels through a `Record`, so the compiler forces every state to be handled.
* Use `role="status"` with `aria-label={name}`. The state is in text, and colour is extra.
* Render it on `app/page.tsx` for `ingest-api` (with the state hard-coded for now).

**4. Docs (≈3 min):** `web/dashboard/README.md`: how to run, how to test, and what `ServiceStatus` does.

**Done when:**

```bash
cd web/dashboard && pnpm test --run && pnpm exec tsc --noEmit && pnpm lint
openspec validate add-dashboard-service-status --strict
```

<details><summary>Hint: exhaustive states</summary><code>const LABELS: Record&lt;ServiceState, string&gt; = { ready: "Healthy", unavailable: "Unavailable", unknown: "…" }</code>. Adding a new state without a label then becomes a compile error.</details>

---

## C — Cloud, DevOps and security: protect `main` (≈15 min)

**Goal:** the repository security baseline, verified by an automated test.
**Serves:** goals 5 (secure by default), 6 (industry standards), 3 (spec-first). Jobs: QA quality gates, DevOps and security practices.
**Context:** everything after today flows through PRs into a protected `main`. The mentor's daily PRs already do; your own work does too from today.
**Industry standard:** branch protection, a security policy and code review are checks in the **OpenSSF Scorecard**. GitHub **rulesets** are the current way to protect branches (layered, and visible to anyone with read access). Private vulnerability reporting gives researchers a confidential channel. Rebase merges keep a linear history *and* your TDD commits.

* [GitHub: about rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
* [GitHub: private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/configuring-private-vulnerability-reporting-for-a-repository)
* [OpenSSF Scorecard checks](https://github.com/ossf/scorecard/blob/main/docs/checks.md)

**Book reference:** DDIA (2nd ed.), ch. 1, "Trade-Offs in Data Systems Architecture". Process and governance are part of the architecture. Today's trade-off is a little friction (PRs only) in exchange for traceability and safety.

**1. Spec (≈2 min):** read `openspec/changes/add-repository-security-baseline/`, and add a requirement for what every PR must confirm (your PR template's checklist).

**2. Red (≈1 min):** `scripts/check-repo-baseline.sh` reports 10 failing checks. This script is the test, written before the configuration exists.

**3. Green (≈10 min):**

* **Settings → Rules → Rulesets → New branch ruleset** "Protect main": enforcement Active, target the default branch. Rules: restrict deletions, block force pushes, require linear history, require a pull request (0 approvals; resolve conversations).
* **Settings → General → Pull Requests:** untick merge commits, keep rebase merging, tick "Automatically delete head branches".
* **Settings → Security (Advanced Security):** enable private vulnerability reporting.
* On your branch, add `SECURITY.md` (supported versions, how to report privately, expected response time), `.github/CODEOWNERS` (`* @doikenichi`) and `.github/pull_request_template.md` (the checklist from your spec).
* Open a PR from `work/day-001`, and merge it with **Rebase and merge**.

Want to try infrastructure as code? The ruleset can also be created with `gh api repos/{owner}/{repo}/rulesets --method POST --input ruleset.json`. Keep the JSON in the repo as a stretch goal.

**4. Docs:** `SECURITY.md` is the doc. Link it from `README.md`.

**Done when:**

```bash
scripts/check-repo-baseline.sh      # All checks passed.
openspec validate add-repository-security-baseline --strict
```

---

## Stretch (optional)

* A: add a `/readyz` detail mode that lists each check's status only when the request comes from localhost.
* C: store the ruleset as JSON (`.github/rulesets/protect-main.json`), and apply it with `gh api`, as code.

## Reading this week (optional, about 2 × 25 min, outside the 60 min)

See [docs/READING.md](../../docs/READING.md) for the plan. This week covers Phase 0 foundations:

1. **DDIA (2nd ed.), ch. 1, "Trade-Offs in Data Systems Architecture", and ch. 2 (nonfunctional requirements).** Focus: what reliability, scalability and maintainability mean, and why percentiles (p95, p99) matter more than averages. You'll use these in the NFR scenarios soon.
2. **AIE, ch. 1, "Introduction to Building AI Applications with Foundation Models".** Focus: the AI engineering stack, and how AI engineering differs from ML engineering and from full stack engineering.

**Reflection prompt:** which of DDIA's nonfunctional requirements does the readiness probe protect, and what would you measure to prove it? Write 5–10 lines in `docs/reading-notes/ddia.md` once the reading plan PR is merged.

## Interview drill (optional, ≈5 min, outside the 60 min) · QA/SDET angle
>
> **You join a team that has a brand-new microservice with no tests. How do you build its test strategy, and what do you automate first?**

Use today as evidence: spec scenarios before code, the test level chosen per scenario (unit with fakes for readiness logic), probes that gate test environments, and a repo baseline that enforces it all. Write your answer in `docs/interview/README.md` under "Practice answers". It gets reviewed tomorrow.

## Your workflow from today

1. `git switch -c work/day-NNN`
2. Spec → red → green → refactor → docs, committing at every green step (`day-NNN: <behaviour>`)
3. Push, open a PR into `main`, then **Rebase and merge** (it keeps your TDD commits)
4. After merging, archive each change: `openspec archive <change-id>`
