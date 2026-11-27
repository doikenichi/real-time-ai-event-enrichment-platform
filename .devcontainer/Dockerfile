# Dev container image: the only thing each machine builds or pulls.
# Versions are pinned; Dependabot (devcontainers and docker ecosystems) proposes updates.
FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

# uv (Python toolchain and package manager), copied from Astral's official image
COPY --from=ghcr.io/astral-sh/uv:0.13.10 /uv /uvx /usr/local/bin/

ENV UV_LINK_MODE=copy \
    UV_PYTHON_PREFERENCE=only-managed
