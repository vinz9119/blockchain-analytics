# Blockchain Analytics

A small, reproducible toolkit for normalizing blockchain transaction data and computing transparent activity metrics.

## Scope
- Normalize JSON/CSV transaction records into a stable schema.
- Compute transaction counts, active-address counts, token-flow totals, and concentration metrics.
- Keep raw data separate from derived metrics.
- Make assumptions and filtering rules explicit.

## Status
Early implementation. The project intentionally uses the Python standard library only so the core logic is easy to run and audit.

## Example

```bash
python -m unittest discover -s tests
```
