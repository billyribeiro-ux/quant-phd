"""Reference solution for SC3: Numeraire Toolkit.

Implements the Margrabe exchange option formula, 2D Monte Carlo verification,
the quanto European call formula with foreign drift adjustment, and invariance
consistency checks.
"""

from __future__ import annotations

import math
import random
from typing import Any


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def margrabe_price(
    s1: float,
    s2: float,
    sig1: float,
    sig2: float,
    rho: float,
    q1: float,
    q2: float,
    t: float,
) -> float:
    """Compute the closed-form Margrabe exchange option price max(S_1(T) - S_2(T), 0).

    Uses asset 2 as numeraire, under which relative volatility is
    sigma_M = sqrt(sig1^2 - 2*rho*sig1*sig2 + sig2^2).
    """
    if s1 <= 0.0 or s2 <= 0.0:
        raise ValueError("Asset prices must be strictly positive.")
    if sig1 <= 0.0 or sig2 <= 0.0:
        raise ValueError("Volatilities must be strictly positive.")
    if t <= 0.0:
        raise ValueError("Maturity must be strictly positive.")
    if not -1.0 <= rho <= 1.0:
        raise ValueError("Correlation rho must lie in [-1, 1].")

    sig_m = math.sqrt(max(sig1**2 - 2.0 * rho * sig1 * sig2 + sig2**2, 0.0))
    f1 = s1 * math.exp(-q1 * t)
    f2 = s2 * math.exp(-q2 * t)

    if sig_m <= 1e-12:
        return max(f1 - f2, 0.0)

    sq_t = math.sqrt(t)
    d1 = (math.log(f1 / f2) + 0.5 * (sig_m**2) * t) / (sig_m * sq_t)
    d2 = d1 - sig_m * sq_t
    return f1 * norm_cdf(d1) - f2 * norm_cdf(d2)


def margrabe_mc(
    s1: float,
    s2: float,
    sig1: float,
    sig2: float,
    rho: float,
    q1: float,
    q2: float,
    t: float,
    r: float,
    n_paths: int,
    seed: int,
) -> tuple[float, float]:
    """Estimate the Margrabe exchange option price and standard error via bivariate Monte Carlo."""
    if s1 <= 0.0 or s2 <= 0.0 or sig1 <= 0.0 or sig2 <= 0.0 or t <= 0.0:
        raise ValueError("Invalid continuous parameters.")
    if not -1.0 <= rho <= 1.0:
        raise ValueError("Correlation rho must lie in [-1, 1].")
    if n_paths < 2:
        raise ValueError("Path count n_paths must be at least 2.")

    rng = random.Random(seed)
    sq_t = math.sqrt(t)
    drift1 = (r - q1 - 0.5 * (sig1**2)) * t
    vol1 = sig1 * sq_t
    drift2 = (r - q2 - 0.5 * (sig2**2)) * t
    vol2 = sig2 * sq_t
    df = math.exp(-r * t)
    rho_perp = math.sqrt(max(1.0 - rho**2, 0.0))

    payoffs: list[float] = []
    for _ in range(n_paths):
        z1 = rng.gauss(0.0, 1.0)
        z2 = rng.gauss(0.0, 1.0)
        w1 = z1
        w2 = rho * z1 + rho_perp * z2

        s1_t = s1 * math.exp(drift1 + vol1 * w1)
        s2_t = s2 * math.exp(drift2 + vol2 * w2)
        payoffs.append(df * max(s1_t - s2_t, 0.0))

    mean = sum(payoffs) / n_paths
    var = sum((x - mean) ** 2 for x in payoffs) / (n_paths - 1)
    se = math.sqrt(var / n_paths)
    return mean, se


def quanto_call_price(
    s_f: float,
    k: float,
    r_d: float,
    r_f: float,
    sig_s: float,
    sig_x: float,
    rho: float,
    t: float,
) -> float:
    """Compute the closed-form quanto European call price with payoff max(S^f_T - K, 0) in domestic currency.

    Under the domestic risk-neutral measure Q^d, the foreign asset drift is shifted to:
        r_f - rho * sig_s * sig_x.
    """
    if s_f <= 0.0 or k <= 0.0:
        raise ValueError("Asset price and strike must be strictly positive.")
    if sig_s <= 0.0 or sig_x <= 0.0:
        raise ValueError("Volatilities must be strictly positive.")
    if t <= 0.0:
        raise ValueError("Maturity must be strictly positive.")
    if not -1.0 <= rho <= 1.0:
        raise ValueError("Correlation rho must lie in [-1, 1].")

    drift_adj = r_f - rho * sig_s * sig_x
    f_q = s_f * math.exp(drift_adj * t)
    sq_t = math.sqrt(t)
    d1 = (math.log(f_q / k) + 0.5 * (sig_s**2) * t) / (sig_s * sq_t)
    d2 = d1 - sig_s * sq_t
    return math.exp(-r_d * t) * (f_q * norm_cdf(d1) - k * norm_cdf(d2))


