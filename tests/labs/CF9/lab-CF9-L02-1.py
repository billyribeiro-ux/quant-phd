"""CF9 lab L02-1: Froot-Scharfstein-Stein (1993) Model and Minimum-Variance Hedge Ratio.

Simulates the Froot, Scharfstein & Stein (1993) framework:
1. Concave investment returns F(I) and convex external financing cost C(e).
2. Proves that costly external finance induces endogenous corporate risk aversion (V''(w) < 0).
3. Demonstrates underinvestment when internal funds drop.
4. Computes the analytical minimum-variance hedge ratio h* = Cov(w, f) / Var(f).
5. Shows that hedging internal cash flow restores optimal investment and increases expected value.
Standard library only; deterministic execution.
"""

from __future__ import annotations

import math
from statistics import NormalDist


def production_function(investment: float, a: float = 20.0, alpha: float = 0.5) -> float:
    """Concave output function: F(I) = a * I^alpha."""
    if investment <= 0.0:
        return 0.0
    return float(a * (investment**alpha))


def external_financing_cost(external_funds: float, lambda_cost: float = 0.05) -> float:
    """Convex deadweight cost of external finance: C(e) = lambda * e^2 for e > 0, 0 otherwise."""
    if external_funds <= 0.0:
        return 0.0
    return lambda_cost * (external_funds**2)


def solve_optimal_investment(
    internal_cash: float, a: float = 20.0, alpha: float = 0.5, lambda_cost: float = 0.05
) -> dict[str, float]:
    """Find optimal investment I* that maximizes Net Value = F(I) - I - C(I - internal_cash)."""
    # First-best unconstrained investment where F'(I_fb) = 1
    i_fb = (alpha * a) ** (1.0 / (1.0 - alpha))
    if internal_cash >= i_fb:
        net_val = production_function(i_fb, a, alpha) - i_fb
        return {"investment": i_fb, "external_funds": 0.0, "net_value": net_val}

    # Bisection search on [internal_cash, i_fb] for F'(I) - 1 - 2*lambda*(I - internal_cash) = 0
    low = max(0.01, internal_cash)
    high = i_fb
    for _ in range(40):
        mid = (low + high) / 2.0
        f_prime = alpha * a * (mid ** (alpha - 1.0))
        g = f_prime - 1.0 - 2.0 * lambda_cost * (mid - internal_cash)
        if g > 0.0:
            low = mid
        else:
            high = mid

    best_i = (low + high) / 2.0
    e_star = max(0.0, best_i - internal_cash)
    output = production_function(best_i, a, alpha)
    cost = best_i + external_financing_cost(e_star, lambda_cost)
    return {
        "investment": best_i,
        "external_funds": e_star,
        "net_value": output - cost,
    }


def simulate_fss_hedging(
    w_bar: float = 25.0,
    sigma_w: float = 12.0,
    sigma_f: float = 15.0,
    rho_wf: float = 0.85,
    n_states: int = 2000,
) -> dict[str, float]:
    """Simulate unhedged vs minimum-variance hedged internal cash flows and corporate investment."""
    dist = NormalDist()
    p1 = [(i + 0.5) / n_states for i in range(n_states)]
    p2 = [((i * 137) % n_states + 0.5) / n_states for i in range(n_states)]

    z1 = [dist.inv_cdf(p) for p in p1]
    z2_raw = [dist.inv_cdf(p) for p in p2]

    # Gram-Schmidt orthogonalization for exact independence
    dot12 = sum(a * b for a, b in zip(z1, z2_raw, strict=True))
    dot11 = sum(a * a for a in z1)
    z2_ortho = [b - (dot12 / dot11) * a for a, b in zip(z1, z2_raw, strict=True)]
    scale2 = math.sqrt(dot11 / sum(b * b for b in z2_ortho))
    z2 = [b * scale2 for b in z2_ortho]

    cov_wf = rho_wf * sigma_w * sigma_f
    var_f = sigma_f**2
    h_star = cov_wf / var_f  # Minimum-variance hedge ratio

    sqrt_factor = math.sqrt(max(0.0, 1.0 - rho_wf**2))

    f_shocks = [sigma_f * s1 for s1 in z1]
    w_shocks = [sigma_w * (rho_wf * s1 + sqrt_factor * s2) for s1, s2 in zip(z1, z2, strict=True)]

    w_unhedged = [max(1.0, w_bar + w) for w in w_shocks]
    w_hedged = [max(1.0, w_bar + w - h_star * f) for w, f in zip(w_shocks, f_shocks, strict=True)]

    vals_unhedged = [solve_optimal_investment(w)["net_value"] for w in w_unhedged]
    vals_hedged = [solve_optimal_investment(w)["net_value"] for w in w_hedged]
    inv_unhedged = [solve_optimal_investment(w)["investment"] for w in w_unhedged]
    inv_hedged = [solve_optimal_investment(w)["investment"] for w in w_hedged]

    mean_val_unhedged = sum(vals_unhedged) / n_states
    mean_val_hedged = sum(vals_hedged) / n_states
    fss_value_gain = mean_val_hedged - mean_val_unhedged

    var_w_unhedged = sum((w - w_bar) ** 2 for w in w_unhedged) / n_states
    mean_w_hedged = sum(w_hedged) / n_states
    var_w_hedged = sum((w - mean_w_hedged) ** 2 for w in w_hedged) / n_states
    var_reduction = 1.0 - (var_w_hedged / var_w_unhedged)

    return {
        "h_star": h_star,
        "cov_wf": cov_wf,
        "var_f": var_f,
        "var_w_unhedged": var_w_unhedged,
        "var_w_hedged": var_w_hedged,
        "var_reduction": var_reduction,
        "mean_val_unhedged": mean_val_unhedged,
        "mean_val_hedged": mean_val_hedged,
        "fss_value_gain": fss_value_gain,
        "mean_inv_unhedged": sum(inv_unhedged) / n_states,
        "mean_inv_hedged": sum(inv_hedged) / n_states,
    }


