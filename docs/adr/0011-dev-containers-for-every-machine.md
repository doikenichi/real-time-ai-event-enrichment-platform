# ADR-0011: Dev containers, so any machine is ready in minutes

- **Status:** accepted
- **Date:** 2026-11-27

## Context and problem
The learner works on more than one machine (a desktop and a laptop) and doesn't want to install and configure the toolchain on each. Host setup should stay at git, Docker and an editor.

## Considered options
1. **Dev container** (Development Container spec, `.devcontainer/`): supported by VS Code, JetBrains, DevPod, the devcontainer CLI and GitHub Codespaces.
2. **Per-host version managers** (mise, asdf) or **Nix/devbox:** reproducible tools, but each machine still installs the manager, Docker and system packages, and Windows support varies.
3. **Cloud-only workspaces** (Codespaces, Gitpod): no local setup, but a monthly free quota that this stack would use up fast.

## Decision outcome
**Option 1**, with Codespaces as the fallback that reuses the same definition:
- Base image `mcr.microsoft.com/devcontainers/base:resolute` (Ubuntu 26.04 LTS); uv copied from Astral's image; official features only (Node.js 26 LTS through nvm, with pnpm; Docker-in-Docker; GitHub CLI); pinned CLI versions in `post-create.sh`.
- **LTS lines only** for the OS and Node.js; the versions live in `.nvmrc` and `.python-version`, which nvm, uv, pyenv and mise all read. uv replaces pyenv inside the container (prebuilt Pythons, no compiling).
- **Docker-in-Docker** over docker-outside-of-docker, because Testcontainers, Compose bind mounts and kind behave the same everywhere.
- Logins (GitHub, Claude, Codex) and caches live in per-machine Docker volumes: never committed, never shared, never in an image.
- How-to: `docs/how-to/develop-on-any-machine.md`.

## Consequences
- New machine: clone, "Reopen in Container", sign in once. The first build takes minutes.
- The container definition is code: version bumps are PRs, and CI checks that it builds (a roadmap milestone).
- Docker-in-Docker runs privileged and keeps a second image cache; acceptable for a personal lab.
- Kubernetes, Argo CD and k6 tools are added to the container in the phases that need them, so it stays small.
