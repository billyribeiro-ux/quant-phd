"""Per-learner instances for the AC1 autograder: a seeded 200-transaction ledger for 2024.

make_instance(seed) is deterministic. Every instance is balanced (each entry's debits equal its credits), uses only
accounts of the chart of accounts, and carries integer cents. The seed changes the amounts, the accounts, the dates
and the mix of entry types. All data are SIMULATED: generated, not a real company's figures.

Standard library only.
"""

from __future__ import annotations

import calendar
import json
import random
from datetime import date
from typing import Any

YEAR = 2024
COUNT = 200


def _entry(day: str, lines: list[tuple[str, int, int]]) -> dict[str, Any]:
    return {
        "date": day,
        "lines": [{"account": account, "debit": debit, "credit": credit} for account, debit, credit in lines],
    }


def _two(day: str, debit_account: str, credit_account: str, cents: int) -> dict[str, Any]:
    return _entry(day, [(debit_account, cents, 0), (credit_account, 0, cents)])


def _day(rng: random.Random, month: int) -> str:
    last = calendar.monthrange(YEAR, month)[1]
    return date(YEAR, month, rng.randint(1, last)).isoformat()


# Entry types for the random part of the ledger: (name, debit account, credit account, weight, low, high), in cents.
_KINDS: list[tuple[str, str, str, int, int, int]] = [
    ("sale_credit", "accounts_receivable", "sales", 30, 50_000, 900_000),
    ("sale_cash", "cash", "sales", 25, 50_000, 900_000),
    ("collection", "cash", "accounts_receivable", 18, 50_000, 900_000),
    ("inventory_credit", "inventory", "accounts_payable", 10, 100_000, 800_000),
    ("supplier_payment", "accounts_payable", "cash", 8, 100_000, 800_000),
    ("cost_of_sales", "cost_of_goods_sold", "inventory", 25, 40_000, 700_000),
    ("opex_cash", "operating_expenses", "cash", 14, 20_000, 300_000),
    ("opex_accrued", "operating_expenses", "accounts_payable", 8, 20_000, 300_000),
    ("borrow", "cash", "long_term_debt", 2, 500_000, 3_000_000),
    ("repay", "long_term_debt", "cash", 2, 100_000, 800_000),
    ("dividend", "dividends", "cash", 2, 50_000, 400_000),
    ("stock_issue", "cash", "common_stock", 1, 500_000, 2_000_000),
]


def make_instance(seed: int) -> dict[str, Any]:
    rng = random.Random(7_919 * int(seed) + 104_729)
    entries: list[dict[str, Any]] = []

    # Fixed structure: opening capital, one depreciation entry per month, and three equipment purchases.
    entries.append(_two(f"{YEAR}-01-02", "cash", "common_stock", rng.randint(60_000_000, 90_000_000)))
    for month in range(1, 13):
        last = calendar.monthrange(YEAR, month)[1]
        cents = rng.randint(150_000, 300_000)
        entries.append(
            _two(f"{YEAR}-{month:02d}-{last:02d}", "depreciation_expense", "accumulated_depreciation", cents)
        )
    for _ in range(3):
        counter = rng.choice(["cash", "accounts_payable", "long_term_debt"])
        entries.append(_two(_day(rng, rng.randint(1, 12)), "equipment", counter, rng.randint(1_000_000, 4_000_000)))

    # Random part: a weighted mix of the kinds above, until the ledger has COUNT entries.
    weights = [kind[3] for kind in _KINDS]
    while len(entries) < COUNT:
        _, debit_account, credit_account, _weight, low, high = rng.choices(_KINDS, weights=weights, k=1)[0]
        entries.append(_two(_day(rng, rng.randint(1, 12)), debit_account, credit_account, rng.randint(low, high)))

    entries.sort(key=lambda entry: entry["date"])
    return {
        "seed": int(seed),
        "label": "SIMULATED",
        "payload": json.dumps(entries, sort_keys=True),
    }
