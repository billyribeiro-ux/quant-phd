"""Gap at a zero fraction reported as 0.0 instead of the limit of Proposition 3 that the page requires.

Single edit of grader/reference.py, written by the verifier (slice d, round 1).
"""

from __future__ import annotations

import math

RISK_AVERSION = 2.0  # a: the CARA coefficient of U(W) = -exp(-a W), fixed for every instance
PRIOR_PRECISION = 1.0  # tau_v: the precision of the payoff's prior, 1 / Var(v), fixed for every instance
SIGNAL_PRECISION = 1.0  # tau_e: the precision of the signal s = v + eps, 1 / Var(eps), fixed for every instance
BISECTION_TOLERANCE = 1e-12  # the search stops when the bracket is narrower than this times its upper end
MAX_BISECTION_STEPS = 240  # a safety bound: each halving halves the bracket, so 240 halvings reach the relative
# tolerance for every root above about 6e-61 (2^-240 is about 5.7e-73). 200 halvings do not reach it near 2e-51.


def _check_inputs(noise_sd: float, info_cost: float) -> tuple[float, float]:
    """The two named conditions of the specification: a positive finite noise volume, a nonnegative information cost."""
    sd = float(noise_sd)
    cost = float(info_cost)
    if not (math.isfinite(sd) and sd > 0.0):
        raise ValueError("noise volume must be positive")
    if not (math.isfinite(cost) and cost >= 0.0):
        raise ValueError("information cost must be nonnegative")
    return sd, cost


def price_precision(lam: float, noise_sd: float) -> float:
    """The precision tau_y of the price signal y = p / b_s, for an informed fraction lam in (0, 1] (derivation step 2).

    y = s + kappa u with kappa = -a / (lam tau_e), so y = v + (eps + kappa u) and the noise has variance
    1 / tau_e + kappa^2 sd^2. Its precision is lam^2 tau_e^2 / (lam^2 tau_e + a^2 sd^2). Returns 0 at lam = 0.
    """
    a, tau_e = RISK_AVERSION, SIGNAL_PRECISION
    return lam * lam * tau_e * tau_e / (lam * lam * tau_e + a * a * noise_sd * noise_sd)


def price_coefficients(lam: float, noise_sd: float) -> tuple[float, float, float]:
    """The linear equilibrium price p = b_s s + b_u u for lam in (0, 1], and the precision tau_y of its signal.

    Returns (b_s, b_u, tau_y). The two coefficient equations of derivation step 3 give b_u / b_s = -a / (lam tau_e),
    and b_s = (lam tau_e + (1 - lam) tau_y) / (lam (tau_v + tau_e) + (1 - lam) (tau_v + tau_y)).
    """
    tau_v, tau_e = PRIOR_PRECISION, SIGNAL_PRECISION
    tau_y = price_precision(lam, noise_sd)
    denominator = lam * (tau_v + tau_e) + (1.0 - lam) * (tau_v + tau_y)
    b_s = (lam * tau_e + (1.0 - lam) * tau_y) / denominator
    b_u = -RISK_AVERSION * b_s / (lam * tau_e)
    return b_s, b_u, tau_y


def informed_term(lam: float, noise_sd: float) -> float:
    """F_I(lam) = (1 + P S_I)^(-1/2), the Gaussian integral of the informed agent's utility (derivation step 5).

    P = tau_v + tau_e is the precision of the informed agent's posterior, and S_I is the variance of m_I - p, where
    m_I = tau_e s / P is the informed agent's conditional mean.
    """
    tau_v, tau_e = PRIOR_PRECISION, SIGNAL_PRECISION
    b_s, b_u, _ = price_coefficients(lam, noise_sd)
    precision = tau_v + tau_e
    slope = tau_e / precision - b_s
    var_signal = 1.0 / tau_v + 1.0 / tau_e
    var_gap = slope * slope * var_signal + b_u * b_u * noise_sd * noise_sd
    return math.pow(1.0 + precision * var_gap, -0.5)


