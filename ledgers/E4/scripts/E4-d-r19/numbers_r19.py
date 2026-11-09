"""Round 19 (E4-d): re-derive the page's numbers and the test docstrings' numbers with plain floats and Decimal.

Run from the checkout root: python -I ledgers/E4/scripts/E4-d-r19/numbers_r19.py  (needs solver on sys.path via SOLVER_DIR)
"""

import math
import os
import sys
from decimal import Decimal, localcontext

SOLVER_DIR = os.environ["SOLVER_DIR"]
sys.path.insert(0, SOLVER_DIR)
import solver as ref  # noqa: E402  (the reference copied as solver.py)

print("== spec box bounds (project.html Inputs; instance.py docstring)")
print("tau_bar(0.150) =", f"{2 * math.exp(-4 * 0.150) - 1:.10f}")
print("tau_bar(0.120) =", f"{2 * math.exp(-4 * 0.120) - 1:.10f}")
print("tau_y(1) at sd 0.75 =", f"{1 / (1 + 4 * 0.75**2):.10f}")
print("2^-240 =", f"{2.0**-240:.6e}", " 2^-200 =", f"{2.0**-200:.6e}")

print("== Lab 1: width after k halvings of [0,1] (first k with width 2^-k reaching fp resolution)")
low, high = 0.0, 1.0
A, TAU_V, TAU_E, SD, COST = 2.0, 1.0, 1.0, 0.60, 0.13
def ty_(lam):
    return lam * lam * TAU_E * TAU_E / (lam * lam * TAU_E + A * A * SD * SD)
def bs_bu(lam):
    ty = ty_(lam)
    den = lam * (TAU_V + TAU_E) + (1.0 - lam) * (TAU_V + ty)
    bs = (lam * TAU_E + (1.0 - lam) * ty) / den
    return bs, -A * bs / (lam * TAU_E)
def g1(lam):
    ty = ty_(lam)
    bs, bu = bs_bu(lam)
    r = ty / (TAU_V + ty) - bs
    fu = math.pow(1.0 + r * r * (TAU_V + ty) * (1.0 / TAU_V + 1.0 / ty), -0.5)
    prec = TAU_V + TAU_E
    slope = TAU_E / prec - bs
    vg = slope * slope * (1.0 / TAU_V + 1.0 / TAU_E) + bu * bu * SD * SD
    fi = math.pow(1.0 + prec * vg, -0.5)
    return fu - math.exp(A * COST) * fi
first_change = None
for k in range(1, 61):
    mid = 0.5 * (low + high)
    if g1(mid) > 0.0:
        low = mid
    else:
        high = mid
    w = high - low
    if k in (52, 53, 54, 55) or k == 60:
        print(f"halving {k}: width {w:.6e}  is_2^-k {w == 2.0**-k}")
print("final width", f"{high - low:.3e}", "lam*", f"{0.5*(low+high):.8f}")

print("== test docstring: gap at fraction 1e-12 vs limit, and oracle vs limit (six inputs)")
import importlib.util  # noqa: E402
import test_project as tp  # noqa: E402  (loads solver and instance from SOLVER_DIR)

for sd, cost in [(0.5, 0.30), (0.6, 0.30), (0.75, 0.30), (0.5, 0.50), (0.6, 0.50), (0.75, 0.50)]:
    lim = ref.gap_at_zero(sd, cost)
    g_small = ref.indifference_gap(1e-12, sd, cost)
    o0 = tp.oracle_gap(0.0, sd, cost)
    print(f"sd {sd} c {cost}: |gap(1e-12)-limit| = {abs(g_small - lim):.3e}; |oracle(0)-limit| = {abs(o0 - lim):.3e}; "
          f"limit = {lim:+.6e}; tol = {1e-14 * max(1.0, abs(lim)):.1e}")

print("== test_gap_at_the_domain_point: root, gap, exact Prop 3 gap")
sd, cost = 3.3245979322709314e-22, 0.059130434782608696
out = ref.solve_model(sd, cost)
lam = out["informed_fraction"]
ex = float(tp.prop3_gap_exact(lam, sd, cost))
print("root", f"{lam:.6e}", "reported gap", f"{out['indifference_gap']:+.6e}", "exact gap", f"{ex:+.6e}",
      "|diff|", f"{abs(out['indifference_gap'] - ex):.3e}", "tol", f"{1e-14 * max(1.0, abs(ex)):.1e}")

print("== accuracy corner: 200 halvings width vs 1e-10 * root")
root = tp.closed_form_root(1e-50, 0.1707691121)
print("root", f"{root:.6e}", "tau_bar", f"{2*math.exp(-4*0.1707691121)-1:.8f}", "1e-10*root", f"{1e-10*root:.3e}",
      "2^-200", f"{2.0**-200:.3e}", "2^-240", f"{2.0**-240:.3e}")

print("== extreme inputs inside the stated range (sd up to 1e150, cost up to 350) and tiny sd")
for sd_, c_ in [(1e150, 350.0), (1e150, 0.0), (1e-50, 350.0), (1e-50, 0.0), (1e-50, 0.1707691121), (1.0, 350.0),
                (1e150, 0.13), (1e-300, 0.13)]:
    try:
        o = ref.solve_model(sd_, c_)
        print(sd_, c_, {k: v for k, v in o.items()})
    except Exception as e:  # noqa: BLE001
        print(sd_, c_, "RAISES", type(e).__name__, e)
