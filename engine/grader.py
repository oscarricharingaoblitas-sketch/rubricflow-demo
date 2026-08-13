"""Transparent, configurable rubric-based grader for written applications."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Mapping


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

Rubric = Mapping[str, Mapping[str, object]]


@dataclass(frozen=True)
class CriterionResult:
    label: str
    score: int
    evidence: list[str]
    explanation: str


def _sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]


def _supports_signal(sentence: str, signal: str) -> bool:
    """Return true when a signal occurs outside a simple negated clause."""
    lowered = sentence.lower()
    for match in re.finditer(rf"\b{re.escape(signal)}\w*\b", lowered):
        prefix = lowered[max(0, match.start() - 100):match.start()]
        if re.search(r"\b(?:no|not|sin|without|falta(?:n)?|carece(?:n)?(?:\s+de)?)\b[^.;:!?]{0,90}$", prefix):
            continue
        return True
    return False


def _score_criterion(text: str, label: str, signals: Iterable[str]) -> CriterionResult:
    lowered = text.lower()
    sentences = _sentences(text)
    matched = [
        signal for signal in signals
        if any(_supports_signal(sentence, signal) for sentence in sentences)
    ]
    evidence = [
        sentence for sentence in sentences
        if any(_supports_signal(sentence, signal) for signal in matched)
    ][:3]

    # Evidence breadth (0-8) plus specificity bonus (0-2).
    breadth = min(8, round(len(matched) / max(1, len(list(signals))) * 10))
    specificity = 0
    if matched:
        specificity = int(bool(re.search(r"\b\d+(?:[.,]\d+)?%?\b", text)))
        specificity += int(any(word in lowered for word in ("pilot", "revenue", "users", "partner")))
    score = min(10, breadth + specificity)
    explanation = (
        f"Matched {len(matched)} rubric signal(s): {', '.join(matched)}."
        if matched else "No explicit evidence matched this rubric criterion."
    )
    return CriterionResult(label, score, evidence, explanation)


def load_rubric(path: Path) -> dict[str, dict[str, object]]:
    """Load a rubric from CSV columns: key, label, weight, signals.

    Signals are separated with ``|``. Weights may be decimals (``0.25``),
    whole numbers (``25``), or percentages (``25%``); scoring normalizes them.
    """
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"key", "label", "weight", "signals"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("Rubric CSV must contain key, label, weight, and signals columns")

    rubric: dict[str, dict[str, object]] = {}
    for number, row in enumerate(rows, start=2):
        key = row["key"].strip()
        label = row["label"].strip()
        if not re.fullmatch(r"[a-z0-9_]+", key):
            raise ValueError(f"Rubric row {number} has an invalid key: {key!r}")
        if key in rubric:
            raise ValueError(f"Rubric key is duplicated: {key}")
        if not label:
            raise ValueError(f"Rubric row {number} has no label")

        raw_weight = row["weight"].strip()
        try:
            weight = float(raw_weight[:-1]) / 100 if raw_weight.endswith("%") else float(raw_weight)
        except ValueError as error:
            raise ValueError(f"Rubric row {number} has an invalid weight: {raw_weight!r}") from error
        if weight <= 0:
            raise ValueError(f"Rubric row {number} weight must be greater than zero")

        signals = list(dict.fromkeys(
            signal.strip().lower() for signal in row["signals"].split("|") if signal.strip()
        ))
        if not signals:
            raise ValueError(f"Rubric row {number} must contain at least one signal")
        rubric[key] = {"weight": weight, "signals": signals, "label": label}
    return rubric


def grade(text: str, rubric: Rubric = RUBRIC) -> dict:
    total_weight = sum(float(config["weight"]) for config in rubric.values())
    if not rubric or total_weight <= 0:
        raise ValueError("Rubric must contain at least one positively weighted criterion")
    criteria = {
        key: _score_criterion(text, config["label"], config["signals"])
        for key, config in rubric.items()
    }
    total = round(
        sum(criteria[key].score * float(rubric[key]["weight"]) for key in rubric) / total_weight,
        2,
    )
    return {
        "overall_score": total,
        "grade": "strong" if total >= 7 else "promising" if total >= 4 else "needs_evidence",
        "criteria": {key: asdict(result) for key, result in criteria.items()},
    }


def grade_csv(source: Path, destination: Path, rubric: Rubric = RUBRIC) -> None:
    with source.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or "application" not in rows[0]:
        raise ValueError("CSV must contain at least one row and an 'application' column")
    output = []
    for row in rows:
        result = grade(row["application"], rubric)
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
    parser.add_argument("--rubric", type=Path, help="Optional rubric CSV with key, label, weight, and signals")
    args = parser.parse_args()
    rubric = load_rubric(args.rubric) if args.rubric else RUBRIC
    grade_csv(args.input, args.output, rubric)
    print(f"Graded applications written to {args.output}")


if __name__ == "__main__":
    main()