def uninformed_term(lam: float, noise_sd: float) -> float:
    """F_U(lam) = (1 + r^2 (tau_v + tau_y)(1/tau_v + 1/tau_y))^(-1/2), for lam in (0, 1] (derivation step 5).

    r = tau_y / (tau_v + tau_y) - b_s, so that the uninformed agent's conditional mean minus the price is r y, with
    Var(y) = 1/tau_v + 1/tau_y, and the posterior variance of v given p is 1 / (tau_v + tau_y).
    """
    tau_v = PRIOR_PRECISION
    b_s, _, tau_y = price_coefficients(lam, noise_sd)
    r = tau_y / (tau_v + tau_y) - b_s
    return math.pow(1.0 + r * r * (tau_v + tau_y) * (1.0 / tau_v + 1.0 / tau_y), -0.5)


def gap_at_zero(noise_sd: float, info_cost: float) -> float:
    """The limit of the gap as the informed fraction tends to 0 (derivation step 6).

    At lam -> 0 the price tends to -a u / tau_v, so the uninformed term tends to (1 + a^2 sd^2 / tau_v)^(-1/2), and the
    informed term tends to (1 + tau_e / tau_v + (tau_v + tau_e) a^2 sd^2 / tau_v^2)^(-1/2).
    """
    tau_v, tau_e = PRIOR_PRECISION, SIGNAL_PRECISION
    a2 = RISK_AVERSION * RISK_AVERSION * noise_sd * noise_sd
    uninformed = math.pow(1.0 + a2 / tau_v, -0.5)
    informed = math.pow(1.0 + tau_e / tau_v + (tau_v + tau_e) * a2 / (tau_v * tau_v), -0.5)
    return uninformed - math.exp(RISK_AVERSION * info_cost) * informed


def indifference_gap(lam: float, noise_sd: float, info_cost: float) -> float:
    """The expected-utility difference E[U_I] - E[U_U] at informed fraction lam, net of the information cost.

    E[U_I] = -exp(a c) F_I(lam) and E[U_U] = -F_U(lam), so the gap is F_U(lam) - exp(a c) F_I(lam). It is evaluated at
    lam = 0 by the limit, and at lam = 1 by the formulas, which need the uninformed term as a hypothetical agent who
    would hold the price of the economy in which every agent is informed.
    """
    if lam == 0.0:
        return gap_at_zero(noise_sd, info_cost)
    return uninformed_term(lam, noise_sd) - math.exp(RISK_AVERSION * info_cost) * informed_term(lam, noise_sd)


def price_informativeness(lam: float, noise_sd: float) -> float:
    """Corr(v, p)^2 = tau_y / (tau_v + tau_y) for lam in (0, 1]; it is 0 at lam = 0, where the price has no signal."""
    if lam == 0.0:
        return 0.0
    tau_y = price_precision(lam, noise_sd)
    return tau_y / (PRIOR_PRECISION + tau_y)


def solve_model(noise_sd: float, info_cost: float) -> dict[str, float]:
    """The informed fraction, the price informativeness and the indifference gap of the model at (noise_sd, info_cost).

    Boundary rule: the informed fraction is 0 when the gap at 0 is nonpositive, 1 when the gap at 1 is nonnegative, and
    otherwise the root of the gap in (0, 1), found by bisection on the sign change with the stated tolerance.
    """
    sd, cost = _check_inputs(noise_sd, info_cost)
    gap_0 = gap_at_zero(sd, cost)
    gap_1 = indifference_gap(1.0, sd, cost)
    if gap_0 <= 0.0:
        lam = 0.0
    elif gap_1 >= 0.0:
        lam = 1.0
    else:
        low, high = 0.0, 1.0  # invariant: the gap is positive at low (its limit, at 0) and negative at high
        steps = 0
        while high - low > BISECTION_TOLERANCE * high and steps < MAX_BISECTION_STEPS:
            mid = 0.5 * (low + high)
            if indifference_gap(mid, sd, cost) > 0.0:
                low = mid
            else:
                high = mid
            steps += 1
        lam = 0.5 * (low + high)
    gap = 0.0 if lam == 0.0 else (indifference_gap(lam, sd, cost) if 0.0 < lam < 1.0 else gap_1)
    return {
        "informed_fraction": lam,
        "price_informativeness": price_informativeness(lam, sd),
        "indifference_gap": gap,
    }
