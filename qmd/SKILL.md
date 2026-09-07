---
name: qmd
description: Use when bootstrapping QMD search instructions to query indexed local markdown.
license: MIT
compatibility: Requires qmd CLI. Run `qmd skill show` for version-matched instructions.
allowed-tools: Bash(qmd:*), mcp__qmd__*
maturity: 0
---

# QMD - Query Markdown Documents

This installed skill is intentionally a small bootstrap so it does not go stale
when the qmd package updates.

Load the full, version-matched QMD instructions from the CLI:

!`qmd skill show`

If your agent does not support bang-command expansion, run:

```bash
qmd skill show
```

Then follow those instructions. In short: search first, fetch full sources with
`qmd get` or `qmd multi-get`, and answer from retrieved text rather than snippets.

## Maturity

Level 0 - Intent. Substantiated by the written contract only; no runnable asset or tests yet.

## Purpose

Bootstrap QMD search from the installed CLI for indexed markdown retrieval.

## Inputs

A question about local notes/wiki content.

## Outputs

Search instructions and retrieved results from the index.

## Example

Convert a question into QMD search instructions and return matching indexed notes.

## Success criteria

The query is translated into a working QMD search and results are grounded in the index.