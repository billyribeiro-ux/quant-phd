# ruff: noqa (verifier scratch code: style is not gated; see the fragment)
"""Verifier implementation C of the A15 contract: frozen record objects, generator pipelines, QR rank test."""

from __future__ import annotations

import datetime as dt
import math
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from typing import Any

import numpy as np

ITEMS: tuple[str, ...] = (
    "revenue",
    "cogs",
    "sga",
    "depreciation",
    "operating_income",
    "net_income",
    "cfo",
    "total_assets",
    "current_assets",
    "cash",
    "receivables",
    "ppe",
    "total_liabilities",
    "current_liabilities",
    "long_term_debt",
    "equity",
    "shares_outstanding",
)
TAG_PRIORITY: Mapping[str, tuple[str, ...]] = {
    "revenue": ("Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet"),
    "cogs": ("CostOfRevenue", "CostOfGoodsAndServicesSold"),
    "sga": ("SellingGeneralAndAdministrativeExpense",),
    "depreciation": ("DepreciationDepletionAndAmortization", "DepreciationAndAmortization", "Depreciation"),
    "operating_income": ("OperatingIncomeLoss",),
    "net_income": ("NetIncomeLoss",),
    "cfo": ("NetCashProvidedByUsedInOperatingActivities",),
    "total_assets": ("Assets",),
    "current_assets": ("AssetsCurrent",),
    "cash": ("CashAndCashEquivalentsAtCarryingValue",),
    "receivables": ("AccountsReceivableNetCurrent",),
    "ppe": ("PropertyPlantAndEquipmentNet",),
    "total_liabilities": ("Liabilities",),
    "current_liabilities": ("LiabilitiesCurrent",),
    "long_term_debt": ("LongTermDebtNoncurrent",),
    "equity": ("StockholdersEquity",),
    "shares_outstanding": ("CommonStockSharesOutstanding",),
}
BENEISH_INTERCEPT: float = -4.84
BENEISH_COEFFICIENTS: Mapping[str, float] = {
    "DSRI": 0.920,
    "GMI": 0.528,
    "AQI": 0.404,
    "SGI": 0.892,
    "DEPI": 0.115,
    "SGAI": -0.172,
    "LVGI": -0.327,
    "TATA": 4.679,
}
__all__ = [
    "BENEISH_COEFFICIENTS",
    "BENEISH_INTERCEPT",
    "ITEMS",
    "TAG_PRIORITY",
    "accruals_balance_sheet",
    "accruals_cash_flow",
    "beneish_m_score",
    "current_ratio",
    "days_sales_outstanding",
    "debt_to_assets",
    "dupont",
    "gross_margin",
    "modified_jones",
    "piotroski_f_score",
    "roic",
    "standardize",
]

_FLOW = frozenset({"revenue", "cogs", "sga", "depreciation", "operating_income", "net_income", "cfo"})


@dataclass(frozen=True)
class _Obs:
    end: dt.date
    filed: dt.date
    accn: str
    value: float
    start: dt.date | None
    form: str
    fp: str


def _parse_date(value: Any, what: str) -> dt.date:
    if not isinstance(value, str):
        raise ValueError(f"{what} must be a string date")
    try:
        return dt.date.fromisoformat(value)
    except ValueError as err:
        raise ValueError(f"{what} is not an ISO date") from err


def _parse_value(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float, np.number)):
        raise ValueError("val must be a number")
    out = float(value)
    if not math.isfinite(out):
        raise ValueError("val must be finite")
    return out


def _to_obs(raw: Mapping[str, Any]) -> _Obs:
    for key in ("end", "val", "filed", "form"):
        if key not in raw:
            raise ValueError(f"observation lacks {key}")
    start = _parse_date(raw["start"], "start") if "start" in raw else None
    return _Obs(
        end=_parse_date(raw["end"], "end"),
        filed=_parse_date(raw["filed"], "filed"),
        accn=str(raw.get("accn") or ""),
        value=_parse_value(raw["val"]),
        start=start,
        form=str(raw["form"]),
        fp=str(raw.get("fp", "")),
    )


