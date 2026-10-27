"""AC2 lab L03: NOPAT, invested capital and ROIC on a SIMULATED generated filer.

SIMULATED: the filer is generated from a seeded RNG (make_filer, the same mapping as Labs 1 and 2). Nothing here is
a real company's data. The definitions follow atlas/A15.contract.md (roic): NOPAT = operating_income * (1 - tax_rate)
with 0 <= tax_rate < 1, and invested capital = equity + long_term_debt - cash at each year end, averaged over the
two year ends. The lab checks that ROIC scales exactly with (1 - tax_rate), and shows what the cash convention and the
denominator convention do to the answer. Standard library only; no network.
"""

from __future__ import annotations

import math
import random
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import date
from typing import Any

SEED = 20261027
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


@dataclass(frozen=True)
class Observation:
    """One parsed observation. Dates are datetime.date; val is a finite float in the filing's unit."""

    end: date
    val: float
    filed: date
    form: str
    fp: str
    accn: str
    start: date | None


def _date(value: object, where: str) -> date:
    """Parse an ISO date with date.fromisoformat; anything else raises ValueError."""
    if not isinstance(value, str):
        raise ValueError(f"{where} must be an ISO date string, not {type(value).__name__}")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{where} is not an ISO date: {value!r}") from exc


def _observation(raw: object, tag: str, unit: str) -> Observation:
    """Validate one raw observation; a missing or malformed required key raises ValueError."""
    where = f"{tag} [{unit}]"
    if not isinstance(raw, Mapping):
        raise ValueError(f"{where}: an observation must be a mapping")
    for key in ("end", "val", "filed", "form"):
        if key not in raw:
            raise ValueError(f"{where}: observation lacks {key!r}")
    value = raw["val"]
    if isinstance(value, bool) or not isinstance(value, int | float) or not math.isfinite(value):
        raise ValueError(f"{where}: val must be a finite number, not {value!r}")
    form = raw["form"]
    if not isinstance(form, str):
        raise ValueError(f"{where}: form must be a string")
    fp = raw.get("fp", "")
    accn = raw.get("accn", "")
    if not isinstance(fp, str) or not isinstance(accn, str):
        raise ValueError(f"{where}: fp and accn must be strings when present")
    start = _date(raw["start"], f"{where}: start") if "start" in raw else None
    return Observation(
        end=_date(raw["end"], f"{where}: end"),
        val=float(value),
        filed=_date(raw["filed"], f"{where}: filed"),
        form=form,
        fp=fp,
        accn=accn,
        start=start,
    )


def _is_annual(obs: Observation, flow: bool) -> bool:
    """Annual: form 10-K*, fp FY, and a 350-380 day duration (flow) or no start date (instant)."""
    if not obs.form.startswith("10-K") or obs.fp != "FY":
        return False
    if flow:
        return obs.start is not None and 350 <= (obs.end - obs.start).days <= 380
    return obs.start is None


def _us_gaap(facts: Mapping[str, Any]) -> Mapping[str, Any]:
    """Return the us-gaap block; a mapping without 'facts' raises ValueError."""
    if not isinstance(facts, Mapping) or "facts" not in facts:
        raise ValueError("the company-facts mapping lacks 'facts'")
    block = facts["facts"]
    if not isinstance(block, Mapping):
        raise ValueError("'facts' must be a mapping")
    gaap = block.get("us-gaap", {})
    if not isinstance(gaap, Mapping):
        raise ValueError("'facts[us-gaap]' must be a mapping")
    return gaap


def _as_of_pick(
    gaap: Mapping[str, Any], tag: str, unit: str, flow: bool, cutoff: date | None
) -> dict[date, Observation]:
    """For one tag: per period end, the annual observation with the greatest (filed, accn) among filed <= cutoff."""
    block = gaap.get(tag)
    if block is None:
        return {}
    if not isinstance(block, Mapping) or not isinstance(block.get("units", {}), Mapping):
        raise ValueError(f"{tag}: must be a mapping with a 'units' mapping")
    rows = block.get("units", {}).get(unit, [])
    if not isinstance(rows, list):
        raise ValueError(f"{tag} [{unit}]: observations must be a list")
    best: dict[date, Observation] = {}
    for raw in rows:
        obs = _observation(raw, tag, unit)
        if not _is_annual(obs, flow):
            continue
        if cutoff is not None and obs.filed > cutoff:
            continue
        current = best.get(obs.end)
        if current is None or (obs.filed, obs.accn) > (current.filed, current.accn):
            best[obs.end] = obs
    return best


