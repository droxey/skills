# Intake Implementation Workflow

## Purpose

Use this recipe to implement the Intake app from its canonical product and build planning documents while keeping the planning materials themselves durable and colocated with the recipe.

## Canonical planning docs

Treat these files as the source planning set for this recipe:
- `planning/spec-v6.md`
- `planning/implementation-spec-v1.md`
- `planning/build-plan-v1.md`

When they disagree, prefer the latest product-facing behavior in `spec-v6.md`, then use `implementation-spec-v1.md` for architecture and delivery sequencing, and `build-plan-v1.md` for milestone framing.

## Expected workflow

1. Read all three planning documents before making implementation decisions.
2. Extract the current MVP scope, edge cases, and any explicit non-goals.
3. Translate the implementation into a small set of verifiable milestones.
4. Keep code changes aligned with the documented scope; do not add speculative features.
5. Validate behavior against the checklist in `templates/implementation-checklist.md`.
6. Update this recipe if the planning set changes materially.

## Deliverables

A complete Intake implementation effort should usually leave behind:
- the relevant application code changes in the target product repo
- any implementation notes needed to preserve architectural intent
- updates to this recipe when planning assumptions change

## Guardrails

- Do not treat old exploratory notes as canonical if they conflict with the planning files in `planning/`.
- Keep reusable workflow guidance here; keep product-specific code in the target application repo.
- Preserve naming, flows, and UI intent from the current planning docs unless a newer approved spec supersedes them.
