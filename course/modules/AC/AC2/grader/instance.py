"""Seeded SIMULATED company-facts filers for the Atlas A15 autograder (the fundamentals engine).

``make_instance(seed)`` is deterministic. It returns a SIMULATED filer in the SEC company-facts shape
(``facts["facts"]["us-gaap"][tag]["units"][unit]`` is a list of observations), with a generated history:

* 5 to 7 fiscal years, one 10-K per year that repeats its two prior years as comparatives;
* a 10-K/A that restates one item of one year, filed later, or on the same day with a larger accession number;
* 10-Q quarterly facts and a six-month transition fact, which are not annual and must be ignored;
* a tag switch for each multi-tag item (an older tag gives way to a newer one in a later year), a lower-priority
  tag that reports a different value, and missing items in some years;
* as-of cut-offs whose expected standardized statements are computed here, from the generator's own record of
  every filing, independently of the engine.

Nothing here is a real company's figures. The filer is labelled SIMULATED.

This file is the one place the grader and the reference solution import the published tables from: ``ITEMS``,
``TAG_PRIORITY`` (the A15 contract's table) and the Beneish (1999) constants. The Beneish constants are
UNCONFIRMED: see ``BENEISH_STATUS``.
"""

from __future__ import annotations

import datetime as dt
import json
from collections.abc import Mapping
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

FLOW_ITEMS: frozenset[str] = frozenset(
    {"revenue", "cogs", "sga", "depreciation", "operating_income", "net_income", "cfo"}
)

BENEISH_STATUS = (
    "UNCONFIRMED. ONE secondary source, the Wikipedia page 'Beneish M-score' (read 2026-10-27), reproduces these "
    "values; nothing else could be read. The values have not been checked against Beneish (1999), registry key "
    "beneish1999detection, and no table or page locator into the paper is confirmed. Grade C at most."
)
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

_MONTH_DAYS: tuple[tuple[int, int], ...] = ((12, 31), (6, 30), (9, 30), (3, 31))
_DISTORTION = 0.97  # the lower-priority tag reports this share of the true value
_Record = dict[str, list[tuple[dt.date, str, float]]]


def _unit(item: str) -> str:
    return "shares" if item == "shares_outstanding" else "USD"


def _one_economy(rng: np.random.Generator, n: int) -> dict[str, list[float]] | None:
    """True values by item and fiscal year. None if the draw gives an invalid balance sheet (the caller redraws)."""
    rev = [float(10 ** rng.uniform(7.5, 9.0))]
    for _ in range(1, n):
        rev.append(rev[-1] * float(1.0 + rng.normal(0.05, 0.08)))
    out: dict[str, list[float]] = {item: [] for item in ITEMS}
    ppe = rev[0] * float(rng.uniform(0.3, 0.7))
    for k in range(n):
        r = rev[k]
        cogs = r * float(rng.uniform(0.4, 0.8))
        sga = r * float(rng.uniform(0.10, 0.25))
        dep = ppe * float(rng.uniform(0.08, 0.14))
        ppe = ppe + r * float(rng.uniform(0.04, 0.09)) - dep
        op = r - cogs - sga - dep
        ni = 0.75 * op + float(rng.normal(0.0, 0.01)) * r
        cfo = ni + dep + float(rng.normal(0.0, 0.02)) * r
        rec = r * float(rng.uniform(0.08, 0.16))
        cash = r * float(rng.uniform(0.03, 0.12))
        ca = cash + rec + r * float(rng.uniform(0.05, 0.10))
        ta = ca + ppe + r * float(rng.uniform(0.05, 0.20))
        cl = r * float(rng.uniform(0.08, 0.18))
        ltd = r * float(rng.uniform(0.10, 0.40))
        ncl = r * float(rng.uniform(0.0, 0.05))
        eq = ta - (cl + ltd + ncl)
        if eq <= 0.25 * ta or cash >= eq + ltd:
            return None
        row = {
            "revenue": r,
            "cogs": cogs,
            "sga": sga,
            "depreciation": dep,
            "operating_income": op,
            "net_income": ni,
            "cfo": cfo,
            "total_assets": ta,
            "current_assets": ca,
            "cash": cash,
            "receivables": rec,
            "ppe": ppe,
            "total_liabilities": cl + ltd + ncl,
            "current_liabilities": cl,
            "long_term_debt": ltd,
            "equity": eq,
        }
        for item, value in row.items():
            out[item].append(round(value, 2))
    return out


