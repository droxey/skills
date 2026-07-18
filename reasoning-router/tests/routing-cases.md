# Reasoning Router Cases

These cases are written before implementation and define the expected routing behavior.

| Case | Expected | Reason |
|---|---|---|
| Rewrite one paragraph under explicit constraints | Medium | Bounded and easy to verify |
| Compare two frameworks and recommend one for a defined system | High | Multi-step synthesis with moderate uncertainty |
| Audit a benchmark, threat model, or concurrency design | Extra High | Difficult verification and high consequence |
| Prove the cause of an intermittent distributed failure after prior attempts failed | Max | One exceptionally entangled problem requiring proof |
| Decide whether a foundational architecture or product premise is framed correctly | Pro | Judgment and framing dominate longer deliberation |
| Review backend, frontend, security, testing, and operations as independent tracks | Ultra | Multiple independent workstreams benefit from coordinated synthesis |

## Pressure cases

1. A user asks for Pro merely because the task is important. Expected: use Extra High unless the frame itself is uncertain or model judgment is the bottleneck.
2. A user asks for Ultra for one tightly coupled debugging problem. Expected: use Max when supported, not Ultra.
3. Max is unavailable in the active surface. Expected: choose Extra High and state the capability fallback only when relevant.
4. Ultra is unavailable but Pro is available. Expected: use Pro for coordination and manually divide independent workstreams.
5. The task is large but routine and mechanically verifiable. Expected: High, not automatically Extra High or Pro.
