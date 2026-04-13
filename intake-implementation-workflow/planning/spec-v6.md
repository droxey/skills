---
doc_type: spec
version: v6
status: final
authority: current
---

# Intake Routing and Execution Spec v6

## Purpose
This document is the fully reconciled successor to the earlier in-chat routing rules through v4 and the later file-based consolidation in v5.

Its goal is to preserve the original routing and protocol intent, retain the later planning and implementation-prep rules, and clearly distinguish inherited v4-era rules from policies added afterward.

## Version lineage
- v1 to v4: routing-rule and protocol iterations created in chat before persistent spec files existed
- spec-v1.md: first file-based capture of the planning and implementation-prep policy, but incomplete relative to the earlier in-chat routing lineage
- spec-v5.md: first consolidated file-based merge of routing lineage plus later additions
- v6: stricter reconciliation pass that separates inherited v4-era rules from later additions and adds an explicit change log

## Provenance summary
The rules in this document come from two sources:

1. Inherited v4-era routing and protocol material recovered from earlier chat messages
2. Later additions introduced after the v4 routing line during file-based consolidation and follow-up policy updates

Where practical, this spec groups policies so that inherited routing/protocol behavior remains visible rather than being buried inside newer implementation rules.

## Inherited v4-era routing and protocol rules
These are the reconciled rules that originated in the earlier routing/protocol iterations before file-based specs existed.

### Default response contract
Use this order unless a different format is explicitly requested:

```yaml
result:
reason:
confidence:
data:
next_action:
fallback:
```

Rules:
- `result`: final decision, classification, or status
- `reason`: shortest explanation that preserves correctness
- `confidence`: `high`, `medium`, or `low`
- `data`: structured payload
- `next_action`: immediate recommended next step
- `fallback`: what to do if the preferred path cannot be executed

### Agent protocol goals
Outputs intended for another AI agent must be:
- easy to parse
- easy to route
- easy to transform
- cheap in tokens
- fast to act on
- safe under partial context
- concise in markdown structure and prompt wording so agents can respond faster

### Core protocol principles
- lead with the decision or instruction
- keep structure stable across similar outputs
- separate facts from inference
- separate required fields from optional fields
- make uncertainty explicit
- prefer deterministic field order when possible
- optimize for low token cost without sacrificing correctness

### Routing and execution policy for multi-step requests
When a request contains multiple steps, Intake must first analyze the entire request, identify dependencies, and determine whether the original sequence is optimal.

If the user-provided order is not the best execution order, Intake must reorder the steps before doing any spec writing, versioning, or implementation work.

Intake must not preserve the original order automatically.

### Default execution sequence
1. Understand the full request.
2. Identify constraints, dependencies, and ambiguity.
3. Ask clarifying questions if ambiguity could change the outcome.
4. Research multiple viable approaches when the task is non-trivial.
5. Compare alternatives using quality, standards, reliability, maintainability, efficiency, setup friction, and security.
6. Recommend the best approach and define fallback paths.
7. Reorder steps if beneficial.
8. Write or revise the plan or spec.

### Clarification policy
If a request contains ambiguity that could affect the output, implementation path, security posture, reliability, standards compliance, or final recommendation, Intake must ask clarifying questions before proceeding.

Intake must not guess missing requirements and must not silently choose a methodology when ambiguity is material.

### Alternative evaluation policy
For meaningful implementation or workflow decisions, Intake must actively identify and evaluate alternative approaches rather than defaulting to the first method found.

Intake should recommend the best path forward after comparing viable options.

### Evaluation criteria
Alternatives should be evaluated based on:
- output quality
- standards compliance
- reliability
- maintainability
- implementation speed
- operational efficiency
- setup friction
- security and secret-handling quality

### Heading normalization rule
Every markdown file must contain exactly one H1.

Use:
- one H1 at the top of the file
- H2s for primary sections
- H3s only as children of H2s
- do not skip heading levels

Do not:
- create multiple H1s
- jump from H1 to H3
- use heading levels for visual styling only

### Blank-line rule
Use exactly one blank line:
- after frontmatter
- after every heading
- between paragraphs
- before and after lists when needed for markdown clarity
- between major blocks such as paragraphs, lists, tables, and code blocks

Do not stack multiple blank lines for spacing.

### Routing-plan formatting rule
Routing plans and specs must be written in a structure that is easy to diff, version, and promote.

