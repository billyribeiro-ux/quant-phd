"""E4 L08 lab 1: the informed fraction in a CARA-normal model with costly information, by bisection.

The parameters are illustrative constants, not data: CARA coefficient a = 2, prior variance of the payoff
sigma_v^2 = 1, signal-noise variance sigma_eps^2 = 1, noise-trader supply variance sigma_u^2 = 1, prior mean 0.
Parts B to D evaluate population formulas in double precision. Part A uses seeded draws and is SIMULATED.
The informed fraction lam lies in [0, 1]. The price is p = (1 - beta) * prior mean + beta * s - kappa * beta * u,
with kappa = a * sigma_eps^2 / lam, where s = v + eps is the signal and u is the noise-trader supply.
The gain from information is the cost at which an informed and an uninformed trader are equally well off.
Part C solves gain(lam) = cost by bisection on (0, 1) to a tolerance of 1e-12 on lam. The boundary rule is:
lam = 0 when gain(0) <= cost, lam = 1 when gain(1) >= cost, and the bisection root otherwise.
The gap printed for each cost is gain(lam) - cost at the reported lam (the net benefit of information).
Standard library only; no network access.
"""

from __future__ import annotations

import itertools
import math
import random

CARA = 2.0
VAR_V = 1.0
VAR_EPS = 1.0
VAR_U = 1.0
PRIOR_MEAN = 0.0
COSTS: tuple[float, ...] = (0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18)
TOL = 1e-12
SEED = 20261103
DRAWS = 20000
GRID = 999


def equilibrium(lam: float, var_u: float = VAR_U) -> dict[str, float]:
    """Price coefficients and the gain from information at informed fraction lam in (0, 1].

    var_u is the variance of the noise-trader supply. The returned dictionary holds beta (the weight of the signal in
    the price), kappa (the noise coefficient divided by beta), corr2 (the squared correlation between payoff and price)
    and gain (the cost at which an informed and an uninformed trader are equally well off).
    """
    if not 0.0 < lam <= 1.0:
        raise ValueError("lam must lie in (0, 1]")
    tau_v = 1.0 / VAR_V
    tau_e = 1.0 / VAR_EPS
    kappa = CARA * VAR_EPS / lam
    tau_eta = 1.0 / (VAR_EPS + kappa * kappa * var_u)
    a_w = lam * tau_e + (1.0 - lam) * tau_eta
    beta = a_w / (tau_v + a_w)
    b_s = tau_e / (tau_v + tau_e)
    b_y = tau_eta / (tau_v + tau_eta)
    post_s = 1.0 / (tau_v + tau_e)
    post_u = 1.0 / (tau_v + tau_eta)
    noise_term = (kappa * beta) ** 2 * var_u
    var_informed = (b_s - beta) ** 2 * (VAR_V + VAR_EPS) + noise_term
    var_uninformed = (b_y - beta) ** 2 * (VAR_V + 1.0 / tau_eta)
    gain = math.log((1.0 + var_informed / post_s) / (1.0 + var_uninformed / post_u)) / (2.0 * CARA)
    return {
        "beta": beta,
        "kappa": kappa,
        "corr2": b_y,
        "gain": gain,
    }


def gain_at_zero(var_u: float = VAR_U) -> float:
    """Gain from becoming informed when no trader is informed; the price is prior mean minus CARA VAR_V u."""
    total = VAR_V + VAR_EPS
    b_s = VAR_V / total
    post_s = 1.0 / (1.0 / VAR_V + 1.0 / VAR_EPS)
    noise = CARA * CARA * VAR_V * VAR_V * var_u
    var_informed = b_s * b_s * total + noise
    return math.log((1.0 + var_informed / post_s) / (1.0 + noise / VAR_V)) / (2.0 * CARA)


def informativeness(lam: float) -> float:
    """Squared correlation between payoff and price at lam; zero when no trader is informed."""
    if lam == 0.0:
        return 0.0
    return equilibrium(lam)["corr2"]


def part_a() -> None:
    """Seeded draws at lam = 0.5: clearing residual below 1e-12, and the sample slope within 0.02 of the formula."""
    lam = 0.5
    eq = equilibrium(lam)
    beta, kappa = eq["beta"], eq["kappa"]
    tau_v = 1.0 / VAR_V
    tau_e = 1.0 / VAR_EPS
    tau_eta = 1.0 / (VAR_EPS + kappa * kappa * VAR_U)
    b_s = tau_e / (tau_v + tau_e)
    b_y = tau_eta / (tau_v + tau_eta)
    post_s = 1.0 / (tau_v + tau_e)
    post_u = 1.0 / (tau_v + tau_eta)
    rng = random.Random(SEED)
    sd_v = math.sqrt(VAR_V)
    sd_e = math.sqrt(VAR_EPS)
    sd_u = math.sqrt(VAR_U)
    worst = 0.0
    prices: list[float] = []
    payoffs: list[float] = []
    for _ in range(DRAWS):
        v = PRIOR_MEAN + rng.gauss(0.0, sd_v)
        eps = rng.gauss(0.0, sd_e)
        u = rng.gauss(0.0, sd_u)
        s = v + eps
        p = (1.0 - beta) * PRIOR_MEAN + beta * s - kappa * beta * u
        demand_i = (PRIOR_MEAN + b_s * (s - PRIOR_MEAN) - p) / (CARA * post_s)
        mean_u = PRIOR_MEAN + (b_y / beta) * (p - PRIOR_MEAN)
        demand_u = (mean_u - p) / (CARA * post_u)
        worst = max(worst, abs(lam * demand_i + (1.0 - lam) * demand_u - u))
        prices.append(p)
        payoffs.append(v)
    n = float(DRAWS)
    mean_p = sum(prices) / n
    mean_v = sum(payoffs) / n
    cov = sum((v - mean_v) * (p - mean_p) for v, p in zip(payoffs, prices, strict=True)) / n
    var_p = sum((p - mean_p) ** 2 for p in prices) / n
    slope = cov / var_p
    formula = b_y / beta
    print(f"part A (SIMULATED draws): lam = {lam}, seed = {SEED}, draws = {DRAWS}")
    print(f"part A: largest market-clearing residual = {worst:.3e} (tolerance 1e-12)")
    print(f"part A: slope of payoff on price, sample = {slope:.4f}, formula b_y / beta = {formula:.4f}")
    print(f"part A: absolute difference = {abs(slope - formula):.4f} (at most 0.02)")
    if worst > 1e-12:
        raise AssertionError("market clearing fails beyond the stated tolerance")
    if abs(slope - formula) > 0.02:
        raise AssertionError("sample slope differs from the formula beyond the stated tolerance")


