"""Find a short stream, with repeated maximum, on which the skip-repeat-of-maximum sketch (d4_02) breaks the rank
guarantee at one of the nine fixed probes of the grader, for epsilon 0.05, 0.1, 0.2, while the reference holds.
Usage: python -I witness_repeat_max.py <d4_02 module> <reference module>"""

import importlib.util
import itertools
import sys
from fractions import Fraction
from pathlib import Path


def load(p: str, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, Path(p).resolve())
    assert spec and spec.loader
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


bad_mod = load(sys.argv[1], "bad")
ref_mod = load(sys.argv[2], "ref")
PROBES = [0.0, 0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 1.0]


def ok(mod, stream, eps, q):  # type: ignore[no-untyped-def]
    sk = mod.QuantileSketch(eps)
    for x in stream:
        sk.add(x)
    v = sk.quantile(q)
    n = len(stream)
    below = sum(1 for y in stream if y < v)
    at = sum(1 for y in stream if y <= v)
    return below <= Fraction(q) * n + Fraction(eps) * n and at >= Fraction(q) * n - Fraction(eps) * n


found = []
for n in range(3, 13):
    for eps in (0.05, 0.1, 0.2):
        for vals in itertools.product((0, 1, 2), repeat=n):
            if vals.count(2) < 2 or vals[-1] != 2:
                continue
            stream = [float(v) for v in vals]
            for q in PROBES:
                if not ok(bad_mod, stream, eps, q) and ok(ref_mod, stream, eps, q):
                    found.append((n, eps, q, stream))
                    break
            if found:
                break
        if found:
            break
    if found:
        break
print("first witness (n, eps, q, stream):", found[0] if found else "none up to n=12")