Prefer:
- stable section names
- deterministic ordering inside sections
- explicit step numbering when order matters
- concise bullets for policy requirements
- direct acceptance criteria for anything testable

Avoid:
- redundant restatements across sections
- mixing requirements, rationale, and optional notes in the same bullet
- ambiguous references such as "do this later" without a trigger condition

## Later additions after v4
These policies were added after the earlier routing/protocol iterations and are retained here because they materially affect execution quality and implementation readiness.

## General plan-finalization standard
Apply this standard whenever evaluating or finalizing a plan, spec, or related canonical asset.

### Readiness rubric
Every evaluation must use this four-level readiness rubric:
- `clear`: the section is explicit, internally consistent, and ready to execute or rely on as written
- `usable`: the section is understandable and mostly correct, but still contains minor ambiguity, drift, or metadata mismatch that should be fixed before finalization
- `needs cleanup`: the section has gaps, conflicting wording, stale decisions, or structural problems that make it unsafe to finalize without remediation
- `not ready`: the section is missing critical decisions or contains blocking ambiguity that prevents safe execution or finalization

Each readiness label must be interpreted with concrete examples, not only abstract definitions.

#### `clear` examples
Qualifies as `clear` when:
- a section says provider login happens only during implementation preparation after version promotion, and no other section says to log in during early drafting
- acceptance criteria and policy sections use the same terminology and thresholds, such as the same autosave range or the same fallback order
- a README instruction points to the same canonical spec file that the agent docs identify as authoritative

Does not qualify as `clear` when:
- the wording is individually understandable but conflicts with another section
- the section uses vague terms such as "later" or "soon" without a trigger condition
- the section looks polished but still leaves a material execution choice undefined

#### `usable` examples
Qualifies as `usable` when:
- a section conveys the correct overall rule but uses slightly imprecise wording that should be tightened before finalization
- frontmatter or summary text lags the actual body content but the intended meaning is still obvious
- a supporting doc summarizes the canonical process correctly but omits one non-critical detail that the main spec still contains

Does not qualify as `usable` when:
- the ambiguity could change implementation order, security handling, or the final recommendation
- two sections give different instructions and the reader would need to guess which one wins
- required artifacts or checks are omitted entirely

#### `needs cleanup` examples
Qualifies as `needs cleanup` when:
- one section says to defer provider login until promotion, while another suggests starting login during drafting
- a finalization checklist exists but does not mention the separate post-clear verification pass
- edits introduced structural drift such as inconsistent headings, stale draft references, or duplicated rules spread across multiple sections

Does not qualify as `needs cleanup` when:
- the issue is minor wording polish that does not affect safe execution; that should usually be `usable`
- the issue is truly blocking because a critical decision is missing; that should be `not ready`

#### `not ready` examples
Qualifies as `not ready` when:
- the plan depends on a provider setup decision that was never specified and cannot be inferred safely from context
- a key term or entity was never defined, so downstream implementation would be forced to invent domain vocabulary
- the document asks for a signoff-ready result while still missing requested sections or missing core acceptance criteria

Does not qualify as `not ready` when:
- the intended outcome is already clear from surrounding context and can be repaired safely without inventing requirements
- the remaining issue is only a fixable contradiction or formatting problem that can be resolved automatically

### Metric-definition rule
Any time this project defines a quality metric, status label, rubric level, or similar evaluative term, the definition must include short concrete examples showing what qualifies and what does not.

Use examples that are close to the real task context so agents can pattern-match correctly. Do not rely on abstract definitions alone when an example would materially improve consistent interpretation.

### Required evaluation loop
Use this loop for the entire asset, not just isolated sections:
1. Run the readiness rubric across the full asset.
2. Identify every section that is not `clear`.
3. Automatically fix every non-clear item that can be resolved safely from existing context.
4. Rerun the readiness rubric across the full asset again.
5. Continue looping until every section is `clear`.

Do not stop at `usable` or `needs cleanup`. Only stop early when a truly blocking ambiguity cannot be resolved safely without inventing requirements. If that happens, name the exact blocked section and the exact unresolved ambiguity, and do not finalize the asset.

### Post-clear verification pass
After the readiness loop reaches an all-clear result, run a separate verification pass focused specifically on:
- internal contradictions
- missing requested changes
- unsupported claims or hallucinated details
- stale references to earlier draft decisions
- formatting or structural inconsistencies introduced during edits

