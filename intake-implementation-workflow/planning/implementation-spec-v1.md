---
doc_type: implementation_spec
version: v1
status: draft
authority: derived
---

# Intake Implementation Spec v1

## Purpose

This document translates the governance rules in `spec-v6.md` into a task-specific implementation spec for the Intake system itself.

The implementation target is a working Intake engine that can analyze requests, normalize them into canonical task structures, evaluate alternatives, enforce project governance, and emit execution-ready plans and specs.

If this document conflicts with `spec-v6.md` on global governance policy, `spec-v6.md` wins. If later implementation details conflict with README or AGENTS docs, this document wins for system design and build behavior.

## System goal

Build Intake as a project-scoped planning and execution-preparation system that:
- ingests a user request
- determines whether clarification is required
- evaluates alternative approaches when needed
- canonicalizes domain vocabulary early
- produces implementation-ready outputs with stable structure
- enforces documentation, credential-handling, and finalization policy

## Scope

### In scope
- request intake and normalization
- ambiguity detection and clarification gating
- alternative evaluation for non-trivial requests
- canonical domain entity registration and reuse
- execution-step dependency analysis and reordering
- minimum required tool-context selection
- missing-tool recovery planning
- provider dependency discovery and setup planning
- document finalization workflow enforcement
- changelog enforcement for substantive canonical document changes
- generation of plans, specs, and agent-facing outputs

### Out of scope
- executing provider logins during early drafting
- storing secrets outside the project-standard secret path without an explicit decision
- general-purpose code execution unrelated to Intake planning behavior
- replacing downstream task-specific implementation systems
- hidden state mutation outside documented project artifacts

## Canonical domain entities

These names are the canonical vocabulary for the Intake implementation. Use them consistently across code, docs, tests, prompts, schemas, and logs.

### Request
The raw user ask before Intake processing.

Qualifies as a `Request` when:
- it is the direct input received from a user or upstream agent
- it may contain multiple steps, ambiguities, constraints, or missing details

Does not qualify as a `Request` when:
- it is already normalized into internal structured fields; that becomes an `IntakeRecord`
- it is a generated execution artifact such as a plan or spec

### IntakeRecord
The normalized internal representation of a Request.

Qualifies as an `IntakeRecord` when:
- it captures the parsed request, constraints, dependencies, ambiguity status, and normalized terminology
- it is stable enough for downstream evaluation and planning

Does not qualify as an `IntakeRecord` when:
- it only stores the original freeform text without normalization
- it skips required fields such as dependency or ambiguity state

### ClarificationIssue
A material ambiguity or missing decision that could change outcome, safety, implementation path, or recommendation.

Qualifies as a `ClarificationIssue` when:
- different reasonable interpretations would change the result
- security, standards, or execution order would differ depending on the missing answer

Does not qualify as a `ClarificationIssue` when:
- the missing detail is cosmetic and can be resolved safely from context
- the ambiguity does not affect implementation or decision quality

### AlternativeOption
A viable candidate approach considered during non-trivial decision-making.

Qualifies as an `AlternativeOption` when:
- it is realistically implementable
- it can be compared using the evaluation criteria defined by governance

Does not qualify as an `AlternativeOption` when:
- it is purely hypothetical and not execution-worthy
- it duplicates another option with no meaningful distinction

### EvaluationReport
The structured comparison of AlternativeOptions and the selected recommendation.

Qualifies as an `EvaluationReport` when:
- it records compared options, criteria, chosen path, and fallback path
- it makes uncertainty explicit where needed

Does not qualify as an `EvaluationReport` when:
- it states a conclusion without comparing alternatives for a non-trivial task
- it omits why the preferred path won

### DomainEntity
A canonical business or project concept chosen early and reused consistently.

Qualifies as a `DomainEntity` when:
- it names a stable concept such as Request, PlanArtifact, or ProviderDependency
- it is intended to remain consistent across code and docs

Does not qualify as a `DomainEntity` when:
- it is an ad hoc synonym introduced casually in one section
- it is a temporary label with no canonical intent

### ProviderDependency
A third-party service requirement needed for a task or plan.

Qualifies as a `ProviderDependency` when:
- a provider, credential, or access artifact is required
- setup method and key-creation link can be identified

Does not qualify as a `ProviderDependency` when:
- the task is fully local and requires no external provider
- the provider mention is incidental and not required for completion

### ToolContext
The minimum tool, integration, or provider context required for successful execution.

Qualifies as a `ToolContext` when:
- it contains only the necessary capabilities for the request
- it can justify why each included tool or connection is needed

Does not qualify as a `ToolContext` when:
- it includes unused or overlapping capabilities by default
- it is vague about which capabilities are required

### ExecutionStep
An ordered action in the optimized path from analysis to deliverable output.

Qualifies as an `ExecutionStep` when:
- it has a clear purpose and dependency position
- it can be reordered based on quality or dependency needs

