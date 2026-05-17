# Example 02: Few-Shot Labeling

## Raw prompt

```text
Classify each customer support ticket as billing, bug, feature request, or account issue.
```

## Why this technique fits

The output classes are small and well-bounded, but borderline cases can drift without demonstrations. Few-shot examples sharpen label boundaries and output consistency.

## Refactored prompt

```text
You are a support operations classifier.

Task:
Classify each ticket into exactly one label:
- billing
n- bug
- feature_request
- account_issue

Examples:
Ticket: I was charged twice for the same month.
Label: billing

Ticket: The app crashes when I upload a PDF.
Label: bug

Ticket: Please add dark mode to the dashboard.
Label: feature_request

Ticket: I cannot sign in after resetting my password.
Label: account_issue

Now classify the following ticket.

Ticket:
{{ticket_text}}

Constraints:
- Return exactly one label.
- Do not explain the answer.
```

## Validation notes

- Structure complete: pass
- Technique fit: strong
- Risk level: low
- Fallback: zero-shot if labels are already highly deterministic
