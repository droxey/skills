# Export-First Fallback Guidance

Keep the connector disabled when any of the following are true:
- API access is not approved.
- Data release or equivalent approval is not confirmed.
- Tenant base URL or OAuth details are missing.
- Approved datasets are not identified.

## What to do instead

1. Request or obtain an approved export from Perceptyx through the customer's supported process.
2. Use the exported file as the system of record for downstream normalization.
3. Record the tenant, dataset, date range, delivery method, and approval source.
4. Re-check whether direct API access has been approved before adding any networked behavior.

## Explicit non-goals

Do not add:
- Write operations
- Endpoint guesses
- Browser automation for login
- HRIS inbound connectors
- Background polling or syncing

## Suggested export metadata to capture

- file_name
- file_format
- dataset
- created_at
- source_file
- approval_reference
- tenant_name
- tenant_region
