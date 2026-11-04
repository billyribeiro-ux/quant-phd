"""E4 L07 lab 1: price informativeness in the linear noisy rational-expectations model, from exact population formulas.

Inputs are illustrative numbers, plus one seeded simulation that is labelled SIMULATED. The model is the one of
lesson L06: a payoff v with prior variance SIG_V2, a signal s = v + eps with noise variance SIG_E2, a noise-trader
supply u with standard deviation sd (the noise volume), a mass lam of CARA investors with coefficient a who observe s,
and a price p = theta_s * s - theta_u * u that clears the market.

Part A: the squared correlation of payoff and price, Corr(v, p)^2, computed from the exact moments, and compared with
the closed form sig_v2 / (sig_v2 + sig_eta2), where sig_eta2 = sig_e2 + kappa^2 sd^2 and kappa = a sig_e2 / lam.
Part B: the sweep over the noise volume sd, with the price variance printed next to the informativeness.
Part C: the sweep over the informed fraction lam at the base noise volume.
Part D: the sweep over the CARA coefficient a at the base noise volume.
Part E: the benchmark of no supply noise, as a limit, and the largest value on the sweep.
Part F: SIMULATED. A seeded sample of N_DRAWS draws of (v, eps, u), and the sample squared correlation of v and p.

Units: the payoff v is in units of the asset (its liquidation value). Corr(v, p)^2 is dimensionless and lies
in [0, 1]. Parts A to E print exact Fraction population values; Part F converts the exact population value
to float for comparison with the sample. The sample uses floating point and prints six decimals.
"""

from __future__ import annotations

import math
import random
from fractions import Fraction
from typing import NamedTuple

SIG_V2 = Fraction(1)
SIG_E2 = Fraction(1)
A_BASE = Fraction(1)
LAM_BASE = Fraction(1, 2)
SD_BASE = Fraction(1, 2)
SD_GRID = (Fraction(1, 4), Fraction(1, 2), Fraction(1), Fraction(2), Fraction(4))
LAM_GRID = (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4))
A_GRID = (Fraction(1, 2), Fraction(1), Fraction(2))
SD_TINY = Fraction(1, 100)
SEED = 7
N_DRAWS = 20000
TOLERANCE = 0.02


class Coefficients(NamedTuple):
    """The linear price p = theta_s * s - theta_u * u.

    sig_eta2 is the variance of eta = eps - kappa * u, the noise in p / theta_s.
    """

    sig_eta2: Fraction
    theta_s: Fraction
    theta_u: Fraction


def check_inputs(sig_v2: Fraction, sig_e2: Fraction, a: Fraction, lam: Fraction, sd: Fraction) -> None:
    """Raise ValueError unless the variances are positive, a is positive, lam lies in (0, 1) and sd >= 0."""
    if sig_v2 <= 0 or sig_e2 <= 0:
        raise ValueError("payoff and signal variances must be positive")
    if a <= 0:
        raise ValueError("CARA coefficient must be positive")
    if not 0 < lam < 1:
        raise ValueError("informed fraction must lie strictly between 0 and 1")
    if sd < 0:
        raise ValueError("noise volume must be nonnegative")


def coefficients(sig_v2: Fraction, sig_e2: Fraction, a: Fraction, lam: Fraction, sd: Fraction) -> Coefficients:
    """The closed-form price coefficients of lesson L06, valid for sd > 0 and, at sd = 0, as the limit they define."""
    check_inputs(sig_v2, sig_e2, a, lam, sd)
    tau_v = 1 / sig_v2
    tau_e = 1 / sig_e2
    kappa = a / (lam * tau_e)
    sig_eta2 = sig_e2 + kappa * kappa * sd * sd
    tau_eta = 1 / sig_eta2
    tau_bar = lam * tau_e + (1 - lam) * tau_eta
    theta_s = tau_bar / (tau_v + tau_bar)
    return Coefficients(sig_eta2, theta_s, kappa * theta_s)


def rho2_from_moments(sig_v2: Fraction, sig_e2: Fraction, coef: Coefficients, sd: Fraction) -> Fraction:
    """Corr(v, p)^2 from the moments of (v, p): Cov(v, p)^2 / (Var(v) Var(p))."""
    cov_vp = coef.theta_s * sig_v2
    var_p = coef.theta_s * coef.theta_s * (sig_v2 + sig_e2) + coef.theta_u * coef.theta_u * sd * sd
    return cov_vp * cov_vp / (sig_v2 * var_p)


def rho2_closed(sig_v2: Fraction, coef: Coefficients) -> Fraction:
    """Corr(v, p)^2 = sig_v2 / (sig_v2 + sig_eta2): the squared correlation of v with Y = p / theta_s."""
    return sig_v2 / (sig_v2 + coef.sig_eta2)


def var_price(sig_v2: Fraction, sig_e2: Fraction, coef: Coefficients, sd: Fraction) -> Fraction:
    """Var(p) = theta_s^2 (sig_v2 + sig_e2) + theta_u^2 sd^2."""
    return coef.theta_s * coef.theta_s * (sig_v2 + sig_e2) + coef.theta_u * coef.theta_u * sd * sd