def main() -> None:
    print("CF9 Lab L02-1: Froot-Scharfstein-Stein (1993) Optimal Hedging")
    print("===========================================================")

    # Demonstrate concavity of firm value in internal cash flow w
    w_low = 10.0
    w_mid = 25.0
    w_high = 40.0
    res_low = solve_optimal_investment(w_low)
    res_mid = solve_optimal_investment(w_mid)
    res_high = solve_optimal_investment(w_high)

    print("1. Costly External Finance and Endogenous Risk Aversion (V''(w) < 0):")
    print(
        f"   Low internal funds  (w = ${w_low:.1f}M): Inv = ${res_low['investment']:.2f}M, "
        f"Ext = ${res_low['external_funds']:.2f}M, Net Val = ${res_low['net_value']:.2f}M"
    )
    print(
        f"   Mid internal funds  (w = ${w_mid:.1f}M): Inv = ${res_mid['investment']:.2f}M, "
        f"Ext = ${res_mid['external_funds']:.2f}M, Net Val = ${res_mid['net_value']:.2f}M"
    )
    print(
        f"   High internal funds (w = ${w_high:.1f}M): Inv = ${res_high['investment']:.2f}M, "
        f"Ext = ${res_high['external_funds']:.2f}M, Net Val = ${res_high['net_value']:.2f}M"
    )

    mv_low = (res_mid["net_value"] - res_low["net_value"]) / (w_mid - w_low)
    mv_high = (res_high["net_value"] - res_mid["net_value"]) / (w_high - w_mid)
    print(f"   Marginal value of cash (low to mid): {mv_low:.4f}")
    print(f"   Marginal value of cash (mid to high):{mv_high:.4f}")
    print(f"   Concavity confirmed (V''(w) < 0):    {mv_low > mv_high} (Diminishing marginal value)")

    sim = simulate_fss_hedging()
    print("\n2. Minimum-Variance Hedge Ratio & Cash Flow Stabilization:")
    print(f"   Covariance Cov(w, f):     {sim['cov_wf']:.2f}")
    print(f"   Futures variance Var(f):  {sim['var_f']:.2f}")
    print(f"   Optimal hedge ratio h*:   {sim['h_star']:.4f}")
    print(f"   Unhedged cash flow Var(w):{sim['var_w_unhedged']:.2f}")
    print(f"   Hedged cash flow Var(w):  {sim['var_w_hedged']:.2f}")
    print(f"   Variance reduction (R^2): {sim['var_reduction']:.2%}")

    print("\n3. Expected Investment and Value Creation:")
    print(f"   Mean investment unhedged: ${sim['mean_inv_unhedged']:.2f}M")
    print(f"   Mean investment hedged:   ${sim['mean_inv_hedged']:.2f}M")
    print(f"   Unhedged expected value:  ${sim['mean_val_unhedged']:.2f}M")
    print(f"   Hedged expected value:    ${sim['mean_val_hedged']:.2f}M")
    pct_val_gain = sim["fss_value_gain"] / sim["mean_val_unhedged"]
    print(f"   FSS Hedging Value Added:  ${sim['fss_value_gain']:.2f}M ({pct_val_gain:.2%})")


main()
