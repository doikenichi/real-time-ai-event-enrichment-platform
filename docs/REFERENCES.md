# Curated reference repositories

Hands-on labs to consult whenever a challenge touches their topics. They complement, and never replace, the primary sources (official docs, standards and changelogs) that every challenge cites.

**Licence note:** these repositories publish no licence file (checked 2026-11-27), so all rights are reserved by default. Read them, learn from them and link to them; don't copy their code or text into this repo. Write your own version, and cite the file you learned from.

| Repository | What it covers | Use it for | Roadmap phases |
|---|---|---|---|
| [brunobml/helm-lab](https://github.com/brunobml/helm-lab) | Helm 3 learned by evolving one chart over 18 labs: values and environments, template logic, helpers and labels, ConfigMaps and rollouts, `values.schema.json` validation, helm-unittest tests and `helm test` hooks, dependencies, packaging and OCI, hooks and failure recovery, library charts, secrets (sops) and signing (cosign) in CI, chart-testing (`ct`), CRDs and operators, production hardening (PDB, HPA, NetworkPolicy, RBAC, non-root), Helmfile and Argo CD ApplicationSets. Maps to the Linux Foundation SC104 Helm certification. Verified on Kubernetes 1.35 with Helm 3.19 | writing and testing this platform's Helm charts | 5 (kind, manifests, Helm charts), 7 |
| [brunobml/gitops-control-plane](https://github.com/brunobml/gitops-control-plane) | A local multi-cluster hub-and-spoke GitOps platform on k3d: self-managed Argo CD with ApplicationSets and AppProjects, kro blueprints, ACK controllers against a moto mock AWS, Kyverno cosign signature checks and admission policies, Keycloak SSO, Prometheus, Loki, Grafana and Alloy, Bats smoke tests as end-to-end gates, CI render and policy checks, runbooks and promotion guardrails | GitOps and continuous delivery on Kubernetes, policy as code, supply-chain admission checks, platform smoke tests, the observability stack on Kubernetes | 4 (observability), 5 (Kubernetes, supply chain, disposable environments), 7 (CD) |
| [brunobml/ollama-lab](https://github.com/brunobml/ollama-lab) | Local LLM inference with Ollama on a 10 GB GPU, in 10 measured labs: models on disk and in memory, VRAM sizing, sampling and reproducibility, streaming and structured output, embeddings and local RAG with retrieval evals, tool calling, MCP and agents (including tool safety), multimodal models and vision prompt injection, Ollama in containers and Kubernetes, and a runtime comparison (Ollama, llama.cpp, LM Studio). Each lab records hypotheses and observed metrics | `OllamaProvider`, inference benchmarks, structured output, RAG, MCP tools, vision descriptions of extracted frames (F19), Ollama deployment | 3 (enricher agent, MCP), 7 (Ollama deployment, inference benchmarks), 8 (Ollama optimization, computer vision) |

Snapshot reviewed: helm-lab `e963679`, gitops-control-plane `55bd48b`, ollama-lab `986341d`. Re-check the latest commit before citing a file.

## How the mentor uses them
- When a challenge touches Helm, Kubernetes, GitOps, policy as code or Ollama, read the matching lab first, and add it as a **Reference lab** line next to the challenge's primary sources.
- Compare its approach with the current official docs. When they differ (newer versions, deprecations), follow the official docs and say so.
- Adapt, don't transplant: these labs target other apps (an NGINX chart, an orders service, a Windows GPU workstation). Translate the idea to this platform's services and events.
