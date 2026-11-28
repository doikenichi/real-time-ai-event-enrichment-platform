"""Run with: python3 -m unittest discover -s scripts/tests"""

import sys
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pace_report import LEAD_IN_MIN, Commit, challenge_of, cycle_minutes, logged_minutes, report, sessions  # noqa: E402

T0 = datetime(2026, 11, 28, 5, 0, tzinfo=UTC)


def commit(minutes: int, *files: str, author: str = "Ken Doi", message: str = "day-001: x") -> Commit:
    return Commit("abc1234", author, T0 + timedelta(minutes=minutes), message, list(files))


class PaceReportTests(unittest.TestCase):
    def test_a_long_gap_starts_a_new_session(self) -> None:
        groups = sessions([commit(0, "a"), commit(20, "b"), commit(120, "c")])
        self.assertEqual([len(g) for g in groups], [2, 1])

    def test_active_minutes_add_a_lead_in_per_session(self) -> None:
        data = report([commit(0, "services/x.py"), commit(30, "services/y.py"), commit(200, "web/z.tsx")])
        self.assertEqual(data["active_minutes"], 30 + LEAD_IN_MIN + LEAD_IN_MIN)

    def test_mentor_commits_are_ignored(self) -> None:
        data = report([commit(0, "services/x.py"), commit(5, "AGENTS.md", author="Claude")])
        self.assertEqual(data["learner_commits"], 1)

    def test_code_paths_decide_the_challenge_over_docs_and_lock_files(self) -> None:
        self.assertEqual(challenge_of(commit(0, "uv.lock", "docs/a.md", "services/ingest-api/src/app.py")), "A")

    def test_a_test_only_commit_counts_as_a_red_step(self) -> None:
        data = report([commit(0, "services/ingest-api/tests/test_health.py")])
        self.assertEqual(data["tdd"]["test_only_commits"], 1)

    def test_messages_without_the_day_prefix_are_reported(self) -> None:
        data = report([commit(0, "docs/adr/x.md", message="added doc")], day_prefix="day-001:")
        self.assertEqual(data["friction"]["messages_without_day_prefix"], ["added doc"])

    def test_the_timer_log_adds_up_closed_sessions(self) -> None:
        log = "start 2026-11-28T05:00:00Z\nstop 2026-11-28T05:40:00Z\nstart 2026-11-28T06:00:00Z\nstop 2026-11-28T06:20:00Z\n"
        self.assertEqual(logged_minutes(log), 60.0)

    def test_cycle_time_is_the_median_gap_within_sessions(self) -> None:
        commits = [commit(0, "a"), commit(10, "b"), commit(40, "c"), commit(300, "d")]
        self.assertEqual(cycle_minutes(commits), 20.0)


if __name__ == "__main__":
    unittest.main()
