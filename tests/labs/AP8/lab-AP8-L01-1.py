"""Lab AP8-L01-1: Equilibrium Degree of Inefficiency in the Grossman-Stiglitz / Pedersen Framework.

SIMULATED: Solves the competitive rational expectations equilibrium with costly information acquisition,
computing the equilibrium fraction of informed searchers lambda*(c), price informativeness,
and the resulting equilibrium degree of mispricing across information cost levels.
"""

from __future__ import annotations

import math


def solve_gs_equilibrium(
    c: float,
    gamma: float = 1.0,
    sigma_v2: float = 4.0,
    sigma_eps2: float = 1.0,
    sigma_x2: float = 1.0,
    tol: float = 1e-8,
    max_iter: int = 100,
) -> dict[str, float]:
    """Solve for equilibrium informed fraction lambda in [0, 1].

    In the classic CARA-normal setup (Grossman & Stiglitz 1980, Pedersen 2015):
    - Payoff v ~ N(mu_v, sigma_v^2)
    - Signal s = v + epsilon, epsilon ~ N(0, sigma_eps^2)
    - Noise trader supply shock x ~ N(0, sigma_x^2)
    - Research cost: c > 0
    - Risk aversion: gamma

    Indifference between informed and uninformed expected utility requires:
        Var(v | P(lambda)) / Var(v | s) = exp(2 * gamma * c)
    where:
        Var(v | s) = 1 / (1/sigma_v^2 + 1/sigma_eps^2)
        Var(v | P(lambda)) = 1 / (1/sigma_v^2 + h_P(lambda))
        h_P(lambda) = (lambda / (gamma * sigma_eps^2))^2 / sigma_x^2
    """
    prec_v = 1.0 / sigma_v2
    prec_eps = 1.0 / sigma_eps2
    prec_inf = prec_v + prec_eps
    var_inf = 1.0 / prec_inf

    target_ratio = math.exp(2.0 * gamma * c)

    def var_uninformed(lam: float) -> float:
        if lam <= 1e-12:
            return sigma_v2
        h_p = ((lam / (gamma * sigma_eps2)) ** 2) / sigma_x2
        return 1.0 / (prec_v + h_p)

    ratio_0 = var_uninformed(0.0) / var_inf
    ratio_1 = var_uninformed(1.0) / var_inf

    if ratio_0 <= target_ratio:
        lam_star = 0.0
    elif ratio_1 >= target_ratio:
        lam_star = 1.0
    else:
        lo = 0.0
        hi = 1.0
        for _ in range(max_iter):
            mid = 0.5 * (lo + hi)
            cur_ratio = var_uninformed(mid) / var_inf
            if abs(cur_ratio - target_ratio) < tol:
                break
            if cur_ratio > target_ratio:
                lo = mid
            else:
                hi = mid
        lam_star = 0.5 * (lo + hi)

    var_uninf = var_uninformed(lam_star)
    # Informativeness: percentage reduction in payoff variance from market price
    informativeness = 1.0 - (var_uninf / sigma_v2)
    # Mispricing standard deviation
    mispricing_std = math.sqrt(var_uninf)

    return {
        "cost": c,
        "lambda_star": lam_star,
        "var_uninformed": var_uninf,
        "informativeness": informativeness,
        "mispricing_std": mispricing_std,
    }


def main() -> None:
    costs = [0.05, 0.15, 0.30, 0.50, 0.70]
    print("================================================================================")
    print("GROSSMAN-STIGLITZ & PEDERSEN EQUILIBRIUM: COSTLY INFORMATION & MARKET EFFICIENCY")
    print("================================================================================")
    print(f"{'Cost (c)':>10} | {'Informed (λ*)':>14} | {'Price Info':>12} | {'Mispricing Std':>16}")
    print("-" * 62)

    for c in costs:
        res = solve_gs_equilibrium(c=c)
        print(
            f"{res['cost']:10.2f} | "
            f"{res['lambda_star']:14.4f} | "
            f"{res['informativeness'] * 100:11.2f}% | "
            f"{res['mispricing_std']:16.4f}"
        )

    print("-" * 62)
    print("Equilibrium Condition: Expected Utility(Informed) == Expected Utility(Uninformed)")
    print("Key Finding: As information cost c rises, equilibrium informed capital λ* falls,")
    print("price informativeness deteriorates, and the equilibrium degree of inefficiency rises.")


main()
