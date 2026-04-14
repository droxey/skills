# Example 05: ReAct Tool Loop

## Raw prompt

```text
Find the latest API rate limit policy for this vendor and tell me whether our current retry strategy is safe.
```

## Why this technique fits

The task requires external lookup plus evaluation. A tool loop is justified because the answer depends on current documentation and likely needs search, read, and assess steps.

## Refactored prompt

```text
You can use tools to search and read external documentation.

Task:
Determine the vendor's current API rate limit policy and assess whether the current retry strategy is safe.

Available tools:
{{available_tools}}

Process:
1. Search for the official rate limit documentation.
2. Read the relevant sections.
3. Extract the current policy details.
4. Compare them to the retry strategy.
5. Return a verdict with evidence.

Constraints:
- Prefer official documentation.
- State uncertainty if the policy is ambiguous.
- Do not assume historical behavior still applies.

Output requirements:
- Current policy summary
- Retry strategy assessment
- Risks or mismatches
- Source citations
```

## Validation notes

- Structure complete: pass
- Technique fit: strong
- Risk level: high
- Fallback: retrieval-grounded prompt if the tool environment does not support iterative search
