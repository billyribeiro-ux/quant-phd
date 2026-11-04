"""Rung 1 worked example: one SIMULATED instance, solved step by step.

Standard library only. The two inputs are stated values for this example, a noise volume of 0.60 and an information
cost of 0.13. They are not a draw from the generator in grader/instance.py. The model constants are a = 2, tau_v = 1
and tau_e = 1. Each step prints the quantity it computes, so every printed number comes from the code below.
"""

import math

A = 2.0  # the CARA coefficient
TAU_V = 1.0  # the prior precision of the payoff v
TAU_E = 1.0  # the precision of the signal s = v + eps
SD = 0.60  # the noise volume: the standard deviation of the noise supply u
COST = 0.13  # the information cost c
BISECTION_STEPS = 60  # 60 halvings of [0, 1] reach the floating-point resolution near the root


def price_precision(lam: float) -> float:
    """tau_y, the precision of the price signal, for an informed fraction lam in (0, 1]: lam^2 tau_e^2 /
    (lam^2 tau_e + a^2 SD^2). It is 0 at lam = 0."""
    return lam * lam * TAU_E * TAU_E / (lam * lam * TAU_E + A * A * SD * SD)


def price_coefficients(lam: float) -> tuple[float, float]:
    """The coefficients b_s and b_u of the linear price p = b_s s + b_u u, for lam in (0, 1]."""
    ty = price_precision(lam)
    denominator = lam * (TAU_V + TAU_E) + (1.0 - lam) * (TAU_V + ty)
    b_s = (lam * TAU_E + (1.0 - lam) * ty) / denominator
    return b_s, -A * b_s / (lam * TAU_E)


def uninformed_term(lam: float) -> float:
    """F_U(lam) for lam in (0, 1]: the Gaussian term of the uninformed investor's expected utility."""
    ty = price_precision(lam)
    b_s, _ = price_coefficients(lam)
    r = ty / (TAU_V + ty) - b_s
    return math.pow(1.0 + r * r * (TAU_V + ty) * (1.0 / TAU_V + 1.0 / ty), -0.5)


def informed_term(lam: float) -> float:
    """F_I(lam) for lam in (0, 1]: the Gaussian term of the informed investor's expected utility."""
    b_s, b_u = price_coefficients(lam)
    precision = TAU_V + TAU_E
    slope = TAU_E / precision - b_s
    var_gap = slope * slope * (1.0 / TAU_V + 1.0 / TAU_E) + b_u * b_u * SD * SD
    return math.pow(1.0 + precision * var_gap, -0.5)


def gap(lam: float) -> float:
    """The informed-minus-uninformed expected utility at lam in (0, 1]: F_U(lam) - exp(a c) F_I(lam)."""
    return uninformed_term(lam) - math.exp(A * COST) * informed_term(lam)


def gap_at_zero() -> float:
    """The limit of the gap as lam tends to 0: the price then tends to -a u / tau_v."""
    uninformed = math.pow(1.0 + A * A * SD * SD / TAU_V, -0.5)
    informed = math.pow(1.0 + TAU_E / TAU_V + (TAU_V + TAU_E) * A * A * SD * SD / (TAU_V * TAU_V), -0.5)
    return uninformed - math.exp(A * COST) * informed


def main() -> None:
    print("step 1 | inputs: noise volume", SD, "| information cost", COST, "| a", A)
    g0, g1 = gap_at_zero(), gap(1.0)
    print("step 2 | gap as the informed fraction tends to 0:", f"{g0:+.6f}")
    print("step 2 | gap at the informed fraction 1:", f"{g1:+.6f}")
    print("step 2 | the gap changes sign on (0, 1):", g0 > 0.0 and g1 < 0.0)
    low, high = 0.0, 1.0
    for step in range(1, BISECTION_STEPS + 1):
        mid = 0.5 * (low + high)
        if gap(mid) > 0.0:
            low = mid
        else:
            high = mid
        if step in (1, 2, 3):
            print(f"step 3 | after halving {step}: bracket [{low:.6f}, {high:.6f}]")
    root = 0.5 * (low + high)
    print("step 3 | after", BISECTION_STEPS, "halvings the bracket width is", f"{high - low:.3e}")
    print("step 4 | informed fraction lambda* =", f"{root:.8f}")
    print("step 4 | gap at lambda* =", f"{gap(root):+.3e}")
    b_s, b_u = price_coefficients(root)
    print("step 5 | price coefficients b_s =", f"{b_s:.8f}", "b_u =", f"{b_u:.8f}")
    print("step 5 | b_u / b_s =", f"{b_u / b_s:.8f}", "and -a / (lambda* tau_e) =", f"{-A / (root * TAU_E):.8f}")
    ty = price_precision(root)
    print(
        "step 6 | tau_y at lambda* =",
        f"{ty:.8f}",
        "| tau_bar = (tau_v + tau_e) exp(-2 a c) - tau_v =",
        f"{(TAU_V + TAU_E) * math.exp(-2.0 * A * COST) - TAU_V:.8f}",
    )
    pi = ty / (TAU_V + ty)
    print("step 6 | price informativeness tau_y / (tau_v + tau_y) =", f"{pi:.8f}")
    print(
        "step 6 | 1 - exp(2 a c) tau_v / (tau_v + tau_e) =",
        f"{1.0 - math.exp(2.0 * A * COST) * TAU_V / (TAU_V + TAU_E):.8f}",
    )


main()