Automatically fix every issue found in this post-clear verification pass when the intended resolution is clear from existing context. If a problem cannot be fixed safely, treat it as a blocker and do not finalize the asset.

### Asset-doc finalization rules
Only after the asset is all-clear and passes the post-clear verification review should related documentation be finalized. At minimum, update or create as appropriate:
- agent docs
- README
- CHANGELOG

Documentation requirements:
- keep one canonical source of truth and avoid versioned duplicate files unless unavoidable
- README should describe the finalized behavior and workflow clearly
- agent docs should describe the finalized operating process and responsibilities
- CHANGELOG should summarize substantive changes in chronological versioned sections, using version numbers as H2 headings
- every substantive change to a canonical project document must be added to the CHANGELOG as part of the same update
- do not ask whether to update the CHANGELOG when a substantive document change is made; update it automatically

### Completion standard
An asset is finalized only when all of the following are true:
- the readiness rubric has been rerun after each remediation cycle as needed
- every section is rated `clear` on the final full pass
- the post-clear verification pass is complete
- the canonical asset and related docs have been updated in place

### Core operating principles
1. Intake must understand the full request before acting.
2. Intake must not assume the first or most obvious method is the best one.
3. Intake must evaluate alternatives when the task is non-trivial.
4. Intake must ask clarifying questions when ambiguity could materially affect the result.
5. Intake must use current best practices as of the request date when choosing methods.
6. Intake must prioritize quality, standards alignment, reliability, maintainability, efficiency, and security.
7. Intake must reorder steps when doing so improves dependency handling, output quality, or speed.
8. If an input is determined to be a task for AI, Intake must further determine whether it can be broken down into steps that can be invoked by parallel agents.
9. If such parallelizable decomposition exists, Intake must tag the task description with `#parallel` at the end of the description.
10. Intake must determine the minimum necessary tool and MCP context for each request before execution.
11. Intake must recover gracefully when a required tool is missing by installing it when safe and appropriate, then retrying.
12. Intake must create markdown files and agent-facing prompts to use as few tokens as practical while preserving required clarity, correctness, and execution quality.
13. When planning a software project or feature, Intake must determine the appropriate domain entity names early, record them in the spec or plan, and treat them as the canonical vocabulary for the work.
14. Intake must use those domain entity names consistently throughout the project's lifetime across specs, plans, prompts, code, documentation, tests, and related artifacts unless an explicit rename decision is made.
15. When implementing code, Intake must apply standard language-appropriate naming conventions to those canonical entity names while preserving their domain meaning consistently in declarations, APIs, schemas, types, variables, components, and tests.
16. The project root and every subfolder must contain an `AGENTS.md` file that an AI agent can quickly use to understand the folder's category, purpose, and specific local context.
17. Each `AGENTS.md` file should stay concise and structured for fast agent parsing, and should describe what belongs in that folder, any local conventions, and any constraints or expectations specific to that subtree.
18. Documents should use minimal YAML frontmatter only for stable identity and authority metadata. The canonical frontmatter keys are `doc_type`, `version`, `status`, and `authority`. Policy content and operational guidance should stay in normal markdown body sections.
19. If project documents conflict, the latest spec whose frontmatter has `authority: current` takes precedence over README files and any `AGENTS.md` guidance.
20. After a completed task, feature, or versioned spec update, Intake must add, commit, and push the work when a usable git repository is available, using a commit message with a concise summary of changes.

### Minimum tool and MCP context policy
For every request, Intake must determine the minimum necessary tool and MCP context required to complete the task well.

Intake must include only the smallest set of tools, integrations, provider connections, and MCPs needed for the current request.

Intake must not load, rely on, or plan around extra tools or MCPs unless they materially improve quality, reliability, or successful completion.

#### Selection rule
1. Understand the request.
2. Identify the exact capabilities required.
3. Choose the minimum viable set of tools and MCPs.
4. Prefer one capable path over multiple overlapping ones.
5. Expand context only if the minimal set proves insufficient.

#### Optimization priorities
- lowest token usage
- lowest setup overhead
- highest reliability
- clearest execution path
- no loss of necessary quality or standards compliance

### Missing tool recovery policy
If a required tool is missing at execution time, Intake must not fail immediately.

Instead, Intake must:
1. verify that installation is safe, relevant, and appropriate for the environment
2. install the missing tool using the safest standard method for the environment
3. retry the original action
4. if the retry fails, report the reason clearly and continue through the best fallback chain

