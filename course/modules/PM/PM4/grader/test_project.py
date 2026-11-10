"""Acceptance test suite for PM4: Real Estate Finance & Mortgage-Backed Securities.

Runs identically in Pyodide and native pytest:
    pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import math
import os
from typing import Any

import numpy as np
import pytest
from instance import make_instance  # type: ignore[import-not-found, unused-ignore]
from reference import (  # type: ignore[import-not-found, unused-ignore]
    generate_mbs_cash_flows,
    price_mbs,
    simulate_interest_rates,
    solve_mbs_pricer,
    solve_oas,
)

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)


# ============================================================================
# 1. Short-Rate Simulation Dynamics (Vasicek 1-factor)
# ============================================================================


def test_rate_simulation_properties() -> None:
    r0 = float(INST["r0"])
    kappa = float(INST["kappa"])
    theta = float(INST["theta"])
    sigma = float(INST["sigma"])
    wam = int(INST["wam"])
    n_paths = int(INST["n_paths"])
    seed = int(INST["sim_seed"])

    rates = simulate_interest_rates(r0, kappa, theta, sigma, wam, n_paths, seed=seed)

    assert rates.shape == (n_paths, wam), f"Expected shape ({n_paths}, {wam}), got {rates.shape}"
    assert np.all(np.isfinite(rates)), "Simulated rates contain NaN or infinite values"
    assert np.allclose(rates[:, 0], r0), f"All paths must start at r0 = {r0}"

    # Mean reversion check: terminal rate mean should be close to theta
    mean_term = float(np.mean(rates[:, -1]))
    assert abs(mean_term - theta) < 0.015, f"Terminal mean {mean_term} drifted too far from theta {theta}"


# ============================================================================
# 2. Cash Flow Waterfall & Prepayment Dynamics
# ============================================================================


def test_cash_flow_generation_and_prepayment() -> None:
    notional = float(INST["notional"])
    wac = float(INST["wac"])
    pass_through_rate = float(INST["pass_through_rate"])
    wam = int(INST["wam"])

    base_cpr = float(INST["base_cpr"])
    max_cpr = float(INST["max_cpr"])
    beta = float(INST["beta"])
    mu = float(INST["mu"])
    margin = float(INST["margin"])
    gamma_burnout = float(INST["gamma_burnout"])

    n_paths = int(INST["n_paths"])
    seed = int(INST["sim_seed"])

    rates = simulate_interest_rates(
        float(INST["r0"]),
        float(INST["kappa"]),
        float(INST["theta"]),
        float(INST["sigma"]),
        wam,
        n_paths,
        seed=seed,
    )

    cash_flows = generate_mbs_cash_flows(
        notional, wac, pass_through_rate, wam, base_cpr, max_cpr, beta, mu, margin, gamma_burnout, rates
    )

    assert cash_flows.shape == (n_paths, wam)
    assert np.all(np.isfinite(cash_flows)), "Cash flows contain NaN or Inf"
    assert np.all(cash_flows > 0.0), "All monthly MBS cash flows must be strictly positive"

    # Prepayment test: total cash flows across paths must return all principal plus interest
    avg_total_cf = float(np.mean(np.sum(cash_flows, axis=1)))
    assert avg_total_cf > notional, f"Total CF {avg_total_cf} must strictly exceed initial notional {notional}"

    # Prepayments must cause principal in first 60 months to exceed pure scheduled amortization
    wac_m = wac / 12.0
    denom = 1.0 - (1.0 + wac_m) ** (-wam)
    base_pmt = notional * (wac_m / denom)
    pure_sched_prin_60 = sum(
        (base_pmt - (notional * ((1.0 - (1.0 + wac_m) ** (-(wam - t))) / denom)) * wac_m) for t in range(60)
    )
    avg_cf_60 = float(np.mean(np.sum(cash_flows[:, :60], axis=1)))
    assert avg_cf_60 > pure_sched_prin_60 * 1.25, "Prepayment acceleration failed to lift early cash flows"


# ============================================================================
# 3. Settlement Delay Discounting
# ============================================================================


def test_delay_days_impact() -> None:
    notional = float(INST["notional"])
    wac = float(INST["wac"])
    pass_through_rate = float(INST["pass_through_rate"])
    wam = int(INST["wam"])

    base_cpr = float(INST["base_cpr"])
    max_cpr = float(INST["max_cpr"])
    beta = float(INST["beta"])
    mu = float(INST["mu"])
    margin = float(INST["margin"])
    gamma_burnout = float(INST["gamma_burnout"])

    n_paths = int(INST["n_paths"])
    seed = int(INST["sim_seed"])

    rates = simulate_interest_rates(
        float(INST["r0"]),
        float(INST["kappa"]),
        float(INST["theta"]),
        float(INST["sigma"]),
        wam,
        n_paths,
        seed=seed,
    )
    cash_flows = generate_mbs_cash_flows(
        notional, wac, pass_through_rate, wam, base_cpr, max_cpr, beta, mu, margin, gamma_burnout, rates
    )

    p_no_delay = price_mbs(cash_flows, rates, spread=0.0, delay_days=0)
    p_fannie_delay = price_mbs(cash_flows, rates, spread=0.0, delay_days=int(INST["delay_days"]))

    # Delay days must strictly decrease present value due to delayed receipt of funds
    delay_drag = p_no_delay - p_fannie_delay
    assert delay_drag > 10_000.0, f"Expected significant delay drag on $100M pool, got {delay_drag}"


# ============================================================================
# 4. OAS Calibration & Root-Finding
# ============================================================================


def test_oas_calibration() -> None:
    notional = float(INST["notional"])
    wac = float(INST["wac"])
    pass_through_rate = float(INST["pass_through_rate"])
    wam = int(INST["wam"])

    base_cpr = float(INST["base_cpr"])
    max_cpr = float(INST["max_cpr"])
    beta = float(INST["beta"])
    mu = float(INST["mu"])
    margin = float(INST["margin"])
    gamma_burnout = float(INST["gamma_burnout"])

    n_paths = int(INST["n_paths"])
    seed = int(INST["sim_seed"])
    delay_days = int(INST["delay_days"])
    target_mkt = float(INST["target_market_price"])

    rates = simulate_interest_rates(
        float(INST["r0"]),
        float(INST["kappa"]),
        float(INST["theta"]),
        float(INST["sigma"]),
        wam,
        n_paths,
        seed=seed,
    )
    cash_flows = generate_mbs_cash_flows(
        notional, wac, pass_through_rate, wam, base_cpr, max_cpr, beta, mu, margin, gamma_burnout, rates
    )

    oas_bps = solve_oas(rates, cash_flows, target_mkt, delay_days=delay_days)
    assert math.isfinite(oas_bps), f"OAS must be finite, got {oas_bps}"
    assert -500.0 <= oas_bps <= 500.0, f"OAS out of plausible bounds: {oas_bps}"

    # Price at calibrated OAS must match target market price within $10 on $100M notional
    p_at_oas = price_mbs(cash_flows, rates, spread=oas_bps / 10000.0, delay_days=delay_days)
    assert abs(p_at_oas - target_mkt) < 10.0, f"Price at OAS {p_at_oas} differs from target {target_mkt}"


# ============================================================================
# 5. Effective Risk Metrics (Duration & Convexity)
# ============================================================================


def test_effective_duration_and_negative_convexity() -> None:
    res = solve_mbs_pricer(INST)

    eff_dur = res["effective_duration"]
    eff_cvx = res["effective_convexity"]
    p_up = res["price_up"]
    p_down = res["price_down"]

    # Effective duration must be strictly positive for a long pass-through
    assert eff_dur > 0.5, f"Effective duration must be positive, got {eff_dur}"
    assert eff_dur < 10.0, f"Effective duration too long for MBS with prepayments: {eff_dur}"

    # Standard duration relation: price down > price up
    assert p_down > p_up, f"Price down {p_down} must exceed price up {p_up}"

    # Negative convexity test: in refinancing regime, eff_cvx must be negative
    assert eff_cvx < 0.0, f"MBS pass-through must exhibit negative convexity, got {eff_cvx}"


# ============================================================================
# 6. Burnout & Compounding Invariants
# ============================================================================


def test_burnout_and_compounding_invariants() -> None:
    notional = float(INST["notional"])
    wac = float(INST["wac"])
    pass_through_rate = float(INST["pass_through_rate"])
    wam = int(INST["wam"])

    base_cpr = float(INST["base_cpr"])
    max_cpr = float(INST["max_cpr"])
    beta = float(INST["beta"])
    mu = float(INST["mu"])
    margin = float(INST["margin"])
    gamma_burnout = float(INST["gamma_burnout"])

    n_paths = int(INST["n_paths"])

    # Constant low rate scenario (1.5% short rate, highly in the money)
    low_rates = np.full((n_paths, wam), 0.015)

    cf_burned = generate_mbs_cash_flows(
        notional, wac, pass_through_rate, wam, base_cpr, max_cpr, beta, mu, margin, gamma_burnout, low_rates
    )
    cf_noburn = generate_mbs_cash_flows(
        notional, wac, pass_through_rate, wam, base_cpr, max_cpr, beta, mu, margin, 0.0, low_rates
    )

    # 1. SMM compounding exactness (kills linear approximation mutants)
    refi_rate = low_rates[0, 0] + margin
    refi_spread = wac - refi_rate - mu
    incentive_0 = max(0.0, wac - refi_rate)
    burnout_0 = float(np.exp(-gamma_burnout * incentive_0))
    cpr_1 = (base_cpr + (max_cpr - base_cpr) / (1.0 + np.exp(-beta * refi_spread))) * burnout_0
    smm_compound = 1.0 - (1.0 - cpr_1) ** (1.0 / 12.0)
    wac_m = wac / 12.0
    denom = 1.0 - (1.0 + wac_m) ** (-wam)
    pmt = notional * (wac_m / denom)
    sp = pmt - notional * wac_m
    expected_cf_1 = (notional * (pass_through_rate / 12.0)) + sp + (notional - sp) * smm_compound
    assert abs(cf_burned[0, 0] - expected_cf_1) < 1.0, "Month 1 cash flow must match exact compound SMM formula"

    # 2. Burnout responsiveness (kills mutants that omit burnout tracking)
    burnout_cf_diff = float(np.mean(np.abs(cf_burned[:, 24] - cf_noburn[:, 24])))
    assert burnout_cf_diff > 5000.0, "Cash flows must respond to burnout parameter gamma_burnout"
