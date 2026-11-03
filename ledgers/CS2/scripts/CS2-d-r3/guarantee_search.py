"""Search for rank-guarantee violations of a QuantileSketch module (exact counts, Fraction epsilon and q).

Usage: python -I guarantee_search.py <module.py> <trials> <seed>
Streams: random length 1-40 with heavy ties and repeated maxima; epsilon in {0.05, 0.1, 0.2}; probes q = k/40 and
q = k/100 for k in 0..100. Prints the first violating (stream, eps, q) found and the counts, or 'no violation'.
"""

import importlib.util
import random
import sys
from fractions import Fraction
from pathlib import Path

path = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("cand", path)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
trials = int(sys.argv[2])
rng = random.Random(int(sys.argv[3]))
PROBES = sorted({Fraction(k, 40) for k in range(41)} | {Fraction(k, 100) for k in range(101)})
violations = 0
first = None
checked = 0
for t in range(trials):
    n = rng.randint(1, 40)
    eps_f = rng.choice([0.05, 0.1, 0.2])
    kind = rng.random()
    if kind < 0.4:
        stream = [float(rng.randint(0, 6)) for _ in range(n)]
    elif kind < 0.7:
        base = [float(rng.randint(0, 6)) for _ in range(n)]
        m = max(base)
        stream = [m if rng.random() < 0.5 else b for b in base]
    else:
        stream = [round(rng.uniform(0, 1), 1) for _ in range(n)]
    sk = mod.QuantileSketch(eps_f)
    for i, x in enumerate(stream):
        sk.add(x)
        if rng.random() < 0.15 or i == n - 1:
            prefix = stream[: i + 1]
            m_ = len(prefix)
            for q in PROBES:
                v = sk.quantile(float(q))
                below = sum(1 for y in prefix if y < v)
                at_or_below = sum(1 for y in prefix if y <= v)
                checked += 1
                e = Fraction(eps_f)
                if not (below <= q * m_ + e * m_ and at_or_below >= q * m_ - e * m_):
                    violations += 1
                    if first is None:
                        first = (prefix, eps_f, float(q), v, below, at_or_below)
print(f"{path.name}: checked {checked} (prefix, probe) pairs, violations {violations}")
if first:
    print("first violation:", first)
