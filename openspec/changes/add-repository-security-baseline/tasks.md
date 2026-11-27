# Tasks

## 1. Spec
- [ ] 1.1 Add the PR checklist requirement; `openspec validate add-repository-security-baseline --strict` passes

## 2. Test (red)
- [ ] 2.1 `scripts/check-repo-baseline.sh` runs and fails

## 3. Configure (green)
- [ ] 3.1 Ruleset "Protect main": target the default branch; restrict deletions, block force pushes, require linear history, require a pull request (0 approvals, since you're a solo maintainer), require conversation resolution
- [ ] 3.2 Merge options: disable merge commits; allow rebase merge (squash optional); automatically delete head branches
- [ ] 3.3 Enable private vulnerability reporting
- [ ] 3.4 `SECURITY.md`, `.github/CODEOWNERS`, `.github/pull_request_template.md`, merged through a PR
- [ ] 3.5 `scripts/check-repo-baseline.sh` passes

## 4. Docs
- [ ] 4.1 `SECURITY.md` is itself the doc; link it from `README.md`
