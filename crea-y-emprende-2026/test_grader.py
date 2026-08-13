import csv
import tempfile
import unittest
from pathlib import Path

from grader import EXPECTED_SECTION_MAX, consolidate, load_rubric, parse_score


HERE = Path(__file__).parent
RUBRIC = HERE / "crea_y_emprende_2026_category_b_rubric.csv"
SCORES = HERE / "synthetic_jury_scores.csv"


class CreaYEmprendeTests(unittest.TestCase):
    def test_official_category_b_limits(self):
        rubric = load_rubric(RUBRIC)
        maxima = {
            section: sum(int(item["max_score"]) for item in rubric if item["section"] == section)
            for section in EXPECTED_SECTION_MAX
        }
        self.assertEqual(maxima, {"project": 28, "portfolio": 48, "expo": 20})
        self.assertEqual(len(rubric), 24)

    def test_score_boundaries_and_non_integers(self):
        self.assertEqual(parse_score("1", "p1"), 1)
        self.assertEqual(parse_score("4", "p1"), 4)
        for invalid in ("0", "5", "2.5", "no aplica", ""):
            with self.assertRaises(ValueError):
                parse_score(invalid, "p1")

    def test_three_human_jurors_and_96_maximum(self):
        results = consolidate(SCORES, RUBRIC)
        self.assertEqual(len(results), 3)
        self.assertTrue(all(row["jurors"] == 3 for row in results))
        self.assertTrue(all(24 <= float(row["total_avg_of_96"]) <= 96 for row in results))
        self.assertTrue(all(row["decision"] == "JURADO HUMANO" for row in results))

    def test_duplicate_juror_is_rejected(self):
        with SCORES.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
            fields = list(rows[0])
        rows[1]["juror"] = "J1"
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaisesRegex(ValueError, "exactamente J1, J2 y J3"):
                consolidate(path, RUBRIC)


if __name__ == "__main__":
    unittest.main()
