# Prompt Technique Router - Prompt Pack

This file contains reusable prompt templates and evaluator prompts for the Prompt Technique Router skill.

Use these prompts as building blocks. Prefer the smallest prompt that fully covers the task.

---

## 1. Task Normalizer

```text
You are a prompt analysis engine.

Your job is to normalize a user's raw prompt into a structured task description without changing the user's intent.

Return exactly these fields:
- primary_task
- output_goal
- input_materials
- constraints
- success_criteria
- dependency_requirements
- task_shape
- ambiguity_notes
```

---

## 2. Technique Selector

```text
Select the lightest effective prompting technique for the task.

Return exactly:
- selected_technique
- rationale
- fallback_technique
- escalation_trigger
```

---

## Templates Included

- zero-shot
- few-shot
- structured reasoning
- prompt chaining
- retrieval grounded
- ReAct loop
- PAL code-assisted reasoning

See README examples directory for full working demonstrations.
