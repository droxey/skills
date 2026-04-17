# Code Skill Eval Scorecard

- Date:
- Evaluator:
- Skill version/commit:

## 1) Trigger Evaluation

### Inputs
- Prompt set file: `code/evals/trigger-prompts.jsonl`
- Total prompts: 20
- Runs per prompt:

### Results
- True Positives (TP):
- False Positives (FP):
- True Negatives (TN):
- False Negatives (FN):

### Metrics
- Precision = TP / (TP + FP):
- Recall = TP / (TP + FN):
- Accuracy = (TP + TN) / (TP + TN + FP + FN):

### Trigger Targets
- Precision target: >= 0.90
- Recall target: >= 0.85

## 2) Output Quality Evaluation (with-skill vs without-skill)

### Scenario Set
- Scenario IDs:
- Repo/task context:

### Scoring Rubric (0-2 each)
- Plan quality:
- Spec completeness:
- Tests-first adherence:
- Manual verification quality:
- Mutation evidence quality:
- Docs/artifact update completeness:

### Aggregate
- With skill total:
- Without skill total:
- Delta:

## 3) Mutation Gate Compliance

- Minimum mutants used (medium/large changes):
- Kill rate achieved:
- Survivor handling documented (Y/N):
- Evidence template completed (Y/N):

## 4) Findings and Next Actions

### Top Failures
1.
2.
3.

### Minimal Fixes Proposed
1.
2.
3.

### Decision
- [ ] Ship as-is
- [ ] Patch description only
- [ ] Patch workflow instructions
- [ ] Re-run evals after patch
