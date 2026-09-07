---
name: essence-commit
description: >
  Write a commit message that stands on its own: Conventional Commits format, why over what,
  zero conversation residue, no AI-attribution trailer. Use when user says "write a commit",
  "commit message", "generate commit", or invokes /essence-commit.
maturity: 0
---

# essence-commit

A commit message is read by someone with no memory of the conversation that produced the change.
It must explain the change on its own terms.

## Format

`<type>(<scope>): <imperative summary>` (`<scope>` optional).
Types: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `chore`, `build`, `ci`, `style`, `revert`.
Imperative mood ("add", "fix", "remove"), ≤50 chars where possible, no trailing period.

Body only when the *why* isn't obvious from the diff. Skip it entirely when the subject already
says everything a future reader needs. When present: wrap ~72 chars, `-` bullets, reference
issues/PRs at the end (`Closes #42`).

## What never goes in

- The diff already shows *what* changed: don't restate it in prose
- Anything referencing this conversation: "as requested", "per your instruction", "you asked me to"
- "This commit does X", first-person narration ("I", "we")
- **No AI-attribution trailer of any kind** (no `Co-Authored-By: Claude`, no "Generated with…"):
  this is a hard rule, not a default; do not add one even if a template suggests it
- Emoji, unless the project's own convention already uses it

## Example

Diff: new endpoint, non-obvious constraint driving the design
```
feat(api): add GET /users/:id/profile

Mobile client needs profile data without the full user payload,
to keep cold-launch bandwidth down on LTE.

Closes #128
```

Diff: obvious rename, no body needed
```
refactor(auth): rename validateToken to verifyToken
```

## Boundaries

Generates the message only; does not run `git commit`, stage files, or amend. Output as a
paste-ready code block. Breaking changes, security fixes, and migrations always keep a full body:
never compress those into subject-only.

## Maturity

Level 0 - Intent. Substantiated by the written contract only; the essence methodology is maintained in the droxey/skills repo.
