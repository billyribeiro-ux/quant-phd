"""Difference set of each tie-rule equivalent file from the reference's _half_up, measured on the floats.

Candidates: every exact half k + 1/2 with |k| <= 2000, the 3 float neighbours on each side of each half, 200000 random
floats in [-3000, 3000], and the float 0.49999999999999994 (the largest float below 1/2). Usage (repo root):
.venv/bin/python -I ledgers/E3/scripts/fixer-d-r15/tie_difference_probe.py
"""

import importlib.util
import math
import random
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EQ = ROOT / "ledgers/E3/equivalent"
REF_PATH = ROOT / "course/modules/E/E3/grader/reference.py"


def load(path: Path, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load(REF_PATH, "ref_half")
files = {
    "f05": "f05_half_cent_goes_toward_minus_infinity.py",
    "m06": "m06_half_cent_rounded_to_even.py",
    "r13n01": "r13n01_half_cent_rounded_half_to_even.py",
    "w05": "w05_half_cent_away_from_zero.py",
}
mods = {k: load(EQ / v, k) for k, v in files.items()}

halves = [k + 0.5 for k in range(-2000, 2000)]
cands = set(halves)
for h in halves:
    x = h
    for _ in range(3):
        x = math.nextafter(x, math.inf)
        cands.add(x)
    x = h
    for _ in range(3):
        x = math.nextafter(x, -math.inf)
        cands.add(x)
rng = random.Random(15)
cands.update(rng.uniform(-3000, 3000) for _ in range(200000))
cands.add(0.49999999999999994)
cands.add(-0.49999999999999994)

for name, mod in mods.items():
    diffs = [y for y in cands if mod._half_up(y) != ref._half_up(y)]
    exact_halves = [y for y in diffs if Fraction(y) - math.floor(Fraction(y)) == Fraction(1, 2)]
    non_half = [y for y in diffs if Fraction(y) - math.floor(Fraction(y)) != Fraction(1, 2)]
    neg = sum(1 for y in exact_halves if y < 0)
    pos = len(exact_halves) - neg
    print(
        f"{name}: differs on {len(diffs)} candidate floats; exact halves {len(exact_halves)} (negative {neg}, "
        f"non-negative {pos}); off-half differences {len(non_half)} {sorted(non_half)[:5]}"
    )

for y in (0.49999999999999994, -0.49999999999999994):
    print("y =", repr(y), "reference", ref._half_up(y), {k: m._half_up(y) for k, m in mods.items()})
print("candidates", len(cands), "halves", len(halves))
