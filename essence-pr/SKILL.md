---
name: essence-pr
description: >
  Write a PR/MR description that stands on its own: no conversation residue, no padding, only
  what a reviewer who wasn't there needs. No fixed template; shape it the way you always would.
  Use when user says "write a PR description", "PR description", or invokes /essence-pr.
maturity: 0
---

# essence-pr

A reviewer opens this PR with no memory of the conversation that produced it. The description's
only job: let them understand what's wrong and why the fix is right, without asking a follow-up
question.

## No template

essence doesn't prescribe a structure. Write it the way you always would: the repo's own PR
template if one exists, two sentences if that's all the change needs, more if the change is
genuinely complex. The shape is your call, same as ever. What essence adds is the filter, not
the format: no conversation residue, no padding, nothing the reviewer needs outside context for.

## What never goes in

- "As discussed", "per your feedback", "you asked me to split this up": the reviewer wasn't there
- Restating the diff line-by-line: the diff already shows *what*; the description explains *why*
  it's the right fix
- Hedging about scope ("not proposing to also fix X"): if it's out of scope, just don't mention it
- Filler acknowledgments, sign-offs, or AI attribution

## Boundaries

Generates the description text only; does not run `gh pr create` or push. If asked to update an
existing PR, produce the replacement text; let the user apply it.

## Maturity

Level 0 - Intent. Substantiated by the written contract only; the essence methodology is maintained in the droxey/skills repo.