def part_a() -> Coefficients:
    """The base instance: the moment formula and the closed form agree exactly."""
    print("Part A: informativeness at the base instance")
    coef = coefficients(SIG_V2, SIG_E2, A_BASE, LAM_BASE, SD_BASE)
    moments = rho2_from_moments(SIG_V2, SIG_E2, coef, SD_BASE)
    closed = rho2_closed(SIG_V2, coef)
    print(f"base sig_v2 {SIG_V2} sig_e2 {SIG_E2} a {A_BASE} lam {LAM_BASE} noise_volume_sd {SD_BASE}")
    print(f"sig_eta2 {coef.sig_eta2} theta_s {coef.theta_s} theta_u {coef.theta_u}")
    print(f"rho2_from_moments {moments} rho2_closed_form {closed} equal {moments == closed}")
    return coef


def part_b() -> list[Fraction]:
    """The sweep over the noise volume, with the price variance beside the informativeness."""
    print("Part B: sweep over the noise volume sd, other parameters at the base instance")
    values: list[Fraction] = []
    for sd in SD_GRID:
        coef = coefficients(SIG_V2, SIG_E2, A_BASE, LAM_BASE, sd)
        rho2 = rho2_from_moments(SIG_V2, SIG_E2, coef, sd)
        values.append(rho2)
        print(f"sd {sd} sig_eta2 {coef.sig_eta2} var_p {var_price(SIG_V2, SIG_E2, coef, sd)} rho2 {rho2}")
    decreasing = all(values[i] > values[i + 1] for i in range(len(values) - 1))
    print(f"rho2_strictly_decreasing_in_sd {decreasing}")
    return values


def part_c() -> list[Fraction]:
    """The sweep over the informed fraction at the base noise volume."""
    print("Part C: sweep over the informed fraction lam, other parameters at the base instance")
    values: list[Fraction] = []
    for lam in LAM_GRID:
        coef = coefficients(SIG_V2, SIG_E2, A_BASE, lam, SD_BASE)
        rho2 = rho2_from_moments(SIG_V2, SIG_E2, coef, SD_BASE)
        values.append(rho2)
        print(f"lam {lam} sig_eta2 {coef.sig_eta2} rho2 {rho2}")
    increasing = all(values[i] < values[i + 1] for i in range(len(values) - 1))
    print(f"rho2_strictly_increasing_in_lam {increasing}")
    return values


def part_d() -> list[Fraction]:
    """The sweep over the CARA coefficient at the base noise volume."""
    print("Part D: sweep over the CARA coefficient a, other parameters at the base instance")
    values: list[Fraction] = []
    for a in A_GRID:
        coef = coefficients(SIG_V2, SIG_E2, a, LAM_BASE, SD_BASE)
        rho2 = rho2_from_moments(SIG_V2, SIG_E2, coef, SD_BASE)
        values.append(rho2)
        print(f"a {a} sig_eta2 {coef.sig_eta2} rho2 {rho2}")
    decreasing = all(values[i] > values[i + 1] for i in range(len(values) - 1))
    print(f"rho2_strictly_decreasing_in_a {decreasing}")
    return values


def part_e(sweep_values: list[Fraction]) -> None:
    """The benchmark of no supply noise, as a limit, and a tiny noise volume near it."""
    print("Part E: benchmark without supply noise, as a limit")
    benchmark = SIG_V2 / (SIG_V2 + SIG_E2)
    print(f"benchmark_corr_v_s_squared {benchmark}")
    coef = coefficients(SIG_V2, SIG_E2, A_BASE, LAM_BASE, SD_TINY)
    tiny = rho2_closed(SIG_V2, coef)
    print(f"sd {SD_TINY} rho2 {tiny} below_benchmark {tiny < benchmark}")
    below = all(value < benchmark for value in sweep_values)
    print(f"largest_sweep_value {max(sweep_values)} all_sweep_values_below_benchmark {below}")


def part_f(coef: Coefficients) -> None:
    """SIMULATED: the squared sample correlation of v and p against the population value."""
    print("Part F: SIMULATED sample check")
    rng = random.Random(SEED)
    sd_v = math.sqrt(float(SIG_V2))
    sd_e = math.sqrt(float(SIG_E2))
    sd_u = float(SD_BASE)
    theta_s = float(coef.theta_s)
    theta_u = float(coef.theta_u)
    v_draws: list[float] = []
    p_draws: list[float] = []
    for _ in range(N_DRAWS):
        v = rng.gauss(0.0, sd_v)
        eps = rng.gauss(0.0, sd_e)
        u = rng.gauss(0.0, sd_u)
        v_draws.append(v)
        p_draws.append(theta_s * (v + eps) - theta_u * u)
    n = len(v_draws)
    mean_v = sum(v_draws) / n
    mean_p = sum(p_draws) / n
    cov = sum((v - mean_v) * (p - mean_p) for v, p in zip(v_draws, p_draws, strict=True))
    var_v = sum((v - mean_v) ** 2 for v in v_draws)
    var_p = sum((p - mean_p) ** 2 for p in p_draws)
    sample_rho2 = cov * cov / (var_v * var_p)
    population = float(rho2_closed(SIG_V2, coef))
    print(f"seed {SEED} draws {N_DRAWS} tolerance {TOLERANCE}")
    print(
        f"sample_rho2 {sample_rho2:.6f} population {population:.6f} within {abs(sample_rho2 - population) <= TOLERANCE}"
    )


def main() -> None:
    """Print Parts A to F. Parts A to E are exact; Part F is one seeded simulation."""
    coef = part_a()
    sweep = part_b()
    part_c()
    part_d()
    part_e(sweep)
    part_f(coef)


main()
