# Goals

**What we're building:** an AI brain for event streams, with two products (see [PRODUCT.md](PRODUCT.md)). The primary one is a **smart surveillance brain** that turns camera detections into a few explained incidents, privacy by design. The second domain is **build insights** from GitHub and CircleCI events, dogfooding this repo's own build system.

## 1. Level up through deliberate daily practice
- **Python and TypeScript**, with a strong focus on **async**: asyncio, TaskGroup, structured concurrency, cancellation, backpressure; Promises, AbortController and streams in Node.js.
- **Industry design patterns and best practices**: ports and adapters (hexagonal architecture), repository, strategy, dependency injection, outbox, retry with backoff and jitter, circuit breaker, idempotency, CQRS where it fits.
- **Latest stable APIs only.** Every challenge checks current versions and avoids deprecated APIs.
- **Cloud-native DevOps**: Docker, Kubernetes, Helm, Terraform, CircleCI, observability.
- **AI engineering**: agents, tool calling, MCP, structured output, evals, agent testing, AI for monitoring, and AI coding agents.
- **Kafka and event-driven architecture.**

## 2. Be the best candidate for the target jobs
Prepare for both **full stack developer** and **QA / SDET (test automation)** roles. The primary posting is below; QA/SDET postings that ask for Kafka and event-driven testing are a second target. Interview prep for both lives in `docs/interview/`.

Target: **Full Stack Developer at Foci Solutions Inc.**, a remote software engineering consultancy (https://foci.bamboohr.com/careers/18).

| What the job asks for | Where this lab covers it |
|---|---|
| Full stack, production-grade applications | Python and TypeScript services plus a Next.js dashboard, deployed to real hosts |
| Deploying on GCP, Azure and/or AWS | AWS through local emulators (AWS Emulator, Floci), Terraform; real deployment to free-tier hosts |
| AI-driven development and AI coding agents | Claude Code / Codex / Copilot challenges, CLAUDE.md, delegating and reviewing, agents in CI |
| Docker and Kubernetes | Compose, kind, Helm, disposable environments |
| Modern languages (.NET, TypeScript, Python) | TypeScript and Python (by choice, no .NET) |
| Architecting solutions, client collaboration | ADRs in `docs/adr/`, trade-off write-ups, clear READMEs and runbooks |
| Maintainability over complexity | Tests at every layer, small reviewed increments, shift-left checks |

## 3. Spec-driven development, TDD and standard documentation
Every change follows spec (OpenSpec, Given/When/Then) → test (TDD) → code → docs (UML and C4 in Mermaid, OpenAPI and AsyncAPI, arc42, ADRs). The same workflow skills are shared by Claude Code and Codex.

## 4. Testing is part of the workflow
Unit, integration, contract, end-to-end (BDD for functional and regression testing), **exploratory testing** (Whittaker's tours, charters and time-boxed sessions), shift-left, disposable test environments, AI agent testing (recorded responses, trajectories, evals, red-teaming, budgets) and telemetry tests.

## 5. Secure by default
Repo rulesets, secret scanning, Dependabot, SAST (CodeQL, Semgrep), supply chain (SBOM, signing, Scorecard), IaC and container scanning, DAST, STRIDE threat modeling, and the OWASP Top 10 for web, API and LLM applications.

## 6. Every lab reflects current industry standards
Before proposing a lab, the mentor researches current industry standards and best practices: official docs, OWASP, NIST, CNCF, OpenSSF, Thoughtworks Technology Radar, vendor engineering blogs and recent job postings. Each challenge says which standard it follows, cites its sources, and names the goal it serves.

## 7. Performance and non-functional quality
Practice load, stress, spike, soak and breakpoint testing, plus resilience, web performance and accessibility testing, on the platform itself. NFRs are written as spec scenarios with numbers, derived from SLOs, and CI is gated on them. The tools are free and widely used: k6 (default), Locust (Python and LLM paths), Kafka perf tools, Pyroscope and py-spy (profiling), Toxiproxy and Chaos Mesh (fault injection), Lighthouse CI (web vitals) and axe-core (WCAG 2.2 AA). AI works on top: the official k6 MCP server and skills for Claude Code and Codex, and a perf-analyst agent that explains regressions. Heavy load runs only against local or disposable environments, never against free-tier hosts.

## 8. Master testing distributed, event-driven systems with Kafka, and explaining it
A core skill to learn and to talk about with confidence: *"How would you approach testing a distributed, event-driven system? Discuss eventual consistency, duplicate events, retries, idempotency, downstream validation and observability."* Kafka is the backbone. Learn it in depth: partitions and keys, producer idempotence and acks, delivery semantics, transactions and exactly-once, consumer groups and rebalances (including the Kafka 4.x protocol), offsets and replay, retry topics and DLQ, Schema Registry compatibility, compaction, lag, and share groups. Practise every failure mode on this platform: duplicate, delayed, missing, out-of-order and poison events; retries; idempotency; outbox and sagas; eventual-consistency assertions without sleeps; downstream validation and reconciliation; trace-based tests with correlation IDs. Show the concepts transfer to other brokers (SQS in Phase 2). Build evidence-backed answers in `docs/interview/`.

## 9. Learn from the canon, and apply it
Get the most out of the books in `docs/READING.md` by reading just in time and applying each idea in the platform the same week. For systems and AI: *Designing Data-Intensive Applications* (2nd ed.), *AI Engineering*, *Designing Machine Learning Systems*, *Machine Learning System Design Interview* and *Inference Engineering*. For the languages and design: *Node.js Design Patterns* (4th ed.), *Fluent Python* (2nd ed.) and *Architecture Patterns with Python*. For product, UX and testing craft: *Lean Inception*, *The Design of Everyday Things* and *Exploratory Software Testing* (James Whittaker). The plan is in `docs/READING.md`, and notes in your own words go in `docs/reading-notes/`. Every challenge links to a chapter, and interview answers cite the concepts.

## 10. Build a robust build system, and measure it
CircleCI pipelines that are fast, reliable and secure: path-filtered builds for the monorepo (only what changed), caching, test splitting by timing, flaky-test detection and quarantine, reproducible builds (lockfiles, pinned toolchains and image digests), disposable environments, supply-chain security, build observability (pipeline traces and metrics), build-time SLOs, and DORA's delivery metrics. The build-insights domain analyses this repo's own builds.

## 11. AI agents wherever they add value
The enricher agent, the ops-agent (AI SRE), test-generation and exploratory e2e agents, LLM-as-judge evals, a CircleCI build-failure agent, PR review, and coding agents. You still write the core code yourself; agents are what you build, test, monitor and work with.

## Constraints
- **Free for me to use.** Open source is preferred, as long as the tool is the industry standard.
- **10–20 minutes per challenge, 3 challenges a day, at most 60 minutes.**
- **LLMs in development:** Claude (Claude Agent SDK, local subscription login) and OpenAI (Codex, Sign in with ChatGPT). Ollama locally is a later optimization.
- **LLMs in deployment:** Ollama on a free-tier host, with recorded-response demo mode as the fallback. Never deploy subscription credentials.
- **AWS stays local** (emulators). Real deployment uses non-AWS free tiers.
