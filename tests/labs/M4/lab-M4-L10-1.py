"""M4 lab L10: sample means under Gaussian, Student-t(3) and standard Cauchy draws.

SIMULATED: every draw comes from a seeded generator; no data is used. Standard library only (math, random,
statistics). Three laws are drawn. The standard normal is drawn with random.gauss(0, 1). The Student-t law with 3
degrees of freedom is V = Z / sqrt(W / 3), with Z a standard normal and W the sum of three squared independent
standard normals, W independent of Z. The standard Cauchy law is drawn by its distribution function's inverse,
tan(pi (U - 1/2)), for a uniform U from random.random(). Part A checks the increment F(2) - F(-2) of the
closed-form distribution function of the t(3) law against a midpoint integral of its density over [-2, 2], the
density being (2 / (pi sqrt 3)) (1 + t^2 / 3)^(-2), and prints the tail probabilities P(|X| > x) at x = 10 for the
three laws. Part B prints the running sample mean of one seeded path of each law at n = 10, 100, 1000 and 10000.
Part C runs 400 seeded replications at n = 10 and n = 100, and prints the interquartile range of the sample mean
(the 75th minus the 25th percentile, with statistics.quantiles, method "inclusive") for each law, and the sample
variance of sqrt(n) Xbar_n / sigma for the normal and t(3) laws, where sigma is 1 for the normal and sqrt(3) for
the t(3). Part D prints the products x P(|X| > x) for the Cauchy law and x^3 P(|V| > x) for the t(3) law at x = 10,
100 and 1000. A sample is one random run.
"""

from __future__ import annotations

import math
import random
import statistics
from collections.abc import Callable

SEED = 2026
CHECKPOINTS = (10, 100, 1000, 10000)
REPLICATIONS = 400
SAMPLE_SIZES = (10, 100)
SQRT3 = math.sqrt(3.0)


def draw_normal(rng: random.Random) -> float:
    """One standard normal draw."""
    return rng.gauss(0.0, 1.0)


def draw_t3(rng: random.Random) -> float:
    """One Student-t draw with 3 degrees of freedom: Z / sqrt(W / 3), W a sum of three squared normals."""
    z = rng.gauss(0.0, 1.0)
    w = sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(3))
    return z / math.sqrt(w / 3.0)


def draw_cauchy(rng: random.Random) -> float:
    """One standard Cauchy draw by the inverse distribution function tan(pi (U - 1/2))."""
    u = rng.random()
    return math.tan(math.pi * (u - 0.5))


def t3_density(t: float) -> float:
    """Density of the Student-t law with 3 degrees of freedom."""
    return 2.0 / (math.pi * SQRT3) * (1.0 + t * t / 3.0) ** -2


def t3_cdf(x: float) -> float:
    """Distribution function of the Student-t law with 3 degrees of freedom, in closed form."""
    y = x / SQRT3
    return 0.5 + (math.atan(y) + y / (1.0 + x * x / 3.0)) / math.pi


def t3_tail_one_sided(x: float) -> float:
    """P(V > x) for x > 0, as arctan(1/y) minus y/(1+y^2) over pi with y = x/sqrt 3.
    Both subtracted terms are near 1/y for large x, so at x = 1000 the difference is about
    2e-6 times each term and about six significant digits are lost; the printed values are unaffected."""
    y = x / SQRT3
    return (math.atan(1.0 / y) - y / (1.0 + y * y)) / math.pi


def cauchy_two_sided_tail(x: float) -> float:
    """P(|X| > x) for the standard Cauchy law and x > 0."""
    return 1.0 - 2.0 * math.atan(x) / math.pi


def midpoint_integral(f: Callable[[float], float], a: float, b: float, steps: int) -> float:
    """Midpoint rule for the integral of f over [a, b] with equal steps."""
    h = (b - a) / steps
    return h * sum(f(a + (k + 0.5) * h) for k in range(steps))


def part_a() -> None:
    check = midpoint_integral(t3_density, -2.0, 2.0, 200000)
    exact = t3_cdf(2.0) - t3_cdf(-2.0)
    print(f"part A: midpoint integral of the t(3) density on [-2, 2] = {check:.9f}")
    print(f"part A: t(3) distribution function difference F(2) - F(-2) = {exact:.9f}")
    print(f"part A: the two agree to 1e-8: {abs(check - exact) < 1e-8}")
    x = 10.0
    normal_tail = math.erfc(x / math.sqrt(2.0))
    cauchy_tail = cauchy_two_sided_tail(x)
    t_tail = 2.0 * t3_tail_one_sided(x)
    print(f"part A: P(|Z| > 10) = {normal_tail:.4e}")
    print(f"part A: P(|X| > 10) for the Cauchy law = {cauchy_tail:.6f}")
    print(f"part A: P(|V| > 10) for the t(3) law = {t_tail:.6f}")
    print(f"part A: the Cauchy tail is {cauchy_tail / normal_tail:.3e} times the normal tail at x = 10")


def running_means(draw: Callable[[random.Random], float], seed: int) -> list[tuple[int, float]]:
    """Running sample means of one seeded path at the checkpoints."""
    rng = random.Random(seed)
    total = 0.0
    out: list[tuple[int, float]] = []
    count = 0
    for target in CHECKPOINTS:
        while count < target:
            total += draw(rng)
            count += 1
        out.append((target, total / target))
    return out


def part_b() -> None:
    laws = (
        ("normal", draw_normal, SEED),
        ("t(3)", draw_t3, SEED + 1),
        ("Cauchy", draw_cauchy, SEED + 2),
    )
    for name, draw, seed in laws:
        for n, mean in running_means(draw, seed):
            print(f"part B: {name:6s} n = {n:5d}, running sample mean = {mean:+.4f}")


def part_c() -> None:
    for name, draw, seed, sigma in (
        ("normal", draw_normal, SEED, 1.0),
        ("t(3)", draw_t3, SEED + 1, SQRT3),
        ("Cauchy", draw_cauchy, SEED + 2, None),
    ):
        for n in SAMPLE_SIZES:
            rng = random.Random(seed + 100 * n)
            means = [sum(draw(rng) for _ in range(n)) / n for _ in range(REPLICATIONS)]
            q1, _, q3 = statistics.quantiles(means, n=4, method="inclusive")
            line = f"part C: {name:6s} n = {n:4d}, interquartile range of the sample mean = {q3 - q1:.4f}"
            if sigma is not None:
                standardized = [math.sqrt(n) * m / sigma for m in means]
                line += f", variance of sqrt(n) Xbar_n / sigma = {statistics.variance(standardized):.4f}"
            print(line)
    exact_iqr = math.tan(math.pi / 4) - math.tan(-math.pi / 4)
    print(f"part C: exact interquartile range of one standard Cauchy draw = {exact_iqr:.6f}")


def part_d() -> None:
    for x in (10.0, 100.0, 1000.0):
        cauchy_product = x * cauchy_two_sided_tail(x)
        t_product = x**3 * 2.0 * t3_tail_one_sided(x)
        print(
            f"part D: x = {x:6.0f}, x P(|X| > x) for Cauchy = {cauchy_product:.6f}, "
            f"x^3 P(|V| > x) for t(3) = {t_product:.6f}"
        )


def main() -> None:
    part_a()
    part_b()
    part_c()
    part_d()


main()
