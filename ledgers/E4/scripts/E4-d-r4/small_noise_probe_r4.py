"""Small-noise probe (round 4): reference, absolute-tolerance mutant and alternatives 1 and 4 against Proposition 4.

Usage: python -I small_noise_probe_r4.py <repo-root>. Prints the informed fraction at c = 0.13 and its relative error.
"""

import importlib.util
import math
import sys
from pathlib import Path

root = Path(sys.argv[1])


def load(path: str, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, root / path)
    mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


mods = {
    "reference": load("course/modules/E/E4/grader/reference.py", "ref"),
    "mutant_absolute_tolerance": load("ledgers/E4/mutants/mutant_r4_absolute_bracket_tolerance.py", "mab"),
    "alt_1": load("ledgers/E4/alternatives/alt_1.py", "a1"),
    "alt_4": load("ledgers/E4/alternatives/alt_4.py", "a4"),
}


def closed(sd: float, c: float) -> float:
    t = 2.0 * math.exp(-4.0 * c) - 1.0
    return 2.0 * sd * math.sqrt(t / (1.0 - t))


for sd in (1e-6, 1e-9):
    exact = closed(sd, 0.13)
    print(f"sd {sd:g}: Proposition 4 closed form {exact:.10e}")
    for name, mod in mods.items():
        lam = mod.solve_model(sd, 0.13)["informed_fraction"]
        print(f"   {name:28s} {lam:.10e} relative error {abs(lam - exact) / exact:.2e}")
