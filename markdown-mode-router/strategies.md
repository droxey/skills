# Markdown Strategies

## General strategy

### Use when

Use for every non-course markdown file.

### Source signal

This strategy is derived from the Apple Notes reference:

- a strong title at the top
- an optional goal block near the top
- one primary section when the file is mainly a list or shortlist
- grouped subheads under that section
- terse bullets with very little filler

### Structure

1. `# H1` title
   - optional emoji allowed only when it adds signal
   - prefer at most one emoji
2. optional goal callout near the top
   - use when the file has a concrete objective
   - format as a blockquote
3. `## H2` sections
   - no emojis in H2
4. `### H3` subgroup headings
   - use when one H2 contains grouped items
5. bullets for entries
   - prefer one idea per bullet
   - nest bullets only when they truly belong together

### Style

- optimize for scanning first
- keep prose short
- prefer labels plus specifics over paragraphs
- keep sibling bullets parallel
- use bold only for labels or high-signal terms
- avoid decorative separators unless they carry meaning

### TOC

Only add a TOC when both are true:

- exactly 1 H2 exists in the file
- at least 2 H3 headings exist in the file

TOC format:

```md
## Contents
- [Section](#section)
  - Subgroup A
  - Subgroup B
```

Rules:

- link the H2 entry
- do not link H3 entries
- omit the TOC in every other heading shape

### Preferred pattern

```md
# Title

> **Goal:** concrete outcome

## Section

### Group A
- item
- item

### Group B
- item
- item
```

## Teaching strategy

### Trigger

Use teaching mode when either condition is true:

- repo name starts with `ACS`
- the markdown is a lesson plan, lab, tip, assignment, slides, speaker notes, or quiz

### Rules

- route to the course-first markdown workflow
- do not inject general-mode defaults just because they look tidy
- preserve established teaching file contracts
- keep lesson assets aligned with the existing teaching system

### Known teaching constraints

- lesson plans stay course-structured
- `plan.md` remains the source of truth for lesson plans when applicable
- `slides.md` uses reveal.js markdown only when applicable
- speaker notes stay embedded when applicable

### Output expectation

Return:

- selected mode
- why the route was chosen
- which strategy rules applied
- any assumptions or unresolved edges
