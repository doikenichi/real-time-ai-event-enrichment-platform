# Practice drill C: predict the checks (≈10 min at your pace)

Warm-up for Challenge C. You already know testing, so this drill practises reading a check before changing anything: the same habit as reading a failing test first.

**Answer sheet:** `lab answer drill-c`, after you've written your predictions.

## 1. Read the test (3 min)
Open `scripts/check-repo-baseline.sh`. Each `check "…"` line is one assertion. For each one, write down in `practice/drill-c.md` (git-ignored; create the folder at the repo root):
- **which GitHub setting or file** it looks at
- **the API path** it calls (the text after `gh api`)

## 2. Predict, then run (4 min)
Before running anything, predict: which checks **pass today**, and which fail? Write PASS or FAIL next to each. Then run:
```bash
scripts/check-repo-baseline.sh
```
Compare. For each wrong prediction, write one sentence on why.

## 3. Map each check to a risk (3 min)
For each check, one line: **what could go wrong** if this setting were missing. For example: "without blocking force pushes, someone could rewrite `main` and erase reviewed history".

**Done when:** `practice/drill-c.md` has, for every check, its setting, API path, prediction, result and risk.
