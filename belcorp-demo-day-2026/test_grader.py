import unittest
from pathlib import Path

from grader import analyze, load_criteria, supports_signal


class BelcorpDemoDayTests(unittest.TestCase):
    def setUp(self):
        self.criteria = load_criteria(Path("belcorp_demo_day_criteria.csv"))

    def test_five_published_criteria_without_weights(self):
        self.assertEqual(len(self.criteria), 5)
        self.assertFalse(any("weight" in item for item in self.criteria))

    def test_negated_evidence_is_rejected(self):
        self.assertFalse(supports_signal("No existe sostenibilidad operativa.", "sostenibilidad operativa"))
        self.assertFalse(supports_signal("Carece de una vision de crecimiento.", "vision de crecimiento"))

    def test_accents_are_ignored(self):
        self.assertTrue(supports_signal("Existe una visión de crecimiento clara.", "vision de crecimiento"))

    def test_attendance_must_be_strictly_over_85(self):
        row = {
            "attendance_percent": "85",
            "initial_form_completed": "yes",
            "exit_form_completed": "yes",
            "presentation": "Modelo de negocio.",
        }
        self.assertEqual(analyze(row, self.criteria)["published_conditions_met"], "NO")
        row["attendance_percent"] = "85.1"
        self.assertEqual(analyze(row, self.criteria)["published_conditions_met"], "YES")

    def test_jury_score_is_always_required(self):
        row = {
            "attendance_percent": "100",
            "initial_form_completed": "yes",
            "exit_form_completed": "yes",
            "presentation": "Modelo de negocio, crecimiento, liderazgo, compromiso y pitch.",
        }
        result = analyze(row, self.criteria)
        self.assertEqual(result["official_jury_score_required"], "YES")
        self.assertIn("not an official score", result["warning"])


if __name__ == "__main__":
    unittest.main()