def _economy(rng: np.random.Generator, n: int) -> dict[str, list[float]]:
    for _ in range(1000):
        out = _one_economy(rng, n)
        if out is not None:
            return out
    raise RuntimeError("the generator could not draw a valid balance sheet")  # unreachable in practice


def _pick(entries: list[tuple[dt.date, str, float]], cut: dt.date | None) -> float | None:
    """The value of the latest (filed, accn) entry filed on or before the cut-off (no cut-off: the latest)."""
    candidates = [e for e in entries if cut is None or e[0] <= cut]
    if not candidates:
        return None
    return max(candidates, key=lambda e: (e[0], e[1]))[2]


def _sample(seed: int) -> tuple[list[dict[str, float]], list[bool]]:
    """A cross-section of firm-years for modified_jones, with a planted discretionary accrual in some of them."""
    rng = np.random.default_rng([23, 16, int(seed)])
    n = int(rng.integers(40, 81))
    lag = 10 ** rng.uniform(7.0, 9.5, n)
    d_rev = lag * rng.normal(0.05, 0.15, n)
    d_rec = lag * rng.normal(0.02, 0.05, n)
    ppe = lag * rng.uniform(0.2, 0.8, n)
    a1 = -0.04 * float(np.median(lag))
    a2 = float(rng.uniform(0.02, 0.05))
    a3 = float(rng.uniform(-0.06, -0.02))
    planted = rng.random(n) < 0.15
    planted[:4] = True
    jump = np.where(planted, rng.uniform(0.03, 0.06, n), 0.0)
    y = a1 / lag + a2 * (d_rev - d_rec) / lag + a3 * ppe / lag + rng.normal(0.0, 0.01, n) + jump
    rows = [
        {
            "total_accruals": float(y[i] * lag[i]),
            "lag_assets": float(lag[i]),
            "d_revenue": float(d_rev[i]),
            "d_receivables": float(d_rec[i]),
            "ppe": float(ppe[i]),
        }
        for i in range(n)
    ]
    return rows, [bool(p) for p in planted]


