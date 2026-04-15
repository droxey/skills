---
name: product-clone-research
description: Plan and execute structured product reconnaissance for open-source cloning efforts. Use when a user provides a product website and wants: (1) screenshots of all reachable unauthenticated pages, (2) authenticated capture after login with user-provided credentials or approved secret manager flow, and (3) a formal product research deliverable that summarizes IA, UX flows, feature surface, data model hints, and implementation implications.
---

# Product Clone Research Operator

Follow this workflow to capture product evidence and produce a reusable research brief for implementation.

## Output contract
Return exactly these sections in order:

1. `## Goal`
2. `## Constraints`
3. `## Capture Plan`
4. `## Execution Log`
5. `## Evidence Index`
6. `## Product Teardown Report`
7. `## Clone Scope Recommendation`
8. `## Risks / Unknowns`

## Naming
Use these terms consistently:
- `Product Teardown Report`: comprehensive analysis of UX, features, and architecture clues.
- `Clone Scope Recommendation`: proposed MVP and phased parity plan.

If user asks for a shorter label, allow `Product Research Report` as alias.

## Guardrails
- Capture only pages the user is authorized to access.
- Never bypass authentication, paywalls, CAPTCHA, robots, or security controls.
- Never store plaintext credentials in repo files or chat logs.
- Prefer ephemeral secret injection and redact secrets in logs.
- Stop and report if terms/legal boundaries are unclear.

## Inputs required
Collect or confirm:
- Target base URL.
- Authentication method (password, SSO, magic link, MFA, etc.).
- Credential source (manual entry, secret manager, 1Password CLI, env vars).
- Scope boundaries (subdomains, locales, billing/admin pages).
- Output depth (MVP only vs full parity).

## Phase 1: Discovery and unauthenticated capture
1. Map public routes:
   - Parse navigation, footer, robots/sitemap references, and in-app links.
   - Build a deduplicated route list (canonical URL, page type, discovery source).
2. Capture each reachable public route:
   - Take deterministic screenshots (desktop baseline; optionally mobile).
   - Record page title, URL, timestamp, auth state=`public`.
3. Note broken links, gated transitions, and dynamic states requiring auth.

## Phase 2: Authenticated capture
1. Authenticate safely:
   - Use user-approved credential path.
   - Prefer non-persistent session strategy.
2. Enumerate authenticated routes:
   - Traverse primary nav, settings, onboarding, empty states, CRUD flows, and account pages.
   - Trigger meaningful states (create/edit/delete previews when safe).
3. Capture evidence per route/state:
   - Screenshot with stable viewport.
   - Log URL, title, state tags (e.g., `dashboard-empty`, `project-detail-populated`), timestamp, auth state=`authenticated`.
4. Terminate session and clear session artifacts when complete.

## Phase 3: Synthesis and reporting
Build a `Product Teardown Report` with:
- Product summary: user segment, core jobs-to-be-done, value loop.
- Information architecture: sitemap and role-based route map.
- UX flow inventory: onboarding, activation, recurring use, settings, billing, support.
- Feature decomposition: modules, key entities, permissions, edge states.
- UI system notes: layout patterns, component families, interaction patterns.
- Technical inference: likely backend domains, integrations, events, and constraints inferred from UI only (mark inferences explicitly).
- Clone complexity: low/medium/high by module with rationale.

Then build `Clone Scope Recommendation`:
- MVP scope (must-clone now).
- Phase 2/3 backlog (later parity).
- Suggested architecture and build order.
- Risks, assumptions, and validation experiments.

## Evidence format
Create an evidence table with columns:
- `id`
- `auth_state`
- `url`
- `page_or_flow`
- `screenshot_path`
- `captured_at_utc`
- `notes`

Use stable IDs like `PUB-001`, `AUTH-001`.

## Minimum completion criteria
Do not claim completion until all are true:
- Public routes captured or explicitly marked unreachable.
- Authenticated routes captured within agreed scope.
- Evidence index is complete and linked to screenshots.
- Product Teardown Report and Clone Scope Recommendation delivered.
- Unknowns and assumptions explicitly listed.

## Failure handling
If blocked by login, MFA, bot defenses, or legal constraints:
- Stop immediately.
- Provide partial deliverables from available evidence.
- Return a precise blocker list and next actions needed from user.
