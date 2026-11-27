# ADR-0008: BDD for end-to-end functional and regression tests

- **Status:** accepted
- **Date:** 2026-11-27

## Context and problem
The e2e suite checks the product's behaviour for its personas (Maya, Sam, Dev) across the web, the API and Kafka. Its tests should read like the spec scenarios, double as regression tests, and be skills that QA/SDET roles ask for.

## Considered options
1. **Plain Playwright and pytest tests:** less tooling, but behaviour is hidden in code.
2. **BDD with Gherkin, run by the existing runners:** playwright-bdd (MIT) generates native Playwright tests; pytest-bdd (MIT) runs inside pytest.
3. **Standalone Cucumber.js and behave:** a separate runner, losing Playwright fixtures, parallelism and traces, and pytest fixtures.

## Decision outcome
**Option 2.** OpenSpec Given/When/Then scenarios that are user-visible or cross services become Gherkin scenarios with the same names in `tests/e2e/features/`. Steps are declarative and in domain language. `@smoke` runs on every PR and after deploys, and `@regression` runs on main and nightly; every fixed bug first adds a tagged regression scenario. Unit, contract and integration tests stay plain pytest and vitest.

## Consequences
- Feature files are living documentation, and reports show which feature or journey failed.
- Step vocabulary needs upkeep; the `bdd-acceptance-testing` skill's checklist is used in reviews.
- Async outcomes poll with SLO timeouts, as in all distributed tests.
