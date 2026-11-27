## ADDED Requirements

### Requirement: Service status indicator
The dashboard SHALL show each service's readiness as an accessible status element (`role="status"`), labelled with the service name, with the state stated in text and not conveyed by colour alone.

#### Scenario: shows the service as healthy when it is ready
- **GIVEN** the service `ingest-api` is ready
- **WHEN** the status indicator renders
- **THEN** a status labelled `ingest-api` shows the text "Healthy"

#### Scenario: shows the service as unavailable when it is not ready
- **GIVEN** the service `ingest-api` is not ready
- **WHEN** the status indicator renders
- **THEN** a status labelled `ingest-api` shows the text "Unavailable"

<!-- TODO (learner): add the scenario for an "unknown" state
     (for example, before the first readiness result arrives).
     Then run: openspec validate add-dashboard-service-status --strict -->
