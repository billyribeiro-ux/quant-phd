# ruff: noqa (verifier scratch code: style is not gated; see the fragment)
"""Verifier implementation B of the A15 contract: table-driven, global sort for selection, bisect for previous years."""

from __future__ import annotations

import bisect
import datetime as dt
import math
from collections.abc import Mapping, Sequence
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

FLOW = frozenset({"revenue", "cogs", "sga", "depreciation", "operating_income", "net_income", "cfo"})
_TABLE: dict[str, tuple[str, ...]] = {"ok": ()}


def _date(value: Any, what: str) -> dt.date:
    if not isinstance(value, str):
        raise ValueError(f"{what}: expected an ISO date string")
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{what}: not an ISO date") from exc


def _finite(value: Any, what: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float, np.integer, np.floating)):
        raise ValueError(f"{what}: not a number")
    x = float(value)
    if not math.isfinite(x):
        raise ValueError(f"{what}: not finite")
    return x


def _ratio(num: float, den: float, what: str) -> float:
    if den == 0:
        raise ValueError(f"{what}: zero denominator")
    r = num / den
    if not math.isfinite(r):
        raise ValueError(f"{what}: result not finite")
    return r


class _Panel:
    """Read-only accessor over a statements mapping, with previous-year lookup by bisect."""

    def __init__(self, statements: Any) -> None:
        if not isinstance(statements, Mapping):
            raise ValueError("statements must be a mapping")
        self.data = statements
        self.dates = sorted(_date(k, "period end") for k in statements)

    def item(self, end: str, name: str) -> float:
        row = self.data.get(end)
        if row is None:
            raise ValueError(f"no period end {end}")
        if name not in row:
            raise ValueError(f"item {name} missing at {end}")
        return _finite(row[name], f"{name}@{end}")

    def prev(self, end: str) -> str:
        d = _date(end, "period end")
        lo = bisect.bisect_left(self.dates, d - dt.timedelta(days=380))
        hi = bisect.bisect_right(self.dates, d - dt.timedelta(days=350))
        if lo >= hi:
            raise ValueError(f"no previous year for {end}")
        return self.dates[hi - 1].isoformat()


def _iso(value: Any, what: str) -> str:
    return _date(value, what).isoformat()


def standardize(facts: Any, as_of: str | None = None) -> dict[str, dict[str, float]]:
    cutoff = None if as_of is None else _date(as_of, "as_of")
    if not isinstance(facts, Mapping) or "facts" not in facts:
        raise ValueError("company facts need a 'facts' key")
    gaap = facts["facts"].get("us-gaap", {})
    flat: list[tuple[str, str, dict[str, Any]]] = []
    for tag, entry in gaap.items():
        for unit, rows in entry.get("units", {}).items():
            for obs in rows:
                flat.append((tag, unit, obs))
    # every observation is validated, whatever its tag
    parsed: list[tuple[str, str, dict[str, Any], dt.date, dt.date, dt.date | None, float]] = []
    for tag, unit, obs in flat:
        for key in ("end", "val", "filed", "form"):
            if key not in obs:
                raise ValueError(f"observation of {tag} lacks {key}")
        end = _date(obs["end"], "end")
        filed = _date(obs["filed"], "filed")
        start = _date(obs["start"], "start") if "start" in obs else None
        parsed.append((tag, unit, obs, end, filed, start, _finite(obs["val"], "val")))
    out: dict[str, dict[str, float]] = {}
    for item in ITEMS:
        unit = "shares" if item == "shares_outstanding" else "USD"
        picks: dict[str, tuple[str, str, float]] = {}  # end -> (filed, accn, value)
        rank: dict[str, int] = {tag: i for i, tag in enumerate(TAG_PRIORITY[item])}
        rows = [p for p in parsed if p[1] == unit and p[0] in rank]
        rows.sort(key=lambda p: (rank[p[0]], p[3].isoformat(), str(p[2]["filed"]), str(p[2].get("accn") or "")))
        for tag, _, obs, end, filed, start, value in rows:
            if str(obs["form"]).startswith("10-K") is False or obs.get("fp") != "FY":
                continue
            if start is not None:
                if item not in FLOW or not (350 <= (end - start).days <= 380):
                    continue
            elif item in FLOW:
                continue
            if cutoff is not None and filed > cutoff:
                continue
            end_s = end.isoformat()
            if end_s in picks:
                continue  # a higher-priority tag already supplies this period end
            key_tag = (filed.isoformat(), str(obs.get("accn") or ""))
            # best observation for this tag and end: scan the same tag's rows
            best = [
                q
                for q in rows
                if q[0] == tag
                and q[3] == end
                and q[4] <= (cutoff or dt.date.max)
                and str(q[2]["form"]).startswith("10-K")
                and q[2].get("fp") == "FY"
                and ((q[5] is not None) == (item in FLOW))
                and (q[5] is None or 350 <= (q[3] - q[5]).days <= 380)
            ]
            best.sort(key=lambda q: (q[4].isoformat(), str(q[2].get("accn") or "")), reverse=True)
            if (
                len(best) > 1
                and best[0][4] == best[1][4]
                and str(best[0][2].get("accn") or "") == str(best[1][2].get("accn") or "")
                and best[0][6] != best[1][6]
            ):
                raise ValueError("inconsistent facts for a tie on (filed, accn)")
            if best:
                picks[end_s] = (key_tag[0], key_tag[1], best[0][6])
        for end_s, (_, _, value) in picks.items():
            out.setdefault(end_s, {})[item] = value
    return {k: out[k] for k in sorted(out)}


