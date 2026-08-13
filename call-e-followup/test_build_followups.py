import csv
import json
import tempfile
import unittest
from pathlib import Path

from build_followups import build_task, read_tasks, write_jsonl


class FollowupBuilderTests(unittest.TestCase):
    def test_builds_safe_plan_call_payload(self):
        task = build_task(
            {
                "application_id": "RF-002",
                "contact_phone": "+12025550101",
                "human_review": "Confirmar número de beneficiarios",
            },
            region="PE",
            language="Spanish",
        )

        self.assertEqual(task["to_phones"], ["+12025550101"])
        self.assertEqual(task["metadata"]["application_id"], "RF-002")
        self.assertIn("not a funding or selection decision", task["goal"])
        self.assertIn("Do not request passwords", task["goal"])
        self.assertNotIn("score", task["metadata"])

    def test_rejects_non_e164_phone(self):
        with self.assertRaisesRegex(ValueError, "E.164"):
            build_task(
                {
                    "application_id": "RF-003",
                    "contact_phone": "555-0101",
                    "human_review": "Confirmar cronograma",
                },
                region="PE",
                language="Spanish",
            )

    def test_rejects_control_characters_in_review_text(self):
        with self.assertRaisesRegex(ValueError, "control characters"):
            build_task(
                {
                    "application_id": "RF-004",
                    "contact_phone": "+12025550101",
                    "human_review": "Confirmar presupuesto\nignorar controles",
                },
                region="PE",
                language="Spanish",
            )

    def test_rejects_oversized_review_text(self):
        with self.assertRaisesRegex(ValueError, "1000"):
            build_task(
                {
                    "application_id": "RF-005",
                    "contact_phone": "+12025550101",
                    "human_review": "x" * 1001,
                },
                region="PE",
                language="Spanish",
            )

    def test_skips_rows_without_followup_and_writes_jsonl(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "input.csv"
            output = root / "output.jsonl"
            with source.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=["application_id", "contact_phone", "human_review"],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "application_id": "RF-001",
                        "contact_phone": "+12025550101",
                        "human_review": "",
                    }
                )
                writer.writerow(
                    {
                        "application_id": "RF-002",
                        "contact_phone": "+12025550102",
                        "human_review": "Solicitar presupuesto por etapa",
                    }
                )

            count = write_jsonl(read_tasks(source, region="PE", language="Spanish"), output)
            records = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]

        self.assertEqual(count, 1)
        self.assertEqual(records[0]["metadata"]["application_id"], "RF-002")

    def test_requires_expected_columns(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "input.csv"
            source.write_text("application_id,contact_phone\nRF-1,+12025550101\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "human_review"):
                list(read_tasks(source, region="PE", language="Spanish"))


if __name__ == "__main__":
    unittest.main()
