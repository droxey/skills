---
name: skill-router-v2
description: Use when routing among globally installed skills to pick the right one for a task.
maturity: 0
---

# Skill Router v2

You have 69 skills. Many share trigger words (`code`, `review`, `test`, `grill`, `write`, `plan`, `spec`, `tickets`). This router uses a **decision tree** — answer each question and it narrows to the exact skill. Each decision point targets a known overlap cluster.

## Decision tree

Start at the top and descend. Each question has exactly one answer.

```
Q1: WHAT kind of work is this?
├─ IDEA → SHIP (I want to build something)        → go to Q2
├─ SOMETHING BROKEN (bug, flake, regression)       → go to Q8
├─ REVIEW / AUDIT (existing work to evaluate)      → go to Q9
├─ WRITE / EDIT (prose, article, skill, lesson)    → go to Q10
├─ RESEARCH / DISCOVER (find information)          → go to Q13
├─ GRILL / INTERVIEW (sharpen thinking)            → go to Q14
├─ TEACH (learn or teach a concept)                → `teach`
├─ SETUP / CONFIGURE (bootstrap tooling)           → go to Q16
├─ TRIAGE / TRIAGE INCOMING (sort raw issues)      → `triage`
├─ MEETING NOTES → ACTION ITEMS                    → `meeting-to-action`
├─ LINKEDIN PROSPECTING / OUTREACH                 → `linkedin-lead-gen-outreach`
├─ RESUME OPTIMIZATION (tailor to job description) → `resume-ats-pdf-optimizer`
└─ SOMETHING ELSE (tell me more)                   → go to Q18

Q2: IDE SIZE — how big is the build?
├─ SINGLE TICKET (well-scoped, fits in one session) → `implement`
├─ MULTI-SESSION (spec then tickets then build)     → `to-spec` then `to-tickets` then `implement` per ticket
└─ FOGGY / UNCLEAR (can't see the path yet)         → `wayfinder` (maps decisions first, then hands off to `to-spec`)

Q3: BEFORE implementing — sharpen the idea?
├─ HAVE A CODEBASE (project exists) → `grill-with-docs` (stateful: saves CONTEXT.md + ADRs)
└─ NO CODEBASE (greenfield / design) → `grill-me` (stateless: no files saved)

Q4: DURING implementation — phase-sensitive guardrails.
├─ BEFORE creative work starts → `brainstorming` (explore intent, requirements, design)
├─ BEFORE writing code → `writing-plans` (turn spec into step-by-step plan)
├─ DURING implementation (many independent tasks) → `subagent-driven-development` (parallel sub-agents)
├─ DURING implementation (need isolated workspace) → `using-git-worktrees` (create worktree)
├─ BEFORE committing / declaring done → `verification-before-completion` (run tests, confirm output)
├─ AFTER implementation, BEFORE PR → `requesting-code-review` (self-review against requirements)
└─ AFTER receiving review feedback → `receiving-code-review` (verify feedback before acting)

Q5: MERGE / INTEGRATE — how to finish the branch?
├─ All tests pass, ready to integrate → `finishing-a-development-branch` (decide merge/PR/cleanup)
└─ Hit a merge/rebase conflict → `resolving-merge-conflicts`

Q6: CROSSING SESSIONS — need to move work between sessions?
├─ Compact conversation FOR A NEW SESSION (write to file, continue later) → `handoff`
└─ Hand off to a BACKGROUND AGENT in the SAME session (immediate continuation) → `claude-handoff`

Q7: DISPATCH PARALLEL WORK — many independent tasks right now?
├─ 2+ tasks, no shared state, no dependencies → `dispatching-parallel-agents`
└─ Sequential tasks with dependencies → stay inline or use `executing-plans` (separate session with checkpoints)

Q8: BROKEN — what kind of bug?
├─ HARD BUG (intermittent, regression, resists first glance) → `diagnosing-bugs` (tight feedback loop first)
├─ ANY BUG / TEST FAILURE / UNEXPECTED BEHAVIOR → `systematic-debugging` (before proposing fixes)
└─ Bug found during review, need to verify fix → `verification-before-completion`

Q9: REVIEW / AUDIT — what are you reviewing?
├─ A PR OR BRANCH (someone else's code, two-axis Standards+Spec review) → `code-review`
├─ YOUR OWN CODE before requesting review → `requesting-code-review`
├─ REVIEW FEEDBACK you just received → `receiving-code-review`
├─ EXISTING CODEBASE HEALTH (find deepening opportunities) → `improve-codebase-architecture`
├─ DOMAIN LANGUAGE / TERMINOLOGY (fuzzy terms, overloaded words) → `domain-modeling`
└─ MODULE INTERFACE DESIGN (deep-module vocabulary) → `codebase-design`

Q10: WRITE / EDIT — what kind of writing?
├─ AUTHOR A NEW SKILL.md → `writing-skills` (workflow: create, edit, verify)
├─ REFERENCE for writing skills well → `writing-great-skills` (vocabulary and principles)
├─ CREATIVE WRITING / ARTICLE — what stage?
│   ├─ FIRST STAGE: mine raw fragments, no structure → `writing-fragments`
│   ├─ MIDDLE STAGE: assemble fragments into beats → `writing-beats`
│   └─ FINAL STAGE: shape into article, paragraph by paragraph → `writing-shape`
├─ EDIT / IMPROVE an existing article → `edit-article`
├─ REMOVE AI PATTERNS from text (make it sound human) → `humanize`
├─ ROUTE MARKDOWN to teaching or general format → `markdown-mode-router`
└─ GENERATE LESSON ASSETS in Dani's teacher voice → `dani-roxberrys-teaching-voice`

Q11: CODE — structured coding workflow?
├─ FULL WORKFLOW (discuss, plan, spec, test-first, verify, review, mutation test, docs) → `code`
└─ TEST-FIRST DEVELOPMENT (red-green-refactor cycle) → `tdd` (Matt Pocock) OR `test-driven-development` (Superpowers) — functionally equivalent, pick either

Q12: PROTOTYPE — need a throwaway answer?
├─ Design question needs runnable answer (state model, UI feel) → `prototype` (keep answer, delete code)
└─ Interactive bash wizard for a manual procedure → `wizard`

Q13: RESEARCH / DISCOVER — what are you looking for?
├─ INVESTIGATE a question against primary sources → `research` (background agent, leaves cited markdown)
├─ WEB SCRAPING (multi-strategy extraction) → `web-scraper`
├─ WEB RETRIEVAL FAILED (curl/search blocked) → `chrome-mcp-web-fallback`
├─ CLONE / REPLICATE a website or UI → `clone-ui` OR `product-clone-research` (reconnaissance first)
├─ SEARCH / MANAGE Obsidian vault notes → `obsidian-vault`
├─ MODEL COST ESTIMATION → `model-cost-estimator`
└─ FLEET AUDIT (toolkit overlap, stale agents, missing skills) → `fleet-audit-patterns`

Q14: GRILL / INTERVIEW — what are you sharpening?
├─ A PLAN OR DESIGN (stateless, no codebase needed) → `grill-me`
├─ A PLAN OR DESIGN (stateful, have a codebase, saves ADRs) → `grill-with-docs`
├─ A DECISION OR IDEA (not a plan, just questioning) → `grilling`
├─ EVERY QUESTION AT ONCE (maximum coverage, minimum rounds) → `batch-grill-me`
└─ SPECS FOR WORKFLOWS (within this Nebula workspace) → `loop-me`

Q15: SPEC / TICKETS — what stage of planning?
├─ TURN CONVERSATION INTO A SPEC (no interview, just synthesis) → `to-spec`
├─ BREAK A SPEC INTO TRACER-BULLET TICKETS (with blocking edges) → `to-tickets`
├─ TURN A DECISION INTO A QUESTIONNAIRE (for someone else) → `to-questionnaire`
└─ CHART A FOGGY EFFORT (decision tickets first, then hand off to to-spec) → `wayfinder`

Q16: SETUP / CONFIGURE — what are you setting up?
├─ GIT HOOKS (pre-commit with lint-staged, type checking, tests) → `setup-pre-commit`
├─ GIT SAFETY (block dangerous commands: push, reset --hard, clean) → `git-guardrails-claude-code`
├─ DEEP MODULES (wire dependency-cruiser into TypeScript repo) → `setup-ts-deep-modules`
├─ SHOEHORN MIGRATION (migrate `as` assertions to @total-typescript/shoehorn) → `migrate-to-shoehorn`
├─ EXERCISE SCAFFOLD (create section/problem/solution/explainer directories) → `scaffold-exercises`
├─ REPO SETTINGS-AS-CODE (.github/settings.yml, governance defaults) → `repo-settings-bootstrap`
├─ NEXT.JS MINIAPP (build or review in Nebula sandbox) → `nextjs-nebula-miniapp`
├─ GITHUB WORKSPACE MODE (pick lightest mode: Codespaces vs other) → `codespace-operator-v2`
└─ INTAKE PRODUCT WORKFLOW → `intake-implementation-workflow`

Q17: DEVOPS — infrastructure work?
├─ ARCHITECTURE / DESIGN decisions → `ah-devops-engineer`
└─ IMPLEMENTATION (CI/CD pipelines, automation scripts) → `senior-devops`

Q18: SOMETHING ELSE — more specialized.
├─ MOBILE FORENSICS (SQLite carving, plist parsing, chat extraction) → `mobile-forensics`
├─ PROMPT TECHNIQUE (pick best prompting strategy for a task) → `prompt-technique-router`
├─ SKILL INVOCATION PROTOCOL (find+use skills before any response) → `using-superpowers`
└─ DOMAIN MODELING (ubiquitous language glossary, flag ambiguities) → `domain-modeling`
```

