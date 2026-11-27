# Interview preparation: QA/SDET and full stack

Prepare for two kinds of roles at once:
- **QA / SDET / test automation:** how you test, find and prevent defects, and build test frameworks and quality gates
- **Full stack developer:** how you design, build, ship and operate features (for example the Foci Full Stack Developer role)

Many questions are asked in both kinds of interview, but a good answer shifts emphasis. **QA answers** lead with test strategy, risk, coverage, automation frameworks and defect prevention. **Developer answers** lead with design for testability, implementation choices and operating in production. This platform is your evidence for both.

The mentor adds one short **interview drill** to each day's challenge PR, tied to that day's work, and alternates between the QA and full stack angles. Write your answers here, and the mentor reviews them the next day.

## How to answer (structure)
1. **Frame:** restate the problem and the goal (for example "correctness under at-least-once delivery").
2. **Approach:** the method, from the top level down.
3. **Specifics:** concrete techniques and tools.
4. **Evidence:** a real example (from past work and from this platform): what you built, which bug a test caught, and the result.
5. **Trade-offs:** what you'd do differently at scale, or for a given client.

Aim for about 2 minutes spoken. Use STAR (Situation, Task, Action, Result) for behavioural questions.

---

## Q1. How would you approach testing a distributed, event-driven system?
*Discuss eventual consistency, duplicate events, retries, idempotency, downstream validation and observability.*
**Asked in:** both kinds of interview. **Core technology:** Kafka.

### My first answer (2026-11-26)
> I would start by understanding the event flow, service dependencies and expected state transitions. I would validate both individual services and end-to-end workflows, ensuring that events are processed correctly and downstream data remains consistent. I would also test failure scenarios, such as duplicate, delayed, missing and out-of-order events, validating retry mechanisms, idempotency and eventual consistency. Finally, I would use logs, metrics and correlation IDs to trace events and troubleshoot failures across services.

**What's strong:** the right areas, in a sensible order. **What to add:** name the delivery guarantee and the invariants; explain *how* each failure mode is made safe (idempotency keys, version checks, the DLQ); explain *how* you assert eventual consistency (polling with a timeout, not sleeps); explain *how* you validate downstream (store queries, reconciliation); and end with a concrete example.

### Strengthened answer (target version)
> **Model first.** I map the event flow (producers, Kafka topics, consumers, stores) and each entity's state machine. I write down the delivery guarantee per hop, usually at-least-once in Kafka, because consumers commit offsets after processing. Then I list the invariants that must always hold, such as "an order is charged at most once".
>
> **Duplicates and idempotency.** At-least-once means duplicates *will* happen: producer retries, consumer crashes before commit, rebalances, replays. So every consumer must be idempotent, using an idempotency key or a conditional upsert with a version. I test it by replaying the same event and by killing the consumer between processing and committing, then asserting there's exactly one effect. On the producer side, I check `enable.idempotence` and `acks=all`.
>
> **Retries.** Transient failures retry with exponential backoff and jitter, with capped attempts. Poison messages go to a retry topic and then a DLQ, without blocking the partition. I test that retries plus idempotency never create duplicate effects, and that the DLQ keeps the error in its headers and can be redriven.
>
> **Ordering.** Kafka only orders events within a partition, so the key choice matters. I test out-of-order and late events for the same key, and assert that version or sequence checks reject stale updates instead of last-writer-wins.
>
> **Eventual consistency.** I never use fixed sleeps. Tests poll for the expected state with a timeout tied to the SLO, check invariants along the way, and report the last observed state on failure.
>
> **Downstream validation.** I check the actual downstream state, meaning the database records and downstream topics, not just the API response. Reconciliation compares counts and checksums between stages, both as a test and as a monitored job.
>
> **Observability.** Every event carries a correlation id and trace context in its Kafka headers, so I can follow one event across logs and traces. Trace-based tests assert the path. Consumer lag, DLQ rate, retries and reconciliation mismatches are metrics with alerts.
>
> **Levels and automation.** Unit tests cover idempotent handlers and state machines. Contract tests cover schemas and Schema Registry compatibility. Component tests run each service against a real Kafka in Testcontainers. A few end-to-end tests cover the critical flows, and fault injection (Toxiproxy) runs in CI.
>
> **Example.** *[Past work: the failure you tested, the bug you found, the result.]* In my current platform, *[link the test that replays duplicates or reorders events]*.

