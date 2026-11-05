"""Probe the page's exception-table scope claim and the 200-halving claim against the reference solver.

Run: python3 -I probe_scope_r9.py <path-to-reference.py>
"""
import importlib.util
import math
import sys

spec = importlib.util.spec_from_file_location("ref", sys.argv[1])
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)

keys = {"informed_fraction", "price_informativeness", "indifference_gap"}
bad = []
n = 0
for sd in [1e-300, 1e-200, 1e-100, 1e-30, 1e-12, 0.5, 1.0, 2.0, 10.0, 1e3, 1e10, 1e50, 1e100, 1e150]:
    for cost in [0.0, 1e-9, 0.13, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0, 200.0, 350.0]:
        n += 1
        try:
            out = ref.solve_model(sd, cost)
        except Exception as err:  # noqa: BLE001 - probe
            bad.append((sd, cost, f"raised {type(err).__name__}: {err}"))
            continue
        ok = set(out) == keys and all(isinstance(v, float) for v in out.values())
        ok = ok and all(math.isfinite(v) for v in out.values())
        ok = ok and 0.0 <= out["informed_fraction"] <= 1.0 and 0.0 <= out["price_informativeness"] <= 1.0
        if not ok:
            bad.append((sd, cost, out))
print(f"scope grid: {n} points, {len(bad)} not valid")
for b in bad[:20]:
    print("  ", b)
# Outside the stated range: which inputs fail?
for sd, cost in [(1e154, 0.13), (1.5e154, 0.13), (1e160, 0.13), (1.0, 355.0), (1.0, 360.0), (1.0, 1e6)]:
    try:
        out = ref.solve_model(sd, cost)
        print(f"outside: sd={sd:g} cost={cost:g} -> {out}")
    except Exception as err:  # noqa: BLE001
        print(f"outside: sd={sd:g} cost={cost:g} -> raised {type(err).__name__}: {err}")
# 200-halving claim: for roots r, does the tolerance limb fire before 200 halvings?
def halvings_and_width(root):
    # emulate the reference's loop on the bracket [0, 1] with a sign change at 'root'
    low, high = 0.0, 1.0
    steps = 0
    while high - low > ref.BISECTION_TOLERANCE * high and steps < ref.MAX_BISECTION_STEPS:
        mid = 0.5 * (low + high)
        if mid < root:
            low = mid
        else:
            high = mid
        steps += 1
    tol_hit = high - low <= ref.BISECTION_TOLERANCE * high
    return steps, tol_hit, 0.5 * (low + high), high - low

print("200-halving claim: roots near the threshold")
for r in [1e-48, 6.5e-49, 6.3e-49, 6.2e-49, 6.0e-49, 5e-49, 1e-49, 1e-50, 1e-60]:
    steps, tol_hit, lam, width = halvings_and_width(r)
    print(f"  root {r:.3g}: steps {steps}, tolerance limb fired {tol_hit}, |lam - root|/root = {abs(lam - r) / r:.3g}, width {width:.3g}")
