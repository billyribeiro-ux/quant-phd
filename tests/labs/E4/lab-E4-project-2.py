"""Rung 2 completion problem: the indifference gap and its bisection, for one SIMULATED instance.

Standard library only. The inputs are stated values for this example: a noise volume of 0.70 and an information cost of
0.14, not a draw from the generator. The model constants are a = 2, tau_v = 1 and tau_e = 1. This file is the completed
solution: the page shows the same lines with the return of indifference_gap replaced by blanks.
"""

import math

A = 2.0  # the CARA coefficient
TAU_V = 1.0  # the prior precision of the payoff v
TAU_E = 1.0  # the precision of the signal s = v + eps
SD = 0.70  # the noise volume: the standard deviation of the noise supply u
COST = 0.14  # the information cost c
BISECTION_STEPS = 60  # 60 halvings of [0, 1] reach the floating-point resolution near the root


def price_precision(lam: float) -> float:
    """tau_y for lam in (0, 1]: lam^2 tau_e^2 / (lam^2 tau_e + a^2 SD^2)."""
    return lam * lam * TAU_E * TAU_E / (lam * lam * TAU_E + A * A * SD * SD)


def price_coefficients(lam: float) -> tuple[float, float]:
    """The coefficients b_s and b_u of the linear price p = b_s s + b_u u, for lam in (0, 1]."""
    ty = price_precision(lam)
    denominator = lam * (TAU_V + TAU_E) + (1.0 - lam) * (TAU_V + ty)
    b_s = (lam * TAU_E + (1.0 - lam) * ty) / denominator
    return b_s, -A * b_s / (lam * TAU_E)


def indifference_gap(lam: float) -> float:
    """The informed-minus-uninformed expected utility at lam in (0, 1]: F_U(lam) - exp(a c) F_I(lam)."""
    ty = price_precision(lam)
    b_s, b_u = price_coefficients(lam)
    r = ty / (TAU_V + ty) - b_s
    f_u = math.pow(1.0 + r * r * (TAU_V + ty) * (1.0 / TAU_V + 1.0 / ty), -0.5)
    precision = TAU_V + TAU_E
    slope = TAU_E / precision - b_s
    var_gap = slope * slope * (1.0 / TAU_V + 1.0 / TAU_E) + b_u * b_u * SD * SD
    f_i = math.pow(1.0 + precision * var_gap, -0.5)
    return f_u - math.exp(A * COST) * f_i


def main() -> None:
    low, high = 0.0, 1.0
    gap_at_zero = math.pow(1.0 + A * A * SD * SD / TAU_V, -0.5) - math.exp(A * COST) * math.pow(
        1.0 + TAU_E / TAU_V + (TAU_V + TAU_E) * A * A * SD * SD / (TAU_V * TAU_V), -0.5
    )
    print("gap as the fraction tends to 0:", f"{gap_at_zero:+.6f}", "| gap at 1:", f"{indifference_gap(1.0):+.6f}")
    for _ in range(BISECTION_STEPS):
        mid = 0.5 * (low + high)
        if indifference_gap(mid) > 0.0:
            low = mid
        else:
            high = mid
    root = 0.5 * (low + high)
    print("informed fraction lambda* =", f"{root:.8f}", "| bracket width", f"{high - low:.3e}")
    print("gap at lambda* =", f"{indifference_gap(root):+.3e}")
    ty = price_precision(root)
    print("price informativeness tau_y / (tau_v + tau_y) =", f"{ty / (TAU_V + ty):.8f}")


main()
