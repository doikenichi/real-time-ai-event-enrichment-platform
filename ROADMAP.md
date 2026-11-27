# Roadmap

Every weekday has **3 challenges** (A, B, C), each taking 10–20 minutes, at most 60 minutes in total. The tracks rotate so that every area moves forward every day:

- **A — Backend:** Python and async services, Kafka, AWS SDK, agents
- **B — Full stack:** TypeScript gateway and the Next.js dashboard, end to end
- **C — Cloud, DevOps and AI agents:** infrastructure, CI/CD, observability, coding agents, agent testing

Testing is part of every challenge. Most challenges come with a failing test, or ask you to write the test first. Phases are guides, not deadlines. The mentor moves to the next milestone only once the current one is done.

## Phase 0 — Foundations (about 2 weeks)
- [ ] Monorepo tooling: uv workspace (Python), pnpm workspace (TypeScript), `.editorconfig`, Makefile or justfile tasks
- [ ] `ingest-api`: async FastAPI app, `/healthz` and `/readyz`, `POST /events` with Pydantic v2 models, unit tests
- [ ] Event schema v1 (`EventIn`, `EnrichedEvent`) shared through JSON Schema
- [ ] `web/dashboard`: Next.js app with strict TypeScript and a first component test (vitest + Testing Library)
- [ ] Shift left: pre-commit with ruff, mypy, eslint, tsc, gitleaks, hadolint
- [ ] Docker: multi-stage, non-root images for `ingest-api`, health checks
- [ ] CircleCI: first pipeline (lint → unit tests), caching, test results
- [ ] ADR-0003: monorepo layout and tooling

## Phase 1 — Event backbone (about 2 weeks)
- [ ] `infra/compose.yaml`: Kafka (KRaft) and Schema Registry
- [ ] Async Kafka producer in `ingest-api`: idempotent producer, keys, headers, graceful shutdown
- [ ] Consumer skeleton in `enricher`: consumer groups, manual commits, retries, dead-letter topic
- [ ] Outbox pattern and idempotent processing
- [ ] Integration tests with Testcontainers (Kafka); contract tests for event schemas
- [ ] `gateway` (TypeScript): Kafka consumer → Server-Sent Events, backpressure, AbortController
- [ ] Dashboard: live event list over SSE, with reconnects
- [ ] CircleCI: integration job on the `machine` executor

## Phase 2 — AWS, locally (about 2 weeks)
- [ ] AWS Emulator (Dockerfile, CA cert, generated credentials) and Floci in compose
- [ ] S3 archive of raw events (async SDK, multipart, presigned URLs)
- [ ] DynamoDB store for enriched events (single-table design, conditional writes)
- [ ] SQS as the dead-letter queue and redrive
- [ ] Moto for unit tests; emulators for integration tests
- [ ] Terraform against Floci: modules, remote state pattern, `terraform test`
- [ ] Ports and adapters: storage interfaces with AWS and in-memory adapters

## Phase 3 — The enricher agent (about 3 weeks)
- [ ] `LLMProvider` port and adapters: `RecordedProvider`, `ClaudeAgentSdkProvider`, `CodexProvider` (`OllamaProvider` comes later)
- [ ] Structured output validated with Pydantic
- [ ] Tool calling: lookup tools for DynamoDB, S3 and HTTP; tool errors and timeouts
- [ ] An MCP server exposing platform tools, with its own contract tests
- [ ] Agent testing pyramid: tool unit tests → scripted LLM → record/replay → trajectories → evals → red-team → budgets
- [ ] Eval suite (promptfoo or DeepEval) with a baseline gate in CircleCI
- [ ] Langfuse (self-hosted) traces, datasets and scores
- [ ] Prompt-injection guardrails for event payloads

## Phase 4 — Observability (about 2 weeks)
- [ ] Structured logging: structlog (Python), pino (TypeScript), correlation IDs
- [ ] OpenTelemetry traces across HTTP → Kafka headers → agent → SSE
- [ ] `grafana/otel-lgtm` in compose: Prometheus, Loki and Tempo
- [ ] RED metrics, consumer lag, and LLM metrics (latency, tokens, cost, fallbacks)
- [ ] Dashboards and alert rules as code, SLOs, runbooks in `docs/runbooks/`
- [ ] Telemetry tests with in-memory exporters

## Phase 5 — Test environments at scale (about 2 weeks)
- [ ] Playwright e2e against the full compose stack
- [ ] Disposable environment for each CircleCI pipeline: bring the stack up → test → tear it down
- [ ] kind cluster, Kubernetes manifests, then Helm charts
- [ ] Image scanning with Trivy, SBOMs, and test splitting in CircleCI

## Phase 6 — The ops-agent, an AI SRE (about 2 weeks)
- [ ] Grafana alert webhook → `ops-agent`
- [ ] Investigating through the Grafana MCP server (Prometheus, Loki, Tempo)
- [ ] Incident reports linked to runbooks
- [ ] Multiple agents: a coordinator plus specialists for metrics, logs and traces
- [ ] Chaos drills used as evals: inject a fault and score the root cause the agent finds

## Phase 7 — Real deployment (about 3 weeks)
- [ ] Vercel Hobby: dashboard, with a preview deployment for each PR
- [ ] Aiven free Kafka (TLS/SASL config, environment-based settings)
- [ ] Render or Koyeb: `ingest-api` and `gateway`; ADR on free tiers going to sleep
- [ ] Oracle Cloud Always Free: Ollama and the enricher (with demo mode as the fallback)
- [ ] Continuous deployment from CircleCI: approval jobs, smoke tests, rollbacks
- [ ] Playwright against preview URLs; production monitoring and uptime checks

## Phase 8 — Agents everywhere, and polish (about 2 weeks)
- [ ] Test-generation agent (you review its output), and exploratory e2e through Playwright MCP
- [ ] CircleCI build-failure explainer agent and a PR review agent
- [ ] Coding-agent workflows: CLAUDE.md, delegating, reviewing diffs (Claude Code, Codex, Copilot)
- [ ] Local Ollama optimization (nice to have): model comparison on the eval suite
- [ ] Portfolio README, architecture diagram, demo script, and job-interview talking points
