"""Instance generator for the FI1 curve engine autograder.

SIMULATED: generates synthetic bond data, discount factors, yield parameters,
and date pairs for testing the Atlas A5 contract. Labelled SIMULATED per BLUEPRINT §5.3.

Deterministic per seed; valid by construction.
"""

from __future__ import annotations

import datetime
import json
import math
import random
from fractions import Fraction
from typing import Any

DAY_COUNT_CONVENTIONS: tuple[str, ...] = ("ACT/360", "ACT/365", "30/360")
NS_LAMBDA_GRID: tuple[float, ...] = tuple(float(x) * 0.25 for x in range(2, 41))
SVENSSON_LAMBDA1_GRID: tuple[float, ...] = (0.5, 1.0, 1.5, 2.0, 3.0, 5.0)
SVENSSON_LAMBDA2_GRID: tuple[float, ...] = (1.0, 2.0, 3.0, 5.0, 8.0, 12.0)


def _calc_unrounded_price(face_cents: int, coupon_rate: Fraction, periods: int, y: Fraction) -> Fraction:
    if y == 0:
        return Fraction(face_cents) * (1 + coupon_rate * periods)
    v = Fraction(1, 1) / (1 + y)
    vn = v**periods
    annuity = (1 - vn) / y
    return Fraction(face_cents) * (coupon_rate * annuity + vn)


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic test instance for a given integer seed."""
    rng = random.Random(seed)

    # 1. Day count test dates
    y_start = rng.randint(2020, 2024)
    m_start = rng.randint(1, 12)
    d_start = rng.randint(1, 28)
    start_date = datetime.date(y_start, m_start, d_start)
    add_days = rng.randint(15, 750)
    end_date = start_date + datetime.timedelta(days=add_days)

    # 2. Bond pricing instance
    face_cents = 100_000 * rng.randint(1, 10)
    c_num = rng.randint(1, 10)
    coupon_rate = Fraction(c_num, 200)  # 0.5% to 5.0% per period
    periods = rng.randint(4, 30)
    y_num = rng.randint(1, 15)
    yield_per_period = Fraction(y_num, 200)

    unrounded = _calc_unrounded_price(face_cents, coupon_rate, periods, yield_per_period)
    dirty_cents = math.floor(unrounded + Fraction(1, 2))

    # 3. YTM problem instance
    ytm_face = 100_000 * rng.randint(1, 5)
    ytm_c = Fraction(rng.randint(2, 8), 100)
    ytm_periods = rng.randint(6, 24)
    ytm_true_y = Fraction(rng.randint(3, 12), 200)
    ytm_unrounded = _calc_unrounded_price(ytm_face, ytm_c, ytm_periods, ytm_true_y)
    ytm_dirty_cents = math.floor(ytm_unrounded + Fraction(1, 2))

    # 4. Bootstrap bonds instance
    n_bootstrap = rng.randint(8, 12)
    bs_face = 100_000
    dfs = [Fraction(1, 1)]
    base_rate = Fraction(rng.randint(15, 35), 1000)
    slope = Fraction(rng.randint(1, 5), 10000)
    for n in range(1, n_bootstrap + 1):
        fwd = base_rate + slope * n
        dfs.append(dfs[-1] / (1 + fwd))

    bootstrap_bonds = []
    for n in range(1, n_bootstrap + 1):
        c = Fraction(rng.randint(10, 40), 1000)
        p_exact = Fraction(bs_face) * (c * sum(dfs[1 : n + 1]) + dfs[n])
        p_cents = math.floor(p_exact + Fraction(1, 2))
        bootstrap_bonds.append(
            {
                "periods": n,
                "coupon_rate": [c.numerator, c.denominator],
                "face_cents": bs_face,
                "price_cents": p_cents,
            }
        )

    # 5. Nelson-Siegel instance
    ns_lam = rng.choice(NS_LAMBDA_GRID)
    ns_b0 = round(rng.uniform(0.04, 0.08), 4)
    ns_b1 = round(rng.uniform(-0.03, -0.01), 4)
    ns_b2 = round(rng.uniform(0.01, 0.04), 4)
    ns_maturities_tuples = [
        [1, 4],
        [1, 2],
        [1, 1],
        [2, 1],
        [3, 1],
        [5, 1],
        [7, 1],
        [10, 1],
        [20, 1],
        [30, 1],
    ]
    ns_yields_tuples = []
    for num, den in ns_maturities_tuples:
        tau_val = float(num) / float(den)
        x = tau_val / ns_lam
        g = (1.0 - math.exp(-x)) / x
        y_val = ns_b0 + ns_b1 * g + ns_b2 * (g - math.exp(-x))
        y_frac = Fraction(round(y_val, 8)).limit_denominator(100_000_000)
        ns_yields_tuples.append([y_frac.numerator, y_frac.denominator])

    # 6. Svensson instance
    sv_l1 = rng.choice(SVENSSON_LAMBDA1_GRID)
    sv_l2 = rng.choice(tuple(lam for lam in SVENSSON_LAMBDA2_GRID if lam != sv_l1))
    sv_b0 = round(rng.uniform(0.04, 0.08), 4)
    sv_b1 = round(rng.uniform(-0.03, -0.01), 4)
    sv_b2 = round(rng.uniform(0.01, 0.04), 4)
    sv_b3 = round(rng.uniform(-0.02, -0.005), 4)
    sv_maturities_tuples = list(ns_maturities_tuples)
    sv_yields_tuples = []
    for num, den in sv_maturities_tuples:
        tau_val = float(num) / float(den)
        x1 = tau_val / sv_l1
        g1 = (1.0 - math.exp(-x1)) / x1
        x2 = tau_val / sv_l2
        g2 = (1.0 - math.exp(-x2)) / x2
        y_val = sv_b0 + sv_b1 * g1 + sv_b2 * (g1 - math.exp(-x1)) + sv_b3 * (g2 - math.exp(-x2))
        y_frac = Fraction(round(y_val, 8)).limit_denominator(100_000_000)
        sv_yields_tuples.append([y_frac.numerator, y_frac.denominator])

    payload_dict = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "face_cents": face_cents,
        "coupon_rate": [coupon_rate.numerator, coupon_rate.denominator],
        "periods": periods,
        "yield_per_period": [yield_per_period.numerator, yield_per_period.denominator],
        "expected_dirty_cents": dirty_cents,
        "ytm_face": ytm_face,
        "ytm_c": [ytm_c.numerator, ytm_c.denominator],
        "ytm_periods": ytm_periods,
        "ytm_true_y": [ytm_true_y.numerator, ytm_true_y.denominator],
        "ytm_dirty_cents": ytm_dirty_cents,
        "bootstrap_bonds": bootstrap_bonds,
        "ns_params": {
            "beta0": ns_b0,
            "beta1": ns_b1,
            "beta2": ns_b2,
            "lam": ns_lam,
        },
        "ns_maturities": ns_maturities_tuples,
        "ns_yields": ns_yields_tuples,
        "sv_params": {
            "beta0": sv_b0,
            "beta1": sv_b1,
            "beta2": sv_b2,
            "beta3": sv_b3,
            "lam1": sv_l1,
            "lam2": sv_l2,
        },
        "sv_maturities": sv_maturities_tuples,
        "sv_yields": sv_yields_tuples,
    }

    return {
        "seed": seed,
        "payload": json.dumps(payload_dict, sort_keys=True),
    }
