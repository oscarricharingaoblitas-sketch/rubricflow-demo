"""Muestra auditable de prelectura para las bases UNAT 2026."""

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
        broad_negation = re.search(
            r"\b(?:no(?!\s+solo\b)|nunca|tampoco)\b|"
            r"\bcarec(?:e|emos|en|ia|ian)(?:\s+de)?\b|"
            r"\bfalta(?:n)?\b|\bsin\b[^,]{0,80}$",
            clause,
        )
        if broad_negation:
            continue
        return True
    return False


def load_rubric(path: Path) -> list[dict[str, object]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"key", "label", "max_points", "signals"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("La rubrica requiere key, label, max_points y signals")
    rubric = []
    for row in rows:
        rubric.append({
            "key": row["key"].strip(),
            "label": row["label"].strip(),
            "max_points": float(row["max_points"]),
            "signals": [item.strip() for item in row["signals"].split("|") if item.strip()],
        })
    if sum(float(item["max_points"]) for item in rubric) != 100:
        raise ValueError("Los maximos oficiales deben sumar 100 puntos")
    return rubric


def published_band(total: float) -> tuple[str, str]:
    if total >= 80:
        return "Excelente", "SELECCIONADO"
    if total >= 70:
        return "Bueno", "SELECCIONADO (lista de espera)"
    if total >= 60:
        return "Regular", "DESAPROBADO"
    return "Deficiente", "DESCALIFICADO"


def grade(text: str, rubric: list[dict[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    total = 0.0
    text_sentences = sentences(text)
    for item in rubric:
        signal_list = list(item["signals"])
        matched = [
            signal for signal in signal_list
            if any(supports_signal(sentence, signal) for sentence in text_sentences)
        ]
        evidence = [
            sentence for sentence in text_sentences
            if any(supports_signal(sentence, signal) for signal in matched)
        ][:3]
        evidence_score = min(10, round(len(matched) / max(1, len(signal_list)) * 10))
        points = round(evidence_score * float(item["max_points"]) / 10, 2)
        total += points
        key = str(item["key"])
        result[f"{key}_evidence_score"] = evidence_score
        result[f"{key}_points"] = points
        result[f"{key}_evidence"] = " | ".join(evidence) or "Sin evidencia explicita"

    total = round(total, 2)
    rating, official_result = published_band(total)
    result["total_points"] = total
    result["published_rating"] = rating
    result["published_result_if_score_confirmed"] = official_result
    result["human_review_required"] = "YES"
    return result


def grade_csv(source: Path, destination: Path, rubric_path: Path) -> None:
    rubric = load_rubric(rubric_path)
    with source.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or "proposal" not in rows[0]:
        raise ValueError("El CSV de entrada requiere una columna proposal")
    output = [{"id": row.get("id", ""), **grade(row["proposal"], rubric)} for row in rows]
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=output[0].keys())
        writer.writeheader()
        writer.writerows(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--rubric", type=Path, default=Path("unat_2026_rubric.csv"))
    parser.add_argument("-o", "--output", type=Path, default=Path("results.csv"))
    args = parser.parse_args()
    grade_csv(args.input, args.output, args.rubric)
    print(f"Resultados escritos en {args.output}")


if __name__ == "__main__":
    main()
