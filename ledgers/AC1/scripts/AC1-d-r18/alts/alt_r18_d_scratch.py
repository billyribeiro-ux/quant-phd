"""Round-18 verifier alternative D: written from the page's Constraints and Conventions, not from the reference.

Ledger is a list of plain dicts (date, account, signed cents). Dates are checked by strptime plus a strftime round
trip; the last day of a month comes from the first day of the next month; balances are summed on demand.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any

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


def _parse_day(value: object) -> date:
    if not isinstance(value, str) or len(value) != 10:
        raise ValueError("a date is YYYY-MM-DD")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as error:
        raise ValueError("a date is YYYY-MM-DD") from error
    if parsed.strftime("%Y-%m-%d") != value:
        raise ValueError("a date is YYYY-MM-DD")
    return parsed


def _amount(value: object) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError("an amount is an integer number of cents")
    if value < 0:
        raise ValueError("an amount is not negative")
    return value


def _last_day(year: int, month: int) -> int:
    first_of_next = date(year + (month == 12), month % 12 + 1, 1)
    return (first_of_next - timedelta(days=1)).day


def _month_end(period_end: object) -> date:
    day = _parse_day(period_end)
    if day.day != _last_day(day.year, day.month):
        raise ValueError("a period end is a month end")
    return day


def post(transactions: Any) -> list[dict[str, Any]]:
    ledger: list[dict[str, Any]] = []
    for entry in transactions:
        if not isinstance(entry, dict) or "date" not in entry or "lines" not in entry:
            raise ValueError("a transaction has a date and lines")
        when = _parse_day(entry["date"])
        lines = entry["lines"]
        if not isinstance(lines, list) or not lines:
            raise ValueError("a transaction has at least one line")
        net = 0
        staged = []
        for line in lines:
            if not isinstance(line, dict) or set(line) < {"account", "debit", "credit"}:
                raise ValueError("a line has an account, a debit and a credit")
            name = line["account"]
            if not isinstance(name, str) or name not in ACCOUNTS:
                raise ValueError("an account is in the chart")
            dr, cr = _amount(line["debit"]), _amount(line["credit"])
            if (dr > 0) is (cr > 0):
                raise ValueError("a line has exactly one of a debit or a credit")
            staged.append({"date": when.isoformat(), "account": name, "signed": dr - cr})
            net += dr - cr
        if net != 0:
            raise ValueError("the entry is unbalanced")
        ledger.extend(staged)
    return ledger


def _through(ledger: list[dict[str, Any]], end: date) -> dict[str, int]:
    totals = {name: 0 for name in ACCOUNTS}
    for row in ledger:
        if date.fromisoformat(row["date"]) <= end:
            totals[row["account"]] += row["signed"]
    return totals


def _prior_end(end: date) -> date:
    return date(end.year, end.month, 1) - timedelta(days=1)


def _sheet(bal: dict[str, int]) -> dict[str, int]:
    acc = -bal["accumulated_depreciation"]
    equip_net = bal["equipment"] - acc
    assets = bal["cash"] + bal["accounts_receivable"] + bal["inventory"] + equip_net
    liab = -bal["accounts_payable"] - bal["long_term_debt"]
    stock = -bal["common_stock"]
    earned = -(bal["sales"] + bal["cost_of_goods_sold"] + bal["operating_expenses"] + bal["depreciation_expense"])
    retained = earned - bal["dividends"]
    equity = stock + retained
    return {
        "cash": bal["cash"],
        "accounts_receivable": bal["accounts_receivable"],
        "inventory": bal["inventory"],
        "equipment": bal["equipment"],
        "accumulated_depreciation": acc,
        "net_equipment": equip_net,
        "total_assets": assets,
        "accounts_payable": -bal["accounts_payable"],
        "long_term_debt": -bal["long_term_debt"],
        "total_liabilities": liab,
        "common_stock": stock,
        "retained_earnings": retained,
        "total_equity": equity,
        "total_liabilities_and_equity": liab + equity,
    }


def balance_sheet(ledger: list[dict[str, Any]], period_end: object) -> dict[str, int]:
    return _sheet(_through(ledger, _month_end(period_end)))


def _month_flow(ledger: list[dict[str, Any]], period_end: object) -> tuple[date, dict[str, int], dict[str, int]]:
    end = _month_end(period_end)
    now, before = _through(ledger, end), _through(ledger, _prior_end(end))
    return end, now, {name: now[name] - before[name] for name in ACCOUNTS}


def income_statement(ledger: list[dict[str, Any]], period_end: object) -> dict[str, int]:
    _, _, flow = _month_flow(ledger, period_end)
    sales = -flow["sales"]
    cogs = flow["cost_of_goods_sold"]
    opex = flow["operating_expenses"]
    dep = flow["depreciation_expense"]
    gross = sales - cogs
    return {
        "sales": sales,
        "cost_of_goods_sold": cogs,
        "gross_profit": gross,
        "operating_expenses": opex,
        "depreciation_expense": dep,
        "net_income": gross - opex - dep,
    }


def cash_flow_statement(ledger: list[dict[str, Any]], period_end: object) -> dict[str, int]:
    end, now, flow = _month_flow(ledger, period_end)
    ni = income_statement(ledger, period_end)["net_income"]
    dep = flow["depreciation_expense"]
    recv = -flow["accounts_receivable"]
    inv = -flow["inventory"]
    pay = -flow["accounts_payable"]
    cfo = ni + dep + recv + inv + pay
    capex = -flow["equipment"]
    debt = -flow["long_term_debt"]
    stock = -flow["common_stock"]
    div = -flow["dividends"]
    cff = debt + stock + div
    start_cash = _through(ledger, _prior_end(end))["cash"]
    return {
        "net_income": ni,
        "depreciation": dep,
        "receivables": recv,
        "inventory": inv,
        "payables": pay,
        "cash_from_operations": cfo,
        "capital_expenditure": capex,
        "cash_from_investing": capex,
        "net_borrowing": debt,
        "stock_issued": stock,
        "dividends_paid": div,
        "cash_from_financing": cff,
        "net_change_in_cash": cfo + capex + cff,
        "beginning_cash": start_cash,
        "ending_cash": start_cash + cfo + capex + cff,
    }


def articulation_check(ledger: list[dict[str, Any]], period_end: object) -> dict[str, int]:
    end = _month_end(period_end)
    sheet_now = _sheet(_through(ledger, end))
    sheet_before = _sheet(_through(ledger, _prior_end(end)))
    cash_flow = cash_flow_statement(ledger, period_end)
    inc = income_statement(ledger, period_end)
    return {
        "balance_gap": sheet_now["total_assets"] - sheet_now["total_liabilities_and_equity"],
        "cash_gap": sheet_now["cash"] - cash_flow["ending_cash"],
        "retained_earnings_gap": sheet_now["retained_earnings"] - sheet_before["retained_earnings"]
        - inc["net_income"] - cash_flow["dividends_paid"],
        "depreciation_gap": sheet_now["accumulated_depreciation"] - sheet_before["accumulated_depreciation"]
        - inc["depreciation_expense"],
    }
