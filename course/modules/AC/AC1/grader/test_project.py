"""Acceptance suite for the AC1 project: the three statements from a transaction ledger (statements.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your statements.py next to this file. Warnings are failures, as in the browser. The suite uses the standard
library only.

Each test checks a property or a number against the definitions in the project specification. Expected values come
from this file's own oracle, which reads the seeded ledger directly, so the suite does not import any solution. A
failure names the property it checks and never prints the expected value.
"""

from __future__ import annotations

import ast
import calendar
import copy
import json
import os
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
import statements as sol  # type: ignore[import-not-found, unused-ignore]
from instance import make_instance  # type: ignore[import-not-found, unused-ignore]

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)
TXS: list[dict[str, Any]] = json.loads(INST["payload"])
MONTH_ENDS = [f"2024-{m:02d}-{calendar.monthrange(2024, m)[1]:02d}" for m in range(1, 13)]

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
BALANCE_SHEET_KEYS = (
    "cash",
    "accounts_receivable",
    "inventory",
    "equipment",
    "accumulated_depreciation",
    "net_equipment",
    "total_assets",
    "accounts_payable",
    "long_term_debt",
    "total_liabilities",
    "common_stock",
    "retained_earnings",
    "total_equity",
    "total_liabilities_and_equity",
)
INCOME_KEYS = (
    "sales",
    "cost_of_goods_sold",
    "gross_profit",
    "operating_expenses",
    "depreciation_expense",
    "net_income",
)
CASH_FLOW_KEYS = (
    "net_income",
    "depreciation",
    "receivables",
    "inventory",
    "payables",
    "cash_from_operations",
    "capital_expenditure",
    "cash_from_investing",
    "net_borrowing",
    "stock_issued",
    "dividends_paid",
    "cash_from_financing",
    "net_change_in_cash",
    "beginning_cash",
    "ending_cash",
)
GAP_KEYS = ("balance_gap", "cash_gap", "retained_earnings_gap", "depreciation_gap")


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Fail unless call() raises ValueError: the grader checks the exception type."""
    try:
        call()
    except ValueError:
        return
    pytest.fail(f"{condition}: the specification requires a ValueError.")


# ---------------------------------------------------------------------------------------------------------------
# The oracle: expected values from the seeded ledger, computed here from the entries alone.
# ---------------------------------------------------------------------------------------------------------


def _through(end: str) -> dict[str, int]:
    """Debit minus credit for every account, over the entries dated on or before end."""
    totals = dict.fromkeys(ACCOUNTS, 0)
    for entry in TXS:
        if entry["date"] <= end:
            for line in entry["lines"]:
                totals[line["account"]] += int(line["debit"]) - int(line["credit"])
    return totals


def _previous_month_end(end: str) -> str:
    year, month = int(end[:4]), int(end[5:7])
    if month == 1:
        return "2023-12-31"
    return f"{year}-{month - 1:02d}-{calendar.monthrange(year, month - 1)[1]:02d}"


def _expected_balance_sheet(end: str) -> dict[str, int]:
    bal = _through(end)
    accumulated = -bal["accumulated_depreciation"]
    net_equipment = bal["equipment"] - accumulated
    assets = bal["cash"] + bal["accounts_receivable"] + bal["inventory"] + net_equipment
    payables = -bal["accounts_payable"]
    debt = -bal["long_term_debt"]
    stock = -bal["common_stock"]
    income = -(bal["sales"] + bal["cost_of_goods_sold"] + bal["operating_expenses"] + bal["depreciation_expense"])
    retained = income - bal["dividends"]
    liabilities = payables + debt
    equity = stock + retained
    return {
        "cash": bal["cash"],
        "accounts_receivable": bal["accounts_receivable"],
        "inventory": bal["inventory"],
        "equipment": bal["equipment"],
        "accumulated_depreciation": accumulated,
        "net_equipment": net_equipment,
        "total_assets": assets,
        "accounts_payable": payables,
        "long_term_debt": debt,
        "total_liabilities": liabilities,
        "common_stock": stock,
        "retained_earnings": retained,
        "total_equity": equity,
        "total_liabilities_and_equity": liabilities + equity,
    }


def _expected_flows(end: str) -> tuple[dict[str, int], dict[str, int]]:
    """The change in every account over the month that ends on end, and the balances at the previous month end."""
    now, before = _through(end), _through(_previous_month_end(end))
    return {account: now[account] - before[account] for account in ACCOUNTS}, before


def _expected_income(end: str) -> dict[str, int]:
    flow, _ = _expected_flows(end)
    sales = -flow["sales"]
    gross = sales - flow["cost_of_goods_sold"]
    net = gross - flow["operating_expenses"] - flow["depreciation_expense"]
    return {
        "sales": sales,
        "cost_of_goods_sold": flow["cost_of_goods_sold"],
        "gross_profit": gross,
        "operating_expenses": flow["operating_expenses"],
        "depreciation_expense": flow["depreciation_expense"],
        "net_income": net,
    }


def _expected_cash_flow(end: str) -> dict[str, int]:
    flow, before = _expected_flows(end)
    now = _through(end)
    net_income = _expected_income(end)["net_income"]
    depreciation = flow["depreciation_expense"]
    receivables = -flow["accounts_receivable"]
    inventory = -flow["inventory"]
    payables = -flow["accounts_payable"]
    operations = net_income + depreciation + receivables + inventory + payables
    capex = -flow["equipment"]
    borrowing = -flow["long_term_debt"]
    stock = -flow["common_stock"]
    dividends = -flow["dividends"]
    financing = borrowing + stock + dividends
    beginning = before["cash"]
    return {
        "net_income": net_income,
        "depreciation": depreciation,
        "receivables": receivables,
        "inventory": inventory,
        "payables": payables,
        "cash_from_operations": operations,
        "capital_expenditure": capex,
        "cash_from_investing": capex,
        "net_borrowing": borrowing,
        "stock_issued": stock,
        "dividends_paid": dividends,
        "cash_from_financing": financing,
        "net_change_in_cash": operations + capex + financing,
        "beginning_cash": beginning,
        "ending_cash": now["cash"],
    }


def _cash_postings(start_exclusive: str, end: str) -> int:
    """The cash the entries move in the window (start_exclusive, end], summed directly from the cash lines."""
    total = 0
    for entry in TXS:
        if start_exclusive < entry["date"] <= end:
            for line in entry["lines"]:
                if line["account"] == "cash":
                    total += int(line["debit"]) - int(line["credit"])
    return total


def _check_values(got: object, expected: dict[str, int], what: str, end: str) -> None:
    # The expected dict is a local of this frame; hiding the frame keeps its values out of the traceback.
    __tracebackhide__ = True
    assert isinstance(got, dict), f"the {what} must be a dict"
    for key, value in expected.items():
        if key not in got:
            pytest.fail(f"the {what} for {end} has no '{key}' entry")
        if type(got[key]) is not int:
            pytest.fail(f"the {what} for {end}: '{key}' must be an integer number of cents")
        if got[key] != value:
            pytest.fail(f"the {what} for {end}: '{key}' does not follow the definition in the specification")


# ---------------------------------------------------------------------------------------------------------------
# A small hand-built ledger with values worked out on paper, independent of the seed.
# ---------------------------------------------------------------------------------------------------------------


def _entry(day: str, lines: list[tuple[str, int, int]]) -> dict[str, Any]:
    return {"date": day, "lines": [{"account": a, "debit": d, "credit": c} for a, d, c in lines]}


SMALL: list[dict[str, Any]] = [
    _entry("2024-01-02", [("cash", 1000, 0), ("common_stock", 0, 1000)]),
    _entry("2024-01-03", [("equipment", 400, 0), ("cash", 0, 400)]),
    _entry("2024-01-04", [("inventory", 200, 0), ("accounts_payable", 0, 200)]),
    _entry("2024-01-10", [("accounts_receivable", 300, 0), ("sales", 0, 300)]),
    _entry("2024-01-15", [("cost_of_goods_sold", 120, 0), ("inventory", 0, 120)]),
    _entry("2024-01-31", [("depreciation_expense", 50, 0), ("accumulated_depreciation", 0, 50)]),
    _entry("2024-01-31", [("dividends", 40, 0), ("cash", 0, 40)]),
]
SMALL_JAN_BALANCE_SHEET = {
    "cash": 560,
    "accounts_receivable": 300,
    "inventory": 80,
    "equipment": 400,
    "accumulated_depreciation": 50,
    "net_equipment": 350,
    "total_assets": 1290,
    "accounts_payable": 200,
    "long_term_debt": 0,
    "total_liabilities": 200,
    "common_stock": 1000,
    "retained_earnings": 90,
    "total_equity": 1090,
    "total_liabilities_and_equity": 1290,
}
SMALL_JAN_CASH_FLOW = {
    "net_income": 130,
    "depreciation": 50,
    "receivables": -300,
    "inventory": -80,
    "payables": 200,
    "cash_from_operations": 0,
    "capital_expenditure": -400,
    "cash_from_investing": -400,
    "net_borrowing": 0,
    "stock_issued": 1000,
    "dividends_paid": -40,
    "cash_from_financing": 960,
    "net_change_in_cash": 560,
    "beginning_cash": 0,
    "ending_cash": 560,
}


# ---------------------------------------------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------------------------------------------


def test_chart_of_accounts_is_the_specified_table() -> None:
    assert sol.ACCOUNTS == ACCOUNTS, "ACCOUNTS must be the chart of accounts given in the starter, unchanged"


def test_seeded_ledger_posts_without_error() -> None:
    assert len(TXS) == 200, "the seeded instance must hold 200 transactions"
    sol.post(TXS)


def test_post_returns_a_ledger_that_the_functions_accept() -> None:
    ledger = sol.post(SMALL)
    sol.balance_sheet(ledger, "2024-01-31")


@pytest.mark.parametrize(
    ("condition", "transactions"),
    [
        ("a transaction without lines", [{"date": "2024-01-02"}]),
        ("a transaction without a date", [{"lines": SMALL[0]["lines"]}]),
        ("a date that is not in YYYY-MM-DD form", [{**SMALL[0], "date": "02/01/2024"}]),
        ("a date that does not exist", [{**SMALL[0], "date": "2024-02-30"}]),
        ("a date in the compact form", [{**SMALL[0], "date": "20240102"}]),
        ("a date in the ISO week form", [{**SMALL[0], "date": "2024-W01-1"}]),
        ("a date with a time of day", [{**SMALL[0], "date": "2024-01-02T10:00"}]),
        ("a date with surrounding spaces", [{**SMALL[0], "date": " 2024-01-02 "}]),
        ("an empty list of lines", [{"date": "2024-01-02", "lines": []}]),
        (
            "a line without a credit",
            [
                {
                    "date": "2024-01-02",
                    "lines": [
                        {"account": "cash", "debit": 5},
                        {"account": "common_stock", "debit": 0, "credit": 5},
                    ],
                }
            ],
        ),
        (
            "a line without a debit",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": "cash", "credit": 5},
                        {"account": "common_stock", "debit": 5, "credit": 0},
                    ],
                }
            ],
        ),
        (
            "an account outside the chart",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": "retained_earnings", "debit": 5, "credit": 0},
                        {"account": "cash", "debit": 0, "credit": 5},
                    ],
                }
            ],
        ),
        (
            "a negative amount",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": "cash", "debit": -5, "credit": 0},
                        {"account": "common_stock", "debit": 0, "credit": -5},
                    ],
                }
            ],
        ),
        (
            "an amount that is not an integer",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": "cash", "debit": 5.0, "credit": 0},
                        {"account": "common_stock", "debit": 0, "credit": 5},
                    ],
                }
            ],
        ),
        (
            "an amount that is a boolean",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": "cash", "debit": True, "credit": 0},
                        {"account": "common_stock", "debit": 0, "credit": 1},
                    ],
                }
            ],
        ),
        (
            "an account name with surrounding spaces",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": " cash ", "debit": 5, "credit": 0},
                        {"account": "common_stock", "debit": 0, "credit": 5},
                    ],
                }
            ],
        ),
        (
            "an account name in capitals",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": "Cash", "debit": 5, "credit": 0},
                        {"account": "common_stock", "debit": 0, "credit": 5},
                    ],
                }
            ],
        ),
        (
            "an amount that is a boolean on the credit side",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": "cash", "debit": 1, "credit": 0},
                        {"account": "common_stock", "debit": 0, "credit": True},
                    ],
                }
            ],
        ),
        (
            "an amount that is a float on the credit side",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": "cash", "debit": 5, "credit": 0},
                        {"account": "common_stock", "debit": 0, "credit": 5.0},
                    ],
                }
            ],
        ),
        (
            "a line with a debit and a credit",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": "cash", "debit": 5, "credit": 5},
                        {"account": "common_stock", "debit": 5, "credit": 5},
                    ],
                }
            ],
        ),
        (
            "a line with neither a debit nor a credit",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": "cash", "debit": 0, "credit": 0},
                        {"account": "common_stock", "debit": 0, "credit": 0},
                    ],
                }
            ],
        ),
        (
            "an unbalanced entry",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": "cash", "debit": 6, "credit": 0},
                        {"account": "common_stock", "debit": 0, "credit": 5},
                    ],
                }
            ],
        ),
        (
            "a line without an account",
            [{**SMALL[0], "lines": [{"debit": 5, "credit": 0}, {"account": "common_stock", "debit": 0, "credit": 5}]}],
        ),
        (
            "a negative amount that balances",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": "cash", "debit": 5, "credit": -5},
                        {"account": "common_stock", "debit": 0, "credit": 10},
                    ],
                }
            ],
        ),
        (
            "a negative credit with no negative debit",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": "cash", "debit": 5, "credit": 0},
                        {"account": "common_stock", "debit": 0, "credit": -5},
                    ],
                }
            ],
        ),
        (
            "an unbalanced entry with credits above debits",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": "cash", "debit": 5, "credit": 0},
                        {"account": "common_stock", "debit": 0, "credit": 6},
                    ],
                }
            ],
        ),
        ("a date with an unpadded month", [{**SMALL[0], "date": "2024-1-02"}]),
        ("a date with an unpadded day", [{**SMALL[0], "date": "2024-01-2"}]),
        ("a date in February of a common year that has no 29th", [{**SMALL[0], "date": "2023-02-29"}]),
        ("a date whose month is beyond twelve", [{**SMALL[0], "date": "2024-13-01"}]),
        ("a date that is not a string", [{**SMALL[0], "date": 20240102}]),
        (
            "an amount that is a numeric string on the debit side",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": "cash", "debit": "5", "credit": 0},
                        {"account": "common_stock", "debit": 0, "credit": 5},
                    ],
                }
            ],
        ),
        (
            "an amount that is a numeric string on the credit side",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": "cash", "debit": 5, "credit": 0},
                        {"account": "common_stock", "debit": 0, "credit": "5"},
                    ],
                }
            ],
        ),
        (
            "a negative debit balanced by a positive credit",
            [_entry("2024-01-02", [("cash", -5, 5), ("common_stock", 5, 0)])],
        ),
        ("a negative debit of one cent", [_entry("2024-01-02", [("cash", -1, 2), ("common_stock", 3, 0)])]),
        ("a negative credit of one cent", [_entry("2024-01-02", [("cash", 1, -1), ("common_stock", 0, 2)])]),
        (
            "an account outside the chart on the second line of an entry",
            [_entry("2024-01-02", [("cash", 5, 0), ("retained_earnings", 0, 5)])],
        ),
        ("a date that is None", [{**SMALL[0], "date": None}]),
        ("an empty date", [{**SMALL[0], "date": ""}]),
        ("a day of zero", [{**SMALL[0], "date": "2024-01-00"}]),
        ("a month of zero", [{**SMALL[0], "date": "2024-00-10"}]),
        ("a date with a letter in it", [{**SMALL[0], "date": "2024-0A-02"}]),
        ("the 31st of April", [{**SMALL[0], "date": "2024-04-31"}]),
        (
            "an account name that is None",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": None, "debit": 5, "credit": 0},
                        {"account": "common_stock", "debit": 0, "credit": 5},
                    ],
                }
            ],
        ),
        (
            "an empty account name",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": "", "debit": 5, "credit": 0},
                        {"account": "common_stock", "debit": 0, "credit": 5},
                    ],
                }
            ],
        ),
        (
            "an amount that is None",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": "cash", "debit": None, "credit": 0},
                        {"account": "common_stock", "debit": 0, "credit": 5},
                    ],
                }
            ],
        ),
        (
            "an amount that is the boolean False",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": "cash", "debit": 5, "credit": 0},
                        {"account": "common_stock", "debit": False, "credit": 5},
                    ],
                }
            ],
        ),
        (
            "an amount that is a float on the debit side",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": "cash", "debit": 5.0, "credit": 0},
                        {"account": "common_stock", "debit": 0, "credit": 5},
                    ],
                }
            ],
        ),
        (
            "an amount that is the boolean True on the debit side",
            [
                {
                    **SMALL[0],
                    "lines": [
                        {"account": "cash", "debit": True, "credit": 0},
                        {"account": "common_stock", "debit": 0, "credit": 1},
                    ],
                }
            ],
        ),
        (
            "an entry that balances only with another entry",
            [
                {"date": "2024-01-02", "lines": [{"account": "cash", "debit": 5, "credit": 0}]},
                {"date": "2024-01-03", "lines": [{"account": "common_stock", "debit": 0, "credit": 5}]},
            ],
        ),
    ],
)
def test_post_raises_a_value_error(condition: str, transactions: list[dict[str, Any]]) -> None:
    must_raise(lambda: sol.post(transactions), condition)


def test_an_invalid_entry_among_valid_ones_still_raises() -> None:
    bad = copy.deepcopy(TXS)
    bad[len(bad) // 2]["lines"][0]["debit"] = int(bad[len(bad) // 2]["lines"][0]["debit"]) + 1
    must_raise(lambda: sol.post(bad), "an unbalanced entry in the middle of a ledger")


def test_a_bad_date_in_a_later_entry_still_raises() -> None:
    must_raise(
        lambda: sol.post([SMALL[0], {**SMALL[1], "date": "2024-02-30"}]),
        "a date that does not exist, in an entry after a valid one",
    )


def test_an_account_repeated_within_one_entry_is_posted_in_full() -> None:
    # Two cash lines and one stock line in one entry: the spec's balance is the debit minus the credit of every line.
    entry = _entry("2024-01-02", [("cash", 5, 0), ("cash", 0, 2), ("common_stock", 0, 3)])
    got = sol.balance_sheet(sol.post([entry]), "2024-01-31")
    _check_values(got, {"cash": 3, "common_stock": 3}, "balance sheet", "2024-01-31")


def test_post_does_not_change_its_argument() -> None:
    # A fresh decode, not the shared TXS list: earlier tests pass TXS to post, so it may already be changed.
    fresh: list[dict[str, Any]] = json.loads(INST["payload"])
    before = copy.deepcopy(fresh)
    sol.post(fresh)
    assert fresh == before, "post must not change the transactions it is given"


def test_post_twice_gives_the_same_statements() -> None:
    first = sol.balance_sheet(sol.post(TXS), MONTH_ENDS[-1])
    second = sol.balance_sheet(sol.post(TXS), MONTH_ENDS[-1])
    assert first == second, "the same transactions must give the same statements"


def test_small_ledger_january_balance_sheet() -> None:
    _check_values(
        sol.balance_sheet(sol.post(SMALL), "2024-01-31"), SMALL_JAN_BALANCE_SHEET, "balance sheet", "2024-01-31"
    )


def test_small_ledger_january_cash_flow() -> None:
    got = sol.cash_flow_statement(sol.post(SMALL), "2024-01-31")
    _check_values(got, SMALL_JAN_CASH_FLOW, "cash flow statement", "2024-01-31")


def test_small_ledger_january_articulation_is_zero() -> None:
    got = sol.articulation_check(sol.post(SMALL), "2024-01-31")
    for key in GAP_KEYS:
        assert got.get(key) == 0, f"the articulation gap '{key}' must be zero for a ledger that articulates"


def test_small_ledger_january_income_statement() -> None:
    got = sol.income_statement(sol.post(SMALL), "2024-01-31")
    expected = {
        "sales": 300,
        "cost_of_goods_sold": 120,
        "gross_profit": 180,
        "operating_expenses": 0,
        "depreciation_expense": 50,
        "net_income": 130,
    }
    _check_values(got, expected, "income statement", "2024-01-31")


def test_a_one_cent_entry_posts_at_one_cent() -> None:
    ledger = sol.post([_entry("2024-01-02", [("cash", 1, 0), ("common_stock", 0, 1)])])
    expected = {"cash": 1, "common_stock": 1, "total_assets": 1, "total_liabilities_and_equity": 1}
    _check_values(sol.balance_sheet(ledger, "2024-01-31"), expected, "balance sheet", "2024-01-31")


def test_a_zero_on_the_debit_side_of_a_credit_line_posts() -> None:
    ledger = sol.post([_entry("2024-01-02", [("cash", 5, 0), ("common_stock", 0, 5)])])
    _check_values(
        sol.balance_sheet(ledger, "2024-01-31"), {"cash": 5, "common_stock": 5}, "balance sheet", "2024-01-31"
    )


def test_an_entry_dated_on_the_period_end_is_in_that_balance() -> None:
    ledger = sol.post([_entry("2024-01-31", [("cash", 7, 0), ("common_stock", 0, 7)])])
    _check_values(
        sol.balance_sheet(ledger, "2024-01-31"), {"cash": 7, "common_stock": 7}, "balance sheet", "2024-01-31"
    )


def test_an_entry_dated_the_day_after_the_period_end_is_not_in_that_balance() -> None:
    ledger = sol.post([_entry("2024-02-01", [("cash", 7, 0), ("common_stock", 0, 7)])])
    expected = {"cash": 0, "common_stock": 0, "total_assets": 0}
    _check_values(sol.balance_sheet(ledger, "2024-01-31"), expected, "balance sheet", "2024-01-31")


# A January sale of 100 (dated on the month end) and a February sale of 40 (dated on the first day of February).
FLOW_LEDGER: list[dict[str, Any]] = [
    _entry("2024-01-31", [("accounts_receivable", 100, 0), ("sales", 0, 100)]),
    _entry("2024-02-01", [("accounts_receivable", 40, 0), ("sales", 0, 40)]),
]


def test_a_month_counts_only_the_entries_after_the_previous_month_end() -> None:
    ledger = sol.post(FLOW_LEDGER)
    feb = {"sales": 40, "gross_profit": 40, "net_income": 40}
    _check_values(sol.income_statement(ledger, "2024-02-29"), feb, "income statement", "2024-02-29")
    jan = {"sales": 100, "gross_profit": 100, "net_income": 100}
    _check_values(sol.income_statement(ledger, "2024-01-31"), jan, "income statement", "2024-01-31")


def test_borrowing_and_repayment_move_net_borrowing_in_both_directions() -> None:
    ledger = sol.post(
        [
            _entry("2024-01-05", [("cash", 500, 0), ("long_term_debt", 0, 500)]),
            _entry("2024-02-05", [("long_term_debt", 200, 0), ("cash", 0, 200)]),
        ]
    )
    jan_flow = {"net_borrowing": 500, "cash_from_financing": 500, "beginning_cash": 0, "ending_cash": 500}
    _check_values(sol.cash_flow_statement(ledger, "2024-01-31"), jan_flow, "cash flow statement", "2024-01-31")
    feb_flow = {"net_borrowing": -200, "cash_from_financing": -200, "beginning_cash": 500, "ending_cash": 300}
    _check_values(sol.cash_flow_statement(ledger, "2024-02-29"), feb_flow, "cash flow statement", "2024-02-29")
    feb_balance = {"cash": 300, "long_term_debt": 300, "total_liabilities_and_equity": 300}
    _check_values(sol.balance_sheet(ledger, "2024-02-29"), feb_balance, "balance sheet", "2024-02-29")


def test_an_empty_list_of_transactions_gives_empty_statements() -> None:
    ledger = sol.post([])
    end = "2024-12-31"
    _check_values(sol.balance_sheet(ledger, end), dict.fromkeys(BALANCE_SHEET_KEYS, 0), "balance sheet", end)
    _check_values(sol.income_statement(ledger, end), dict.fromkeys(INCOME_KEYS, 0), "income statement", end)
    _check_values(sol.cash_flow_statement(ledger, end), dict.fromkeys(CASH_FLOW_KEYS, 0), "cash flow statement", end)
    got = sol.articulation_check(ledger, end)
    for key in GAP_KEYS:
        assert got.get(key) == 0, f"the articulation gap '{key}' must be zero for an empty ledger"


def test_a_repeated_entry_is_posted_each_time() -> None:
    ledger = sol.post([SMALL[0], SMALL[0]])
    _check_values(
        sol.balance_sheet(ledger, "2024-01-31"), {"cash": 2000, "common_stock": 2000}, "balance sheet", "2024-01-31"
    )


def test_the_order_of_the_transactions_does_not_change_the_statements() -> None:
    ledger = sol.post(list(reversed(SMALL)))
    _check_values(sol.balance_sheet(ledger, "2024-01-31"), SMALL_JAN_BALANCE_SHEET, "balance sheet", "2024-01-31")
    _check_values(
        sol.cash_flow_statement(ledger, "2024-01-31"), SMALL_JAN_CASH_FLOW, "cash flow statement", "2024-01-31"
    )


def test_two_entries_on_one_date_both_count() -> None:
    ledger = sol.post(
        [
            _entry("2024-01-31", [("cash", 10, 0), ("common_stock", 0, 10)]),
            _entry("2024-01-31", [("cash", 20, 0), ("common_stock", 0, 20)]),
        ]
    )
    _check_values(
        sol.balance_sheet(ledger, "2024-01-31"), {"cash": 30, "common_stock": 30}, "balance sheet", "2024-01-31"
    )


# Worked on paper. Cash is 1,000 less 100 paid, so the balance sheet shows cash of 900. The cash flow statement sees
# only the 1,000 of stock issued, so its ending cash is 1,000 and the cash gap is -100. The 100 debit to accumulated
# depreciation makes accumulated depreciation -100 (a debit balance), so net equipment is 100 and total assets are
# 1,000, equal to common stock. Depreciation expense is zero, so the depreciation gap is the change of -100.
GAP_WITNESS: list[dict[str, Any]] = [
    _entry("2024-01-02", [("cash", 1000, 0), ("common_stock", 0, 1000)]),
    _entry("2024-01-15", [("accumulated_depreciation", 100, 0), ("cash", 0, 100)]),
]
GAP_WITNESS_JAN = {"balance_gap": 0, "cash_gap": -100, "retained_earnings_gap": 0, "depreciation_gap": -100}


def test_articulation_gaps_report_a_ledger_that_does_not_articulate() -> None:
    got = sol.articulation_check(sol.post(GAP_WITNESS), "2024-01-31")
    _check_values(got, GAP_WITNESS_JAN, "articulation check", "2024-01-31")


def test_the_module_imports_only_the_standard_library() -> None:
    tree = ast.parse(Path(str(sol.__file__)).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.level > 0:
            pytest.fail("statements.py must not use a relative import")
        if isinstance(node, ast.Import):
            modules = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            modules = [node.module or ""]
        else:
            continue
        for name in modules:
            top = name.split(".")[0]
            if top not in sys.stdlib_module_names:
                pytest.fail(f"statements.py imports '{top}', which is not in the standard library")


def test_a_month_before_any_entry_is_empty() -> None:
    ledger = sol.post(TXS)
    got = sol.balance_sheet(ledger, "2023-12-31")
    _check_values(got, dict.fromkeys(BALANCE_SHEET_KEYS, 0), "balance sheet", "2023-12-31")


@pytest.mark.parametrize("end", MONTH_ENDS)
def test_balance_sheet_matches_the_ledger(end: str) -> None:
    got = sol.balance_sheet(sol.post(TXS), end)
    _check_values(got, _expected_balance_sheet(end), "balance sheet", end)


@pytest.mark.parametrize("end", MONTH_ENDS)
def test_income_statement_matches_the_ledger(end: str) -> None:
    got = sol.income_statement(sol.post(TXS), end)
    _check_values(got, _expected_income(end), "income statement", end)


@pytest.mark.parametrize("end", MONTH_ENDS)
def test_cash_flow_statement_matches_the_ledger(end: str) -> None:
    got = sol.cash_flow_statement(sol.post(TXS), end)
    _check_values(got, _expected_cash_flow(end), "cash flow statement", end)


@pytest.mark.parametrize("end", MONTH_ENDS)
def test_the_balance_sheet_balances(end: str) -> None:
    got = sol.balance_sheet(sol.post(TXS), end)
    assert got["total_assets"] == got["total_liabilities_and_equity"], (
        f"the balance sheet at {end} does not balance: assets must equal liabilities plus equity"
    )


@pytest.mark.parametrize("end", MONTH_ENDS)
def test_cash_flow_ends_at_the_balance_sheet_cash(end: str) -> None:
    ledger = sol.post(TXS)
    cash = sol.balance_sheet(ledger, end)["cash"]
    ending = sol.cash_flow_statement(ledger, end)["ending_cash"]
    assert cash == ending, f"the cash flow statement for {end} must end at the balance sheet's cash"


@pytest.mark.parametrize("end", MONTH_ENDS)
def test_net_change_in_cash_equals_the_cash_lines_of_the_month(end: str) -> None:
    got = sol.cash_flow_statement(sol.post(TXS), end)
    start = _previous_month_end(end)
    moved = _cash_postings(start, end)
    assert got["net_change_in_cash"] == moved, (
        f"the net change in cash for {end} must equal the cash the month's entries move"
    )


@pytest.mark.parametrize("end", MONTH_ENDS)
def test_articulation_gaps_are_zero(end: str) -> None:
    got = sol.articulation_check(sol.post(TXS), end)
    for key in GAP_KEYS:
        assert key in got, f"the articulation check has no '{key}' entry"
        assert got[key] == 0, f"the articulation gap '{key}' at {end} must be zero"


@pytest.mark.parametrize("end", MONTH_ENDS)
def test_retained_earnings_move_by_net_income_less_dividends(end: str) -> None:
    ledger = sol.post(TXS)
    now = sol.balance_sheet(ledger, end)["retained_earnings"]
    before = sol.balance_sheet(ledger, _previous_month_end(end))["retained_earnings"]
    net = sol.income_statement(ledger, end)["net_income"]
    dividends = sol.cash_flow_statement(ledger, end)["dividends_paid"]
    assert now - before == net + dividends, f"retained earnings at {end} must move by net income less dividends"


@pytest.mark.parametrize("end", MONTH_ENDS)
def test_operating_cash_flow_is_net_income_plus_add_backs_and_working_capital(end: str) -> None:
    got = sol.cash_flow_statement(sol.post(TXS), end)
    expected = got["net_income"] + got["depreciation"] + got["receivables"] + got["inventory"] + got["payables"]
    assert got["cash_from_operations"] == expected, (
        f"operating cash flow for {end} must be net income plus the non-cash add-back and the working-capital changes"
    )


@pytest.mark.parametrize("end", MONTH_ENDS)
def test_statements_hold_integer_cents_and_the_required_keys(end: str) -> None:
    ledger = sol.post(TXS)
    for name, got, keys in (
        ("balance sheet", sol.balance_sheet(ledger, end), BALANCE_SHEET_KEYS),
        ("income statement", sol.income_statement(ledger, end), INCOME_KEYS),
        ("cash flow statement", sol.cash_flow_statement(ledger, end), CASH_FLOW_KEYS),
    ):
        assert isinstance(got, dict), f"the {name} must be a dict"
        for key in keys:
            assert key in got, f"the {name} for {end} has no '{key}' entry"
            assert type(got[key]) is int, f"the {name} for {end}: '{key}' must be an integer number of cents"


@pytest.mark.parametrize(
    "call",
    [
        lambda ledger, end: sol.balance_sheet(ledger, end),
        lambda ledger, end: sol.income_statement(ledger, end),
        lambda ledger, end: sol.cash_flow_statement(ledger, end),
        lambda ledger, end: sol.articulation_check(ledger, end),
    ],
)
@pytest.mark.parametrize(
    "period_end",
    [
        "2024-02-28",
        "2024-1-31",
        "2024-02-30",
        "31/01/2024",
        "2024-01-31T00:00",
        "2024-04-15",
        "2024-01-30",
        "2024-04-31",
        "2024-03-01",
        "2024-03-30",
        "2024-06-29",
        "2024-12-30",
        "2023-02-27",
        "",
        " 2024-01-31",
    ],
)
def test_period_end_must_be_a_month_end(call: Callable[[object, str], object], period_end: str) -> None:
    ledger = sol.post(TXS)
    must_raise(lambda: call(ledger, period_end), f"a period end of {period_end!r}")


@pytest.mark.parametrize("bad_end", [20240131, None, True])
def test_a_period_end_that_is_not_a_string_is_rejected(bad_end: Any) -> None:
    ledger = sol.post(TXS)
    condition = f"a period end of {bad_end!r} that is not a string"
    must_raise(lambda: sol.balance_sheet(ledger, bad_end), condition)
    must_raise(lambda: sol.income_statement(ledger, bad_end), condition)
    must_raise(lambda: sol.cash_flow_statement(ledger, bad_end), condition)
    must_raise(lambda: sol.articulation_check(ledger, bad_end), condition)


def test_a_leap_year_month_end_is_accepted() -> None:
    ledger = sol.post(TXS)
    sol.balance_sheet(ledger, "2024-02-29")
    sol.cash_flow_statement(ledger, "2024-02-29")


def test_a_non_leap_year_february_end_is_accepted() -> None:
    # 2023 is not in the ledger, so every balance through its February end is zero.
    _check_values(
        sol.balance_sheet(sol.post(TXS), "2023-02-28"),
        dict.fromkeys(BALANCE_SHEET_KEYS, 0),
        "balance sheet",
        "2023-02-28",
    )


def test_the_statements_return_fresh_objects() -> None:
    ledger = sol.post(TXS)
    first = sol.balance_sheet(ledger, MONTH_ENDS[2])
    first["cash"] = -999_999
    second = sol.balance_sheet(ledger, MONTH_ENDS[2])
    assert second is not first, "balance_sheet must return a new dict on each call"
    assert second == _expected_balance_sheet(MONTH_ENDS[2]), "a change to a returned dict must not reach later calls"


def test_the_functions_are_silent(capsys: pytest.CaptureFixture[str]) -> None:
    ledger = sol.post(TXS)
    sol.balance_sheet(ledger, MONTH_ENDS[5])
    sol.income_statement(ledger, MONTH_ENDS[5])
    sol.cash_flow_statement(ledger, MONTH_ENDS[5])
    sol.articulation_check(ledger, MONTH_ENDS[5])
    assert capsys.readouterr().out == "", "the functions must not print"
