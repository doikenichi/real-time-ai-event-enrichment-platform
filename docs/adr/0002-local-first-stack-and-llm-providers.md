# ADR-0002: Local-first stack, AWS emulators and swappable LLM providers

- **Status:** accepted
- **Date:** 2026-11-26

## Context
- Everything must be free for me to use; open source is preferred when it is the industry standard.
- LocalStack now requires an account and an auth token (since March 2026).
- I have Claude and ChatGPT subscriptions, but no paid API keys.
- The deployed app cannot use personal subscription credentials.

## Decision
- **AWS locally:** AWS Emulator (official, CC0, 200+ services) for SDK-level work, and Floci (MIT, published Docker image, documented Terraform support) for Terraform and CI. Moto handles fast unit tests.
- **LLMs** sit behind an `LLMProvider` port with these adapters:
  - `RecordedProvider`: tests, CI and the demo-mode fallback; deterministic and free
  - `ClaudeAgentSdkProvider`: local development through the Claude Agent SDK with my own subscription login, personal use only
  - `CodexProvider`: local development through Codex / Sign in with ChatGPT
  - `OllamaProvider`: the deployment target (Oracle Cloud Always Free), and a later local optimization
- **Real deployment** goes to free tiers outside AWS: Vercel Hobby, Aiven Kafka free tier, Render or Koyeb, and Oracle Cloud Always Free.

## Consequences
- Provider choice is one environment variable, and an eval suite can compare providers.
- The subscription SDKs are agent frameworks, so each call has more overhead than a plain chat endpoint. That is acceptable in development.
- Free tiers change, so their limits are checked again before each deployment challenge.