def dupont(statements: Any, period_end: str) -> dict[str, float]:
    p = _Panel(statements)
    t = _iso(period_end, "period_end")
    q = p.prev(t)
    avg_a = (p.item(t, "total_assets") + p.item(q, "total_assets")) / 2
    avg_e = (p.item(t, "equity") + p.item(q, "equity")) / 2
    ni, rev = p.item(t, "net_income"), p.item(t, "revenue")
    return {
        "net_margin": _ratio(ni, rev, "net margin"),
        "asset_turnover": _ratio(rev, avg_a, "asset turnover"),
        "leverage": _ratio(avg_a, avg_e, "leverage"),
        "roe": _ratio(ni, avg_e, "roe"),
        "roa": _ratio(ni, avg_a, "roa"),
    }


def roic(statements: Any, period_end: str, tax_rate: float) -> float:
    p = _Panel(statements)
    t = _iso(period_end, "period_end")
    rate = _finite(tax_rate, "tax_rate")
    if rate < 0 or rate >= 1:
        raise ValueError("tax rate must lie in [0, 1)")
    q = p.prev(t)

    def cap(e: str) -> float:
        return p.item(e, "equity") + p.item(e, "long_term_debt") - p.item(e, "cash")

    avg = (cap(t) + cap(q)) / 2
    if not avg > 0:
        raise ValueError("average invested capital must be positive")
    return _ratio(p.item(t, "operating_income") * (1 - rate), avg, "roic")


def current_ratio(statements: Any, period_end: str) -> float:
    p = _Panel(statements)
    t = _iso(period_end, "period_end")
    return _ratio(p.item(t, "current_assets"), p.item(t, "current_liabilities"), "current ratio")


def gross_margin(statements: Any, period_end: str) -> float:
    p = _Panel(statements)
    t = _iso(period_end, "period_end")
    rev = p.item(t, "revenue")
    return _ratio(rev - p.item(t, "cogs"), rev, "gross margin")


def debt_to_assets(statements: Any, period_end: str) -> float:
    p = _Panel(statements)
    t = _iso(period_end, "period_end")
    return _ratio(p.item(t, "long_term_debt"), p.item(t, "total_assets"), "debt to assets")


def days_sales_outstanding(statements: Any, period_end: str) -> float:
    p = _Panel(statements)
    t = _iso(period_end, "period_end")
    return _ratio(p.item(t, "receivables"), p.item(t, "revenue"), "DSO") * 365


def accruals_cash_flow(statements: Any, period_end: str) -> float:
    p = _Panel(statements)
    t = _iso(period_end, "period_end")
    q = p.prev(t)
    avg = (p.item(t, "total_assets") + p.item(q, "total_assets")) / 2
    return _ratio(p.item(t, "net_income") - p.item(t, "cfo"), avg, "cash-flow accruals")


def accruals_balance_sheet(statements: Any, period_end: str) -> float:
    p = _Panel(statements)
    t = _iso(period_end, "period_end")
    q = p.prev(t)
    d = {k: p.item(t, k) - p.item(q, k) for k in ("current_assets", "cash", "current_liabilities")}
    num = (d["current_assets"] - d["cash"]) - d["current_liabilities"] - p.item(t, "depreciation")
    avg = (p.item(t, "total_assets") + p.item(q, "total_assets")) / 2
    return _ratio(num, avg, "balance-sheet accruals")


def modified_jones(sample: Any) -> dict[str, Any]:
    if not isinstance(sample, Sequence) or isinstance(sample, (str, bytes)):
        raise ValueError("sample must be a sequence of firm-years")
    if len(sample) < 4:
        raise ValueError("fewer than four firm-years")
    names = ("total_accruals", "lag_assets", "d_revenue", "d_receivables", "ppe")
    data = []
    for row in sample:
        vals = [_finite(row[n], n) for n in names]
        if vals[1] <= 0:
            raise ValueError("lag_assets must be positive")
        data.append(vals)
    arr = np.array(data, dtype=float)
    lag = arr[:, 1]
    y = arr[:, 0] / lag
    x = np.stack([1.0 / lag, (arr[:, 2] - arr[:, 3]) / lag, arr[:, 4] / lag], axis=1)
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError("non-finite regression input")
    norms = np.sqrt((x * x).sum(axis=0))
    if (norms == 0).any():
        raise ValueError("rank-deficient design")
    xs = x / norms
    _, r = np.linalg.qr(xs)
    if abs(np.diag(r)).min() <= 1e-9 * abs(np.diag(r)).max():
        raise ValueError("rank-deficient design")
    beta_scaled = np.linalg.lstsq(xs, y, rcond=None)[0]
    beta = beta_scaled / norms
    beta_check = np.linalg.lstsq(x, y, rcond=None)[0]
    beta = beta_check  # the contract's lstsq on the raw design; the scaled fit is only the rank test
    fit = x @ beta
    return {
        "coefficients": (float(beta[0]), float(beta[1]), float(beta[2])),
        "nondiscretionary": [float(v) for v in fit],
        "discretionary": [float(v) for v in y - fit],
    }


