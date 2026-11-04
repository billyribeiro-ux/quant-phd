"""Rung 3 reference case: the solver on the 3 by 3 grid that the report uses, with stated SIMULATED inputs.

Standard library only. The grid values are stated parameters of the model, not a draw from the generator. The model
constants are a = 2, tau_v = 1 and tau_e = 1. The function solve is the reference: copy this file as report/run_case.py
and replace the body of solve with a call to your module's solve_model; the file must then print the same lines.

Each row gives the informed fraction (bisection on the gap, with the stated tolerance), the price informativeness, the
gap at the reported fraction, and the closed-form fraction of the report's appendix. The last line checks the box of
the autograder's generator on a 22 by 22 grid, which includes the four corners: the gap must be positive at fraction 0
and negative at fraction 1 at every grid point.
"""

import math

A = 2.0  # the CARA coefficient
TAU_V = 1.0  # the prior precision of the payoff v
TAU_E = 1.0  # the precision of the signal s = v + eps
NOISE_GRID = (0.500, 0.625, 0.750)  # the noise volumes the report uses
COST_GRID = (0.120, 0.135, 0.150)  # the information costs the report uses
TOLERANCE = 1e-12  # the bisection stops when the bracket is narrower than this times its upper end


def price_precision(lam: float, sd: float) -> float:
    """tau_y for lam in (0, 1]: lam^2 tau_e^2 / (lam^2 tau_e + a^2 sd^2)."""
    return lam * lam * TAU_E * TAU_E / (lam * lam * TAU_E + A * A * sd * sd)


def indifference_gap(lam: float, sd: float, cost: float) -> float:
    """F_U(lam) - exp(a c) F_I(lam) for lam in (0, 1]; at lam = 1 the uninformed term is a hypothetical agent's."""
    ty = price_precision(lam, sd)
    denominator = lam * (TAU_V + TAU_E) + (1.0 - lam) * (TAU_V + ty)
    b_s = (lam * TAU_E + (1.0 - lam) * ty) / denominator
    b_u = -A * b_s / (lam * TAU_E)
    r = ty / (TAU_V + ty) - b_s
    f_u = math.pow(1.0 + r * r * (TAU_V + ty) * (1.0 / TAU_V + 1.0 / ty), -0.5)
    precision = TAU_V + TAU_E
    slope = TAU_E / precision - b_s
    var_gap = slope * slope * (1.0 / TAU_V + 1.0 / TAU_E) + b_u * b_u * sd * sd
    f_i = math.pow(1.0 + precision * var_gap, -0.5)
    return f_u - math.exp(A * cost) * f_i


def gap_at_zero(sd: float, cost: float) -> float:
    """The limit of the gap as the informed fraction tends to 0."""
    uninformed = math.pow(1.0 + A * A * sd * sd / TAU_V, -0.5)
    informed = math.pow(1.0 + TAU_E / TAU_V + (TAU_V + TAU_E) * A * A * sd * sd / (TAU_V * TAU_V), -0.5)
    return uninformed - math.exp(A * cost) * informed


def closed_form_fraction(sd: float, cost: float) -> float:
    """The root in closed form: tau_y(lam) = tau_bar = (tau_v + tau_e) exp(-2 a c) - tau_v, solved for lam, with
    the same boundary rule as solve. Valid as an appendix check of the bisection, not as the solver."""
    t = (TAU_V + TAU_E) * math.exp(-2.0 * A * cost) - TAU_V
    if t <= 0.0:
        return 0.0
    if t >= TAU_E * TAU_E / (TAU_E + A * A * sd * sd):
        return 1.0
    return A * sd * math.sqrt(t / (TAU_E * (TAU_E - t)))


def solve(sd: float, cost: float) -> dict[str, float]:
    """The reference solver: the boundary rule, then bisection on the sign change of the gap."""
    g_0, g_1 = gap_at_zero(sd, cost), indifference_gap(1.0, sd, cost)
    if g_0 <= 0.0:
        lam = 0.0
    elif g_1 >= 0.0:
        lam = 1.0
    else:
        low, high = 0.0, 1.0
        while high - low > TOLERANCE * high:
            mid = 0.5 * (low + high)
            if indifference_gap(mid, sd, cost) > 0.0:
                low = mid
            else:
                high = mid
        lam = 0.5 * (low + high)
    if lam == 0.0:
        gap, pi = g_0, 0.0
    elif lam == 1.0:
        gap, pi = g_1, price_precision(1.0, sd) / (TAU_V + price_precision(1.0, sd))
    else:
        gap = indifference_gap(lam, sd, cost)
        ty = price_precision(lam, sd)
        pi = ty / (TAU_V + ty)
    return {"informed_fraction": lam, "price_informativeness": pi, "indifference_gap": gap}


def main() -> None:
    print("noise volume | cost | informed fraction | informativeness | gap | closed-form fraction")
    worst = 0.0
    for sd in NOISE_GRID:
        for cost in COST_GRID:
            out = solve(sd, cost)
            closed = closed_form_fraction(sd, cost)
            worst = max(worst, abs(out["informed_fraction"] - closed))
            print(
                f"{sd:.3f} | {cost:.3f} | {out['informed_fraction']:.4f} | {out['price_informativeness']:.4f} | "
                f"{out['indifference_gap']:+.2e} | {closed:.4f}"
            )
    print("largest difference between the bisection and the closed form on the grid:", f"{worst:.1e}")
    inside = 0
    for i in range(22):
        for j in range(22):
            sd = 0.500 + 0.250 * i / 21.0
            cost = 0.120 + 0.030 * j / 21.0
            if gap_at_zero(sd, cost) > 0.0 and indifference_gap(1.0, sd, cost) < 0.0:
                inside += 1
    print("box grid points with an interior fraction (gap positive at 0, negative at 1):", inside, "of", 22 * 22)


main()
