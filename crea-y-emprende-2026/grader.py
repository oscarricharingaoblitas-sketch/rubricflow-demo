"""Validador y consolidador no oficial para Crea y Emprende 2026, categoria B."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


EXPECTED_SECTION_MAX = {"project": 28, "portfolio": 48, "expo": 20}
EXPECTED_JURORS = {"J1", "J2", "J3"}


def load_rubric(path: Path) -> list[dict[str, object]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"section", "key", "label", "min_score", "max_score"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("La rubrica requiere section, key, label, min_score y max_score")
    keys = [row["key"].strip() for row in rows]
    if len(keys) != len(set(keys)):
        raise ValueError("La rubrica contiene claves duplicadas")
    rubric = []
    for row in rows:
        section = row["section"].strip()
        if section not in EXPECTED_SECTION_MAX:
            raise ValueError(f"Seccion desconocida: {section}")
        item = {
            "section": section,
            "key": row["key"].strip(),
            "label": row["label"].strip(),
            "min_score": int(row["min_score"]),
            "max_score": int(row["max_score"]),
        }
        if (item["min_score"], item["max_score"]) != (1, 4):
            raise ValueError("Cada criterio oficial debe usar la escala entera de 1 a 4")
        rubric.append(item)
    for section, expected in EXPECTED_SECTION_MAX.items():
        calculated = sum(int(item["max_score"]) for item in rubric if item["section"] == section)
        if calculated != expected:
            raise ValueError(f"Maximo incorrecto para {section}: {calculated}; esperado {expected}")
    return rubric


def parse_score(value: str, key: str) -> int:
    try:
        score = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Puntaje no entero para {key}: {value!r}") from exc
    if not 1 <= score <= 4:
        raise ValueError(f"Puntaje fuera de la escala 1-4 para {key}: {score}")
    return score


def consolidate(source: Path, rubric_path: Path) -> list[dict[str, object]]:
    rubric = load_rubric(rubric_path)
    keys = [str(item["key"]) for item in rubric]
    required = {"project_id", "title", "school", "juror", *keys}
    with source.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or not required.issubset(rows[0]):
        raise ValueError("Faltan columnas obligatorias en los puntajes")
    projects: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        projects[row["project_id"].strip()].append(row)
    output = []
    for project_id, evaluations in projects.items():
        jurors = [row["juror"].strip() for row in evaluations]
        if set(jurors) != EXPECTED_JURORS or len(jurors) != 3:
            raise ValueError(f"{project_id} requiere exactamente J1, J2 y J3, sin duplicados")
        identities = {(row["title"].strip(), row["school"].strip()) for row in evaluations}
        if len(identities) != 1:
            raise ValueError(f"Titulo o IE inconsistente para {project_id}")
        section_values: dict[str, list[int]] = defaultdict(list)
        totals = []
        for row in evaluations:
            section_total = defaultdict(int)
            for item in rubric:
                section_total[str(item["section"])] += parse_score(row[str(item["key"])], str(item["key"]))
            for section in EXPECTED_SECTION_MAX:
                section_values[section].append(section_total[section])
            totals.append(sum(section_total.values()))
        title, school = identities.pop()
        output.append({
            "project_id": project_id,
            "title": title,
            "school": school,
            "jurors": 3,
            "project_avg_of_28": round(sum(section_values["project"]) / 3, 2),
            "portfolio_avg_of_48": round(sum(section_values["portfolio"]) / 3, 2),
            "expo_avg_of_20": round(sum(section_values["expo"]) / 3, 2),
            "total_avg_of_96": round(sum(totals) / 3, 2),
            "decision": "JURADO HUMANO",
        })
    output.sort(key=lambda row: (-float(row["total_avg_of_96"]), str(row["project_id"])))
    for rank, row in enumerate(output, start=1):
        row["rank_by_average"] = rank
    return output


def write_results(rows: list[dict[str, object]], destination: Path) -> None:
    if not rows:
        raise ValueError("No hay resultados para escribir")
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--rubric", type=Path, default=Path("crea_y_emprende_2026_category_b_rubric.csv"))
    parser.add_argument("-o", "--output", type=Path, default=Path("results.csv"))
    args = parser.parse_args()
    write_results(consolidate(args.input, args.rubric), args.output)
    print(f"Resultados escritos en {args.output}")


if __name__ == "__main__":
    main()
