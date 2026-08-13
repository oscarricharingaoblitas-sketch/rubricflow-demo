import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from plan_followups import plan_task, read_queue


class FollowupPlannerTests(unittest.TestCase):
    def test_calls_plan_call_without_run_call(self):
        observed = {}

        def fake_runner(command, **kwargs):
            observed["command"] = command
            observed["kwargs"] = kwargs
            return subprocess.CompletedProcess(command, 0, stdout='{"ok":true}', stderr="")

        result = plan_task(
            {
                "to_phones": ["+12025550101"],
                "region": "PE",
                "language": "Spanish",
                "goal": "Ask for the approved missing information.",
                "user_input": "Plan the approved follow-up.",
                "metadata": {"application_id": "RF-001"},
            },
            runner=fake_runner,
        )

        self.assertEqual(result, {"ok": True})
        self.assertEqual(observed["command"][:4], ["calle", "mcp", "call", "plan_call"])
        self.assertNotIn("run_call", observed["command"])
        payload = json.loads(observed["command"][-1])
        self.assertNotIn("metadata", payload)
        self.assertEqual(payload["to_phones"], ["+12025550101"])
        self.assertTrue(observed["kwargs"]["check"])

    def test_reads_jsonl_and_requires_plan_fields(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "queue.jsonl"
            source.write_text(
                '{"to_phones":["+12025550101"],"goal":"Confirm","user_input":"Plan"}\n',
                encoding="utf-8",
            )
            self.assertEqual(len(list(read_queue(source))), 1)

            source.write_text('{"goal":"Confirm"}\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "to_phones"):
                list(read_queue(source))


if __name__ == "__main__":
    unittest.main()
