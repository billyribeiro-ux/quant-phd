"""Round-15 seed sweep: L02 identity lines (dyadic count, grid-sup line) for seeds 0..299.

Loads the twin by path and calls its functions with a different SEED; checks that the two
identity lines are all-true for every seed. Usage: python3 -I seed_sweep_r15.py <checkout-root>
"""
import importlib.util
import io
import contextlib
import random
import sys

root = sys.argv[1]
spec = importlib.util.spec_from_file_location("l2", root + "/tests/labs/SC1/lab-SC1-L02-1.py")
mod = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(mod)
bad = []
for seed in range(300):
    rng = random.Random(seed)
    xi0 = rng.gauss(0.0, 1.0)
    coeffs = [[rng.gauss(0.0, 1.0) for _ in range(2 ** (m - 1))] for m in range(1, mod.LEVELS + 1)]
    fixed_cases = fixed_equal = 0
    for n in range(5):
        for k in range(2 ** n + 1):
            t = k / 2 ** n
            base = mod.partial_sum(xi0, coeffs, n, t)
            for levels in range(n, mod.LEVELS + 1):
                fixed_cases += 1
                fixed_equal += mod.partial_sum(xi0, coeffs, levels, t) == base
    grid = [i / 2 ** mod.GRID_DEPTH for i in range(2 ** mod.GRID_DEPTH + 1)]
    sup_agree = 0
    for m in range(1, mod.LEVELS + 1):
        scale = 2 ** (-(m + 1) / 2)
        grid_sup = max(abs(sum(coeffs[m - 1][j - 1] * mod.hat(m, j, t) for j in range(1, 2 ** (m - 1) + 1)) * scale)
                       for t in grid)
        sup_agree += grid_sup == mod.level_term_sup(coeffs[m - 1], m)
    if fixed_equal != 216 or fixed_cases != 216 or sup_agree != mod.LEVELS:
        bad.append((seed, fixed_equal, fixed_cases, sup_agree))
print(f"seeds 0..299: identity-line failures = {len(bad)}; first failures: {bad[:5]}")
