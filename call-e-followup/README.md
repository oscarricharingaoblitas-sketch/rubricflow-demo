# RubricFlow + CALL-E follow-up planner

This integration converts reviewer requests in a RubricFlow CSV into the JSONL format consumed by CALL-E's official Python batch runner. It is designed for a narrow use case: asking an applicant for missing information without revealing a score or implying an approval or rejection.

## Safety model

- The builder only creates a task file; it never places or schedules calls.
- Rows without a `human_review` request are skipped.
- Phone numbers must use E.164 format.
- Identifiers and review requests have length limits, and control characters are rejected.
- Missing-information text is treated as quoted data rather than executable instructions.
- The call goal forbids collecting passwords, banking details, government identifiers, or other sensitive data.
- The recipient may decline and end the call.
- A human operator must inspect the JSONL and explicitly choose CALL-E's execute mode before any real call.
- Use only contacts who have consented to receive program follow-ups. The included `+1 202-555-01xx` numbers are fictional examples and must never be executed.

## 1. Build the queue

```bash
cd call-e-followup
python build_followups.py sample-followups.csv -o followups.jsonl
```

Expected result:

```text
Prepared 2 CALL-E follow-up task(s) in followups.jsonl. No calls were placed.
```

Required input columns:

| Column | Meaning |
| --- | --- |
| `application_id` | Internal reference, not a score or decision |
| `contact_phone` | Consented contact in E.164 format |
| `human_review` | Exact missing information approved by a reviewer |

## 2. Inspect and plan with CALL-E

Use the [official CALL-E Python batch runner](https://github.com/CALLE-AI/call-e-integrations/tree/main/examples/python-batch-runner). Its default `--dry-run` mode invokes `plan_call` only and does not start a phone call:

```bash
uv run python client.py --input /path/to/followups.jsonl --dry-run
```

The operator must authenticate with `calle auth login` when prompted. Review the returned plans and verify every destination, purpose, language, and question.

## 3. Execute only after human approval

Real calls require a deliberate second command from the operator:

```bash
uv run python client.py --input /path/to/followups.jsonl --execute
```

CALL-E then performs `plan_call → run_call → get_call_run` and stores the plan, run result, final status, summary, and transcript. Never use `--execute` as a connectivity test.

## Tests

```bash
python -m unittest -v
```

The tests cover safe payload generation, E.164 validation, input bounds, control-character rejection, empty-review filtering, JSONL output, and required-column validation. No network access, CALL-E account, or paid API is needed.
