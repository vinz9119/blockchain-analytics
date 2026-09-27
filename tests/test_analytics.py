import unittest
from decimal import Decimal

from analytics import (
    active_addresses,
    asset_totals,
    normalize_transaction,
    sender_concentration,
    transaction_count,
)


class AnalyticsTests(unittest.TestCase):
    def setUp(self):
        self.transactions = [
            {"tx_hash": "a", "sender": "alice", "recipient": "bob", "asset": "sui", "amount": "2"},
            {"tx_hash": "b", "sender": "alice", "recipient": "carol", "asset": "SUI", "amount": "3"},
            {"tx_hash": "c", "sender": "bob", "recipient": "alice", "asset": "USDC", "amount": "7"},
        ]

    def test_normalization(self):
        tx = normalize_transaction(self.transactions[0])
        self.assertEqual(tx["asset"], "SUI")
        self.assertEqual(tx["amount"], Decimal("2"))

    def test_counts_and_addresses(self):
        self.assertEqual(transaction_count(self.transactions), 3)
        self.assertEqual(active_addresses(self.transactions), {"alice", "bob", "carol"})

    def test_asset_totals(self):
        self.assertEqual(asset_totals(self.transactions), {"SUI": Decimal("5"), "USDC": Decimal("7")})

    def test_concentration(self):
        result = sender_concentration(self.transactions)
        self.assertAlmostEqual(result["alice"], 2 / 3)
        self.assertAlmostEqual(result["bob"], 1 / 3)


if __name__ == "__main__":
    unittest.main()
