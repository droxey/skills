# Dani Roxberry's Teaching Voice - Prompt Pack

Use the smallest subset needed.

## 1) Lesson normalizer

Task:
Read the lesson plan, topic outline, or source notes and extract the teaching structure.

Return:
- title
- audience if stated
- objectives
- core concepts
- sequence
- required examples
- constraints
- exclusions
- unknowns

Rules:
- treat the lesson plan or topic outline as content authority
- do not add curriculum not supported by the source
- keep the structure compact and explicit

## 2) Voice application guide

Task:
Apply the precomputed Dani Roxberry teaching voice to the normalized lesson without changing lesson scope.

Return:
- tone rules
- phrasing rules
- example rules
- suppression rules
- final checks

Rules:
- practical
- direct
- example-first
- engineering-grounded
- clear rather than polished
- avoid academic inflation and AI-generic language

## 3) Generate examples.md

Task:
Generate examples before slides.

Requirements:
- practical
- concrete
- directly supportive of the lesson objectives
- teachable live
- no new curriculum
- no institution-specific details

Structure:
# Examples
For each concept:
- concept
- example
- why it works
- common mistake if useful

## 4) Generate slides.md

Task:
Generate the deck from the normalized lesson and examples.

Requirements:
- one clear teaching job per slide
- concise text
- plainspoken phrasing
- examples where helpful
- no invented assignments
- no logistics
- no identifying details

Recommended structure:
- title
- why this matters
- concept slides
- example slides
- failure modes or comparison slides where useful
- recap

## 5) Generate speaker-notes.md

Task:
Generate speaker notes that expand delivery without changing curriculum.

For each slide include:
- teaching intent
- what to say
- where to slow down
- likely confusion
- transition to next slide

Requirements:
- natural spoken support
- practical and direct
- no drift
- no essay-style overexpansion

## 6) Privacy scrub

Task:
Review outputs for identifying or institution-specific details.

Remove or rewrite:
- names
- dates
- times
- student references
- course-section identifiers
- transcript-like quotation fragments

Return:
- scrubbed outputs
- short note listing what was generalized if anything was changed

## 7) Drift audit

Task:
Audit examples.md, slides.md, and speaker-notes.md against the lesson plan or topic outline.

Check for:
- unsupported content
- invented assignments
- examples that expand scope
- contradictions
- off-plan terminology

Return:
- status: pass or fail
- findings
- minimal required fixes

## 8) Final assembly

Finalize only if:
- drift audit passes
- privacy scrub passes
- voice calibration is acceptable

Return:
- examples.md
- slides.md
- speaker-notes.md
- short validation note

## 9) Ace Quiz Maker companion asset

Generate a short review quiz from the lesson plan, examples, and slides.

Requirements:
- 5 to 10 multiple-choice questions
- one short hint per question
- explanation for every answer option
- practical wording
- no trivia
- no institution-specific details
- no content not grounded in the lesson
