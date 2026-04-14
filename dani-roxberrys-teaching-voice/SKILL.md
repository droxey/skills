---
name: dani-roxberrys-teaching-voice
description: Generate lesson assets in Dani Roxberry's builder-teacher voice from a lesson plan, plan, or topic outline without requiring a transcript at runtime.
---

# Dani Roxberry's Teaching Voice

Use this skill when the user wants lesson materials, slides, speaker notes, examples, or companion quiz assets that sound like Dani Roxberry teaching in class.

## Runtime model

The teaching voice is precomputed.

Do not require a transcript at runtime unless the user explicitly asks to refresh or re-study the voice model.

At runtime, use:
- lesson plan
- topic outline
- explicit user constraints
- existing course materials if provided

Do not require:
- transcript
- class recording
- voice sample

## Core rule

Lesson content comes from:
1. lesson plan or topic outline
2. explicit user constraints
3. existing course materials provided for the lesson

Voice comes from the precomputed Dani Roxberry teaching voice model.

Do not treat voice guidance as curriculum authority.

## What this skill produces

Primary outputs:
- slides.md
- speaker-notes.md
- examples.md

Optional outputs:
- quiz spec for Ace Quiz Maker
- voice-report.md
- drift-report.md
- privacy-audit.md

## Voice model

Target voice:
- builder-teacher
- practical
- direct
- example-first
- engineering-grounded
- clear over polished
- verification-oriented
- tradeoff-aware

Increase:
- concrete examples
- real engineering framing
- operational language
- likely failure modes
- verification loops
- concise transitions

Suppress:
- academic inflation
- corporate enablement tone
- motivational fluff
- AI-generic phrasing
- overproduced polish
- vague abstraction
- transcript filler speech
- empty summary language

## Generation order

Always generate in this order:
1. examples.md
2. slides.md
3. speaker-notes.md
4. optional quiz asset

Reason:
- examples anchor the teaching
- slides organize the teaching
- notes expand the teaching without changing scope
- quiz checks what the lesson actually teaches

## Output rules

### examples.md
Must:
- align to the lesson plan or topic outline
- be teachable live
- stay concrete
- reinforce the lesson objectives directly

Must not:
- introduce new curriculum
- become an assignment unless requested
- depend on session-specific context

### slides.md
Must:
- use one clear teaching job per slide
- prefer concrete over abstract
- use plainspoken language
- sound like Dani teaching, not like AI or institutional curriculum copy
- stay tightly aligned to the lesson plan or topic outline

Must not:
- sound too polished
- sound academic
- invent exercises or logistics
- include institution-specific or student-specific details

### speaker-notes.md
Must:
- expand delivery, not curriculum
- explain examples naturally
- include likely confusion points where useful
- feel like live teaching support, not an essay

Must not:
- add new learning objectives
- drift away from the lesson plan
- become transcript-like
- repeat slide text without purpose

## Standard workflow

1. Read the lesson plan or topic outline first
2. Normalize objectives, sequence, and constraints
3. Apply the precomputed voice model
4. Generate examples.md
5. Generate slides.md
6. Generate speaker-notes.md
7. Run privacy scrub if source materials include identifying details
8. Run drift audit against the lesson plan or topic outline
9. Optionally generate a quiz spec for Ace Quiz Maker
10. Finalize only after drift and privacy checks pass

## Validation passes

### Privacy scrub
Remove or generalize:
- names
- dates
- times
- institutional identifiers
- student-specific references
- class-session logistics

### Drift audit
Check for:
- unsupported content
- invented assignments
- contradictions with stated lesson goals
- examples that expand scope without permission
- terminology not grounded in the lesson plan

### Voice calibration
Check for:
- too polished
- too academic
- too corporate
- too generic
- too verbose

## Batch mode

When the input contains multiple lessons:
- process each lesson independently
- do not leak curriculum from one lesson into another
- keep one folder per lesson
- preserve the same voice model across all lessons

## GitHub repo mode

If the source is a GitHub repo:
1. inspect repo structure first
2. locate lesson sources
3. write outputs into a predictable lesson folder
4. dry-run the file plan first when possible
5. commit when requested
6. push when requested

Recommended output path:
lessons/<lesson-slug>/
- examples.md
- slides.md
- speaker-notes.md
- quiz.md

## Ace Quiz Maker companion mode

Ace Quiz Maker is optional and supplemental.

Use it after the lesson assets are generated.

Generate:
- concept-check quizzes
- review quizzes
- instructor self-check quizzes

Do not use Ace Quiz Maker as the primary generator for:
- slides.md
- speaker-notes.md
- examples.md

Quiz content must come from:
- the lesson plan or topic outline
- generated examples
- generated slides

## Refusal and fallback rules

If no lesson plan or topic outline exists:
- do not invent a complete lesson silently
- offer a compact lesson scaffold first
- clearly label inferred structure as inferred

If privacy requirements cannot be satisfied:
- remove the unsafe details
- return a generalized version instead

## Success criteria

A successful run:
- preserves lesson authority
- uses the precomputed voice model rather than requiring transcript input
- sounds human
- stays practical and direct
- avoids academic and AI-polished drift
- produces examples, slides, and notes that align with the lesson plan