def part_b() -> None:
    """Closed-form gains at the boundaries (double precision) and monotonicity of gain and informativeness on a grid."""
    g0 = gain_at_zero()
    g1 = equilibrium(1.0)["gain"]
    gmid = equilibrium(0.5)["gain"]
    print(f"part B: gain(0) = {g0:.6f}  gain(0.5) = {gmid:.6f}  gain(1) = {g1:.6f}")
    near = equilibrium(1e-6)["gain"] - g0
    print(f"part B: gain(1e-6) - gain(0) = {near:.2e} (continuity at zero with noise supply)")
    lams = [k / (GRID + 1) for k in range(1, GRID + 1)]
    gains = [equilibrium(x)["gain"] for x in lams]
    corrs = [equilibrium(x)["corr2"] for x in lams]
    dec_gain = all(b < a for a, b in itertools.pairwise(gains))
    inc_corr = all(b > a for a, b in itertools.pairwise(corrs))
    print(f"part B: gain strictly decreasing on {GRID} interior grid points: {dec_gain}")
    print(f"part B: Corr(v,p)^2 strictly increasing on the same grid: {inc_corr}")
    if not (dec_gain and inc_corr):
        raise AssertionError("monotonicity fails on the grid")


def solve_fraction(cost: float) -> tuple[float, float, str]:
    """Return the informed fraction, the net benefit gain(lam) - cost there, and the rule that applied."""
    g0 = gain_at_zero()
    if cost >= g0:
        return 0.0, g0 - cost, "zero"
    g1 = equilibrium(1.0)["gain"]
    if cost <= g1:
        return 1.0, g1 - cost, "one"
    lo, hi = 0.0, 1.0
    while hi - lo > TOL:
        mid = 0.5 * (lo + hi)
        if equilibrium(mid)["gain"] - cost > 0.0:
            lo = mid
        else:
            hi = mid
    lam = 0.5 * (lo + hi)
    return lam, equilibrium(lam)["gain"] - cost, "bisection"


def part_c() -> None:
    """The informed fraction, the gap and the informativeness across the cost grid."""
    previous = 2.0
    for cost in COSTS:
        lam, gap, rule = solve_fraction(cost)
        corr = informativeness(lam)
        label = {"zero": "boundary: cost >= gain(0)", "one": "boundary: cost <= gain(1)", "bisection": "root"}[rule]
        print(f"part C: cost = {cost:.2f}  lam* = {lam:.9f}  gap = {gap:.2e}  Corr(v,p)^2 = {corr:.6f}  ({label})")
        if lam > previous:
            raise AssertionError("the informed fraction rises with cost on the grid")
        previous = lam


def part_d() -> None:
    """No noise supply: gain is zero on the interior grid, so no grid fraction or endpoint is an equilibrium at 0.15."""
    grid = [k / (GRID + 1) for k in range(1, GRID + 1)]
    cost = 0.15
    gains = [equilibrium(x, var_u=0.0)["gain"] for x in grid]
    g0 = gain_at_zero(var_u=0.0)
    g1 = equilibrium(1.0, var_u=0.0)["gain"]
    worst = max(abs(x) for x in gains)
    interior_roots = [x for x, g in zip(grid, gains, strict=True) if abs(g - cost) <= 1e-9]
    zero_is_equilibrium = g0 <= cost
    one_is_equilibrium = g1 >= cost
    print(f"part D: sigma_u^2 = 0: largest |gain| on the (0, 1) grid = {worst:.1e}")
    print(f"part D: sigma_u^2 = 0: gain(0) = {g0:.6f}, gain(1) = {g1:.6f}, cost = {cost:.2f}")
    print(f"part D: sigma_u^2 = 0: interior fractions with gain = cost: {len(interior_roots)}")
    print(f"part D: sigma_u^2 = 0: lam = 0 is an equilibrium: {zero_is_equilibrium}")
    print(f"part D: sigma_u^2 = 0: lam = 1 is an equilibrium: {one_is_equilibrium}")
    if interior_roots or zero_is_equilibrium or one_is_equilibrium:
        raise AssertionError("an equilibrium exists in the noiseless case at this cost")


def main() -> None:
    part_a()
    part_b()
    part_c()
    part_d()


main()
