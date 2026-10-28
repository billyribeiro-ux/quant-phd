"""Rung 2 completed solution: the contraction ratio of the Bellman operator, and the certified error of its iteration.

Standard library only. The model is the rung 1 model: output k**alpha, feasible savings kp <= k**alpha, utility sqrt of
consumption, and beta times the continuation value. The completed lines are the modulus step (the observed ratio
sup|BV - BW| / sup|V - W|) and the bound line (beta / (1 - beta) times the last change).
"""

import math

BETA = 0.9
ALPHA = 0.5
GRID = [0.5, 0.9, 1.4]


def resources(k: float) -> float:
    """Output available from capital k: k to the power alpha."""
    return float(k**ALPHA)


def bellman(values: list[float]) -> list[float]:
    """One application of the discounted Bellman operator: max over feasible kp of sqrt(k**alpha - kp) + beta V(kp)."""
    out = []
    for k in GRID:
        best = max(math.sqrt(resources(k) - kp) + BETA * values[j] for j, kp in enumerate(GRID) if kp <= resources(k))
        out.append(best)
    return out


def sup_distance(a: list[float], b: list[float]) -> float:
    """The sup norm of a difference: the largest absolute entry."""
    return max(abs(x - y) for x, y in zip(a, b, strict=False))


def main() -> None:
    v = [0.0, 0.0, 0.0]
    w = [0.1, 0.2, 0.3]
    ratio = sup_distance(bellman(v), bellman(w)) / sup_distance(v, w)
    print(f"contraction ratio: {ratio:.6f} | modulus beta: {BETA}")
    print("ratio at most beta:", ratio <= BETA)
    values = [0.0, 0.0, 0.0]
    n = 0
    certified = math.inf
    while certified > 1e-6 and n < 300:
        n += 1
        new = bellman(values)
        change = sup_distance(new, values)
        certified = BETA / (1 - BETA) * change
        values = new
    print(f"sweeps: {n} | certified error: {certified:.3e} | last change: {change:.3e}")
    print("values:", [f"{x:.6f}" for x in values])


main()
