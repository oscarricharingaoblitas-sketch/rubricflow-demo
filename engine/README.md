# Transparent Application Grader — working demo

A zero-cost Python prototype for scoring written applications against five criteria. It produces an overall score, individual criterion scores, matched evidence, and explanations suitable for reviewer audit.

## What this demonstrates

- Five weighted criteria matching the project brief
- Explainable scoring rather than an opaque number
- Batch CSV input and flat, spreadsheet-ready CSV output
- No paid API or external dependency
- Unit tests and a clean extension point for an optional LLM layer

## Run

```powershell
python grader.py sample_applications.csv -o results.csv
python -m unittest -v
```

Input requires an `application` column; `id` is optional.

The output contains the overall result plus three columns per criterion: score, matched evidence, and explanation. A final `human_review` column makes the required reviewer action explicit.

## Production path

For production, calibrate scoring anchors against 20–50 previously human-scored applications. Keep factual fields rule-based and add a client-approved LLM only for qualitative criteria. The same output contract remains stable, making the system auditable and easy to integrate.
