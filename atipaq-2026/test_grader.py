Exit code: 0
Wall time: 0.6 seconds
Output:
import unittest
from pathlib import Path

from grader import grade, load_rubric, supports_signal


class AtipaqSampleTests(unittest.TestCase):
    def setUp(self):
        self.rubric = load_rubric(Path("atipaq_2026_rubric.csv"))

    def test_published_weights_total_100(self):
        self.assertEqual(sum(item["max_points"] for item in self.rubric), 100)

    def test_negated_evidence_is_rejected(self):
        self.assertFalse(supports_signal("No tenemos usuarios activos.", "usuarios activos"))
        self.assertFalse(supports_signal("Carecemos de una ventaja competitiva.", "ventaja competitiva"))
        sentence = "Tampoco contamos con un plan, presupuesto, experiencia o perfiles complementarios."
        self.assertFalse(supports_signal(sentence, "presupuesto"))
        self.assertFalse(supports_signal(sentence, "experiencia"))
        self.assertFalse(supports_signal(sentence, "perfiles complementarios"))

    def test_positive_evidence_is_accepted_without_accents(self):
        self.assertTrue(supports_signal("Existe innovacion y tecnologia propietaria.", "innovaciÃ³n"))
        self.assertTrue(supports_signal("Existe innovacion y tecnologia propietaria.", "tecnologÃ­a"))

    def test_weak_case_does_not_meet_thresholds(self):
        result = grade(
            "No tenemos usuarios activos ni ventas. Carecemos de una ventaja competitiva. "
            "No existe tecnologÃ­a propietaria. Tampoco contamos con un plan de ejecuciÃ³n, "
            "presupuesto, experiencia o perfiles complementarios.",
            self.rubric,
        )
        self.assertEqual(result["total_points"], 0)
        self.assertEqual(result["reference_check"], "human_review_required")


if __name__ == "__main__":
    unittest.main()

