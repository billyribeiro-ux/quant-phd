"""E4 L06 lab 1: the linear noisy rational-expectations price, exact population values and a seeded sample check.

Inputs are illustrative numbers, plus one seeded simulation that is labelled SIMULATED. The model has one risky asset
with payoff v of prior mean zero and variance SIG_V2, a signal s = v + eps with noise variance SIG_E2, and a
noise-trader supply u with mean zero and variance SIG_U2. A mass LAM of CARA investors with coefficient A_CARA observes
s; the rest observe only the price p. Market clearing requires total demand to equal the supply u.

Part A: the closed-form coefficients of the linear price p = THETA_S * s - THETA_U * u, as exact Fractions.
Part B: exact population moments of (s, p), the projection coefficient of v on p, and the posterior variance of an
uninformed investor, each computed from the moments and not from the closed form.
Part C: market clearing checked exactly on a grid of (s, u). Demands come from the Gaussian conditional formulas,
and the uninformed belief is the projection of v on p, computed from the moments of p. Every residual is zero.
Part D: a slope other than the equilibrium slope leaves a nonzero residual at one point of the grid.
Part E: SIMULATED. A seeded sample of N_DRAWS draws of (v, eps, u). The sample slope of p on s and of v on p each lie
within three estimated standard errors of the population value.

Units: the payoff, the signal and the price are in price units per unit of the asset, so their variances are in squared
price units. The supply u is in units of the asset. The coefficient theta_s is dimensionless. The coefficients kappa and
theta_u have units of price per unit of the asset, because theta_u * u is a price. The sample uses floating point and
prints six decimals. Every other value is an exact Fraction.
"""

from __future__ import annotations

import math
import random
from fractions import Fraction
from typing import NamedTuple

SIG_V2 = Fraction(1)
SIG_E2 = Fraction(1)
A_CARA = Fraction(1)
LAM = Fraction(1, 2)
SIG_U2 = Fraction(1, 4)
ALT_SLOPE = Fraction(1, 2)
SEED = 6
N_DRAWS = 20000
GRID_S = (Fraction(-1), Fraction(0), Fraction(1), Fraction(2))
GRID_U = (Fraction(-1), Fraction(0), Fraction(1, 2), Fraction(2))


class Price(NamedTuple):
    """The closed-form linear price p = theta_s * s - theta_u * u and the intermediate quantities that define it."""

    kappa: Fraction
    sig_eta2: Fraction
    tau_eta: Fraction
    tau_bar: Fraction
    theta_s: Fraction
    theta_u: Fraction


def check_inputs(sig_v2: Fraction, sig_e2: Fraction, a: Fraction, lam: Fraction, sig_u2: Fraction) -> None:
    """Raise ValueError unless the variances are positive, a is positive and the informed mass lies in (0, 1)."""
    if sig_v2 <= 0 or sig_e2 <= 0 or sig_u2 <= 0:
        raise ValueError("payoff, signal and supply variances must be positive")
    if a <= 0:
        raise ValueError("CARA coefficient must be positive")
    if not 0 < lam < 1:
        raise ValueError("informed fraction must lie strictly between 0 and 1")


def closed_form(sig_v2: Fraction, sig_e2: Fraction, a: Fraction, lam: Fraction, sig_u2: Fraction) -> Price:
    """The linear noisy REE coefficients: kappa = a / (lam / sig_e2), tau_eta = 1 / (sig_e2 + kappa^2 sig_u2)."""
    check_inputs(sig_v2, sig_e2, a, lam, sig_u2)
    tau_v = 1 / sig_v2
    tau_e = 1 / sig_e2
    kappa = a / (lam * tau_e)
    sig_eta2 = sig_e2 + kappa * kappa * sig_u2
    tau_eta = 1 / sig_eta2
    tau_bar = lam * tau_e + (1 - lam) * tau_eta
    theta_s = tau_bar / (tau_v + tau_bar)
    theta_u = kappa * theta_s
    return Price(kappa, sig_eta2, tau_eta, tau_bar, theta_s, theta_u)


def residual(
    s: Fraction,
    u: Fraction,
    theta_s: Fraction,
    theta_u: Fraction,
    sig_v2: Fraction,
    sig_e2: Fraction,
    a: Fraction,
    lam: Fraction,
    sig_u2: Fraction,
) -> Fraction:
    """Total demand minus supply at (s, u) when the price is theta_s * s - theta_u * u.

    The informed demand uses E[v | s, p] = omega s with omega = sig_v2 / (sig_v2 + sig_e2), and Var(v | s, p) = V_I
    (Lemma 6.3, which holds for any price coefficients). The uninformed belief is the
    projection of v on p, with slope Cov(v, p) / Var(p) and residual variance Var(v) - slope Cov(v, p). Both use the
    moments of p, so the residual does not depend on the closed form.
    """
    price = theta_s * s - theta_u * u
    var_p = theta_s * theta_s * (sig_v2 + sig_e2) + theta_u * theta_u * sig_u2
    cov_vp = theta_s * sig_v2
    slope = cov_vp / var_p
    resid_var = sig_v2 - slope * cov_vp
    var_inf = sig_v2 * sig_e2 / (sig_v2 + sig_e2)
    mean_inf = sig_v2 * s / (sig_v2 + sig_e2)
    demand_inf = (mean_inf - price) / (a * var_inf)
    demand_unf = (slope * price - price) / (a * resid_var)
    return lam * demand_inf + (1 - lam) * demand_unf - u