def _annual(item: str, o: _Obs) -> bool:
    if not o.form.startswith("10-K") or o.fp != "FY":
        return False
    if item in _FLOW:
        return o.start is not None and 350 <= (o.end - o.start).days <= 380
    return o.start is None


def _fraction(num: float, den: float, what: str) -> float:
    if den == 0:
        raise ValueError(f"{what} divides by zero")
    out = num / den
    if not math.isfinite(out):
        raise ValueError(f"{what} is not finite")
    return out


class _Statements:
    """Validated view of a statements mapping: items by period end, previous-year lookup."""

    __slots__ = ("_ends", "_rows")

    def __init__(self, statements: Any) -> None:
        if not isinstance(statements, Mapping):
            raise ValueError("statements must be a mapping")
        self._rows = {_parse_date(k, "period end").isoformat(): v for k, v in statements.items()}
        self._ends = sorted(self._rows)

    def value(self, end: str, item: str) -> float:
        if end not in self._rows:
            raise ValueError(f"period end {end} is not in the statements")
        row = self._rows[end]
        if item not in row:
            raise ValueError(f"{item} is missing at {end}")
        return _parse_value(row[item])

    def previous(self, end: str) -> str:
        t = dt.date.fromisoformat(end)
        candidates = [e for e in self._ends if 350 <= (t - dt.date.fromisoformat(e)).days <= 380]
        if not candidates:
            raise ValueError(f"no previous year before {end}")
        return candidates[-1]


def _end(period_end: Any) -> str:
    return _parse_date(period_end, "period_end").isoformat()


def standardize(facts: Any, as_of: str | None = None) -> dict[str, dict[str, float]]:
    cutoff = None if as_of is None else _parse_date(as_of, "as_of")
    if not isinstance(facts, Mapping) or "facts" not in facts:
        raise ValueError("company facts need a facts key")
    gaap: Mapping[str, Any] = facts["facts"].get("us-gaap", {})
    everything = [
        (tag, unit, _to_obs(raw))
        for tag, entry in gaap.items()
        for unit, rows in entry.get("units", {}).items()
        for raw in rows
    ]
    result: dict[str, dict[str, float]] = {}
    for item in ITEMS:
        unit = "shares" if item == "shares_outstanding" else "USD"
        done: dict[str, float] = {}
        for tag in TAG_PRIORITY[item]:
            pool = [o for t, u, o in everything if t == tag and u == unit and _annual(item, o)]
            if cutoff is not None:
                pool = [o for o in pool if o.filed <= cutoff]
            by_end: dict[dt.date, list[_Obs]] = {}
            for o in pool:
                by_end.setdefault(o.end, []).append(o)
            for end, group in by_end.items():
                group.sort(key=lambda o: (o.filed, o.accn), reverse=True)
                top = group[0]
                if len(group) > 1 and (group[1].filed, group[1].accn) == (top.filed, top.accn):
                    if group[1].value != top.value:
                        raise ValueError("facts disagree on a tie of (filed, accn)")
                key = end.isoformat()
                done.setdefault(key, top.value)
        for key, value in done.items():
            result.setdefault(key, {})[item] = value
    return {k: result[k] for k in sorted(result)}


def dupont(statements: Any, period_end: str) -> dict[str, float]:
    s = _Statements(statements)
    t = _end(period_end)
    p = s.previous(t)
    avg_a = (s.value(t, "total_assets") + s.value(p, "total_assets")) * 0.5
    avg_e = (s.value(t, "equity") + s.value(p, "equity")) * 0.5
    rev, ni = s.value(t, "revenue"), s.value(t, "net_income")
    return {
        "net_margin": _fraction(ni, rev, "net margin"),
        "asset_turnover": _fraction(rev, avg_a, "asset turnover"),
        "leverage": _fraction(avg_a, avg_e, "leverage"),
        "roe": _fraction(ni, avg_e, "roe"),
        "roa": _fraction(ni, avg_a, "roa"),
    }


