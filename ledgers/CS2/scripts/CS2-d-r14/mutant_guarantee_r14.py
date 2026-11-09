"""Rank-guarantee battery (the specification's two inequalities, exact counts) for the reference and for named
QuantileSketch mutants. Reports, per module, how many streams break the guarantee and one witness if any.

Usage: python -I mutant_guarantee_r14.py <module.py> [<module.py> ...]   (run from the checkout root)
"""

from __future__ import annotations

import importlib.util
import random
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def load(path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def streams(rng: random.Random):  # type: ignore[no-untyped-def]
    for trial in range(900):
        eps = rng.choice([0.05, 0.1, 0.2, 0.3, 0.5, 0.9])
        n = rng.randint(1, 400) if trial % 3 else rng.randint(1, 40)
        kind = trial % 6
        if kind == 0:
            xs = [round(rng.uniform(-5, 5), 1) for _ in range(n)]
        elif kind == 1:
            xs = sorted(round(rng.uniform(1e4, 1e4 + 10), 6) for _ in range(n))
        elif kind == 2:
            xs = [float(rng.randint(0, 4)) for _ in range(n)]
        elif kind == 3:
            xs = sorted((round(rng.uniform(-5, 5), 1) for _ in range(n)), reverse=True)
        elif kind == 4:
            xs = [7.0] * n
        else:
            xs = [rng.uniform(0, 1) for _ in range(n)]
        yield eps, xs


def main() -> None:
    for name in sys.argv[1:]:
        mod = load(Path(name).resolve())
        rng = random.Random(1414)
        broke = 0
        total = 0
        witness = None
        for eps, xs in streams(rng):
            sk = mod.QuantileSketch(eps)
            for x in xs:
                sk.add(x)
            n = len(xs)
            for q in [k / 100 for k in range(101)]:
                v = sk.quantile(q)
                below = sum(1 for x in xs if x < v)
                at_or_below = sum(1 for x in xs if x <= v)
                total += 1
                if not (below <= Fraction(q) * n + Fraction(eps) * n and at_or_below >= Fraction(q) * n - Fraction(eps) * n):
                    broke += 1
                    if witness is None:
                        witness = (eps, n, q, v, xs[:12])
        print(f"{Path(name).name}: {broke} of {total} checks break the guarantee; first witness: {witness}")


if __name__ == "__main__":
    main()
