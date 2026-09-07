---
name: prompt-technique-router
description: Use when choosing and applying the best-fit prompting technique for a task.
maturity: 0
---

# Prompt Technique Router

Use this skill when a user wants help improving a prompt, selecting a prompting strategy, restructuring a task for better model performance, or reducing ambiguity/failure risk before execution.

This skill does **not** assume one prompting pattern fits every task. It first identifies the user's real task shape, then selects the lightest effective prompting technique, rewrites the prompt into a stronger structure, and validates the rewrite before returning it.

## What this skill does

Given a raw prompt or task request, this skill will:

1. identify the real task goal,
2. classify the task shape,
3. select the best-fit prompting technique,
4. refactor the prompt into that technique,
5. validate the refactored prompt,
6. return the rewritten prompt plus rationale, risks, and fallback guidance.

## Default operating principle

Choose the **simplest technique that can reliably satisfy the task**.

Do not escalate to heavier techniques such as ReAct, PAL, self-consistency, or Tree of Thoughts unless the task actually needs them.

## Supported techniques in v1

- zero-shot
- few-shot
- structured reasoning scaffold
- prompt chaining
- retrieval-grounded prompt
- ReAct-style tool loop
- PAL-style code-assisted reasoning

## Inputs

Expected inputs:

- `raw_prompt`
- `user_goal`
- `constraints`
- `available_tools`
- `source_context`
- `target_model`
- `risk_level`

## Outputs

Return:

- `selected_technique`
- `why_this_technique`
- `refactored_prompt`
- `validation_report`
- `fallback_technique`
- `operator_notes`

## Workflow

Follow this workflow in order:

1. Normalize the task
2. Route to a technique
3. Refactor the prompt
4. Validate the rewritten prompt

Always:

- avoid inventing tools or sources
- preserve unresolved ambiguity
- prefer minimal intervention over maximal structure

## Maturity

Level 0 - Intent. Substantiated by the written contract only; no runnable asset or tests yet.

## Purpose

Select and apply the right prompting technique for the task.

## Example

Classify a task's ambiguity and apply the matching technique to the actual prompt.

## Success criteria

A specific technique is chosen and applied, not left as generic advice.