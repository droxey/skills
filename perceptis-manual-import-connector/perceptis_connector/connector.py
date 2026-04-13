import argparse
import json
import shutil
from pathlib import Path

import pandas as pd


def load_schema(schema_path: Path) -> dict:
    with schema_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_input(input_path: Path) -> pd.DataFrame:
    suffix = input_path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(input_path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(input_path)
    raise ValueError(
        "Unsupported input format. Use CSV or Excel for automated processing. "
        "PDF is documented fallback only and is not auto-parsed by this connector."
    )


def normalize_headers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(col).strip() for col in df.columns]
    return df


def validate_required_columns(df: pd.DataFrame, schema: dict) -> list:
    required = schema.get("required_columns", [])
    missing = [col for col in required if col not in df.columns]
    return missing


def apply_rename_map(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    rename_map = schema.get("rename_map", {})
    return df.rename(columns=rename_map)


def normalize_values(df: pd.DataFrame, schema: dict) -> tuple[pd.DataFrame, list[dict]]:
    df = df.copy()
    exceptions = []

    for col in schema.get("string_trim_columns", []):
        if col in df.columns:
            df[col] = df[col].astype("string").fillna("").str.strip()

    for col in schema.get("date_columns", []):
        if col in df.columns:
            parsed = pd.to_datetime(df[col], errors="coerce")
            bad_mask = parsed.isna() & df[col].notna() & (df[col].astype("string").str.strip() != "")
            for idx in df[bad_mask].index.tolist():
                exceptions.append({
                    "row_number": int(idx) + 2,
                    "column": col,
                    "issue": "invalid_date",
                    "value": str(df.at[idx, col]),
                })
            df[col] = parsed.dt.strftime("%Y-%m-%d")

    for col in schema.get("numeric_columns", []):
        if col in df.columns:
            parsed = pd.to_numeric(df[col], errors="coerce")
            bad_mask = parsed.isna() & df[col].notna() & (df[col].astype("string").str.strip() != "")
            for idx in df[bad_mask].index.tolist():
                exceptions.append({
                    "row_number": int(idx) + 2,
                    "column": col,
                    "issue": "invalid_number",
                    "value": str(df.at[idx, col]),
                })
            df[col] = parsed

    return df, exceptions


def detect_missing_required_values(df: pd.DataFrame, schema: dict) -> list[dict]:
    exceptions = []
    normalized_required = [schema.get("rename_map", {}).get(col, col) for col in schema.get("required_columns", [])]
    for col in normalized_required:
        if col not in df.columns:
            continue
        mask = df[col].isna() | (df[col].astype("string").fillna("").str.strip() == "")
        for idx in df[mask].index.tolist():
            exceptions.append({
                "row_number": int(idx) + 2,
                "column": col,
                "issue": "missing_required_value",
                "value": "",
            })
    return exceptions


def detect_duplicates(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    key_cols = schema.get("duplicate_key_columns", [])
    usable_keys = [col for col in key_cols if col in df.columns]
    if not usable_keys:
        return df.iloc[0:0].copy()
    return df[df.duplicated(subset=usable_keys, keep=False)].copy()


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def archive_source(input_path: Path, archive_dir: Path) -> Path:
    ensure_dir(archive_dir)
    archived_path = archive_dir / input_path.name
    shutil.copy2(input_path, archived_path)
    return archived_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Perceptis manual import connector")
    parser.add_argument("--input", required=True, help="Path to CSV or Excel export")
    parser.add_argument("--schema", required=True, help="Path to schema JSON")
    parser.add_argument("--output-dir", required=True, help="Directory for generated outputs")
    parser.add_argument("--archive-dir", required=True, help="Directory for archived original inputs")
    args = parser.parse_args()

    input_path = Path(args.input)
    schema_path = Path(args.schema)
    output_dir = Path(args.output_dir)
    archive_dir = Path(args.archive_dir)

    ensure_dir(output_dir)
    ensure_dir(archive_dir)

    schema = load_schema(schema_path)
    df = load_input(input_path)
    df = normalize_headers(df)

    missing_columns = validate_required_columns(df, schema)
    if missing_columns:
        exceptions = pd.DataFrame([
            {
                "row_number": "",
                "column": col,
                "issue": "missing_required_column",
                "value": "",
            }
            for col in missing_columns
        ])
        exceptions.to_csv(output_dir / "exceptions.csv", index=False)
        summary = {
            "status": "failed",
            "reason": "missing_required_columns",
            "missing_columns": missing_columns,
            "artifacts": {
                "exceptions": str(output_dir / "exceptions.csv"),
            },
        }
        with (output_dir / "summary.json").open("w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        archive_source(input_path, archive_dir)
        return

    df = apply_rename_map(df, schema)
    df, normalization_exceptions = normalize_values(df, schema)
    required_value_exceptions = detect_missing_required_values(df, schema)
    duplicates = detect_duplicates(df, schema)

    preview_row_limit = int(schema.get("preview_row_limit", 25))
    preview = df.head(preview_row_limit).copy()
    exceptions = pd.DataFrame(normalization_exceptions + required_value_exceptions)
    if exceptions.empty:
        exceptions = pd.DataFrame(columns=["row_number", "column", "issue", "value"])

    normalized_path = output_dir / "normalized.csv"
    preview_path = output_dir / "preview.csv"
    duplicates_path = output_dir / "duplicates.csv"
    exceptions_path = output_dir / "exceptions.csv"
    summary_path = output_dir / "summary.json"

    df.to_csv(normalized_path, index=False)
    preview.to_csv(preview_path, index=False)
    duplicates.to_csv(duplicates_path, index=False)
    exceptions.to_csv(exceptions_path, index=False)
    archived_path = archive_source(input_path, archive_dir)

    summary = {
        "status": "ok",
        "input_file": str(input_path),
        "archived_input": str(archived_path),
        "row_count": int(len(df)),
        "preview_row_count": int(len(preview)),
        "duplicate_row_count": int(len(duplicates)),
        "exception_count": int(len(exceptions)),
        "artifacts": {
            "normalized": str(normalized_path),
            "preview": str(preview_path),
            "duplicates": str(duplicates_path),
            "exceptions": str(exceptions_path),
            "summary": str(summary_path),
        },
    }
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)


if __name__ == "__main__":
    main()
