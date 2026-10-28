"""Verifier M5-d round 2: witness for the tie test and the alternative residual-stop solver.

Runs the grader reference and ledgers/M5/alternatives/alt2_residual_stop.py on the tie-test parameters
(beta 0.5, alpha 0.5, grid [0.75, 1.0]), then on the proposed fix (tol taken from the solver's own first certified
error). Usage: .venv/bin/python -I ledgers/M5/scripts/M5-d-r2/tie_witness_r2.py
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[4]


def load(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    ref = load(ROOT / "course/modules/M/M5/grader/reference.py")
    alt2 = load(ROOT / "ledgers/M5/alternatives/alt2_residual_stop.py")
    p = {"beta": 0.5, "alpha": 0.5}
    grid = [0.75, 1.0]
    print("tie test as written (tol = 0.5 = the page-formula certified error after sweep 1):")
    for name, m in (("reference", ref), ("alt2", alt2)):
        print(" ", name, m.solve(p, grid, 0.5, 1000))
    print("proposed fix (tol = the solver's own certified error after one sweep):")
    for name, m in (("reference", ref), ("alt2", alt2)):
        first = m.solve(p, grid, 1e-12, 1)["certified_error"]
        out = m.solve(p, grid, first, 1000)
        print(" ", name, "tol", first, "iterations", out["iterations"], "converged", out["converged"])


if __name__ == "__main__":
    main()
