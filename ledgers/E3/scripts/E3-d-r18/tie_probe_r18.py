"""Verifier probe (round 18): difference set of the four tie-rule equivalents against the pinned reference's _half_up.

Usage (repo root): .venv/bin/python -I ledgers/E3/scripts/E3-d-r18/tie_probe_r18.py
Loads each file as a module (no pytest), compares _half_up on a candidate set, and reports where each differs and
whether every difference is an exact half. Candidates: every k + 1/2 for k in [-2000, 2000), the three floats on each side
of each half, 200,000 random floats in [-3000, 3000] (fixed seed), and the two floats nearest to 1/2 in absolute value.
"""

import importlib.util
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path.cwd()


def load(path: Path, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load(ROOT / "course/modules/E/E3/grader/reference.py", "ref_r18")
files = {
    "f05": ROOT / "ledgers/E3/equivalent/f05_half_cent_goes_toward_minus_infinity.py",
    "m06": ROOT / "ledgers/E3/equivalent/m06_half_cent_rounded_to_even.py",
    "r13n01": ROOT / "ledgers/E3/equivalent/r13n01_half_cent_rounded_half_to_even.py",
    "w05": ROOT / "ledgers/E3/equivalent/w05_half_cent_away_from_zero.py",
}
mods = {k: load(p, "mut_" + k) for k, p in files.items()}

cands: list[float] = []
for k in range(-2000, 2000):
    h = k + 0.5
    cands.append(h)
    x = h
    for _ in range(3):
        x = math.nextafter(x, math.inf)
        cands.append(x)
    x = h
    for _ in range(3):
        x = math.nextafter(x, -math.inf)
        cands.append(x)
rng = random.Random(18)
cands += [rng.uniform(-3000, 3000) for _ in range(200_000)]
cands += [math.nextafter(0.5, 0.0), 0.5]
cands += [0.49999999999999994, -0.49999999999999994]

cands = sorted(set(cands))
print("distinct candidates", len(cands))
print("reference _half_up at 0.49999999999999994 =", ref._half_up(0.49999999999999994))
print("old reference floor(y+0.5) at 0.49999999999999994 =", math.floor(0.49999999999999994 + 0.5))
for name, mod in mods.items():
    diff = [y for y in cands if mod._half_up(y) != ref._half_up(y)]
    non_half = [y for y in diff if Fraction(y) - math.floor(Fraction(y)) != Fraction(1, 2)]
    print(f"{name}: differs on {len(diff)} candidates; non-exact-half differences {len(non_half)}")
    if diff:
        print("   sample", diff[:3])

# Nearest-cent property of the reference at every candidate that is not an exact half
bad = [y for y in cands if abs(ref._half_up(y) - Fraction(y)) > Fraction(1, 2)]
print("reference not within 1/2 of y:", len(bad))