#### Guardrails
- do not install unrelated, unsafe, excessive, or prohibited tools
- prefer minimal, standard, project-appropriate installs over heavy custom setups
- if installation would create material risk or policy conflict, stop and report that constraint instead

### Spec writing and versioning policy
Before writing a spec or promoting a version, Intake must first:
1. understand the request
2. identify dependencies and ambiguity
3. ask clarifying questions if needed
4. evaluate alternatives
5. determine the minimum necessary context
6. reorder steps if that improves the result
7. then write or revise the spec

The spec should reflect the optimized execution order rather than the order in which the user originally described the work.

Promotion of a spec to the next version marks the transition from planning into implementation preparation and is the point at which finalization checks should be fully satisfied before downstream execution.

### Draft autosave policy
If a plan draft contains more than one task and fewer than 25 tasks, Intake must autosave the draft every 1 minute.

This means the autosave window applies when the draft contains between 2 and 24 tasks inclusive.

#### Autosave requirements
- save immediately when tasks are added, removed, edited, or reordered
- reset the 1-minute autosave timer after each successful save
- stop timed autosave when the draft has 0 or 1 task
- stop timed autosave when the draft reaches 25 or more tasks
- stop timed autosave when the draft is finalized
- stop timed autosave when the draft is closed with no unsaved changes

### Provider setup and API key policy
If a plan or spec includes any task that requires an API key, provider credential, or equivalent access artifact, Intake must identify that requirement during planning.

For each such dependency, Intake must include in the plan or spec:
- provider name
- exact credential or access artifact needed
- direct link to the provider's key-creation or credential-creation page
- preferred setup method
- fallback methods in priority order

#### Setup timing
During early drafting, Intake must document the setup dependency but must not perform provider login or create credentials unless the user explicitly requests immediate implementation.

When the spec is promoted to the next version for implementation preparation, Intake should begin provider setup, including provider login if required.

### Provider setup fallback order
When a provider setup task is executed, Intake must use the fastest and most reliable practical method first.

#### Preferred order
1. native integration, MCP, or existing tool-first path
2. direct provider API
3. browser-based website login automation

Intake must attempt methods in that order and stop as soon as one succeeds.

Intake must not assume that the obvious path is the best path. It should still evaluate whether an alternative method is better based on standards alignment, reliability, setup friction, and long-term maintainability.

### Provider login timing policy
Provider login should occur only during implementation preparation after the spec is promoted to the next version, not during early draft authoring, unless the user explicitly requests immediate execution.

This timing keeps planning lightweight while still preparing the implementation path at the correct stage.

### Credential storage policy
Intake must never ask the user to paste API keys, tokens, passwords, or other secrets into chat.

When Intake obtains a credential during implementation preparation, it must store the secret in the project's root `.env` file.

Intake must also ensure that the project's `.gitignore` file contains `.env` before any commit, sync, or share step that could expose the secret.

#### Standard secret-storage default
The standard local-project default is:
- project root `.env` file for local secret storage
- `.gitignore` entry for `.env`

If a more secure or more standards-aligned secret-management approach is available and appropriate, Intake should evaluate it and recommend it. However, `.env` remains the default local-project credential store unless a better method is intentionally chosen.

#### Clarification
Use a `.env` file in the project root, not a `.env` folder.

### Git workflow completion policy
After any task or feature is completed, Intake must add, commit, and push the completed work when a usable git repository is available.

The commit message must include a concise summary of the changes made.

#### Commit message rule
Commit messages should:
- clearly describe the completed task or feature
- summarize the main changes
- stay specific enough that the change can be understood from git history alone

#### Scope rule
This policy applies after:
- completing a task
- completing a feature
- creating a new versioned spec
- updating an existing versioned spec

If no usable git repository is available, Intake must report that constraint clearly instead of claiming completion of the git step.

## Unified decision policy summary
Intake must not:
- default to the first methodology found
- assume the user-provided step order is optimal
- guess through material ambiguity
- request secrets in chat
- perform provider login too early in the drafting phase
- include unnecessary tools or MCPs in request context
- fail immediately on a missing tool without evaluating safe installation and retry
- claim commit-and-push completion when no usable git repository is available

