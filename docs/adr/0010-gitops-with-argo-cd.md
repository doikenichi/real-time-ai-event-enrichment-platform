# ADR-0010: GitOps continuous delivery with Argo CD on the local cluster

- **Status:** accepted
- **Date:** 2026-11-27

## Context and problem
Phase 5 brings a local Kubernetes cluster (kind or k3d) with Helm charts. Deploying to it from CI by pushing `helm upgrade` needs cluster credentials in CI and leaves no record of the desired state. GitOps is the standard way teams deliver to Kubernetes, and it's common in full stack and platform job postings.

## Considered options
1. **Push-based:** CircleCI runs `helm upgrade` against the cluster.
2. **Argo CD** (CNCF graduated): pulls the desired state from git and reconciles it; UI, ApplicationSets, sync waves, health checks.
3. **Flux** (CNCF graduated): pull-based, controller-only, no built-in UI.

## Decision outcome
**Argo CD**, current supported minor (3.x, checked at install time against the release notes), installed with its Helm chart and managing itself:
- **CircleCI is CI:** test, build, scan, sign the images, and update the image tag in the GitOps folder (`infra/gitops/`) through a PR.
- **Argo CD is CD:** it syncs `infra/gitops/` into the cluster. An ApplicationSet with the pull-request generator creates **one namespace per open PR** (a preview environment) and deletes it when the PR closes.
- It also deploys the platform add-ons on the cluster: the observability stack and ReportPortal (ADR-0009).
- Real deployments to free-tier hosts (Vercel, Render or Koyeb, Oracle) stay CircleCI-driven, because those aren't Kubernetes.
- Reference lab: `brunobml/gitops-control-plane` (see `docs/REFERENCES.md`).

## Consequences
- No cluster credentials in CI; git is the audit log, and rollback is a revert.
- The cluster must be reachable from GitHub by Argo CD polling (no inbound webhook needed on a workstation).
- Flux knowledge transfers easily; the ADR is revisited if the UI stops being useful.
