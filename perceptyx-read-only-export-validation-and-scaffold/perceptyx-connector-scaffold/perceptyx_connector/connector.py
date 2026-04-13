from typing import Any, Dict

from perceptyx_connector.normalize import (
    normalize_export_file_metadata,
    normalize_fetch_payload,
    normalize_list_payload,
)
from perceptyx_connector.status import disabled_state_message, evaluate_status


class PerceptyxConnector:
    """Minimal read-only scaffold with explicit disabled-state behavior.

    This class does not perform network requests. Tenant-specific API calls must
    be implemented only after approval, verified access, and confirmed endpoint
    details are available.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.status = evaluate_status(config)

    def get_status(self) -> Dict[str, Any]:
        return {
            "enabled": self.status.enabled,
            "ready": self.status.ready,
            "mode": self.status.mode,
            "reasons": self.status.reasons,
            "message": disabled_state_message(self.config),
        }

    def assert_ready(self) -> None:
        if not self.status.ready:
            raise RuntimeError(disabled_state_message(self.config))

    def list_exports(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.assert_ready()
        return normalize_list_payload(payload)

    def fetch_export(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.assert_ready()
        return normalize_fetch_payload(payload)

    def describe_export_file(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_export_file_metadata(metadata)

    def fallback_guidance(self) -> str:
        return (
            "Use approved export files when API access, OAuth details, or data approval is missing. "
            "Do not guess endpoints or attempt write actions. Keep the connector disabled until "
            "tenant-specific approval is confirmed."
        )