def piotroski_f_score(statements: Any, period_end: str) -> dict[str, Any]:
    p = _Panel(statements)
    t = _iso(period_end, "period_end")
    t1 = p.prev(t)
    t2 = p.prev(t1)
    ta = [p.item(e, "total_assets") for e in (t, t1, t2)]
    f = {
        "roa": _ratio(p.item(t, "net_income"), ta[1], "ROA"),
        "roa0": _ratio(p.item(t1, "net_income"), ta[2], "ROA0"),
        "cfo": _ratio(p.item(t, "cfo"), ta[1], "CFO"),
        "lev": _ratio(p.item(t, "long_term_debt"), (ta[0] + ta[1]) / 2, "LEV"),
        "lev0": _ratio(p.item(t1, "long_term_debt"), (ta[1] + ta[2]) / 2, "LEV0"),
        "cr": _ratio(p.item(t, "current_assets"), p.item(t, "current_liabilities"), "CR"),
        "cr0": _ratio(p.item(t1, "current_assets"), p.item(t1, "current_liabilities"), "CR0"),
        "gm": _ratio(p.item(t, "revenue") - p.item(t, "cogs"), p.item(t, "revenue"), "GM"),
        "gm0": _ratio(p.item(t1, "revenue") - p.item(t1, "cogs"), p.item(t1, "revenue"), "GM0"),
        "ato": _ratio(p.item(t, "revenue"), ta[1], "ATO"),
        "ato0": _ratio(p.item(t1, "revenue"), ta[2], "ATO0"),
    }
    s = [
        f["roa"] > 0,
        f["cfo"] > 0,
        f["roa"] > f["roa0"],
        f["cfo"] > f["roa"],
        f["lev"] < f["lev0"],
        f["cr"] > f["cr0"],
        p.item(t, "shares_outstanding") <= p.item(t1, "shares_outstanding"),
        f["gm"] > f["gm0"],
        f["ato"] > f["ato0"],
    ]
    signals = tuple(int(bool(v)) for v in s)
    return {"signals": signals, "score": sum(signals)}


def beneish_m_score(statements: Any, period_end: str) -> dict[str, float]:
    p = _Panel(statements)
    t = _iso(period_end, "period_end")
    q = p.prev(t)
    rev_t, rev_q = p.item(t, "revenue"), p.item(q, "revenue")
    gm_t = _ratio(rev_t - p.item(t, "cogs"), rev_t, "GM")
    gm_q = _ratio(rev_q - p.item(q, "cogs"), rev_q, "GM")
    ta_t, ta_q = p.item(t, "total_assets"), p.item(q, "total_assets")
    pe_t, pe_q = p.item(t, "ppe"), p.item(q, "ppe")
    dp_t, dp_q = p.item(t, "depreciation"), p.item(q, "depreciation")
    vars_ = {
        "DSRI": _ratio(
            _ratio(p.item(t, "receivables"), rev_t, "DSR"), _ratio(p.item(q, "receivables"), rev_q, "DSR"), "DSRI"
        ),
        "GMI": _ratio(gm_q, gm_t, "GMI"),
        "AQI": _ratio(
            1 - _ratio(p.item(t, "current_assets") + pe_t, ta_t, "AQ"),
            1 - _ratio(p.item(q, "current_assets") + pe_q, ta_q, "AQ"),
            "AQI",
        ),
        "SGI": _ratio(rev_t, rev_q, "SGI"),
        "DEPI": _ratio(_ratio(dp_q, dp_q + pe_q, "DEP"), _ratio(dp_t, dp_t + pe_t, "DEP"), "DEPI"),
        "SGAI": _ratio(_ratio(p.item(t, "sga"), rev_t, "SGA"), _ratio(p.item(q, "sga"), rev_q, "SGA"), "SGAI"),
        "LVGI": _ratio(
            _ratio(p.item(t, "current_liabilities") + p.item(t, "long_term_debt"), ta_t, "LV"),
            _ratio(p.item(q, "current_liabilities") + p.item(q, "long_term_debt"), ta_q, "LV"),
            "LVGI",
        ),
        "TATA": _ratio(p.item(t, "net_income") - p.item(t, "cfo"), ta_t, "TATA"),
    }
    m = BENEISH_INTERCEPT + sum(BENEISH_COEFFICIENTS[k] * v for k, v in vars_.items())
    return {**vars_, "m_score": float(m)}
