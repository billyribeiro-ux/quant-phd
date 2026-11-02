"""Verifier round-1: m11 (loss sign flipped) equals a conforming implementation that draws -Z, for every seed tested.

Prints, for seeds 0-9, whether the mutant's losses equal the negated-normal variant's losses (Student-t and Gaussian families).
Run from the checkout root: .venv/bin/python -I ledgers/M4/scripts/M4-d-r1/verifyD1_sign_equivalence.py
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def load(path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    mutant = load(ROOT / "ledgers/M4/mutants/m11_loss_sign_flipped.py")
    negated = load(ROOT / "ledgers/M4/scripts/M4-d-r1/verifyD1_alt_negated_normals.py")
    positions = [3_000_000, 2_000_000]
    cov = [[4e-4, 1e-4], [1e-4, 9e-4]]
    for family, nu in (("student_t", 5), ("gaussian", None)):
        same = all(
            mutant.simulate_losses(positions, cov, 2000, s, family, nu) == negated.simulate_losses(positions, cov, 2000, s, family, nu)
            for s in range(10)
        )
        print(f"{family}: mutant m11 losses == negated-normal conforming variant, seeds 0-9: {same}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
