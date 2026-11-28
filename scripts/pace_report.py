#!/usr/bin/env python3
"""Pace report: measures how a day's work actually went, from the commits of its PR.

Used by the mentor in each review to calibrate the size of the next day's challenges
(docs/learning/README.md, "Feedback and pace"). Standard library only; needs the gh CLI.

    python3 scripts/pace_report.py --pr 13              # Markdown report
    python3 scripts/pace_report.py --pr 13 --json       # JSON for .lab/pace.json
    python3 scripts/pace_report.py --pr 4 --pr 13       # a day split over two PRs

What it measures (commit timestamps are evidence, not the whole truth: reading,
thinking and setup before the first commit are invisible, so the learner's own
FEEDBACK.md always wins when the two disagree):
- active minutes: commits are grouped into sessions (a gap over SESSION_GAP_MIN starts
  a new one); each session counts last - first + LEAD_IN_MIN for the work before its
  first commit
- minutes and commits per challenge, from the paths each commit touches
- TDD signals: test-only commits (red steps), code commits without tests
- the timer: if `scripts/lab` wrote challenges/day-NNN/sessions.log, its total minutes
  (the most accurate number, after the learner's own FEEDBACK.md)
- cycle time: the median minutes between commits in a session; it falls as TDD gets routine
- friction signals: learner edits to challenge files (often a fix to unclear or wrong
  instructions), commits fixing lint or types, commit messages without the day prefix
"""

from __future__ import annotations

import argparse
import statistics
from pathlib import Path
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime

REPO = "doikenichi/real-time-ai-event-enrichment-platform"
SESSION_GAP_MIN = 45
LEAD_IN_MIN = 15
MENTOR_NAMES = {"Claude", "claude[bot]", "github-actions[bot]"}

# First matching prefix wins. Paths that match nothing count as "other".
CHALLENGE_PATHS: list[tuple[str, str]] = [
    ("services/", "A"),
    ("packages/py", "A"),
    ("web/", "B"),
    ("packages/ts", "B"),
    (".github/", "C"),
    (".circleci/", "C"),
    ("infra/", "C"),
    ("scripts/check-repo-baseline", "C"),
    ("SECURITY.md", "C"),
    ("CODEOWNERS", "C"),
    ("docs/", "docs"),
    ("openspec/", "spec"),
    ("challenges/", "challenge-files"),
]
TEST_PATH = re.compile(r"(^|/)(tests?|__tests__)/|(_test|\.test|\.spec)\.[a-z]+$|(^|/)test_[^/]+$")
LOCK_FILES = {"uv.lock", "pnpm-lock.yaml"}


@dataclass
class Commit:
    sha: str
    author: str
    when: datetime
    message: str
    files: list[str] = field(default_factory=list)


def classify(path: str) -> str:
    for prefix, challenge in CHALLENGE_PATHS:
        if path.startswith(prefix) or path == prefix:
            return challenge
    return "other"


def challenge_of(commit: Commit) -> str:
    """The challenge a commit mostly belongs to (ignoring lock files)."""
    counts: dict[str, int] = {}
    for path in commit.files:
        if path.rsplit("/", 1)[-1] in LOCK_FILES:
            continue
        key = classify(path)
        counts[key] = counts.get(key, 0) + 1
    if not counts:
        return "other"
    for preferred in ("A", "B", "C"):  # code beats docs and challenge files
        if preferred in counts:
            return preferred
    return max(counts, key=lambda k: counts[k])


def sessions(commits: list[Commit], gap_min: int = SESSION_GAP_MIN) -> list[list[Commit]]:
    ordered = sorted(commits, key=lambda c: c.when)
    groups: list[list[Commit]] = []
    for commit in ordered:
        if groups and (commit.when - groups[-1][-1].when).total_seconds() <= gap_min * 60:
            groups[-1].append(commit)
        else:
            groups.append([commit])
    return groups


def minutes_by_challenge(commits: list[Commit]) -> dict[str, float]:
    """Each session's time goes to the challenge of the commit that ends each stretch."""
    totals: dict[str, float] = {}
    for group in sessions(commits):
        first = group[0]
        key = challenge_of(first)
        totals[key] = totals.get(key, 0.0) + LEAD_IN_MIN
        for previous, current in zip(group, group[1:]):
            key = challenge_of(current)
            stretch = (current.when - previous.when).total_seconds() / 60
            totals[key] = totals.get(key, 0.0) + stretch
    return {k: round(v, 1) for k, v in totals.items()}


def is_test_only(commit: Commit) -> bool:
    code = [p for p in commit.files if p.rsplit("/", 1)[-1] not in LOCK_FILES]
    return bool(code) and all(TEST_PATH.search(p) for p in code)


def touches_code_without_tests(commit: Commit) -> bool:
    code = [p for p in commit.files if classify(p) in {"A", "B", "C"}]
    return bool(code) and not any(TEST_PATH.search(p) for p in code)


