# ruff: noqa (verifier scratch code: style is not gated; see the fragment)
"""Verifier implementation A of the A15 contract: plain loops, validation at every read (independent of the reference)."""

from __future__ import annotations

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


def _iso(value: Any, what: str) -> dt.date:
    if not isinstance(value, str):
        raise ValueError(f"{what} must be a string")
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{what} is not an ISO date") from exc


def _num(value: Any, what: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float, np.integer, np.floating)):
        raise ValueError(f"{what} is not a number")
    out = float(value)
    if not math.isfinite(out):
        raise ValueError(f"{what} is not finite")
    return out


def _quot(a: float, b: float, what: str) -> float:
    if b == 0:
        raise ValueError(f"zero denominator in {what}")
    return a / b


def _check_statements(statements: Any) -> None:
    if not isinstance(statements, Mapping):
        raise ValueError("statements must be a mapping")


def _val(statements: Any, end: str, item: str) -> float:
    _check_statements(statements)
    row = statements.get(end)
    if row is None:
        raise ValueError(f"no statements for {end}")
    if item not in row:
        raise ValueError(f"{item} missing at {end}")
    return _num(row[item], item)


def _prev_end(statements: Any, end: str) -> str:
    _check_statements(statements)
    t = dt.date.fromisoformat(end)
    found: list[dt.date] = []
    for key in statements:
        d = _iso(key, "period end")
        gap = (t - d).days
        if 350 <= gap <= 380:
            found.append(d)
    if not found:
        raise ValueError(f"no previous year for {end}")
    return max(found).isoformat()


def _avg(a: float, b: float) -> float:
    return 0.5 * (a + b)


def _is_annual(item: str, obs: Mapping[str, Any]) -> bool:
    if not str(obs["form"]).startswith("10-K") or obs.get("fp") != "FY":
        return False
    if "start" in obs:
        if item not in ("revenue", "cogs", "sga", "depreciation", "operating_income", "net_income", "cfo"):
            return False
        span = (_iso(obs["end"], "end").__sub__(_iso(obs["start"], "start"))).days
        return 350 <= span <= 380
    return item not in ("revenue", "cogs", "sga", "depreciation", "operating_income", "net_income", "cfo")


def standardize(facts: Any, as_of: str | None = None) -> dict[str, dict[str, float]]:
    cut = None if as_of is None else _iso(as_of, "as_of")
    if not isinstance(facts, Mapping) or "facts" not in facts:
        raise ValueError("no facts")
    gaap = facts["facts"].get("us-gaap", {})
    # validate every observation of every tag first
    for tag, entry in gaap.items():
        for unit_obs in entry.get("units", {}).values():
            for obs in unit_obs:
                for key in ("end", "val", "filed", "form"):
                    if key not in obs:
                        raise ValueError(f"{tag} observation lacks {key}")
                _iso(obs["end"], "end")
                _iso(obs["filed"], "filed")
                _num(obs["val"], "val")
                if "start" in obs:
                    _iso(obs["start"], "start")
    result: dict[str, dict[str, float]] = {}
    for item in ITEMS:
        unit = "shares" if item == "shares_outstanding" else "USD"
        chosen: dict[str, float] = {}
        for tag in TAG_PRIORITY[item]:
            obs_list = gaap.get(tag, {}).get("units", {}).get(unit, [])
            best: dict[str, tuple[tuple[str, str], float]] = {}
            tied: dict[str, list[tuple[tuple[str, str], float]]] = {}
            for obs in obs_list:
                if not _is_annual(item, obs):
                    continue
                if cut is not None and _iso(obs["filed"], "filed") > cut:
                    continue
                k = (str(obs["filed"]), str(obs.get("accn") or ""))
                end = str(obs["end"])
                tied.setdefault(end, []).append((k, _num(obs["val"], "val")))
                if end not in best or k > best[end][0]:
                    best[end] = (k, _num(obs["val"], "val"))
            for end, entries in tied.items():
                top_key = best[end][0]
                at_top = [v for kk, v in entries if kk == top_key]
                if len(set(at_top)) > 1:
                    raise ValueError("inconsistent facts: tie on (filed, accn) with different values")
            for end, (_, v) in best.items():
                if end not in chosen:
                    chosen[end] = v
        for end, v in chosen.items():
            result.setdefault(end, {})[item] = v
    return {end: result[end] for end in sorted(result)}


