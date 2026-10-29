"""Round-7 verifier script: (a) the rank-target example on project.html:219, (b) the infinite-value behaviour of the
reference classes that the Constraints rule (project.html:209) must cover.

Usage (from the checkout root): .venv/bin/python -I ledgers/CS2/scripts/CS2-d-r7/spec_probes_r7.py
"""

import math
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "course/modules/CS/CS2/grader"))
import reference as ref  # noqa: E402

print("float target :", math.ceil(0.1 * 20 - 0.05 * 20), "| exact target :", math.ceil(Fraction(0.1) * 20 - Fraction(0.05) * 20))
print("exact difference:", float(Fraction(0.1) * 20 - Fraction(0.05) * 20))

w = ref.RollingMinMax(3)
w.push(1.0)
w.push(float("inf"))
print("RollingMinMax.push(inf): no exception; maximum =", w.maximum())
s = ref.QuantileSketch(0.1)
s.add(1.0)
s.add(float("inf"))
print("QuantileSketch.add(inf): no exception; quantile(1.0) =", s.quantile(1.0))
acc = ref.WelfordAccumulator()
acc.update(1.0)
try:
    acc.update(float("inf"))
    print("WelfordAccumulator.update(inf): no exception; mean =", acc.mean(), "variance(1) =", acc.variance(1))
except ValueError as exc:
    print("WelfordAccumulator.update(inf) raises ValueError:", exc)
