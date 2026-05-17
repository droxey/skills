# Perceptis Manual Import Connector

## Scope
This project implements a conservative, read-only connector for Perceptis-exported reports.

Validated boundaries:
- No direct API client
- No browser automation
- No writeback to Perceptis
- Excel and CSV are the primary supported inputs
- PDF is a documented fallback only when structured exports are unavailable

## What it does
- Loads a user-supplied CSV or Excel export
- Validates required columns against a configurable schema
- Normalizes headers and values into a stable tabular shape
- Detects duplicate rows using configurable key fields
- Produces preview and exception outputs for review
- Copies the original input into an archive folder for auditability

## Recommended workflow
1. Export a report from Perceptis as Excel or CSV.
2. Place the file into a working directory.
3. Run the connector against the exported file.
4. Review the generated preview, exceptions, and duplicate reports.
5. If the output is acceptable, pass the normalized file to the downstream system manually or through a separate approved workflow.
6. Preserve the archived original file for traceability.

## PDF fallback
PDF is intentionally not part of the automated first-pass parser in this project. If a report is only available as PDF:
- request Excel or CSV first
- if unavailable, convert PDF through a supervised extraction step outside this connector
- validate the extracted tabular output before downstream use

## Files
- `perceptis_connector/connector.py` - main import pipeline
- `perceptis_connector/schema.json` - configurable schema and duplicate rules
- `examples/sample_perceptis_report.csv` - sample input file
- `output/` - generated preview, normalized, duplicate, and exception files
- `archive/` - archived copies of original input files

## Example usage
```bash
python3 perceptis_connector/connector.py \
  --input examples/sample_perceptis_report.csv \
  --schema perceptis_connector/schema.json \
  --output-dir output \
  --archive-dir archive
```

## Outputs
- `normalized.csv`
- `preview.csv`
- `duplicates.csv`
- `exceptions.csv`
- `summary.json`

## Notes
This implementation is a staging connector only. It is intended to make exported Perceptis reporting data safe to inspect and normalize before any downstream import. It does not establish a live system integration.
