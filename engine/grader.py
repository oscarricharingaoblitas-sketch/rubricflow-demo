"""Transparent, configurable rubric-based grader for written applications."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


RUBRIC = {
    "problem_specificity": {
        "weight": 0.20,
        "signals": ["because", "affects", "currently", "cost", "delay", "lack", "problem"],
        "label": "Problem specificity",
    },
    "solution_uniqueness": {
        "weight": 0.20,
        "signals": ["unlike", "unique", "novel", "instead", "proprietary", "differentiator", "solution"],
        "label": "Solution uniqueness",
    },
    "development_stage": {
        "weight": 0.20,
        "signals": ["prototype", "pilot", "launched", "users", "revenue", "tested", "mvp"],
        "label": "Development stage",
    },
    "beneficiaries_and_funding": {
        "weight": 0.20,
        "signals": ["beneficiaries", "customers", "community", "funding", "grant", "investor", "target"],
        "label": "Beneficiaries and funding",
    },
    "value_partnerships_presentation": {
        "weight": 0.20,
        "signals": ["partner", "recognised", "award", "impact", "scalable", "market", "milestone"],
        "label": "Value, partnerships and presentation",
    },
}


@dataclass(frozen=True)
class CriterionResult:
    label: str
    score: int
    evidence: list[str]
    explanation: str


def _sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]


def _score_criterion(text: str, label: str, signals: Iterable[str]) -> CriterionResult:
    lowered = text.lower()
    matched = [signal for signal in signals if re.search(rf"\b{re.escape(signal)}\w*\b", lowered)]
    evidence = [
        sentence for sentence in _sentences(text)
        if any(re.search(rf"\b{re.escape(signal)}\w*\b", sentence.lower()) for signal in matched)
    ][:3]

    # Evidence breadth (0-8) plus specificity bonus (0-2).
    breadth = min(8, round(len(matched) / max(1, len(list(signals))) * 10))
    specificity = int(bool(re.search(r"\b\d+(?:[.,]\d+)?%?\b", text)))
    specificity += int(any(word in lowered for word in ("pilot", "revenue", "users", "partner")))
    score = min(10, breadth + specificity)
    explanation = (
        f"Matched {len(matched)} rubric signal(s): {', '.join(matched)}."
        if matched else "No explicit evidence matched this rubric criterion."
    )
    return CriterionResult(label, score, evidence, explanation)


def grade(text: str) -> dict:
    criteria = {
        key: _score_criterion(text, config["label"], config["signals"])
        for key, config in RUBRIC.items()
    }
    total = round(sum(criteria[key].score * RUBRIC[key]["weight"] for key in RUBRIC), 2)
    return {
        "overall_score": total,
        "grade": "strong" if total >= 7 else "promising" if total >= 4 else "needs_evidence",
        "criteria": {key: asdict(result) for key, result in criteria.items()},
    }


def grade_csv(source: Path, destination: Path) -> None:
    with source.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or "application" not in rows[0]:
        raise ValueError("CSV must contain at least one row and an 'application' column")
    output = []
    for row in rows:
        result = grade(row["application"])
        flat = {
            "id": row.get("id", ""),
            "overall_score": result["overall_score"],
            "grade": result["grade"],
        }
        for key, criterion in result["criteria"].items():
            flat[f"{key}_score"] = criterion["score"]
            flat[f"{key}_evidence"] = " | ".join(criterion["evidence"])
            flat[f"{key}_explanation"] = criterion["explanation"]
        flat["human_review"] = (
            "Verify cited facts and make the final decision."
            if result["overall_score"] >= 7
            else "Request or review missing evidence before deciding."
        )
        output.append(flat)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=output[0].keys())
        writer.writeheader()
        writer.writerows(output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Grade application text with an auditable rubric.")
    parser.add_argument("input", type=Path, help="Input CSV containing an 'application' column")
    parser.add_argument("-o", "--output", type=Path, default=Path("results.csv"))
    args = parser.parse_args()
    grade_csv(args.input, args.output)
    print(f"Graded applications written to {args.output}")


if __name__ == "__main__":
    main()