Does not qualify as an `ExecutionStep` when:
- it is only a loose idea with no trigger or role in the flow
- it duplicates another step unnecessarily

### PlanArtifact
A structured implementation or execution plan generated by Intake.

Qualifies as a `PlanArtifact` when:
- it describes ordered work, dependencies, and acceptance conditions
- it is intended for execution or review

Does not qualify as a `PlanArtifact` when:
- it is only a brainstorm list with no execution structure
- it lacks enough detail to guide implementation

### SpecArtifact
A structured canonical specification generated or maintained by Intake.

Qualifies as a `SpecArtifact` when:
- it defines authoritative behavior, constraints, and acceptance criteria
- it is intended to guide implementation or finalization

Does not qualify as a `SpecArtifact` when:
- it is an informal note or scratch draft
- it lacks authority, scope, or acceptance criteria

### FinalizationReview
The full-document readiness loop plus post-clear verification pass.

Qualifies as a `FinalizationReview` when:
- every section is checked against the readiness rubric
- non-clear items are remediated until clear or a true blocker is named
- a separate verification pass checks contradictions, missing changes, unsupported claims, stale references, and edit drift

Does not qualify as a `FinalizationReview` when:
- the document is reviewed only once without remediation
- the separate post-clear verification pass is skipped

## Functional requirements

1. Intake must accept a Request and create an IntakeRecord.
2. Intake must detect whether the Request is single-step or multi-step.
3. Intake must extract dependencies, constraints, and candidate ambiguities.
4. Intake must create ClarificationIssues only for material ambiguity.
5. Intake must pause for clarification when a ClarificationIssue could change the result materially.
6. Intake must identify AlternativeOptions for non-trivial implementation or workflow decisions.
7. Intake must score or compare AlternativeOptions using quality, standards compliance, reliability, maintainability, implementation speed, operational efficiency, setup friction, and security.
8. Intake must choose a preferred approach and record fallback paths in an EvaluationReport.
9. Intake must determine canonical DomainEntities early and reuse them consistently in outputs.
10. Intake must determine the minimum ToolContext required for the request.
11. Intake must identify required ProviderDependencies and include setup metadata in outputs.
12. Intake must produce stable, structured PlanArtifacts and SpecArtifacts.
13. Intake must run FinalizationReview before a canonical document is considered finalized.
14. Intake must require changelog updates for substantive canonical document changes.
15. Intake must support a parallelizable-task tag decision when decomposition into parallel steps is justified.

## Non-functional requirements

### Reliability
- deterministic output structure for similar inputs
- no silent skipping of material ambiguity checks
- explicit fallback recording when a preferred path cannot be executed

### Maintainability
- canonical entity names remain stable across modules and docs
- rule evaluation should be implemented in separable components rather than a single monolith
- configuration and policy data should be inspectable and testable

### Security
- secrets must never be requested in chat
- secret-handling rules must be enforceable in generated outputs
- provider setup planning must separate planning from credential execution timing

### Performance
- optimize for low token and tool-context cost without lowering decision quality
- use minimal context by default and expand only when justified

### Auditability
- generated decisions should be explainable through structured artifacts
- evaluation outcomes, blockers, and finalization status should be inspectable

## Recommended stack

This is the preferred stack for the first implementation because it best matches the current environment and the document-heavy, schema-heavy nature of the system.

### Preferred stack
- TypeScript
- Node.js runtime
- Zod for schema validation
- Markdown files for canonical artifacts
- YAML frontmatter with minimal stable metadata
- Vitest for unit and integration tests
- ESLint and Prettier or equivalent formatting/linting baseline

Why this qualifies as preferred:
- strong schema support for structured artifacts
- good fit for markdown- and JSON-oriented workflows
- easy testing of policy logic and transformation pipelines

Why a simpler script-only approach does not qualify as preferred:
- weaker long-term maintainability for expanding rule systems
- less explicit type safety for canonical entities and interfaces

### Acceptable fallback stack
- Python 3.14
- Pydantic for schema validation
- pytest for testing

This qualifies as fallback when:
- the surrounding project is already Python-first
- the implementation must integrate tightly with an existing Python codebase

This does not qualify as preferred by default when:
- no surrounding Python dependency exists and the primary need is typed document and interface orchestration

## System components

### Request Parser
Converts a Request into an IntakeRecord.

### Ambiguity Analyzer
Detects ClarificationIssues and determines whether clarification is blocking.

### Alternative Evaluator
Builds AlternativeOptions and produces an EvaluationReport.

### Domain Vocabulary Registry
Stores canonical DomainEntities and enforces consistent terminology.

### Dependency Planner
Finds ProviderDependencies and ExecutionStep ordering.

### Tool Context Selector
Determines the minimum ToolContext required.

### Artifact Generator
Produces PlanArtifacts, SpecArtifacts, and agent-facing outputs.

### Finalization Engine
Runs the readiness loop and post-clear verification process.

### Changelog Enforcer
Ensures substantive canonical document changes include changelog updates.

