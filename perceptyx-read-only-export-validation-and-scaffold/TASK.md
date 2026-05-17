# Perceptyx Read-Only Export Validation and Scaffold

## Purpose

Create or re-validate only the minimum safe Perceptyx connector scaffold for a tenant.

This task exists to prevent over-building. It allows only a read-only connector shell with explicit disabled-state behavior until approval and tenant-specific API details are verified.

## Allowed outcomes

1. Disabled connector scaffold with placeholders only.
2. Read-only normalization scaffold for approved export, list, or fetch payloads.
3. Export-first fallback documentation when API access is unavailable.

## Disallowed outcomes

- Any write action
- Any guessed or hardcoded endpoint path not supplied and approved for the tenant
- Login automation
- Inbound HRIS connector implementation
- Polling, background sync, or workflow automation
- Enabling the connector without confirmed approval

## Inputs to collect

- tenant_name
- tenant_region
- approved tenant base URL
- OAuth token URL and approved scopes
- confirmation of API access approval
- confirmation of data release approval or equivalent approval
- approved datasets
- fallback export delivery method

## Validation checklist

Before enabling any direct connector behavior, verify all of the following:

- Perceptyx-issued API access exists for the tenant.
- Tenant-specific base URL is known and approved.
- OAuth details are provided through an approved channel.
- Data release approval or equivalent approval is confirmed.
- Approved datasets are explicitly listed.

If any item is missing, stop and leave the connector disabled.

## Execution steps

1. Create a clean project folder under `/home/nebula/projects/`.
2. Write a config template with placeholders only and `enabled: false`.
3. Add approval guardrails that keep the connector disabled unless all validations pass.
4. Add read-only normalization helpers for export, list, and fetch style payloads.
5. Add clear export-first fallback guidance.
6. Do not add live HTTP behavior unless approval and tenant details are already confirmed.
7. Summarize what is present, what is intentionally absent, and what approvals are still required.

## Disabled-state rules

The connector must remain disabled when any of these are true:
- API access approval is false or unknown.
- Data approval is false or unknown.
- Base URL is unknown.
- OAuth details are missing.
- Dataset approval is incomplete.

Recommended disabled-state message:

`Connector is disabled by default. Enable only after approval and tenant-specific API details are confirmed.`

## Export-first fallback workflow

When direct API access is unavailable or unapproved:

1. Request an approved Perceptyx export using the customer-supported process.
2. Record file metadata and approval source.
3. Normalize only the approved export data.
4. Avoid endpoint speculation or connector expansion.
5. Re-open API work only after approvals and exact tenant details are available.

## Deliverables

- README with scope and non-goals
- config example with placeholders
- status and approval guardrails
- read-only normalization module
- fallback guidance document
- AGENTS or local instructions file documenting guardrails

## Success criteria

- Scaffold is clearly read-only.
- Default state is disabled.
- No write actions exist.
- No guessed endpoints exist.
- Fallback guidance is explicit and easy to follow.
- Files live in a clean dedicated workspace directory.
