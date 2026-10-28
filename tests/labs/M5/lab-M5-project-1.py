"""Rung 1 worked example: one discounted Bellman sweep and its certified error on a three-point grid.

Standard library only; the example uses no random numbers. The model: output from capital k is k**alpha, so saving
kp leaves consumption k**alpha - kp; utility is sqrt(consumption); the operator takes the best feasible saving plus
beta times the value of that saving. Step 1 prints the resources, step 2 the feasible savings, step 3 one sweep from
zero, step 4 a contraction check, step 5 the iteration to a certified error of 1e-6, and step 6 the actual error
against a reference fixed point iterated to 1e-12.
"""

import math

BETA = 0.9
ALPHA = 0.5
GRID = [0.5, 0.9, 1.4]


def resources(k: float) -> float:
    """Output available from capital k: k to the power alpha."""
    return float(k**ALPHA)


def feasible(k: float) -> list[int]:
    """Indices of the successors kp with kp <= k**alpha, that is, consumption k**alpha - kp >= 0."""
    return [j for j, kp in enumerate(GRID) if kp <= resources(k)]


def bellman(values: list[float]) -> list[float]:
    """One application of the discounted Bellman operator: max over feasible kp of sqrt(k**alpha - kp) + beta V(kp)."""
    out = []
    for k in GRID:
        out.append(max(math.sqrt(resources(k) - GRID[j]) + BETA * values[j] for j in feasible(k)))
    return out


def sup_distance(a: list[float], b: list[float]) -> float:
    """The sup norm of a difference: the largest absolute entry."""
    return max(abs(x - y) for x, y in zip(a, b, strict=False))


def main() -> None:
    # Step 1. The resources k**alpha at each grid point.
    for k in GRID:
        print(f"resources at k={k}: {resources(k):.6f}")
    # Step 2. The feasible successors: kp is feasible from k when kp <= k**alpha.
    for k in GRID:
        print(f"feasible successors from k={k}: {[GRID[j] for j in feasible(k)]}")
    # Step 3. One sweep from the zero vector: the continuation term beta V(kp) is zero, so V1 is the best consumption.
    v0 = [0.0, 0.0, 0.0]
    v1 = bellman(v0)
    print("V1:", [f"{x:.6f}" for x in v1])
    # Step 4. Contraction check with V = V0 and W = V1: sup|BV - BW| is at most beta times sup|V - W|.
    bv, bw = bellman(v0), bellman(v1)
    lhs = sup_distance(bv, bw)
    rhs = BETA * sup_distance(v0, v1)
    print(f"sup|BV - BW| = {lhs:.6f} | beta * sup|V - W| = {rhs:.6f} | holds: {lhs <= rhs}")
    # Step 5. Iterate from V0. After each sweep: the change sup|V_n - V_{n-1}| and the certified error
    # beta/(1-beta) times that change. Print the first three sweeps, then stop at the first certified error <= 1e-6.
    values = v0
    n = 0
    certified = math.inf
    while certified > 1e-6:
        n += 1
        new = bellman(values)
        change = sup_distance(new, values)
        certified = BETA / (1 - BETA) * change
        values = new
        if n <= 3:
            print(f"sweep {n}: change {change:.6f} | certified error {certified:.6f}")
    print(f"stopped after sweep {n}: change {change:.9f} | certified error {certified:.9f}")
    # Step 6. Compare with a reference fixed point, iterated until its certified error is at most 1e-12.
    reference = v0
    for _ in range(100_000):
        nxt = bellman(reference)
        small = BETA / (1 - BETA) * sup_distance(nxt, reference) <= 1e-12
        reference = nxt
        if small:
            break
    print("value after the last sweep:", [f"{x:.6f}" for x in values])
    print(f"actual error {sup_distance(values, reference):.9f} <= certified error {certified:.9f}")


main()
