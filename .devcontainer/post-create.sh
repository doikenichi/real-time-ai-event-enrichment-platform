#!/usr/bin/env bash
# Runs once when the dev container is created. Idempotent: safe to run again.
set -euo pipefail

# Named volumes are created as root; give them to the dev user.
sudo chown -R "$(id -u):$(id -g)" ~/.claude ~/.codex ~/.cache/uv ~/.local/share/pnpm 2>/dev/null || true

# Runtime versions come from the standard pin files, so host tools read the same ones:
#   .python-version → uv (and pyenv or mise on a host)
#   .nvmrc          → nvm (installed by the node feature; also fnm or mise on a host)
uv python install            # reads .python-version
source "${NVM_DIR:-/usr/local/share/nvm}/nvm.sh" && nvm install && nvm alias default "$(cat .nvmrc)"

# CLI tools pinned to the versions checked on 2026-11-27 (bump them through a PR)
npm install -g \
  @fission-ai/openspec@2.2.0 \
  @anthropic-ai/claude-code@2.1.332 \
  @openai/codex@0.172.0

# Project dependencies, once the workspaces exist (Day 001 creates them)
if [ -f pyproject.toml ]; then uv sync --all-packages; fi
if [ -f pnpm-workspace.yaml ]; then pnpm install --frozen-lockfile; fi
if [ -f .pre-commit-config.yaml ]; then uvx pre-commit install; fi

cat <<'MSG'

Dev container ready. First time on this machine only:
  gh auth login          # GitHub
  claude                 # Claude Code: sign in with your Claude subscription
  codex login            # Codex: Sign in with ChatGPT (or: codex login --device-auth)
Logins are kept in Docker volumes on this machine and survive rebuilds.
MSG
