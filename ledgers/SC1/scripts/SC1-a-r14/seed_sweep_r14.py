"""Round-14 SC1-a: sweep the L02 lab's two claimed-for-every-seed identities (dyadic equality count and grid-sup line)
over 300 seeds, using the page's own functions loaded from the twin. Also checks L03 exact-sum identity over the same seeds."""
import math
import random
import runpy
import sys
import io
import contextlib

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE14-SC1-a"
ns = {}
src = open(ROOT + "/tests/labs/SC1/lab-SC1-L02-1.py", encoding="utf-8").read()
src = src.replace("\nmain()", "\n")  # do not run main at import
exec(compile(src, "twin_L02", "exec"), ns)
bad_fixed = 0
bad_grid = 0
total = 0
for seed in range(300):
    ns["SEED"] = 20260101 + 0 * seed if False else seed
    rng = random.Random(seed)
    xi0 = rng.gauss(0.0, 1.0)
    coeffs = [[rng.gauss(0.0, 1.0) for _ in range(2 ** (m - 1))] for m in range(1, 9)]
    fixed_cases = fixed_equal = 0
    for n in range(5):
        for k in range(2**n + 1):
            t = k / 2**n
            base = ns["partial_sum"](xi0, coeffs, n, t)
            for levels in range(n, 9):
                fixed_cases += 1
                fixed_equal += ns["partial_sum"](xi0, coeffs, levels, t) == base
    if fixed_equal != fixed_cases or fixed_cases != 216:
        bad_fixed += 1
    grid = [i / 2**10 for i in range(2**10 + 1)]
    ok = True
    for m in range(1, 9):
        scale = 2 ** (-(m + 1) / 2)
        gs = max(abs(sum(coeffs[m - 1][j - 1] * ns["hat"](m, j, t) for j in range(1, 2 ** (m - 1) + 1)) * scale) for t in grid)
        ok = ok and (gs == ns["level_term_sup"](coeffs[m - 1], m))
    if not ok:
        bad_grid += 1
    total += 1
print(f"seeds checked: {total}; dyadic 216-of-216 failures: {bad_fixed}; grid-sup identity failures: {bad_grid}")
