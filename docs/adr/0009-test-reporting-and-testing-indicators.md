# ADR-0009: Test reporting and testing indicators (CTRF, Allure, ReportPortal)

- **Status:** accepted
- **Date:** 2026-11-27

## Context and problem
Test automation produces results at every level (pytest, Vitest, Playwright and BDD, k6, agent evals). We need readable reports for each run, history across runs, failure triage, and **testing indicators** monitored over time, not just a red or green build. Build Insights (F15–F17) also needs the same data. QA/SDET roles expect experience with test reporting platforms.

## Considered options
1. **JUnit XML only**, read by CircleCI test insights: no extra tools, but shallow history and no triage.
2. **Allure Report 3:** a static HTML report per run, with steps, attachments, trends and categories; no server; metrics export to Prometheus or InfluxDB.
3. **ReportPortal (self-hosted, open source):** run history, ML auto-analysis of failures, triage states, flaky detection and dashboards; needs several services (API, UI, analyzer, a search engine, a message broker).
4. **Paid platforms** (Allure TestOps, TestRail, Xray, Qase, Currents): no usable free tier for this lab.

## Decision outcome
- **CTRF** (Common Test Report Format, JSON) is the single normalised results format, emitted by every runner (pytest, Vitest, Playwright, k6 summaries converted), next to JUnit XML for CircleCI.
- **Allure 3** from Phase 0: one readable report per CircleCI run, stored as an artifact (and later published), no account needed to read it.
- **Testing indicators** are a Build Insights feature (merged into F17): pass rate, flaky rate and score, duration trends per level, coverage and mutation score trends, spec scenarios with a BDD test, escaped defects with the level that should have caught them, exploratory session findings, and time to fix a red build. The series go to Prometheus and Grafana, next to the product telemetry, with alerts on regressions.
- **ReportPortal** in Phase 5, self-hosted only on the local Kubernetes cluster, deployed by Argo CD. It's the **industry benchmark** for Build Insights: on the same runs, compare its failure auto-analysis and flaky detection with our CI failure explainer and flaky score. Publishing to it never fails a build.
- **Authority:** the OpenSpec specs and their tests say whether a requirement is met; reports and portals only say what happened in a run.

## Consequences
- One format (CTRF) feeds Allure, ReportPortal and Build Insights, so no tool locks in the data.
- ReportPortal is heavy, so it never runs on free-tier hosts or in throwaway CI environments.
- Indicators are monitored, not gamed: none becomes a build gate without an ADR saying why.
