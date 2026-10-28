"""Round-14 alternative B: day ordinals, month end by next-day check, prefix sums over sorted postings."""
from __future__ import annotations

from bisect import bisect_right
from datetime import date
from typing import Any

ACCOUNTS = {"cash": "asset", "accounts_receivable": "asset", "inventory": "asset", "equipment": "asset",
            "accumulated_depreciation": "contra_asset", "accounts_payable": "liability",
            "long_term_debt": "liability", "common_stock": "equity", "dividends": "distribution", "sales": "revenue",
            "cost_of_goods_sold": "expense", "operating_expenses": "expense", "depreciation_expense": "expense"}
CHART = set(ACCOUNTS)
ACCOUNT_NAMES = tuple(ACCOUNTS)
MSG = "a date must be an ISO date, YYYY-MM-DD"


def _ord(value: object) -> int:
    if not isinstance(value, str) or len(value) != 10 or value[4] != "-" or value[7] != "-":
        raise ValueError(MSG)
    try:
        d = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(MSG) from exc
    if d.isoformat() != value:
        raise ValueError(MSG)
    return d.toordinal()


def _amount(value: object) -> int:
    if isinstance(value, bool) or type(value).__name__ != "int":
        raise ValueError("an amount must be an integer number of cents")
    if value < 0:
        raise ValueError("an amount must not be negative")
    return value


class _Ledger:
    def __init__(self, postings: list[tuple[int, str, int]]) -> None:
        self.days = [p[0] for p in postings]
        self.sums: dict[str, tuple[list[int], list[int]]] = {a: ([], []) for a in ACCOUNT_NAMES}
        for account in ACCOUNT_NAMES:
            days, cum = self.sums[account][0], self.sums[account][1]
            total = 0
            for day, acct, s in sorted(p for p in postings if p[1] == account):
                total += s
                days.append(day)
                cum.append(total)

    def upto(self, day: int) -> dict[str, int]:
        out: dict[str, int] = {}
        for account in ACCOUNT_NAMES:
            days, cum = self.sums[account]
            i = bisect_right(days, day)
            out[account] = cum[i - 1] if i else 0
        return out


def _month_end_ord(value: object) -> int:
    o = _ord(value)
    d = date.fromordinal(o)
    if (d.toordinal() + 1) == date(d.year + (d.month == 12), d.month % 12 + 1, 1).toordinal():
        return o
    raise ValueError("a period end must be the last day of a calendar month")


def post(transactions: Any) -> _Ledger:
    out: list[tuple[int, str, int]] = []
    for entry in transactions:
        if not isinstance(entry, dict) or "date" not in entry or "lines" not in entry:
            raise ValueError("a transaction needs a date and its lines")
        o = _ord(entry["date"])
        lines = entry["lines"]
        if isinstance(lines, (str, bytes)) or not isinstance(lines, (list, tuple)) or not lines:
            raise ValueError("a transaction needs at least one line")
        total = 0
        for line in lines:
            if not isinstance(line, dict) or not {"account", "debit", "credit"} <= set(line):
                raise ValueError("a line needs an account, a debit and a credit")
            if not isinstance(line["account"], str) or line["account"] not in CHART:
                raise ValueError("an unknown account is not in the chart of accounts")
            dr = _amount(line["debit"])
            cr = _amount(line["credit"])
            if bool(dr) == bool(cr):
                raise ValueError("a line carries a debit or a credit, and exactly one")
            out.append((o, line["account"], dr - cr))
            total += dr - cr
        if total:
            raise ValueError("unbalanced entry: the debits must equal the credits")
    return _Ledger(out)


def _at(ledger: _Ledger, o: int) -> dict[str, int]:
    return ledger.upto(o)


def balance_sheet(ledger: _Ledger, period_end: str) -> dict[str, int]:
    o = _month_end_ord(period_end)
    b = _at(ledger, o)
    acc = -b["accumulated_depreciation"]
    net_eq = b["equipment"] - acc
    ta = b["cash"] + b["accounts_receivable"] + b["inventory"] + net_eq
    pay, debt = -b["accounts_payable"], -b["long_term_debt"]
    com = -b["common_stock"]
    rev = -(b["sales"] + b["cost_of_goods_sold"] + b["operating_expenses"] + b["depreciation_expense"])
    re_ = rev - b["dividends"]
    tl, te = pay + debt, com + re_
    return {"cash": b["cash"], "accounts_receivable": b["accounts_receivable"], "inventory": b["inventory"],
            "equipment": b["equipment"], "accumulated_depreciation": acc, "net_equipment": net_eq,
            "total_assets": ta, "accounts_payable": pay, "long_term_debt": debt, "total_liabilities": tl,
            "common_stock": com, "retained_earnings": re_, "total_equity": te,
            "total_liabilities_and_equity": tl + te}


def _delta(ledger: _Ledger, o: int) -> tuple[dict[str, int], dict[str, int], dict[str, int]]:
    prev_end = date.fromordinal(o).replace(day=1).toordinal() - 1
    now, before = _at(ledger, o), _at(ledger, prev_end)
    return now, before, {a: now[a] - before[a] for a in ACCOUNT_NAMES}


def income_statement(ledger: _Ledger, period_end: str) -> dict[str, int]:
    _, _, d = _delta(ledger, _month_end_ord(period_end))
    sales, cogs = -d["sales"], d["cost_of_goods_sold"]
    gp = sales - cogs
    opx, dep = d["operating_expenses"], d["depreciation_expense"]
    return {"sales": sales, "cost_of_goods_sold": cogs, "gross_profit": gp, "operating_expenses": opx,
            "depreciation_expense": dep, "net_income": gp - opx - dep}


def cash_flow_statement(ledger: _Ledger, period_end: str) -> dict[str, int]:
    o = _month_end_ord(period_end)
    now, before, d = _delta(ledger, o)
    ni = income_statement(ledger, period_end)["net_income"]
    dep = d["depreciation_expense"]
    rec = -d["accounts_receivable"]
    inv = -d["inventory"]
    pay = -d["accounts_payable"]
    ops = ni + dep + rec + inv + pay
    capex = -d["equipment"]
    fin = -d["long_term_debt"] - d["common_stock"] - d["dividends"]
    beg = before["cash"]
    return {"net_income": ni, "depreciation": dep, "receivables": rec, "inventory": inv, "payables": pay,
            "cash_from_operations": ops, "capital_expenditure": capex, "cash_from_investing": capex,
            "net_borrowing": -d["long_term_debt"], "stock_issued": -d["common_stock"],
            "dividends_paid": -d["dividends"], "cash_from_financing": fin,
            "net_change_in_cash": ops + capex + fin, "beginning_cash": beg, "ending_cash": beg + ops + capex + fin}


def articulation_check(ledger: _Ledger, period_end: str) -> dict[str, int]:
    o = _month_end_ord(period_end)
    prev = date.fromordinal(o).replace(day=1).toordinal() - 1
    now, before = balance_sheet(ledger, period_end), balance_sheet(ledger, date.fromordinal(prev).isoformat())
    cf = cash_flow_statement(ledger, period_end)
    inc = income_statement(ledger, period_end)
    return {
        "balance_gap": now["total_assets"] - now["total_liabilities_and_equity"],
        "cash_gap": now["cash"] - cf["ending_cash"],
        "retained_earnings_gap": (now["retained_earnings"] - before["retained_earnings"])
        - (inc["net_income"] + cf["dividends_paid"]),
        "depreciation_gap": (now["accumulated_depreciation"] - before["accumulated_depreciation"])
        - inc["depreciation_expense"],
    }
