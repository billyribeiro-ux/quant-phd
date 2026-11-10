"""Lab PR3-project-1: Project Rung 1 Worked Example in Exact Arithmetic.

SIMULATED: Closed-form verification of discrete and continuous Kelly sizing.
"""

from __future__ import annotations

from fractions import Fraction


def main() -> None:
    # 1. Discrete Binary Bet: win prob p = 3/5 (60%), net odds b = 2/1 (payoff 2 to 1)
    p = Fraction(3, 5)
    b = Fraction(2, 1)
    q = Fraction(1, 1) - p  # 2/5

    # Kelly formula: f* = (b*p - q) / b
    edge = b * p - q  # 2 * 3/5 - 2/5 = 6/5 - 2/5 = 4/5
    f_star_discrete = edge / b  # (4/5) / 2 = 2/5 = 0.40

    # Expected log multiplier per bet:
    # E[ln(1 + f*X)] = (3/5)*ln(1 + 2*(2/5)) + (2/5)*ln(1 - 2/5)
    #               = (3/5)*ln(9/5) + (2/5)*ln(3/5)

    print("Project Rung 1 · Worked Example: Exact Kelly Derivations")
    print("=" * 60)
    print("1. Discrete Binary Bet:")
    print(f"   Win probability p: {p} ({float(p):.2f})")
    print(f"   Net payoff ratio b: {b} ({float(b):.2f})")
    print(f"   Loss probability q: {q} ({float(q):.2f})")
    print(f"   Net Expected Edge: {edge} ({float(edge):.2f})")
    print(f"   Optimal Kelly Fraction f*: {f_star_discrete} ({float(f_star_discrete):.4f})")

    # 2. Continuous Single-Asset Sizing:
    # Expected return mu = 12/100, risk-free r = 4/100, vol sigma = 20/100
    mu = Fraction(12, 100)
    r = Fraction(4, 100)
    sigma = Fraction(20, 100)

    excess_mu = mu - r  # 8/100
    variance = sigma**2  # 400/10000 = 4/100 = 1/25
    f_star_cont = excess_mu / variance  # (8/100) / (4/100) = 2/1 = 2.0

    # Optimal continuous growth rate: g* = r + 0.5 * (excess_mu^2 / variance)
    max_excess_growth = Fraction(1, 2) * (excess_mu**2 / variance)  # 0.5 * (8/100 * 2) = 8/100
    g_star = r + max_excess_growth  # 4/100 + 8/100 = 12/100

    # Half-Kelly continuous growth rate:
    # g(0.5 f*) = r + 0.5 * excess_mu * f* - 0.5 * (0.5 f*)^2 * variance
    half_excess_growth = Fraction(3, 4) * max_excess_growth  # 6/100
    g_half = r + half_excess_growth  # 10/100

    print("\n2. Continuous Diffusion Sizing:")
    print(f"   Expected return mu: {mu} ({float(mu):.4f})")
    print(f"   Risk-free rate r: {r} ({float(r):.4f})")
    print(f"   Annualized volatility sigma: {sigma} ({float(sigma):.4f})")
    print(f"   Excess return (mu - r): {excess_mu} ({float(excess_mu):.4f})")
    print(f"   Variance sigma^2: {variance} ({float(variance):.4f})")
    print(f"   Continuous Kelly Leverage f*: {f_star_cont} ({float(f_star_cont):.4f})")
    print(f"   Full Kelly Growth Rate g*: {g_star} ({float(g_star):.4f})")
    print(f"   Half-Kelly Growth Rate g(0.5f*): {g_half} ({float(g_half):.4f})")
    print(f"   Half-Kelly Excess Growth Capture: {half_excess_growth / max_excess_growth} (75.0%)")


main()
