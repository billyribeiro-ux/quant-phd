"""Check the reference QuantileSketch docstring claims after every add: sum of g = n; g + delta <= floor(2 eps n) + 1;
for each stored value some copy has exact 1-based rank in [running sum of g, running sum of g + delta].
Usage: python -I invariant_check.py <reference.py>"""
import importlib.util, random, sys
from fractions import Fraction
from pathlib import Path
spec = importlib.util.spec_from_file_location("ref", Path(sys.argv[1]).resolve())
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
rng = random.Random(3)
checks = bad_sum = bad_band = bad_rank = 0
for trial in range(400):
    eps = rng.choice([0.05, 0.1, 0.2, 0.3, 0.45])
    n = rng.randint(1, 120)
    stream = [rng.choice([round(rng.uniform(0, 5), 1), float(rng.randint(0, 3))]) for _ in range(n)]
    sk = mod.QuantileSketch(eps)
    seen = []
    for x in stream:
        sk.add(x)
        seen.append(x)
        m = len(seen)
        checks += 1
        if sum(sk._g) != m:
            bad_sum += 1
        cap = int(Fraction(2 * eps) * m) + 1  # floor(2 eps n) + 1
        if any(g + d > cap for g, d in zip(sk._g, sk._delta)):
            bad_band += 1
        srt = sorted(seen)
        run = 0
        for v, g, d in zip(sk._values, sk._g, sk._delta):
            run += g
            lo, hi = run, run + d
            copies = [p + 1 for p, y in enumerate(srt) if y == v]
            if not any(lo <= p <= hi for p in copies):
                bad_rank += 1
                break
print(f"{Path(sys.argv[1]).name}: states={checks} sum_g_mismatch={bad_sum} band_violation={bad_band} rank_claim_violation={bad_rank}")
