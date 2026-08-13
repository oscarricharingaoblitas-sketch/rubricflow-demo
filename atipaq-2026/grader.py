Exit code: 0
Wall time: 0.6 seconds
Output:
"""Auditable, evidence-first sample grader for ATIPAQ 2026 criteria."""

from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from pathlib import Path


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFD", value.lower())
    return "".join(char for char in value if unicodedata.category(char) != "Mn")


def sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]


def supports_signal(sentence: str, signal: str) -> bool:
    text = normalize(sentence)
    term = normalize(signal)
    for match in re.finditer(rf"\b{re.escape(term)}\b", text):
        prefix = text[max(0, match.start() - 100):match.start()]
        clause = re.split(r"[.;:!?]", prefix)[-1]
        broad_negation = re.search(
            r"\b(?:no(?!\s+solo\b)|nunca|tampoco)\b|"
            r"\bcarec(?:e|emos|en|ia|ian)(?:\s+de)?\b",
            clause,
        )
        local_without = re.search(r"\bsin\b[^,]{0,60}$", clause)
        if broad_negation or local_without:
            continue
        return True
    return False


def load_rubric(path: Path) -> list[dict[str, object]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"key", "label", "max_points", "signals"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("Rubric requires key, label, max_points and signals")
    rubric = []
    for row in rows:
        rubric.append({
            "key": row["key"].strip(),
            "label": row["label"].strip(),
            "max_points": float(row["max_points"]),
            "signals": [item.strip() for item in row["signals"].split("|") if item.strip()],
        })
    if sum(float(item["max_points"]) for item in rubric) != 100:
        raise ValueError("Official criterion maxima must total 100 points")
    return rubric


def grade(text: str, rubric: list[dict[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    total = 0.0
    for item in rubric:
        signal_list = list(item["signals"])
        matched = [
            signal for signal in signal_list
            if any(supports_signal(sentence, signal) for sentence in sentences(text))
        ]
        evidence = [
            sentence for sentence in sentences(text)
            if any(supports_signal(sentence, signal) for signal in matched)
        ][:3]
        evidence_score = min(10, round(len(matched) / max(1, len(signal_list)) * 10))
        points = round(evidence_score * float(item["max_points"]) / 10, 2)
        total += points
        key = str(item["key"])
        result[f"{key}_evidence_score"] = evidence_score
        result[f"{key}_points"] = points
        result[f"{key}_evidence"] = " | ".join(evidence) or "Sin evidencia explÃ­cita"

    total = round(total, 2)
    innovation_scalability = round(
        float(result["merito_innovador_points"]) + float(result["escalabilidad_points"]), 2
    )
    result["total_points"] = total
    result["innovation_plus_scalability"] = innovation_scalability
    result["reference_check"] = (
        "meets_published_thresholds"
        if total >= 70 and innovation_scalability >= 25
        else "human_review_required"
    )
    return result


def grade_csv(source: Path, destination: Path, rubric_path: Path) -> None:
    rubric = load_rubric(rubric_path)
    with source.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or "application" not in rows[0]:
        raise ValueError("Input CSV requires an application column")
    output = []
    for row in rows:
        output.append({"id": row.get("id", ""), **grade(row["application"], rubric)})
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=output[0].keys())
        writer.writeheader()
        writer.writerows(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--rubric", type=Path, default=Path("atipaq_2026_rubric.csv"))
    parser.add_argument("-o", "--output", type=Path, default=Path("results.csv"))
    args = parser.parse_args()
    grade_csv(args.input, args.output, args.rubric)
    print(f"Results written to {args.output}")


if __name__ == "__main__":
    main()

