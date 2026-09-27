"""Small standard-library blockchain activity analytics helpers."""

from collections import Counter
from decimal import Decimal
from typing import Iterable, Mapping


def normalize_transaction(tx: Mapping) -> dict:
    """Return a stable transaction record from a loose mapping."""
    return {
        "tx_hash": str(tx.get("tx_hash", "")).strip(),
        "sender": str(tx.get("sender", "")).strip(),
        "recipient": str(tx.get("recipient", "")).strip(),
        "asset": str(tx.get("asset", "")).strip().upper(),
        "amount": Decimal(str(tx.get("amount", "0"))),
        "timestamp": str(tx.get("timestamp", "")).strip(),
        "status": str(tx.get("status", "unknown")).strip().lower(),
    }


def transaction_count(transactions: Iterable[Mapping]) -> int:
    return sum(1 for _ in transactions)


def active_addresses(transactions: Iterable[Mapping]) -> set[str]:
    addresses: set[str] = set()
    for tx in transactions:
        for key in ("sender", "recipient"):
            value = str(tx.get(key, "")).strip()
            if value:
                addresses.add(value)
    return addresses


def asset_totals(transactions: Iterable[Mapping]) -> dict[str, Decimal]:
    totals: Counter[str] = Counter()
    for tx in transactions:
        asset = str(tx.get("asset", "")).strip().upper()
        if asset:
            totals[asset] += Decimal(str(tx.get("amount", "0")))
    return dict(totals)


def sender_concentration(transactions: Iterable[Mapping]) -> dict[str, float]:
    counts = Counter(str(tx.get("sender", "")).strip() for tx in transactions)
    counts.pop("", None)
    total = sum(counts.values())
    if not total:
        return {}
    return {address: count / total for address, count in counts.items()}
