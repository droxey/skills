# Evals Scaffolding

This folder provides lightweight evaluation assets for the `code` skill.

## Files

- `trigger-prompts.jsonl`: 27 prompts for trigger precision/recall checks (`should_trigger: true|false`).
- `scorecard-template.md`: run template for recording trigger and quality results.

## Suggested Run Loop

1. Execute all prompts with skill routing enabled.
2. Record predicted activation (`triggered`) per prompt.
3. Compute precision/recall for trigger behavior.
4. Run output-quality checks on representative tasks and fill scorecard.
5. Iterate on `SKILL.md` description only if metrics regress or remain below target.

## Command

Run trigger eval and write a dated report:

```bash
python code/evals/run_trigger_eval.py --observed code/evals/observed-trigger-results.jsonl
```

Observed results file format (`id`, `triggered`):

```json
{"id":"T01","triggered":true}
{"id":"F01","triggered":false}
```
