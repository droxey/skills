# Example 01: Zero-Shot Rewrite

## Raw prompt

```text
Summarize this meeting transcript into five bullets for executives.
```

## Why this technique fits

This is a direct transformation task with a clear output target. It does not require examples, retrieval, or a multi-step tool loop.

## Refactored prompt

```text
You are an expert executive communications assistant.

Task:
Summarize the provided meeting transcript for an executive audience.

Input:
{{meeting_transcript}}

Constraints:
- Keep it to exactly five bullets.
- Focus on decisions, risks, blockers, and next steps.
- Omit side discussion and repetition.
- Use concise executive language.

Output requirements:
- Return exactly five markdown bullets.
- Each bullet should be one sentence.
```

## Validation notes

- Structure complete: pass
- Technique fit: strong
- Risk level: low
- Fallback: few-shot if outputs are too verbose or stylistically inconsistent
