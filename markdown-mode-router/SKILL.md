---
name: markdown-mode-router
description: Routes markdown work to teaching or general formatting mode. Use when a user asks to write, rewrite, or normalize markdown with minimal structural changes.
---

# Markdown Mode Router

Use this skill before writing, rewriting, or normalizing a markdown file.

It decides whether the file should use the teaching strategy or the general non-course strategy, then applies the lightest correct structure.

## Route

Choose `teaching` when either condition is true:

- repo name starts with `ACS`
- the file is, or clearly contains, a lesson plan, lab, tip, assignment, slides, speaker notes, or quiz

Choose `general` for every other markdown file.

## Goal

- avoid mixing course formatting into non-course files
- avoid applying general formatting rules to teaching artifacts
- make the minimum necessary structural change
- preserve stable headings when links may already exist

## Workflow

1. Inspect repo name, file purpose, and heading shape.
2. Select `teaching` or `general`.
3. Apply the selected strategy.
4. Return:
   - `selected_mode`
   - `why`
   - `toc_decision`
   - `heading_plan`
   - `formatted_markdown`
   - `assumptions`

## TOC rule

Add a TOC only when both are true:

- the file has exactly 1 H2
- the file has at least 2 H3 headings

When a TOC is allowed:

- place it near the top of the file
- link the H2 entry
- list H3 entries as nested plain bullets without links

Do not generate a TOC in any other case.

## Guardrails

- never use emojis in H2
- prefer scan-first structure over prose-heavy structure
- preserve teaching-specific constraints when in `teaching` mode
- preserve existing meaning and ordering unless the file is clearly broken
