# Prompt Technique Router

Route a raw prompt to the lightest effective prompting technique, rewrite it into a stronger structure, and validate the result before use.

## What this skill does

This skill takes a user prompt or rough task description and returns:

- the selected prompting technique,
- why that technique fits,
- a refactored prompt,
- a validation report,
- a fallback technique,
- operator notes.

It is designed to avoid two common failures:

1. overengineering simple prompts,
2. under-structuring prompts that need retrieval, staged reasoning, tools, or code execution.

## Included files

- `SKILL.md` — runtime instructions and routing policy
- `prompts.md` — templates, evaluators, and validation prompts
- `examples/` — worked examples for installation, testing, and regression checks

## v1 techniques

- zero-shot
- few-shot
- structured reasoning scaffold
- prompt chaining
- retrieval-grounded prompt
- ReAct-style tool loop
- PAL-style code-assisted reasoning

## Installation

Copy this skill folder into your skills directory.

Example layout:

```text
skills/
  prompt-technique-router/
    README.md
    SKILL.md
    prompts.md
    examples/
```

## How to use

Invoke the skill when the user asks to improve a prompt, choose a prompting strategy, or diagnose prompt failure.

Expected inputs:

- `raw_prompt`
- `user_goal` (optional)
- `constraints` (optional)
- `available_tools` (optional)
- `source_context` (optional)
- `target_model` (optional)
- `risk_level` (optional)

Expected outputs:

- `selected_technique`
- `why_this_technique`
- `refactored_prompt`
- `validation_report`
- `fallback_technique`
- `operator_notes`

## Fast test flow

Use this four-step test loop.

### 1. Normalize

Extract the real task shape from the raw prompt.

### 2. Route

Select the lightest effective technique.

### 3. Refactor

Rewrite into the appropriate template.

### 4. Validate

Run at least these checks:

- structure complete
- technique fit
- ambiguity check
- risk check
- minimality check

## Validation suggestions

These are the highest-value validation passes to implement first.

### PromptLint

Verify the rewritten prompt contains:

- a clear task,
- bounded inputs,
- constraints,
- output requirements,
- uncertainty behavior.

### TechniqueFitCheck

Verify the chosen technique is justified and not heavier than necessary.

### RiskGate

Escalate to retrieval-grounded or source-bounded prompting when the task is factual, current, contractual, or otherwise high risk.

### Golden-set evaluation

Keep a small benchmark set of raw prompts and compare:

- original result,
- refactored result,
- output compliance,
- factual grounding,
- error rate.

## Recommended scoring rubric

Use a 1–5 scale for each category:

- technique fit
- structural completeness
- ambiguity handling
- hallucination resistance
- output format compliance
- unnecessary complexity

## Worked examples

See the `examples/` directory:

- `01-zero-shot-rewrite.md`
- `02-few-shot-labeling.md`
- `03-structured-reasoning-decision.md`
- `04-retrieval-grounded-analysis.md`
- `05-react-tool-loop.md`
- `06-pal-calculation.md`

These are designed to be used as smoke tests and regression fixtures.

## Design principles

- choose the simplest effective technique
- do not fabricate tools, context, or sources
- do not force retrieval when the task is local transformation
- do not force reasoning scaffolds on trivial prompts
- do not use tool loops unless tools actually exist
- prefer explicit uncertainty over confident guessing

## Good fit

Use this skill for:

- prompt rewrites
- prompting strategy selection
- reliability tuning
- structured-output improvement
- hallucination-risk reduction
- refactoring prompts for RAG, tools, or code execution

## Poor fit

Do not use this skill when:

- the user only wants the answer,
- the task is so small that rewriting adds no value,
- the prompt depends on unavailable systems that cannot be represented honestly.

## Maintenance notes

When extending the skill:

- add new techniques only when they solve a distinct class of problems,
- keep routing rules conservative,
- add at least one worked example per new technique,
- prefer regression examples over abstract theory.
