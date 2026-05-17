# Perceptyx Read-Only Connector Scaffold

This project is a minimal, validated scaffold for a Perceptyx connector.

Scope:
- Read-only only
- Disabled by default
- No write actions
- No guessed endpoints
- No login automation
- No inbound HRIS connector implementation
- Export-first fallback guidance when API access or approval is missing

What this scaffold includes:
- Configuration placeholders only
- Approval and access guardrails
- A disabled-by-default connector shell
- Read-only normalization helpers for list and fetch style payloads
- Clear instructions for when to stop and fall back to approved exports

What this scaffold intentionally does not include:
- Hardcoded Perceptyx API URLs or endpoint paths
- Survey mutation, admin mutation, or writeback actions
- Background sync jobs
- Tenant-specific assumptions
- Any attempt to bypass approval or missing access

## Validated operating model

Use this scaffold only when all of the following are true:
1. Perceptyx-issued API access exists for the target tenant.
2. OAuth details and tenant base URL are provided through approved channels.
3. Any required data release approval or equivalent customer approval is confirmed.
4. The dataset requested is approved for API export.

If any of those conditions are missing, the connector must remain disabled.

## Export-first fallback

If API access or approval is missing:
- Keep the connector in disabled state.
- Use approved export files instead of attempting direct API calls.
- Document the missing approvals or missing tenant details.
- Revisit API enablement only after approval and tenant-specific details are available.

## Project layout

- `config.example.json` - placeholder configuration only
- `perceptyx_connector/status.py` - access and approval guardrails
- `perceptyx_connector/connector.py` - disabled-by-default connector shell
- `perceptyx_connector/normalize.py` - normalization helpers for read-only export/list/fetch payloads
- `perceptyx_connector/fallback.md` - export-first fallback guidance

## Quick start

1. Copy `config.example.json` to a local config file outside source control.
2. Fill in only approved, tenant-specific values.
3. Confirm approval status before enabling anything.
4. Leave `enabled` as `false` until all validations are satisfied.
5. If validation fails, stop and use the export-first fallback.