def select(facts: Mapping[str, Any], as_of: str | None = None) -> dict[str, dict[date, tuple[str, Observation]]]:
    """Per item and period end, the winning (tag, observation) under the tag priority and the as-of rule."""
    cutoff = None if as_of is None else _date(as_of, "as_of")
    gaap = _us_gaap(facts)
    out: dict[str, dict[date, tuple[str, Observation]]] = {}
    for item in ITEMS:
        flow = item in FLOW_ITEMS
        unit = "shares" if item == "shares_outstanding" else "USD"
        per_tag = {tag: _as_of_pick(gaap, tag, unit, flow, cutoff) for tag in TAG_PRIORITY[item]}
        ends: set[date] = set()
        for picks in per_tag.values():
            ends.update(picks)
        winners: dict[date, tuple[str, Observation]] = {}
        for end in ends:
            for tag in TAG_PRIORITY[item]:
                if end in per_tag[tag]:
                    winners[end] = (tag, per_tag[tag][end])
                    break
        out[item] = winners
    return out


def standardize(facts: Mapping[str, Any], as_of: str | None = None) -> dict[str, dict[str, float]]:
    """{period_end_iso: {item: value}}, period ends ascending; absent items are absent (nothing imputed)."""
    picked = select(facts, as_of)
    table: dict[date, dict[str, float]] = {}
    for item in ITEMS:
        for end, (_tag, obs) in picked[item].items():
            table.setdefault(end, {})[item] = obs.val
    return {end.isoformat(): table[end] for end in sorted(table)}


