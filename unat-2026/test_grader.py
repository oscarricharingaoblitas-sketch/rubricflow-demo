import unittest
from pathlib import Path

from grader import grade, load_rubric, published_band, supports_signal


class UnatSampleTests(unittest.TestCase):
    def setUp(self):
        self.rubric = load_rubric(Path("unat_2026_rubric.csv"))

    def test_official_weights_total_100(self):
        self.assertEqual([item["max_points"] for item in self.rubric], [20, 25, 20, 15, 15, 5])
        self.assertEqual(sum(item["max_points"] for item in self.rubric), 100)

    def test_published_bands(self):
        self.assertEqual(published_band(80), ("Excelente", "SELECCIONADO"))
        self.assertEqual(published_band(70), ("Bueno", "SELECCIONADO (lista de espera)"))
        self.assertEqual(published_band(60), ("Regular", "DESAPROBADO"))
        self.assertEqual(published_band(59.99), ("Deficiente", "DESCALIFICADO"))

    def test_negated_evidence_is_rejected(self):
        self.assertFalse(supports_signal("No incluye cronograma ni presupuesto.", "cronograma"))
        self.assertFalse(supports_signal("Carece de metodologia y viabilidad tecnica.", "metodologia"))
        self.assertFalse(supports_signal("El asesor no tiene CTI Vitae ni ORCID.", "ORCID"))

    def test_positive_evidence_is_accent_insensitive(self):
        self.assertTrue(supports_signal("La metodología es viable.", "metodologia"))

    def test_weak_case_scores_zero(self):
        text = (
            "No se alinea con una linea de investigacion de la UNAT ni atiende una problematica regional de Huancavelica. "
            "Carece de problema, objetivo, hipotesis, metodologia y viabilidad tecnica. "
            "No incluye cronograma ni presupuesto. El asesor no tiene CTI Vitae ni ORCID. "
            "No demuestra aplicabilidad o desarrollo cientifico. La documentacion no esta completa ni foliada."
        )
        result = grade(text, self.rubric)
        self.assertEqual(result["total_points"], 0)
        self.assertEqual(result["human_review_required"], "YES")


if __name__ == "__main__":
    unittest.main()
