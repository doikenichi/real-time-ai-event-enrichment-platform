# Practice drill C: the ruleset as code (≈15 min at your pace)

Warm-up for Challenge C, and a real piece of the repo: the `main` protection rules written as a JSON file (**policy as code**). In Challenge C you apply this file with one command instead of clicking through the ruleset screen, and the file stays in git as the record of the rules.

**Concepts:** branch protection rules (the same as in the challenge), and reading an API's JSON format from its docs.
**Answer sheet:** `lab answer drill-c`, after you've tried.

## 1. Read the test first (3 min)
Open `scripts/check-repo-baseline.sh` and find the four ruleset checks. Note the four rule **types** they look for. Then open `challenges/day-001/check-drill-c.sh`: it's this drill's test.

Run `bash challenges/day-001/check-drill-c.sh`. **Expected:** `FAIL .github/rulesets/protect-main.json doesn't exist yet`.

## 2. Your turn: write the file (10 min)
Create `.github/rulesets/protect-main.json`. Use GitHub's REST API docs for creating a repository ruleset ([Create a repository ruleset](https://docs.github.com/en/rest/repos/rules#create-a-repository-ruleset)): the request body is exactly this file. It needs:
- a `name`, `"target": "branch"` and `"enforcement": "active"`
- `conditions.ref_name.include` with the special value for the default branch (search the docs page for `~DEFAULT_BRANCH`)
- `rules`: the four types from step 1. The `pull_request` rule needs `parameters`; set 0 required approvals and require conversations to be resolved. The docs list the other parameters it needs.

**Done when:** `bash challenges/day-001/check-drill-c.sh` → `All drill checks passed.` **Commit:** `lab save "main protection ruleset as code"`

## How Challenge C uses it
In `guide-c.md`, step 2, apply the file with `gh api` instead of the ruleset screen.