## Disambiguation rules for known overlap clusters

When two skills could both match, use these tiebreakers:

### Grill family (grill-me vs grill-with-docs vs grilling vs batch-grill-me vs loop-me)
- **Has a codebase?** → `grill-with-docs` (stateful). No codebase → `grill-me` (stateless).
- **Sharpening a DECISION (not a plan)?** → `grilling`.
- **Want every question at once?** → `batch-grill-me`.
- **Specs for Nebula workflows?** → `loop-me`.

### Code review (code-review vs requesting-code-review vs receiving-code-review)
- **Reviewing SOMEONE ELSE'S branch/PR?** → `code-review`.
- **About to submit YOUR OWN work for review?** → `requesting-code-review` (BEFORE).
- **Just received feedback on YOUR work?** → `receiving-code-review` (AFTER).

### Handoff (handoff vs claude-handoff)
- **Want a FILE to reference in a NEW session later?** → `handoff` (cross-session bridge).
- **Want a BACKGROUND AGENT to pick up RIGHT NOW?** → `claude-handoff` (same-session).

### Test-driven (tdd vs test-driven-development)
- Functionally equivalent — pick either. Both implement red-green-refactor.

### DevOps (ah-devops-engineer vs senior-devops)
- **Designing architecture / making decisions?** → `ah-devops-engineer`.
- **Implementing pipelines / writing automation?** → `senior-devops`.

