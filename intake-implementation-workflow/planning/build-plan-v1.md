---
doc_type: build_plan
version: v1
status: draft
authority: derived
---

# Intake Build Plan v1

## Purpose

This document defines the concrete build sequence for implementing the Intake system described in `spec-v6.md` and `implementation-spec-v1.md`.

It converts governance and implementation requirements into an execution-ready plan with delivery phases, interfaces to build first, testing sequence, and definition-of-done checkpoints.

If this plan conflicts with `spec-v6.md` on global governance, `spec-v6.md` wins. If this plan conflicts with `implementation-spec-v1.md` on canonical entities or system boundaries, `implementation-spec-v1.md` wins.

## Build objective

Deliver a first working Intake implementation that can:
- normalize requests into structured records
- identify material ambiguity
- compare alternatives for non-trivial tasks
- register and reuse canonical domain vocabulary
- produce stable plan and spec artifacts
- enforce finalization and changelog rules
- provide a testable core suitable for extension into CLI or service form

## Delivery strategy

### Recommended delivery shape
Build the first version as a core library with a thin local CLI wrapper.

Qualifies as the recommended shape when:
- the core policy and transformation logic is the hardest part and should be testable without network boundaries
- the same engine may later back a service, agent runtime, or editor tooling
- a CLI gives fast manual validation without locking the architecture into a server-first design

Does not qualify as the recommended shape when:
- the first implementation is built directly as a network service with transport concerns mixed into core policy logic
- document generation logic depends on UI state or framework-specific components from day one

### Fallback delivery shape
A library-only first release is acceptable if CLI work would slow validation.

Qualifies as acceptable fallback when:
- all core modules and tests are still present
- manual invocation can happen through direct test fixtures or scripts

Does not qualify as acceptable fallback when:
- the lack of a thin invocation path makes it hard to validate end-to-end behavior

## Canonical implementation modules

Use these module names as the initial build vocabulary. Apply language-appropriate casing in code while preserving the same domain meaning.

- RequestParser
- AmbiguityAnalyzer
- AlternativeEvaluator
- DomainVocabularyRegistry
- DependencyPlanner
- ToolContextSelector
- ArtifactGenerator
- FinalizationEngine
- ChangelogEnforcer
- IntakeCli

## Proposed repository layout

This layout is the recommended first-pass structure.

```text
intake/
  src/
    schemas/
    policies/
    services/
    generators/
    finalization/
    cli/
    index.ts
  tests/
    unit/
    integration/
    golden/
    fixtures/
  docs/
    examples/
  AGENTS.md
  README.md
  CHANGELOG.md
```

### Layout rationale
- `schemas/` for canonical entity definitions and validators
- `policies/` for evaluative rules and shared governance checks
- `services/` for request analysis and planning modules
- `generators/` for plan and spec artifact generation
- `finalization/` for readiness and verification logic
- `cli/` for the thin command interface only
- `tests/` separated by level so failures are easy to localize

## Build phases

## Phase 1: foundation

### Goal
Establish the canonical entities, schemas, and project skeleton.

### Deliverables
- project scaffold
- schema definitions for all canonical entities
- shared policy constants and types
- test harness setup
- folder-level `AGENTS.md` files for the root and each implementation subfolder

### Acceptance checkpoint
This phase is complete only if:
- every canonical entity from `implementation-spec-v1.md` has a schema
- schemas distinguish required and optional fields clearly
- test tooling runs successfully
- folder-level agent docs exist where the implementation will live

## Phase 2: request analysis core

### Goal
Implement request normalization, ambiguity detection, and domain vocabulary capture.

### Deliverables
- RequestParser
- AmbiguityAnalyzer
- DomainVocabularyRegistry
- fixtures for representative requests

### Acceptance checkpoint
This phase is complete only if:
- a raw request can become a valid IntakeRecord
- material ambiguity produces ClarificationIssues
- canonical entity names can be registered and reused consistently

## Phase 3: evaluation and planning

### Goal
Implement alternative comparison, dependency analysis, and context minimization.

### Deliverables
- AlternativeEvaluator
- DependencyPlanner
- ToolContextSelector
- EvaluationReport generation

### Acceptance checkpoint
This phase is complete only if:
- non-trivial requests compare viable alternatives before recommendation
- dependency-aware step reordering works for representative cases
- the selected ToolContext is minimal and explainable

## Phase 4: artifact generation

### Goal
Generate stable plan and spec outputs from the analyzed request state.

### Deliverables
- ArtifactGenerator
- markdown templates or renderers
- golden-file fixtures for output stability

