import sys, random
from fractions import Fraction
sys.path.insert(0, sys.argv[1])
import l04_module_r5 as m
rng = random.Random(m.SEED)
kinds = ("shift", "equal-mean", "random")
pairs = []
while len(pairs) < m.N_PAIRS:
    kind = kinds[len(pairs) % 3]
    px = m.draw_pmf(rng)
    if kind == "shift":
        py = m.shift_up(px, rng)
    elif kind == "equal-mean":
        py = m.match_mean(m.draw_pmf(rng), m.mean(px))
    else:
        py = m.draw_pmf(rng)
    if py is not None:
        pairs.append((kind, px, py))
def dens(p):
    from math import lcm
    d = 1
    for q in p:
        d = lcm(d, q.denominator)
    return d
from collections import Counter
print("pairs:", len(pairs), Counter(k for k, _, _ in pairs))
for kind in kinds:
    ds = Counter(dens(py) for k, _, py in pairs if k == kind)
    dx = Counter(dens(px) for k, px, _ in pairs)
    print(f"{kind}: denominators of second lottery {dict(ds)}; first lottery denominators {dict(dx)}")
for n, (k, px, py) in enumerate(pairs):
    if k == "equal-mean" or n in (16, 19):
        pass
eqm = [(n, k, px, py) for n, (k, px, py) in enumerate(pairs) if m.mean(px) == m.mean(py)]
print("equal-mean pair indices:", [n for n, *_ in eqm])
for n, k, px, py in eqm:
    print(n, m.sosd_cdf_verdict(px, py))
print("pair 16:", m.describe(pairs[16][1]), "|", m.describe(pairs[16][2]))
print("pair 19:", m.describe(pairs[19][1]), "|", m.describe(pairs[19][2]))
print("max denominators of mean-matched second lotteries:", max(dens(py) for k, _, py in pairs if k == "equal-mean"))
# verify that the FOSD-ranked pairs' integrated order holds, and count
fos = Counter(m.fosd_cdf_verdict(px, py) for _, px, py in pairs)
print("FOSD:", dict(fos))