def ols(x: list[float], y: list[float]) -> tuple[float, float]:
    """Slope and its standard error from a simple regression of y on x, with an intercept."""
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    sxx = sum((xi - mean_x) ** 2 for xi in x)
    sxy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y, strict=True))
    slope = sxy / sxx
    intercept = mean_y - slope * mean_x
    rss = sum((yi - intercept - slope * xi) ** 2 for xi, yi in zip(x, y, strict=True))
    return slope, math.sqrt(rss / (n - 2) / sxx)


def part_a(price: Price) -> None:
    """Print the closed-form coefficients at the base instance."""
    print("Part A: closed-form coefficients at the base instance")
    print(
        f"base sig_v2 {SIG_V2} sig_e2 {SIG_E2} a {A_CARA} lam {LAM} sig_u2 {SIG_U2}",
    )
    print(f"kappa {price.kappa} sig_eta2 {price.sig_eta2} tau_eta {price.tau_eta} tau_bar {price.tau_bar}")
    print(f"theta_s {price.theta_s} theta_u {price.theta_u}")


def part_b(price: Price) -> Fraction:
    """Print the population moments and the projection of v on p; return the projection slope."""
    print("Part B: population moments and the projection of v on p")
    var_s = SIG_V2 + SIG_E2
    var_p = price.theta_s**2 * var_s + price.theta_u**2 * SIG_U2
    cov_vp = price.theta_s * SIG_V2
    slope = cov_vp / var_p
    resid_var = SIG_V2 - slope * cov_vp
    print(f"var_s {var_s} var_p {var_p} cov_vp {cov_vp}")
    print(f"slope_v_on_p {slope} posterior_var_uninformed {resid_var}")
    tau_v = 1 / SIG_V2
    print(f"posterior_var_is_1_over_P_U {resid_var == 1 / (tau_v + price.tau_eta)}")
    closed = price.tau_eta / ((tau_v + price.tau_eta) * price.theta_s)
    print(f"slope_equals_closed_form {slope == closed}")
    rho2 = cov_vp**2 / (SIG_V2 * var_p)
    print(f"rho2_from_moments {rho2}")
    return slope


def part_c(price: Price) -> None:
    """Check market clearing exactly on the grid of (s, u)."""
    print("Part C: market clearing on the grid, exact")
    values = [
        residual(s, u, price.theta_s, price.theta_u, SIG_V2, SIG_E2, A_CARA, LAM, SIG_U2)
        for s in GRID_S
        for u in GRID_U
    ]
    zeros = sum(1 for r in values if r == 0)
    print(f"grid_points {len(values)} zero_residuals {zeros} all_zero {zeros == len(values)}")
    s_example = Fraction(1)
    demand_inf = (SIG_V2 * s_example / (SIG_V2 + SIG_E2) - (price.theta_s * s_example)) / (
        A_CARA * SIG_V2 * SIG_E2 / (SIG_V2 + SIG_E2)
    )
    print(f"informed_demand_at_s1_u0 {demand_inf}")


def part_d(price: Price) -> None:
    """A slope other than the equilibrium slope leaves a nonzero residual."""
    print("Part D: an alternative slope fails market clearing")
    r = residual(Fraction(1), Fraction(0), ALT_SLOPE, price.theta_u, SIG_V2, SIG_E2, A_CARA, LAM, SIG_U2)
    print(f"alternative_slope {ALT_SLOPE} residual_at_s1_u0 {r} nonzero {r != 0}")


def part_e(price: Price, slope_vp: Fraction) -> None:
    """SIMULATED: the seeded sample slopes against the population slopes."""
    print("Part E: SIMULATED sample check")
    rng = random.Random(SEED)
    sd_v = math.sqrt(float(SIG_V2))
    sd_e = math.sqrt(float(SIG_E2))
    sd_u = math.sqrt(float(SIG_U2))
    theta_s = float(price.theta_s)
    theta_u = float(price.theta_u)
    s_draws: list[float] = []
    p_draws: list[float] = []
    v_draws: list[float] = []
    for _ in range(N_DRAWS):
        v = rng.gauss(0.0, sd_v)
        eps = rng.gauss(0.0, sd_e)
        u = rng.gauss(0.0, sd_u)
        s = v + eps
        s_draws.append(s)
        p_draws.append(theta_s * s - theta_u * u)
        v_draws.append(v)
    slope_ps, se_ps = ols(s_draws, p_draws)
    slope_vp_hat, se_vp = ols(p_draws, v_draws)
    tol_ps = 3.0 * se_ps
    tol_vp = 3.0 * se_vp
    print(f"seed {SEED} draws {N_DRAWS}")
    print(
        f"p_on_s slope {slope_ps:.6f} population {float(price.theta_s):.6f} "
        f"tolerance {tol_ps:.6f} within {abs(slope_ps - float(price.theta_s)) <= tol_ps}"
    )
    print(
        f"v_on_p slope {slope_vp_hat:.6f} population {float(slope_vp):.6f} "
        f"tolerance {tol_vp:.6f} within {abs(slope_vp_hat - float(slope_vp)) <= tol_vp}"
    )


def main() -> None:
    """Print Parts A to E. Parts A to D are exact; Part E is one seeded simulation."""
    price = closed_form(SIG_V2, SIG_E2, A_CARA, LAM, SIG_U2)
    part_a(price)
    slope = part_b(price)
    part_c(price)
    part_d(price)
    part_e(price, slope)


main()
