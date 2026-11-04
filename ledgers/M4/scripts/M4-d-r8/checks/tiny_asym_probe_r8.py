"""Probe: a covariance of order 1e-14 whose off-diagonal entries differ (not symmetric) must raise ValueError.

Runs the reference and the round-8 absolute-tolerance mutant on the same inputs and prints what each returns or raises.
Usage: python -I ledgers/M4/scripts/M4-d-r8/checks/tiny_asym_probe_r8.py
"""

import importlib.util
import pathlib

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD8-M4-d")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CASES = {
    "tiny_asymmetric_1e-15": [[1e-14, 1e-15], [2e-15, 9e-14]],
    "scale_1e-5_asymmetric_1e-6": [[4e-4, 1e-4], [1e-4 + 1e-6, 9e-4]],
}
for label, path in [
    ("reference", ROOT / "course/modules/M/M4/grader/reference.py"),
    ("r8d_01 mutant", ROOT / "ledgers/M4/mutants/r8d_01_symmetry_checked_to_absolute_tolerance_1e9.py"),
]:
    mod = load(path, label.replace(" ", "_"))
    for name, cov in CASES.items():
        try:
            out = mod.simulate_losses([1_000_000, 1_000_000], cov, 10, 0, "gaussian", None)
            print(f"{label:14s} {name}: returned {len(out)} losses (accepted)")
        except ValueError as exc:
            print(f"{label:14s} {name}: ValueError: {exc}")
