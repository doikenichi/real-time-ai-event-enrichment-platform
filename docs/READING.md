# Reading plan: eleven books, applied to this platform

Read a little, just in time, and apply it the same week. The mentor assigns reading that matches the current milestone, links each challenge to a chapter, and checks your notes (skill `reading-companion`).

| Short name | Book | Why it matters here |
|---|---|---|
| **DDIA** | *Designing Data-Intensive Applications*, 2nd ed., Martin Kleppmann and Chris Riccomini (O'Reilly, 2026) | Kafka, replication, transactions, streams: the theory behind the event backbone and the distributed-testing goal |
| **AIE** | *AI Engineering*, Chip Huyen (O'Reilly, 2025) | Building on foundation models: evals, prompts, RAG, agents, inference cost, architecture and user feedback |
| **DMLS** | *Designing Machine Learning Systems*, Chip Huyen (O'Reilly, 2022) | ML in production: data, features, deployment, drift, monitoring, testing in production, MLOps |
| **MLSDI** | *Machine Learning System Design Interview*, Ali Aminian and Alex Xu (ByteByteGo, 2023) | A repeatable framework for ML and AI system design interviews, plus case studies |
| **IE** | *Inference Engineering*, Philip Kiely (Baseten Books, 2026; free to read online at baseten.co) | Serving models: GPU and memory fundamentals, inference engines, KV cache, quantization, batching, autoscaling |

**Product and UX books** (what to build, and how it should feel):

| Short name | Book | Why it matters here |
|---|---|---|
| **LI** | *Lean Inception: How to Align People and Build the Right Product*, Paulo Caroli (2018); the activities are also summarised on martinfowler.com | Vision, personas, journeys, feature review, the Feature Sequencer and the MVP Canvas behind `docs/product/lean-inception.md` |
| **DOET** | *The Design of Everyday Things*, revised and expanded edition, Don Norman (Basic Books, 2013) | Discoverability, affordances, signifiers, constraints, mapping, feedback, conceptual models, designing for error: the basis of `docs/ux/PRINCIPLES.md` |

**Testing craft:**

| Short name | Book | Why it matters here |
|---|---|---|
| **EST** | *Exploratory Software Testing: Tips, Tricks, Tours, and Techniques to Guide Test Design*, James A. Whittaker (Addison-Wesley, 2009) | Exploratory testing as a discipline: varying inputs, state, code paths, data and environment, and the tourist metaphor with its tours. The weekly exploratory sessions follow it (`docs/testing/exploratory/`) |

**Language and design books** (how to write the code well, in each language):

| Short name | Book | Why it matters here |
|---|---|---|
| **NodeDP** | *Node.js Design Patterns*, 4th ed., Luciano Mammino and Mario Casciaro (Packt, 2025) | The TypeScript side: the gateway, async control flow, streams and backpressure, GoF patterns in JavaScript, testing, scalability and messaging. Updated for Node.js 24, ESM and TypeScript; this platform runs Node.js 26 LTS, so check the Node.js changelog when an example uses an API that changed. Companion code: your fork `doikenichi/Node.js-Design-Patterns-Fourth-Edition` |
| **FP** | *Fluent Python*, 2nd ed., Luciano Ramalho (O'Reilly, 2022) | Idiomatic modern Python: the data model, protocols, type hints, decorators, context managers, and concurrency with async/await |
| **APP** | *Architecture Patterns with Python* ("Cosmic Python"), Harry Percival and Bob Gregory (O'Reilly, 2020; free to read online at cosmicpython.com) | The Python equivalent of a patterns book for this platform: ports and adapters, repository, unit of work, aggregates, events and message bus, CQRS and dependency injection, all test-driven |

*Why two Python books:* Fluent Python teaches the **language** (the counterpart to NodeDP's platform chapters), and Architecture Patterns with Python teaches the **architecture patterns** (the counterpart to NodeDP's design-pattern chapters), using exactly the patterns this platform uses. APP is from 2020, so its examples use older Flask and SQLAlchemy APIs; the patterns hold, and you implement them with FastAPI and current libraries.

*If you meant a different "Inference Engineering" book (for example the Manning compilation), tell the mentor, and it will remap.*

## How to read (about 2 × 25 min a week, outside the daily 60 minutes)
1. **Before:** skim the assigned section's headings, then read with one question in mind, taken from the challenge.
2. **After:** write 5–10 lines in `docs/reading-notes/<book>.md`, in your own words: the key idea, where it shows up in the platform (a link), and one open question.
3. **Apply:** the same week's challenges use the idea; their "Book reference" line points back to it.
4. **Recall:** later drills ask about it with the book closed.
5. **Tip:** books age. When a book and the current docs disagree, the current docs win, and that difference is worth a note.

## Map: roadmap phases → chapters
Chapter numbers come from each publisher's table of contents. For IE, the mentor uses the free online index for exact chapter names, and refers to topics until it has checked them.

| Phase | Lab focus | Read |
|---|---|---|
| **0 Foundations** | services, dashboard, protected repo | DDIA ch. 1 "Trade-Offs in Data Systems Architecture", ch. 2 (nonfunctional requirements: reliability, scalability, maintainability) · AIE ch. 1 "Introduction to Building AI Applications with Foundation Models" · DMLS ch. 1 "Overview of Machine Learning Systems" |
| **1 Event backbone** | Kafka, idempotency, retries, DLQ, ordering, schema evolution | DDIA ch. 5 "Encoding and Evolution" (schemas, compatibility) · ch. 6 "Replication" · ch. 9 (faults in distributed systems: timeouts, unreliable networks and clocks) · ch. 12 (stream processing: logs, exactly-once, idempotence) |
| **2 AWS locally** | storage, DynamoDB, S3, sagas, reconciliation | DDIA ch. 3 "Data Models and Query Languages" · ch. 4 "Storage and Retrieval" · ch. 7 (sharding and partitioning) · ch. 8 "Transactions" · DMLS ch. 3 "Data Engineering Fundamentals" |
| **3 Enricher agent** | LLM providers, tools, MCP, structured output, evals, guardrails | AIE ch. 2 "Understanding Foundation Models" · ch. 3 "Evaluation Methodology" · ch. 4 "Evaluate AI Systems" · ch. 5 "Prompt Engineering" (including prompt attacks and defences) · ch. 6 "RAG and Agents" (tools, planning, agent failure modes) · DMLS ch. 6 "Model Development and Offline Evaluation" (baselines) |
| **4 Observability** | logs, traces, metrics, SLOs, drift | DMLS ch. 8 "Data Distribution Shifts and Monitoring" · AIE ch. 10 "AI Engineering Architecture and User Feedback" · DDIA ch. 13 "A Philosophy of Streaming Systems" (derived data) |
| **5 Test environments at scale** | performance gates, Kubernetes, resilience | DDIA ch. 2 (performance: percentiles, load) again · ch. 10 "Consistency and Consensus" · DMLS ch. 10 "Infrastructure and Tooling for MLOps" |
| **6 Ops agent** | AI SRE, multi-agent, chaos drills as evals | AIE ch. 6 (agents and their evaluation) again · ch. 4 (building an evaluation pipeline) · DMLS ch. 8 (monitoring and observability) |
| **7 Real deployment** | Ollama on free tiers, CD, canary, smoke tests | IE (inference fundamentals, engines, quantization, KV cache, batching, autoscaling) · AIE ch. 9 "Inference Optimization" · DMLS ch. 7 "Model Deployment and Prediction Service" · ch. 9 "Continual Learning and Test in Production" (shadow, canary, A/B) |
| **8 Agents everywhere and polish** | agents in CI, Ollama optimization, interview readiness | IE (performance tuning and benchmarking) · AIE ch. 7 "Finetuning" and ch. 8 "Dataset Engineering" (when *not* to finetune; eval datasets) · DMLS ch. 11 "The Human Side of Machine Learning" · DDIA ch. 14 "Doing the Right Thing" · MLSDI (the whole framework and case studies, as drills) |

### Language and design books, by phase
NodeDP chapter numbers 1–4 and 10–13 are checked against Packt's table of contents. For chapters 5–9 (promises and async/await, streams, and the creational, structural and behavioral patterns), the mentor confirms the numbers before citing them. For FP and APP, the mentor checks against the O'Reilly tables of contents and cosmicpython.com.

| Phase | NodeDP (TypeScript side) | FP (Python language) | APP (Python architecture) |
|---|---|---|---|
| **0** | ch. 1 "The Node.js Platform" (event loop, non-blocking I/O) · ch. 2 "The Module System" (ESM) | the Python data model; data class builders | introduction and the chapter on coupling and abstractions (why `create_app` injects its checks) |
| **1** | ch. 3 "Callbacks and Events" · ch. 4 async control flow patterns · promises and async/await · streams (the SSE gateway and backpressure) · ch. 13 "Messaging and Integration Patterns" | concurrency models; asynchronous programming (asyncio, TaskGroup, cancellation) | events and the message bus; commands and handlers; using events to integrate microservices |
| **2** | the creational and structural patterns (factory, adapter, proxy for the storage clients) | interfaces, protocols and ABCs (`typing.Protocol` for ports) | repository pattern; unit of work; aggregates and consistency boundaries |
| **3** | the behavioral patterns (strategy, middleware, command) | type hints in depth; design patterns with first-class functions (strategy for LLM providers) | the service layer; domain modelling for the enrichment rules |
| **4** | — | decorators and closures (instrumentation); context managers (spans, timeouts) | — |
| **5** | ch. 10 "Testing: Patterns and Best Practices" · ch. 12 "Scalability and Architectural Patterns" | — | TDD "in high gear and low gear" (which level to test at) |
| **7–8** | ch. 11 "Advanced Recipes" (cancellation, batching and caching of async work) | — | CQRS; dependency injection and bootstrapping |

**Product and UX:** LI at the start of each new wave (re-check the vision, journeys and sequencer) · DOET when building the dashboard, alerts and review queue (chapters on the psychology of everyday actions, and on human error). Check chapter titles against the publishers' tables of contents.

**Exploratory testing (EST), checked against the publisher's table of contents:** ch. 1 "The Case for Software Quality" and ch. 2 "The Case for Manual Testing" (Phase 0, quick reads) · ch. 3 "Exploratory Testing in the Small" (Phase 0–1: user input, state, code paths, user data, environment; the first sessions on the ingest API) · ch. 4 "Exploratory Testing in the Large" (Phase 1–2: the tourist metaphor and the tours, one district at a time) · ch. 5 "Hybrid Exploratory Testing Techniques" (Phase 3–5: scenario-based exploration, varying the BDD scenarios) · ch. 6 "Exploratory Testing in Practice" (Phase 5: how real teams adapted the tours) · ch. 7 "Touring and Testing's Primary Pain Points" (Phase 5–8: flaky tests, regression, test-case churn) · the closing chapter and appendices (testing careers) for interview prep. The book is from 2009, so its examples are desktop and early web apps; apply the tours to APIs, event streams and agents, and pair them with session-based test management (charters, time boxes, debriefs).

**Persistence (ADR-0006):** DDIA ch. 3 (relational vs document models), ch. 4 (storage engines and indexes), ch. 6–8 (replication, sharding, transactions) and ch. 12 (change data capture, the outbox) · APP repository and unit of work · FP data classes for row and document mapping.

**MLSDI runs alongside every phase:** its first chapter's framework (clarify requirements → frame as an ML task → data → model → evaluation → deployment and serving → monitoring) becomes a weekly design drill. Its case-study chapters are practised one per drill, each re-told with this platform's components.

## New lab milestones these books add
These are already in `ROADMAP.md`:
- **Baseline before LLM** (DMLS ch. 6, AIE ch. 1): a cheap classical classifier for event category, compared with the LLM on cost and quality, then a cascade (try cheap first, escalate to the LLM)
- **Drift monitoring for inputs and outputs** (DMLS ch. 8): alert when the event mix or the enrichment output distribution shifts
- **User feedback loop** (AIE ch. 10): thumbs up or down on the dashboard flows into the eval dataset
- **Test in production** (DMLS ch. 9): shadow and canary releases for prompt or model versions, gated by evals
- **Inference benchmarks** (IE, AIE ch. 9): time to first token, time per output token, throughput and cost, across Ollama quantization levels, under k6/Locust load
- **Semantic and prompt caching** (AIE ch. 9): measured hit rate and latency savings
- **Streams as the source of truth** (DDIA ch. 12–13): rebuild a derived view from the Kafka log, and prove it with a replay test
