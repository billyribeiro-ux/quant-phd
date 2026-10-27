"""Round-5 independent recomputation of R3 (digital bounds on a grid of call prices).

Market: a discrete state-price measure mu* with atoms off the grid. Assets: bond (payoff 1),
underlying (payoff S), calls with strikes K in STRIKES (payoff (S-K)^+). Prices p_i = E_mu*[f_i].
Bounds on E[g] for g in {1{S>=k}, 1{S>k}} over nonnegative measures on a node set N that is
{0} U strikes U recipe nodes U {ray atom at M}, with the ray atom at M = 1e4 (its weight is e/M in the
limit; it is an honest atom at a finite point, so it is exact for that point).
The 'truth' set is the same LP with a dense node set on [0, 200] (step 0.01) plus the ray atom.
"""

import sys

import numpy as np
from scipy.optimize import linprog

STRIKES = [80.0, 90.0, 100.0, 110.0, 120.0]
M_RAY = 1.0e4
ATOMS = [(70.0, 0.10), (85.0, 0.20), (97.0, 0.15), (103.0, 0.15), (115.0, 0.20), (125.0, 0.10), (300.0, 0.0)]
# mu*: weights sum to 0.98 (bond price) — the last atom is weight 0 (kept only to show no mass beyond 125)
MU = [(x, w) for x, w in ATOMS if w > 0]
BOND = sum(w for _, w in MU)
UND = sum(w * x for x, w in MU)
CALLS = {K: sum(w * max(x - K, 0.0) for x, w in MU) for K in STRIKES}


def rows(x: float) -> list[float]:
    return [1.0, x] + [max(x - K, 0.0) for K in STRIKES]


P_EQ = [BOND, UND] + [CALLS[K] for K in STRIKES]


def bounds(nodes: list[float], g) -> tuple[float, float]:
    xs = sorted(set(nodes + [M_RAY]))
    A = np.array([rows(x) for x in xs]).T  # assets x atoms
    c = np.array([g(x) for x in xs])
    lo = linprog(c, A_eq=A, b_eq=np.array(P_EQ), bounds=[(0, None)] * len(xs), method="highs")
    hi = linprog(-c, A_eq=A, b_eq=np.array(P_EQ), bounds=[(0, None)] * len(xs), method="highs")
    if lo.status != 0 or hi.status != 0:
        return float("nan"), float("nan")
    return float(lo.fun), float(-hi.fun)


def ge(k):
    return lambda x: 1.0 if x >= k else 0.0


def gt(k):
    return lambda x: 1.0 if x > k else 0.0


if __name__ == "__main__":
    print("bond", BOND, "und", UND, "calls", CALLS)
    dense = [round(i * 0.01, 10) for i in range(0, 20001)]  # 0..200
    base = [0.0] + STRIKES
    for k in (100.0, 95.0):
        for name, mk in (("ge", ge), ("gt", gt)):
            g = mk(k)
            truth = bounds(dense + [k - 1e-3, k + 1e-3], g)
            print(f"\nk={k} convention 1{{S{'>=' if name=='ge' else '>'}k}} truth(dense 0.01 + k+-1e-3, ray) = {truth}")
            print("  base grid only       ", bounds(base, g))
            print("  +k only              ", bounds(base + [k], g))
            for d in (1.0, 0.1, 0.01, 0.001):
                print(f"  delta={d:<6}", "both k-d,k+d", bounds(base + [k - d, k + d], g),
                      "| k-d,k", bounds(base + [k - d, k], g),
                      "| k,k+d", bounds(base + [k, k + d], g),
                      "| only k-d", bounds(base + [k - d], g),
                      "| only k+d", bounds(base + [k + d], g))
    sys.stdout.flush()