## Interfaces

These are logical interfaces. They define the canonical boundaries even if the first implementation uses in-process modules rather than network APIs.

### Request intake interface
Input:
- raw request text
- optional upstream metadata

Output:
- IntakeRecord

### Clarification interface
Input:
- IntakeRecord

Output:
- list of ClarificationIssues
- blocking or non-blocking decision

### Alternative evaluation interface
Input:
- IntakeRecord
- candidate approaches

Output:
- EvaluationReport

### Domain entity registry interface
Input:
- proposed canonical names
- existing registry state

Output:
- accepted DomainEntities
- rename or conflict decisions

### Planning interface
Input:
- IntakeRecord
- EvaluationReport
- ToolContext
- ProviderDependencies

Output:
- PlanArtifact

### Specification interface
Input:
- IntakeRecord
- EvaluationReport
- canonical DomainEntities

Output:
- SpecArtifact

### Finalization interface
Input:
- canonical document

Output:
- per-section readiness states
- remediation actions
- post-clear verification findings
- final readiness decision

## Data shape requirements

The first implementation should define explicit schemas for at least:
- Request
- IntakeRecord
- ClarificationIssue
- AlternativeOption
- EvaluationReport
- DomainEntity
- ProviderDependency
- ToolContext
- ExecutionStep
- PlanArtifact
- SpecArtifact
- FinalizationReviewResult

Every schema should:
- have a stable primary identifier or stable name field where applicable
- distinguish required versus optional fields clearly
- support explicit uncertainty or confidence when relevant
- avoid hidden implicit defaults for governance-critical behavior

## Acceptance criteria

The implementation is acceptable only if all of the following are true:
1. A raw Request can be transformed into a valid IntakeRecord using an explicit schema.
2. Material ambiguity produces a ClarificationIssue instead of silent guessing.
3. Non-trivial decisions generate at least one AlternativeOption comparison before selecting a preferred path.
4. The system records a preferred path and fallback path in an EvaluationReport.
5. Canonical DomainEntities are defined and then reused consistently in produced artifacts.
6. The chosen ToolContext is minimal relative to the actual request needs.
7. Required ProviderDependencies include provider name, needed credential or access artifact, direct setup link, preferred setup path, and fallback order.
8. Generated PlanArtifacts have stable ordering and dependency-aware step structure.
9. Generated SpecArtifacts include scope, requirements, interfaces, and acceptance criteria.
10. FinalizationReview can mark sections as `clear`, `usable`, `needs cleanup`, or `not ready`, and each state has example-based interpretation in the canonical docs.
11. Substantive canonical document changes are rejected or flagged if no changelog update is present.
12. The implementation can explain why a request was clarified, reordered, or tagged for parallelization.
13. The implementation never instructs a user to paste secrets into chat.

## Test approach

### Unit tests
Test each core component independently:
- Request Parser normalizes representative requests into valid IntakeRecords
- Ambiguity Analyzer distinguishes material ambiguity from cosmetic ambiguity
- Alternative Evaluator compares viable options and rejects empty pseudo-options
- Domain Vocabulary Registry preserves canonical names and flags synonym drift
- Tool Context Selector minimizes included capabilities
- Changelog Enforcer detects substantive document changes without changelog updates

### Integration tests
Test end-to-end flows across components:
- multi-step request with reorderable dependencies
- request blocked by material ambiguity
- provider-dependent request requiring setup metadata
- canonical doc update requiring FinalizationReview and changelog update
- task eligible for parallel decomposition and `#parallel` tagging

### Golden-file tests
Use representative markdown outputs to verify:
- stable headings and blank-line discipline
- deterministic section ordering
- consistent canonical entity names across artifacts

### Negative tests
Verify rejection or blocking behavior when:
- a document has no changelog update for a substantive canonical change
- a spec omits acceptance criteria
- a tool context includes unjustified extra capabilities
- a request with material ambiguity attempts to proceed without clarification

### Example-based evaluation tests
Use labeled examples for readiness states and ambiguity classification so the implementation can be regression-tested against the exact interpretation standards in the spec.

Qualifies as good coverage when:
- tests include both qualifying and non-qualifying examples for major labels and rules
- failures make the violated policy obvious

Does not qualify as good coverage when:
- tests only cover happy paths
- evaluative labels are tested without concrete example cases

## Build outputs

The first implementation should produce at minimum:
- a schema layer for canonical entities
- a policy engine for governance rules
- a planning and spec generation layer
- a finalization review module
- a changelog consistency check
- test fixtures and golden examples

## Open decisions

These items are intentionally left open for the build plan to sequence, not for the implementation spec to redefine:
- exact repo layout
- whether the first delivery is a library, CLI, or service boundary on top of the same core modules
- whether document generation templates live inline or in separate template files

## Notes

This spec is task-specific to the Intake system implementation itself. It does not replace the global governance rules in `spec-v6.md`; it operationalizes them for code design.