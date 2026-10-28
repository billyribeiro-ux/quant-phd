"""Per-learner instances for the AC1 autograder: a seeded 200-transaction ledger for 2024.

make_instance(seed) is deterministic. Every instance is balanced (each entry's debits equal its credits), uses only
accounts of the chart of accounts, and carries integer cents. The seed changes the amounts, the accounts, the dates
and the mix of entry types. No cash, receivable, inventory, equipment (net of accumulated depreciation), payable or
debt balance is ever negative on any date: an entry that would overdraw an account is capped at the balance on hand,
and an entry whose capped amount is below MIN_CENTS is replaced by a credit sale, which overdraws nothing. All data
are SIMULATED: generated, not a real company's figures.

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
# A slot whose amount, capped at the balance on hand, falls below this many cents (USD 100) posts a credit sale instead.
MIN_CENTS = 10_000

_ACCOUNTS = (
    "cash",
    "accounts_receivable",
    "inventory",
    "equipment",
    "accumulated_depreciation",
    "accounts_payable",
    "long_term_debt",
    "common_stock",
    "dividends",
    "sales",
    "cost_of_goods_sold",
    "operating_expenses",
    "depreciation_expense",
)
_ASSETS = ("cash", "accounts_receivable", "inventory", "equipment")

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


def _room(balance: dict[str, int], debit_account: str, credit_account: str) -> int | None:
    """The most cents this entry may move without an asset, payable or debt going negative; None if it is unlimited.

    balance holds debit minus credit per account, in cents, over the entries already posted. Net equipment is the
    equipment balance less the accumulated depreciation credit, so a depreciation credit is limited by it.
    """
    limits: list[int] = []
    if credit_account in _ASSETS:
        limits.append(balance[credit_account])
    if credit_account == "accumulated_depreciation":
        limits.append(balance["equipment"] + balance["accumulated_depreciation"])
    if debit_account in ("accounts_payable", "long_term_debt"):
        limits.append(-balance[debit_account])
    return min(limits) if limits else None


def make_instance(seed: int) -> dict[str, Any]:
    rng = random.Random(7_919 * int(seed) + 104_729)

    # Slots: (day, debit account, credit account, cents wanted). Opening capital, one depreciation entry per month
    # and three equipment purchases come first; then a weighted mix of the kinds above, until there are COUNT slots.
    slots: list[tuple[str, str, str, int]] = [
        (f"{YEAR}-01-02", "cash", "common_stock", rng.randint(60_000_000, 90_000_000)),
    ]
    for month in range(1, 13):
        last = calendar.monthrange(YEAR, month)[1]
        slots.append(
            (
                f"{YEAR}-{month:02d}-{last:02d}",
                "depreciation_expense",
                "accumulated_depreciation",
                rng.randint(150_000, 300_000),
            )
        )
    for _ in range(3):
        counter = rng.choice(["cash", "accounts_payable", "long_term_debt"])
        slots.append((_day(rng, rng.randint(1, 12)), "equipment", counter, rng.randint(1_000_000, 4_000_000)))
    weights = [kind[3] for kind in _KINDS]
    while len(slots) < COUNT:
        _, debit_account, credit_account, _weight, low, high = rng.choices(_KINDS, weights=weights, k=1)[0]
        slots.append((_day(rng, rng.randint(1, 12)), debit_account, credit_account, rng.randint(low, high)))

    # Post in date order (the sort is stable, so equal dates keep their slot order), capping each amount so that no
    # asset, payable or debt balance goes negative on any date. Each slot posts exactly one entry.
    balance = dict.fromkeys(_ACCOUNTS, 0)
    entries: list[dict[str, Any]] = []
    for day, debit_account, credit_account, wanted in sorted(slots, key=lambda slot: slot[0]):
        room = _room(balance, debit_account, credit_account)
        cents = wanted if room is None else min(wanted, room)
        if cents < MIN_CENTS:
            debit_account, credit_account = "accounts_receivable", "sales"
            cents = rng.randint(50_000, 900_000)
        balance[debit_account] += cents
        balance[credit_account] -= cents
        entries.append(_two(day, debit_account, credit_account, cents))

    return {
        "seed": int(seed),
        "label": "SIMULATED",
        "payload": json.dumps(entries, sort_keys=True),
    }
