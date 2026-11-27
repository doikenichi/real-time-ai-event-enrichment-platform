# real-time-ai-event-enrichment-platform

An **AI brain for event streams**, built step by step through short daily coding challenges:

- **Smart surveillance brain** (primary): turns a flood of camera detections into a few explained incidents. It deduplicates across cameras, suppresses false alarms, scores severity, summarises the night and answers questions. Privacy by design: no facial recognition, no identity, limited retention.
- **Build insights** (second domain): explains CI failures, detects flaky tests and tracks delivery metrics from GitHub and CircleCI events, dogfooding this repo's own build system.

See [docs/PRODUCT.md](docs/PRODUCT.md) for the product and [ADR-0007](docs/adr/0007-product-domains-and-privacy-by-design.md) for why.

```
 cameras ─MQTT─► bridge ─┐       GitHub / CircleCI ─webhooks─┐
                        ▼                                   ▼
 clients ──► ingest-api (Python, FastAPI, async)
                 │  produce
                 ▼
             Apache Kafka ──► enricher (Python AI agent: tools, MCP, LLM providers)
                 ▲                │  enriched events
                 │                ▼
             schema registry   Kafka ──► gateway (TypeScript, SSE/WebSocket)
                                              │
                                              ▼
                                   web/dashboard (Next.js, live view)

 Data: PostgreSQL (events, outbox → Debezium → Kafka, pgvector) · DynamoDB / MongoDB (enriched) · Valkey (cache)
 AWS (local): AWS Emulator + Floci ── S3 archive · DynamoDB store · SQS DLQ
 Observability: OpenTelemetry ─► Grafana (Prometheus · Loki · Tempo) + Langfuse (agents)
 Operations: ops-agent (AI SRE) investigates alerts through the Grafana MCP server
 Delivery: CircleCI ─► disposable test envs ─► Vercel · Aiven · Render/Koyeb · Oracle (Ollama)
```

## How this repo grows

Every weekday at about 17:40 (America/Edmonton), a mentor agent:

1. Reads [`.lab/state.json`](.lab/state.json) and your commits since the last challenge.
2. Writes `challenges/day-NNN/REVIEW.md` for the previous day: feedback on your code, and a reference solution for anything left unfinished.
3. Opens a pull request named `lab/day-NNN`, with `challenges/day-NNN/README.md` describing **3 challenges** (10–20 min each, at most 60 min in total) and any failing tests or stubs you need.

**Your loop:** merge the day's PR, `git pull`, solve the challenges, make the tests pass, and commit with `day-NNN: <what you did>`. Push before about 17:30 the next weekday. If a day isn't finished, the next run adapts to it instead of moving on.

See [ROADMAP.md](ROADMAP.md) for the curriculum, [docs/READING.md](docs/READING.md) for the reading plan, [docs/GOALS.md](docs/GOALS.md) for the goals and how they map to the target job, and [challenges/README.md](challenges/README.md) for the challenge format.

## How changes are made: spec → test → code → docs

1. **Spec:** an [OpenSpec](https://github.com/Fission-AI/OpenSpec) change with Given/When/Then scenarios (`openspec/changes/`)
2. **Test:** TDD, red → green → refactor, with tests named after the scenarios
3. **Code:** ports and adapters, async-first, current stable APIs
4. **Docs:** UML and C4 diagrams (Mermaid), OpenAPI and AsyncAPI contracts, arc42 ([docs/architecture](docs/architecture/README.md)), ADRs ([docs/adr](docs/adr/))

Instructions for coding agents live in [AGENTS.md](AGENTS.md), shared by Claude Code and Codex. Workflow skills come from [spec-driven-tdd-agent-skills](https://github.com/doikenichi/spec-driven-tdd-agent-skills) and are installed in `.claude/skills/` and `.agents/skills/`.

## Stack (all free for personal use; open source preferred)

| Area | Tools |
|---|---|
| Languages | Python 3.13 (uv, ruff, mypy, pytest), TypeScript (pnpm, tsc strict, eslint, vitest) |
| Services | FastAPI, asyncio, Node.js, Next.js / React |
| Events | Apache Kafka (KRaft), Confluent Schema Registry |
| AWS (local) | AWS Emulator (SDK work), Floci (Terraform/CI), Moto (unit tests) |
| AI | Claude Agent SDK and Codex (local dev, subscription login), Ollama (deployment), recorded responses (tests), MCP |
| Testing | pytest, vitest, Testcontainers, contract tests, Playwright, promptfoo / DeepEval |
| Performance and NFRs | k6 (with its MCP server), Locust, Kafka perf tools, Pyroscope, Toxiproxy, Chaos Mesh, Lighthouse CI, axe-core |
| Data | PostgreSQL 18 (with pgvector), Alembic, Debezium (CDC and outbox), DynamoDB (local) and MongoDB, Valkey |
| Observability | OpenTelemetry, Grafana LGTM (Prometheus, Loki, Tempo), Langfuse |
| Delivery | Docker, Terraform, kind, Kubernetes, Helm, CircleCI, Trivy, gitleaks, pre-commit |
| Deployment | Vercel Hobby, Aiven Kafka free tier, Render / Koyeb, Oracle Cloud Always Free |

## Repository layout

```
services/ingest-api/   Python FastAPI service that accepts events
services/enricher/     Python AI agent that enriches events
services/gateway/      TypeScript service that streams results
services/ops-agent/    Python AI SRE agent
web/dashboard/         Next.js live dashboard
tests/contract/        cross-service contract tests
tests/e2e/             Playwright end-to-end tests
infra/                 compose, terraform, k8s, helm, observability
.circleci/             CI/CD pipeline
openspec/              living specs and change proposals (OpenSpec)
docs/architecture/     arc42 with C4 and UML diagrams
docs/contracts/        OpenAPI, AsyncAPI, JSON Schemas
docs/adr/              architecture decision records
.claude/skills/        shared skills for Claude Code
.agents/skills/        shared skills for Codex
challenges/day-NNN/    daily challenges and reviews
.lab/state.json        lab progress (updated by the mentor)
```

Folders are created by the challenges as the platform grows.
