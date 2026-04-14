# Example 03: Structured Reasoning Decision

## Raw prompt

```text
Should we migrate this internal service from Python to Go this quarter?
```

## Why this technique fits

This is a multi-factor decision problem. It benefits from explicit decomposition of criteria, tradeoffs, risks, and recommendation structure, but it does not require tools or retrieval by default.

## Refactored prompt

```text
You are an engineering strategy advisor.

Task:
Evaluate whether the service should be migrated from Python to Go this quarter.

Input:
{{service_context}}

Evaluate using these sections:
1. Current pain points
2. Expected gains
3. Migration cost and complexity
4. Operational risk
5. Team readiness
6. Recommendation

Constraints:
- Base the answer only on the provided context.
- State assumptions separately.
- If evidence is insufficient, say so directly.

Output requirements:
- Return the six sections above.
- End with one recommendation: migrate now, defer, or reject.
```

## Validation notes

- Structure complete: pass
- Technique fit: strong
- Risk level: medium
- Fallback: prompt chaining if the input is large or mixed-quality
