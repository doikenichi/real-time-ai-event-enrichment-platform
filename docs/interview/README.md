# Interview preparation

Each question here is answered with evidence from this platform: a link to the code, test, diagram or ADR that proves it. The mentor adds one short **interview drill** to each day's challenge PR, tied to that day's work. Write your answer here in your own words.

## How to answer (structure)
1. **Frame:** restate the problem and the goal (for example "correctness under at-least-once delivery").
2. **Approach:** the method, from the top level down.
3. **Specifics:** concrete techniques and tools.
4. **Evidence:** a real example (from past work and from this platform): what you built, which bug a test caught, and the result.
5. **Trade-offs:** what you'd do differently at scale, or for a given client.

Aim for about 2 minutes spoken. Use STAR (Situation, Task, Action, Result) for behavioural questions.

---

## Q1. How would you approach testing a distributed, event-driven system?
*Topics: eventual consistency, duplicate events, retries, idempotency, downstream validation, observability. Past experience: Paysafe asynchronous microservices, MapR.*

### My first answer (2026-11-26)
> I would start by understanding the event flow, service dependencies and expected state transitions. I would validate both individual services and end-to-end workflows, ensuring that events are processed correctly and downstream data remains consistent. I would also test failure scenarios, such as duplicate, delayed, missing and out-of-order events, validating retry mechanisms, idempotency and eventual consistency. Finally, I would use logs, metrics and correlation IDs to trace events and troubleshoot failures across services.

### Strengthened answer (target version)
> **Model first.** I map the event flow (producers, topics, consumers, stores) and each entity's state machine. I write down the delivery guarantee per hop, usually at-least-once, and the invariants that must always hold, such as "a payment is captured at most once".
>
> **Test at the right level.** Unit tests prove the handlers are idempotent and that illegal state transitions are rejected; I use property-based tests here. Contract tests keep producers and consumers aligned on schemas and headers. Component tests run each service against a real broker in Testcontainers. A small number of end-to-end tests cover the critical workflows.
>
> **Inject the failure modes deliberately.** I test duplicates (replay after a crash before commit), delays, gaps, out-of-order events for the same key (version checks, not last-writer-wins), poison messages (DLQ without blocking the partition), transient downstream failures (backoff with jitter, capped attempts) and consumer rebalances. Retries are only safe with idempotency, through idempotency keys or conditional upserts. For workflows across services, I verify the outbox pattern or saga compensation.
>
> **Assert eventual consistency properly.** I never use fixed sleeps. I poll for the expected state with a timeout tied to the SLO, check invariants along the way, and validate downstream data directly in the stores and downstream topics. Reconciliation of counts and checksums between stages runs both as a test and as a monitored job.
>
> **Make it observable.** Every event carries a correlation id and trace context in its headers. Trace-based tests assert the path across services. Lag, DLQ rate, retries and reconciliation mismatches are metrics with alerts, and runbooks explain how to follow one id across logs and traces.
>
> **Example.** At Paysafe, on asynchronous microservices running on MapR Streams (Kafka-API compatible), *[add a concrete case: the failure you tested, the bug you found, the result]*. In my current platform, *[link the challenge or test that reproduces duplicate or out-of-order events]*.

### Evidence from this platform
| Technique | Where it's implemented |
|---|---|
| Idempotent consumer, duplicate test | *TBD (Phase 1)* |
| Out-of-order events with version checks | *TBD* |
| DLQ and redrive | *TBD* |
| Eventual-consistency polling helper | *TBD* |
| Reconciliation job and test | *TBD* |
| Trace-based e2e test | *TBD (Phase 4)* |
| Fault injection (Toxiproxy) | *TBD (Phase 5)* |

## Question bank (the mentor adds to it)
- How do you guarantee exactly-once processing with Kafka, and what are its limits?
- How would you design and test an idempotent API?
- How do you test eventual consistency without flaky tests?
- How do you load-test an event-driven pipeline end to end?
- How do you secure a CI/CD pipeline and the software supply chain?
- How do you test an AI agent that calls tools?
- How do you explain an architecture trade-off to a non-technical client?
