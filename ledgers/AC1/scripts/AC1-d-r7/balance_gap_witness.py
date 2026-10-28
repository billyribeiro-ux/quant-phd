"""Round-7 witness: (1) every seeded autograder transaction is dated 2024 and labelled SIMULATED;
(2) balance_gap from the reference solution is zero for random balanced ledgers over the 12 month ends.
Usage: balance_gap_witness.py <grader dir> <reference.py path>"""

import importlib.util
import json
import random
import sys
from pathlib import Path

grader = Path(sys.argv[1])
sys.path.insert(0, str(grader))
from instance import make_instance  # noqa: E402

spec = importlib.util.spec_from_file_location("ref", sys.argv[2])
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)

dated_2024 = 0
total_txns = 0
labels = set()
for seed in range(50):
    inst = make_instance(seed)
    labels.add(inst.get("label", "") if isinstance(inst, dict) else "")
    txns = json.loads(inst["payload"])
    total_txns += len(txns)
    dated_2024 += sum(1 for t in txns if t["date"].startswith("2024-"))
print(f"instances 0-49: transactions {total_txns}, dated 2024 {dated_2024}, labels seen {sorted(labels)}")

accounts = list(ref.ACCOUNTS)
rng = random.Random(7)
max_gap = 0
checked = 0
month_ends = ["2024-%02d-%02d" % (m, [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]) for m in range(1, 13)]
for _ in range(60):
    txns = []
    for _ in range(rng.randint(5, 40)):
        day = "2024-%02d-%02d" % (rng.randint(1, 12), rng.randint(1, 28))
        lines = []
        total = 0
        for _ in range(rng.randint(1, 3)):
            acct = rng.choice(accounts)
            amt = rng.randint(1, 10_000)
            if rng.random() < 0.5:
                lines.append({"account": acct, "debit": amt, "credit": 0})
                total += amt
            else:
                lines.append({"account": acct, "debit": 0, "credit": amt})
                total -= amt
        # balance the entry with a final line on cash or equity so the debits equal the credits
        if total > 0:
            lines.append({"account": "common_stock", "debit": 0, "credit": total})
        elif total < 0:
            lines.append({"account": "cash", "debit": -total, "credit": 0})
        txns.append({"date": day, "lines": lines})
    ledger = ref.post(txns)
    for end in month_ends:
        gap = ref.articulation_check(ledger, end)["balance_gap"]
        max_gap = max(max_gap, abs(gap))
        checked += 1
print(f"random balanced ledgers: month-end balance_gap values checked {checked}, max |balance_gap| = {max_gap}")
