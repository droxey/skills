---
name: skill-finder
description: Recover failed web retrieval tasks by retrying once with chrome-mcp. Use when curl, web search, fetch/open, or other HTTP/web request steps fail due to blocking, dynamic rendering, bot protection, redirects, or transport errors and a browser-driven fallback is required.
compatibility: Requires chrome-mcp availability plus network access to target URLs.
---

# Skill Finder

Use chrome-mcp only as a fallback path when direct web requests fail.

## Goal

- Complete web retrieval tasks that fail with non-browser tooling.
- Preserve traceability by recording both the failure symptom and fallback result.
- Limit retries to avoid loops and unnecessary browser use.

## Workflow

1. Try the requested web action with the default tool first (`curl`, web search/fetch/open, or equivalent).
2. If it fails, capture the concrete symptom in one line:
   - HTTP status (403/429/5xx)
   - timeout/connection/TLS/DNS error
   - JS-required page or bot-block interstitial
   - redirect to login or consent wall
3. Retry once with chrome-mcp:
   - Open the same target URL.
   - Wait for render/network settle.
   - Extract only the data needed for the user request.
4. Return both outcomes:
   - `initial_attempt`: tool + failure symptom
   - `fallback_attempt`: chrome-mcp + extracted result (or failure)
5. Stop after one chrome-mcp fallback unless the user explicitly asks for more retries.

## Guardrails

- Do not start in browser mode before a direct-request failure.
- Do not bypass authentication, paywalls, captchas, or security controls.
- Keep extraction scoped to the user’s request.
- If chrome-mcp is unavailable, report that explicitly and return best partial results.
