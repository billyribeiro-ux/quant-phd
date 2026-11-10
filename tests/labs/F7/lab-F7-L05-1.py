"""Lab F7-L05-1: Fung-Hsieh Nonlinear Payoff Detection and Option-Adjusted Alpha.

Demonstrates how nonlinear option-like strategies (trend-following straddles vs.
systematic put writing) distort classical linear CAPM alpha. Implements the
Treynor-Mazuy / Fung-Hsieh quadratic payoff model to extract option convexity
gamma and recover option-adjusted alpha.
"""

from __future__ import annotations

import numpy as np


def run_nonlinear_payoff_analysis(seed: int = 42) -> dict[str, float]:
    """Evaluate linear vs nonlinear option-like payoffs for two alternative managers."""
    rng = np.random.default_rng(seed)
    n_months = 180  # 15 years

    # 1. Market excess return (mean = 0.70% / mo, vol = 4.5% / mo)
    mkt = rng.normal(0.0070, 0.0450, size=n_months)
    mkt_demeaned_sq = (mkt - np.mean(mkt)) ** 2

    # 2. Simulate Manager A: Trend Follower / CTA (Convex Payoff / Long Straddle)
    # Generates convex gains in extreme market moves, true alpha = 0.20% / mo
    gamma_cta_true = 4.50
    alpha_cta_true = 0.0020
    r_cta = alpha_cta_true + 0.10 * mkt + gamma_cta_true * mkt_demeaned_sq + rng.normal(0.0, 0.020, size=n_months)

    # 3. Simulate Manager B: Systematic Put Seller / Carry (Concave Payoff / Short Volatility)
    # Collects regular option premium (1.10% / mo) but suffers in large market moves (-5.50 * mkt^2).
    # True skill alpha is zero!
    gamma_put_true = -5.50
    premium_put = 0.0110
    alpha_put_true = 0.0000
    r_put = (
        alpha_put_true
        + premium_put
        + 0.40 * mkt
        + gamma_put_true * mkt_demeaned_sq
        + rng.normal(0.0, 0.015, size=n_months)
    )

    # Regression helper
    def estimate_regressions(
        r_series: np.ndarray,
    ) -> tuple[float, float, float, float, float]:
        ones = np.ones((n_months, 1))

        # (a) Linear CAPM regression: r = alpha + beta * mkt
        x_lin = np.column_stack([ones, mkt])
        b_lin = np.linalg.lstsq(x_lin, r_series, rcond=None)[0]
        e_lin = r_series - x_lin @ b_lin
        s2_lin = float(np.sum(e_lin**2) / (n_months - 2))
        se_lin = np.sqrt(np.diag(np.linalg.inv(x_lin.T @ x_lin) * s2_lin))
        alpha_lin_ann = float(b_lin[0] * 12.0 * 100.0)
        t_alpha_lin = float(b_lin[0] / se_lin[0])

        # (b) Quadratic Treynor-Mazuy / Fung-Hsieh: r = alpha* + beta * mkt + gamma * mkt^2
        x_quad = np.column_stack([ones, mkt, mkt_demeaned_sq])
        b_quad = np.linalg.lstsq(x_quad, r_series, rcond=None)[0]
        e_quad = r_series - x_quad @ b_quad
        s2_quad = float(np.sum(e_quad**2) / (n_months - 3))
        se_quad = np.sqrt(np.diag(np.linalg.inv(x_quad.T @ x_quad) * s2_quad))
        alpha_quad_ann = float(b_quad[0] * 12.0 * 100.0)
        gamma_hat = float(b_quad[2])
        t_gamma = float(b_quad[2] / se_quad[2])

        return alpha_lin_ann, t_alpha_lin, alpha_quad_ann, gamma_hat, t_gamma

    (
        cta_a_lin,
        cta_t_lin,
        cta_a_quad,
        cta_gamma,
        cta_t_gamma,
    ) = estimate_regressions(r_cta)

    (
        put_a_lin,
        put_t_lin,
        put_a_quad,
        put_gamma,
        put_t_gamma,
    ) = estimate_regressions(r_put)

    return {
        "cta_alpha_lin": round(cta_a_lin, 2),
        "cta_t_lin": round(cta_t_lin, 2),
        "cta_alpha_quad": round(cta_a_quad, 2),
        "cta_gamma": round(cta_gamma, 2),
        "cta_t_gamma": round(cta_t_gamma, 2),
        "put_alpha_lin": round(put_a_lin, 2),
        "put_t_lin": round(put_t_lin, 2),
        "put_alpha_quad": round(put_a_quad, 2),
        "put_gamma": round(put_gamma, 2),
        "put_t_gamma": round(put_t_gamma, 2),
    }


def main() -> None:
    print("Lab F7-L05-1 | Fung-Hsieh Nonlinear Payoff Detection")
    print("-----------------------------------------------------")
    res = run_nonlinear_payoff_analysis(seed=42)
    print("Manager A (Trend Follower / CTA):")
    print(f"  Linear CAPM Alpha:         {res['cta_alpha_lin']:+.2f}% / yr (t = {res['cta_t_lin']:+.2f})")
    print(f"  Quadratic Convexity gamma: {res['cta_gamma']:+.2f} (t = {res['cta_t_gamma']:+.2f}) -> Convexity")
    print(f"  Option-Adjusted Alpha:     {res['cta_alpha_quad']:+.2f}% / yr")
    print("Manager B (Put Seller / Short Volatility):")
    print(f"  Linear CAPM Alpha:         {res['put_alpha_lin']:+.2f}% / yr (t = {res['put_t_lin']:+.2f}) -> 'Alpha'")
    print(f"  Quadratic Concavity gamma: {res['put_gamma']:+.2f} (t = {res['put_t_gamma']:+.2f}) -> Negative Gamma")
    print(f"  Zero-Vol Regime Intercept: {res['put_alpha_quad']:+.2f}% / yr (Unhedged option premium)")


main()
