# ADR-0005: Monorepo layout and tooling

- **Status:** accepted
- **Date:** 2026-11-28

## Context

The platform has Python services, a TypeScript dashboard, and API contracts that evolve together. A change to an API response can require updates to the service, the contract, and the dashboard tests. The lab needs a way to review those changes together and install consistent dependency versions in development and CI.

## Options considered

1. **Separate repositories.** Each component can have its own access controls and release workflow. Coordinated changes require multiple pull requests and careful merge ordering.
2. **One repository with uv and pnpm workspaces.** The tools group related projects by language and maintain a lockfile per workspace. Developers and CI need both toolchains when a change spans Python and TypeScript.
3. **Poetry for Python.** Poetry manages Python dependencies and lockfiles. Keeping separate Poetry projects would require managing their environments and dependency updates individually. The uv workspace shares one lockfile across Python services.
4. **Nx or Turborepo.** Either can coordinate tasks and cache outputs. With one initial project per language, the extra task configuration has little immediate value.

## Decision

Keep services, the dashboard, and contracts in one Git repository. Use a uv workspace defined in the root `pyproject.toml` for Python projects under `services/*`, starting with `services/ingest-api`. Use a pnpm workspace defined in `pnpm-workspace.yaml` for web projects under `web/*`, starting with the planned `web/dashboard`. Commit `uv.lock` and commit `pnpm-lock.yaml` when the web workspace is set up.

## Consequences

A single pull request can update the API, its contract, and the dashboard together. The lockfiles allow developers and CI to install the same resolved dependency versions. Changes to shared configuration or lockfiles can affect multiple projects, so CI must account for those dependencies when selecting checks. Revisit task orchestration and caching if build times become a problem.
