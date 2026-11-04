# ruff: noqa: E501
"""Round-5 witness: the surviving mutant r5v_01 and the reference on the two-value stream [1.0, 2.0], q = 1.0.

Prints each answer, the two rank counts and the two bounds, with exact Fractions. Run with argv[1] = module path, argv[2] = epsilon.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction

spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
eps_text = sys.argv[2]
eps = Fraction(eps_text)
stream = [1.0, 2.0]
sk = mod.QuantileSketch(float(eps_text))
for x in stream:
    sk.add(x)
q = Fraction(1)
n = len(stream)
v = sk.quantile(float(q))
below = sum(1 for y in stream if y < v)
at_or_below = sum(1 for y in stream if y <= v)
print(
    f"module={sys.argv[1].split('/')[-1]} eps={eps_text} answer={v} strictly_below={below} (<= {float(q * n + eps * n)})"
    f" at_or_below={at_or_below} (>= {float(q * n - eps * n)})"
    f" ok={below <= q * n + eps * n and at_or_below >= q * n - eps * n}"
)
