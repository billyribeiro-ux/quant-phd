"""Starter for the AC1 project: statements.py, the three statements from a transaction ledger.

Implement every function to the specification (project page, section "Rung 3 · Specification"), then run the
autograder there, or locally with the browser's flags:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

The chart of accounts below is given. Do not import any file from the grader: the module must run on its own, with
the standard library only. Every function validates its inputs and raises ValueError for the conditions the
specification names. None may print or warn, or change its arguments.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

# The chart of accounts is given. Each account has one class; the class fixes its normal balance:
# asset, distribution and expense are debit-normal; contra_asset, liability, equity and revenue are credit-normal.
ACCOUNTS: dict[str, str] = {
    "cash": "asset",
    "accounts_receivable": "asset",
    "inventory": "asset",
    "equipment": "asset",
    "accumulated_depreciation": "contra_asset",
    "accounts_payable": "liability",
    "long_term_debt": "liability",
    "common_stock": "equity",
    "dividends": "distribution",
    "sales": "revenue",
    "cost_of_goods_sold": "expense",
    "operating_expenses": "expense",
    "depreciation_expense": "expense",
}

# A Ledger is whatever post returns. Callers never look inside it; they pass it to the functions below.
Ledger = Any


def post(transactions: Sequence[Mapping[str, Any]]) -> Ledger:
    """Validate the entries and return the ledger. Raises ValueError as the specification names."""
    raise NotImplementedError("post is not implemented yet")


def balance_sheet(ledger: Ledger, period_end: str) -> dict[str, int]:
    """Balances through period_end, in integer cents. Raises ValueError for a period end that is not a month end."""
    raise NotImplementedError("balance_sheet is not implemented yet")


def income_statement(ledger: Ledger, period_end: str) -> dict[str, int]:
    """The month that ends on period_end, in integer cents. Raises ValueError as for balance_sheet."""
    raise NotImplementedError("income_statement is not implemented yet")


def cash_flow_statement(ledger: Ledger, period_end: str) -> dict[str, int]:
    """The month that ends on period_end, indirect method, in integer cents. Raises ValueError as for balance_sheet."""
    raise NotImplementedError("cash_flow_statement is not implemented yet")


def articulation_check(ledger: Ledger, period_end: str) -> dict[str, int]:
    """Four gaps for the month that ends on period_end. Each is zero when the statements articulate."""
    raise NotImplementedError("articulation_check is not implemented yet")
