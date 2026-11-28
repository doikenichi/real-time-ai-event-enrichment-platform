# Answer sheet: Day 001, Challenge C (protect `main`)

## The settings
- **Ruleset** "Protect main": Active; target: default branch; rules: restrict deletions, require linear history, require a pull request (0 approvals, conversation resolution required), block force pushes.
- **General → Pull Requests:** merge commits off, rebase merging on, squash optional (off keeps every TDD commit), "Automatically delete head branches" on.
- **Advanced Security:** private vulnerability reporting on; secret scanning push protection on.

As code (drill C), `.github/rulesets/protect-main.json`, applied with one command instead of the ruleset screen:
```json
{
  "name": "Protect main",
  "target": "branch",
  "enforcement": "active",
  "conditions": { "ref_name": { "include": ["~DEFAULT_BRANCH"], "exclude": [] } },
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    { "type": "required_linear_history" },
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": false,
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_review_thread_resolution": true
      }
    }
  ]
}
```
Apply it: `gh api repos/doikenichi/real-time-ai-event-enrichment-platform/rulesets --method POST --input .github/rulesets/protect-main.json`.

## The files
`SECURITY.md`:
```markdown
# Security policy

## Supported versions
Only the latest `main` gets security fixes.

## Reporting a vulnerability
Please don't open a public issue. Use **Security → Report a vulnerability** on this repository
(private vulnerability reporting). Include what you found, how to reproduce it, and its impact.

You'll get an answer within 7 days. Fixed issues are published as GitHub security advisories,
with credit if you want it.
```
`.github/CODEOWNERS`:
```
* @doikenichi
```
`.github/pull_request_template.md`:
```markdown
## What changed and why

## Checklist
- [ ] The OpenSpec change is updated, and `openspec validate --strict` passes
- [ ] Tests were written first and named after the scenarios (red → green commits)
- [ ] Lint, format and type checks pass
- [ ] Docs, diagrams or contracts are updated
- [ ] No secrets, no personal data, no copyrighted material
```
And the spec requirement (in `repository-governance/spec.md`):
```markdown
### Requirement: Pull request checklist
Every pull request SHALL confirm the spec, test-first commits, quality checks, docs and the security checklist.

#### Scenario: a new pull request shows the checklist
- **GIVEN** the default branch has `.github/pull_request_template.md`
- **WHEN** a pull request is opened
- **THEN** its description starts from the template's checklist
```

## Why this way
- **Rulesets** over classic branch protection: they layer, can target many branches, can be exported as JSON (**policy as code**), and anyone with read access can see them.
- **0 approvals:** a solo maintainer can't approve their own PR; the PR is still required, so CI and the checklist run on every change.
- **Rebase merges:** keep a linear history *and* each red, green and refactor commit, which the pace report and reviews use.

## Common mistakes
- Creating a classic branch protection rule instead of a ruleset: the script reads rulesets (`rules/branches`), so it stays red.
- `CODEOWNERS` in the wrong place or with an extension: it must be `.github/CODEOWNERS`, `CODEOWNERS` or `docs/CODEOWNERS`, with no extension.
- Running the check before merging: the file checks read `main`.

## Check yourself
1. What's the difference between a ruleset and a classic branch protection rule?
2. Why keep the ruleset JSON in the repo if it's already set in GitHub?
3. What does "require conversation resolution" protect against?
