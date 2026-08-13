"""Build safe CALL-E follow-up tasks from RubricFlow review output.

This module only creates JSONL input. It never places or schedules a call.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Iterable


E164 = re.compile(r"^\+[1-9]\d{7,14}$")
REQUIRED_COLUMNS = {"application_id", "contact_phone", "human_review"}


def build_task(row: dict[str, str], *, region: str, language: str) -> dict[str, object]:
    application_id = row["application_id"].strip()
    phone = row["contact_phone"].strip()
    review_request = row["human_review"].strip()

    if not application_id:
        raise ValueError("application_id cannot be empty")
    if not E164.fullmatch(phone):
        raise ValueError(f"{application_id}: contact_phone must use E.164 format")
    if not review_request:
        raise ValueError(f"{application_id}: human_review cannot be empty")

    goal = (
        "Place a short follow-up call about an application reviewed with RubricFlow. "
        "Identify the program and application reference, explain that this is an information-"
        "gathering call and not a funding or selection decision, and ask only for the missing "
        f"information listed here: {review_request}. "
        "Do not reveal or invent a score, ranking, approval, rejection, deadline, or commitment. "
        "Do not request passwords, banking details, government identifiers, or other sensitive "
        "data. If the recipient does not consent to continue, thank them and end the call. "
        "Return a concise summary with whether the recipient consented, the information supplied, "
        "and any requested next step."
    )
    user_input = (
        f"Call the contact for RubricFlow application {application_id} in {language}. "
        f"Request this missing information only: {review_request}"
    )

    return {
        "to_phones": [phone],
        "region": region,
        "language": language,
        "goal": goal,
        "user_input": user_input,
        "metadata": {
            "workflow": "rubricflow-followup-v1",
            "application_id": application_id,
            "purpose": "missing-information-followup",
        },
    }


def read_tasks(source: Path, *, region: str, language: str) -> Iterable[dict[str, object]]:
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_COLUMNS.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"missing required columns: {', '.join(sorted(missing))}")

        for row in reader:
            if not row["human_review"].strip():
                continue
            yield build_task(row, region=region, language=language)


def write_jsonl(tasks: Iterable[dict[str, object]], destination: Path) -> int:
    destination.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with destination.open("w", encoding="utf-8", newline="\n") as handle:
        for task in tasks:
            handle.write(json.dumps(task, ensure_ascii=False, separators=(",", ":")) + "\n")
            count += 1
    return count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create CALL-E plan_call JSONL from RubricFlow follow-up rows. No calls are placed."
    )
    parser.add_argument("input", type=Path, help="CSV containing application_id, contact_phone, and human_review")
    parser.add_argument("-o", "--output", type=Path, default=Path("followups.jsonl"))
    parser.add_argument("--region", default="PE", help="CALL-E region hint (default: PE)")
    parser.add_argument("--language", default="Spanish", help="CALL-E call language (default: Spanish)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    count = write_jsonl(read_tasks(args.input, region=args.region, language=args.language), args.output)
    print(f"Prepared {count} CALL-E follow-up task(s) in {args.output}. No calls were placed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