def make_filer(seed: int = SEED) -> dict[str, Any]:
    """A SIMULATED company-facts mapping: five fiscal years, 10-K comparatives, a restatement, a 10-Q, a Q4 row."""
    rng = random.Random(seed)
    years = (2020, 2021, 2022, 2023, 2024)
    rev = {2020: 1_000_000_000}
    for y in years[1:]:
        rev[y] = round(rev[y - 1] * (1 + rng.uniform(0.04, 0.09)))
    cogs = {y: round(rev[y] * rng.uniform(0.58, 0.64)) for y in years}
    sga = {y: round(rev[y] * rng.uniform(0.18, 0.22)) for y in years}
    noise = {y: round(rev[y] * rng.uniform(-0.03, 0.03)) for y in years}
    dep: dict[int, int] = {2020: 38_000_000}
    ppe: dict[int, int] = {2020: 400_000_000}
    for y in years[1:]:
        dep[y] = round(ppe[y - 1] * 0.10)
        ppe[y] = ppe[y - 1] + round(rev[y] * 0.06) - dep[y]
    oi = {y: rev[y] - cogs[y] - sga[y] - dep[y] for y in years}
    ni = {y: round(oi[y] * 0.75) for y in years}
    cfo = {y: ni[y] + dep[y] + noise[y] for y in years}
    eq: dict[int, int] = {2020: 600_000_000}
    for y in years[1:]:
        eq[y] = eq[y - 1] + ni[y] - round(0.4 * ni[y])
    ltd = {y: 300_000_000 + 10_000_000 * (y - 2020) for y in years}
    cash = {y: round(rev[y] * 0.08) for y in years}
    recv = {y: round(rev[y] * 0.12) for y in years}
    inv = {y: round(cogs[y] * 0.15) for y in years}
    other_ca = {y: round(rev[y] * 0.03) for y in years}
    ca = {y: cash[y] + recv[y] + inv[y] + other_ca[y] for y in years}
    cl = {y: round(cogs[y] * 0.25) for y in years}
    ol = {y: round(rev[y] * 0.05) for y in years}
    tl = {y: cl[y] + ltd[y] + ol[y] for y in years}
    ta = {y: tl[y] + eq[y] for y in years}
    shares = {y: 50_000_000 if y < 2024 else 52_000_000 for y in years}

    def fy_tag(item: str, fy: int) -> str:
        if item == "revenue":
            return "Revenues" if fy <= 2021 else "RevenueFromContractWithCustomerExcludingAssessedTax"
        if item == "cogs":
            return "CostOfRevenue" if fy <= 2022 else "CostOfGoodsAndServicesSold"
        return TAG_PRIORITY[item][0]

    truth: dict[str, dict[int, int]] = {
        "revenue": rev,
        "cogs": cogs,
        "sga": sga,
        "depreciation": dep,
        "operating_income": oi,
        "net_income": ni,
        "cfo": cfo,
        "total_assets": ta,
        "current_assets": ca,
        "cash": cash,
        "receivables": recv,
        "ppe": ppe,
        "total_liabilities": tl,
        "current_liabilities": cl,
        "long_term_debt": ltd,
        "equity": eq,
        "shares_outstanding": shares,
    }
    flows = {"revenue", "cogs", "sga", "depreciation", "operating_income", "net_income", "cfo"}
    gaap: dict[str, dict[str, dict[str, list[dict[str, Any]]]]] = {}

    def add(item: str, fy: int, end_year: int, val: int, form: str, fp: str, accn: str, filed: str) -> None:
        tag = fy_tag(item, fy)
        unit = "shares" if item == "shares_outstanding" else "USD"
        obs: dict[str, Any] = {"end": f"{end_year}-12-31", "val": val, "filed": filed, "form": form, "fp": fp}
        if item in flows:
            obs["start"] = f"{end_year}-01-01"  # a full fiscal year, 365 days
            if fp == "Q1":
                obs["end"] = f"{end_year}-03-31"
            if fp == "Q4":
                obs["start"] = f"{end_year}-10-01"
        obs["accn"] = accn
        units: dict[str, list[dict[str, Any]]] = gaap.setdefault(tag, {"units": {}})["units"]
        units.setdefault(unit, []).append(obs)

    for fy in years:
        filed = f"{fy + 1}-02-15"
        accn = f"SIM-{fy}-K"
        for end_year in (fy, fy - 1):
            if end_year < 2020:
                continue
            for item in truth:
                if item == "long_term_debt" and end_year == 2020:
                    continue  # never published: the 2020 long-term debt is absent from the file
                add(item, fy, end_year, truth[item][end_year], "10-K", "FY", accn, filed)
        if fy == 2023:
            add("revenue", fy, 2023, rev[2023] // 4, "10-K", "Q4", accn, filed)
    # Restatement of FY2022 revenue, filed later as a 10-K/A.
    add("revenue", 2023, 2022, round(rev[2022] * 1.012), "10-K/A", "FY", "SIM-2023-KA", "2024-03-01")
    # Quarterly revenue from 10-Q filings: never annual, so the rules ignore them.
    for fy in years[1:]:
        add("revenue", fy, fy, rev[fy] // 4, "10-Q", "Q1", f"SIM-{fy}-Q1", f"{fy}-05-10")
    return {
        "cik": 1,
        "entityName": "SIMULATED FILER 1 (generated; not a real company)",
        "facts": {"us-gaap": gaap},
    }


Statements = Mapping[str, Mapping[str, float]]


def _previous_year(statements: Statements, period_end: str) -> str:
    """The latest period end 350 to 380 days before period_end; none raises ValueError."""
    end = _date(period_end, "period_end")
    earlier = [e for e in statements if 350 <= (end - date.fromisoformat(e)).days <= 380]
    if not earlier:
        raise ValueError(f"no previous year for {period_end}: no period end 350 to 380 days earlier")
    return max(earlier, key=date.fromisoformat)


def _item(statements: Statements, period_end: str, item: str) -> float:
    row = statements.get(period_end)
    if row is None:
        raise ValueError(f"no statement for period end {period_end}")
    if item not in row:
        raise ValueError(f"{item} is missing for period end {period_end}")
    return row[item]


def invested_capital(statements: Statements, period_end: str) -> float:
    """Year-end invested capital under the A15 convention: equity + long_term_debt - cash."""
    return (
        _item(statements, period_end, "equity")
        + _item(statements, period_end, "long_term_debt")
        - _item(statements, period_end, "cash")
    )


def nopat(statements: Statements, period_end: str, tax_rate: float) -> float:
    """Operating income after tax at the stated rate; 0 <= tax_rate < 1 or ValueError."""
    if not math.isfinite(tax_rate) or not 0 <= tax_rate < 1:
        raise ValueError(f"tax_rate must satisfy 0 <= tax_rate < 1, got {tax_rate!r}")
    return _item(statements, period_end, "operating_income") * (1 - tax_rate)


def roic(statements: Statements, period_end: str, tax_rate: float) -> float:
    """NOPAT over the average of the two year-end invested-capital balances (A15 contract, roic)."""
    operating = nopat(statements, period_end, tax_rate)
    previous = _previous_year(statements, period_end)
    average_ic = (invested_capital(statements, period_end) + invested_capital(statements, previous)) / 2
    if average_ic <= 0:
        raise ValueError(f"average invested capital at {period_end} is not positive ({average_ic:,.0f})")
    value = operating / average_ic
    if not math.isfinite(value):
        raise ValueError("roic: non-finite result")
    return value


def millions(value: float) -> str:
    return f"{value / 1e6:,.1f}"


def main() -> None:
    filer = make_filer()
    statements = standardize(filer)
    ends = list(statements)
    print("invested capital at year ends, USD millions (equity + long-term debt - cash)")
    print("period_end  equity  long_term_debt     cash  invested_capital  operating_income  net_income")
    for end in ends:
        row = statements[end]
        if "long_term_debt" not in row:
            print(f"{end}  {millions(row['equity']):>6}  absent: long_term_debt not published")
            continue
        ic = invested_capital(statements, end)
        print(
            f"{end}  {millions(row['equity']):>6}  {millions(row['long_term_debt']):>14}  {millions(row['cash']):>7}"
            f"  {millions(ic):>16}  {millions(row['operating_income']):>16}  {millions(row['net_income']):>10}"
        )

    implied = {end: 1 - statements[end]["net_income"] / statements[end]["operating_income"] for end in ends}
    print("tax rate implied by net income (1 - NI/OI):", ", ".join(f"{implied[e]:.4f}" for e in ends))

    rates = (0.0, 0.15, 0.21, 0.25, 0.30)
    print("ROIC, average invested capital, by tax rate (rates are grid values, not statutory claims)")
    print("period_end  " + "  ".join(f"t={r:.2f}" for r in rates))
    worst = 0.0
    for end in ends[2:]:
        values = [roic(statements, end, r) for r in rates]
        base = values[0]
        for r, value in zip(rates, values, strict=True):
            worst = max(worst, abs(value - base * (1 - r)) / abs(base))
        print(f"{end}  " + "  ".join(f"{v:6.4f}" for v in values))
    print("largest relative deviation of ROIC(t) from ROIC(0) * (1 - t):", f"{worst:.1e}")

    end = "2023-12-31"
    no_cash = {e: {**row, "cash": 0.0} for e, row in statements.items()}
    print(
        f"FY2023 ROIC at 25%: with cash netted {roic(statements, end, 0.25):.4f};"
        f" cash not netted {roic(no_cash, end, 0.25):.4f}"
    )
    average_ic = (invested_capital(statements, end) + invested_capital(statements, "2022-12-31")) / 2
    year_end_roic = nopat(statements, end, 0.25) / invested_capital(statements, end)
    print(
        f"FY2023 ROIC at 25%: on average invested capital {roic(statements, end, 0.25):.4f}"
        f" ({average_ic / 1e6:,.1f} USD m); on year-end invested capital {year_end_roic:.4f}"
    )

    cases: list[tuple[str, Callable[[], float]]] = [
        ("roic at 2021-12-31 (2020 long-term debt not published)", lambda: roic(statements, "2021-12-31", 0.25)),
        ("roic with tax_rate 1.0", lambda: roic(statements, end, 1.0)),
        ("roic with tax_rate -0.1", lambda: roic(statements, end, -0.1)),
    ]
    for label, call in cases:
        try:
            call()
        except ValueError as exc:
            print(f"ValueError ({label}): {exc}")
        else:
            print(f"no error ({label})")
    negative = {
        "2022-12-31": {"operating_income": 1.0, "equity": -10.0, "long_term_debt": 0.0, "cash": 0.0},
        "2023-12-31": {"operating_income": 1.0, "equity": -10.0, "long_term_debt": 0.0, "cash": 0.0},
    }
    try:
        roic(negative, "2023-12-31", 0.0)
    except ValueError as exc:
        print(f"ValueError (non-positive average invested capital): {exc}")


if __name__ == "__main__":
    main()
