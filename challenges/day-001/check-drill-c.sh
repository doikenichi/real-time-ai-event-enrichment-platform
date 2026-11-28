#!/usr/bin/env bash
# Day 001 · drill C check: is .github/rulesets/protect-main.json a ruleset for the default branch
# with the four rules the baseline needs? Run: bash challenges/day-001/check-drill-c.sh
set -uo pipefail
file=".github/rulesets/protect-main.json"
cd "$(git rev-parse --show-toplevel)"
[ -f "$file" ] || { echo "FAIL $file doesn't exist yet"; exit 1; }
jq empty "$file" 2>/dev/null || { echo "FAIL $file isn't valid JSON"; exit 1; }
failures=0
expect() { if [ "$(jq -r "$2" "$file")" = "true" ]; then echo "PASS $1"; else echo "FAIL $1"; failures=$((failures + 1)); fi; }
expect "it's a branch ruleset" '.target == "branch"'
expect "it's active" '.enforcement == "active"'
expect "it targets the default branch" '(.conditions.ref_name.include // []) | index("~DEFAULT_BRANCH") != null'
for rule in pull_request non_fast_forward deletion required_linear_history; do
  expect "it has the $rule rule" "[.rules[].type] | index(\"$rule\") != null"
done
expect "pull requests need 0 approvals (solo repo)" '[.rules[] | select(.type == "pull_request") | .parameters.required_approving_review_count] == [0]'
[ "$failures" -eq 0 ] && echo "All drill checks passed." || { echo "$failures check(s) failed."; exit 1; }