### Acceptance checkpoint
This phase is complete only if:
- PlanArtifacts have deterministic structure and ordering
- SpecArtifacts include scope, interfaces, requirements, and acceptance criteria
- canonical domain entity names remain consistent across outputs

## Phase 5: finalization and changelog enforcement

### Goal
Implement readiness review, verification review, and changelog enforcement.

### Deliverables
- FinalizationEngine
- ChangelogEnforcer
- readiness fixtures with qualifying and non-qualifying examples

### Acceptance checkpoint
This phase is complete only if:
- readiness states can be assigned per section
- remediation candidates are surfaced clearly
- missing changelog updates for substantive canonical changes are detected

## Phase 6: local invocation and end-to-end verification

### Goal
Expose a thin CLI and verify full workflows.

### Deliverables
- IntakeCli
- end-to-end integration suite
- example commands and fixture docs

### Acceptance checkpoint
This phase is complete only if:
- a user can run a local command against a sample request and receive stable structured output
- the full pipeline can produce plan/spec artifacts and finalization findings end to end

## Interface implementation order

Build these interfaces in this order to minimize rework:
1. schema interfaces
2. request intake interface
3. clarification interface
4. domain entity registry interface
5. alternative evaluation interface
6. planning interface
7. specification interface
8. finalization interface
9. thin CLI interface

This qualifies as the preferred order because:
- upstream normalization and schemas stabilize the rest of the system
- planning and generation depend on earlier analysis outputs
- the CLI should wrap completed behavior rather than define it

This does not qualify as the preferred order when:
- transport or presentation layers are built before the core schemas and policy engine
- generation is implemented before ambiguity and evaluation logic exist

## Stack decision

### Chosen stack
- TypeScript
- Node.js
- Zod
- Vitest
- markdown artifact generation

### Why chosen
This stack provides the best fit for typed schemas, markdown-first outputs, and stable testable transformation logic in the current environment.

### Fallback stack
- Python
- Pydantic
- pytest

Use the fallback only if surrounding repo constraints make the preferred stack materially worse.

## Testing plan

## Test layers

### Unit layer
Focus on deterministic behavior of each module.

Must cover:
- schema validation
- ambiguity classification
- alternative scoring or comparison behavior
- domain entity registration and conflict handling
- changelog presence checks

### Integration layer
Focus on multi-module flows.

Must cover:
- multi-step request with dependency reordering
- blocking clarification flow
- provider dependency extraction
- finalization review plus changelog enforcement

### Golden layer
Focus on output stability.

Must cover:
- stable section ordering
- heading normalization
- blank-line discipline
- canonical vocabulary reuse

### Regression layer
Focus on previously fixed failures and edge cases.

Must cover:
- duplicated changelog entry detection
- stale terminology drift
- missing acceptance criteria in generated specs
- unjustified extra tool-context inclusion

## Definition of done

The first implementation is done only if all of the following are true:
1. All canonical schemas exist and validate representative fixtures.
2. Request analysis can classify ambiguity and dependencies correctly for representative examples.
3. Non-trivial requests produce alternative evaluation output before a final recommendation.
4. Plan and spec outputs are generated with stable markdown structure.
5. Finalization review can flag non-clear sections and produce verification findings.
6. Changelog enforcement catches substantive canonical changes that are not logged.
7. Unit, integration, and golden tests pass.
8. Root and subfolder `AGENTS.md` files exist and are consistent with folder purpose.
9. README and CHANGELOG can be updated in the documented workflow without contradicting the spec.
10. The local CLI or fallback invocation path can demonstrate the full pipeline.

## Risks and mitigations

### Risk: governance logic becomes too implicit
Mitigation:
- centralize rule definitions in schema and policy modules
- use fixtures that show both qualifying and non-qualifying cases

### Risk: artifact generation diverges from canonical vocabulary
Mitigation:
- pass DomainEntities through a shared registry
- add golden tests for term consistency

### Risk: test coverage validates only happy paths
Mitigation:
- require negative and example-based evaluation tests
- add regression cases for prior cleanup failures

### Risk: build starts with the wrong boundary
Mitigation:
- keep the first implementation library-first
- keep the CLI thin and non-authoritative

## Immediate next actions

1. create the implementation repo scaffold
2. define schemas for canonical entities
3. add fixtures for request, ambiguity, and document examples
4. implement RequestParser, AmbiguityAnalyzer, and DomainVocabularyRegistry first
5. add unit tests before moving to artifact generation

## Notes

This build plan is concrete enough to start coding, but it intentionally leaves transport and packaging details secondary to the core policy engine. That keeps the first version aligned with the governance and implementation specs rather than over-optimizing delivery shape too early.
