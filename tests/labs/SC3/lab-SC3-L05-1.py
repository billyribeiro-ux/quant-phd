"""Lab 1 · The T-forward measure under stochastic Vasicek interest rates.

With stochastic interest rates, discounting exp(-int_0^T r_s ds) is correlated with terminal stock price S_T.
Under the risk-neutral measure Q, the option price is E^Q[exp(-int_0^T r_s ds) * (S_T - K)^+].
Under the T-forward measure Q^T (with zero-coupon bond P(t, T) as numeraire):
    V_0 = P(0, T) * E^{Q^T}[(F_T - K)^+]
where F_t = S_t / P(t, T) is a Q^T-martingale. In the Gaussian Vasicek model, the integrated forward volatility
v_F^2 is available analytically, yielding a closed-form Black-76 forward formula.
This lab simulates 10,000 coupled (r, S) paths under Q (SIMULATED) and verifies that the path-discounted
Monte Carlo price matches the analytical T-forward price within 2 standard errors.
"""

from __future__ import annotations

import math
import random


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def vasicek_bond(r0: float, kappa: float, theta: float, sig_r: float, tau: float) -> float:
    b = (1.0 - math.exp(-kappa * tau)) / kappa
    a = (theta - (sig_r**2) / (2.0 * (kappa**2))) * (b - tau) - ((sig_r**2) / (4.0 * kappa)) * (b**2)
    return math.exp(a - b * r0)


def forward_call_price(
    s0: float,
    k: float,
    r0: float,
    kappa: float,
    theta: float,
    sig_r: float,
    sig_s: float,
    rho: float,
    t: float,
) -> float:
    p0 = vasicek_bond(r0, kappa, theta, sig_r, t)
    f0 = s0 / p0

    # Integrated bond volatility components:
    # sigma_P(tau) = (sig_r / kappa) * (1 - exp(-kappa * tau))
    int_sig_p = (sig_r / kappa) * (t - (1.0 - math.exp(-kappa * t)) / kappa)
    int_sig_p2 = ((sig_r**2) / (kappa**2)) * (
        t - (2.0 / kappa) * (1.0 - math.exp(-kappa * t)) + (1.0 / (2.0 * kappa)) * (1.0 - math.exp(-2.0 * kappa * t))
    )
    vf2 = (sig_s**2) * t + int_sig_p2 - 2.0 * rho * sig_s * int_sig_p
    vf = math.sqrt(vf2)

    d1 = (math.log(f0 / k) + 0.5 * vf2) / vf
    d2 = d1 - vf
    return p0 * (f0 * norm_cdf(d1) - k * norm_cdf(d2))


def main() -> None:
    seed = 42
    r0 = 0.04
    kappa = 0.5
    theta = 0.05
    sig_r = 0.02
    s0 = 100.0
    k = 100.0
    sig_s = 0.20
    rho = 0.30
    t = 1.0

    p0 = vasicek_bond(r0, kappa, theta, sig_r, t)
    ana_price = forward_call_price(s0, k, r0, kappa, theta, sig_r, sig_s, rho, t)

    # Monte Carlo simulation under Q with pathwise discounting
    rng = random.Random(seed)
    n_steps = 50
    n_paths = 10000
    dt = t / n_steps
    sq_dt = math.sqrt(dt)

    payoffs: list[float] = []
    for _ in range(n_paths):
        r = r0
        s = s0
        int_r = 0.0
        for _ in range(n_steps):
            z1 = rng.gauss(0.0, 1.0)
            z2 = rng.gauss(0.0, 1.0)
            zr = z1
            zs = rho * z1 + math.sqrt(max(1.0 - rho**2, 0.0)) * z2

            int_r += r * dt
            r += kappa * (theta - r) * dt + sig_r * sq_dt * zr
            s *= math.exp((r - 0.5 * (sig_s**2)) * dt + sig_s * sq_dt * zs)

        payoffs.append(math.exp(-int_r) * max(s - k, 0.0))

    mc_price = sum(payoffs) / n_paths
    var_mc = sum((x - mc_price) ** 2 for x in payoffs) / (n_paths - 1)
    se_mc = math.sqrt(var_mc / n_paths)

    print(f"zero-coupon bond price P(0, T): {p0:.6f}")
    print(f"analytical T-forward call price: {ana_price:.4f}")
    print(f"path-discounted Q Monte Carlo price: {mc_price:.4f} (se {se_mc:.4f})")
    print(f"absolute difference: {abs(mc_price - ana_price):.4f}")
    print("MC inside 2*se band:", abs(mc_price - ana_price) <= 2.0 * se_mc)


main()
