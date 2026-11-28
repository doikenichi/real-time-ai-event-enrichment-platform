## ADDED Requirements

### Requirement: Liveness probe
The service SHALL expose `GET /livez`, which reports whether the process can serve requests at all. It MUST NOT check downstream dependencies.

#### Scenario: liveness reports alive without checking dependencies
- **GIVEN** the service is running
- **AND** a downstream dependency is unavailable
- **WHEN** an orchestrator calls `GET /livez`
- **THEN** the service responds `200`

### Requirement: Readiness probe
The service SHALL expose `GET /readyz`, which runs every configured readiness check concurrently and reports whether the service should receive traffic.

#### Scenario: readiness is ok when all checks pass
- **GIVEN** every readiness check reports ready
- **WHEN** an orchestrator calls `GET /readyz`
- **THEN** the service responds `200`

#### Scenario: readiness is unavailable when any check fails
- **GIVEN** at least one readiness check reports not ready
- **WHEN** an orchestrator calls `GET /readyz`
- **THEN** the service responds `503`
- **AND** the body is RFC 9457 problem details (`application/problem+json`) without internal details

<!-- TODO (learner): add the scenario for a readiness check that hangs.
     It should say what happens, and within what time budget.
     Then run: openspec validate add-service-health-probes --strict -->
