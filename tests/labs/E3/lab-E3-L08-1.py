"""E3 L08 lab 1: certainty equivalents of one gamble under four preference models, and a two-urn check.

Inputs are integer cents (100 cents = 1 CU). Initial wealth is W0 = 100000 cents (1000 CU). The gamble is a bet on
one ball drawn from an urn of 90 balls: final wealth is 110000 cents (a gain of 10000 cents) if the ball is red and
95000 cents (a loss of 5000 cents) otherwise. A certainty equivalent (CE) is the sure final wealth, in cents, that
the model ranks equal to the gamble. Part A prints each of the four model CEs at four decimals and rounds it once, half
up, to a whole cent; Parts B and C print at fixed decimals and round nothing to a whole cent.

The ambiguous urn holds k red balls, with k unknown and only known to lie in 30 to 60 (the prior set). Four models:
 1. Expected utility with CRRA utility u(W) = -1/W (gamma = 2), at P(red) = 1/2, the average of the prior set.
 2. Prospect value on changes from the reference point 0, with v(x) = x**(1/2) for gains and -2 * (-x)**(1/2) for
    losses (alpha = delta = 1/2, lambda = 2), at P(red) = 1/2. The gamble's value is inverted in closed form.
 3. Epstein-Zin over two dates: date 0 consumes W0; date 1 consumes final wealth. psi = 1/2, beta = 0.95, gamma = 2,
    at P(red) = 1/2. The CE is the sure date-1 amount that gives the same date-0 value, found by 200 halvings of
    a bracket of 17000 cents, which reaches floating-point resolution.
 4. Maxmin expected utility over the prior set (tau = 1), and alpha-MEU with tau = 1/2, which weights the lowest
    and highest expected utility over the prior set.

Part A prints the four CEs, the alpha-MEU value at tau = 1/2, the prospect closed form against bisection, and
the ambiguity-aversion check. Part B checks the Epstein-Zin CE against the CRRA CE for three values of psi and two of
beta. Part C is an Ellsberg-type two-urn check: a known urn (30 red of 90) against an ambiguous urn whose red count is
any of 0 to 90, under the CRRA utility u(W) = -1/W. Part D checks that a one-element prior set gives expected
utility. Standard library only; no randomness and no network access.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from fractions import Fraction

W0_CENTS = 100_000
WIN_CENTS = 110_000
LOSS_CENTS = 95_000
URN_SIZE = 90
PRIOR_SET: tuple[Fraction, ...] = tuple(Fraction(k, URN_SIZE) for k in range(30, 61))
FULL_PRIOR_SET: tuple[Fraction, ...] = tuple(Fraction(k, URN_SIZE) for k in range(0, URN_SIZE + 1))
GAMMA = 2.0
PSI_VALUES: tuple[float, ...] = (0.5, 1.5, 3.0)
BETA_VALUES: tuple[float, ...] = (0.9, 0.95)
ALPHA_VALUE = 0.5
LAMBDA_VALUE = 2.0
GAIN_CU = 100.0
LOSS_CU = -50.0


def average(values: Sequence[Fraction]) -> Fraction:
    """Arithmetic mean of exact fractions."""
    return sum(values, Fraction(0)) / len(values)


def ce_single_prior(p: Fraction) -> Fraction:
    """CE in cents of the gamble when red has probability p, under CRRA gamma = 2 (u(W) = -1/W), exactly.

    The CE solves -1/CE = E u(W) = -(p/WIN + (1 - p)/LOSS), so CE = 1 / E[1/W]."""
    return 1 / (p / WIN_CENTS + (1 - p) / LOSS_CENTS)


def alpha_meu_ce(priors: Sequence[Fraction], tau: Fraction) -> Fraction:
    """CE in cents of alpha-MEU: V = tau * min_P E_P u + (1 - tau) * max_P E_P u, then CE = u^{-1}(V).

    With u(W) = -1/W and inv(P) = E_P[1/W], V = -(tau * max inv + (1 - tau) * min inv), so CE = 1/(tau * max inv
    + (1 - tau) * min inv). tau = 1 is maxmin expected utility."""
    invs = [ce_inv(p) for p in priors]
    return 1 / (tau * max(invs) + (1 - tau) * min(invs))


def ce_inv(p: Fraction) -> Fraction:
    """E[1/W] of the gamble when red has probability p, in 1/cents."""
    return p / WIN_CENTS + (1 - p) / LOSS_CENTS


def half_up(value: Fraction) -> int:
    """Return an exact fraction as a whole number of cents, half up."""
    return math.floor(value + Fraction(1, 2))


def half_up_float(value_cents: float) -> int:
    """Return a float number of cents as a whole number, half up; refuse a value within 1e-6 cents of a half cent."""
    floor_part = math.floor(value_cents)
    if abs(value_cents - floor_part - 0.5) < 1e-6:
        raise ValueError("the unrounded CE lies within 1e-6 cents of a half cent; the rounding rule is not applied")
    return math.floor(value_cents + 0.5)


def prospect_value(x_cu: float) -> float:
    """Prospect value of a change x in CU: x**(1/2) for gains, -LAMBDA * (-x)**(1/2) for losses."""
    if x_cu >= 0:
        return float(x_cu**ALPHA_VALUE)
    return float(-LAMBDA_VALUE * (-x_cu) ** (1.0 / 2.0))


def prospect_inverse(v: float) -> float:
    """Closed-form inverse of prospect_value: v**2 for v >= 0, and -(-v / LAMBDA)**2 for v < 0."""
    if v >= 0:
        return float(v ** (1.0 / ALPHA_VALUE))
    return float(-((-v / LAMBDA_VALUE) ** 2))


def prospect_inverse_by_bisection(v: float) -> float:
    """The same inverse by 200 halvings of prospect_value over [-1000, 1000] CU, which reaches
    floating-point resolution."""
    lo, hi = -1000.0, 1000.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if prospect_value(mid) < v:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def ez_value(c0: float, date1: Sequence[tuple[float, float]], psi: float, beta: float) -> float:
    """Two-date Epstein-Zin value V0 = [(1 - beta) c0**a + beta * (E[c1**(1 - gamma)])**(a / (1 - gamma))]**(1/a),
    with a = 1 - 1/psi, gamma = GAMMA and the terminal value V1 = c1. The sure amount is a one-point distribution."""
    a = 1.0 - 1.0 / psi
    expectation = sum(p * c1 ** (1.0 - GAMMA) for c1, p in date1)
    inner = (1.0 - beta) * c0**a + beta * expectation ** (a / (1.0 - GAMMA))
    return float(inner ** (1.0 / a))


def ez_certainty_equivalent(c0: float, date1: Sequence[tuple[float, float]], psi: float, beta: float) -> float:
    """The sure date-1 amount c with ez_value(c0, [(c, 1)]) equal to ez_value(c0, date1), by 200 halvings of
    a bracket of 17000 cents, which reaches floating-point resolution."""
    target = ez_value(c0, date1, psi, beta)
    lo, hi = float(LOSS_CENTS - 1000), float(WIN_CENTS + 1000)
    for _ in range(200):
        mid = (lo + hi) / 2
        if ez_value(c0, [(mid, 1.0)], psi, beta) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def gamble_outcomes(p: float) -> list[tuple[float, float]]:
    """Final wealth in cents with probabilities: (WIN, p) and (LOSS, 1 - p)."""
    return [(float(WIN_CENTS), p), (float(LOSS_CENTS), 1.0 - p)]


def part_a() -> None:
    p_bar = average(PRIOR_SET)
    print(
        f"part A: wealth W0 = {W0_CENTS} cents; red pays +{WIN_CENTS - W0_CENTS} cents, otherwise "
        f"{LOSS_CENTS - W0_CENTS} cents"
    )
    print(f"part A: prior set = red counts 30 to 60 out of {URN_SIZE}; average prior P(red) = {p_bar}")
    eu = ce_single_prior(p_bar)
    print(f"part A: EU, CRRA gamma = 2, P(red) = 1/2: CE = {float(eu):.4f} cents, whole cents = {half_up(eu)}")
    prospect_cu = 0.5 * prospect_value(GAIN_CU) + 0.5 * prospect_value(LOSS_CU)
    prospect_wealth = W0_CENTS + 100.0 * prospect_inverse(prospect_cu)
    print(
        f"part A: prospect value V = {prospect_cu:.6f} (CU to the 1/2 power), CE = {prospect_wealth:.4f} cents, "
        f"whole cents = {half_up_float(prospect_wealth)}"
    )
    gap_inverse = prospect_inverse(prospect_cu) - prospect_inverse_by_bisection(prospect_cu)
    print(f"part A: prospect inverse, closed form minus bisection = {gap_inverse:.2e} CU")
    ez_cents = ez_certainty_equivalent(float(W0_CENTS), gamble_outcomes(0.5), psi=0.5, beta=0.95)
    print(
        f"part A: Epstein-Zin, psi = 0.5, beta = 0.95, P(red) = 1/2: CE = {ez_cents:.4f} cents, "
        f"whole cents = {half_up_float(ez_cents)}"
    )
    worst = min(PRIOR_SET, key=ce_single_prior)
    maxmin = alpha_meu_ce(PRIOR_SET, Fraction(1))
    print(
        f"part A: maxmin, tau = 1: worst prior is P(red) = {worst}; CE = {float(maxmin):.4f} cents, "
        f"whole cents = {half_up(maxmin)}"
    )
    mix = alpha_meu_ce(PRIOR_SET, Fraction(1, 2))
    print(f"part A: alpha-MEU, tau = 1/2: CE = {float(mix):.4f} cents, whole cents = {half_up(mix)}")
    print(f"part A: alpha-MEU at tau = 1/2 equals the EU CE here = {mix == eu}")
    print(f"part A: ambiguity aversion holds (maxmin CE <= CE at the average prior) = {maxmin <= eu}")


def part_b() -> None:
    eu_exact = ce_single_prior(average(PRIOR_SET))
    worst = 0.0
    for psi in PSI_VALUES:
        for beta in BETA_VALUES:
            ez = ez_certainty_equivalent(float(W0_CENTS), gamble_outcomes(0.5), psi, beta)
            gap = abs(ez - float(eu_exact))
            worst = max(worst, gap)
            print(
                f"part B: psi = {psi:g}, beta = {beta:g}: EZ CE = {ez:.6f} cents, "
                f"EZ minus CRRA CE = {ez - float(eu_exact):.2e}"
            )
    print(f"part B: largest absolute gap over the six (psi, beta) pairs = {worst:.2e} cents")
    print(f"part B: all six gaps below 1e-6 cents = {worst < 1e-6}")


def part_c() -> None:
    red_known = Fraction(30, URN_SIZE)
    black_known = Fraction(60, URN_SIZE)
    prize_win, prize_lose = W0_CENTS + 10_000, W0_CENTS

    def ce_bet(p: Fraction) -> Fraction:
        return 1 / (p / prize_win + (1 - p) / prize_lose)

    known_red = ce_bet(red_known)
    known_black = ce_bet(black_known)
    amb_red = min(ce_bet(p) for p in FULL_PRIOR_SET)
    amb_black = min(ce_bet(1 - p) for p in FULL_PRIOR_SET)
    print("part C: CRRA utility u(W) = -1/W; the bet pays 10000 cents on a win and 0 otherwise")
    print("part C: wealth is 100000 or 110000 cents")
    print(f"part C: known urn (30 red of 90): red CE = {float(known_red):.4f}, black CE = {float(known_black):.4f}")
    print(
        f"part C: ambiguous urn (red count 0 to 90): maxmin red CE = {float(amb_red):.4f}, "
        f"maxmin black CE = {float(amb_black):.4f}"
    )
    print(f"part C: known urn preferred for red = {known_red > amb_red}; for black = {known_black > amb_black}")


def part_d() -> None:
    p_bar = average(PRIOR_SET)
    singleton = (p_bar,)
    eu = ce_single_prior(p_bar)
    print(f"part D: singleton prior {{1/2}}: maxmin CE equals EU CE = {alpha_meu_ce(singleton, Fraction(1)) == eu}")
    print(
        f"part D: singleton prior {{1/2}}: alpha-MEU with tau = 1/2 equals EU CE = "
        f"{alpha_meu_ce(singleton, Fraction(1, 2)) == eu}"
    )


def main() -> None:
    part_a()
    part_b()
    part_c()
    part_d()


main()
