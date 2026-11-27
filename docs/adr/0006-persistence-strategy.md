# ADR-0006: Persistence strategy, polyglot with a purpose

- **Status:** accepted
- **Date:** 2026-11-26

## Context and problem
The platform needs durable state beyond Kafka: accepted events and idempotency keys, enrichment configuration, enriched results, embeddings for agent retrieval, caches and rate limits, and incident reports from the ops-agent. The goals require practising both SQL and NoSQL, as full stack and QA/SDET roles expect, with data validation across stores. The constraints still apply: every tool is free, open source is preferred when it's the industry standard, AWS runs locally only, and deployment uses free tiers.

The risk is **polyglot sprawl**: adding databases for their own sake. Each store below must own a job that it does better than the others, and the job must teach a concept that will come up in interviews.

## Options considered (by job)

| Job | Options | Choice | Why |
|---|---|---|---|
| System of record for ingested events, idempotency keys, tenants, enrichment rules | PostgreSQL, MySQL, MongoDB | **PostgreSQL 18** | Transactions and constraints make idempotency correct (unique keys, conditional inserts). It's the most popular open-source relational database, and has had async I/O and `uuidv7()` since 18 |
| Publishing events reliably (no dual writes) | App-level outbox poller, **transactional outbox + Debezium CDC**, Kafka transactions only | **Outbox table in Postgres, with Debezium's Outbox Event Router** into Kafka | One local transaction writes both the event and its outbox row. Debezium tails the write-ahead log and routes by aggregate type, with the aggregate id as the Kafka key, which keeps per-key ordering. This is the industry pattern for the dual-write problem, and the core of the distributed-testing goal |
| Enriched-event store (key-value access by `event_id` and tenant/time) | DynamoDB, MongoDB, Cassandra/ScyllaDB, Postgres JSONB | **Behind one port, with two adapters:** DynamoDB (local, AWS emulators) and MongoDB (deployed, Atlas free tier) | Teaches access-pattern-first NoSQL design: DynamoDB's single-table key-value design, and MongoDB's document design. One contract test suite runs against both adapters, which shows the value of ports and adapters. MongoDB data validation also appears in QA/SDET Kafka testing postings |
| Vector search for agent retrieval | pgvector, Qdrant, Weaviate | **pgvector in the same Postgres** | One less system to run. It's enough at this scale; a dedicated vector database is a documented scale-out option |
| Cache, rate limiting, semantic and prompt cache | Valkey, Redis 8, in-process | **Valkey** | BSD-licensed under the Linux Foundation, and Redis-compatible. Redis 8 is open source again under AGPLv3 (alongside source-available licences), and is fine to learn too; Valkey avoids licence ambiguity for clients |
| Raw-event archive and replay | S3 (emulated), Postgres | **S3**, unchanged | Cheap, immutable object storage |
| Ops-agent incident reports (flexible documents, evolving shape) | MongoDB, Postgres JSONB | **MongoDB** (same cluster as the enriched store when deployed) | Naturally document-shaped, and a good fit to contrast with relational modelling |

**Not adopted:** Cassandra and ScyllaDB (DynamoDB covers wide-column key design concepts), graph databases (no graph-shaped problem yet), and a separate vector database (pgvector is enough). Revisit if a real need appears.

## Decision outcome
- **SQL:** PostgreSQL 18 with SQLAlchemy 2.x async (asyncpg or psycopg 3) and Alembic migrations in Python; a typed query builder (Drizzle or Kysely) in TypeScript when the gateway needs to read. Versions are checked at challenge time.
- **NoSQL:** DynamoDB (local) and MongoDB (deployed) behind an `EnrichedEventStore` port; MongoDB for incident documents; Valkey for caching and rate limiting.
- **Integration:** a transactional outbox, published by Debezium CDC into Kafka. Kafka remains the backbone, and the databases feed it and are fed by it.
- **Free deployment:** Neon Free for Postgres (1 GB per project, scale to zero, no credit card) and MongoDB Atlas Free (512 MB, free forever). Valkey runs self-hosted on the Oracle Always Free VM. All limits are checked again before the deployment challenges.

## Consequences
- **Testing:** Testcontainers for Postgres, MongoDB and Valkey; migration tests (upgrade, downgrade, expand/contract compatibility); CDC tests (an outbox row becomes exactly one Kafka message with the right key); cross-store reconciliation (Postgres ↔ Kafka ↔ DynamoDB/MongoDB); data validation and integrity tests; SQL injection and authorization tests.
- **Security:** least-privilege database roles per service, row-level security for tenants, parameterized queries only, secrets in platform stores, and the Debezium user limited to replication on the outbox table.
- **Performance:** connection pooling, `EXPLAIN ANALYZE` checks on key queries, and k6 scenarios that include the database.
- **Cost of polyglot:** more moving parts. They're mitigated by ports and adapters, one Compose file and disposable test environments.
- **Books:** DDIA ch. 3–8 and 12 (data models, storage, encoding, replication, sharding, transactions, change data capture); APP repository and unit of work; DMLS ch. 3.
