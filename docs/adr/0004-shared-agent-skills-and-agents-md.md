# ADR-0004: Shared Agent Skills and AGENTS.md for Claude Code and Codex

- **Status:** accepted
- **Date:** 2026-11-26

## Context and problem
I use both Claude Code and OpenAI Codex. Instructions and workflows should be written once and behave the same in both.

## Decision outcome
- **Instructions:** `AGENTS.md` is the single source. `CLAUDE.md` contains only `@AGENTS.md`, which works on every Claude Code version, and Codex reads `AGENTS.md` natively.
- **Skills:** shared [Agent Skills](https://agentskills.io) live in their own repo, [spec-driven-tdd-agent-skills](https://github.com/doikenichi/spec-driven-tdd-agent-skills). They are installed into this repo with `npx skills add … -a claude-code -a codex`, which writes `.claude/skills/` (Claude Code) and `.agents/skills/` (Codex). The installed copies are committed, and `.lab/skills.json` records the source commit.

## Consequences
- One place to improve a workflow, and every project that installs the skills benefits.
- The two installed folders must not be edited directly; they are re-synced from the skills repo.
- The skills repo is portfolio material on its own.