**QA emphasis:** spend more time on the test strategy, the risk-based choice of failure scenarios, the fault-injection harness and the CI gates. **Developer emphasis:** spend more time on designing for idempotency (keys, outbox, versioned upserts), partition-key choice and the producer and consumer configuration.

### Evidence from this platform
| Technique | Where it's implemented |
|---|---|
| Idempotent consumer; duplicate replay test | *TBD (Phase 1)* |
| Crash before commit, and rebalance tests | *TBD (Phase 1)* |
| Out-of-order events with version checks | *TBD (Phase 1)* |
| Retry topic, DLQ and redrive | *TBD (Phase 1)* |
| Eventual-consistency polling helper | *TBD (Phase 1)* |
| Downstream validation and reconciliation | *TBD (Phase 2)* |
| Trace-based e2e test | *TBD (Phase 4)* |
| Fault injection (Toxiproxy) | *TBD (Phase 5)* |

---

## Question bank (the mentor adds to it)

### Asked in both
- How do you guarantee exactly-once processing with Kafka, and what are its limits?
- How do you test eventual consistency without flaky tests?
- How do you load-test an event-driven pipeline end to end?
- How do you test an AI agent that calls tools?
- How do you secure a CI/CD pipeline and the software supply chain?

### QA / SDET focus
- How do you build a test strategy for a new microservice? What goes in each layer of the pyramid, and why?
- How would you design a test automation framework for REST APIs plus Kafka events?
- How do you deal with flaky tests? Which root causes have you found?
- How do you decide what to automate, and what not to?
- How do you do contract testing between services?
- How do you test data integrity across services and databases?
- How do you set and enforce quality gates in CI?
- Tell me about a critical defect you found before production (STAR).
- How do you run an exploratory testing session, and how do you make it accountable? (charters, time boxes, tours, debriefs, turning findings into automated regression tests)
- How would you explore an event-driven system that has no UI? (follow one event by correlation id, vary duplicates, order and faults, watch traces and topics)

### Full stack focus
- How would you design an idempotent API?
- How do you choose a Kafka partition key, and what goes wrong with a bad one?
- How do you stream live updates to a web UI (SSE vs WebSockets), and how do you test it?
- How do you design a service to be testable (ports and adapters, dependency injection)?
- How do you handle schema evolution across producers and consumers?
- How do you explain an architecture trade-off to a non-technical client?
- Tell me about a production incident you debugged across services (STAR).

---

## ML / AI system design (MLSDI framework)
Asked in AI engineer and senior full stack interviews. Practise it weekly, using this platform as the example.

**Framework:** clarify requirements → frame it as an ML task (inputs, outputs, objective) → data preparation → model development (start with a baseline) → evaluation (offline, then online) → deployment and serving (latency, cost, inference optimization) → monitoring (drift, feedback loops).

### Drills
- Design the real-time AI event enrichment platform end to end. Where does a classical model beat an LLM? (MLSDI framework; DMLS ch. 6; AIE ch. 1)
- How would you detect and handle data distribution shift in the enrichment pipeline? (DMLS ch. 8)
- How do you evaluate an LLM feature before and after launch? (AIE ch. 3–4; DMLS ch. 9)
- How would you cut inference cost by 5× without losing quality? (AIE ch. 9; IE)
- Re-tell an MLSDI case study (for example harmful content detection, or a recommendation system) using this platform's components.
