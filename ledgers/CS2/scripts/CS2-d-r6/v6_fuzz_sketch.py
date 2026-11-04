"""Round-6 fuzz of the rank guarantee (VERIFIER_RULES 2.6 / Conventions) for QuantileSketch variants.
usage: python -I v6_fuzz_sketch.py <module-file> [more module files]
Random streams of 1-60 values with heavy ties, epsilon in {0.05, 0.1, 0.2, 0.3, 0.5, 0.9}, probes k/40 plus random q.
Every add is followed by a check of both inequalities at every probe, using exact Fractions."""

import importlib.util
import math
import random
import sys
from fractions import Fraction


def load(path):
    spec = importlib.util.spec_from_file_location("m_" + str(abs(hash(path))), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.QuantileSketch


def check(stream, sketch_cls, eps):
    sk = sketch_cls(eps)
    seen = []
    probes = [k / 40 for k in range(41)] + [random.random() for _ in range(3)]
    for x in stream:
        sk.add(x)
        seen.append(x)
        n = len(seen)
        for q in probes:
            v = sk.quantile(q)
            qn = Fraction(q) * n
            ee = Fraction(eps) * n
            below = sum(1 for y in seen if y < v)
            at = sum(1 for y in seen if y <= v)
            if not (below <= qn + ee and at >= qn - ee):
                return (n, q, v, below, at)
    return None


def main():
    random.seed(20261104)
    classes = {p: load(p) for p in sys.argv[1:]}
    fails = {p: 0 for p in classes}
    trials = 0
    for t in range(200):
        length = random.randint(1, 60)
        base = random.choice([0.0, 10000.0, 1e6])
        if random.random() < 0.5:
            stream = [base + random.randint(-4, 4) / 2 for _ in range(length)]  # heavy ties
        else:
            stream = [base + round(random.uniform(-5, 5), random.choice([1, 6])) for _ in range(length)]
        if random.random() < 0.2:
            stream.sort(reverse=random.random() < 0.5)
        eps = random.choice([0.05, 0.1, 0.2, 0.3, 0.5, 0.9])
        trials += 1
        for p, cls in classes.items():
            bad = check(stream, cls, eps)
            if bad:
                fails[p] += 1
                if fails[p] <= 2:
                    print("COUNTEREXAMPLE", p, "eps", eps, "n,q,v,below,at", bad)
    print("trials", trials)
    for p in classes:
        print("violating streams:", fails[p], "|", p)


main()
