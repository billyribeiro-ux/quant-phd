"""E5 L04 lab 1: the IS-LM equilibrium solved exactly, and its fiscal and monetary multipliers.

Inputs are illustrative parameters, not data: marginal propensity to consume c = 3/4, autonomous consumption 1,
autonomous investment 1, investment sensitivity to the interest rate b = 2, money-demand sensitivity to output
d = 1/2, money-demand sensitivity to the interest rate h = 1, lump-sum tax 0, government spending G = 1, and real
money supply mbar = 2. Every quantity is a Fraction, so each step is exact and the printed fractions are the
solution itself. No random draws are used.

Part A: the IS-LM equilibrium (Y*, i*) from the closed form, and the residuals of the IS and LM equations at it.
Part B: the fiscal multiplier, the change in Y* for an increase in G from 1 to 11/10 and from 1 to 2, against
1/(1 - c).
Part C: the monetary multiplier, the change in Y* and in i* for an increase in real money from 2 to 5/2.
Part D: the fiscal multiplier with b = 0, where investment does not respond to the interest rate.
"""

from __future__ import annotations

from fractions import Fraction

C = Fraction(3, 4)
AUTONOMOUS_CONSUMPTION = Fraction(1)
AUTONOMOUS_INVESTMENT = Fraction(1)
B = Fraction(2)
D_OUTPUT = Fraction(1, 2)
H = Fraction(1)
TAX = Fraction(0)
G_BASE = Fraction(1)
MBAR_BASE = Fraction(2)


def autonomous_demand(g: Fraction, tax: Fraction = TAX) -> Fraction:
    """The constant A = c0 - c*Tax + b0 + G in the IS relation (1 - c) Y + b i = A."""
    return AUTONOMOUS_CONSUMPTION - C * tax + AUTONOMOUS_INVESTMENT + g


def denominator(c: Fraction, b: Fraction, d: Fraction, h: Fraction) -> Fraction:
    """The determinant magnitude D = h (1 - c) + b d of the IS-LM system.

    D is positive under A2: 0 < c < 1, h > 0, b >= 0, d >= 0.
    """
    return h * (1 - c) + b * d


def equilibrium(g: Fraction, mbar: Fraction, b: Fraction = B) -> tuple[Fraction, Fraction]:
    """The IS-LM solution (Y*, i*) = ((h A + b mbar)/D, (d A - (1 - c) mbar)/D) for the given G, mbar and b."""
    a = autonomous_demand(g)
    d_value = denominator(C, b, D_OUTPUT, H)
    y = (H * a + b * mbar) / d_value
    i = (D_OUTPUT * a - (1 - C) * mbar) / d_value
    return y, i


def is_residual(y: Fraction, i: Fraction, g: Fraction, b: Fraction = B) -> Fraction:
    """Y minus the goods-market demand c0 + c (Y - Tax) + b0 - b i + G. It is zero at an IS point."""
    demand = AUTONOMOUS_CONSUMPTION + C * (y - TAX) + AUTONOMOUS_INVESTMENT - b * i + g
    return y - demand


def lm_residual(y: Fraction, i: Fraction, mbar: Fraction) -> Fraction:
    """Real money demand d Y - h i minus the real money supply mbar. It is zero at an LM point."""
    return D_OUTPUT * y - H * i - mbar


def part_a() -> tuple[Fraction, Fraction]:
    """Print the closed-form equilibrium and the two exact residuals."""
    y, i = equilibrium(G_BASE, MBAR_BASE)
    print("Part A: IS-LM equilibrium")
    print(f"autonomous_demand {autonomous_demand(G_BASE)}")
    print(f"denominator_D {denominator(C, B, D_OUTPUT, H)}")
    print(f"Y_star {y} {float(y):.10f}")
    print(f"i_star {i} {float(i):.10f}")
    print(f"is_residual {is_residual(y, i, G_BASE)}")
    print(f"lm_residual {lm_residual(y, i, MBAR_BASE)}")
    return y, i


def part_b(y0: Fraction, i0: Fraction) -> None:
    """Print the fiscal multiplier from two exact shifts in G, and the closed form h/D."""
    print("Part B: fiscal multiplier")
    crossing = 1 / (1 - C)
    print(f"keynesian_cross_multiplier {crossing}")
    for g_new in (Fraction(11, 10), Fraction(2)):
        y1, i1 = equilibrium(g_new, MBAR_BASE)
        multiplier = (y1 - y0) / (g_new - G_BASE)
        print(f"shift_G_to {g_new} delta_Y {y1 - y0} multiplier {multiplier} ({float(multiplier):.10f})")
        print(f"shift_G_to {g_new} delta_i {i1 - i0} ({float(i1 - i0):.10f})")
        print(f"is_residual_after_shift {is_residual(y1, i1, g_new)}")
    closed_form = H / denominator(C, B, D_OUTPUT, H)
    print(f"closed_form_h_over_D {closed_form}")
    print(f"multiplier_below_cross {closed_form < crossing}")


def part_c(y0: Fraction, i0: Fraction) -> None:
    """Print the monetary multiplier from an exact shift in real money, and its closed form b/D."""
    print("Part C: monetary multiplier")
    m_new = Fraction(5, 2)
    y1, i1 = equilibrium(G_BASE, m_new)
    print(f"shift_mbar_to {m_new} delta_Y {y1 - y0} multiplier {(y1 - y0) / (m_new - MBAR_BASE)}")
    print(f"shift_mbar_to {m_new} delta_i {i1 - i0} per_unit {(i1 - i0) / (m_new - MBAR_BASE)}")
    print(f"closed_form_b_over_D {B / denominator(C, B, D_OUTPUT, H)}")
    print(f"closed_form_minus_one_minus_c_over_D {-(1 - C) / denominator(C, B, D_OUTPUT, H)}")
    print(f"is_residual_after_shift {is_residual(y1, i1, G_BASE)} lm_residual_after_shift {lm_residual(y1, i1, m_new)}")


def part_d() -> None:
    """Print the fiscal multiplier with investment insensitive to the interest rate (b = 0)."""
    print("Part D: fiscal multiplier with b = 0")
    y0, _ = equilibrium(G_BASE, MBAR_BASE, Fraction(0))
    y1, _ = equilibrium(Fraction(2), MBAR_BASE, Fraction(0))
    print(f"multiplier_b_zero {(y1 - y0) / (Fraction(2) - G_BASE)}")
    print(f"equals_one_over_one_minus_c {(y1 - y0) / (Fraction(2) - G_BASE) == 1 / (1 - C)}")


def main() -> None:
    """Print Parts A to D. Every value is an exact Fraction, or a Fraction with its decimal value to ten places."""
    y0, i0 = part_a()
    part_b(y0, i0)
    part_c(y0, i0)
    part_d()


main()
