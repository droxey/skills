---
name: intake-implementation-workflow
description: Use when resuming Intake product implementation or onboarding a new engineer to its canonical plan.
maturity: 0
---

# Intake Implementation Workflow

## Agent guidance

- Start by reading every file in planning/
- Summarize the intended product behavior before making changes
- Favor small, testable implementation passes over broad refactors
- If a requirement is ambiguous, document the ambiguity and resolve it against the most recent planning document

## Source directory structure

- planning/ — Planning documents (build-plan, implementation-spec, spec versions)
- templates/ — Implementation checklists and templates
- AGENTS.md — Agent guidance
- TASK.md — Task specification

## Workflow

1. Read all files in planning/ first
2. Summarize intended product behavior
3. Implement in small, testable passes
4. Validate against the most recent planning document

## Maturity

Level 0 - Intent. Substantiated by the written contract only; no runnable asset or tests yet.

## Purpose

Provide the canonical planning context for implementing the Intake product.

## Inputs

The current Intake task or the engineer's onboarding need.

## Outputs

The implementation steps and context needed to proceed.

## Example

Hand a new engineer the Intake planning context so implementation resumes without re-deriving decisions.

## Success criteria

The engineer or run has the canonical context and the next implementation step.