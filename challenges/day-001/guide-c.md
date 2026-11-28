# Guide for Challenge C: protect `main`, step by step

Level 2 (supported): you know testing, so this guide gives the steps, a check after each, and hints, without long explanations. About 30–40 minutes the first time, mostly clicking through GitHub settings.

**Fast path**
1. `scripts/check-repo-baseline.sh`: 10 red checks. That script is the test.
2. Do drill C (the ruleset as JSON), apply it with `gh api`, then set rebase merges only and private vulnerability reporting.
3. Add `SECURITY.md`, `.github/CODEOWNERS` and `.github/pull_request_template.md`.
4. `lab finish`, then merge the PR with **Rebase and merge**.
5. `scripts/check-repo-baseline.sh`: all green.

---

## Step 1: Spec and red (5 min)
**Why:** the script checks the spec's scenarios against the real repository, like an acceptance test for configuration.

1. Read `openspec/changes/add-repository-security-baseline/specs/repository-governance/spec.md`.
2. Add a requirement for what every PR must confirm. Pick 3 or 4 checklist items, for example "tests written first", "docs updated", "no secrets". Copy the shape of an existing requirement and scenario.
3. Run:
   ```bash
   openspec validate add-repository-security-baseline --strict
   scripts/check-repo-baseline.sh
   ```
**Expected:** the spec is valid, and the script prints **10 failing checks**.

**Commit:** `lab save "governance spec and failing baseline check"`

<details><summary>Hint: the script says gh isn't logged in, or lacks permission</summary>Run <code>gh auth login</code> and choose your account. The checks read admin settings, so the account must own the repo.</details>

## Step 2: The ruleset (10 min)
**Why:** a ruleset makes the rules about `main` enforced by GitHub, not just agreed.

**Did drill C?** Apply your file instead of clicking (2 min):
```bash
gh api repos/doikenichi/real-time-ai-event-enrichment-platform/rulesets --method POST \
  --input .github/rulesets/protect-main.json
```
Then check the ruleset appears under **Settings → Rules → Rulesets**, and skip to the **Check** below. (To change it later: `gh api .../rulesets` to find its `id`, then `--method PUT` on `.../rulesets/<id>`.)

**Otherwise, by hand:** On github.com, in the repository: **Settings → Rules → Rulesets → New ruleset → New branch ruleset**.
- **Name:** `Protect main`. **Enforcement status:** Active.
- **Target branches:** Add target → **Include default branch**.
- **Rules**, tick:
  - Restrict deletions
  - Require linear history
  - Require a pull request before merging (required approvals: **0**; tick "Require conversation resolution before merging")
  - Block force pushes
- **Create.**

**Check:** run `scripts/check-repo-baseline.sh`. The four "ruleset" lines are now PASS.

<details><summary>Hint: why 0 approvals?</summary>You're the only person on the repo, and GitHub doesn't let you approve your own PR. The PR is still required, so every change gets a reviewable record and the checks can run on it.</details>

## Step 3: Merge settings and private reporting (5 min)
1. **Settings → General → Pull Requests:**
   - untick **Allow merge commits**
   - keep **Allow rebase merging** ticked (it keeps your red and green commits)
   - tick **Automatically delete head branches**
2. **Settings → Advanced Security** (it may be called "Code security"): **Private vulnerability reporting → Enable**. Check that **Push protection** for secret scanning is enabled too.

**Check:** the script now passes everything except the three files.

## Step 4: The governance files (10 min)
Create these on your branch. Short is fine.

| File | What goes in it |
|---|---|
| `SECURITY.md` | which versions get fixes (for now: `main`), how to report privately (the "Report a vulnerability" button on the Security tab, never a public issue), and when you'll answer (for example, within 7 days) |
| `.github/CODEOWNERS` | one line: `* @doikenichi` (you own every file, so you're asked to review every PR) |
| `.github/pull_request_template.md` | the checklist from your spec in step 1, as `- [ ]` items |

Add a link to `SECURITY.md` in the main `README.md`.

**Commit:** `lab save "security policy, code owners and PR template"`

## Step 5: Merge through a PR, and see green (5 min)
```bash
lab finish        # pushes your branch and opens the PR (or shows it)
```
On the PR page, notice the checklist from your template. Merge with **Rebase and merge** (the other buttons should be gone or disabled now).

Then:
```bash
git switch main && git pull
scripts/check-repo-baseline.sh
```
**Expected:** `All checks passed.` The file checks look at `main`, so they only pass after the merge.

<details><summary>Hint: still failing after the merge?</summary>Read which line fails. Each line names the exact setting or file. For a file, check its path and name: <code>.github/CODEOWNERS</code> has no extension.</details>

---

## Glossary
| Term | Meaning |
|---|---|
| **ruleset** | rules GitHub enforces on branches, for example "only through PRs" |
| **linear history** | no merge commits: history is one straight line of commits |
| **rebase merge** | puts your PR's commits on top of `main` one by one, so each TDD step stays visible |
| **force push** | overwriting a branch's history; blocked on `main` so history can't be rewritten |
| **CODEOWNERS** | who is asked to review changes to which files |
| **private vulnerability reporting** | a confidential way for anyone to report a security problem |

## Learn more (optional)
- [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [OpenSSF Scorecard checks](https://github.com/ossf/scorecard/blob/main/docs/checks.md): branch protection, security policy and code review are scored checks