def quanto_call_mc(
    s_f: float,
    x0: float,
    k: float,
    r_d: float,
    r_f: float,
    sig_s: float,
    sig_x: float,
    rho: float,
    t: float,
    n_paths: int,
    seed: int,
) -> tuple[float, float]:
    """Estimate the quanto call price and standard error via Monte Carlo under domestic measure Q^d."""
    if s_f <= 0.0 or k <= 0.0 or sig_s <= 0.0 or sig_x <= 0.0 or t <= 0.0:
        raise ValueError("Invalid continuous parameters.")
    if not -1.0 <= rho <= 1.0:
        raise ValueError("Correlation rho must lie in [-1, 1].")
    if n_paths < 2:
        raise ValueError("Path count n_paths must be at least 2.")

    drift_qd = (r_f - rho * sig_s * sig_x - 0.5 * (sig_s**2)) * t
    vol_qd = sig_s * math.sqrt(t)
    df = math.exp(-r_d * t)
    rng = random.Random(seed)

    payoffs: list[float] = []
    for _ in range(n_paths):
        z = rng.gauss(0.0, 1.0)
        sf_t = s_f * math.exp(drift_qd + vol_qd * z)
        payoffs.append(df * max(sf_t - k, 0.0))

    mean = sum(payoffs) / n_paths
    var = sum((x - mean) ** 2 for x in payoffs) / (n_paths - 1)
    se = math.sqrt(var / n_paths)
    return mean, se


def verify_invariance(instance: dict[str, Any]) -> dict[str, Any]:
    """Verify numeraire invariance, homogeneity, exchange parity, and simulation concordance."""
    s1 = float(instance["s1"])
    s2 = float(instance["s2"])
    sig1 = float(instance["sig1"])
    sig2 = float(instance["sig2"])
    rho = float(instance["rho"])
    q1 = float(instance["q1"])
    q2 = float(instance["q2"])
    t = float(instance["t"])
    r = float(instance["r"])

    s_f = float(instance["s_f"])
    x0 = float(instance["x0"])
    k_quanto = float(instance["k_quanto"])
    r_d = float(instance["r_d"])
    r_f = float(instance["r_f"])
    sig_s = float(instance["sig_s"])
    sig_x = float(instance["sig_x"])
    rho_sx = float(instance["rho_sx"])
    n_paths = int(instance["n_paths"])
    seed = int(instance["seed"])

    # 1. Margrabe closed-form and MC
    m_price = margrabe_price(s1, s2, sig1, sig2, rho, q1, q2, t)
    m_mc, m_se = margrabe_mc(s1, s2, sig1, sig2, rho, q1, q2, t, r, n_paths, seed)

    # 2. Homogeneity of degree 1 (scale 2.0)
    scaled_price = margrabe_price(2.0 * s1, 2.0 * s2, sig1, sig2, rho, q1, q2, t)
    homogeneity_error = abs(scaled_price - 2.0 * m_price)

    # 3. Put-call exchange parity: Call(S1, S2) - Call(S2, S1) = F1 - F2
    rev_price = margrabe_price(s2, s1, sig2, sig1, rho, q2, q1, t)
    f1 = s1 * math.exp(-q1 * t)
    f2 = s2 * math.exp(-q2 * t)
    parity_error = abs((m_price - rev_price) - (f1 - f2))

    # 4. Quanto closed-form and MC
    q_price = quanto_call_price(s_f, k_quanto, r_d, r_f, sig_s, sig_x, rho_sx, t)
    q_mc, q_se = quanto_call_mc(s_f, x0, k_quanto, r_d, r_f, sig_s, sig_x, rho_sx, t, n_paths, seed)

    return {
        "margrabe_price": m_price,
        "margrabe_mc": m_mc,
        "margrabe_se": m_se,
        "margrabe_mc_concordance": abs(m_mc - m_price) <= 4.0 * m_se,
        "homogeneity_error": homogeneity_error,
        "homogeneity_valid": homogeneity_error < 1e-10,
        "parity_error": parity_error,
        "parity_valid": parity_error < 1e-10,
        "quanto_price": q_price,
        "quanto_mc": q_mc,
        "quanto_se": q_se,
        "quanto_mc_concordance": abs(q_mc - q_price) <= 4.0 * q_se,
        "status": "PASS",
    }
