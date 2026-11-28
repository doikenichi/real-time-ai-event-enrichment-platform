# Add the repository security baseline

## Why
The default branch is the source of truth for the platform. Before any code lands, changes must be reviewable and traceable, history must be protected, and vulnerabilities must have a private reporting path. This matches the branch-protection, security-policy and code-review expectations in common baselines such as the OpenSSF Scorecard.

## What changes
- A ruleset on the default branch: pull requests only, linear history, no force pushes, no deletion
- No merge commits; rebase merge allowed (keeps each TDD commit); head branches deleted after merge
- Private vulnerability reporting enabled; `SECURITY.md`
- `.github/CODEOWNERS` and a PR template with a spec/test/docs/security checklist
- `scripts/check-repo-baseline.sh` as the automated test for the baseline

## Impact
- New capability: `repository-governance`
- Settings: repository rulesets, merge options, security settings
