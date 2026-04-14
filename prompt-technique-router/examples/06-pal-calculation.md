# Example 06: PAL Calculation

## Raw prompt

```text
Given these subscription counts and prices, calculate monthly revenue, annual revenue, and ARPU.
```

## Why this technique fits

The task is computational. Using code-assisted reasoning reduces arithmetic error and keeps the calculation path precise.

## Refactored prompt

```text
Use code to perform the calculations.

Task:
Compute monthly revenue, annual revenue, and ARPU from the provided subscription data.

Input:
{{subscription_data}}

Constraints:
- Use executable code for all arithmetic.
- Show formulas clearly in the final answer.
- If any inputs are missing or invalid, stop and report that explicitly.

Output requirements:
- Monthly revenue
- Annual revenue
- ARPU
- Short calculation notes
```

## Validation notes

- Structure complete: pass
- Technique fit: strong
- Risk level: medium
- Fallback: structured reasoning only if code execution is unavailable and the arithmetic is trivial
