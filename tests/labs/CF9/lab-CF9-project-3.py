"""CF9 project lab 3 (rung 3 check): Reference numbers for independent memo evaluation.

SIMULATED: Meridian Global Industries generated deterministically from seed 42.
Standard library only; deterministic execution.
Computes and prints the exact baseline table, portfolio variance, CFaR,
and cross-border project valuation that the student's project memo must evaluate.
"""

from __future__ import annotations

import math
import random
from statistics import NormalDist
from typing import Any

CURRENCIES = ["EUR", "JPY", "GBP"]


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic, valid corporate hedging instance for the given seed."""
    rng = random.Random(seed)

    eur_rec = round(rng.uniform(22.0, 35.0), 2)
    eur_pay = round(rng.uniform(8.0, 14.0), 2)
    jpy_rec = round(rng.uniform(2500.0, 4200.0), 1)
    jpy_pay = round(rng.uniform(800.0, 1600.0), 1)
    gbp_rec = round(rng.uniform(14.0, 24.0), 2)
    gbp_pay = round(rng.uniform(4.0, 9.0), 2)

    s_eur = round(rng.uniform(1.05, 1.15), 4)
    s_jpy = round(rng.uniform(0.0065, 0.0075), 6)
    s_gbp = round(rng.uniform(1.24, 1.34), 4)

    vol_eur = round(rng.uniform(0.09, 0.12), 4)
    vol_jpy = round(rng.uniform(0.10, 0.14), 4)
    vol_gbp = round(rng.uniform(0.08, 0.11), 4)
    vols = [vol_eur, vol_jpy, vol_gbp]

    rho_ej = round(rng.uniform(0.25, 0.45), 4)
    rho_eg = round(rng.uniform(0.55, 0.75), 4)
    rho_jg = round(rng.uniform(0.20, 0.40), 4)

    corr_matrix = [
        [1.0, rho_ej, rho_eg],
        [rho_ej, 1.0, rho_jg],
        [rho_eg, rho_jg, 1.0],
    ]

    cov_matrix: list[list[float]] = []
    for i in range(3):
        row: list[float] = []
        for j in range(3):
            cov_ij = corr_matrix[i][j] * vols[i] * vols[j]
            row.append(round(cov_ij, 8))
        cov_matrix.append(row)

    hurdle = round(rng.uniform(42.0, 55.0), 2)
    domestic_costs_usd = round(rng.uniform(15.0, 25.0), 2)

    delta_exposure = round(rng.uniform(-12.0, -8.0), 2)
    ratio = round(rng.uniform(0.75, 1.30), 4)
    delta_derivative = round(abs(delta_exposure) * ratio, 2)

    initial_outlay_eur = round(rng.uniform(40.0, 60.0), 2)
    cf_eur_1 = round(rng.uniform(12.0, 18.0), 2)
    cf_eur_2 = round(rng.uniform(16.0, 24.0), 2)
    cf_eur_3 = round(rng.uniform(20.0, 28.0), 2)
    cf_eur_4 = round(rng.uniform(18.0, 25.0), 2)
    project_cfs_eur = [cf_eur_1, cf_eur_2, cf_eur_3, cf_eur_4]

    r_usd = round(rng.uniform(0.045, 0.055), 4)
    r_eur = round(rng.uniform(0.025, 0.035), 4)
    wacc_usd = round(rng.uniform(0.095, 0.115), 4)

    return {
        "seed": seed,
        "currencies": list(CURRENCIES),
        "receivables": [eur_rec, jpy_rec, gbp_rec],
        "payables": [eur_pay, jpy_pay, gbp_pay],
        "spot_rates": [s_eur, s_jpy, s_gbp],
        "fx_volatilities": [vol_eur, vol_jpy, vol_gbp],
        "correlation_matrix": corr_matrix,
        "covariance_matrix": cov_matrix,
        "hurdle_cash_flow": hurdle,
        "domestic_costs_usd": domestic_costs_usd,
        "delta_exposure": delta_exposure,
        "delta_derivative": delta_derivative,
        "initial_outlay_eur": initial_outlay_eur,
        "project_cfs_eur": project_cfs_eur,
        "r_usd": r_usd,
        "r_eur": r_eur,
        "wacc_usd": wacc_usd,
    }


def compute_net_transaction_exposure(receivables: dict[str, float], payables: dict[str, float]) -> dict[str, float]:
    """Calculate net contractual foreign currency exposure."""
    return {c: receivables[c] - payables[c] for c in receivables}


def compute_usd_exposure(net_fc_exposure: dict[str, float], spot_rates: dict[str, float]) -> dict[str, float]:
    """Translate foreign currency net exposures to domestic USD base currency."""
    return {c: net_fc_exposure[c] * spot_rates[c] for c in net_fc_exposure}


def portfolio_cash_flow_variance(weights: list[float], cov_matrix: list[list[float]]) -> float:
    """Calculate multi-currency portfolio cash flow variance: Var(CF) = w^T * Sigma * w."""
    n = len(weights)
    return sum(weights[i] * weights[j] * cov_matrix[i][j] for i in range(n) for j in range(n))


def evaluate_hedge_effectiveness(var_unhedged: float, var_hedged: float) -> float:
    """Calculate variance reduction percentage."""
    return 1.0 - (var_hedged / var_unhedged)


def compute_cfar(
    mean_cf: float,
    std_cf: float,
    alpha: float = 0.05,
    hurdle: float | None = None,
) -> dict[str, float]:
    """Compute analytical Cash-Flow-at-Risk under normality."""
    dist = NormalDist()
    z_alpha = dist.inv_cdf(1.0 - alpha)
    cfar_amount = z_alpha * std_cf
    worst_case_cf = mean_cf - cfar_amount
    prob_shortfall = 0.0
    if hurdle is not None:
        z_hurdle = (hurdle - mean_cf) / std_cf
        prob_shortfall = dist.cdf(z_hurdle)
    return {
        "mean_cf": mean_cf,
        "std_cf": std_cf,
        "cfar": cfar_amount,
        "worst_case_cf": worst_case_cf,
        "prob_shortfall": prob_shortfall,
    }


def hedge_accounting_test(delta_derivative: float, delta_exposure: float) -> dict[str, Any]:
    """Evaluate retrospective dollar-offset ratio for hedge accounting."""
    ratio = abs(delta_derivative) / abs(delta_exposure)
    qualified = 0.80 <= ratio <= 1.25
    return {
        "dollar_offset_ratio": ratio,
        "is_qualified": qualified,
    }


def cross_border_npv(
    initial_outlay_foreign: float,
    foreign_cfs: list[float],
    spot_fx: float,
    wacc_home: float,
    r_home: float,
    r_foreign: float,
    method: str = "foreign",
) -> float:
    """Calculate cross-border capital budgeting NPV in domestic currency."""
    if method == "foreign":
        wacc_foreign = ((1.0 + wacc_home) * (1.0 + r_foreign) / (1.0 + r_home)) - 1.0
        pv_foreign = sum(cf / ((1.0 + wacc_foreign) ** (t + 1)) for t, cf in enumerate(foreign_cfs))
        npv_foreign = -initial_outlay_foreign + pv_foreign
        return npv_foreign * spot_fx

    forward_rates = [spot_fx * (((1.0 + r_home) / (1.0 + r_foreign)) ** (t + 1)) for t in range(len(foreign_cfs))]
    home_cfs = [cf * fwd for cf, fwd in zip(foreign_cfs, forward_rates, strict=True)]
    pv_home = sum(cf / ((1.0 + wacc_home) ** (t + 1)) for t, cf in enumerate(home_cfs))
    return (-initial_outlay_foreign * spot_fx) + pv_home


def main() -> None:
    print("CF9 Project Lab 3: Seed 42 Reference Benchmark")
    print("==============================================")

    seed = 42
    inst = make_instance(seed)

    currencies = inst["currencies"]
    rec = dict(zip(currencies, inst["receivables"], strict=True))
    pay = dict(zip(currencies, inst["payables"], strict=True))
    spots = dict(zip(currencies, inst["spot_rates"], strict=True))
    cov_matrix = inst["covariance_matrix"]

    # 1. Net exposures
    net_fc = compute_net_transaction_exposure(rec, pay)
    usd_exp = compute_usd_exposure(net_fc, spots)
    exp_vector = [usd_exp[c] for c in currencies]

    print("1. Net Exposures (Seed 42):")
    for c in currencies:
        print(
            f"   {c}: Rec = {rec[c]:,.2f}M, Pay = {pay[c]:,.2f}M -> "
            f"Net = {net_fc[c]:,.2f}M (Spot = {spots[c]:.6f}, USD = ${usd_exp[c]:,.2f}M)"
        )

    gross_usd = sum(exp_vector)
    domestic_costs = inst["domestic_costs_usd"]
    expected_cf = gross_usd - domestic_costs
    print(f"   Total Gross Foreign Cash Flow:   ${gross_usd:,.2f}M")
    print(f"   Domestic Operating Costs:        ${domestic_costs:,.2f}M")
    print(f"   Expected Net Cash Flow:          ${expected_cf:,.2f}M")

    # 2. Portfolio Risk
    var_unhedged = portfolio_cash_flow_variance(exp_vector, cov_matrix)
    std_unhedged = math.sqrt(var_unhedged)

    print("\n2. Portfolio Variance & Risk (Unhedged):")
    print(f"   Cash Flow Variance:              {var_unhedged:.4f}")
    print(f"   Cash Flow Volatility:            ${std_unhedged:.2f}M")

    # 3. Minimum-variance hedge (80% across all currencies)
    hedged_weights = [x * 0.20 for x in exp_vector]
    var_hedged = portfolio_cash_flow_variance(hedged_weights, cov_matrix)
    std_hedged = math.sqrt(var_hedged)
    eff = evaluate_hedge_effectiveness(var_unhedged, var_hedged)

    print("\n3. Hedged Portfolio Risk (80% Cover Benchmark):")
    print(f"   Hedged Variance:                 {var_hedged:.4f}")
    print(f"   Hedged Volatility:               ${std_hedged:.2f}M")
    print(f"   Variance Reduction (R^2):        {eff:.2%}")

    # 4. CFaR & Hurdle
    hurdle = inst["hurdle_cash_flow"]
    cfar_un = compute_cfar(mean_cf=expected_cf, std_cf=std_unhedged, alpha=0.05, hurdle=hurdle)
    cfar_hd = compute_cfar(mean_cf=expected_cf, std_cf=std_hedged, alpha=0.05, hurdle=hurdle)

    print(f"\n4. Cash-Flow-at-Risk (Hurdle = ${hurdle:,.2f}M):")
    print(f"   Unhedged 95% CFaR:               ${cfar_un['cfar']:.2f}M")
    print(f"   Unhedged Worst 5% CF:            ${cfar_un['worst_case_cf']:.2f}M")
    print(f"   Unhedged Shortfall Risk:         {cfar_un['prob_shortfall']:.2%}")
    print(f"   Hedged 95% CFaR:                 ${cfar_hd['cfar']:.2f}M")
    print(f"   Hedged Worst 5% CF:              ${cfar_hd['worst_case_cf']:.2f}M")
    print(f"   Hedged Shortfall Risk:           {cfar_hd['prob_shortfall']:.4%}")

    # 5. Hedge Accounting
    ha = hedge_accounting_test(delta_derivative=inst["delta_derivative"], delta_exposure=inst["delta_exposure"])
    print("\n5. Hedge Accounting Compliance:")
    print(f"   Derivative Delta:                ${inst['delta_derivative']:,.2f}M")
    print(f"   Exposure Delta:                  ${inst['delta_exposure']:,.2f}M")
    print(f"   Dollar-Offset Ratio:             {float(ha['dollar_offset_ratio']):.2%}")
    print(f"   ASC 815 / IFRS 9 Qualified:      {ha['is_qualified']}")

    # 6. Cross-Border Project
    npv_f = cross_border_npv(
        initial_outlay_foreign=inst["initial_outlay_eur"],
        foreign_cfs=inst["project_cfs_eur"],
        spot_fx=spots["EUR"],
        wacc_home=inst["wacc_usd"],
        r_home=inst["r_usd"],
        r_foreign=inst["r_eur"],
        method="foreign",
    )
    npv_h = cross_border_npv(
        initial_outlay_foreign=inst["initial_outlay_eur"],
        foreign_cfs=inst["project_cfs_eur"],
        spot_fx=spots["EUR"],
        wacc_home=inst["wacc_usd"],
        r_home=inst["r_usd"],
        r_foreign=inst["r_eur"],
        method="home",
    )
    print("\n6. Cross-Border Project Valuation:")
    print(f"   Initial Outlay (EUR):            €{inst['initial_outlay_eur']:,.2f}M")
    print(f"   Cash Flows (EUR):                {inst['project_cfs_eur']}")
    print(f"   Project NPV (Foreign Method):    ${npv_f:,.2f}M")
    print(f"   Project NPV (Home Method):       ${npv_h:,.2f}M")
    print(f"   Valuation Equivalence:           {abs(npv_f - npv_h) < 1e-4}")


main()
