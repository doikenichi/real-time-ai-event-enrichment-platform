# Answer sheet: Day 001, drill C (predict the checks)

## The answer
| Check | Setting or file | API path | Fresh repo | Risk if missing |
|---|---|---|---|---|
| ruleset requires a pull request | ruleset rule `pull_request` | `repos/{repo}/rules/branches/main` | FAIL | changes skip review and CI |
| ruleset blocks force pushes | ruleset rule `non_fast_forward` | same | FAIL | reviewed history can be rewritten or erased |
| ruleset blocks deletion | ruleset rule `deletion` | same | FAIL | `main` can be deleted by mistake |
| ruleset requires linear history | ruleset rule `required_linear_history` | same | FAIL | merge commits hide the red/green steps |
| rebase merge is allowed | repo setting `allow_rebase_merge` | `repos/{repo}` | PASS (on by default) | TDD commits get squashed away |
| merge commits are disabled | repo setting `allow_merge_commit` | `repos/{repo}` | FAIL (on by default) | non-linear history |
| head branches are deleted after merge | `delete_branch_on_merge` | `repos/{repo}` | FAIL (off by default) | stale branches pile up |
| private vulnerability reporting | security setting | `repos/{repo}/private-vulnerability-reporting` | FAIL | reporters open public issues, exposing the bug |
| push protection | `security_and_analysis.secret_scanning_push_protection` | `repos/{repo}` | PASS (GitHub turns it on for public repos) | a pushed secret becomes public |
| `SECURITY.md`, `CODEOWNERS`, PR template exist | files on `main` | `repos/{repo}/contents/<path>?ref=main` | FAIL | no reporting policy, no owner review, no checklist |

On this repository today: **2 pass, 10 fail**, matching the table.

## Why it matters
Reading the check first is the same habit as reading a failing test first: you know exactly what "done" means before touching anything. The script is an **acceptance test for configuration**, and it can run in CI on a schedule to catch **configuration drift** (someone changing a setting by hand).

## Common mistakes
- Expecting the three file checks to pass after creating the files on your branch: they read `main`, so they pass only after the PR is merged.
- Thinking "rebase allowed" means "merge commits disabled": they're separate settings.

## Check yourself
1. Why do the file checks use `?ref=main`?
2. Which two checks are already green on a new public repo, and why?