def dupont(statements: Any, period_end: str) -> dict[str, float]:
    end = _iso(period_end, "period_end").isoformat()
    prev = _prev_end(statements, end)
    rev = _val(statements, end, "revenue")
    ni = _val(statements, end, "net_income")
    avg_ta = _avg(_val(statements, end, "total_assets"), _val(statements, prev, "total_assets"))
    avg_eq = _avg(_val(statements, end, "equity"), _val(statements, prev, "equity"))
    nm = _quot(ni, rev, "net margin")
    at = _quot(rev, avg_ta, "asset turnover")
    lev = _quot(avg_ta, avg_eq, "leverage")
    roe = _quot(ni, avg_eq, "roe")
    roa = _quot(ni, avg_ta, "roa")
    return {"net_margin": nm, "asset_turnover": at, "leverage": lev, "roe": roe, "roa": roa}


def roic(statements: Any, period_end: str, tax_rate: float) -> float:
    end = _iso(period_end, "period_end").isoformat()
    tr = _num(tax_rate, "tax_rate")
    if not (0.0 <= tr < 1.0):
        raise ValueError("tax rate out of range")
    prev = _prev_end(statements, end)

    def ic(e: str) -> float:
        return _val(statements, e, "equity") + _val(statements, e, "long_term_debt") - _val(statements, e, "cash")

    nopat = _val(statements, end, "operating_income") * (1.0 - tr)
    avg_ic = _avg(ic(end), ic(prev))
    if avg_ic <= 0:
        raise ValueError("average invested capital must be positive")
    return _quot(nopat, avg_ic, "roic")


def current_ratio(statements: Any, period_end: str) -> float:
    end = _iso(period_end, "period_end").isoformat()
    return _quot(_val(statements, end, "current_assets"), _val(statements, end, "current_liabilities"), "CR")


def gross_margin(statements: Any, period_end: str) -> float:
    end = _iso(period_end, "period_end").isoformat()
    rev = _val(statements, end, "revenue")
    return _quot(rev - _val(statements, end, "cogs"), rev, "gross margin")


def debt_to_assets(statements: Any, period_end: str) -> float:
    end = _iso(period_end, "period_end").isoformat()
    return _quot(_val(statements, end, "long_term_debt"), _val(statements, end, "total_assets"), "D/A")


def days_sales_outstanding(statements: Any, period_end: str) -> float:
    end = _iso(period_end, "period_end").isoformat()
    rev = _val(statements, end, "revenue")
    return _quot(_val(statements, end, "receivables"), rev, "DSO") * 365.0


def accruals_cash_flow(statements: Any, period_end: str) -> float:
    end = _iso(period_end, "period_end").isoformat()
    prev = _prev_end(statements, end)
    avg_ta = _avg(_val(statements, end, "total_assets"), _val(statements, prev, "total_assets"))
    return _quot(_val(statements, end, "net_income") - _val(statements, end, "cfo"), avg_ta, "accruals")


def accruals_balance_sheet(statements: Any, period_end: str) -> float:
    end = _iso(period_end, "period_end").isoformat()
    prev = _prev_end(statements, end)
    dca = _val(statements, end, "current_assets") - _val(statements, prev, "current_assets")
    dcash = _val(statements, end, "cash") - _val(statements, prev, "cash")
    dcl = _val(statements, end, "current_liabilities") - _val(statements, prev, "current_liabilities")
    dep = _val(statements, end, "depreciation")
    avg_ta = _avg(_val(statements, end, "total_assets"), _val(statements, prev, "total_assets"))
    return _quot((dca - dcash) - dcl - dep, avg_ta, "balance-sheet accruals")


def modified_jones(sample: Any) -> dict[str, Any]:
    if isinstance(sample, (str, bytes)) or not isinstance(sample, Sequence):
        raise ValueError("sample must be a sequence")
    if len(sample) < 4:
        raise ValueError("at least four firm-years are needed")
    keys = ("total_accruals", "lag_assets", "d_revenue", "d_receivables", "ppe")
    cols: list[list[float]] = [[], [], [], [], []]
    for row in sample:
        vals = [_num(row[k], k) for k in keys]
        if vals[1] <= 0:
            raise ValueError("lag_assets must be positive")
        for i, v in enumerate(vals):
            cols[i].append(v)
    lag = np.asarray(cols[1], dtype=np.float64)
    y = np.asarray(cols[0], dtype=np.float64) / lag
    x = np.column_stack(
        [
            1.0 / lag,
            (np.asarray(cols[2]) - np.asarray(cols[3])) / lag,
            np.asarray(cols[4], dtype=np.float64) / lag,
        ]
    )
    if not (np.all(np.isfinite(x)) and np.all(np.isfinite(y))):
        raise ValueError("non-finite regression input")
    scale = np.linalg.norm(x, axis=0)
    if np.any(scale == 0):
        raise ValueError("rank-deficient design")
    sv = np.linalg.svd(x / scale, compute_uv=False)
    if sv.min() <= 1e-10 * sv.max():
        raise ValueError("rank-deficient design")
    beta = np.linalg.lstsq(x, y, rcond=None)[0]
    fit = x @ beta
    return {
        "coefficients": tuple(float(b) for b in beta),
        "nondiscretionary": [float(f) for f in fit],
        "discretionary": [float(r) for r in (y - fit)],
    }