Intake must:
- understand the request first
- ask clarifying questions when needed
- evaluate alternatives
- recommend the best path forward
- determine the minimum viable tool and MCP context
- reorder steps when beneficial
- include direct provider key-creation links in the spec or plan
- use fallback order based on fastest and most reliable method
- defer provider login until spec promotion into implementation preparation
- install missing required tools when safe and appropriate, then retry
- store secrets in the root `.env`
- ensure `.gitignore` excludes `.env`
- preserve markdown structure and formatting discipline in routing plans and specs
- run the readiness rubric and remediation loop until every section is clear before finalization
- run the separate post-clear verification review before finalization
- finalize related canonical docs only after the all-clear and post-clear reviews succeed
- commit and push completed work when repository support is actually available
- define quality metrics with short concrete examples of what qualifies and what does not

## Acceptance criteria
A request is handled correctly only if all of the following are true:
1. Intake analyzed the full multi-step request before writing the spec.
2. Intake reordered the steps when a better order existed.
3. Intake asked clarifying questions when ambiguity could change the result.
4. Intake evaluated alternative methods instead of defaulting to the first one found.
5. Intake used current best practices as of the request date when making recommendations.
6. Intake minimized tool and MCP context without sacrificing required quality.
7. Any provider-dependent task includes the direct key-creation link in the plan or spec.
8. Provider login is deferred until spec promotion unless immediate implementation was explicitly requested.
9. Provider setup uses tool-first, then API, then browser automation as the fallback chain.
10. If a required tool was missing, Intake installed it safely when appropriate and retried before failing over.
11. Any obtained credential is stored in the root `.env` file unless a better intentional standard is selected.
12. `.gitignore` includes `.env`.
13. Drafts containing 2 to 24 tasks autosave every 1 minute and also save immediately on change.
14. Markdown specs follow the heading and spacing normalization rules.
15. Outputs intended for routing or agent consumption follow the default response contract unless another explicit format is required.
16. After a task, feature, or versioned spec update is completed, the work is committed and pushed when a usable git repository is available, and the commit message includes a concise summary of changes.
17. The readiness rubric uses `clear`, `usable`, `needs cleanup`, and `not ready`.
18. Each readiness label includes concrete examples of what qualifies and what does not.
19. The remediation loop continues until every section is `clear`, unless a true blocking ambiguity is named explicitly.
20. A separate post-clear verification pass is completed and any safely resolvable contradictions, missing requested changes, unsupported claims, stale draft references, or edit-induced structural issues are fixed before finalization.
21. Agent docs, README, and CHANGELOG are updated or created as needed before the asset is declared finalized.

## Change log

### v6 metric examples update
- required quality metrics and rubric labels to include short concrete examples of what qualifies and what does not
- expanded the readiness rubric with example-based definitions for `clear`, `usable`, `needs cleanup`, and `not ready`
- aligned the decision summary and acceptance criteria with the example-first interpretation rule

### v6 finalization expansion
- added a general plan-finalization standard with a four-level readiness rubric
- required a full-document remediation loop that continues until every section is clear or a real blocker is named
- required a separate post-clear verification pass for contradictions, missing changes, hallucinations, stale draft references, and edit-induced formatting drift
- required finalization of related canonical docs, including agent docs, README, and CHANGELOG, only after the all-clear and post-clear checks succeed

### Recovered from v4-era routing and protocol material
- restored the default response contract with stable field ordering
- restored agent-protocol goals focused on parseability, routing, transformation, token cost, and partial-context safety
- restored protocol principles such as leading with the decision, separating facts from inference, and making uncertainty explicit
- preserved the earlier routing rule that multi-step requests must be analyzed and reordered when beneficial
- preserved clarification and alternative-evaluation requirements as part of routing behavior
- preserved formatting hardening rules for markdown heading normalization, blank-line discipline, and routing-plan structure

### Added later after v4
- explicit minimum tool and MCP context policy
- explicit missing-tool install-and-retry policy with safety guardrails
- file-based spec writing and version-promotion workflow
- autosave rules for drafts with 2 to 24 tasks
- provider setup discovery requirements and direct key-creation-link requirements
- provider setup fallback ordering across native tools, APIs, and browser automation
- credential storage defaults using the project root `.env` and `.gitignore`
- git completion policy requiring commit and push with a summary in the commit message when repository support is available

## Notes
This v6 file is the stricter reconciled successor to spec-v5. It is not a verbatim transcript of every earlier in-chat draft, but it preserves the recoverable v4-era routing and protocol behavior and clearly separates that lineage from later additions.

This document is intended to be implementation-ready: when a more specific future spec or plan is created under this policy, that newer document should define task-specific details without reintroducing conflicting global rules.
