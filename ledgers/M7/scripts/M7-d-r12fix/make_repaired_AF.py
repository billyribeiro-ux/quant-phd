"""Repair alternatives A, C, D, E, F (round 10): one step of iterative refinement on the KKT solve.

Usage: python -I make_repaired_AF.py <repo_root>
Writes <repo_root>/ledgers/M7/scripts/M7-d-r12fix/alts_repaired/alt_<X>_r12fix_<name>.py. Only the _kkt_step return is
changed; the cutoffs, the rank test and the active-set rule of each original are kept.
"""

import sys
from pathlib import Path

root = Path(sys.argv[1])
src_dir = root / "ledgers/M7/scripts/M7-d-r10/alts"
out_dir = root / "ledgers/M7/scripts/M7-d-r12fix/alts_repaired"
OLD = "    solution = _solve_linear(matrix, [-g for g in gradient] + [Fraction(0)] * m)\n    return solution[:n], solution[n:]\n"
NEW = (
    "    rhs = [-g for g in gradient] + [Fraction(0)] * m\n"
    "    solution = _solve_linear(matrix, rhs)\n"
    "    # One step of iterative refinement: the KKT matrix mixes O(1) constraint rows with O(gamma) Hessian rows, so the\n"
    "    # first solve can leave a residual above the cutoffs when gamma is small (round-12 finding PRJ-R10-02).\n"
    "    residual = [rhs[r] - sum(matrix[r][c] * solution[c] for c in range(size)) for r in range(size)]\n"
    "    correction = _solve_linear(matrix, residual)\n"
    "    solution = [s + c for s, c in zip(solution, correction, strict=True)]\n"
    "    return solution[:n], solution[n:]\n"
)
out_dir.mkdir(parents=True, exist_ok=True)
for src in sorted(src_dir.glob("alt_[ACDEF]_*.py")):
    text = src.read_text(encoding="utf-8")
    assert text.count(OLD) == 1, src.name
    letter = src.name.split("_")[1]
    rest = "_".join(src.stem.split("_")[2:])
    out = out_dir / f"alt_{letter}_r12fix_{rest}_refined.py"
    out.write_text(text.replace(OLD, NEW), encoding="utf-8")
    print(out.name)
