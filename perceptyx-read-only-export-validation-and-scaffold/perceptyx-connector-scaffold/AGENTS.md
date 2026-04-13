# Perceptyx Connector Guardrails

This workspace contains only a minimum validated scaffold.

Rules:
- Treat the connector as read-only.
- Leave it disabled by default.
- Do not invent or hardcode Perceptyx endpoints.
- Do not add write or admin mutation paths.
- Do not add tenant-specific logic until approval and access are verified.
- Prefer approved exports when API access is unavailable.
