# Roadmap

Every weekday has **3 challenges** (A, B, C), each taking 10–20 minutes, at most 60 minutes in total. The tracks rotate so that every area moves forward every day:

- **A — Backend:** Python and async services, Kafka, AWS SDK, agents
- **B — Full stack:** TypeScript gateway and the Next.js dashboard, end to end
- **C — Cloud, DevOps and AI agents:** infrastructure, CI/CD, observability, coding agents, agent testing

Every challenge follows **spec → test → code → docs**: an OpenSpec change with Given/When/Then scenarios, TDD (red → green → refactor), then updated UML/C4 diagrams, contracts and ADRs. The shared skills from [spec-driven-tdd-agent-skills](https://github.com/doikenichi/spec-driven-tdd-agent-skills) guide each step. Each challenge links to a book chapter from [docs/READING.md](docs/READING.md) (skill `reading-companion`). Security is secure-by-default from day 1 (skill `security-hardening`). Distributed-systems testing is a core thread (skill `distributed-event-testing`): every event-flow milestone includes its failure-mode tests. Non-functional quality (performance, resilience, accessibility) is tested from Phase 1 onward (skill `performance-and-nfr-testing`). Phases are guides, not deadlines. The mentor moves to the next milestone only once the current one is done.

## Phase 0 — Foundations (about 2 weeks)
- [ ] Repo security baseline: a ruleset on `main` (PRs only, no force pushes or deletion, conversation resolution), linear history with rebase merges (keeps TDD commits), no merge commits, delete branches after merge, disable unused features
- [ ] `SECURITY.md` and private vulnerability reporting; review the secret scanning and push protection settings (with custom patterns)
- [ ] `CODEOWNERS`, a PR template with a security checklist, issue templates (bug, feature, security hardening)
- [ ] Spec-driven setup: `openspec init` (configured for Claude Code and Codex), first capability spec `event-ingest`
- [ ] Contracts skeleton: `docs/contracts/openapi.yaml`, `asyncapi.yaml`, and the first JSON Schema
- [ ] Monorepo tooling: uv workspace (Python), pnpm workspace (TypeScript), `.editorconfig`, Makefile or justfile tasks
- [ ] `ingest-api`: async FastAPI app, `/healthz` and `/readyz`, `POST /events` with Pydantic v2 models, unit tests
- [ ] Event schema v1 (`EventIn`, `EnrichedEvent`) shared through JSON Schema
- [ ] `web/dashboard`: Next.js app with strict TypeScript and a first component test (vitest + Testing Library)
- [ ] Shift left: pre-commit with ruff, mypy, eslint, tsc, gitleaks, hadolint
- [ ] Docker: multi-stage, non-root images for `ingest-api`, health checks
- [ ] CircleCI: first pipeline (lint → unit tests), caching, test results
- [ ] ADR-0005: monorepo layout and tooling
- [ ] Threat model v0: STRIDE for the ingest flow, plus a data-flow diagram in arc42 §11

## Phase 1 — Event backbone (about 2 weeks)
- [ ] `infra/compose.yaml`: Kafka 4.x (KRaft) and Schema Registry
- [ ] Kafka fundamentals lab: topics, partitions, keys and ordering, replication and `min.insync.replicas`; inspect them with the CLI tools and an admin client in tests
- [ ] Async Kafka producer in `ingest-api`: idempotent producer (`enable.idempotence`, `acks=all`), keys, headers, graceful shutdown; a test that a broker restart loses and duplicates nothing
- [ ] Consumer skeleton in `enricher`: consumer groups, manual commits, retries, dead-letter topic
- [ ] Event flow model: sequence diagram, entity state machine and invariants, delivery guarantee per hop (AsyncAPI and arc42)
- [ ] Idempotent consumer: idempotency key or conditional upsert; tests that replay duplicates and crash before commit
- [ ] Out-of-order and late events for the same key: version or sequence checks (no last-writer-wins); partition-key ordering tests
- [ ] Poison events: DLQ with the reason in headers, without blocking the partition; redrive tool and test
- [ ] Retries: exponential backoff with jitter and capped attempts; a test proving retries plus idempotency give no duplicate effects
- [ ] Eventual-consistency test helper: poll until the state matches, with an SLO timeout and the last observed state on failure (no sleeps)
- [ ] PostgreSQL 18 in compose: `ingest-api` persists accepted events and idempotency keys (unique constraint, `INSERT … ON CONFLICT`), with SQLAlchemy 2.x async and Alembic migrations; Testcontainers Postgres tests
- [ ] Transactional outbox: the event row and outbox row are written in one transaction; Debezium (Kafka Connect) Outbox Event Router publishes to Kafka, keyed by aggregate id. Tests: an outbox row becomes exactly one Kafka message; a rollback publishes nothing; a connector restart creates no lost or out-of-order keys
- [ ] Outbox pattern and idempotent processing (consumers dedupe by event id)
- [ ] Integration tests with Testcontainers (Kafka); contract tests for event schemas (including Pact message pacts)
- [ ] Consumer crash and rebalance test: kill a consumer mid-batch; no loss and no duplicate effects; compare rebalances under the Kafka 4.x consumer group protocol (KIP-848)
- [ ] Offsets and replay: reset a consumer group to a timestamp and rebuild state with idempotent projections; test that a replay converges
- [ ] Schema evolution: Schema Registry compatibility modes, and a CI check that rejects breaking changes
- [ ] `gateway` (TypeScript): Kafka consumer → Server-Sent Events, backpressure, AbortController
- [ ] Dashboard: live event list over SSE, with reconnects
- [ ] CircleCI: integration job on the `machine` executor
- [ ] Dependency security: Dependabot alerts and security updates; `dependabot.yml` for uv, npm/pnpm, docker and github-actions; license allow-list check
- [ ] SAST: CodeQL (security-extended) for Python and TypeScript; Semgrep in CircleCI with a severity gate; ruff `S` rules and eslint security rules
- [ ] The ruleset requires the CI checks to pass before merge
- [ ] First NFR: a quality scenario with numbers for `POST /events` (spec and arc42 §10), and a k6 smoke test (TypeScript, thresholds) in `tests/perf/` run on every PR
- [ ] Kafka throughput baseline: produce/consume perf tools, end-to-end latency and consumer lag
- [ ] API security: input validation tests with malicious payloads, rate limiting, CORS allow-list, security headers (OWASP API Top 10)

## Phase 2 — AWS, locally (about 2 weeks)
- [ ] AWS Emulator (Dockerfile, CA cert, generated credentials) and Floci in compose
- [ ] S3 archive of raw events (async SDK, multipart, presigned URLs)
- [ ] DynamoDB store for enriched events (single-table design, conditional writes)
- [ ] `EnrichedEventStore` port with two adapters, DynamoDB and MongoDB, both passing one shared contract test suite (access-pattern-first design: key-value vs document)
- [ ] MongoDB for ops-agent incident documents: schema validation (`$jsonSchema`), indexes, and data validation and integrity tests
- [ ] Migrations done safely: expand/contract (backward-compatible) migrations, tested upgrade and downgrade in CI, and zero-downtime rules in an ADR
- [ ] Database security: least-privilege roles per service, Postgres row-level security per tenant, SQL injection tests, and the Debezium user limited to replication
- [ ] SQS as the dead-letter queue and redrive
- [ ] Moto for unit tests; emulators for integration tests
- [ ] Terraform against Floci: modules, remote state pattern, `terraform test`
- [ ] IaC scanning with Checkov and Trivy config; least-privilege IAM policies for each service
- [ ] Ports and adapters: storage interfaces with AWS and in-memory adapters
- [ ] Downstream validation: assert the DynamoDB and S3 state and the downstream topics, not just API responses
- [ ] Reconciliation job: counts and checksums across Postgres (ingested), Kafka and DynamoDB/MongoDB (enriched) per window; as a test and as a scheduled check
- [ ] Exactly-once inside Kafka: transactional read-process-write with `read_committed` consumers; a test that aborted transactions are never visible, and why external side effects still need idempotency
- [ ] Compacted topic for latest-state-per-key (for example enrichment rules), with tombstones and a rebuild test
- [ ] Same failure modes on SQS (through the emulators): visibility timeout, redrive policy, FIFO deduplication, to show the concepts transfer across brokers
- [ ] Streams as the source of truth (DDIA ch. 12–13): rebuild a derived view from the Kafka log, with a replay test
- [ ] Saga across services, with compensation for partial failures, and tests for each failure step

## Phase 3 — The enricher agent (about 3 weeks)
- [ ] `LLMProvider` port and adapters: `RecordedProvider`, `ClaudeAgentSdkProvider`, `CodexProvider` (`OllamaProvider` comes later)
- [ ] Structured output validated with Pydantic
- [ ] Retrieval for the agent: pgvector embeddings of enrichment reference data in Postgres; tests for recall on a small labelled set (AIE ch. 6)
- [ ] Valkey for LLM rate limiting (token bucket) and request deduplication; tests for limits under concurrency
- [ ] Tool calling: lookup tools for DynamoDB, S3 and HTTP; tool errors and timeouts
- [ ] An MCP server exposing platform tools, with its own contract tests
- [ ] Agent testing pyramid: tool unit tests → scripted LLM → record/replay → trajectories → evals → red-team → budgets
- [ ] LLM path load test with Locust: concurrency limits, rate-limit handling and backoff, token and cost budget under load (recorded provider plus a short live run)
- [ ] Baseline before LLM (DMLS ch. 6): a cheap classical classifier (scikit-learn) for event category; compare cost and quality with the LLM, then a cascade that tries cheap first and escalates
- [ ] Eval suite (promptfoo or DeepEval) with a baseline gate in CircleCI
- [ ] Langfuse (self-hosted) traces, datasets and scores
- [ ] Prompt-injection guardrails for event payloads
- [ ] OWASP Top 10 for LLM applications: tool allow-lists, output handling, spend limits, no secrets in prompts or logs; red-team suite in CI

## Phase 4 — Observability (about 2 weeks)
- [ ] Structured logging: structlog (Python), pino (TypeScript), correlation IDs
- [ ] OpenTelemetry traces across HTTP → Kafka headers → agent → SSE
- [ ] `grafana/otel-lgtm` in compose: Prometheus, Loki and Tempo
- [ ] RED metrics, consumer lag, and LLM metrics (latency, tokens, cost, fallbacks)
- [ ] Dashboards and alert rules as code, SLOs, runbooks in `docs/runbooks/`
- [ ] Telemetry tests with in-memory exporters
- [ ] Trace-based e2e tests: assert the span path HTTP → Kafka → agent → store → SSE for one correlation id
- [ ] Kafka share groups (Queues for Kafka, production-ready in 4.2) for parallel enrichment work: acknowledgement, redelivery and delivery-count tests
- [ ] Distributed-bug metrics and alerts: lag, DLQ rate, retries, duplicates detected, reconciliation mismatches; a runbook for following one id across logs and traces
- [ ] Load testing with observability: average-load and spike tests (open arrival-rate model), k6 metrics streamed to Prometheus, a Grafana dashboard next to the RED metrics and traces
- [ ] Database performance: connection pooling, `EXPLAIN ANALYZE` checks on key queries in CI, and k6 scenarios that include the database; Postgres and Valkey metrics in Grafana
- [ ] Profiling: Pyroscope continuous profiling, plus py-spy and the Node.js CPU profiler; fix one hotspot found under load (with a test-first regression check)
- [ ] Drift monitoring (DMLS ch. 8): alert on shifts in the input event mix and in the enrichment output distribution
- [ ] Soak test: detect memory, connection and consumer-lag drift; a runbook for what to watch

## Phase 5 — Test environments at scale (about 2 weeks)
- [ ] Playwright e2e against the full compose stack
- [ ] Disposable environment for each CircleCI pipeline: bring the stack up → test → tear it down
- [ ] kind cluster, Kubernetes manifests, then Helm charts
- [ ] Image scanning with Trivy, SBOMs, and test splitting in CircleCI
- [ ] Performance gate in CircleCI: load and spike tests in the disposable environment, compared with a stored baseline; a regression fails the build
- [ ] Stress and breakpoint tests on kind, horizontal pod autoscaling (HPA), and a capacity-planning ADR (where it saturates and why)
- [ ] Fault-injecting test harness: a producer and proxy that duplicate, delay, drop and reorder events on demand, used by the e2e suite
- [ ] Resilience: Toxiproxy faults between services (latency, timeouts, resets), plus Chaos Mesh pod and network chaos on kind; verify retries, circuit breakers and the DLQ hold their SLOs
- [ ] Supply chain: SBOMs (CycloneDX) for every image, keyless cosign signing and attestation, actions and orbs pinned by SHA, OpenSSF Scorecard with a badge
- [ ] Kubernetes security: Pod Security Standards (restricted), securityContext, NetworkPolicies, resource limits; Checkov for manifests and Helm

## Phase 6 — The ops-agent, an AI SRE (about 2 weeks)
- [ ] Grafana alert webhook → `ops-agent`
- [ ] Investigating through the Grafana MCP server (Prometheus, Loki, Tempo)
- [ ] Incident reports linked to runbooks
- [ ] Multiple agents: a coordinator plus specialists for metrics, logs and traces
- [ ] Chaos drills used as evals: inject a fault and score the root cause the agent finds

## Phase 7 — Real deployment (about 3 weeks)
- [ ] Vercel Hobby: dashboard, with a preview deployment for each PR
- [ ] Aiven free Kafka (TLS/SASL config, environment-based settings)
- [ ] Managed databases on free tiers: Neon (Postgres, with a branch per PR as a disposable test database) and MongoDB Atlas Free; the adapter is chosen by configuration; Valkey self-hosted on Oracle
- [ ] Render or Koyeb: `ingest-api` and `gateway`; ADR on free tiers going to sleep
- [ ] Oracle Cloud Always Free: Ollama and the enricher (with demo mode as the fallback)
- [ ] Continuous deployment from CircleCI: approval jobs, smoke tests, rollbacks
- [ ] Test in production (DMLS ch. 9): shadow and canary releases for prompt or model versions, gated by evals
- [ ] Inference benchmarks (IE, AIE ch. 9): time to first token, time per output token, throughput and cost across Ollama quantization levels, under load
- [ ] Semantic and prompt caching (AIE ch. 9): hit rate and latency savings, measured
- [ ] User feedback loop (AIE ch. 10): thumbs up or down on the dashboard feeds the eval dataset
- [ ] Playwright against preview URLs; production monitoring and uptime checks
- [ ] Web performance and accessibility: Lighthouse CI budgets (LCP, INP, CLS) and axe-core WCAG 2.2 AA checks on Vercel preview deployments
- [ ] Production synthetic checks: k6 smoke tests only, within free-tier fair use (no load or stress against hosted tiers)
- [ ] DAST: OWASP ZAP baseline scan against preview and production URLs in CircleCI
- [ ] Secrets in each platform's secret store, rotation runbook, least-privilege deploy tokens

## Phase 8 — Agents everywhere, and polish (about 2 weeks)
- [ ] Test-generation agent (you review its output), and exploratory e2e through Playwright MCP
- [ ] CircleCI build-failure explainer agent and a PR review agent
- [ ] AI for performance: the k6 MCP server and `k6 x agent` skills in Claude Code and Codex for writing and validating scripts; a `perf-analyst` agent that compares runs with the baseline, investigates through the Grafana MCP server (metrics, traces, profiles) and posts a regression report on the PR, tested with recorded results that contain known regressions
- [ ] Coding-agent workflows: AGENTS.md and shared skills, delegating, reviewing diffs (Claude Code, Codex, Copilot)
- [ ] Local Ollama optimization (nice to have): model comparison on the eval suite
- [ ] Security review: an OWASP ASVS level 1 self-assessment, threat model refresh, Scorecard ≥ 7
- [ ] ML/AI system design drills (MLSDI): run the framework on this platform and on 3 of the book's case studies
- [ ] Interview readiness: every answer in `docs/interview/` backed by platform evidence; a mock interview on distributed testing, run by the mentor
- [ ] Portfolio README, architecture diagram, demo script, and job-interview talking points
