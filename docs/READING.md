# Reading plan: five books, applied to this platform

Read a little, just in time, and apply it the same week. The mentor assigns reading that matches the current milestone, links each challenge to a chapter, and checks your notes (skill `reading-companion`).

| Short name | Book | Why it matters here |
|---|---|---|
| **DDIA** | *Designing Data-Intensive Applications*, 2nd ed., Martin Kleppmann and Chris Riccomini (O'Reilly, 2026) | Kafka, replication, transactions, streams: the theory behind the event backbone and the distributed-testing goal |
| **AIE** | *AI Engineering*, Chip Huyen (O'Reilly, 2025) | Building on foundation models: evals, prompts, RAG, agents, inference cost, architecture and user feedback |
| **DMLS** | *Designing Machine Learning Systems*, Chip Huyen (O'Reilly, 2022) | ML in production: data, features, deployment, drift, monitoring, testing in production, MLOps |
| **MLSDI** | *Machine Learning System Design Interview*, Ali Aminian and Alex Xu (ByteByteGo, 2023) | A repeatable framework for ML and AI system design interviews, plus case studies |
| **IE** | *Inference Engineering*, Philip Kiely (Baseten Books, 2026; free to read online at baseten.co) | Serving models: GPU and memory fundamentals, inference engines, KV cache, quantization, batching, autoscaling |

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
