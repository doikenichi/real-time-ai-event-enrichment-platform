#!/usr/bin/env bash
# Day 001 · Challenge C: an automated test for the repository-governance spec.
#
# RED until the repo security baseline is configured. Run it with:
#   scripts/check-repo-baseline.sh [owner/repo]
# Needs the GitHub CLI (`gh auth login`) with admin access to the repo.
set -uo pipefail

REPO="${1:-$(gh repo view --json nameWithOwner --jq .nameWithOwner)}"
failures=0

pass() { printf '  \033[32mPASS\033[0m %s\n' "$1"; }
fail() { printf '  \033[31mFAIL\033[0m %s\n' "$1"; failures=$((failures + 1)); }
check() { if [ "$2" = "true" ]; then pass "$1"; else fail "$1"; fi; }

echo "Repository security baseline for $REPO"

# Scenario: the default branch only changes through pull requests
default_branch=$(gh api "repos/$REPO" --jq .default_branch)
rules=$(gh api "repos/$REPO/rules/branches/$default_branch" --jq '[.[].type] | join(",")' 2>/dev/null || echo "")
has_rule() { case ",$rules," in *",$1,"*) echo true ;; *) echo false ;; esac; }
check "ruleset on '$default_branch' requires a pull request" "$(has_rule pull_request)"
check "ruleset on '$default_branch' blocks force pushes" "$(has_rule non_fast_forward)"
check "ruleset on '$default_branch' blocks deletion" "$(has_rule deletion)"
check "ruleset on '$default_branch' requires linear history" "$(has_rule required_linear_history)"

# Scenario: history stays linear, TDD commits are preserved, branches are cleaned up
repo_json=$(gh api "repos/$REPO")
check "rebase merge is allowed (keeps red/green commits)" "$(jq -r '.allow_rebase_merge' <<<"$repo_json")"
check "merge commits are disabled" "$(jq -r '(.allow_merge_commit | not)' <<<"$repo_json")"
check "head branches are deleted after merge" "$(jq -r '.delete_branch_on_merge' <<<"$repo_json")"

# Scenario: vulnerabilities can be reported privately
check "private vulnerability reporting is enabled" \
  "$(gh api "repos/$REPO/private-vulnerability-reporting" --jq .enabled 2>/dev/null || echo false)"
check "secret scanning push protection is enabled" \
  "$(jq -r '.security_and_analysis.secret_scanning_push_protection.status == "enabled"' <<<"$repo_json")"

# Scenario: governance files exist on the default branch
for path in SECURITY.md .github/CODEOWNERS .github/pull_request_template.md; do
  if gh api "repos/$REPO/contents/$path?ref=$default_branch" --silent 2>/dev/null; then
    pass "$path exists"
  else
    fail "$path exists"
  fi
done

if [ "$failures" -gt 0 ]; then
  echo "$failures check(s) failed."
  exit 1
fi
echo "All checks passed."
