---
name: product-clone-research
description: Run authenticated website reconnaissance with chrome-mcp for clone planning. Use when a user provides a domain and wants structured route/flow capture, high-resolution screenshots, workflow documentation, coverage validation, and a handoff prompt to begin clone planning from captured research artifacts.
---

# Product Clone Research Operator (chrome-mcp)

Use this workflow to map a target web product, capture evidence, and generate clone-ready research artifacts.

## Goal
Create a reproducible research package in `research/$DOMAIN` that includes:
- public and authenticated route inventory
- workflow-level evidence with high-resolution screenshots
- coverage report with explicit unknowns
- product teardown and clone implementation handoff

## Guardrails
- Capture only pages and actions the user is authorized to access.
- Never bypass authentication, CAPTCHA, paywalls, robots restrictions, or other security controls.
- Never store plaintext credentials in repository files.
- Redact secrets and user PII from logs and reports when possible.
- If legal/ToS boundaries are unclear, stop and report blockers.

## Hard truth on “complete coverage”
Absolute proof of "every path" is usually impossible for modern apps (feature flags, role-gated UIs, time-based states, hidden APIs).

Instead, enforce **defensible completeness**:
1. Exhaustive crawl of all discoverable UI routes in scope.
2. Deterministic action sweep for each discovered screen.
3. Coverage manifest showing visited vs pending items.
4. Explicit unknowns list and why each remains unverified.

Do not claim full completion without this evidence.

## Required inputs
Collect or confirm before running:
- `DOMAIN` and base URL
- auth method (password, SSO, magic link, MFA)
- credential source (manual entry, env vars, secret manager)
- allowed scope (subdomains, roles, locales, billing/admin)
- role matrix (e.g., admin, manager, member)
- stop criteria (MVP flows only vs broad parity)

## Directory contract
Create and maintain:

`research/$DOMAIN/`
- `manifest.json` — route/action registry and status
- `routes-public.csv`
- `routes-authenticated.csv`
- `actions.csv` — buttons/controls/actions found and execution status
- `workflows.md` — end-to-end flow docs
- `evidence/` — screenshots and page metadata
- `coverage-report.md`
- `product-teardown-report.md`
- `clone-scope-recommendation.md`
- `execution-log.md`

Screenshot naming:
- `evidence/<AUTH_STATE>/<ROUTE_ID>/<STEP_ID>--<STATE_TAG>.png`

## Phase 1 — Public discovery
1. Discover public pages via nav, footer, sitemap/robots hints, and internal links.
2. Deduplicate and canonicalize URLs.
3. For each route, capture:
   - URL, title, timestamp, route id
   - high-res screenshot (desktop baseline)
   - outbound actions/controls detected
4. Store results in `routes-public.csv` and `manifest.json`.

## Phase 2 — Authenticated traversal with chrome-mcp
1. Login through user-approved credential path.
2. Traverse primary nav plus deep states:
   - onboarding, empty/populated states, CRUD, settings, billing, support
3. For each screen/state:
   - capture high-resolution screenshot
   - enumerate actionable controls (buttons, menu items, toggles, form submissions)
   - execute safe actions to reveal downstream states
4. Track discovered transitions as edges in `manifest.json`.
5. Repeat traversal per approved role in scope.
6. Clear session artifacts at end.

## Phase 3 — Workflow documentation
Build `workflows.md` with each workflow containing:
- objective
- prerequisites/role
- start URL
- ordered UI steps
- expected outcomes
- screenshots
- branch/exception paths

## Phase 4 — Coverage validation
Generate `coverage-report.md` with:
- discovered routes count (public/auth by role)
- visited route count
- discovered actionable controls count
- executed control count
- blocked/unverified items with reasons
- confidence score by module (high/medium/low)

Completion gate:
- all discovered in-scope routes visited OR marked blocked with reason
- all discovered in-scope actions executed OR marked unsafe/blocked with reason
- unknowns explicitly listed

## Phase 5 — Synthesis and clone handoff
Produce:
- `product-teardown-report.md`
- `clone-scope-recommendation.md`

Then issue this exact handoff prompt:

`/brainstorm write a clone based on the files in research/$DOMAIN`

And begin `/write-plan` using artifacts in `research/$DOMAIN` as canonical input.

## Output contract (chat response)
Return exactly these sections in order:
1. `## Goal`
2. `## Constraints`
3. `## Capture Plan`
4. `## Execution Log`
5. `## Evidence Index`
6. `## Coverage Report`
7. `## Product Teardown Report`
8. `## Clone Scope Recommendation`
9. `## Risks / Unknowns`
10. `## Handoff Triggered`

## Failure handling
If blocked by auth, MFA, legal constraints, anti-bot controls, or environment/tool limits:
- stop at boundary
- produce partial artifacts
- list exact blockers and next required user actions
- do not claim full completion