def report(commits: list[Commit], day_prefix: str | None = None) -> dict[str, object]:
    learner = [c for c in commits if c.author not in MENTOR_NAMES]
    groups = sessions(learner)
    active = sum((g[-1].when - g[0].when).total_seconds() / 60 + LEAD_IN_MIN for g in groups)
    per_challenge: dict[str, int] = {}
    for c in learner:
        key = challenge_of(c)
        per_challenge[key] = per_challenge.get(key, 0) + 1
    no_prefix = [
        c.message for c in learner if day_prefix and not c.message.startswith(day_prefix)
    ]
    return {
        "learner_commits": len(learner),
        "sessions": [
            {"start": g[0].when.isoformat(), "end": g[-1].when.isoformat(), "commits": len(g)}
            for g in groups
        ],
        "active_minutes": round(active, 1),
        "median_minutes_between_commits": cycle_minutes(learner),
        "minutes_by_challenge": minutes_by_challenge(learner),
        "commits_by_challenge": per_challenge,
        "tdd": {
            "test_only_commits": sum(is_test_only(c) for c in learner),
            "code_commits_without_tests": sum(touches_code_without_tests(c) for c in learner),
        },
        "friction": {
            "challenge_file_edits": [c.message for c in learner if any(p.startswith("challenges/") for p in c.files)],
            "lint_or_type_fix_commits": sum(bool(re.search(r"lint|ruff|mypy|type|format", c.message, re.I)) for c in learner),
            "messages_without_day_prefix": no_prefix,
        },
    }


def logged_minutes(log_text: str) -> float:
    """Total minutes from a sessions.log written by `scripts/lab` (start/stop lines)."""
    total, start = 0.0, None
    for line in log_text.splitlines():
        kind, _, when = line.partition(" ")
        if not when:
            continue
        moment = datetime.fromisoformat(when.replace("Z", "+00:00"))
        if kind == "start":
            start = moment
        elif kind == "stop" and start is not None:
            total += (moment - start).total_seconds() / 60
            start = None
    return round(total, 1)


def cycle_minutes(commits: list[Commit]) -> float | None:
    """Median minutes between consecutive learner commits in the same session (red, green, refactor...)."""
    gaps = [
        (b.when - a.when).total_seconds() / 60
        for group in sessions(commits)
        for a, b in zip(group, group[1:])
    ]
    return round(statistics.median(gaps), 1) if gaps else None


def gh_json(path: str) -> object:
    out = subprocess.run(["gh", "api", "--paginate", path], check=True, capture_output=True, text=True).stdout
    # --paginate concatenates JSON arrays as "][": join them
    return json.loads("[" + out.strip()[1:-1].replace("]\n[", ",").replace("][", ",") + "]") if out.strip().startswith("[") else json.loads(out)


def load_pr(repo: str, pr: int) -> list[Commit]:
    raw = gh_json(f"repos/{repo}/pulls/{pr}/commits")
    commits: list[Commit] = []
    for item in raw:  # type: ignore[union-attr]
        if len(item.get("parents", [])) > 1:  # merge commits aren't work
            continue
        detail = gh_json(f"repos/{repo}/commits/{item['sha']}")
        commits.append(
            Commit(
                sha=item["sha"][:7],
                author=item["commit"]["author"]["name"],
                when=datetime.fromisoformat(item["commit"]["author"]["date"].replace("Z", "+00:00")),
                message=item["commit"]["message"].splitlines()[0],
                files=[f["filename"] for f in detail.get("files", [])],  # type: ignore[union-attr]
            )
        )
    return commits


def to_markdown(data: dict[str, object]) -> str:
    lines = ["| Measure | Value |", "|---|---|"]
    for key, value in data.items():
        lines.append(f"| {key} | `{json.dumps(value, ensure_ascii=False)}` |")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pr", type=int, action="append", required=True, help="repeat for a day split over several PRs")
    parser.add_argument("--repo", default=REPO)
    parser.add_argument("--day", help="expected commit prefix, for example day-001")
    parser.add_argument("--since", help="ignore commits before this ISO time, for example 2026-11-27T03:20:00+00:00")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    commits = [c for pr in args.pr for c in load_pr(args.repo, pr)]
    if args.since:
        since = datetime.fromisoformat(args.since)
        commits = [c for c in commits if c.when >= since]
    data = report(commits, f"{args.day}:" if args.day else None)
    if args.day:
        log = Path(f"challenges/{args.day}/sessions.log")
        if log.exists():
            data["timer_minutes"] = logged_minutes(log.read_text())
            data["answer_sheets_opened"] = [line.split(" ", 2)[2] for line in log.read_text().splitlines() if line.startswith("answer ")]
    print(json.dumps(data, indent=2, ensure_ascii=False) if args.json else to_markdown(data))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
