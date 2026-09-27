"""Command-line report generator for simple blockchain transaction datasets."""

import argparse
import csv
import json
from pathlib import Path

from analytics import (
    active_addresses,
    asset_totals,
    normalize_transaction,
    sender_concentration,
    transaction_count,
)


def load_transactions(path: str) -> list[dict]:
    source = Path(path)
    if source.suffix.lower() == ".json":
        data = json.loads(source.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("JSON input must contain an array of transactions.")
        return [normalize_transaction(tx) for tx in data]

    if source.suffix.lower() == ".csv":
        with source.open(newline="", encoding="utf-8") as handle:
            return [normalize_transaction(row) for row in csv.DictReader(handle)]

    raise ValueError("Input must be a .json or .csv file.")


def build_report(transactions: list[dict]) -> dict:
    concentration = sender_concentration(transactions)
    return {
        "transactions": transaction_count(transactions),
        "active_addresses": len(active_addresses(transactions)),
        "asset_totals": {asset: str(amount) for asset, amount in asset_totals(transactions).items()},
        "top_senders": [
            {"address": address, "share": round(share, 6)}
            for address, share in sorted(
                concentration.items(), key=lambda item: (-item[1], item[0])
            )
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a transparent activity summary from JSON or CSV transactions."
    )
    parser.add_argument("input", help="Path to a .json or .csv transaction file.")
    parser.add_argument("-o", "--output", help="Optional path for a JSON report.")
    args = parser.parse_args()

    report = build_report(load_transactions(args.input))
    rendered = json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
