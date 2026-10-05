"""Tests for scripts/check_docs.py. Run with: python3 -m unittest discover tests"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_docs  # noqa: E402

LOG = """# Decisions

## 2026-03-02 — Third
## 2026-01-12 (b) — Second on a date
## 2026-01-12 — First on a date
"""


class DecisionIds(unittest.TestCase):
    def test_bare_date_counts_as_a(self):
        self.assertIn("2026-01-12 (a)", check_docs.decision_ids(LOG))

    def test_no_duplicates_in_a_clean_log(self):
        self.assertEqual(check_docs.duplicate_ids(LOG), [])

    def test_bare_date_and_explicit_a_collide(self):
        log = LOG + "## 2026-01-12 (a) — Same id, spelled differently\n"
        self.assertEqual(check_docs.duplicate_ids(log), ["2026-01-12 (a)"])

    def test_next_id_on_a_new_date_is_the_bare_date(self):
        self.assertEqual(check_docs.next_id(LOG, "2026-04-01"), "2026-04-01")

    def test_next_id_skips_used_letters(self):
        self.assertEqual(check_docs.next_id(LOG, "2026-01-12"), "2026-01-12 (c)")

    def test_headings_inside_text_are_not_ids(self):
        self.assertEqual(check_docs.decision_ids("Not a heading: ## 2026-01-01 — x"), [])


class RulesBudget(unittest.TestCase):
    def test_flags_a_file_over_budget(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "AGENTS.md"
            f.write_text("x" * 101)
            self.assertEqual(len(check_docs.oversized_rules([f], budget=100)), 1)

    def test_missing_file_is_not_an_error(self):
        self.assertEqual(check_docs.oversized_rules([Path("/nonexistent/AGENTS.md")], budget=1), [])


class RealRepository(unittest.TestCase):
    def test_the_repository_itself_passes(self):
        self.assertEqual(check_docs.main([]), 0)


if __name__ == "__main__":
    unittest.main()
