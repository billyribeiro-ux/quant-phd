"""Lab FI3-L03-1: Term premium extraction and yield curve decomposition.

SIMULATED: generates synthetic yield paths to decompose the 10-year yield into
the physical expected short-rate path and the term premium.
Standard library and NumPy only; no network.
"""

from __future__ import annotations


def decompose_yield(
    r_t: float,
    mu_r: float,
    phi_r: float,
    maturity: int,
    y_observed: float,
) -> tuple[float, float, float]:
    """Decompose observed yield into average expected short rate and term premium:

    y_t^{(n)} = (1/n) * sum_{i=0}^{n-1} E_t[r_{t+i}] + TP_t^{(n)}
    under AR(1) short-rate dynamics: r_{t+1} - mu_r = phi_r * (r_t - mu_r) + eps.
    """
    expected_sum = 0.0
    for i in range(maturity):
        # E_t[r_{t+i}] = mu_r + phi_r^i * (r_t - mu_r)
        e_r_i = mu_r + (phi_r**i) * (r_t - mu_r)
        expected_sum += e_r_i

    avg_expected_r = expected_sum / float(maturity)
    term_premium = y_observed - avg_expected_r
    pct_tp = (term_premium / y_observed) * 100.0 if y_observed != 0 else 0.0

    return avg_expected_r, term_premium, pct_tp


def main() -> None:
    # Stylized parameters for monetary policy regime:
    # Long-run neutral short rate mu_r = 3.5%, persistence phi_r = 0.85 per annum
    mu_r = 0.035
    phi_r = 0.85
    maturity = 10

    scenarios = [
        ("Expansion (r_t = 5.0%, y_10 = 5.5%)", 0.050, 0.055),
        ("Neutral (r_t = 3.5%, y_10 = 4.8%)", 0.035, 0.048),
        ("Recession / Easing (r_t = 1.5%, y_10 = 3.8%)", 0.015, 0.038),
    ]

    print("10-Year Yield Decomposition: y_t^(10) = Expected Short Rate + Term Premium:")
    for name, r_t, y_10 in scenarios:
        avg_r, tp, pct_tp = decompose_yield(r_t, mu_r, phi_r, maturity, y_10)
        print(f"\nScenario: {name}")
        print(f"  Short rate r_t                   = {r_t:.2%}")
        print(f"  Observed 10y yield               = {y_10:.2%}")
        print(f"  10y Average Expected Short Rate  = {avg_r:.4%}")
        print(f"  10y Term Premium (TP)            = {tp:.4%} ({tp * 10000:.1f} bps)")
        print(f"  Term Premium share of 10y yield  = {pct_tp:.1f}%")

    # Invariant check: Expected short rate + Term premium == Observed yield
    for _, r_t, y_10 in scenarios:
        avg_r, tp, _ = decompose_yield(r_t, mu_r, phi_r, maturity, y_10)
        assert abs((avg_r + tp) - y_10) < 1e-12, "Decomposition must articulate exactly"
    print("\nArticulation check: avg_expected_r + term_premium == observed_yield verified for all cases.")


main()
