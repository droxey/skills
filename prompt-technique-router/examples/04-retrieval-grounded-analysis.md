# Example 04: Retrieval-Grounded Analysis

## Raw prompt

```text
Answer this contract question using the attached MSA and cite the clauses.
```

## Why this technique fits

The task is source-bound and high risk. The answer must be grounded in provided documents rather than model memory.

## Refactored prompt

```text
Use only the provided source materials.

Task:
Answer the user's contract question.

Question:
{{user_question}}

Sources:
{{retrieved_contract_clauses}}

Constraints:
- Use only the provided sources.
- Cite the relevant clause or section for each key claim.
- If the sources are insufficient, say exactly what is missing.
- Do not rely on outside knowledge.

Output requirements:
- Answer the question directly.
- Then provide a short evidence section with citations.
```

## Validation notes

- Structure complete: pass
- Technique fit: strong
- Risk level: high
- Fallback: clarification-first prompt if no relevant clauses are retrieved
