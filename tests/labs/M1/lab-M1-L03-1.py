"""M1 lab L03: the exponential and logarithm identities, checked to a stated tolerance.

Standard library only. No randomness and no network. The identities are checked on finite grids of
inputs with math.exp and math.log, which are floating-point approximations. A check on a grid is
numerical evidence that the identity holds to the tolerance on that grid. It does not prove the
identity, and the proofs on the page establish the identities from the stated properties.
"""

from __future__ import annotations

import math

TOL = 1e-12


def close(x: float, y: float) -> bool:
    """True when |x - y| <= TOL * max(1, |y|): an absolute tolerance near 1, a relative one above 1."""
    return abs(x - y) <= TOL * max(1.0, abs(y))


def grid(lo: float, hi: float, step: float) -> list[float]:
    """Evenly spaced values from lo to hi inclusive, as lo + i * step for integers i >= 0."""
    count = round((hi - lo) / step)
    return [lo + i * step for i in range(count + 1)]


def product_rule(values: list[float]) -> tuple[int, int]:
    """Count pairs (a, b) from values where exp(a + b) is close to exp(a) * exp(b). Returns (holds, pairs)."""
    holds = pairs = 0
    for a in values:
        for b in values:
            pairs += 1
            holds += close(math.exp(a + b), math.exp(a) * math.exp(b))
    return holds, pairs


def log_of_exp(values: list[float]) -> int:
    """Count x in values with log(exp(x)) close to x."""
    return sum(close(math.log(math.exp(x)), x) for x in values)


def exp_of_log(values: list[float]) -> int:
    """Count y in values (all positive) with exp(log(y)) close to y."""
    return sum(close(math.exp(math.log(y)), y) for y in values)


def log_product(values: list[float]) -> tuple[int, int]:
    """Count pairs (a, b) of positive values with log(a * b) close to log(a) + log(b). Returns (holds, pairs)."""
    holds = pairs = 0
    for a in values:
        for b in values:
            pairs += 1
            holds += close(math.log(a * b), math.log(a) + math.log(b))
    return holds, pairs


def doubling_time(rate: float) -> float:
    """The time t with exp(rate * t) = 2, namely log(2) / rate, for a continuously compounded rate > 0."""
    if rate <= 0.0:
        raise ValueError(f"doubling_time needs a rate above 0, got {rate}")
    return math.log(2.0) / rate


def main() -> None:
    xs = grid(-3.0, 3.0, 0.5)
    holds, pairs = product_rule(xs)
    print(f"grid for x: {len(xs)} values from -3 to 3 in steps of 0.5")
    print(f"exp(a + b) equals exp(a) * exp(b) to tolerance: {holds} of {pairs} pairs")
    print(f"log(exp(x)) equals x to tolerance: {log_of_exp(xs)} of {len(xs)} values")

    ys = [0.1, 0.5, 1.0, 2.0, 10.0, 100.0]
    print(f"exp(log(y)) equals y to tolerance: {exp_of_log(ys)} of {len(ys)} values")
    holds, pairs = log_product(ys)
    print(f"log(a * b) equals log(a) + log(b) to tolerance: {holds} of {pairs} pairs")

    rate = 0.05
    t = doubling_time(rate)
    print(f"continuously compounded rate {rate}: doubling time log(2)/rate = {t:.4f} years")
    print(f"exp(rate * t) at that time, to 4 decimals: {math.exp(rate * t):.4f}")
    print(f"exp(rate * t) equals 2 to tolerance: {close(math.exp(rate * t), 2.0)}")
    growth = math.exp(0.05 * 10)
    print(f"exp(0.05 * 10), the growth factor after 10 years at rate 0.05: {growth:.4f}")


main()
