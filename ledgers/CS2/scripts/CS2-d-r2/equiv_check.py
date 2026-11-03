"""Compare two QuantileSketch modules output-for-output on exhaustive short streams and random streams.

Usage: python -I equiv_check.py <reference.py> <candidate.py>. Prints the counts of compared queries and of differences."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


def load(path: str, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, Path(path).resolve())
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load(sys.argv[1], "ref_mod")
cand = load(sys.argv[2], "cand_mod")
EPS = [0.01, 0.05, 0.1, 0.2, 0.3, 0.45, 0.7, 0.999]
QS = [k / 40 for k in range(41)] + [1e-300, 0.1, 0.25, 0.5, 0.9, 0.999999, 1 - 2**-53]
compared = 0
diffs = 0


def compare(stream: list[float], eps: float) -> None:
    global compared, diffs
    a = ref.QuantileSketch(eps)
    b = cand.QuantileSketch(eps)
    for x in stream:
        a.add(x)
        b.add(x)
        for q in QS:
            compared += 1
            if a.quantile(q) != b.quantile(q):
                diffs += 1
                if diffs <= 3:
                    print("DIFF", eps, stream, q, a.quantile(q), b.quantile(q))
                return


for length in range(1, 7):
    for combo in itertools.product([0.0, 1.0, 2.0], repeat=length):
        for eps in EPS:
            compare(list(combo), eps)
rng = random.Random(5)
for _ in range(120):
    n = rng.randint(1, 60)
    stream = [round(rng.uniform(-3, 3), rng.choice([0, 1, 6])) for _ in range(n)]
    compare(stream, rng.choice(EPS))
print(f"{Path(sys.argv[2]).name} vs reference: queries compared={compared} differences={diffs}")
