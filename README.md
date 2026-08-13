# RubricFlow

[Open the live demo](https://oscarricharingaoblitas-sketch.github.io/rubricflow-demo/)

RubricFlow is a privacy-first proof of concept for transparent first-pass application review. It highlights text evidence for five configurable business-evaluation criteria while keeping the final decision with a human reviewer.

## What is available

- Interactive browser demo; entered text stays in the browser
- Five-criterion explainable score breakdown
- [Sample rubric](sample-rubric.csv)
- [Sample auditable results](sample-results.csv)
- [Dependency-free Python batch engine](engine/grader.py) with [unit tests](engine/test_grader.py)

## Run the batch engine

```powershell
cd engine
python grader.py sample_applications.csv -o results.csv
python -m unittest -v
```

Input requires an `application` column; `id` is optional. Output is a flat CSV containing the overall result plus score, evidence, and explanation columns for every criterion.

## Intended use

RubricFlow supports accelerators, incubators, grant programs, and similar workflows that need an auditable first review. It is not a substitute for human judgment, and it should not make autonomous high-impact decisions.

## Fixed-scope pilot

**US$95** includes:

- adaptation of one existing rubric;
- processing of up to 50 applications;
- a spreadsheet-ready, auditable CSV;
- one calibration round using reviewer feedback;
- no subscription or mandatory integration.

[Request a RubricFlow pilot](https://github.com/oscarricharingaoblitas-sketch/rubricflow-demo/issues/new?template=pilot-request.yml)

## License

MIT
