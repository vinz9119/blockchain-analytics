import json
import tempfile
import unittest
from pathlib import Path

from report import build_report, load_transactions


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.transactions = [
            {"sender": "alice", "recipient": "bob", "asset": "sui", "amount": "2"},
            {"sender": "alice", "recipient": "carol", "asset": "SUI", "amount": "3"},
            {"sender": "bob", "recipient": "alice", "asset": "USDC", "amount": "7"},
        ]

    def test_build_report(self):
        report = build_report(self.transactions)
        self.assertEqual(report["transactions"], 3)
        self.assertEqual(report["active_addresses"], 3)
        self.assertEqual(report["asset_totals"], {"SUI": "5", "USDC": "7"})
        self.assertEqual(report["top_senders"][0]["address"], "alice")

    def test_load_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "transactions.json"
            path.write_text(json.dumps(self.transactions), encoding="utf-8")
            loaded = load_transactions(str(path))
            self.assertEqual(loaded[0]["asset"], "SUI")

    def test_load_csv(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "transactions.csv"
            path.write_text(
                "sender,recipient,asset,amount\nalice,bob,SUI,2\n",
                encoding="utf-8",
            )
            loaded = load_transactions(str(path))
            self.assertEqual(loaded[0]["amount"], "2")


if __name__ == "__main__":
    unittest.main()
