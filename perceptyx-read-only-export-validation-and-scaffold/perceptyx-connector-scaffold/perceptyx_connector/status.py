from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class ConnectorStatus:
    enabled: bool
    ready: bool
    reasons: List[str]
    mode: str = "read_only"


REQUIRED_APPROVAL_FLAGS = [
    "api_access_approved",
    "data_release_approved",
]


def evaluate_status(config: Dict[str, Any]) -> ConnectorStatus:
    reasons: List[str] = []

    enabled = bool(config.get("enabled", False))
    mode = config.get("connector_mode", "read_only")
    if mode != "read_only":
        reasons.append("connector_mode must remain read_only")

    approvals = config.get("approvals", {})
    for flag in REQUIRED_APPROVAL_FLAGS:
        if not approvals.get(flag, False):
            reasons.append(f"missing required approval: {flag}")

    required_values = {
        "tenant_name": config.get("tenant_name"),
        "tenant_region": config.get("tenant_region"),
        "tenant_base_url": config.get("tenant_base_url"),
        "oauth.client_id": config.get("oauth", {}).get("client_id"),
        "oauth.client_secret_env": config.get("oauth", {}).get("client_secret_env"),
        "oauth.token_url": config.get("oauth", {}).get("token_url"),
    }

    for key, value in required_values.items():
        if not value or str(value).startswith("REQUIRED_"):
            reasons.append(f"missing required configuration: {key}")

    ready = enabled and not reasons
    return ConnectorStatus(enabled=enabled, ready=ready, reasons=reasons, mode=mode)


def disabled_state_message(config: Dict[str, Any]) -> str:
    status = evaluate_status(config)
    if status.ready:
        return "Connector is approved for read-only operation."
    if not status.enabled:
        return "Connector is disabled by default. Enable only after approval and tenant-specific API details are confirmed."
    return "Connector is not ready: " + "; ".join(status.reasons)