def roic(statements: Any, period_end: str, tax_rate: float) -> float:
    s = _Statements(statements)
    t = _end(period_end)
    tr = _parse_value(tax_rate)
    if not 0.0 <= tr < 1.0:
        raise ValueError("tax_rate outside [0, 1)")
    p = s.previous(t)
    capital: Callable[[str], float] = lambda e: s.value(e, "equity") + s.value(e, "long_term_debt") - s.value(e, "cash")
    avg = 0.5 * (capital(t) + capital(p))
    if avg <= 0:
        raise ValueError("average invested capital is not positive")
    return _fraction(s.value(t, "operating_income") * (1.0 - tr), avg, "roic")


def current_ratio(statements: Any, period_end: str) -> float:
    s = _Statements(statements)
    t = _end(period_end)
    return _fraction(s.value(t, "current_assets"), s.value(t, "current_liabilities"), "current ratio")


def gross_margin(statements: Any, period_end: str) -> float:
    s = _Statements(statements)
    t = _end(period_end)
    rev = s.value(t, "revenue")
    return _fraction(rev - s.value(t, "cogs"), rev, "gross margin")


def debt_to_assets(statements: Any, period_end: str) -> float:
    s = _Statements(statements)
    t = _end(period_end)
    return _fraction(s.value(t, "long_term_debt"), s.value(t, "total_assets"), "debt to assets")


def days_sales_outstanding(statements: Any, period_end: str) -> float:
    s = _Statements(statements)
    t = _end(period_end)
    return _fraction(s.value(t, "receivables"), s.value(t, "revenue"), "days sales outstanding") * 365.0


def accruals_cash_flow(statements: Any, period_end: str) -> float:
    s = _Statements(statements)
    t = _end(period_end)
    p = s.previous(t)
    avg = 0.5 * (s.value(t, "total_assets") + s.value(p, "total_assets"))
    return _fraction(s.value(t, "net_income") - s.value(t, "cfo"), avg, "cash-flow accruals")


def accruals_balance_sheet(statements: Any, period_end: str) -> float:
    s = _Statements(statements)
    t = _end(period_end)
    p = s.previous(t)
    change = {k: s.value(t, k) - s.value(p, k) for k in ("current_assets", "cash", "current_liabilities")}
    num = (change["current_assets"] - change["cash"]) - change["current_liabilities"] - s.value(t, "depreciation")
    avg = 0.5 * (s.value(t, "total_assets") + s.value(p, "total_assets"))
    return _fraction(num, avg, "balance-sheet accruals")


def modified_jones(sample: Any) -> dict[str, Any]:
    if isinstance(sample, (str, bytes)) or not isinstance(sample, Iterable):
        raise ValueError("sample must be a sequence")
    rows = list(sample)
    if len(rows) < 4:
        raise ValueError("the model needs at least four firm-years")
    cols = ("total_accruals", "lag_assets", "d_revenue", "d_receivables", "ppe")
    table = []
    for r in rows:
        if not isinstance(r, Mapping):
            raise ValueError("each firm-year must be a mapping")
        vals = [_parse_value(r[c]) for c in cols]
        if vals[1] <= 0:
            raise ValueError("lag_assets must be positive")
        table.append(vals)
    m = np.array(table, dtype=float)
    lag = m[:, 1]
    y = m[:, 0] / lag
    X = np.stack([1.0 / lag, (m[:, 2] - m[:, 3]) / lag, m[:, 4] / lag], axis=1)
    if not (np.isfinite(X).all() and np.isfinite(y).all()):
        raise ValueError("non-finite input")
    Q = X / np.where(np.linalg.norm(X, axis=0) == 0, 1.0, np.linalg.norm(X, axis=0))
    if np.any(np.linalg.norm(X, axis=0) == 0):
        raise ValueError("a regressor is identically zero")
    _, R = np.linalg.qr(Q)
    diag = np.abs(np.diag(R))
    if diag.min() <= 1e-10 * diag.max():
        raise ValueError("rank-deficient design")
    coef = np.linalg.lstsq(X, y, rcond=None)[0]
    fit = X @ coef
    return {
        "coefficients": tuple(float(c) for c in coef),
        "nondiscretionary": [float(v) for v in fit],
        "discretionary": [float(v) for v in y - fit],
    }


