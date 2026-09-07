---
name: essence-doc
description: Use when rewriting a document to stand alone while preserving code, URLs, and paths.
maturity: 0
---

# essence-doc

## Trigger

`/essence-doc <filepath>` or a request to tighten a doc/comment/note file.

## Process

1. Read the target file.
2. Rewrite it applying both essence rules from `../essence/SKILL.md`:
   - Cut everything that only makes sense to someone who saw the conversation that produced
     this doc: the reader of this file was never in that conversation.
   - Find what you actually mean in each paragraph and write only that. Collapse padded
     paragraphs to their real point; merge bullets that repeat the same idea; drop redundant
     examples once the pattern is shown once.
   - Preserve every code fence, inline code span, URL, file path, and heading/list structure
     exactly. Do not touch content inside code fences.
3. Save the original as `<filepath>.original.md` before overwriting.
4. Validate: from this skill's directory, run
   `python3 scripts/essence_doc.py validate <filepath>.original.md <filepath>`
   This confirms every code fence / inline code / URL / path from the original still appears
   verbatim in the rewrite. It does not check prose quality: that's your judgment call, not
   the script's.
5. If validation fails, restore the missing span exactly and re-run validation (up to 2
   retries). If it still fails, restore `<filepath>.original.md` over `<filepath>`, report the
   failure, and stop.
6. Report the result: what changed, in essence, not a paragraph recapping the process.

## Boundaries

Only rewrites the file. Does not commit or open a PR. If the file mixes prose with large data
blocks (config, generated tables), leave the data blocks untouched: only prose is essence's
target.

## Maturity

Level 0 - Intent. Substantiated by the written contract only; the essence methodology is maintained in the droxey/skills repo.

## Purpose

Tighten documentation without changing its protected literal content.

## Inputs

A documentation file to rewrite.

## Outputs

A concise rewrite and a validated backup of the original.

## Example

Rewrite a project note, then validate that its original code fences, URLs, and paths remain verbatim.

## Success criteria

The revised document stands alone and the protected-span validator succeeds.
