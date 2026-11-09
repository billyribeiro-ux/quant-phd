"""Round-21: compare the reported fraction of the r19_02 equivalent variant with the reference over the page's accuracy domain.

Also measures the variant's off-root gap error against the reference's Proposition 3 gap at a fixed interior fraction set,
to show the gap differs off the root (the README sweep measures only at the reported fractions).
Usage: python3 -I root_identity_r19_02_r21.py <reference.py> <variant.py>
"""
import importlib.util
import math
import sys


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


ref = load(sys.argv[1], "ref")
var = load(sys.argv[2], "var")
n = 0
max_root_diff = 0.0
worst = None
for i in range(200):
    sd = 10 ** (-50 + 52 * i / 199)
    for j in range(120):
        cost = 0.4 * j / 119
        t = 2.0 * math.exp(-4.0 * cost) - 1.0
        if t < 1e-2:
            continue
        a = ref.solve_model(sd, cost)["informed_fraction"]
        b = var.solve_model(sd, cost)["informed_fraction"]
        n += 1
        if a > 0.0:
            rel = abs(a - b) / a
        else:
            rel = abs(a - b)
        if rel > max_root_diff:
            max_root_diff, worst = rel, (sd, cost, a, b)
print("points", n, "max relative difference of reported fraction", f"{max_root_diff:.3e}", "at", worst)
off = []
for sd, cost in [(0.6, 0.13), (1e-2, 0.1), (0.5, 0.12)]:
    for lam in (0.1, 0.3, 0.5, 0.7):
        off.append(abs(var.indifference_gap(lam, sd, cost) - ref.indifference_gap(lam, sd, cost)))
print("off-root gap difference, max over (sd,cost,lam) probes", f"{max(off):.3e}")
