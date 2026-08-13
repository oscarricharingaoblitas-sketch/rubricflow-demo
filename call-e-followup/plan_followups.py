"""Send a prepared RubricFlow queue to CALL-E's plan_call tool only."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Callable, Iterable


PLAN_FIELDS = ("to_phones", "region", "language", "goal", "user_input")


def read_queue(source: Path) -> Iterable[dict[str, object]]:
    with source.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            item = json.loads(line)
            if not isinstance(item, dict):
                raise ValueError(f"line {line_number}: expected a JSON object")
            missing = {"to_phones", "goal", "user_input"}.difference(item)
            if missing:
                raise ValueError(f"line {line_number}: missing {', '.join(sorted(missing))}")
            yield item


def plan_task(
    task: dict[str, object],
    *,
    cli: str = "calle",
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> dict[str, object]:
    arguments = {field: task[field] for field in PLAN_FIELDS if field in task}
    command = [
        cli,
        "mcp",
        "call",
        "plan_call",
        "--args-json",
        json.dumps(arguments, ensure_ascii=False, separators=(",", ":")),
    ]
    completed = runner(command, check=True, capture_output=True, text=True)
    response = json.loads(completed.stdout)
    if not isinstance(response, dict):
        raise ValueError("CALL-E plan_call returned a non-object response")
    return response


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call CALL-E plan_call for a prepared queue. This never invokes run_call."
    )
    parser.add_argument("input", type=Path, help="JSONL created by build_followups.py")
    parser.add_argument("--cli", default="calle", help="CALL-E CLI executable (default: calle)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    for task in read_queue(args.input):
        result = plan_task(task, cli=args.cli)
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
