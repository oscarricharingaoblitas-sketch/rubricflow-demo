"""Matriz no oficial de evidencia para el Demo Day Belcorp/Emprende UP 2026."""

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
        prefix = text[max(0, match.start() - 120):match.start()]
        clause = re.split(r"[.;:!?]", prefix)[-1]
        if re.search(
            r"\b(?:no(?!\s+solo\b)|nunca|tampoco)\b|"
            r"\bcarec(?:e|emos|en|ia|ian)(?:\s+de)?\b|"
            r"\bsin\b[^,]{0,80}$",
            clause,
        ):
            continue
        return True
    return False


def load_criteria(path: Path) -> list[dict[str, object]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"key", "label", "signals"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("Los criterios requieren key, label y signals")
    if len(rows) != 5:
        raise ValueError("Los terminos publican exactamente cinco criterios")
    return [{
        "key": row["key"].strip(),
        "label": row["label"].strip(),
        "signals": [part.strip() for part in row["signals"].split("|") if part.strip()],
    } for row in rows]


def is_yes(value: str) -> bool:
    return normalize(value.strip()) in {"yes", "si", "true", "1"}


def analyze(row: dict[str, str], criteria: list[dict[str, object]]) -> dict[str, object]:
    text = row["presentation"]
    text_sentences = sentences(text)
    result: dict[str, object] = {}
    coverages = []
    for criterion in criteria:
        signals = list(criterion["signals"])
        matched = [
            signal for signal in signals
            if any(supports_signal(sentence, signal) for sentence in text_sentences)
        ]
        evidence = [
            sentence for sentence in text_sentences
            if any(supports_signal(sentence, signal) for signal in matched)
        ][:3]
        coverage = round(len(matched) / len(signals) * 100)
        coverages.append(coverage)
        key = str(criterion["key"])
        result[f"{key}_evidence_coverage_percent"] = coverage
        result[f"{key}_evidence"] = " | ".join(evidence) or "Sin evidencia explicita"

    attendance = float(row["attendance_percent"])
    initial_complete = is_yes(row["initial_form_completed"])
    exit_complete = is_yes(row["exit_form_completed"])
    result["average_evidence_coverage_percent"] = round(sum(coverages) / len(coverages), 1)
    result["attendance_over_85"] = "YES" if attendance > 85 else "NO"
    result["forms_completed"] = "YES" if initial_complete and exit_complete else "NO"
    result["published_conditions_met"] = "YES" if attendance > 85 and initial_complete and exit_complete else "NO"
    result["official_jury_score_required"] = "YES"
    result["warning"] = "Evidence coverage is not an official score and uses no invented weights"
    return result


def analyze_csv(source: Path, destination: Path, criteria_path: Path) -> None:
    criteria = load_criteria(criteria_path)
    with source.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"presentation", "attendance_percent", "initial_form_completed", "exit_form_completed"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("Faltan columnas obligatorias en el CSV")
    output = [{"id": row.get("id", ""), **analyze(row, criteria)} for row in rows]
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=output[0].keys())
        writer.writeheader()
        writer.writerows(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--criteria", type=Path, default=Path("belcorp_demo_day_criteria.csv"))
    parser.add_argument("-o", "--output", type=Path, default=Path("results.csv"))
    args = parser.parse_args()
    analyze_csv(args.input, args.output, args.criteria)
    print(f"Resultados escritos en {args.output}")


if __name__ == "__main__":
    main()
