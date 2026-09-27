# Blockchain Analytics

A small, reproducible toolkit for normalizing blockchain transaction data and computing transparent activity metrics.

## What it does

- Normalize JSON/CSV transaction records into a stable schema.
- Compute transaction counts, active-address counts, token-flow totals, and sender concentration.
- Generate a machine-readable JSON activity report from a local dataset.
- Keep raw data separate from derived metrics.
- Use only the Python standard library.

## Quick start

Run the tests:

```bash
python -m unittest discover -s tests -v
```

Generate a report from the included example:

```bash
python report.py examples/transactions.json
```

Write the report to a file:

```bash
python report.py examples/transactions.json --output report.json
```

CSV files with columns such as `tx_hash,sender,recipient,asset,amount,timestamp,status` are also supported:

```bash
python report.py transactions.csv
```

## Example output

The example dataset produces a report containing:

- 3 transactions
- 3 active addresses
- SUI total: 5
- USDC total: 7
- Sender concentration, with Alice responsible for 2/3 of the sample transactions

The metrics are descriptive only; they do not attempt to label activity as legitimate, suspicious, profitable, or otherwise.

## Design goals

1. **Reproducibility** — the same input produces the same report.
2. **Transparency** — calculations are simple and inspectable.
3. **Portability** — no third-party Python dependencies are required.
4. **Conservative interpretation** — metrics describe observed records rather than making unsupported claims.

## Status

Working prototype with unit tests and GitHub Actions CI.