def make_instance(seed: int) -> dict[str, Any]:
    """A deterministic SIMULATED filer and cross-section for ``seed``. Every instance is valid."""
    rng = np.random.default_rng([23, 15, int(seed)])
    n = int(rng.integers(5, 8))  # fiscal years 0..n-1; the tests use n-1 (latest), n-2 and n-3
    month, day = _MONTH_DAYS[int(rng.integers(0, len(_MONTH_DAYS)))]
    first = int(rng.integers(2013, 2019))
    ends = [dt.date(first + k, month, day) for k in range(n)]
    values: dict[str, list[float]] = _economy(rng, n)
    base_shares = float(rng.uniform(1e7, 9e8))
    values["shares_outstanding"] = [round(base_shares * (1.0 + float(rng.normal(0.0, 0.03)))) for _ in range(n)]

    filed = [e + dt.timedelta(days=int(rng.integers(55, 80))) for e in ends]
    rs = int(rng.integers(n - 3, n - 1))  # the restated year: n-3 or n-2
    rs_item = ("revenue", "receivables", "total_assets")[int(rng.integers(0, 3))]
    same_day = bool(rng.random() < 0.5)
    amend = filed[rs] if same_day else filed[rs] + dt.timedelta(days=int(rng.integers(120, 200)))
    restated_factor = 1.0 + float(rng.uniform(0.02, 0.08)) * (1.0 if rng.random() < 0.5 else -1.0)

    reported: dict[str, list[int]] = {}
    distractor: dict[str, int | None] = {}
    missing: dict[str, int | None] = {}
    for item in ITEMS:
        tags = TAG_PRIORITY[item]
        if len(tags) == 1:
            reported[item] = [0] * n
            distractor[item] = None
            if item == "cfo":
                missing[item] = 0  # the earliest year has no cfo: nothing is imputed
            else:
                missing[item] = int(rng.integers(0, n - 3)) if rng.random() < 0.4 else None
        else:
            switch = int(rng.integers(0, n + 1))
            reported[item] = [0 if y < switch else 1 for y in range(n)]
            distractor[item] = len(tags) - 1
            missing[item] = int(rng.integers(0, n - 3)) if rng.random() < 0.3 else None

    units: dict[str, dict[str, list[dict[str, Any]]]] = {}
    records: dict[tuple[str, int], _Record] = {}
    cik = 320000 + 7 * int(seed)

    def accn(year: int, seq: int) -> str:
        return f"{cik:010d}-{ends[year].year % 100:02d}-{seq:06d}"

    def add(tag: str, unit: str, obs: dict[str, Any]) -> None:
        units.setdefault(tag, {}).setdefault(unit, []).append(obs)

    def record(item: str, year: int, kind: str, when: dt.date, acc: str, value: float) -> None:
        records.setdefault((item, year), {"prim": [], "dist": []})[kind].append((when, acc, value))

    def annual(item: str, year: int, when: dt.date, form: str, acc: str, value: float) -> dict[str, Any]:
        obs: dict[str, Any] = {
            "end": ends[year].isoformat(),
            "val": value,
            "filed": when.isoformat(),
            "form": form,
            "fp": "FY",
            "accn": acc,
        }
        if item in FLOW_ITEMS:
            obs["start"] = (ends[year] - dt.timedelta(days=364)).isoformat()
        return obs

    for k in range(n):  # the 10-K for fiscal year k repeats years k-2, k-1 and k
        for y in range(max(0, k - 2), k + 1):
            for item in ITEMS:
                unit = _unit(item)
                acc = accn(k, k + 1)
                true_value = values[item][y]
                if missing[item] != y:
                    primary = true_value * restated_factor if (item == rs_item and y == rs and k == rs) else true_value
                    tag = TAG_PRIORITY[item][reported[item][y]]
                    add(tag, unit, annual(item, y, filed[k], "10-K", acc, round(primary, 2)))
                    record(item, y, "prim", filed[k], acc, round(primary, 2))
                d = distractor[item]
                if d is not None and d != reported[item][y]:
                    tag = TAG_PRIORITY[item][d]
                    add(tag, unit, annual(item, y, filed[k], "10-K", acc, round(true_value * _DISTORTION, 2)))
                    record(item, y, "dist", filed[k], acc, round(true_value * _DISTORTION, 2))

    for item in ITEMS:  # the 10-K/A restates the year rs, with the true values
        if missing[item] == rs:
            continue
        acc = accn(rs, 50 + rs)
        tag = TAG_PRIORITY[item][reported[item][rs]]
        add(tag, _unit(item), annual(item, rs, amend, "10-K/A", acc, round(values[item][rs], 2)))
        record(item, rs, "prim", amend, acc, round(values[item][rs], 2))

    for k in range(n):  # 10-Q quarters: not annual, ignored
        for q in (1, 2, 3):
            qend = ends[k] - dt.timedelta(days=91 * (4 - q))
            for item in ITEMS:
                tag = TAG_PRIORITY[item][reported[item][k]]
                if item in FLOW_ITEMS:
                    val = round(values[item][k] / 4.0, 2)
                    obs: dict[str, Any] = {"start": (qend - dt.timedelta(days=90)).isoformat()}
                else:
                    val = round(values[item][k] * 1.01, 2)
                    obs = {}
                obs.update(
                    {
                        "end": qend.isoformat(),
                        "val": val,
                        "filed": (qend + dt.timedelta(days=40)).isoformat(),
                        "form": "10-Q",
                        "fp": f"Q{q}",
                        "accn": accn(k, 20 + q),
                    }
                )
                add(tag, _unit(item), obs)

    # a six-month transition period reported under the annual form: its duration is not a fiscal year
    transition_end = ends[n - 1] - dt.timedelta(days=150)
    transition_tag = TAG_PRIORITY["revenue"][reported["revenue"][n - 1]]
    add(
        transition_tag,
        "USD",
        {
            "start": (transition_end - dt.timedelta(days=182)).isoformat(),
            "end": transition_end.isoformat(),
            "val": round(values["revenue"][n - 1] / 2.0, 2),
            "filed": filed[n - 1].isoformat(),
            "form": "10-K",
            "fp": "FY",
            "accn": accn(n - 1, 9),
        },
    )

    us_gaap: dict[str, Any] = {tag: {"label": tag, "units": unit_map} for tag, unit_map in units.items()}
    facts: dict[str, Any] = {
        "cik": cik,
        "entityName": f"SIMULATED FILER {int(seed):04d}",
        "label": "SIMULATED",
        "facts": {
            "dei": {
                "EntityCommonStockSharesOutstanding": {
                    "units": {
                        "shares": [
                            {
                                "end": filed[n - 1].isoformat(),
                                "val": values["shares_outstanding"][n - 1],
                                "filed": filed[n - 1].isoformat(),
                                "form": "10-K",
                            }
                        ]
                    }
                }
            },
            "us-gaap": us_gaap,
        },
    }

    def truth_at(cut: dt.date | None) -> dict[str, dict[str, float]]:
        out: dict[str, dict[str, float]] = {}
        for y in range(n):
            row: dict[str, float] = {}
            for item in ITEMS:
                entry = records.get((item, y))
                if entry is None:
                    continue
                value = _pick(entry["prim"], cut)
                if value is None:
                    value = _pick(entry["dist"], cut)
                if value is not None:
                    row[item] = value
            if row:
                out[ends[y].isoformat()] = row
        return out

    cutoffs: dict[str, str | None] = {
        "before_latest_filing": (filed[n - 1] - dt.timedelta(days=1)).isoformat(),
        "latest_filing": filed[n - 1].isoformat(),
        "original_restatement": None if same_day else filed[rs].isoformat(),
        "after_restatement": amend.isoformat(),
    }
    as_of: dict[str, dict[str, dict[str, float]]] = {}
    for name in ("before_latest_filing", "latest_filing", "original_restatement", "after_restatement"):
        iso = cutoffs[name]
        if iso is not None:
            as_of[iso] = truth_at(dt.date.fromisoformat(iso))

    sample, planted = _sample(seed)
    conflict = json.loads(json.dumps(facts))  # the same filing twice, with a different value and the same (filed, accn)
    latest_assets = [
        obs
        for obs in conflict["facts"]["us-gaap"]["Assets"]["units"]["USD"]
        if obs["end"] == ends[-1].isoformat() and obs["form"] == "10-K"
    ]
    twin = dict(latest_assets[0])
    twin["val"] = round(float(twin["val"]) * 1.01, 2)
    conflict["facts"]["us-gaap"]["Assets"]["units"]["USD"].append(twin)
    payload = {
        "facts": facts,
        "conflict": conflict,
        "period_ends": [e.isoformat() for e in ends],
        "truth": {"final": truth_at(None), "as_of": as_of},
        "cutoffs": cutoffs,
        "restatement": {"year": ends[rs].isoformat(), "item": rs_item, "same_day": same_day},
        "sample": sample,
        "planted": planted,
    }
    return {
        "seed": int(seed),
        "label": "SIMULATED",
        "latest": ends[-1].isoformat(),
        "prior": ends[-2].isoformat(),
        "prior2": ends[-3].isoformat(),
        "payload": json.dumps(payload, sort_keys=True),
    }
