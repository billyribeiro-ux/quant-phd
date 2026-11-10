"""Mutant 4: Relaxes hedge accounting corridor from [0.80, 1.25] to [0.70, 1.30]."""

from __future__ import annotations

import math
from statistics import NormalDist


def compute_net_transaction_exposure(
    receivables: dict[str, float], payables: dict[str, float]
) -> dict[str, float]:
    """Calculate net contractual foreign currency exposure: Net = Receivables - Payables."""
    if not receivables or not payables:
        raise ValueError("Receivables and payables dictionaries cannot be empty.")
    if set(receivables.keys()) != set(payables.keys()):
        raise ValueError("Currency keys in receivables and payables must match exactly.")

    net: dict[str, float] = {}
    for c, rec in receivables.items():
        if rec < 0.0 or payables[c] < 0.0:
            raise ValueError(f"Receivables and payables for {c} must be non-negative.")
        net[c] = round(rec - payables[c], 6)
    return net


def compute_usd_exposure(
    net_exposure_fc: dict[str, float], spot_rates: dict[str, float]
) -> dict[str, float]:
    """Convert net foreign exposures into USD values: USD_exp = Net_FC * Spot_Rate."""
    if not net_exposure_fc or not spot_rates:
        raise ValueError("Exposures and spot rates cannot be empty.")
    if set(net_exposure_fc.keys()) != set(spot_rates.keys()):
        raise ValueError("Currency keys in net exposures and spot rates must match.")

    usd_exp: dict[str, float] = {}
    for c, net in net_exposure_fc.items():
        s = spot_rates[c]
        if s <= 0.0:
            raise ValueError(f"Spot exchange rate for {c} must be strictly positive.")
        usd_exp[c] = round(net * s, 6)
    return usd_exp


def minimum_variance_hedge_ratio(cov_cf_f: float, var_f: float) -> float:
    """Calculate minimum-variance hedge ratio: h* = Cov(Delta CF, Delta F) / Var(Delta F)."""
    if var_f <= 0.0:
        raise ValueError("Variance of hedging instrument must be strictly positive.")
    return cov_cf_f / var_f


def portfolio_cash_flow_variance(
    usd_exposures: list[float], cov_matrix: list[list[float]]
) -> float:
    """Calculate total portfolio cash flow variance: Var(CF) = w^T * Sigma * w."""
    n = len(usd_exposures)
    if n == 0:
        raise ValueError("Exposures list cannot be empty.")
    if len(cov_matrix) != n or any(len(row) != n for row in cov_matrix):
        raise ValueError("Covariance matrix dimensions must match number of exposures.")

    total_var = 0.0
    for i in range(n):
        for j in range(n):
            total_var += usd_exposures[i] * usd_exposures[j] * cov_matrix[i][j]

    if total_var < -1e-9:
        raise ValueError("Computed portfolio variance cannot be negative.")
    return max(0.0, total_var)


def compute_cfar(
    mean_cf: float,
    std_cf: float,
    alpha: float = 0.05,
    hurdle: float | None = None,
) -> dict[str, float]:
    """Compute analytical Cash-Flow-at-Risk at confidence level 1 - alpha."""
    if std_cf < 0.0:
        raise ValueError("Cash flow standard deviation must be non-negative.")
    if not (0.0 < alpha < 0.5):
        raise ValueError("Significance level alpha must be strictly between 0 and 0.5.")

    dist = NormalDist()
    z_alpha = dist.inv_cdf(1.0 - alpha)
    cfar_amount = z_alpha * std_cf
    worst_case_cf = mean_cf - cfar_amount

    prob_shortfall = 0.0
    if hurdle is not None:
        if std_cf > 1e-12:
            z_hurdle = (hurdle - mean_cf) / std_cf
            prob_shortfall = dist.cdf(z_hurdle)
        else:
            prob_shortfall = 1.0 if mean_cf < hurdle else 0.0

    return {
        "cfar": cfar_amount,
        "worst_case_cf": worst_case_cf,
        "prob_shortfall": prob_shortfall,
    }


def evaluate_hedge_effectiveness(var_unhedged: float, var_hedged: float) -> float:
    """Calculate variance reduction effectiveness: HE = 1 - (Var_hedged / Var_unhedged)."""
    if var_unhedged <= 0.0:
        raise ValueError("Unhedged variance must be strictly positive.")
    if var_hedged < 0.0:
        raise ValueError("Hedged variance cannot be negative.")

    he = 1.0 - (var_hedged / var_unhedged)
    return max(0.0, min(1.0, he))


def hedge_accounting_test(
    delta_derivative: float, delta_exposure: float
) -> dict[str, float | bool]:
    """Test retrospective dollar-offset ratio - MUTATED: uses incorrect bounds 0.70 to 1.30."""
    if abs(delta_exposure) < 1e-9:
        raise ValueError("Delta exposure change cannot be zero.")

    ratio = abs(delta_derivative) / abs(delta_exposure)
    # MUTANT ERROR: relaxed corridor [0.70, 1.30] violates ASC 815 / IFRS 9 rule [0.80, 1.25]
    qualified = 0.70 <= ratio <= 1.30

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
    """Compute cross-border project NPV in base currency ($USD)."""
    if spot_fx <= 0.0:
        raise ValueError("Spot exchange rate must be strictly positive.")
    if wacc_home <= -1.0 or r_home <= -1.0 or r_foreign <= -1.0:
        raise ValueError("Discount and interest rates must be greater than -1.0.")
    if method not in ("foreign", "home"):
        raise ValueError("Method must be either 'foreign' or 'home'.")

    wacc_foreign = ((1.0 + wacc_home) * (1.0 + r_foreign) / (1.0 + r_home)) - 1.0

    if method == "foreign":
        pv_fc = sum(cf / ((1.0 + wacc_foreign) ** (t + 1)) for t, cf in enumerate(foreign_cfs))
        npv_fc = -initial_outlay_foreign + pv_fc
        return npv_fc * spot_fx

    forward_rates = [
        spot_fx * (((1.0 + r_home) / (1.0 + r_foreign)) ** (t + 1))
        for t in range(len(foreign_cfs))
    ]
    cfs_home = [cf * fwd for cf, fwd in zip(foreign_cfs, forward_rates, strict=True)]
    initial_outlay_home = initial_outlay_foreign * spot_fx

    pv_home = sum(cf / ((1.0 + wacc_home) ** (t + 1)) for t, cf in enumerate(cfs_home))
    return -initial_outlay_home + pv_home
