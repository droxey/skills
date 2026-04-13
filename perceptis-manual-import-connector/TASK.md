# Perceptis Manual Import Recipe

## Purpose
Process Perceptis-exported report files through a safe, read-only staging workflow without assuming any direct system integration surface.

## Default standards
Apply these defaults unless the user explicitly overrides them:
- Accept Excel or CSV exports first.
- Treat PDF as a documented fallback only.
- Do not build or use a direct API client.
- Do not automate browser interaction with the live Perceptis UI.
- Do not write data back into Perceptis.
- Validate schemas before normalization.
- Produce preview, duplicate, and exception outputs for review.
- Archive the original source file for auditability.

## Expected inputs
- A Perceptis-exported CSV or Excel report file.
- Optional schema adjustments for the specific report variant.
- Optional downstream field mapping requirements.

## Outputs
- A normalized CSV suitable for downstream review.
- A preview file containing a limited sample of normalized rows.
- A duplicate report using configured key fields.
- An exception report covering schema and row-level problems.
- A summary file with counts and generated artifact paths.
- An archived copy of the original source file.

## Recommended folder shape
```text
perceptis-manual-import-connector/
  archive/
  examples/
  output/
  perceptis_connector/
    connector.py
    schema.json
  README.md
```

## Workflow
1. Confirm the request remains within the validated scope:
   - read-only import
   - Excel or CSV first
   - no API assumptions
   - no browser automation
   - no writeback
2. Obtain the exported report from the user or customer admin.
3. Review the schema configuration and adjust required or optional columns only if justified by the report format.
4. Run the connector against the source file.
5. Review generated outputs:
   - normalized data
   - preview sample
   - duplicates
   - exceptions
   - summary metadata
6. If the report exists only as PDF, stop automated processing and document a supervised extraction fallback instead of expanding the connector scope.
7. Preserve the original file in the archive folder and report all output paths.

## Verification checklist
- Source file is CSV or Excel unless PDF fallback was explicitly documented.
- No live Perceptis access was used.
- Required columns were checked before downstream use.
- Duplicate detection ran against the configured key fields.
- Exceptions were generated when rows or schema elements were invalid.
- Original source file was archived.

## Implementation notes
This recipe intentionally limits the connector to manual imports from user-visible exports. Upgrade to a direct integration only if official Perceptis integration documentation or approved enterprise access is later provided.
