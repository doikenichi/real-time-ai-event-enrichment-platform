# Answer sheet: Day 001, drill C (the ruleset as code)

> Verified: this file passes `bash challenges/day-001/check-drill-c.sh`.

## The answer
`.github/rulesets/protect-main.json`:
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

## Line by line
- `"target": "branch"`: the ruleset applies to branches (rulesets can also target tags).
- `"enforcement": "active"`: enforced now. `"evaluate"` (on some plans) only reports what would be blocked; `"disabled"` turns it off.
- `"~DEFAULT_BRANCH"`: a special value meaning "whatever the default branch is", so renaming `main` doesn't break the protection.
- `deletion`: nobody can delete the branch.
- `non_fast_forward`: blocks **force pushes** (pushes that rewrite history).
- `required_linear_history`: no merge commits on `main`.
- `pull_request`: changes only arrive through PRs. `required_review_thread_resolution: true` means every review comment must be resolved before merging. 0 approvals, because you can't approve your own PR when you're the only maintainer.

## Why this way
- **Policy as code:** the rules live in git next to the code, are reviewed in PRs, and can be re-applied to a new repo with one command. Clicking through settings leaves no record of why a rule exists.
- **Rulesets** rather than classic branch protection: they layer (several rulesets can apply), can be exported and imported as JSON, and anyone with read access can see them.
- Applying: `gh api repos/<owner>/<repo>/rulesets --method POST --input .github/rulesets/protect-main.json` creates it; `--method PUT` on `.../rulesets/<id>` updates it. Tools such as Terraform's GitHub provider or Probot settings do the same at scale.

## Common mistakes
- `"include": ["main"]`: works, but `"refs/heads/main"` or `"~DEFAULT_BRANCH"` is the documented form; plain `main` may not match.
- Leaving out the `pull_request` parameters: the API rejects the request; all five are required.
- Running POST twice: you get two rulesets. Use PUT to update.

## Check yourself
1. What's the difference between `non_fast_forward` and `required_linear_history`?
2. Why is a JSON file in git better than clicking, even for a one-person repo?
