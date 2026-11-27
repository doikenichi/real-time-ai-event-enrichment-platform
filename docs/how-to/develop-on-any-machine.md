# How to develop on any machine (dev container)

The whole toolchain (Python 3.15 with uv, Node.js 26 LTS with nvm and pnpm, Docker, GitHub CLI, OpenSpec, Claude Code and Codex) lives in a **dev container** defined in `.devcontainer/`. Each machine needs only three things.

## On each machine, once
1. **git**
2. **Docker**: Docker Desktop (macOS, Windows with WSL 2) or Docker Engine (Linux). Give it at least 4 CPUs and 8 GB of memory.
3. **An editor that opens dev containers.** Pick one:
   - **VS Code** with the *Dev Containers* extension (recommended)
   - a **JetBrains** IDE (built-in dev container support)
   - **DevPod** (open source, client-only, works with any editor over SSH)

## Start working
```bash
git clone https://github.com/doikenichi/real-time-ai-event-enrichment-platform.git
code real-time-ai-event-enrichment-platform   # then: "Reopen in Container"
```
The first build takes a few minutes; later starts take seconds. When it finishes, sign in once per machine:
```bash
gh auth login
claude          # Claude subscription login
codex login     # Sign in with ChatGPT (or: codex login --device-auth)
```
Logins, the uv cache and the pnpm store live in Docker volumes on that machine, so they survive rebuilds. They are never committed and never copied between machines.

## Switching machines
Commit and push on one machine, pull on the other. That's all: the container definition is in git, so both machines get the same tools and versions.

**Your `.env`** (git-ignored) is the one thing that doesn't travel. Keep its values in a password manager, and copy them from `.env.example`.

## No machine at all: GitHub Codespaces
The same `.devcontainer/` opens in a browser through GitHub Codespaces. Personal accounts include 120 core hours and 15 GB of storage a month, which is about 30 hours on the 4-core machine this stack needs. Stop the codespace when you finish, and delete old ones to save storage.

## How it's built
- **Base image:** `mcr.microsoft.com/devcontainers/base:resolute` (Ubuntu 26.04 LTS), plus uv copied from Astral's official image (`.devcontainer/Dockerfile`).
- **Features** (official ones only): Node.js 26 LTS (through nvm) with pnpm, Docker-in-Docker, GitHub CLI.
- **Runtime versions live in the standard pin files,** so every tool agrees on them:
  - `.python-version` → uv inside the container; pyenv or mise if you ever work on a host without the container
  - `.nvmrc` → nvm inside the container; nvm, fnm or mise on a host
  - Why uv instead of pyenv: uv installs prebuilt Python builds in seconds and reads the same `.python-version` file, while pyenv compiles Python from source. Install pyenv only on a host where you won't use the container.
- **Upgrading a runtime** is a one-line PR: change `.nvmrc` (and the node feature version) or `.python-version`, rebuild the container, and let CI prove it.
- **Docker-in-Docker,** not docker-outside-of-docker: Testcontainers, Compose bind mounts and kind clusters behave the same on every host, at the cost of a separate image cache inside the container (kept in a volume).
- **`post-create.sh`:** installs Python 3.15 (from `.python-version`), the pinned CLIs, and the project dependencies once the workspaces exist.
- Versions are pinned. Updating them is a PR, like any other change. See ADR-0011.

## Troubleshooting
| Symptom | Fix |
|---|---|
| Docker commands fail inside the container | Rebuild the container; check Docker Desktop is running with enough memory |
| `codex login` callback doesn't return | Use `codex login --device-auth` |
| Disk filling up | `docker volume ls`, then remove old `dind-*`, cache or store volumes |
