# Contracts

The source of truth for the platform's interfaces (see the `api-and-event-contracts` skill):

| File | Standard | Covers |
|---|---|---|
| `openapi.yaml` | OpenAPI 3.1 | HTTP APIs (ingest-api, gateway) |
| `asyncapi.yaml` | AsyncAPI 3.0 | Kafka topics and SSE streams |
| `schemas/*.json` | JSON Schema | shared payloads (`EventIn`, `EnrichedEvent`, …) |

The files are created by the challenges, and every change is covered by contract tests.
