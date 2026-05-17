from typing import Any, Dict, Iterable, List


ALLOWED_RECORD_KEYS = {
    "id",
    "export_id",
    "survey_id",
    "survey_name",
    "status",
    "created_at",
    "updated_at",
    "completed_at",
    "respondent_id",
    "dataset",
    "region",
    "source_file",
}


def normalize_record(record: Dict[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = {}
    for key in ALLOWED_RECORD_KEYS:
        if key in record:
            normalized[key] = record[key]
    return normalized


def normalize_records(records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [normalize_record(record) for record in records]


def normalize_list_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    items = payload.get("items", [])
    return {
        "mode": "list",
        "count": len(items),
        "items": normalize_records(items),
    }


def normalize_fetch_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    record = payload.get("record", payload)
    return {
        "mode": "fetch",
        "record": normalize_record(record if isinstance(record, dict) else {}),
    }


def normalize_export_file_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    output = {
        "mode": "export_file",
        "file_name": metadata.get("file_name"),
        "file_format": metadata.get("file_format"),
        "dataset": metadata.get("dataset"),
        "created_at": metadata.get("created_at"),
        "source_file": metadata.get("source_file"),
    }
    return {k: v for k, v in output.items() if v is not None}
