# Dani Roxberry's Teaching Voice

Generate lesson assets in Dani Roxberry's teaching voice from a lesson plan, topic outline, or source materials without requiring a transcript at runtime.

## What it produces

Primary outputs:
- slides.md
- speaker-notes.md
- examples.md

Optional companion outputs:
- quiz content for Ace Quiz Maker
- voice-report.md
- drift-report.md
- privacy-audit.md

## Core model

This skill uses a precomputed voice model.

A transcript was useful to derive the voice profile once. It is not required for normal runs.

At runtime:
- lesson plan or topic outline = content authority
- Dani Roxberry teaching voice = style layer

That separation prevents lesson drift while keeping the output human and consistent.

## Operating rules

Content authority order:
1. lesson plan or topic outline
2. explicit user constraints
3. supporting lesson materials provided for the same lesson

Voice authority:
- precomputed Dani Roxberry teaching voice model

Never use voice guidance to add curriculum.

## Voice target

The output should feel:
- practical
- direct
- example-first
- engineering-grounded
- clear rather than polished
- strong on verification, tradeoffs, and failure modes

Suppress:
- academic inflation
- corporate tone
- generic AI phrasing
- overproduced polish
- vague abstraction

## Standard workflow

1. normalize the lesson plan
2. apply the precomputed voice model
3. generate examples.md
4. generate slides.md
5. generate speaker-notes.md
6. run privacy scrub if needed
7. run drift audit
8. optionally generate quiz companion
9. finalize

## Install

### ChatGPT web/app
1. Add the `dani-roxberrys-teaching-voice` folder to your skills library or upload the bundle where your agent can read it.
2. Keep `SKILL.md`, `prompts.md`, and `AGENTS.md` together.
3. Invoke with: `Use Dani Roxberry's Teaching Voice for this lesson.`

### Codex web/cli
1. Place the folder in your global or project skills directory.
2. Ensure `SKILL.md` is present at the skill root.
3. Invoke with: `Use the dani-roxberrys-teaching-voice skill to generate lesson assets from this plan.`

### Claude Code web/app
1. Add the folder to your shared or project skill path.
2. Keep `AGENTS.md` alongside `SKILL.md`.
3. Invoke with: `Use Dani Roxberry's Teaching Voice to produce slides, notes, and examples.`

### Claude Code CLI
1. Copy the skill folder into your CLI-visible skills directory.
2. Keep the bundle flat and self-contained.
3. Invoke with: `Use the dani-roxberrys-teaching-voice skill on this lesson plan.`

## Example invocation

Use Dani Roxberry's Teaching Voice.

Inputs:
- lesson plan: [paste or attach]
- topic outline: [optional]
- constraints: [optional]

Generate:
- examples.md
- slides.md
- speaker-notes.md

Rules:
- lesson plan or topic outline is the source of truth
- apply the precomputed Dani Roxberry teaching voice
- do not invent curriculum
- keep the result practical, direct, and example-first
- avoid sounding too polished or too academic
- run drift audit before finalizing

## Ace Quiz Maker example

Copy/paste prompt:

```text
@Ace Quiz Maker Create a 6-question multiple-choice review quiz from the attached slides.md and examples.md generated with Dani Roxberry's Teaching Voice. Focus on core concepts, use practical wording, include one short hint per question, and provide explanations for every answer option.
```

## GitHub repo mode

When working from a repo:
1. inspect the repo structure first
2. locate lesson sources
3. write outputs into the lesson folder
4. dry-run where possible
5. commit when requested
6. push when requested

## Limitations

Do not rely on transcript-only material for normal runs.

If no lesson plan or topic outline exists:
- build a scaffold first
- clearly mark inferred content as inferred
- do not pretend the lesson is fully specified

## Validation standard

A run is valid when:
- lesson authority is preserved
- the precomputed voice model was applied
- privacy scrub passed if needed
- drift audit passed
- the outputs sound human, practical, and teachable
