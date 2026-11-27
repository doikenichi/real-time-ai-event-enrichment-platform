# Tasks

## 1. Spec
- [ ] 1.1 Add the "hung readiness check" scenario; `openspec validate add-service-health-probes --strict` passes

## 2. Tests (red)
- [ ] 2.1 The starter tests in `services/ingest-api/tests/test_health.py` run and fail
- [ ] 2.2 Write the test for the hung-check scenario

## 3. Code (green → refactor)
- [ ] 3.1 `create_app(readiness_checks=...)` app factory, with dependency injection of the checks
- [ ] 3.2 `/livez` and `/readyz`; checks run concurrently under `asyncio.timeout`
- [ ] 3.3 The 503 response uses `application/problem+json`
- [ ] 3.4 `uv run ruff check`, `uv run ruff format --check` and `uv run mypy --strict` are clean

## 4. Docs
- [ ] 4.1 ADR-0005: monorepo layout and tooling (uv workspace, pnpm workspace)