### Spec flow (to-spec vs to-tickets vs implement)
- **Step 1: CONVERSATION → SPEC** → `to-spec`.
- **Step 2: SPEC → TICKETS (with blocking edges)** → `to-tickets`.
- **Step 3: TICKET → CODE (TDD internally)** → `implement`.
- Never skip steps — `wayfinder` feeds into `to-spec`, never directly into `implement`.

### Writing (writing-fragments vs writing-beats vs writing-shape)
- **Stage 1: gathering raw material** → `writing-fragments`.
- **Stage 2: structuring into beats** → `writing-beats`.
- **Stage 3: polishing into final article** → `writing-shape`.
- **Editing existing prose** → `edit-article`.
- **Authoring a SKILL.md** → `writing-skills` / `writing-great-skills`.

## How to use this router

1. Read `skill-router-v2` when you're unsure which skill to reach for.
2. Start at Q1 and descend the decision tree — each answer narrows the field.
3. When you land on a skill, `read_skill(name=...)` to load its full instructions.
4. If the tree doesn't cover your task, use the tiebreaker rules for known clusters.
5. If still unmatched, `read_skill(name='skill-router-v2')` again and trace from Q18.

## Maturity

Level 0 - Intent. Substantiated by the written contract only; no runnable asset or tests yet.

## Purpose

Route a task to the correct installed skill via a decision tree.

## Inputs

The task and the set of installed skills.

## Outputs

A single best-fit skill selection.

## Example

Classify a request and traverse the router to select the one skill that covers it.

## Success criteria

Exactly one skill is selected and it demonstrably covers the request.