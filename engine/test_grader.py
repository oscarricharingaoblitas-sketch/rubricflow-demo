import tempfile
import unittest
import csv
from pathlib import Path

from grader import grade, grade_csv


STRONG = (
    "The problem currently affects 12,000 rural students because transport delays access. "
    "Our unique solution uses an offline-first workflow unlike existing tools. "
    "We launched an MVP, tested a pilot with 240 users, and earned $8,000 revenue. "
    "Target beneficiaries are rural schools; we secured grant funding and met two investors. "
    "A university partner recognised the impact, and our next market milestone is scalable rollout."
)


class GraderTests(unittest.TestCase):
    def test_strong_application_scores_higher(self):
        self.assertGreater(grade(STRONG)["overall_score"], grade("We have an idea.")["overall_score"])

    def test_all_criteria_are_reported(self):
        result = grade(STRONG)
        self.assertEqual(5, len(result["criteria"]))
        self.assertTrue(all("evidence" in item for item in result["criteria"].values()))

    def test_csv_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.csv"
            target = Path(directory) / "output.csv"
            source.write_text('id,application\n1,"We launched a pilot with 20 users."\n', encoding="utf-8")
            grade_csv(source, target)
            with target.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(1, len(rows))
            self.assertIn("overall_score", rows[0])
            self.assertIn("development_stage_evidence", rows[0])
            self.assertIn("pilot", rows[0]["development_stage_evidence"].lower())
            self.assertIn("human_review", rows[0])


if __name__ == "__main__":
    unittest.main()