def piotroski_f_score(statements: Any, period_end: str) -> dict[str, Any]:
    s = _Statements(statements)
    t = _end(period_end)
    t1 = s.previous(t)
    t2 = s.previous(t1)
    a0, a1, a2 = (s.value(e, "total_assets") for e in (t, t1, t2))
    roa = _fraction(s.value(t, "net_income"), a1, "ROA")
    roa_prev = _fraction(s.value(t1, "net_income"), a2, "ROA")
    cfo = _fraction(s.value(t, "cfo"), a1, "CFO")
    lev = _fraction(s.value(t, "long_term_debt"), 0.5 * (a0 + a1), "leverage")
    lev_prev = _fraction(s.value(t1, "long_term_debt"), 0.5 * (a1 + a2), "leverage")
    cr = _fraction(s.value(t, "current_assets"), s.value(t, "current_liabilities"), "CR")
    cr_prev = _fraction(s.value(t1, "current_assets"), s.value(t1, "current_liabilities"), "CR")
    gm = _fraction(s.value(t, "revenue") - s.value(t, "cogs"), s.value(t, "revenue"), "GM")
    gm_prev = _fraction(s.value(t1, "revenue") - s.value(t1, "cogs"), s.value(t1, "revenue"), "GM")
    ato = _fraction(s.value(t, "revenue"), a1, "ATO")
    ato_prev = _fraction(s.value(t1, "revenue"), a2, "ATO")
    bits = [
        roa > 0,
        cfo > 0,
        roa > roa_prev,
        cfo > roa,
        lev < lev_prev,
        cr > cr_prev,
        s.value(t, "shares_outstanding") <= s.value(t1, "shares_outstanding"),
        gm > gm_prev,
        ato > ato_prev,
    ]
    signals = tuple(1 if b else 0 for b in bits)
    return {"signals": signals, "score": sum(signals)}


def beneish_m_score(statements: Any, period_end: str) -> dict[str, float]:
    s = _Statements(statements)
    t = _end(period_end)
    p = s.previous(t)
    v = s.value

    def idx(e: str, num: Callable[[str], float], den: Callable[[str], float], what: str) -> float:
        return _fraction(num(e), den(e), what)

    def gm(e: str) -> float:
        return idx(e, lambda x: v(x, "revenue") - v(x, "cogs"), lambda x: v(x, "revenue"), "GM")

    def aq(e: str) -> float:
        return 1.0 - idx(e, lambda x: v(x, "current_assets") + v(x, "ppe"), lambda x: v(x, "total_assets"), "AQ")

    def dep(e: str) -> float:
        return idx(e, lambda x: v(x, "depreciation"), lambda x: v(x, "depreciation") + v(x, "ppe"), "DEP")

    def lvg(e: str) -> float:
        return idx(
            e, lambda x: v(x, "current_liabilities") + v(x, "long_term_debt"), lambda x: v(x, "total_assets"), "LVG"
        )

    def sales_share(e: str, item: str) -> float:
        return idx(e, lambda x: v(x, item), lambda x: v(x, "revenue"), item)

    variables = {
        "DSRI": _fraction(sales_share(t, "receivables"), sales_share(p, "receivables"), "DSRI"),
        "GMI": _fraction(gm(p), gm(t), "GMI"),
        "AQI": _fraction(aq(t), aq(p), "AQI"),
        "SGI": _fraction(v(t, "revenue"), v(p, "revenue"), "SGI"),
        "DEPI": _fraction(dep(p), dep(t), "DEPI"),
        "SGAI": _fraction(sales_share(t, "sga"), sales_share(p, "sga"), "SGAI"),
        "LVGI": _fraction(lvg(t), lvg(p), "LVGI"),
        "TATA": _fraction(v(t, "net_income") - v(t, "cfo"), v(t, "total_assets"), "TATA"),
    }
    total = BENEISH_INTERCEPT
    for name in variables:
        total += BENEISH_COEFFICIENTS[name] * variables[name]
    return {**variables, "m_score": total}
