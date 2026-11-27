# ADR-0007: Product domains (surveillance brain and build insights) and privacy by design

- **Status:** accepted
- **Date:** 2026-11-27

## Context and problem
The platform was generic: it enriched any events. A concrete product gives the specs, tests and demos a story, and makes interview answers concrete. The domain should need little industry knowledge, exercise Kafka failure modes naturally, and support the goal of a robust build system. One hour a day means focus matters: two products in parallel would dilute progress.

## Considered options
1. **Payments monitoring:** reuses Paysafe experience, but has heavier domain rules.
2. **Package delivery tracking:** the simplest domain, but a less compelling demo.
3. **Smart surveillance brain:** a compelling demo, and a natural fit for duplicates, clock skew, heartbeats and bursts. It brings privacy obligations, and optional computer vision.
4. **Build insights (GitHub and CircleCI events):** real free data, dogfooding, the build-system goal and QA relevance.

## Decision outcome
- **Primary domain: the smart surveillance brain**, from Phase 1. It starts with **simulated detection events** (no computer vision), then bridges MQTT into Kafka, with Frigate on public sample footage as an optional later phase.
- **Second domain: build insights**, added in Phase 5 as a plug-in tenant, once CircleCI and the test infrastructure exist to feed it.
- **Privacy by design** is a set of requirements, not guidelines:
  - no facial recognition or plate recognition, with identity attributes stripped at ingestion and tested
  - own premises or public footage only
  - TTL retention with tested deletion
  - access audit logging
  - optional face blurring
  - a privacy section in the threat model
- **MQTT → Kafka:** your own small async bridge first (a learning challenge, with full control of keys and idempotency). The open-source Stream Reactor MQTT source connector is the documented alternative. Confluent's MQTT connector is avoided because it needs a commercial licence.

## Consequences
- The specs, contracts, tests and dashboard use camera, incident and build events. The architecture is unchanged.
- Strong distributed-testing scenarios: duplicates across cameras, clock skew (event time vs processing time), dropped heartbeats, bursts.
- Privacy and ethics become part of the security track, and an interview topic.
- Computer vision and vision-language models stay optional, so the daily time budget holds; recorded responses cover them in tests.
- Adding build insights tests the plug-in design: a new domain must not change the core.
