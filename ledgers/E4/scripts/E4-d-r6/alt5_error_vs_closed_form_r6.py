"""Relative error of the informed fraction against the closed form of Proposition 4, for the reference, alt_5 and the two
spec-compliant variants, on random interior inputs. Usage: python -I alt5_error_vs_closed_form_r6.py <checkout-root>."""

from __future__ import annotations

import importlib.util
import math
import random
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()


def load(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def closed(sd: float, cost: float) -> float:
    t = 2 * math.exp(-4 * cost) - 1
    if t <= 0.0:
        return 0.0
    if t >= 1.0 / (1.0 + 4 * sd * sd):
        return 1.0
    return 2 * sd * math.sqrt(t / (1 - t))


mods = {
    "reference": load("r_ref6", root / "course/modules/E/E4/grader/reference.py"),
    "alt_5": load("r_alt5", root / "ledgers/E4/alternatives/alt_5.py"),
    "mutant_08": load("r_m08", root / "ledgers/E4/equivalent/mutant_r6_08_bracket_reports_lower_end.py"),
    "mutant_09": load("r_m09", root / "ledgers/E4/equivalent/mutant_r6_09_stop_rule_never_relative.py"),
}
rng = random.Random(11)
cases = []
while len(cases) < 4000:
    sd = 10 ** rng.uniform(-12, math.log10(5.0))
    cost = rng.uniform(0.0, 0.4)
    c = closed(sd, cost)
    if 0.0 < c < 1.0:
        cases.append((sd, cost, c))
for name, mod in mods.items():
    worst = 0.0
    for sd, cost, c in cases:
        lam = mod.solve_model(sd, cost)["informed_fraction"]  # type: ignore[attr-defined]
        worst = max(worst, abs(lam - c) / c)
    print(f"{name}: worst relative error vs closed form over {len(cases)} interior inputs = {worst:.3e}")
