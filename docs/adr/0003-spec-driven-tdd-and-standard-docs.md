# ADR-0003: Spec-driven development with OpenSpec, TDD, and standard documentation

- **Status:** accepted
- **Date:** 2026-11-26

## Context and problem
AI coding agents write code fast, but they drift without clear intent. The lab also needs to build habits that industry teams and consulting clients expect: written requirements, tests first, and current architecture docs.

## Considered options
1. **GitHub Spec Kit:** the most widely known, with a full `/specify` → `/plan` → `/tasks` → `/implement` flow. Heavier per change.
2. **OpenSpec:** lightweight and spec-anchored. Small change proposals with spec deltas that are archived into living specs. Works with any agent.
3. **Plain plan mode in each agent:** no persistent artifacts.

## Decision outcome
**OpenSpec**, because daily 10–20 minute increments match its small change proposals, and its living specs stay current as changes are archived. It's combined with:
- **TDD:** red → green → refactor, with tests named after spec scenarios
- **UML and C4 diagrams** as Mermaid in Markdown
- **arc42** for architecture, **MADR** for ADRs, **Diátaxis** for the docs layout
- **OpenAPI 3.1 and AsyncAPI 3** as contracts

## Consequences
- Each challenge carries a little spec and docs work (about 5 minutes), offset by clearer tests and fewer rewrites.
- Specs and docs are reviewed alongside the code in every PR.
- Switching to Spec Kit later stays possible, because both store plain Markdown specs in git.
