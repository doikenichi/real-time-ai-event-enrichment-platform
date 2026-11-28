#!/usr/bin/env bash
# Runs once when the dev container is created. Idempotent: safe to run again.
set -euo pipefail

# The workspace mount is often owned by root on devcontainer and Codespaces hosts.
# Trust the physical path, the logical path, and the whole /workspaces/* tree.
workspace_dir="$(pwd -P)"
for dir in "$workspace_dir" "$PWD" "/workspaces/*"; do
  git config --global --get-all safe.directory | grep -Fxq "$dir" \
    || git config --global --add safe.directory "$dir"
done

# The `lab` helper on the PATH (scripts/lab: start, test, watch, check, save, stop, finish)
mkdir -p ~/.local/bin && ln -sf "$(pwd -P)/scripts/lab" ~/.local/bin/lab

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

# Set git email to the GitHub noreply address so commits never expose a private email.
# Runs immediately if gh is already authenticated (e.g. on a container rebuild with a
# persisted login volume); otherwise prints a one-liner to run after 'gh auth login'.
if gh auth status &>/dev/null; then
  noreply="$(gh api user --jq '"\(.id)+\(.login)@users.noreply.github.com"')"
  git config --global user.email "$noreply"
  echo "Git email set to $noreply"
else
  cat <<'HINT'
After 'gh auth login', set your git email once with:
  gh api user --jq '"\(.id)+\(.login)@users.noreply.github.com"' \
    | xargs git config --global user.email
HINT
fi

cat <<'MSG'

Dev container ready. First time on this machine only:
  gh auth login          # GitHub (then re-run the git email snippet above)
  claude                 # Claude Code: sign in with your Claude subscription
  codex login            # Codex: Sign in with ChatGPT (or: codex login --device-auth)
Logins are kept in Docker volumes on this machine and survive rebuilds.
MSG