def piotroski_f_score(statements: Any, period_end: str) -> dict[str, Any]:
    t = _iso(period_end, "period_end").isoformat()
    t1 = _prev_end(statements, t)
    t2 = _prev_end(statements, t1)
    ta = {e: _val(statements, e, "total_assets") for e in (t, t1, t2)}
    roa_t = _quot(_val(statements, t, "net_income"), ta[t1], "ROA")
    roa_p = _quot(_val(statements, t1, "net_income"), ta[t2], "ROA prev")
    cfo_t = _quot(_val(statements, t, "cfo"), ta[t1], "CFO")
    lev_t = _quot(_val(statements, t, "long_term_debt"), _avg(ta[t], ta[t1]), "LEV")
    lev_p = _quot(_val(statements, t1, "long_term_debt"), _avg(ta[t1], ta[t2]), "LEV prev")
    cr_t = _quot(_val(statements, t, "current_assets"), _val(statements, t, "current_liabilities"), "CR")
    cr_p = _quot(_val(statements, t1, "current_assets"), _val(statements, t1, "current_liabilities"), "CR prev")
    gm_t = _quot(_val(statements, t, "revenue") - _val(statements, t, "cogs"), _val(statements, t, "revenue"), "GM")
    gm_p = _quot(
        _val(statements, t1, "revenue") - _val(statements, t1, "cogs"), _val(statements, t1, "revenue"), "GM prev"
    )
    ato_t = _quot(_val(statements, t, "revenue"), ta[t1], "ATO")
    ato_p = _quot(_val(statements, t1, "revenue"), ta[t2], "ATO prev")
    sh_t = _val(statements, t, "shares_outstanding")
    sh_p = _val(statements, t1, "shares_outstanding")
    sig = (
        int(roa_t > 0),
        int(cfo_t > 0),
        int(roa_t > roa_p),
        int(cfo_t > roa_t),
        int(lev_t < lev_p),
        int(cr_t > cr_p),
        int(sh_t <= sh_p),
        int(gm_t > gm_p),
        int(ato_t > ato_p),
    )
    return {"signals": sig, "score": int(sum(sig))}


def beneish_m_score(statements: Any, period_end: str) -> dict[str, float]:
    t = _iso(period_end, "period_end").isoformat()
    p = _prev_end(statements, t)

    def v(e: str, k: str) -> float:
        return _val(statements, e, k)

    def gm(e: str) -> float:
        return _quot(v(e, "revenue") - v(e, "cogs"), v(e, "revenue"), "GM")

    def aq(e: str) -> float:
        return 1.0 - _quot(v(e, "current_assets") + v(e, "ppe"), v(e, "total_assets"), "AQ")

    def dep_share(e: str) -> float:
        return _quot(v(e, "depreciation"), v(e, "depreciation") + v(e, "ppe"), "DEP")

    def lev(e: str) -> float:
        return _quot(v(e, "current_liabilities") + v(e, "long_term_debt"), v(e, "total_assets"), "LEV")

    out: dict[str, float] = {
        "DSRI": _quot(
            _quot(v(t, "receivables"), v(t, "revenue"), "DSR"),
            _quot(v(p, "receivables"), v(p, "revenue"), "DSR"),
            "DSRI",
        ),
        "GMI": _quot(gm(p), gm(t), "GMI"),
        "AQI": _quot(aq(t), aq(p), "AQI"),
        "SGI": _quot(v(t, "revenue"), v(p, "revenue"), "SGI"),
        "DEPI": _quot(dep_share(p), dep_share(t), "DEPI"),
        "SGAI": _quot(_quot(v(t, "sga"), v(t, "revenue"), "SGA"), _quot(v(p, "sga"), v(p, "revenue"), "SGA"), "SGAI"),
        "LVGI": _quot(lev(t), lev(p), "LVGI"),
        "TATA": _quot(v(t, "net_income") - v(t, "cfo"), v(t, "total_assets"), "TATA"),
    }
    m = BENEISH_INTERCEPT
    for name, value in out.items():
        m += BENEISH_COEFFICIENTS[name] * value
    out["m_score"] = float(m)
    return out
