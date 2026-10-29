"""Check the reference QuantileSketch docstring invariants after every add: sum(g) == n and g + delta <= floor(2 eps n) + 1."""
import importlib.util, math, random, sys
from fractions import Fraction
spec = importlib.util.spec_from_file_location("impl", sys.argv[1]); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
bad_sum = bad_cap = 0; worst = None; checks = 0
for t in range(300):
    rng = random.Random(t)
    eps = rng.choice([0.05, 0.1, 0.2, 0.3])
    n = rng.randint(1, 300)
    sk = mod.QuantileSketch(eps)
    for i in range(n):
        x = rng.choice([round(rng.uniform(-5, 5), 1), float(rng.randint(0, 4))])
        sk.add(x)
        checks += 1
        if sum(sk._g) != sk._n:
            bad_sum += 1
        cap = math.floor(2 * Fraction(eps) * sk._n) + 1
        for g, d in zip(sk._g, sk._delta):
            if g + d > cap:
                bad_cap += 1
                if worst is None:
                    worst = (t, eps, sk._n, g, d, cap)
                break
print("checks", checks, "sum(g)!=n", bad_sum, "g+delta>cap", bad_cap, "first", worst)
