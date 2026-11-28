# Add service health probes to ingest-api

## Why
Orchestrators (Docker, Kubernetes, CI environments) need to know two different things about a service: is it alive (restart it if not), and is it ready (send it traffic only if so). Mixing the two causes restart storms when a dependency is down.

## What changes
- New `ingest-api` service, the first member of the uv workspace
- `GET /livez`: liveness, with no dependency checks
- `GET /readyz`: readiness, which runs injectable async readiness checks (a port), and returns RFC 9457 problem details on failure
- Readiness checks run under a time budget, so a hung dependency can't hang the probe

## Impact
- New capability: `service-health`
- New code: `services/ingest-api/`
- Docs: ADR-0005 (monorepo layout and tooling)
