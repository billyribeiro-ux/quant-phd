"""Round-5: the page's own grid model: node states plus one ray state whose payoff row is the slope beyond the top node.

Asset rows: bond (1 at nodes, slope 0), underlying (x, slope 1), calls (max(x-K,0), slope 1).
Digital g: node value 1{S>=k} or 1{S>k}, slope 0 (constant beyond top).  Top node = largest strike (120).
Bounds: min/max of g' psi over psi >= 0 with X' psi = p.
"""

import sys

sys.path.insert(0, "/tmp/ap1-r5/L03-L04/scripts")
import numpy as np  # noqa: E402
from scipy.optimize import linprog  # noqa: E402

from r3_lp import P_EQ, STRIKES, bounds, ge, gt  # noqa: E402
from r3_lp import bounds as measure_bounds  # noqa: E402

TOP = max(STRIKES)


def asset_row(x: float | None, slope: float, kind: str) -> list[float]:
    """Row of an asset at a node x (x given) or the ray (x None, uses slope)."""
    if kind == "bond":
        return [1.0 if x is not None else 0.0]
    if kind == "und":
        return [x if x is not None else 1.0]
    return [max(x - K, 0.0) if x is not None else 1.0 for K in STRIKES] if False else []


def ray_model(nodes: list[float], g) -> tuple[float, float]:
    xs = sorted(set(nodes + [TOP]))
    cols = []  # each state = a column over (bond, und, calls...)
    for x in xs:
        cols.append([1.0, x] + [max(x - K, 0.0) for K in STRIKES])
    cols.append([0.0, 1.0] + [1.0 for _ in STRIKES])  # ray: slopes
    A = np.array(cols).T
    c = np.array([g(x) for x in xs] + [0.0])
    lo = linprog(c, A_eq=A, b_eq=np.array(P_EQ), bounds=[(0, None)] * len(cols), method="highs")
    hi = linprog(-c, A_eq=A, b_eq=np.array(P_EQ), bounds=[(0, None)] * len(cols), method="highs")
    return float(lo.fun), float(-hi.fun)


if __name__ == "__main__":
    dense = [round(i * 0.01, 10) for i in range(0, 20001)]
    base = [0.0] + STRIKES
    for k in (95.0, 97.3):
        for name, mk in (("ge", ge), ("gt", gt)):
            g = mk(k)
            print(f"k={k} {name}: ray-model base {ray_model(base, g)} | ray-model +k {ray_model(base+[k], g)}")
            for d in (0.1, 0.001, 1e-5):
                print(f"   d={d}: page {{k-d,k,k+d}} ray-model {ray_model(base + [k - d, k, k + d], g)}"
                      f"  | {{k-d}} {ray_model(base + [k - d], g)} | {{k+d}} {ray_model(base + [k + d], g)}")
            print("   measure-model truth (dense+ray atom, recipe incl. k-1e-6,k,k+1e-6):",
                  measure_bounds(dense + [k - 1e-6, k, k + 1e-6], g))
    sys.stdout.flush()
