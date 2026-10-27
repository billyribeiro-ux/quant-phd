"""Lab AC2-L08-1: the eight Beneish indices and the M-score on generated firm-years,
and the false-positive base-rate arithmetic for a screen.

Every firm is SIMULATED (seeded generator, no filer represented). Index definitions are the
contract's (atlas/A15.contract.md, beneish_m_score), which follow Beneish (1999).

UNCONFIRMED CONSTANTS. The intercept and the eight weights below are candidate values taken from
the Wikipedia page "Beneish M-score" (https://en.wikipedia.org/wiki/Beneish_M-score, read by plain
curl on 2026-10-27), a secondary source. They have NOT been confirmed against Beneish (1999) or a
source that reproduces its table. The M-values printed here are therefore illustrations of the
arithmetic, not evidence of anything.

The base-rate section uses illustrative inputs (a sensitivity of 0.5 and the grid of prevalences
and specificities printed below). They are assumptions, not estimates from any study.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

SEED = 20260528
N_CLEAN = 300
N_PLANTED = 300

# UNCONFIRMED candidate constants (see the module docstring). Do not cite as Beneish's values.
UNCONFIRMED_INTERCEPT = -4.84
UNCONFIRMED_COEFFICIENTS: dict[str, float] = {
    "DSRI": 0.920,
    "GMI": 0.528,
    "AQI": 0.404,
    "SGI": 0.892,
    "DEPI": 0.115,
    "SGAI": -0.172,
    "LVGI": -0.327,
    "TATA": 4.679,
}


@dataclass(frozen=True)
class FirmYear:
    """One fiscal year of a SIMULATED firm. Money in SCU."""

    revenue: float
    cogs: float
    receivables: float
    current_assets: float
    ppe: float
    total_assets: float
    depreciation: float
    sga: float
    current_liabilities: float
    long_term_debt: float
    net_income: float
    cfo: float


def gross_margin(f: FirmYear) -> float:
    """Gross margin (revenue - cogs) / revenue, dimensionless; revenue must be positive."""
    if f.revenue <= 0.0:
        raise ValueError("revenue must be positive")
    return (f.revenue - f.cogs) / f.revenue


def _need_positive(value: float, name: str) -> None:
    if not value > 0.0:
        raise ValueError(f"{name} must be positive")


def beneish_indices(t: FirmYear, p: FirmYear) -> dict[str, float]:
    """Return the eight Beneish indices for year t (= t) against year t-1 (= p), per the contract.

    Raises ValueError on any zero or negative denominator the formulas need.
    """
    for name, v in (
        ("revenue_t", t.revenue),
        ("revenue_t-1", p.revenue),
        ("total_assets_t", t.total_assets),
        ("total_assets_t-1", p.total_assets),
        ("gross_margin_t", gross_margin(t)),
        ("gross_margin_t-1", gross_margin(p)),
        ("sga_t", t.sga),
        ("sga_t-1", p.sga),
        ("dep+ppe_t", t.depreciation + t.ppe),
        ("dep+ppe_t-1", p.depreciation + p.ppe),
        ("depreciation_t", t.depreciation),
        ("depreciation_t-1", p.depreciation),
    ):
        _need_positive(v, name)
    dsri = (t.receivables / t.revenue) / (p.receivables / p.revenue)
    gmi = gross_margin(p) / gross_margin(t)
    aqi_t = 1.0 - (t.current_assets + t.ppe) / t.total_assets
    aqi_p = 1.0 - (p.current_assets + p.ppe) / p.total_assets
    _need_positive(aqi_p, "asset-quality denominator t-1")
    aqi = aqi_t / aqi_p
    sgi = t.revenue / p.revenue
    depi = (p.depreciation / (p.depreciation + p.ppe)) / (t.depreciation / (t.depreciation + t.ppe))
    sgai = (t.sga / t.revenue) / (p.sga / p.revenue)
    lvgi = ((t.current_liabilities + t.long_term_debt) / t.total_assets) / (
        (p.current_liabilities + p.long_term_debt) / p.total_assets
    )
    tata = (t.net_income - t.cfo) / t.total_assets
    return {"DSRI": dsri, "GMI": gmi, "AQI": aqi, "SGI": sgi, "DEPI": depi, "SGAI": sgai, "LVGI": lvgi, "TATA": tata}


def m_score(indices: dict[str, float]) -> float:
    """M = intercept + sum of weight * index, with the UNCONFIRMED candidate constants."""
    return UNCONFIRMED_INTERCEPT + sum(UNCONFIRMED_COEFFICIENTS[k] * indices[k] for k in UNCONFIRMED_COEFFICIENTS)


def _clean_pair(rng: random.Random) -> tuple[FirmYear, FirmYear]:
    """A SIMULATED firm with ordinary year-on-year movement."""
    assets = rng.uniform(900.0, 1100.0)
    revenue = assets * rng.uniform(0.9, 1.3)
    gm = rng.uniform(0.3, 0.5)
    years: list[FirmYear] = []
    for _ in range(2):
        assets *= rng.uniform(0.97, 1.05)
        revenue *= rng.uniform(0.97, 1.06)
        ppe = assets * rng.uniform(0.25, 0.35)
        dep = ppe * rng.uniform(0.09, 0.12)
        sga = revenue * rng.uniform(0.15, 0.22)
        cogs = revenue * (1.0 - gm * rng.uniform(0.97, 1.03))
        receivables = revenue * rng.uniform(0.11, 0.14)
        ca = assets * rng.uniform(0.3, 0.4)
        cl = assets * rng.uniform(0.2, 0.3)
        ltd = assets * rng.uniform(0.1, 0.2)
        ni = revenue * rng.uniform(0.02, 0.06)
        cfo = ni + rng.uniform(-0.03, 0.03) * assets
        years.append(
            FirmYear(
                revenue=revenue,
                cogs=cogs,
                receivables=receivables,
                current_assets=ca,
                ppe=ppe,
                total_assets=assets,
                depreciation=dep,
                sga=sga,
                current_liabilities=cl,
                long_term_debt=ltd,
                net_income=ni,
                cfo=cfo,
            )
        )
    return years[0], years[1]


def _planted_pair(rng: random.Random) -> tuple[FirmYear, FirmYear]:
    """A SIMULATED firm whose year t carries the usual manipulation footprints:
    receivables outrun revenue, margins fall, depreciation is slowed, and accruals are high."""
    p, t = _clean_pair(rng)
    t_rec = t.receivables * rng.uniform(1.35, 1.6)
    t_gm_cogs = t.revenue * (1.0 - (gross_margin(p) * rng.uniform(0.7, 0.85)))
    t_dep = p.depreciation * rng.uniform(0.7, 0.85)
    t_cfo = t.net_income - rng.uniform(0.06, 0.1) * t.total_assets
    planted = FirmYear(
        revenue=t.revenue,
        cogs=t_gm_cogs,
        receivables=t_rec,
        current_assets=t.current_assets,
        ppe=t.ppe,
        total_assets=t.total_assets,
        depreciation=t_dep,
        sga=t.sga,
        current_liabilities=t.current_liabilities,
        long_term_debt=t.long_term_debt,
        net_income=t.net_income,
        cfo=t_cfo,
    )
    return p, planted


def scale(f: FirmYear, k: float) -> FirmYear:
    """Multiply every money item by k > 0."""
    return FirmYear(
        revenue=f.revenue * k,
        cogs=f.cogs * k,
        receivables=f.receivables * k,
        current_assets=f.current_assets * k,
        ppe=f.ppe * k,
        total_assets=f.total_assets * k,
        depreciation=f.depreciation * k,
        sga=f.sga * k,
        current_liabilities=f.current_liabilities * k,
        long_term_debt=f.long_term_debt * k,
        net_income=f.net_income * k,
        cfo=f.cfo * k,
    )


def _median(xs: list[float]) -> float:
    s = sorted(xs)
    n = len(s)
    mid = n // 2
    return s[mid] if n % 2 else (s[mid - 1] + s[mid]) / 2.0


def base_rate_table() -> list[tuple[float, float, float, float, float]]:
    """Rows (prevalence, specificity, FPR, PPV, false flags per 1000 firm-years).

    Illustrative sensitivity 0.5 (an assumption, not an estimate). PPV by Bayes' rule:
    PPV = p*s / (p*s + (1-p)*(1-spec)); FPR = 1 - spec; false flags per 1000 = 1000*(1-p)*FPR.
    """
    sensitivity = 0.5
    rows: list[tuple[float, float, float, float, float]] = []
    for prevalence in (0.001, 0.01, 0.05):
        for spec in (0.90, 0.95, 0.99):
            fpr = 1.0 - spec
            ppv = prevalence * sensitivity / (prevalence * sensitivity + (1.0 - prevalence) * fpr)
            false_flags = 1000.0 * (1.0 - prevalence) * fpr
            rows.append((prevalence, spec, fpr, ppv, false_flags))
    return rows


def combined_false_positive_rates(f1: float, f2: float) -> tuple[float, float]:
    """False-positive rates of the AND and OR rules for two screens with false-positive rates f1, f2.

    Assumes the two screens' false flags are independent among clean firms, which the lesson
    states as an assumption and does not establish. AND = f1*f2; OR = 1-(1-f1)*(1-f2).
    """
    if not (0.0 <= f1 <= 1.0 and 0.0 <= f2 <= 1.0):
        raise ValueError("false-positive rates must lie in [0, 1]")
    return f1 * f2, 1.0 - (1.0 - f1) * (1.0 - f2)


def main() -> None:
    """Print the worked index vector for one planted and one clean firm, the M-score distributions,
    the scale-invariance check, and the base-rate table."""
    rng = random.Random(SEED)
    clean_m: list[float] = []
    planted_m: list[float] = []
    clean_pairs = [_clean_pair(rng) for _ in range(N_CLEAN)]
    planted_pairs = [_planted_pair(rng) for _ in range(N_PLANTED)]

    p0, t0 = planted_pairs[0]
    idx0 = beneish_indices(t0, p0)
    print("SIMULATED planted firm, year t against t-1 (index, value):")
    for name in ("DSRI", "GMI", "AQI", "SGI", "DEPI", "SGAI", "LVGI", "TATA"):
        print(f"  {name:4s} {idx0[name]:.4f}")
    print(f"  M (UNCONFIRMED constants) = {m_score(idx0):.4f}")

    for p, t in clean_pairs:
        clean_m.append(m_score(beneish_indices(t, p)))
    for p, t in planted_pairs:
        planted_m.append(m_score(beneish_indices(t, p)))
    print("M-score medians (UNCONFIRMED constants, SIMULATED firms):")
    print(f"  clean firm-years   n={N_CLEAN}: median M = {_median(clean_m):.4f}")
    print(f"  planted firm-years n={N_PLANTED}: median M = {_median(planted_m):.4f}")

    # Each index is a ratio of money items, so every index and M are unchanged when money scales.
    unchanged = 0
    all_pairs = clean_pairs + planted_pairs
    for p, t in all_pairs:
        a = beneish_indices(t, p)
        b = beneish_indices(scale(t, 1000.0), scale(p, 1000.0))
        if all(abs(a[k] - b[k]) <= 1e-9 * max(1.0, abs(a[k])) for k in a):
            unchanged += 1
    print(f"indices unchanged under money x1000 (all clean and planted firm-years): {unchanged}/{len(all_pairs)}")

    print("base-rate table (illustrative sensitivity 0.5):")
    print("  prevalence  specificity   FPR    PPV     false flags per 1000")
    for prevalence, spec, fpr, ppv, flags in base_rate_table():
        print(f"  {prevalence:9.3f}  {spec:11.2f}  {fpr:5.3f}  {ppv:6.4f}  {flags:8.2f}")
    and_fpr, or_fpr = combined_false_positive_rates(0.10, 0.05)
    print("combined rules, illustrative false-positive rates 0.10 (screen 1) and 0.05 (screen 2):")
    print(f"  AND rule FPR = {and_fpr:.4f}")
    print(f"  OR rule  FPR = {or_fpr:.4f}")


main()
