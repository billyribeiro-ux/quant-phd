"""Lab X2-project-2: Rung 2 completion problem for currency factor replication.

SIMULATED: generates sample carry portfolio returns and factor matrices.
On the project page, the core factor and pricing lines are blanked:
dol_factor = ___
hml_factor = ___
lambda_premia = ___
pricing_errors = ___
The twin contains the complete solution.
"""

from __future__ import annotations

from typing import Any


def compute_factors_and_pricing(
    portfolio_returns: list[list[float]],
) -> dict[str, Any]:
    """Compute Dollar factor, HML-FX factor, and cross-sectional pricing errors."""
    t_obs = len(portfolio_returns)
    k_ports = len(portfolio_returns[0])

    # 1. Compute Dollar factor: unweighted mean across all K portfolios
    dol_factor = [sum(portfolio_returns[t]) / k_ports for t in range(t_obs)]

    # 2. Compute HML-FX factor: Portfolio K (highest carry) minus Portfolio 1 (lowest carry)
    hml_factor = [portfolio_returns[t][-1] - portfolio_returns[t][0] for t in range(t_obs)]

    # 3. Time-series regression: estimate betas for each portfolio
    # Design matrix: [DOL, HML]
    mean_excess_returns = [sum(portfolio_returns[t][k] for t in range(t_obs)) / t_obs for k in range(k_ports)]
    mean_dol = sum(dol_factor) / t_obs
    mean_hml = sum(hml_factor) / t_obs

    s_dd = sum((d - mean_dol) ** 2 for d in dol_factor)
    s_hh = sum((h - mean_hml) ** 2 for h in hml_factor)
    s_dh = sum((dol_factor[t] - mean_dol) * (hml_factor[t] - mean_hml) for t in range(t_obs))
    det_f = s_dd * s_hh - s_dh * s_dh

    betas: list[list[float]] = []
    for k in range(k_ports):
        yk = [portfolio_returns[t][k] for t in range(t_obs)]
        myk = sum(yk) / t_obs
        s_yd = sum((yk[t] - myk) * (dol_factor[t] - mean_dol) for t in range(t_obs))
        s_yh = sum((yk[t] - myk) * (hml_factor[t] - mean_hml) for t in range(t_obs))
        b_dol = (s_hh * s_yd - s_dh * s_yh) / det_f
        b_hml = (s_dd * s_yh - s_dh * s_yd) / det_f
        betas.append([b_dol, b_hml])

    # 4. Cross-sectional regression: bar{R}_k = lambda_DOL * beta_{k,DOL} + lambda_HML * beta_{k,HML}
    b11 = sum(b[0] ** 2 for b in betas)
    b22 = sum(b[1] ** 2 for b in betas)
    b12 = sum(b[0] * b[1] for b in betas)
    br1 = sum(b[0] * r for b, r in zip(betas, mean_excess_returns, strict=True))
    br2 = sum(b[1] * r for b, r in zip(betas, mean_excess_returns, strict=True))
    det_b = b11 * b22 - b12 * b12

    lam_dol = (b22 * br1 - b12 * br2) / det_b
    lam_hml = (b11 * br2 - b12 * br1) / det_b
    lambda_premia = [round(lam_dol, 6), round(lam_hml, 6)]

    # 5. Pricing errors: alpha_k = bar{R}_k - (lambda_DOL * beta_{k,DOL} + lambda_HML * beta_{k,HML})
    pricing_errors = [
        round(r - (lam_dol * b[0] + lam_hml * b[1]), 6) for r, b in zip(mean_excess_returns, betas, strict=True)
    ]
    mape = sum(abs(a) for a in pricing_errors) / k_ports

    return {
        "dol_mean_ann": round(mean_dol * 12.0 * 100, 2),
        "hml_mean_ann": round(mean_hml * 12.0 * 100, 2),
        "lambda_premia": lambda_premia,
        "pricing_errors": pricing_errors,
        "mape_ann": round(mape * 12.0 * 100, 3),
    }


def main() -> None:
    print("Lab X2-project-2 | Currency Factor Replication (Rung 2 Completion Problem)")
    print("-------------------------------------------------------------------------")

    # Sample 5-portfolio returns over 10 periods
    port_rets = [
        [-0.005, -0.002, 0.001, 0.004, 0.008],
        [0.010, 0.012, 0.015, 0.018, 0.022],
        [-0.015, -0.010, -0.005, 0.000, 0.005],
        [0.002, 0.004, 0.006, 0.008, 0.011],
        [-0.008, -0.004, -0.001, 0.003, 0.007],
        [0.005, 0.007, 0.010, 0.012, 0.016],
        [-0.012, -0.008, -0.004, 0.001, 0.006],
        [0.008, 0.011, 0.014, 0.017, 0.021],
        [-0.003, -0.001, 0.002, 0.005, 0.009],
        [0.004, 0.006, 0.009, 0.011, 0.015],
    ]

    res = compute_factors_and_pricing(port_rets)
    print(f"Annualized Dollar Factor Mean:  {res['dol_mean_ann']}%")
    print(f"Annualized HML-FX Factor Mean:  {res['hml_mean_ann']}%")
    print(f"Estimated Factor Premia lambda: {res['lambda_premia']}")
    print(f"Pricing Errors alpha:           {res['pricing_errors']}")
    print(f"Mean Absolute Pricing Error:    {res['mape_ann']}% ann")


main()
